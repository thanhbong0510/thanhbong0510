@echo off
REM Vi du: run.bat scenes.json --out paperclip.mp4
cd /d "%~dp0"
if not exist venv\Scripts\python.exe (
  echo [LOI] Chua cai dat. Hay chay install_windows.bat truoc.
  pause
  exit /b 1
)
venv\Scripts\python.exe make_video.py %*
pause
