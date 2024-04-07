import tkinter as tk


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.side_panel_width = 200
        self.is_panel_visible = False

        self.update()  # 창의 정보를 최신 상태로 갱신

        # 사이드 패널 초기 위치를 창의 너비에 맞춰 설정하여 숨김
        self.side_panel = tk.Frame(self, width=self.side_panel_width, bg='#68a6fc')
        self.side_panel.place(x=self.winfo_width(), y=0, relheight=1.0)

        # 사이드 패널 토글 버튼 (메인 윈도우에 추가)
        self.toggle_button = tk.Button(self, text="Toggle Side Panel", command=self.toggle_side_panel,
                                       highlightbackground='#68a6fc', highlightthickness=0, bd=0, relief='flat')
        self.toggle_button.pack(pady=20)

        # 메뉴 버튼 추가
        self.menu_button = tk.Button(self, text="≡", font=('Helvetica', 14, 'bold'), fg='white', bg='#68a6fc',
                                     highlightbackground='#68a6fc', highlightthickness=0, bd=0, relief='flat',
                                     command=self.toggle_side_panel)  # 사이드 패널 토글 기능 연결
        self.menu_button.pack(side='right', padx=10, pady=10)

        # 사이드 패널 닫기 버튼
        self.close_button = tk.Button(self.side_panel, text="X", command=self.toggle_side_panel, bg='#68a6fc',
                                      fg='white', highlightbackground='#68a6fc', highlightthickness=0, bd=0,
                                      relief='flat')
        self.close_button.pack(anchor='ne')

        # 사이드 패널 내 '내정보' 버튼
        self.info_button = tk.Button(self.side_panel, text="                    내정보                    ", bg='#68a6fc', fg='white',
                                     highlightbackground='#68a6fc', highlightthickness=0, bd=0, relief='flat')
        self.info_button.pack(pady=60)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
