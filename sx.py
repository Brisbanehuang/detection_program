from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import tkinter as tk
from tkinter import messagebox
import os
import sys
import re

def get_chrome_driver():
    try:
        # 自动下载和管理 ChromeDriver
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        service.log_path = 'NUL'
        
        options = Options()
        options.add_argument('--log-level=3')  # 设置日志级别为错误
        options.add_argument('--disable-extensions')  # 禁用扩展
        options.add_argument('--incognito')  # 启用无痕模式
        
        # 尝试创建 WebDriver
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        show_alert(f"启动失败：请确保已安装 Google Chrome 浏览器\n错误信息：{str(e)}")
        sys.exit(1)

def show_alert(message):
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    alert = tk.Toplevel()
    alert.title('提醒')
    alert.geometry("300x150+500+300")  # 设置窗口大小和位置
    alert.attributes('-topmost', True)  # 置顶窗口
    alert.grab_set()  # 模态窗口
    
    label = tk.Label(alert, text=message, font=("Helvetica", 14))
    label.pack(pady=20)
    
    ok_button = tk.Button(alert, text="确定", command=alert.destroy)
    ok_button.pack(pady=10)
    
    alert.wait_window()  # 等待窗口关闭

def show_login_prompt():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    alert = tk.Toplevel()
    alert.title('登录提示')
    alert.geometry("300x150+500+300")  # 设置窗口大小和位置
    alert.attributes('-topmost', True)  # 置顶窗口
    alert.grab_set()  # 模态窗口
    
    label = tk.Label(alert, text="请在浏览器中完成登录，然后点击确定继续", font=("Helvetica", 14), wraplength=250)
    label.pack(pady=20)
    
    ok_button = tk.Button(alert, text="确定", command=alert.destroy)
    ok_button.pack(pady=10)
    
    alert.wait_window()  # 等待窗口关闭

# 删除 create_status_window 函数

def main():
    # 初始化 WebDriver
    driver = get_chrome_driver()
    
    # 登录页面URL
    login_url = 'https://merchant-staff.tuxiaodui.com/login'
    target_url = 'https://merchant-staff.tuxiaodui.com/task'
    
    try:
        # 打开登录页面
        driver.get(login_url)
        show_login_prompt()
        
        # 主循环
        while True:
            try:
                driver.get(target_url)
                time.sleep(5)
                
                visible_text = driver.execute_script("return document.documentElement.innerText;")
                
                # 检测关键词
                if '生产' in visible_text:
                    show_alert('检测到"生产"关键词！')
                elif '质检' in visible_text:
                    show_alert('检测到"质检"关键词！')
                
                # 检测"我的"后面是否有数字
                pattern = r'我的\s*\d+'
                matches = re.search(pattern, visible_text)
                if matches:
                    show_alert('检测到"驳回"的任务！')
                
            except Exception as e:
                # 出错时静默等待，不显示状态
                time.sleep(60)
            
            time.sleep(60)
    except KeyboardInterrupt:
        show_alert("程序已停止")
    except Exception as e:
        show_alert(f"程序发生错误：{str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()