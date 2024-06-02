import tkinter as tk
from tkinter import messagebox
from src.GUI.Weather import Weather

class SidePanel:
    def __init__(self, root, open_myinfo_callback, panel_width=300):  # 너비를 300으로 변경
        self.root = root
        self.panel_width = panel_width
        self.is_panel_visible = False
        self.open_myinfo_callback = open_myinfo_callback
        self.create_side_panel()

    def create_side_panel(self):
        self.side_panel = tk.Frame(self.root, width=self.panel_width, height=500, bg='#68a6fc')
        initial_x = self.root.winfo_screenwidth()
        self.side_panel.place(x=initial_x, y=0)  # Initial position off the right edge to hide

        # Create a frame for the close button and pack it to the top right
        close_button_frame = tk.Frame(self.side_panel, bg='#68a6fc')
        close_button_frame.pack(fill='x')

        close_button = tk.Button(close_button_frame, text="X", bg="#68a6fc", fg="white", borderwidth=0,
                                 font=('Helvetica', 25, 'bold'), command=self.toggle_side_panel)
        close_button.pack(side='right', padx=5, pady=5)

        self.create_button("내 정보", self.open_myinfo_callback, ("center", 60), 20)
        self.create_button("날씨 정보", self.open_Weather_window, ("center", 0), 20)

        # 이 공백을 안 쓰면 네모가 작아져요
        dot_label = tk.Label(self.side_panel, text="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n                                                 ",
                             bg='#68a6fc', fg='white', font=('Helvetica', 16))
        dot_label.pack(side='bottom', anchor='se')

    def create_button(self, text, command, pack_options, font_size, pady=0, font_weight='normal'):
        button = tk.Button(self.side_panel, text=text, bg='#68a6fc', fg='white',
                           font=('Helvetica', font_size, font_weight),
                           highlightbackground='#68a6fc', highlightthickness=0, bd=0, relief='flat',
                           command=command)
        if len(pack_options) == 1:
            button.pack(anchor=pack_options[0], pady=pady)
        else:
            button.pack(anchor=pack_options[0], pady=pack_options[1])

    def toggle_side_panel(self):
        target_x = self.root.winfo_width() - self.panel_width if not self.is_panel_visible else self.root.winfo_width()
        self.slide_panel(target_x)
        self.is_panel_visible = not self.is_panel_visible

    def slide_panel(self, target_x):
        current_x = self.side_panel.winfo_x()
        step = 10  # 이동 속도 조절을 위한 단계 값
        new_x = min(current_x + step, target_x) if current_x < target_x else max(current_x - step, target_x)

        self.side_panel.place(x=new_x, y=0)
        if new_x != target_x:  # 목표 위치에 도달하지 않았다면 계속 이동
            self.root.after(10, lambda: self.slide_panel(target_x))

    def open_Weather_window(self):
        weather_window = tk.Toplevel(self.root)
        Weather(weather_window)  # Weather 클래스의 인스턴스를 생성하고 초기화합니다.
