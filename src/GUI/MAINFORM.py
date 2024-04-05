#MAINFORM.py
import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Frame, Scrollbar, font as tkFont
import webbrowser

import link
from PIL import Image, ImageTk
from src.main.API import (get_news_search_result, clean_html, get_politics_headlines, get_Economy_headlines,
                          get_Society_headlines, get_IT_headlines,get_Car_headlines, get_Life_headlines,get_World_headlines)
class NewsFeedApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.root.title("개인화된 뉴스 피드")
        self.root.geometry("1700x900")
        self.root.resizable(False, False)
        self.create_menu()
        self.create_search_frame()
        self.create_topic_frame()
        self.create_news_frame()
        self.load_initial_news()
        """self.topic_functions = {
            "정치": self.load_Politics_headlines,
            "경제": self.load_Economy_headlines,
            "사회": self.load_Society_headlines,
            "생활/문화" : self.load_Life_headlines,
            "세계": self.load_World_headlines,
            "IT과학" : self.load_IT_headlines,

        }"""

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
        search_photo = ImageTk.PhotoImage(search_img)

        search_canvas = tk.Canvas(search_frame, width=30, height=30, bg='#68a6fc', highlightthickness=0, bd=0)
        search_canvas.pack(side='left', padx=10, pady=10)
        search_canvas.create_image(17, 17, image=search_photo)
        search_canvas.bind("<Button-1>", self.handle_search)
        search_canvas.image = search_photo

    def create_topic_frame(self):
        self.topics = ["정치", "경제", "사회", "자동차", "IT/과학", "세계", "건강", "여행/레저", "음식/맛집", "패션/뷰티", "공연/전시", "책", "종교",
                       "날씨"]
        self.topic_frame = tk.Frame(self.root, bg='#68a6fc')
        self.topic_frame.pack(fill='x', padx=5, pady=5)
        self.topic_labels = []  # 주제 라벨들을 저장할 리스트

        for topic in self.topics:
            topic_label = tk.Label(self.topic_frame, text=topic, fg='white', bg='#68a6fc', padx=6,
                                   font=('Helvetica', 12, 'bold'))
            topic_label.pack(side='left', padx=4, pady=4)
            topic_label.bind("<Button-1>", lambda e, t=topic: self.on_topic_click(e, t))
            self.topic_labels.append(topic_label)

    def create_news_frame(self):
        # 뉴스 프레임 컨테이너 생성 (프레임의 위치와 크기를 place를 이용해 지정)
        container = ttk.Frame(self.root)
        container.place(x=0, y=120, width=1000, height=470)  # 윈도우의 오른쪽 900x500 영역에 위치

        # 스크롤바 생성
        canvas = tk.Canvas(container, width=880, height=480)  # canvas 크기를 조금 더 작게 설정하여 scrollbar에 공간을 제공
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        # 스크롤 가능한 프레임에 스크롤바 연결
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # 캔버스에 스크롤 가능한 프레임을 추가하고, 스크롤바 설정
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 컨테이너에 캔버스와 스크롤바를 배치
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.news_frame = self.scrollable_frame

    def load_initial_news(self):
        self.search_news("일반")

    def on_topic_click(self, event, topic):
        # 모든 주제 라벨의 배경색을 원래대로 되돌림
        for label in self.topic_labels:
            label.config(bg='#68a6fc')

        # 선택된 주제의 배경색 변경
        event.widget.config(bg='#1859b5')

        # 선택된 주제의 뉴스 검색
        # 선택된 토픽에 맞는 함수를 호출

        self.search_news(topic)
    """ 공사중 (헤드라인 뉴스를 가져오기 위한 웹크롤링)
        if topic in self.topic_functions:
            self.topic_functions[topic]()
    def load_Politics_headlines(self):
        headlines = get_politics_headlines()
        self.display_news(headlines)

    def load_World_headlines(self):
        headlines = get_World_headlines()
        self.display_news(headlines)
    def load_IT_headlines(self):
        headlines = get_IT_headlines()
        self.display_news(headlines)
    def load_Car_headlines(self):
        headlines = get_Car_headlines()
        self.display_news(headlines)
    def load_Life_headlines(self):
        headlines = get_Life_headlines()
        self.display_news(headlines)
    def load_Economy_headlines(self):
        headlines = get_Economy_headlines()
        self.display_news(headlines)
    def load_Society_headlines(self):
        headlines = get_Society_headlines()
        self.display_news(headlines)"""

    def search_news(self, topic):
        news_data = get_news_search_result(topic)
        if news_data:
            self.display_news(news_data)
        else:
            messagebox.showerror('오류', '뉴스를 가져오지 못했습니다.')

    def display_news(self, news_data):
        # 뉴스 프레임 내의 기존 위젯들을 모두 제거
        for widget in self.news_frame.winfo_children():
            widget.destroy()

        # news_data가 리스트라면 그대로 사용, 딕셔너리라면 'items' 키에서 데이터를 가져옴
        items = news_data if isinstance(news_data, list) else news_data.get('items', [])

        # 데이터 표시
        for item in items:
            # API 호출 결과 또는 직접 스크랩한 데이터 처리
            title = clean_html(item.get('title', ''))
            link = item.get('link', '')

            # 뉴스 제목과 링크 표시
            ttk.Label(self.news_frame, text=f"{title}", font=('Helvetica', 10)).pack(anchor='w')

            # 링크를 올바르게 열기 위한 람다 함수 수정
            # 람다 함수에 현재 link 값을 캡처하기 위해 기본값을 사용
            title_label = ttk.Label(self.news_frame, text=title, font=('Helvetica', 12, 'bold'), foreground="blue",
                                    cursor="hand2")
            title_label.pack(anchor='w')
            title_label.bind("<Button-1>", lambda e, l=link: webbrowser.open(l))
    def handle_search(self, event=None):
        search_query = self.search_entry.get().strip()
        if search_query:
            self.search_news(search_query)
        else:
            messagebox.showinfo('알림', '검색어가 없습니다.')

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
    app = NewsFeedApp(root)
    root.mainloop()


