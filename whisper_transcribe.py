from __future__ import annotations

import argparse
from pathlib import Path

import whisper


def fmt_time(seconds: float) -> str:
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes:02d}:{secs:02d}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Transcribe a local WAV file with Whisper.")
    parser.add_argument("wav", help="Path to the WAV file")
    parser.add_argument("--model", default="medium", help="Whisper model name")
    parser.add_argument("--lang", default="zh", help="Language code, or auto")
    parser.add_argument("--out", default=None, help="Output transcript path")
    args = parser.parse_args()

    wav = Path(args.wav)
    out = Path(args.out) if args.out else wav.with_name(wav.stem + "_transcript.txt")

    print(f"Loading Whisper model: {args.model}")
    model = whisper.load_model(args.model)

    print("Transcribing...")
    lang = None if args.lang == "auto" else args.lang
    result = model.transcribe(str(wav), language=lang, verbose=True)

    with open(out, "w", encoding="utf-8") as f:
        f.write(f"《{wav.stem}》视频语音转文字\n")
        f.write(f"输入文件: {wav}\n")
        f.write("=" * 60 + "\n\n")
        for seg in result["segments"]:
            start = fmt_time(seg["start"])
            end = fmt_time(seg["end"])
            text = seg["text"].strip()
            f.write(f"[{start} --> {end}] {text}\n")
        f.write("\n" + "=" * 60 + "\n【纯文字版】\n\n")
        f.write(result["text"])

    print(f"\nDone. Output: {out}")


if __name__ == "__main__":
    main()
