# YouTube Speech-to-Text Transcriber

Paste a YouTube link, download the audio, and transcribe it locally with Whisper.
This project runs offline after the dependencies and model are installed. No API key is required.

## Quick Start

1. Install Python 3.10 or 3.11.
2. Create and activate a virtual environment.
3. Run `pip install -r requirements.txt`.
4. Install `ffmpeg`.
5. Download `yt-dlp.exe` and place it in the project root.
6. Start the app with `cd webapp` and `python app.py`.
7. Open `http://127.0.0.1:5000` in your browser.

## Features

- Paste a YouTube URL and start transcription
- Live progress updates for download, transcription, and save steps
- Timestamped transcript output
- Whisper model selection
- Automatic or manual language selection
- Local history in the browser
- Embedded YouTube preview

## Project Structure

```text
youtube-transcriber/
|-- webapp/
|   |-- app.py
|   |-- templates/
|   |   `-- index.html
|   `-- results/
|-- whisper_transcribe.py
|-- download_and_transcribe.bat
|-- webapp/启动服务.bat
`-- .gitignore
```

## Requirements

- Python 3.10 or 3.11
- `ffmpeg`
- `yt-dlp.exe` in the project root
- Python packages listed in `requirements.txt`

## Installation

### 1. Install Python

Make sure Python is installed and available on PATH:

```bash
python --version
```

### 2. Create a virtual environment

From the project root:

```bash
python -m venv .venv
.venv\Scripts\activate
```

If you prefer PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install everything in one step:

```bash
pip install -r requirements.txt
```

### 4. Install ffmpeg

Install `ffmpeg` with `winget` or manually add it to PATH:

```bash
winget install --id Gyan.FFmpeg -e --source winget
```

Verify it works:

```bash
ffmpeg -version
```

### 5. Download yt-dlp.exe

Download the latest `yt-dlp.exe` from the official releases page and place it in the project root:

https://github.com/yt-dlp/yt-dlp/releases/latest

### 6. First run model download

Whisper downloads the selected model on first use and stores it in the local cache.

## Run the web app

```bash
cd webapp
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## CLI mode

You can also use `whisper_transcribe.py` or `download_and_transcribe.bat` for a direct command-line workflow.

### CLI example

```bash
python whisper_transcribe.py "C:\path\to\audio.wav" --model medium --lang zh
```

### Batch example

Double-click `download_and_transcribe.bat`, paste a YouTube URL, and follow the prompts.

## Why this is a good portfolio project

- It solves a real workflow problem end to end.
- It shows practical Python, Flask, and local automation skills.
- It demonstrates product thinking through a usable UI, history tracking, and structured output.
- It is easy to explain in interviews because the goal is clear and the result is visible.

## Output

Transcripts are saved under `webapp/results/` as:

- `result.json`
- `transcript.txt`

## Notes

- For Chinese audio, `medium` or `large-v3` usually gives better accuracy.
- The first run may take a while because Whisper downloads the model to the local cache.
- If you have an NVIDIA GPU, you can swap the CPU-only PyTorch install for a CUDA build.
- If you want a faster first demo, start with `base` or `small`.

## License

MIT
