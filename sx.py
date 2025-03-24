from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import tkinter as tk
from tkinter import messagebox, IntVar, Checkbutton, Frame, Label, Button
import os
import sys
import re
import threading

# 全局变量，用于控制监控选项
monitor_settings = {
    "production": True,  # 监控"生产"
    "quality": True,     # 监控"质检"
    "rejected": True     # 监控"驳回任务"
}

# 全局变量，用于控制程序运行
running = True

# 图标文件路径
ICON_PATH = "icon.ico"

# 字体设置
FONT_FAMILY = "Microsoft YaHei"  # 微软雅黑
FONT_TITLE = (FONT_FAMILY, 14, "bold")  # 标题字体
FONT_NORMAL = (FONT_FAMILY, 12)         # 正常字体
FONT_SMALL = (FONT_FAMILY, 10)          # 小字体

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
        options.add_argument('--disable-gpu')  # 禁用GPU加速
        options.add_argument('--disable-software-rasterizer')  # 禁用软件光栅化器
        options.add_argument('--disable-dev-shm-usage')  # 禁用/dev/shm使用
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 禁用日志输出
        
        # 重定向控制台输出
        if sys.platform == 'win32':
            devnull = open('NUL', 'w')
        else:
            devnull = open('/dev/null', 'w')
        sys.stdout = devnull
        
        # 尝试创建 WebDriver
        driver = webdriver.Chrome(service=service, options=options)
        
        # 恢复标准输出
        sys.stdout = sys.__stdout__
        
        return driver
    except Exception as e:
        show_alert(f"启动失败：请确保已安装 Google Chrome 浏览器\n错误信息：{str(e)}")
        sys.exit(1)

def set_window_icon(window):
    """为窗口设置图标"""
    try:
        if os.path.exists(ICON_PATH):
            window.iconbitmap(ICON_PATH)
    except Exception:
        # 如果设置图标失败，静默忽略
        pass

def show_alert(message):
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    alert = tk.Toplevel()
    alert.title('提醒')
    alert.geometry("300x150+500+300")  # 设置窗口大小和位置
    alert.attributes('-topmost', True)  # 置顶窗口
    alert.grab_set()  # 模态窗口
    
    # 设置窗口图标
    set_window_icon(alert)
    
    label = tk.Label(alert, text=message, font=FONT_NORMAL)
    label.pack(pady=20)
    
    ok_button = tk.Button(alert, text="确定", font=FONT_NORMAL, command=alert.destroy)
    ok_button.pack(pady=10)
    
    alert.wait_window()  # 等待窗口关闭

def create_control_window():
    """创建控制窗口，允许用户开启或关闭监控选项"""
    window = tk.Tk()
    window.title("关键词检测控制面板")
    window.geometry("380x450+200+200")  # 增加窗口宽度和高度
    window.resizable(False, False)
    
    # 设置窗口图标
    set_window_icon(window)
    
    # 创建标题
    title_label = Label(window, text="关键词检测控制面板", font=FONT_TITLE)
    title_label.pack(pady=20)  # 增加上下间距
    
    # 创建监控选项
    options_frame = Frame(window)
    options_frame.pack(pady=10)  # 增加上下间距
    
    # 创建变量用于跟踪复选框状态
    production_var = IntVar(value=int(monitor_settings["production"]))
    quality_var = IntVar(value=int(monitor_settings["quality"]))
    rejected_var = IntVar(value=int(monitor_settings["rejected"]))
    
    # 定义更新函数
    def update_settings():
        monitor_settings["production"] = bool(production_var.get())
        monitor_settings["quality"] = bool(quality_var.get())
        monitor_settings["rejected"] = bool(rejected_var.get())
        status_label.config(text=get_status_text())
    
    # 创建复选框
    production_cb = Checkbutton(options_frame, text="监控\"生产\"关键词", variable=production_var, 
                               font=FONT_NORMAL, command=update_settings)
    production_cb.grid(row=0, column=0, sticky="w", pady=8)  # 增加项目间距
    
    quality_cb = Checkbutton(options_frame, text="监控\"质检\"关键词", variable=quality_var, 
                            font=FONT_NORMAL, command=update_settings)
    quality_cb.grid(row=1, column=0, sticky="w", pady=8)  # 增加项目间距
    
    rejected_cb = Checkbutton(options_frame, text="监控\"驳回任务\"", variable=rejected_var, 
                             font=FONT_NORMAL, command=update_settings)
    rejected_cb.grid(row=2, column=0, sticky="w", pady=8)  # 增加项目间距
    
    # 创建状态显示框
    status_frame = Frame(window, relief=tk.GROOVE, bd=1)
    status_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)  # 增加边距
    
    status_title = Label(status_frame, text="当前监控状态:", font=FONT_NORMAL)
    status_title.pack(anchor="w", padx=15, pady=(15, 8))  # 增加内边距
    
    def get_status_text():
        return (f"{'✓' if monitor_settings['production'] else '✗'} 生产关键词\n"
                f"{'✓' if monitor_settings['quality'] else '✗'} 质检关键词\n"
                f"{'✓' if monitor_settings['rejected'] else '✗'} 驳回任务")
    
    status_label = Label(status_frame, text=get_status_text(), font=FONT_NORMAL, justify="left")
    status_label.pack(anchor="w", padx=35, pady=(0, 15))  # 增加内边距
    
    # 创建退出按钮框架
    button_frame = Frame(window)
    button_frame.pack(pady=20, fill=tk.X)
    
    # 创建退出按钮
    def on_exit():
        global running
        if messagebox.askyesno("确认退出", "确定要退出程序吗？"):
            running = False
            window.destroy()
    
    # 处理窗口关闭事件
    def on_closing():
        message = """关闭控制面板将最小化到系统托盘继续运行。

如果要完全退出程序，请点击"退出程序"按钮。

确定要关闭控制面板吗？"""
        if messagebox.askyesno("确认", message):
            window.withdraw()  # 隐藏窗口而不是销毁
    
    window.protocol("WM_DELETE_WINDOW", on_closing)  # 捕获窗口关闭事件
    
    # 创建退出按钮，给予足够空间
    exit_button = Button(
        button_frame, 
        text="退出程序", 
        font=FONT_NORMAL, 
        bg="#ff6b6b", 
        fg="white", 
        command=on_exit,
        width=10,  # 设置按钮宽度
        height=1,  # 设置按钮高度
        padx=10,   # 内部水平填充
        pady=5     # 内部垂直填充
    )
    exit_button.pack(pady=5)
    
    # 添加右键菜单，用于重新显示控制面板
    def show_window(event=None):
        window.deiconify()  # 重新显示窗口
        window.lift()  # 将窗口提升到最前
        window.focus_force()  # 强制获取焦点
    
    # 返回窗口实例以便主线程可以更新它
    return window

