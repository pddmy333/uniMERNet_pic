import pyautogui
import tkinter as tk
import os
import demo

root_path = os.path.abspath(os.getcwd())
image_path = os.path.join(root_path, 'asset/test_imgs', 'screenshot.png')


def move(event):
    # global用于声明其变量为全局变量 函数里面改变 外面的同名函数也会改变
    global x, y, xstart, ystart
    new_x = (event.x - x) + canvas.winfo_x()
    new_y = (event.y - y) + canvas.winfo_y()
    s = "300x200+" + str(new_x) + "+" + str(new_y)
    canvas.place(x=new_x - xstart, y=new_y - ystart)
    print("s = ", s)
    print(root.winfo_x(), root.winfo_y())
    print(event.x, event.y)


def button_1(event):
    global x, y, xstart, ystart
    global rec
    x, y = event.x, event.y
    xstart, ystart = event.x, event.y
    print("event.x, event.y = ", event.x, event.y)
    xstart, ystart = event.x, event.y
    cv.configure(height=1)
    cv.configure(width=1)
    cv.config(highlightthickness=0)  # 无边框
    cv.place(x=event.x, y=event.y)
    rec = cv.create_rectangle(0, 0, 0, 0, outline='red', width=8, dash=(4, 4))


def b1_Motion(event):
    global x, y, xstart, ystart
    x, y = event.x, event.y
    print("event.x, event.y = ", event.x, event.y)
    cv.configure(height=event.y - ystart)
    cv.configure(width=event.x - xstart)
    cv.coords(rec, 0, 0, event.x - xstart, event.y - ystart)


def buttonRelease_1(event):
    global xend, yend
    xend, yend = event.x, event.y


def button_3(event):
    global xstart, ystart, xend, yend
    cv.delete(rec)
    cv.place_forget()
    img = pyautogui.screenshot(region=[xstart, ystart, xend - xstart, yend - ystart])  # x,y,w,h
    img.save(image_path)
    sys_out(None)


def sys_out(even):
    root.destroy()



root = tk.Tk()
root.overrideredirect(True)  # 隐藏窗口的标题栏
root.attributes("-alpha", 0.1)  # 窗口透明度10%
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(bg="black")

# 再创建1个Canvas用于圈选
cv = tk.Canvas(root)
x, y = 0, 0
xstart, ystart = 0, 0
xend, yend = 0, 0
rec = ''

canvas = tk.Canvas(root)
canvas.configure(width=300)
canvas.configure(height=100)
canvas.configure(bg="yellow")
canvas.configure(highlightthickness=0)  # 高亮厚度
canvas.place(x=(root.winfo_screenwidth() - 500), y=(root.winfo_screenheight() - 300))
canvas.create_text(150, 50, font='Arial -20 bold', text='ESC退出，假装工具条')

# 绑定事件
canvas.bind("<B1-Motion>", move)  # 鼠标左键移动->显示当前光标位置
root.bind('<Escape>', sys_out)  # 键盘Esc键->退出
root.bind("<Button-1>", button_1)  # 鼠标左键点击->显示子窗口
root.bind("<B1-Motion>", b1_Motion)  # 鼠标左键移动->改变子窗口大小
root.bind("<ButtonRelease-1>", buttonRelease_1)  # 鼠标左键释放->记录最后光标的位置
root.bind("<Button-3>", button_3)  # 鼠标右键点击->截屏并保存图片
root.mainloop()


config_path = os.path.join(root_path, "configs/demo.yaml")

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

