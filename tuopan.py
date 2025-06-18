import pystray
from PIL import Image
import threading
# import keyboard
import subprocess
import os
import sys
import time
from pynput import keyboard
import demo
import tkinter as tk
import act_chip_2

root_path = os.path.abspath(os.getcwd())
image_path = os.path.join(root_path, 'asset/test_imgs', 'screenshot.png')
config_path = os.path.join(root_path, "configs/demo.yaml")
logo_path = os.path.join(root_path, 'asset/images', 'modelscope_logo.png')


# 在模块级别定义全局变量
icon = None
sign = None
current_keys = set()
# 定义热键组合
HOTKEY_COMBO = {keyboard.Key.ctrl, keyboard.Key.shift, keyboard.KeyCode.from_char('c')}


# 定义快捷键触发的回调函数 修改此函数内容改成函数调用形式
def on_activate():
    print("快捷键触发！执行任务...")
    act = act_chip_2.action_chip(image_path)

    processor = demo.ImageProcessor(config_path)

    latex_code = processor.process_single_image(image_path)

    # 创建识别窗口
    rt_1 = tk.Tk()
    rt_1.title("识别")  # 设置窗口标题
    rt_1.geometry("300x200")  # 设置窗口大小

    # 创建一个 Label 控件，用于显示文本
    text = tk.Text(rt_1, font=("Arial", 16))
    text.pack(fill=tk.BOTH, expand=True)  # 使 Text 控件填充整个窗口
    text.insert(tk.END, latex_code)
    rt_1.mainloop()

    print(latex_code)


# # 注册快捷键（例如 Ctrl+Shift+A）
# keyboard.add_hotkey('ctrl+shift+c', on_activate)


# 创建系统托盘图标
def create_tray_icon():
    global icon
    global sign
    image = Image.open(logo_path)  # 替换为你的图标文件路径
    menu = pystray.Menu(
        pystray.MenuItem("截图", on_activate),
        pystray.MenuItem("退出", exit_program)
    )
    icon = pystray.Icon("后台程序", image, "后台程序", menu)
    icon.run()


# 退出程序
def exit_program():
    global icon
    global sign
    try:
        icon.stop()
        print("程序已退出")
        listener.stop()
        print("停止监听")
        sign = 1
        time.sleep(5)
        sys.exit()
    except Exception as e:
        print(f"停止托盘图标失败: {e}")
        sign = 0
    # sys.exit()  # 为什么会错


# 启动系统托盘图标
threading.Thread(target=create_tray_icon, daemon=True).start()


# 注册快捷键（例如 Ctrl+Shift+C）
# 定义监听器
hotkey = keyboard.HotKey(
    {keyboard.Key.ctrl, keyboard.Key.shift, keyboard.KeyCode(char='c')},
    on_activate
)


def for_canonical(f):
    return lambda k: f(listener.canonical(k))


# 让程序保持在后台运行
print("程序已在后台运行，等待快捷键触发...")
# 创建键盘监听器
listener = keyboard.Listener(on_press=for_canonical(hotkey.press), on_release=for_canonical(hotkey.release))
listener.start()
listener.join()
