@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo  YouTube Speech-to-Text Transcriber
echo ========================================
echo.
echo This script assumes yt-dlp.exe is in the project root.
echo

set /p VIDEO_URL=Paste YouTube URL: 
if "%VIDEO_URL%"=="" (
    echo No URL provided.
    pause
    exit /b 1
)

if not exist "视频" mkdir "视频"

echo.
echo ========================================
echo  Step 1: Download audio
echo ========================================
.\yt-dlp.exe -x --audio-format wav --audio-quality 0 ^
  -o "视频\%%(title)s.%%(ext)s" ^
  "%VIDEO_URL%"

echo.
echo ========================================
echo  Step 2: Find the latest WAV file
echo ========================================
for /f "delims=" %%F in ('dir /b /o-d "视频\*.wav" 2^>nul') do (
    set "WAVFILE=视频\%%F"
    goto :found
)
echo No WAV file found.
pause
exit /b 1

:found
echo Found audio file: %WAVFILE%

echo.
echo ========================================
echo  Step 3: Whisper transcription
echo ========================================
python whisper_transcribe.py "%WAVFILE%" --model medium --lang zh

echo.
echo ========================================
echo  Done
echo ========================================
pause
