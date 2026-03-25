"""
YouTube speech-to-text web app.
Dependencies: flask, openai-whisper, yt-dlp.exe
"""

from __future__ import annotations

import json
import subprocess
import threading
import uuid
from pathlib import Path

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).parent
YTDLP = BASE_DIR.parent / "yt-dlp.exe"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
JOBS: dict[str, dict] = {}


def fmt_time(seconds: float) -> str:
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"


def fmt_duration(seconds: float) -> str:
    hours, rem = divmod(int(seconds), 3600)
    minutes, secs = divmod(rem, 60)
    return f"{hours}h{minutes:02d}m{secs:02d}s" if hours else f"{minutes}m{secs:02d}s"


def job_log(job: dict, msg: str) -> None:
    job["log"].append(msg)
    print(msg)


def run_job(job_id: str, url: str, model_name: str, lang: str) -> None:
    job = JOBS[job_id]
    job["status"] = "running"
    job["step_download"] = "running"
    job["step_whisper"] = "pending"
    job["step_doc"] = "pending"

    work_dir = RESULTS_DIR / job_id
    work_dir.mkdir(exist_ok=True)
    wav_path = work_dir / "audio.wav"

    job_log(job, "⬇️  Starting audio download...")
    cmd = [
        str(YTDLP),
        "-x",
        "--audio-format",
        "wav",
        "--audio-quality",
        "0",
        "--no-playlist",
        "--print",
        "title",
        "--print",
        "duration",
        "-o",
        str(work_dir / "audio.%(ext)s"),
        url,
    ]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        output_lines = (proc.stdout or "").strip().splitlines()
        title = output_lines[0] if len(output_lines) > 0 else url
        duration = float(output_lines[1]) if len(output_lines) > 1 else 0
        job["title"] = title
        job["duration"] = fmt_duration(duration)
        job_log(job, f"✅ Title: {title}")
        job_log(job, f"⏱️ Duration: {fmt_duration(duration)}")
        if not wav_path.exists():
            raise FileNotFoundError(f"Audio file not generated: {wav_path}")
    except Exception as exc:
        job["step_download"] = "error"
        job["status"] = "error"
        job["error"] = str(exc)
        job_log(job, f"❌ Download failed: {exc}")
        return

    job["step_download"] = "done"
    job["step_whisper"] = "running"
    job_log(job, "🎙️ Starting Whisper transcription...")

    try:
        import whisper

        job_log(job, f"   Loading model: {model_name}")
        model = whisper.load_model(model_name)
        lang_arg = None if lang == "auto" else lang
        job_log(job, "   Transcribing... please wait.")
        result = model.transcribe(str(wav_path), language=lang_arg, verbose=False)
        segments = [
            {
                "start": fmt_time(seg["start"]),
                "end": fmt_time(seg["end"]),
                "text": seg["text"].strip(),
            }
            for seg in result["segments"]
        ]
        full_text = result["text"]
        job_log(job, f"✅ Transcription complete, {len(segments)} segments")
    except Exception as exc:
        job["step_whisper"] = "error"
        job["status"] = "error"
        job["error"] = str(exc)
        job_log(job, f"❌ Transcription failed: {exc}")
        return

    job["step_whisper"] = "done"
    job["step_doc"] = "running"
    job_log(job, "📄 Generating structured output...")

    try:
        result_data = {
            "job_id": job_id,
            "url": url,
            "title": job["title"],
            "duration": job["duration"],
            "model": model_name,
            "segments": segments,
            "full_text": full_text,
        }

        with open(work_dir / "result.json", "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)

        with open(work_dir / "transcript.txt", "w", encoding="utf-8") as f:
            f.write(f"《{job['title']}》语音转写\n")
            f.write("=" * 60 + "\n\n")
            for seg in segments:
                f.write(f"[{seg['start']} → {seg['end']}] {seg['text']}\n")
            f.write("\n" + "=" * 60 + "\n【纯文字版】\n\n")
            f.write(full_text)

        job["result"] = result_data
        job["step_doc"] = "done"
        job["status"] = "done"
        job_log(job, "🎉 All done. Results saved.")
    except Exception as exc:
        job["step_doc"] = "error"
        job["status"] = "error"
        job["error"] = str(exc)
        job_log(job, f"❌ Save failed: {exc}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/start", methods=["POST"])
def api_start():
    data = request.get_json(force=True)
    url = data.get("url", "").strip()
    model = data.get("model", "medium")
    lang = data.get("lang", "zh")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    job_id = str(uuid.uuid4())[:8]
    JOBS[job_id] = {
        "id": job_id,
        "url": url,
        "status": "queued",
        "step_download": "pending",
        "step_whisper": "pending",
        "step_doc": "pending",
        "log": [],
        "log_sent": 0,
        "title": "",
        "duration": "",
        "result": None,
        "error": None,
    }
    threading.Thread(target=run_job, args=(job_id, url, model, lang), daemon=True).start()
    return jsonify({"job_id": job_id})


@app.route("/api/status/<job_id>")
def api_status(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    sent = job["log_sent"]
    new_logs = job["log"][sent:]
    job["log_sent"] = len(job["log"])

    return jsonify(
        {
            "status": job["status"],
            "step_download": job["step_download"],
            "step_whisper": job["step_whisper"],
            "step_doc": job["step_doc"],
            "log_new": new_logs,
            "result": job["result"],
            "error": job["error"],
        }
    )


@app.route("/api/result/<job_id>")
def api_result(job_id: str):
    job = JOBS.get(job_id)
    if job and job.get("result"):
        return jsonify({"result": job["result"]})

    result_file = RESULTS_DIR / job_id / "result.json"
    if result_file.exists():
        with open(result_file, encoding="utf-8") as f:
            return jsonify({"result": json.load(f)})

    return jsonify({"error": "Result not found"}), 404


if __name__ == "__main__":
    print("Service ready: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)
