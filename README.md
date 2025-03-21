# 关键词检测程序

## 程序介绍

这是一个基于Selenium的自动化检测工具，用于监控特定网页中是否出现"生产"或"质检"关键词。当检测到关键词时，程序会弹出提醒窗口通知用户。

## 功能特点

- 自动登录目标网站（需要用户手动完成登录操作）
- 定期检查目标页面内容
- 检测到"生产"或"质检"关键词时弹出提醒窗口
- 自动处理错误并继续运行
- 每分钟自动刷新检测一次

## 使用方法

### 快速启动

1. 双击 `启动程序.bat` 文件
2. 系统将自动安装所需依赖并启动程序
3. 在打开的浏览器中完成登录操作
4. 点击弹出窗口中的"确定"按钮继续运行程序

### 手动安装与运行

如果您希望手动安装和运行程序，请按照以下步骤操作：

1. 确保已安装Python 3.6或更高版本
2. 打开命令提示符，进入程序所在目录
3. 运行 `pip install -r requirements.txt` 安装依赖
4. 运行 `python sx.py` 启动程序

## 系统要求

- Windows操作系统
- Python 3.6+
- Google Chrome浏览器
- 网络连接

## 注意事项

- 程序运行期间请勿关闭浏览器窗口
- 如需停止程序，请按Ctrl+C或关闭命令提示符窗口
- 首次运行时会自动下载ChromeDriver，请确保网络连接正常