@echo off
REM Cai dat 1 lan cho Windows 10/11 + card NVIDIA GTX 10xx tro len
cd /d "%~dp0"

REM --- Tim Python 3.10 / 3.11 / 3.12 (3.13, 3.14 qua moi, thu vien chua ho tro) ---
set "PY="
py -3.11 --version >nul 2>nul && set "PY=py -3.11"
if not defined PY py -3.12 --version >nul 2>nul && set "PY=py -3.12"
if not defined PY py -3.10 --version >nul 2>nul && set "PY=py -3.10"
if not defined PY (
  echo.
  echo [LOI] Khong tim thay Python 3.11.
  echo Python 3.13 / 3.14 qua moi, chua chay duoc numpy va Kokoro.
  echo.
  echo Cach sua: mo cmd va go lenh:   py install 3.11
  echo Hoac tai ban cai: https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
  echo Sau do chay lai file nay.
  pause
  exit /b 1
)
echo Dung Python:
%PY% --version

REM --- Xoa venv cu neu duoc tao bang Python sai phien ban ---
if exist venv\Scripts\python.exe (
  venv\Scripts\python.exe -c "import sys; sys.exit(0 if (3,10) <= sys.version_info[:2] <= (3,12) else 1)" || rmdir /s /q venv
) else (
  if exist venv rmdir /s /q venv
)
if not exist venv (
  %PY% -m venv venv || goto :fail
)
set "VPY=venv\Scripts\python.exe"

REM --- ffmpeg ---
where ffmpeg >nul 2>nul || winget install -e --id Gyan.FFmpeg --accept-source-agreements --accept-package-agreements

%VPY% -m pip install --upgrade pip || goto :fail

REM PyTorch ban CUDA 12.6: van ho tro card Pascal (GTX 1070), ban moi hon thi khong
%VPY% -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126 || goto :fail
%VPY% -m pip install -r requirements.txt || goto :fail

echo.
%VPY% -c "import torch; print('GPU OK:', torch.cuda.get_device_name(0)) if torch.cuda.is_available() else print('KHONG THAY GPU - kiem tra driver NVIDIA')"
echo.
echo Cai dat xong. Hay dong TAT CA cua so cmd roi mo lai truoc khi chay run.bat
pause
exit /b 0

:fail
echo.
echo [LOI] Cai dat bi loi o buoc ben tren. Chup man hinh gui lai de duoc ho tro.
pause
exit /b 1
