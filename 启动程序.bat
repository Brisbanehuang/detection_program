@echo off
setlocal enabledelayedexpansion
chcp 65001 > nul
echo [INFO] Starting program...
echo.

:: 检查Python是否已安装
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.6 or higher.
    echo Download from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: 先尝试直接运行程序
echo [INFO] Launching program...
echo [NOTE] After program starts, please complete login in browser.
echo.

python sx.py
if %errorlevel% equ 0 (
    echo [SUCCESS] Program ran successfully!
    pause
    exit /b 0
)

:: 如果运行失败，尝试安装依赖
echo [INFO] Program launch failed, installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies. Please check network or run manually: pip install -r requirements.txt
    pause
    exit /b 1
)

echo [SUCCESS] Dependencies installed! Restarting program...
python sx.py

pause