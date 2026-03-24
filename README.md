# YouTube Speech-to-Text Transcriber

Paste a YouTube link, and this tool automatically downloads the audio and transcribes it using a local Whisper model — results are displayed in a clean web interface. **Runs entirely offline. No API key required. No cloud AI calls.**

---

## Features

- One-click processing from a YouTube URL
- Real-time progress display (Download → Transcribe → Save)
- Timestamped transcript output (`[00:12 → 00:18]` format)
- Supports all Whisper model sizes (tiny / base / small / medium / large)
- Auto language detection or manual language selection
- History saved automatically — revisit any past result
- Embedded YouTube player for side-by-side playback and transcript review

---

## Project Structure

```
youtube-transcriber/
├── yt-dlp.exe                  # YouTube downloader (download manually, see Step 2)
├── webapp/
│   ├── app.py                  # Flask backend
│   ├── 启动服务.bat             # Windows launcher script
│   ├── templates/
│   │   └── index.html          # Frontend page
│   └── results/                # Transcript output directory (auto-created)
├── whisper_transcribe.py       # Standalone CLI transcription script
├── download_and_transcribe.bat # CLI all-in-one batch script
├── ocr_batch.py                # Batch image OCR script
├── pdf_extract.py              # PDF text extraction script
└── .gitignore
```

---

## Installation

### Step 1 — Install Python

1. Go to https://www.python.org/downloads/
2. Download **Python 3.10 or 3.11** (3.11 recommended)
3. Run the installer — **check "Add Python to PATH"** before clicking Install Now
4. After installation, open Command Prompt (Win + R → type `cmd` → Enter) and verify:
   ```
   python --version
   ```
   You should see a version number like `Python 3.11.x`.

---

### Step 2 — Download yt-dlp.exe

1. Go to https://github.com/yt-dlp/yt-dlp/releases/latest
2. Download `yt-dlp.exe`
3. Place `yt-dlp.exe` in the project root directory (same level as the `webapp/` folder)

---

### Step 3 — Install ffmpeg

Whisper requires ffmpeg to process audio files.

**Option A: Install via winget (recommended — built into Windows 10/11)**

Open Command Prompt and run:
```
winget install --id Gyan.FFmpeg -e --source winget
```
After installation, **close and reopen** Command Prompt, then verify:
```
ffmpeg -version
```

**Option B: Manual installation**

1. Go to https://www.gyan.dev/ffmpeg/builds/
2. Download `ffmpeg-release-essentials.zip`
3. Extract it to `C:\ffmpeg\`
4. Add `C:\ffmpeg\bin` to your system PATH:
   - Right-click "This PC" → Properties → Advanced system settings → Environment Variables
   - Under "System variables", find `Path` → double-click → New → enter `C:\ffmpeg\bin`
   - Click OK, then reopen Command Prompt and verify with `ffmpeg -version`

---

### Step 4 — Install Python Dependencies

Open Command Prompt and run the following commands one by one:

```
pip install flask
pip install openai-whisper
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

> **Notes:**
> - `flask` — lightweight web framework for the UI
> - `openai-whisper` — local speech recognition model (runs fully offline)
> - `torch` — required by Whisper; the command above installs the CPU-only version (~200 MB)
>
> **If you have an NVIDIA GPU**, install the GPU version of torch for 5–10× faster transcription:
> ```
> pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
> ```
> *(cu121 = CUDA 12.1 — choose the version matching your GPU driver)*

---

### Step 5 — Whisper Model (Auto-downloaded on First Run)

On first use, Whisper automatically downloads the model file to your local cache  
(`C:\Users\YourName\.cache\whisper\`). **This only happens once.**

Model size and speed comparison:

| Model | Size | Speed | Best For |
|-------|------|-------|----------|
| tiny | 75 MB | Fastest | Quick tests |
| base | 142 MB | Fast | English content |
| small | 466 MB | Medium | General use |
| **medium** | **1.4 GB** | **Slow** | **Chinese recommended** |
| large | 2.9 GB | Slowest | Highest accuracy |

> For Chinese or other non-English videos, **medium** or **large** is strongly recommended. tiny/base have noticeably lower accuracy on non-English audio.

---

## Starting the Web App

Once everything is installed, you have two options:

**Option A: Double-click the batch file**

Double-click `webapp\启动服务.bat` in the project folder.

**Option B: Command line**

```
cd webapp
python app.py
```

Then open your browser and visit:

```
http://127.0.0.1:5000
```

---

## How to Use

1. Paste a YouTube video URL into the input box
2. Select a Whisper model (medium recommended for Chinese)
3. Select the language (`zh` for Chinese, `auto` to detect automatically)
4. Click **Start**
5. Wait for all three steps to complete (roughly 1–3× the video duration, depending on your hardware)
6. View the timestamped transcript and download the result

---

## Troubleshooting

**Q: `ffmpeg not found` error**  
A: ffmpeg was not added to PATH correctly. Revisit Step 3, then close and reopen Command Prompt.

**Q: First run is very slow / stuck on "Loading model"**  
A: Whisper is downloading the model file in the background (medium = ~1.4 GB). Wait for it to finish — subsequent runs will start immediately.

**Q: Transcription is very slow**  
A: On CPU, the medium model takes roughly 2–4 hours for a 1-hour video. Installing the GPU version of torch (see Step 4) significantly reduces this.

**Q: Poor accuracy on Chinese audio**  
A: Try a larger model (medium → large) or explicitly set the language to `zh`.

**Q: `pip install` fails or times out**  
A: Try using a mirror:
```
pip install flask -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install openai-whisper -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## Changelog

| Version | Date | Notes |
|---------|------|-------|
| v1.0 | 2026-03-24 | Initial release — web UI, real-time progress, history |

---

## License

MIT License — free to use, modify, and distribute.
