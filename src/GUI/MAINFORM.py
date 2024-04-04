#MAINFORM.py
import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Frame, Scrollbar, font as tkFont
import webbrowser
from PIL import Image, ImageTk
from src.main.API import get_news_search_result, clean_html

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
        container.place(x=695, y=120, width=1000, height=470)  # 윈도우의 오른쪽 900x500 영역에 위치

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
        self.search_news(topic)

    def search_news(self, topic):
        news_data = get_news_search_result(topic)
        if news_data:
            self.display_news(news_data)
        else:
            messagebox.showerror('오류', '뉴스를 가져오지 못했습니다.')

    def display_news(self, news_data):
        for widget in self.news_frame.winfo_children():
            widget.destroy()

        for item in news_data['items']:
            clean_title = clean_html(item['title'])
            clean_description = clean_html(item['description'])
            link = item['link']
            pubDate = item['pubDate']
            source = item['originallink'].split('/')[2].replace('www.', '')

            ttk.Label(self.news_frame, text=f"{source} | {pubDate}", font=('Helvetica', 10)).pack(anchor='w')
            title_label = ttk.Label(self.news_frame, text=clean_title, font=('Helvetica', 12, 'bold'), foreground="blue", cursor="hand2")
            title_label.pack(anchor='w')
            title_label.bind("<Button-1>", lambda e, link=link: webbrowser.open(link))
            ttk.Label(self.news_frame, text=clean_description, font=('Helvetica', 10)).pack(anchor='w')

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


