#MAINFORM.py
import queue
import threading
import requests
from io import BytesIO
import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Frame, Scrollbar, font as tkFont
import webbrowser
from PIL import Image, ImageTk


from src.main.API import (get_news_search_result, clean_html, get_politics_headlines, get_Economy_headlines,
                          get_Society_headlines, get_IT_headlines,get_Car_headlines, get_Life_headlines,get_World_headlines,get_Fashion_headlines,get_Exhibition_headlines,
                          get_Travel_headlines,get_Health_headlines,get_Food_headlines,get_Book_headlines,get_Religion_headlines)

class NewsFeedApp:

    def __init__(self, root, username=None, access_token=None,search_photo= None):
        self.root = root
        self.userid = username
        self.access_token = access_token
        self.search_photo = search_photo # 이미지를 저장할 속성 추가
        self.is_panel_visible = False
        self.panel_width = 200
        self.setup_ui()
        self.image_queue = queue.Queue()
        self.load_user_info()
        self.start_image_update_loop()

    def setup_ui(self):
        self.root.title("개인화된 뉴스 피드")
        self.root.geometry("1700x900")
        self.root.resizable(False, False)
        self.create_menu()
        self.create_search_frame()
        self.create_topic_frame()
        self.create_news_frame()
        self.load_initial_news()
        self.create_side_panel()
        self.create_headline_frame()
        self.topic_functions = {
            "정치": self.load_Politics_headlines,
            "경제": self.load_Economy_headlines,
            "사회": self.load_Society_headlines,
            "생활/문화" : self.load_Life_headlines,
            "세계": self.load_World_headlines,
            "IT/과학" : self.load_IT_headlines,
            "건강" : self.load_Health_headlines,
            "여행/레저" : self.load_Travel_headlines,
            "음식/맛집" : self.load_Food_headlines,
            "패션/뷰티" : self.load_Fashion_headlines,
            "공연/전시" : self.load_Exhibition_headlines,
            "책" : self.load_Book_headlines,
            "종교" : self.load_Religion_headlines,
            "자동차" : self.load_Car_headlines

        }

    def load_image_async(self, image_url, image_label):
        try:
            response = requests.get(image_url)
            img_data = BytesIO(response.content)
            image = Image.open(img_data).resize((100, 100))
            photo = ImageTk.PhotoImage(image)
            self.image_queue.put((image_label, photo))  # 큐에 (레이블, 이미지) 튜플 추가
        except Exception as e:
            print(f"Error loading image: {e}")

    def start_image_update_loop(self):
        try:
            while not self.image_queue.empty():
                image_label, photo = self.image_queue.get_nowait()
                image_label.configure(image=photo)
                image_label.image = photo  # 참조 유지
        except queue.Empty:
            pass
        finally:
            # 100ms 후에 이 메소드를 다시 호출하여 큐를 확인
            self.root.after(100, self.start_image_update_loop)

    def load_user_info(self):
        if self.userid and self.access_token:
            messagebox.showinfo("성공", "{}님 반갑습니다.".format(self.userid))
            # 여기서 추가 로직을 구현할 수 있습니다. 예: API 호출에 토큰 사용
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
        setting_canvas.bind("<Button-1>", self.toggle_side_panel)  # 오른쪽 패널을 여는 기능 바인딩
        setting_canvas.image = setting_photo

    def create_side_panel(self):
        from src.Server.Client import open_Myinfo_window
        self.side_panel = tk.Frame(self.root, width=self.panel_width, height=500, bg='#68a6fc')
        initial_x = self.root.winfo_screenwidth()
        self.side_panel.place(x=initial_x, y=0)  # 초기 위치 오른쪽 바깥으로 설정하여 숨김

        close_button = tk.Button(self.side_panel, text="X", bg="#68a6fc", fg="white", borderwidth=0,
                                 font=('Helvetica', 25, 'bold'),
                                 command=self.toggle_side_panel)
        close_button.pack(anchor='ne')

        # open_Myinfo_window 함수를 my_info_button 생성 전에 정의합니다.


        my_info_button = tk.Button(self.side_panel, text="내 정보", bg='#68a6fc',
                                   fg='white',
                                   font=('Helvetica', 20),
                                   highlightbackground='#68a6fc', highlightthickness=0, bd=0, relief='flat',
                                   command=open_Myinfo_window)  # 여기서 함수를 command로 지정합니다.
        my_info_button.pack(pady=60)

        # 이 공백을 안 쓰면 네모가 작아져요
        dot_label = tk.Label(self.side_panel, text="\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n                                 ", bg='#68a6fc', fg='white', font=('Helvetica', 16))
        dot_label.pack(side='bottom', anchor='se')

    def toggle_side_panel(self, _=None):
        # 사이드 패널이 화면 오른쪽에서 왼쪽으로 이동하게끔 시작 위치 변경
        if not self.is_panel_visible:
            target_x = self.root.winfo_width() - self.panel_width  # 사이드 패널을 보이게 할 위치
        else:
            target_x = self.root.winfo_width()  # 사이드 패널을 숨길 위치
        self.slide_panel(target_x)
        self.is_panel_visible = not self.is_panel_visible

    def slide_panel(self, target_x):
        current_x = self.side_panel.winfo_x()
        step = 10  # 이동 속도 조절을 위한 단계 값
        if current_x < target_x:
            new_x = min(current_x + step, target_x)  # 오른쪽으로 이동
        else:
            new_x = max(current_x - step, target_x)  # 왼쪽으로 이동

        self.side_panel.place(x=new_x, y=0)
        if new_x != target_x:  # 목표 위치에 도달하지 않았다면 계속 이동
            self.root.after(10, lambda: self.slide_panel(target_x))

    def create_topic_frame(self):
        self.topics = ["정치", "경제", "사회", "자동차", "IT/과학", "세계", "건강", "여행/레저", "음식/맛집", "패션/뷰티", "공연/전시", "책", "종교"]
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

        # 컨테이너에 캔버스와 스크롤바를 배치1
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.news_frame = self.scrollable_frame
        canvas.bind("<MouseWheel>", lambda e: self.on_mousewheel(e, canvas))

    def on_mousewheel(self, event, canvas):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_headline_frame(self):
        container = ttk.Frame(self.root)
        container.place(x=551, y=120, width=700, height=900)

        self.canvas = tk.Canvas(container)
        self.canvas.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.headline_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.headline_frame, anchor="nw")

        self.headline_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # 마우스 휠 이벤트 바인딩을 추가합니다.
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
                # 이미지 로드 작업을 별도의 스레드에서 실행
                threading.Thread(target=self.load_image_async, args=(headline['image_url'], image_label)).start()
            title_font = ('Helvetica', 12, 'bold')
            title_label = tk.Label(frame, text=headline['title'], fg='blue', font=title_font, cursor='hand2',
                                   wraplength=500, justify="left")
            title_label.grid(row=0, column=1, sticky="w")
            title_label.bind("<Button-1>", lambda e, l=headline['link']: webbrowser.open(l))
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

        if topic in self.topic_functions:
            self.topic_functions[topic]()
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
        # get_news_search_result 함수를 사용하여 뉴스 데이터 가져오기
        news_data = get_news_search_result(query)
        if news_data:
            self.display_news(news_data['items'])  # 'items' 내의 뉴스 데이터를 화면에 표시
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
        search_query = self.search_entry.get().strip()  # 검색어 가져오기

        if search_query:
            # 검색어가 있다면, 뉴스 검색 함수 호출
            self.search_news(search_query)
        else:
            # 검색어가 없다면, 사용자에게 알림
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
    # 예를 들어, 로그인 성공 후에 사용자 이름과 토큰을 얻었다고 가정
    username = "사용자 이름"
    access_token = "액세스 토큰"
    app = NewsFeedApp(root, username, access_token)
    root.mainloop()