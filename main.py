import os.path
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from function import check_location  # 从 function.py 导入 check_location 函数

# 自定义圆角按钮类
class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=120, height=40, corner_radius=20, bg="#4CAF50", fg="white", **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0, **kwargs)
        self.command = command
        self.corner_radius = corner_radius
        self.bg = bg
        self.fg = fg
        self.text = text

        # 创建圆角矩形
        self.rect_id = self.create_rounded_rectangle(0, 0, width, height, radius=corner_radius, fill=bg, outline=bg)
        self.text_id = self.create_text(width // 2, height // 2, text=text, fill=fg, font=("Arial", 12, "bold"))
        self.bind_events()

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1, x2, y1 + radius,
            x2, y2 - radius,
            x2, y2, x2 - radius, y2,
            x1 + radius, y2,
            x1, y2, x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def bind_events(self):
        self.tag_bind(self.rect_id, "<Button-1>", lambda e: self.on_click())
        self.tag_bind(self.text_id, "<Button-1>", lambda e: self.on_click())

    def on_click(self):
        if self.command:
            self.command()


# 主应用程序类
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("模组管理工具")
        self.geometry("400x500")
        self.resizable(False, False)

        # 页面容器
        self.pages = {}
        self.create_pages()

    def create_pages(self):
        # 初始化页面
        self.pages["main"] = MainPage(self)
        self.pages["progress"] = ProgressPage(self)
        self.pages["confirmation"] = ConfirmationPage(self)
        self.pages["module_view"] = ModuleViewPage(self)

        # 默认显示主页面
        self.show_page("main")

    def show_page(self, page_name):
        for page in self.pages.values():
            page.pack_forget()
        self.pages[page_name].pack(fill="both", expand=True)


# 主页面
class MainPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.master = master

        # 标题
        title = tk.Label(self, text="模组管理工具", font=("Arial", 20, "bold"), bg="white", fg="black")
        title.pack(pady=40)

        # 按钮
        button1 = RoundedButton(self, text="安装模组", command=self.install_module)
        button1.pack(pady=20)

        button2 = RoundedButton(self, text="模组介绍", command=self.view_modules)
        button2.pack(pady=20)

        button3 = RoundedButton(self, text="重置原版", command=self.reset_game)
        button3.pack(pady=20)

    def install_module(self):
        self.master.show_page("progress")
        self.master.pages["progress"].start_task("安装模组")

    def reset_game(self):
        self.master.show_page("progress")
        self.master.pages["progress"].start_task("重置原版")

    def view_modules(self):
        self.master.show_page("module_view")


# 进度条页面
class ProgressPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.master = master

        # 标题
        self.title = tk.Label(self, text="", font=("Arial", 18), bg="white")
        self.title.pack(pady=40)

        # 进度条
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=20)

    def start_task(self, task_name):
        self.title.config(text=task_name)
        self.progress["value"] = 0
        self.after(100, self.simulate_progress)

    def simulate_progress(self):
        if self.progress["value"] < 100:
            self.progress["value"] += 5
            self.after(100, self.simulate_progress)
        else:
            self.master.show_page("confirmation")


# 确认页面
class ConfirmationPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.master = master

        # 消息
        message = tk.Label(self, text="操作完成！", font=("Arial", 18), bg="white")
        message.pack(pady=40)

        # 返回主页按钮
        back_button = RoundedButton(self, text="返回主页", command=lambda: master.show_page("main"))
        back_button.pack(pady=20)


# 查看模组页面
class ModuleViewPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.master = master

        # 模组介绍
        description = tk.Label(self, text="这里是模组的介绍内容。", font=("Arial", 14), bg="white")
        description.pack(pady=40)

        # 返回主页按钮
        back_button = RoundedButton(self, text="返回主页", command=lambda: master.show_page("main"))
        back_button.pack(pady=20)


# 启动应用程序
if __name__ == "__main__":
    if not os.path.exists('main.py') or check_location():  # 检查路径是否有效
        tk.Tk().withdraw()  # 隐藏根窗口
        messagebox.showerror("错误", "请将文件移动至游戏根目录下！")
    else:
        app = Application()
        app.mainloop()
