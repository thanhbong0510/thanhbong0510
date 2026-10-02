@echo off
REM Cai dat 1 lan cho Windows 10/11 + card NVIDIA GTX 10xx tro len
cd /d "%~dp0"

where ffmpeg >nul 2>nul || winget install -e --id Gyan.FFmpeg

py -3.11 -m venv venv 2>nul || python -m venv venv
call venv\Scripts\activate.bat
python -m pip install --upgrade pip

REM PyTorch ban CUDA 12.6: van ho tro card Pascal (GTX 1070), ban moi hon thi khong
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
pip install -r requirements.txt

python -c "import torch; print('GPU OK:', torch.cuda.get_device_name(0)) if torch.cuda.is_available() else print('KHONG THAY GPU - kiem tra driver NVIDIA')"
echo.
echo Cai dat xong. Neu ffmpeg vua duoc cai, hay dong cua so nay va mo lai.
pause
