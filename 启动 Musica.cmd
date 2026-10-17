@echo off
chcp 65001 >nul
cd /d "%~dp0"
if exist "releases\Musica-Windows-x64-v0.2.0\Musica.exe" (
    start "" "releases\Musica-Windows-x64-v0.2.0\Musica.exe"
    exit /b
)
if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" "run.py"
    exit /b
)
echo 未找到发行程序。请解压完整的 Windows 发行包后运行 Musica.exe。
pause
