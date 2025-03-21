@echo off
chcp 65001 > nul
echo 正在启动关键词检测程序...
echo.

:: 检查Python是否已安装
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未检测到Python，请安装Python 3.6或更高版本后重试。
    echo 您可以从 https://www.python.org/downloads/ 下载Python。
    echo.
    pause
    exit /b 1
)

:: 安装依赖
echo 正在安装必要的依赖项...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 安装依赖失败，请检查网络连接或手动运行：pip install -r requirements.txt
    pause
    exit /b 1
)

echo 依赖安装完成！
echo.

echo 正在启动程序...
echo 提示：程序启动后，请在浏览器中完成登录操作，然后再点击弹出窗口中的"确定"按钮继续。
echo.

:: 运行程序
python sx.py

pause