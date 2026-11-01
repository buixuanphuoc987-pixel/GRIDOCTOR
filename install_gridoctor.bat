@echo off
cd /d "%~dp0"

echo ========================================
echo        CAI DAT GRIDOCTOR
echo ========================================
echo.

echo Dang kiem tra Python...
python --version

if errorlevel 1 (
    echo.
    echo LOI: May chua cai Python hoac Python chua duoc them vao PATH.
    echo Hay cai Python truoc khi tiep tuc.
    echo.
    pause
    exit /b
)

echo.
echo Dang nang cap pip...
python -m pip install --upgrade pip

echo.
echo Dang cai cac thu vien can thiet...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ========================================
    echo CAI DAT KHONG THANH CONG
    echo ========================================
    echo Kiem tra ket noi Internet va thu lai.
    pause
    exit /b
)

echo.
echo ========================================
echo       CAI DAT THANH CONG
echo ========================================
echo.
echo Bay gio hay chay:
echo run_gridoctor.bat
echo.

pause