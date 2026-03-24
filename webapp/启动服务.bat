@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ========================================
echo  视频语音转文字工具  http://127.0.0.1:5000
echo ========================================
echo.
echo 正在启动服务，请稍候...
start "" "http://127.0.0.1:5000"
python app.py
pause
