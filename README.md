# YouTube Speech-to-Text Transcriber

Paste a YouTube link, download the audio, and transcribe it locally with Whisper.
This project runs offline after the dependencies and model are installed. No API key is required.

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
├── webapp/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── results/
├── whisper_transcribe.py
├── download_and_transcribe.bat
├── webapp/启动服务.bat
└── .gitignore
```

## Requirements

- Python 3.10 or 3.11
- `ffmpeg`
- `yt-dlp.exe` in the project root
- Python packages:
  - `flask`
  - `openai-whisper`
  - `torch`

## Installation

### 1. Install Python

Make sure Python is installed and available on PATH:

```bash
python --version
```

### 2. Download yt-dlp.exe

Download the latest `yt-dlp.exe` from the official releases page and place it in the project root.

### 3. Install ffmpeg

Install `ffmpeg` with `winget` or manually add it to PATH.

### 4. Install dependencies

```bash
pip install flask
pip install openai-whisper
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

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

## Output

Transcripts are saved under `webapp/results/` as:

- `result.json`
- `transcript.txt`

## Notes

- For Chinese audio, `medium` or `large-v3` usually gives better accuracy.
- The first run may take a while because Whisper downloads the model to the local cache.

## License

MIT

