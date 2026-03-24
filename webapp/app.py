"""
视频语音转文字 Web 应用
依赖: flask, openai-whisper, yt-dlp（exe）
"""
import os, sys, json, uuid, threading, time, subprocess
from pathlib import Path
from flask import Flask, request, jsonify, render_template

BASE_DIR   = Path(__file__).parent
YTDLP      = BASE_DIR.parent / 'yt-dlp.exe'
AUDIO_DIR  = BASE_DIR / 'results'
AUDIO_DIR.mkdir(exist_ok=True)

app  = Flask(__name__)
JOBS = {}   # job_id -> job dict

# ─────────────────────────────────────────
def fmt_time(seconds):
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"

def fmt_duration(seconds):
    h, rem = divmod(int(seconds), 3600)
    m, s   = divmod(rem, 60)
    return f"{h}h{m:02d}m{s:02d}s" if h else f"{m}m{s:02d}s"

def job_log(job, msg):
    job['log'].append(msg)
    print(msg)

def run_job(job_id, url, model_name, lang):
    job = JOBS[job_id]
    job['status']        = 'running'
    job['step_download'] = 'running'
    job['step_whisper']  = 'pending'
    job['step_doc']      = 'pending'

    work_dir = AUDIO_DIR / job_id
    work_dir.mkdir(exist_ok=True)
    wav_path = work_dir / 'audio.wav'

    # ── 步骤1: yt-dlp 下载音频 ────────────────────
    job_log(job, '⬇️  开始下载音频...')
    cmd = [
        str(YTDLP),
        '-x', '--audio-format', 'wav', '--audio-quality', '0',
        '--no-playlist',
        '--print', 'title',
        '--print', 'duration',
        '-o', str(work_dir / 'audio.%(ext)s'),
        url
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        output_lines = (proc.stdout or '').strip().splitlines()
        title    = output_lines[0] if len(output_lines) > 0 else url
        duration = float(output_lines[1]) if len(output_lines) > 1 else 0
        job['title']    = title
        job['duration'] = fmt_duration(duration)
        job_log(job, f'✅  标题: {title}')
        job_log(job, f'⏱️  时长: {fmt_duration(duration)}')
        if not wav_path.exists():
            raise FileNotFoundError(f'音频文件未生成: {wav_path}')
    except Exception as e:
        job['step_download'] = 'error'
        job['status']        = 'error'
        job['error']         = str(e)
        job_log(job, f'❌  下载失败: {e}')
        return

    job['step_download'] = 'done'
    job['step_whisper']  = 'running'
    job_log(job, '🎙️  开始 Whisper 转录...')

    # ── 步骤2: Whisper 转录 ───────────────────────
    try:
        import whisper
        import numpy as np
        job_log(job, f'   加载模型: {model_name}')
        model  = whisper.load_model(model_name)
        lang_  = None if lang == 'auto' else lang
        job_log(job, '   转录中，请耐心等待...')
        result = model.transcribe(str(wav_path), language=lang_, verbose=False)
        segments = [
            {
                'start': fmt_time(s['start']),
                'end':   fmt_time(s['end']),
                'text':  s['text'].strip()
            }
            for s in result['segments']
        ]
        full_text = result['text']
        job_log(job, f'✅  转录完成，共 {len(segments)} 段')
    except Exception as e:
        job['step_whisper'] = 'error'
        job['status']       = 'error'
        job['error']        = str(e)
        job_log(job, f'❌  转录失败: {e}')
        return

    job['step_whisper'] = 'done'
    job['step_doc']     = 'running'
    job_log(job, '📄  生成结构化文档...')

    # ── 步骤3: 保存结果 ────────────────────────────
    try:
        result_data = {
            'job_id':    job_id,
            'url':       url,
            'title':     job['title'],
            'duration':  job['duration'],
            'model':     model_name,
            'segments':  segments,
            'full_text': full_text,
        }
        # 保存 JSON
        with open(work_dir / 'result.json', 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        # 保存 TXT
        with open(work_dir / 'transcript.txt', 'w', encoding='utf-8') as f:
            f.write(f'《{job["title"]}》语音转录\n')
            f.write('=' * 60 + '\n\n')
            for s in segments:
                f.write(f'[{s["start"]} → {s["end"]}] {s["text"]}\n')
            f.write('\n' + '=' * 60 + '\n【纯文字版】\n\n')
            f.write(full_text)

        job['result']   = result_data
        job['step_doc'] = 'done'
        job['status']   = 'done'
        job_log(job, f'🎉  全部完成！结果已保存')
    except Exception as e:
        job['step_doc'] = 'error'
        job['status']   = 'error'
        job['error']    = str(e)
        job_log(job, f'❌  保存失败: {e}')

# ─────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def api_start():
    data  = request.get_json()
    url   = data.get('url', '').strip()
    model = data.get('model', 'medium')
    lang  = data.get('lang', 'zh')
    if not url:
        return jsonify({'error': 'URL 为空'}), 400

    job_id = str(uuid.uuid4())[:8]
    JOBS[job_id] = {
        'id':            job_id,
        'url':           url,
        'status':        'queued',
        'step_download': 'pending',
        'step_whisper':  'pending',
        'step_doc':      'pending',
        'log':           [],
        'log_sent':      0,
        'title':         '',
        'duration':      '',
        'result':        None,
        'error':         None,
    }
    t = threading.Thread(target=run_job, args=(job_id, url, model, lang), daemon=True)
    t.start()
    return jsonify({'job_id': job_id})

@app.route('/api/status/<job_id>')
def api_status(job_id):
    job = JOBS.get(job_id)
    if not job:
        return jsonify({'error': '任务不存在'}), 404

    sent     = job['log_sent']
    new_logs = job['log'][sent:]
    job['log_sent'] = len(job['log'])

    return jsonify({
        'status':        job['status'],
        'step_download': job['step_download'],
        'step_whisper':  job['step_whisper'],
        'step_doc':      job['step_doc'],
        'log_new':       new_logs,
        'result':        job['result'],
        'error':         job['error'],
    })

@app.route('/api/result/<job_id>')
def api_result(job_id):
    # 优先从内存取，否则从磁盘读
    job = JOBS.get(job_id)
    if job and job.get('result'):
        return jsonify({'result': job['result']})
    result_file = AUDIO_DIR / job_id / 'result.json'
    if result_file.exists():
        with open(result_file, encoding='utf-8') as f:
            return jsonify({'result': json.load(f)})
    return jsonify({'error': '结果不存在'}), 404

if __name__ == '__main__':
    print('启动服务: http://127.0.0.1:5000')
    app.run(host='0.0.0.0', port=5000, debug=False)
