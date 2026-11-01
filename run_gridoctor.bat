@echo off
cd /d "%~dp0"

echo ========================================
echo          DANG KHOI DONG GRIDOCTOR
echo ========================================
echo.

python -m streamlit run app.py

echo.
echo GRIDOCTOR da dung.
pause