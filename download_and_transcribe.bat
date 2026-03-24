@echo off
chcp 65001 >nul
cd /d "C:\Users\james\OneDrive\桌面\油管视频处理"

echo ========================================
echo  步骤 1: 下载音频（最佳音质）
echo ========================================
.\yt-dlp.exe -x --audio-format wav --audio-quality 0 ^
  -o "视频\%(title)s.%%(ext)s" ^
  "https://www.youtube.com/watch?v=7BtVrfUe0QY"

echo.
echo ========================================
echo  步骤 2: 查找刚下载的 wav 文件
echo ========================================
for /f "delims=" %%F in ('dir /b /o-d "视频\*.wav" 2^>nul') do (
    set WAVFILE=视频\%%F
    goto :found
)
echo 未找到 wav 文件，退出。
pause
exit /b 1

:found
echo 找到音频文件: %WAVFILE%

echo.
echo ========================================
echo  步骤 3: Whisper 转文字（medium 中文模型）
echo ========================================
python -c "
import whisper, os, sys
wav = r'%WAVFILE%'
print('加载 Whisper medium 模型（首次运行会下载约1.4GB）...')
model = whisper.load_model('medium')
print('开始转录...')
result = model.transcribe(wav, language='zh', verbose=True)
out = wav.replace('.wav', '_transcript.txt')
with open(out, 'w', encoding='utf-8') as f:
    f.write(result['text'])
print()
print('转录完成！输出文件:', out)
"

echo.
echo ========================================
echo  全部完成！
echo ========================================
pause
