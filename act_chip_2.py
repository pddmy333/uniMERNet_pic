import pyautogui
import tkinter as tk
import os
import demo

root_path = os.path.abspath(os.getcwd())
image_path = os.path.join(root_path, 'asset/test_imgs', 'screenshot.png')
config_path = os.path.join(root_path, "configs/demo.yaml")

class action_chip:
    def __init__(self,image_path):
        self.image_path = image_path

        self.root = tk.Tk()
        self.root.overrideredirect(True)  # 隐藏窗口的标题栏
        self.root.attributes("-alpha", 0.1)  # 窗口透明度10%
        self.root.geometry("{0}x{1}+0+0".format(self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.root.configure(bg="black")

        # 再创建1个Canvas用于圈选
        self.cv = tk.Canvas(self.root)
        self.x, self.y = 0, 0
        self.xstart, self.ystart = 0, 0
        self.xend, self.yend = 0, 0
        self.rec = ''

        self.canvas = tk.Canvas(self.root)
        self.canvas.configure(width=300)
        self.canvas.configure(height=100)
        self.canvas.configure(bg="yellow")
        self.canvas.configure(highlightthickness=0)  # 高亮厚度
        self.canvas.place(x=(self.root.winfo_screenwidth() - 500), y=(self.root.winfo_screenheight() - 300))
        self.canvas.create_text(150, 50, font='Arial -20 bold', text='ESC退出，假装工具条')

        # 绑定事件
        self.canvas.bind("<B1-Motion>", self.move)  # 鼠标左键移动->显示当前光标位置
        self.root.bind('<Escape>', self.sys_out)  # 键盘Esc键->退出
        self.root.bind("<Button-1>", self.button_1)  # 鼠标左键点击->显示子窗口
        self.root.bind("<B1-Motion>", self.b1_Motion)  # 鼠标左键移动->改变子窗口大小
        self.root.bind("<ButtonRelease-1>", self.buttonRelease_1)  # 鼠标左键释放->记录最后光标的位置
        self.root.bind("<Button-3>", self.button_3)  # 鼠标右键点击->截屏并保存图片
        self.root.mainloop()

    def move(self, event):
        # global用于声明其变量为全局变量 函数里面改变 外面的同名函数也会改变
        new_x = (event.x - self.x) + self.canvas.winfo_x()
        new_y = (event.y - self.y) + self.canvas.winfo_y()
        s = "300x200+" + str(new_x) + "+" + str(new_y)
        self.canvas.place(x=new_x - self.xstart, y=new_y - self.ystart)
        print("s = ", s)
        print(self.root.winfo_x(), self.root.winfo_y())
        print(event.x, event.y)

    def button_1(self, event):
        self.x, self.y = event.x, event.y
        self.xstart, self.ystart = event.x, event.y
        print("event.x, event.y = ", event.x, event.y)
        self.xstart, self.ystart = event.x, event.y
        self.cv.configure(height=1)
        self.cv.configure(width=1)
        self.cv.config(highlightthickness=0)  # 无边框
        self.cv.place(x=event.x, y=event.y)
        self.rec = self.cv.create_rectangle(0, 0, 0, 0, outline='red', width=8, dash=(4, 4))

    def b1_Motion(self,event):
        self.x, self.y = event.x, event.y
        print("event.x, event.y = ", event.x, event.y)
        self.cv.configure(height=event.y - self.ystart)
        self.cv.configure(width=event.x - self.xstart)
        self.cv.coords(self.rec, 0, 0, event.x - self.xstart, event.y - self.ystart)

    def buttonRelease_1(self,event):
        self.xend, self.yend = event.x, event.y

    def button_3(self,event):
        self.cv.delete(self.rec)
        self.cv.place_forget()
        img = pyautogui.screenshot(region=[self.xstart, self.ystart, self.xend - self.xstart, self.yend - self.ystart])  # x,y,w,h
        img.save(self.image_path)
        self.sys_out(None)

    def sys_out(self,event):
        self.root.destroy()

    # processor = demo.ImageProcessor(config_path)

    # latex_code = processor.process_single_image(image_path)

    # # 创建识别窗口
    # rt_1 = tk.Tk()
    # rt_1.title("识别")  # 设置窗口标题
    # rt_1.geometry("300x200")  # 设置窗口大小
    #
    # # 创建一个 Label 控件，用于显示文本
    # text = tk.Text(rt_1, font=("Arial", 16))
    # text.pack(fill=tk.BOTH, expand=True)  # 使 Text 控件填充整个窗口
    # text.insert(tk.END, latex_code)
    # rt_1.mainloop()
    #
    # print(latex_code)

