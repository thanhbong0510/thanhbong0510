@echo off
REM Vi du: run.bat scenes.json --out paperclip.mp4
cd /d "%~dp0"
call venv\Scripts\activate.bat
python make_video.py %*
pause
