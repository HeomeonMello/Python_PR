import queue
import threading
import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Frame, Scrollbar, font as tkFont
import webbrowser
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
import numpy as np
import matplotlib.font_manager as fm
from src.Server.Client import Client
from src.GUI.Bubble_Chart import BubbleChart
from src.main.API import (get_news_search_result, clean_html, get_politics_headlines, get_Economy_headlines,
                          get_Society_headlines, get_IT_headlines, get_Car_headlines, get_Life_headlines, get_World_headlines, get_Fashion_headlines, get_Exhibition_headlines,
                          get_Travel_headlines, get_Health_headlines, get_Food_headlines, get_Book_headlines, get_Religion_headlines, get_trending_keywords, get_entertainment_headlines,
                          ImageLoader, get_Breaking_headlines)
from src.GUI.Weather import Weather
from src.GUI.Side_panel import SidePanel  # Import SidePanel class

class NewsFeedApp:
    def __init__(self, root, username=None, access_token=None):
        self.root = root
        self.userid = username
        self.access_token = access_token
        self.server_url = os.getenv('SERVER_URL', 'http://localhost:5000')
        self.client = Client(self.server_url, self.userid, self.access_token)
        self.search_photo = None  # 이미지를 저장할 속성 추가
        self.background_image = None
        self.setup_ui()
        self.image_queue = queue.Queue()
        self.image_loader = ImageLoader(self.root, self.image_queue)  # 이미지 로더 초기화
        self.image_loader.start_image_update_loop()
        self.load_user_info()

    def setup_ui(self):
        self.root.title("개인화된 뉴스 피드")
        self.root.configure(background='white')  # 전체 배경을 하얀색으로 설정
        self.root.geometry("1700x900")
        self.root.resizable(False, False)
        self.create_menu()
        self.create_search_frame()
        self.create_topic_frame()
        self.create_news_frame()
        self.create_keyword_frame()
        self.create_headline_frame()
        self.side_panel = SidePanel(self.root, self.open_myinfo_window)  # 사이드 패널 인스턴스 생성, 콜백 전달
        self.topic_functions = {
            "정치": self.load_Politics_headlines,
            "경제": self.load_Economy_headlines,
            "사회": self.load_Society_headlines,
            "생활/문화": self.load_Life_headlines,
            "세계": self.load_World_headlines,
            "IT/과학": self.load_IT_headlines,
            "건강": self.load_Health_headlines,
            "여행/레저": self.load_Travel_headlines,
            "음식/맛집": self.load_Food_headlines,
            "패션/뷰티": self.load_Fashion_headlines,
            "공연/전시": self.load_Exhibition_headlines,
            "책": self.load_Book_headlines,
            "종교": self.load_Religion_headlines,
            "자동차": self.load_Car_headlines,
            "연예": self.load_Entertain_headlines,
            "속보": self.load_Breaking_headlines
        }
        self.load_initial_news()  # setup_ui의 맨 마지막에 호출

    def open_myinfo_window(self):
        from src.Server.Client import open_Myinfo_window
        open_Myinfo_window()

    def load_user_info(self):
        if self.userid and self.access_token:
            messagebox.showinfo("성공", "{}님 반갑습니다.".format(self.userid))
        else:
            print("로그인한 사용자 정보를 찾을 수 없습니다.")

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="정보", command=self.about)
        menu_bar.add_cascade(label="내정보", command=self.privacy)
        menu_bar.add_cascade(label="도움말", menu=help_menu)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="종료", command=self.exit_app)
        menu_bar.add_cascade(label="현재 창 종료", menu=file_menu)

        self.root.config(menu=menu_bar)

    def create_search_frame(self):
        search_frame = tk.Frame(self.root, bg='#68a6fc')
        search_frame.pack(fill='x', pady=10)

        self.search_entry = tk.Entry(search_frame, font=('Helvetica', 14), width=40)
        self.search_entry.pack(side='left', padx=(10, 0), pady=10)
        self.search_entry.bind('<Return>', self.handle_search)

        search_img = Image.open('../Image/search.png').resize((25, 25))
        self.search_photo = ImageTk.PhotoImage(search_img)

        search_canvas = tk.Canvas(search_frame, width=30, height=30, bg='#68a6fc', highlightthickness=0, bd=0)
        search_canvas.pack(side='left', padx=10, pady=10)
        search_canvas.create_image(17, 17, image=self.search_photo)
        search_canvas.bind("<Button-1>", self.handle_search)
        search_canvas.image = self.search_photo

        # 설정 버튼 이미지 로드 및 버튼화
        setting_img = Image.open('../Image/setting.png').resize((25, 25))
        setting_photo = ImageTk.PhotoImage(setting_img)

        # 설정 버튼으로 사용될 캔버스 생성 및 오른쪽에 배치
        setting_canvas = tk.Canvas(search_frame, width=30, height=30, bg='#68a6fc', highlightthickness=0, bd=0)
        setting_canvas.pack(side='right', padx=10, pady=10)  # 오른쪽에 배치
        setting_canvas.create_image(17, 17, image=setting_photo)
        setting_canvas.bind("<Button-1>", lambda e: self.side_panel.toggle_side_panel())  # 사이드 패널 토글 기능 바인딩
        setting_canvas.image = setting_photo

    def create_topic_frame(self):
        self.topics = ["정치", "경제", "사회", "자동차", "IT/과학", "세계", "건강", "여행/레저", "음식/맛집", "연예", "패션/뷰티", "공연/전시", "책", "종교", "속보"]
        self.topic_frame = tk.Frame(self.root, bg='#68a6fc')
        self.topic_frame.pack(fill='x', padx=1, pady=8)
        self.topic_labels = []  # 주제 라벨들을 저장할 리스트

        for topic in self.topics:
            topic_label = tk.Label(self.topic_frame, text=topic, fg='white', bg='#68a6fc', padx=6,
                                   font=('Helvetica', 12, 'bold'))
            topic_label.pack(side='left', padx=4, pady=4)
            topic_label.bind("<Button-1>", lambda e, t=topic: self.on_topic_click(e, t))
            self.topic_labels.append(topic_label)

    def create_news_frame(self):
        # 테두리를 추가하기 위해 tk.Frame 사용
        container = tk.Frame(self.root, highlightbackground='red', highlightthickness=2, relief='solid')
        container.place(x=5, y=120, width=560, height=455)

        # Canvas와 Scrollbar 설정
        self.canvas_news = tk.Canvas(container, width=560, height=455, bg='white', highlightthickness=0)
        self.scrollbar_news = ttk.Scrollbar(container, orient="vertical", command=self.canvas_news.yview)

        # Scrollbar와 Canvas를 배치
        self.canvas_news.pack(side="left", fill="both", expand=True)
        self.scrollbar_news.pack(side="right", fill="y")

        # Scrollbar와 Canvas 연결
        self.canvas_news.configure(yscrollcommand=self.scrollbar_news.set)

        # 스크롤 가능한 Frame 설정
        self.news_frame = ttk.Frame(self.canvas_news)
        self.canvas_news.create_window((0, 0), window=self.news_frame, anchor="nw")

        self.canvas_news.bind("<MouseWheel>", lambda e: self.on_mousewheel(e, self.canvas_news))

    def on_mousewheel(self, event, canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_headline_frame(self):
        container = tk.Frame(self.root, highlightbackground='red', highlightthickness=2, relief='solid')

        container.place(x=570, y=120, width=670, height=770)

        self.canvas = tk.Canvas(container)
        self.canvas.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.headline_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.headline_frame, anchor="nw")

        self.headline_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))


        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_unix_mousewheel(event):
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")

        # OS에 따라 다른 이벤트 바인딩을 사용합니다.
        if self.root.tk.call('tk', 'windowingsystem') == 'win32':
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        else:
            self.canvas.bind_all("<Button-4>", _on_unix_mousewheel)
            self.canvas.bind_all("<Button-5>", _on_unix_mousewheel)

    def display_headlines(self, headlines):
        for widget in self.headline_frame.winfo_children():
            widget.destroy()

        loading_image_path = '../Image/loading.png'
        loading_image = Image.open(loading_image_path).resize((100, 100))
        photo_loading = ImageTk.PhotoImage(loading_image)

        for i, headline in enumerate(headlines):
            frame = ttk.Frame(self.headline_frame)
            frame.grid(row=i, column=0, sticky="ew", padx=10, pady=5)

            image_label = tk.Label(frame, image=photo_loading)
            image_label.image = photo_loading  # 참조 유지
            image_label.grid(row=0, column=0, rowspan=2, padx=10, pady=5)


            if headline['image_url']:
                # 이미지 로드 작업을 ImageLoader 클래스를 사용하여 비동기적으로 실행
                threading.Thread(target=self.image_loader.load_image_async,
                                 args=(headline['image_url'], image_label)).start()

            title_font = ('Helvetica', 12, 'bold')
            title_label = tk.Label(frame, text=headline['title'], fg='blue', font=title_font, cursor='hand2',
                                   wraplength=500, justify="left")
            title_label.grid(row=0, column=1, sticky="w", padx=5)
            title_label.bind("<Button-1>", lambda e, l=headline['link']: webbrowser.open(l))

            summary_font = ('Helvetica', 10)
            summary_label = tk.Label(frame, text=headline['summary'], font=summary_font, wraplength=500, justify="left")
            summary_label.grid(row=1, column=1, sticky="w", padx=1)

            frame.columnconfigure(1, weight=1)  # 콘텐츠에 맞춰 열 너비 조정

    def create_keyword_frame(self):
        container = tk.Frame(self.root, highlightbackground='red', highlightthickness=2, relief='solid')
        container.place(x=5, y=580, width=560, height=310)
        self.display_bubble_chart(container)

    def display_bubble_chart(self, container):
        keywords, popularity = get_trending_keywords()

        if not keywords:
            print("No keywords to display.")
            return

        # 한글 폰트 설정
        font_path = "../Font/Chartfont1_Bold.ttf"
        font_prop = fm.FontProperties(fname=font_path)

        # 버블 크기 조정
        scale_factor = 4  # 기본 스케일 팩터

        # 각 순위마다 버블 크기의 편차를 크게 조정
        area = np.array([popularity[0] * scale_factor * 2] +
                        [popularity[1] * scale_factor * 1.7] +
                        [popularity[2] * scale_factor * 1.3] +
                        [popularity[i] * scale_factor for i in range(3, 10)])

        # area 값 확인 출력
        print("area values:", area)

        data = {
            'keywords': keywords,
            'market_share': area,
            'color': plt.cm.tab10(np.linspace(0, 1, len(keywords)))
        }

        bubble_chart = BubbleChart(area=data['market_share'], bubble_spacing=0.1)
        bubble_chart.collapse()

        fig, ax = plt.subplots(figsize=(15.5, 5.90), subplot_kw=dict(aspect="equal"))

        # 버블 차트 그리기
        bubble_chart.plot(fig, ax, data['keywords'], data['color'], font_prop)

        # 타이틀 설정
        ax.set_title('인기 검색어 TOP 10', fontproperties=font_prop, pad=-20)  # pad 값 추가하여 아래로 이동

        # 축 숨기기
        ax.axis("off")

        # 축 범위 재조정
        ax.relim()
        ax.autoscale_view()

        plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=0, y=0, width=555, height=305)
        canvas.draw()

        def mouse_event(event):
            bubble_chart.on_hover(event)
            bubble_chart.update()

        canvas.mpl_connect("motion_notify_event", mouse_event)


    def on_topic_click(self, event, topic):
        for label in self.topic_labels:
            label.config(bg='#68a6fc')

        event.widget.config(bg='#1859b5')

        self.search_news(topic)

        if topic in self.topic_functions:
            self.topic_functions[topic]()

    def load_initial_news(self):
        self.search_news("일반")

    def load_Breaking_headlines(self):
        headlines = get_Breaking_headlines()
        self.display_headlines(headlines)

    def load_Politics_headlines(self):
        headlines = get_politics_headlines()
        self.display_headlines(headlines)

    def load_World_headlines(self):
        headlines = get_World_headlines()
        self.display_headlines(headlines)

    def load_IT_headlines(self):
        headlines = get_IT_headlines()
        self.display_headlines(headlines)

    def load_Car_headlines(self):
        headlines = get_Car_headlines()
        self.display_headlines(headlines)

    def load_Life_headlines(self):
        headlines = get_Life_headlines()
        self.display_headlines(headlines)

    def load_Economy_headlines(self):
        headlines = get_Economy_headlines()
        self.display_headlines(headlines)

    def load_Society_headlines(self):
        headlines = get_Society_headlines()
        self.display_headlines(headlines)

    def load_Health_headlines(self):
        headlines = get_Health_headlines()
        self.display_headlines(headlines)

    def load_Travel_headlines(self):
        headlines = get_Travel_headlines()
        self.display_headlines(headlines)

    def load_Food_headlines(self):
        headlines = get_Food_headlines()
        self.display_headlines(headlines)

    def load_Entertain_headlines(self):
        headlines = get_entertainment_headlines()
        self.display_headlines(headlines)

    def load_Fashion_headlines(self):
        headlines = get_Fashion_headlines()
        self.display_headlines(headlines)

    def load_Book_headlines(self):
        headlines = get_Book_headlines()
        self.display_headlines(headlines)

    def load_Exhibition_headlines(self):
        headlines = get_Exhibition_headlines()
        self.display_headlines(headlines)

    def load_Religion_headlines(self):
        headlines = get_Religion_headlines()
        self.display_headlines(headlines)

    def search_news(self, query):
        news_data = get_news_search_result(query)
        if news_data:  # 검색 결과가 존재하고, 리스트가 비어 있지 않은 경우
            filtered_news = news_data  # 여기서 필요하다면 중복 제거 로직을 추가
            if filtered_news:
                self.display_news(filtered_news)  # 뉴스 데이터를 화면에 표시
            else:
                messagebox.showinfo('결과 없음', '중복을 제외한 결과가 없습니다.')
        else:
            messagebox.showerror('오류', '뉴스를 가져오지 못했습니다.')

    def display_news(self, news_data):
        for widget in self.news_frame.winfo_children():
            widget.destroy()

        canvas = tk.Canvas(self.news_frame, width=540, height=450, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.news_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        background_image_path = '../Image/back.png'
        pil_image = Image.open(background_image_path)
        background_image = ImageTk.PhotoImage(pil_image)

        self.news_background = canvas.create_image(0, 0, image=background_image, anchor='nw')
        canvas.lower(self.news_background)
        canvas.image = background_image  # 이미지 참조 유지
        for i in range(0, 2000, pil_image.height):  # 2000은 임의의 큰 값으로, 필요에 따라 조정 가능
            canvas.create_image(0, i, image=background_image, anchor='nw')
            canvas.create_image(pil_image.width, i, image=background_image, anchor='nw')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=False)
        scrollbar.pack(side="right", fill="y")

        font_path = '../Font/Newsfont1_bold.ttf'
        custom_font = tkFont.Font(family=font_path, size=11, weight='bold')

        y_position = 10
        y_position_increment = 70  # 뉴스 아이템 간 간격을 70 픽셀로 설정

        for item in news_data:
            title = clean_html(item['title'])
            link = item['link']
            description = clean_html(item['description'])
            pubDate = item['pubDate']

            title_id = canvas.create_text(10, y_position, text=title, anchor='nw',
                                          font=custom_font, fill="blue", tags="news_item")
            canvas.tag_bind(title_id, "<Button-1>", lambda e, t=title, d=description, l=link, p=pubDate: [
                webbrowser.open(l),
                self.client.save_user_click(t, d, l, p)
            ])

            y_position += 20
            description_id = canvas.create_text(10, y_position, text=description, anchor='nw',
                                                font=('Helvetica', 10), fill="black", tags="news_item",
                                                width=530)

            y_position += 50  # 요약 내용의 높이를 고려하여 간격을 넓게 설정
            pubDate_id = canvas.create_text(10, y_position, text=f"제공된 시간: {pubDate}", anchor='nw',
                                            font=('Helvetica', 9), fill="gray", tags="news_item")

            y_position += y_position_increment  # 다음 뉴스 아이템의 위치 조정

        total_height = y_position + y_position_increment - 100  # 전체 높이를 계산
        canvas.configure(scrollregion=(0, 0, 540, total_height))  # 스크롤 영역을 뉴스 아이템에 맞게 설정

    def handle_search(self, event=None):
        search_query = self.search_entry.get().strip()  # 검색어 가져오기

        if search_query:
            self.search_news(search_query)
        else:
            messagebox.showinfo('알림', '검색어를 입력해 주세요.')

    def about(self):
        messagebox.showinfo("정보", "개인화된 뉴스 피드 애플리케이션입니다.\n원하시는 키워드는 검색하실 수 있습니다.")

    def privacy(self):
        """내 정보 클릭시 MyInfo 호출 subprocess 사용"""
        messagebox.showinfo("내 정보", "자신이 선택한 주제입니다.\n")

    def exit_app(self):
        if messagebox.askyesno("종료", "애플리케이션을 종료하시겠습니까?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    username = "사용자 이름"
    access_token = "액세스 토큰"
    app = NewsFeedApp(root, username, access_token)
    root.mainloop()