def monitor_loop(driver, control_window):
    """监控循环，在单独的线程中运行"""
    global running
    
    # 登录页面URL
    login_url = 'https://merchant-staff.tuxiaodui.com/login'
    target_url = 'https://merchant-staff.tuxiaodui.com/task'
    
    try:
        # 打开登录页面
        driver.get(login_url)
        
        # 等待用户登录
        logged_in = False
        login_attempt_count = 0
        max_login_attempts = 30  # 最多等待30次，每次5秒
        
        # 登录检测循环
        while not logged_in and login_attempt_count < max_login_attempts and running:
            try:
                visible_text = driver.execute_script("return document.documentElement.innerText;")
                
                # 检测页面上是否存在登录后才会显示的关键词
                login_indicators = ['任务广场', '我的', '首页', '任务看板']
                for indicator in login_indicators:
                    if indicator in visible_text:
                        logged_in = True
                        break
                
                if not logged_in:
                    # 不再显示登录提示，只是等待检测登录成功
                    login_attempt_count += 1
                    time.sleep(5)  # 每5秒检查一次登录状态
                
            except Exception as e:
                login_attempt_count += 1
                time.sleep(5)
        
        if not logged_in and running:
            show_alert("登录超时，请重新启动程序并完成登录")
            return
            
        # 主循环
        while running:
            try:
                driver.get(target_url)
                time.sleep(5)
                
                visible_text = driver.execute_script("return document.documentElement.innerText;")
                
                # 检测关键词
                if monitor_settings["production"] and '生产' in visible_text:
                    show_alert('检测到"生产"关键词！')
                elif monitor_settings["quality"] and '质检' in visible_text:
                    show_alert('检测到"质检"关键词！')
                
                # 检测"我的"后面是否有数字
                if monitor_settings["rejected"]:
                    pattern = r'我的\s*\d+'
                    matches = re.search(pattern, visible_text)
                    if matches:
                        show_alert('有驳回的任务！')
                
            except Exception as e:
                # 出错时静默等待，不显示状态
                time.sleep(60)
            
            # 每分钟检测一次
            for i in range(60):
                if not running:
                    break
                time.sleep(1)
                
    except Exception as e:
        show_alert(f"程序发生错误：{str(e)}")
    finally:
        # 确保关闭浏览器
        try:
            driver.quit()
        except:
            pass

def main():
    global running
    
    # 初始化 WebDriver
    driver = get_chrome_driver()
    
    # 创建控制窗口
    control_window = create_control_window()
    
    # 在单独的线程中启动监控循环
    monitor_thread = threading.Thread(target=monitor_loop, args=(driver, control_window))
    monitor_thread.daemon = True  # 将线程设为守护线程，主线程结束时自动结束
    monitor_thread.start()
    
    # 启动主窗口的事件循环
    control_window.mainloop()
    
    # 等待监控线程结束
    running = False
    monitor_thread.join(timeout=5)
    
    # 确保浏览器被关闭
    try:
        driver.quit()
    except:
        pass
    
    print("程序已退出")

if __name__ == "__main__":
    main()