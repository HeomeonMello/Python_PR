import urllib.request
from urllib.parse import quote
import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Frame, Scrollbar, font as tkFont
import json
import webbrowser
from PIL import Image, ImageTk
import io
import link
from bs4 import BeautifulSoup

import sys
sys.path.append("..\\main")  # 상위 디렉토리로 올라간 뒤 main 폴더로 내려감
from API import client_id, client_secret

# 네이버 Open API URL 정보
base_url = "https://openapi.naver.com/v1/search"
node = "/news.json"


def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text()
    return text

def on_frame_configure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

# 네이버 Open API 요청 함수
def get_request_url(api_url):
    req = urllib.request.Request(api_url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            return response.read().decode('UTF-8')
    except Exception as e:
        return None

# 주제 클릭 이벤트 처리 함수
def on_topic_click(event, topic):
    # 모든 주제 라벨의 배경색을 원래대로 되돌림
    for label in topic_labels:
        label.config(bg='#68a6fc')

    # 선택된 주제의 배경색 변경
    event.widget.config(bg='#1859b5')

    # 선택된 주제의 뉴스 검색
    search_news(topic)

# 뉴스 검색 결과 가져오기
def get_news_search_result(src_text, start=1, display=10):
    api_url = f"{base_url}{node}?query={quote(src_text)}&start={start}&display={display}"
    response_decode = get_request_url(api_url)
    if response_decode:
        return json.loads(response_decode)
    return None


def display_news(news_data):
    for widget in news_frame.winfo_children():
        widget.destroy()

    for i, item in enumerate(news_data['items']):
        raw_title = item['title']
        clean_title = clean_html(raw_title)  # HTML 태그 제거
        raw_description = item['description']
        clean_description = clean_html(raw_description)  # HTML 태그 제거
        link = item['link']
        pubDate = item['pubDate']
        source = item['originallink'].split('/')[2].replace('www.', '')  # 도메인 추출

        ttk.Label(news_frame, text=f"{source} | {pubDate}", font=('Helvetica', 10)).pack(anchor='w')
        title_label = ttk.Label(news_frame, text=clean_title, font=('Helvetica', 12, 'bold'), foreground="blue",
                                cursor="hand2")
        title_label.pack(anchor='w')
        ttk.Label(news_frame, text=clean_description, font=('Helvetica', 10)).pack(anchor='w')
        title_label.bind("<Button-1>", lambda e, link=link: webbrowser.open(link))

def search_news(topic):
    news_data = get_news_search_result(topic)
    if news_data:
        display_news(news_data)
    else:
        messagebox.showerror('오류', '뉴스를 가져오지 못했습니다.')

# 초기 뉴스 로딩 함수
def load_initial_news():
    initial_topic = "일반"  # 또는 다른 기본 검색어
    search_news(initial_topic)

def handle_search(event=None):  # `event` 매개변수 추가
    # 사용자 입력을 받아오기
    search_query = search_entry.get().strip()  # 앞뒤 공백 제거
    if search_query:  # 검색어가 비어있지 않을 경우에만 검색 진행
        search_news(search_query)
    else:
        messagebox.showinfo('알림', '검색어가 없습니다.')

        # 사용자 정보 표시 함수
        def show_user_info():
            messagebox.showinfo('사용자 정보', '사용자: 홍길동\n등급: VIP\n가입일: 2023-01-01')


# 메인 윈도우 설정
root = tk.Tk()
root.title("개인화된 뉴스 피드")
root.geometry("1340x800")


# 검색창 프레임 설정
search_frame = tk.Frame(root, bg='#68a6fc')
search_frame.pack(fill='x', pady=10)

# 검색창 입력 필드
search_entry = tk.Entry(search_frame, font=('Helvetica', 14), width=40)
search_entry.pack(side='left', padx=(10, 0), pady=10)

# 검색 버튼 이미지 로드 및 설정
search_img = Image.open('../Image/search.png')  # 이미지 파일 위치
search_img = search_img.resize((20, 20)) # 이미지 사이즈 조절
search_photo = ImageTk.PhotoImage(search_img)

# 검색 버튼을 이미지 버튼으로 변경
search_button = tk.Button(search_frame, image=search_photo, command=handle_search,
                          borderwidth=2, relief=tk.RAISED)
search_button.image = search_photo  # 이미지가 가비지 컬렉션에 의해 삭제되는 것을 방지
search_button.pack(side='left', padx=10, pady=10)

# 엔터 키를 눌렀을 때 검색이 되도록 바인딩, 함수 호출 수정
search_entry.bind('<Return>', handle_search)

# 뉴스 항목을 Canvas 위에 표시하는 함수

# 뉴스 프레임과 스크롤바를 포함한 Canvas 설정
news_canvas = Canvas(root, borderwidth=0, background="#ffffff")
news_frame = Frame(news_canvas, background="#ffffff")
v_scrollbar = Scrollbar(root, orient="vertical", command=news_canvas.yview)
news_canvas.configure(yscrollcommand=v_scrollbar.set)


v_scrollbar.pack(side="right", fill="y")
news_canvas.pack(side="left", fill="both", expand=True)
canvas = Canvas(news_frame)
canvas.pack(side="left", fill="both", expand=True)

news_canvas.create_window((4, 4), window=news_frame, anchor="nw", tags="frame")
news_frame.bind("<Configure>", lambda event, canvas=news_canvas: on_frame_configure(news_canvas))


# 배경색 설정을 위한 메인 프레임
main_frame = tk.Frame(root, bg='#68a6fc')
main_frame.pack(fill='x', expand=False)

# 스크롤 가능한 프레임 설정
scrollable_frame = tk.Frame(main_frame, bg='#68a6fc')
scrollable_frame.pack(side='left', fill='x', expand=True)

# 주제 목록
topics = ["정치", "경제", "사회", "자동차", "IT/과학", "세계", "건강", "여행/레저", "음식/맛집", "패션/뷰티", "공연/전시", "책", "종교", "날씨"]
topic_labels = []

# 주제 표시
for topic in topics:
    label_font = tkFont.Font(family='Helvetica', size=12, weight='bold')  # 폰트 설정
    topic_label = tk.Label(scrollable_frame, text=topic, fg='white', bg='#68a6fc', padx=6, font=label_font)
    topic_label.pack(side='left', padx=4, pady=4)
    topic_label.bind("<Button-1>", lambda e, t=topic: on_topic_click(e, t))
    topic_labels.append(topic_label)  # 추후 배경색 변경을 위해 저장


# 뉴스 프레임 생성
news_frame = ttk.Frame(root)
news_frame.pack(fill='both', expand=True, padx=10, pady=10)
# 주제 버튼 생성 코드 뒤에 초기 뉴스 로딩 호출
load_initial_news()

root.mainloop()

