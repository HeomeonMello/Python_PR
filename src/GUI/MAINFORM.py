import urllib.request
from urllib.parse import quote
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, messagebox, Canvas, Frame, Scrollbar, font as tkFont
import json
import webbrowser
from PIL import Image, ImageTk
import io
import link
from bs4 import BeautifulSoup


import sys
sys.path.append("..\\main")  # 상위 디렉토리로 올라간 뒤 main 폴더로 내려감
from src.main.API import client_id, client_secret

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

def about():
    messagebox.showinfo("정보", "개인화된 뉴스 피드 애플리케이션입니다.\n원하시는 키워드는 검색하실 수 있습니다.")

def privacy():
    messagebox.showinfo("내 정보", "자신이 선택한 주제입니다.\n")

def exit_app():
    response = messagebox.askyesno("종료", "애플리케이션을 종료하시겠습니까?")
    if response:
        root.destroy()

def open_info_window():
    new_window = tk.Toplevel(root)
    new_window.title("내 정보")
    new_window.geometry("1200x800")
    tk.Label(new_window, text="이곳은 사용자의 정보를 보여주는 창입니다.").pack()

def open_fav_news_window():
    new_window = tk.Toplevel(root)
    new_window.title("내 관심 뉴스 골라보기")
    new_window.geometry("1200x800")
    tk.Label(new_window, text="이곳은 사용자의 관심 뉴스를 보여주는 창입니다.").pack()

def open_similar_news_window():
    new_window = tk.Toplevel(root)
    new_window.title("최근 열람한 기사와 비슷한 내용의 기사")
    new_window.geometry("1200x800")
    tk.Label(new_window, text="이곳은 최근 열람한 기사와 비슷한 내용의 기사를 보여주는 창입니다.").pack()

# 메인 윈도우 설정
root = tk.Tk()
root.title("개인화된 뉴스 피드")
root.geometry("1700x800")

# 메뉴 바 생성
menu_bar = tk.Menu(root)

# 도움말 메뉴
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="정보", command=about)
menu_bar.add_cascade(label="내정보", command=privacy)
menu_bar.add_cascade(label="도움말", menu=help_menu)

# 파일 메뉴
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="종료", command=exit_app)
menu_bar.add_cascade(label="현재 창 종료", menu=file_menu)


# 메뉴 바를 윈도우에 추가
root.config(menu=menu_bar)

# 검색창 프레임 설정
search_frame = tk.Frame(root, bg='#68a6fc')
search_frame.pack(fill='x', pady=10)

# 좌측 메뉴 프레임 설정
menu_frame = tk.Frame(root, bg='#68a6fc')
menu_frame.pack(fill='y', side='left', padx=10)

# 메뉴 버튼 스타일 설정
menu_button_font = tkFont.Font(family='Helvetica', size=12)

# '내 정보' 버튼
btn_my_info = tk.Button(menu_frame, text='내 정보', font=menu_button_font, command=open_info_window)
btn_my_info.pack(fill='x', pady=5)

# '내 관심 뉴스 골라보기' 버튼
btn_fav_news = tk.Button(menu_frame, text='내 관심 뉴스 골라보기', font=menu_button_font, command=open_fav_news_window)
btn_fav_news.pack(fill='x', pady=5)

# '최근 열람한 기사와 비슷한 내용의 기사' 버튼
btn_similar_news = tk.Button(menu_frame, text='최근 열람한 기사와 비슷한 내용의 기사', font=menu_button_font, command=open_similar_news_window)
btn_similar_news.pack(fill='x', pady=5)

# 검색창 입력 필드
search_entry = tk.Entry(search_frame, font=('Helvetica', 14), width=40)
search_entry.pack(side='left', padx=(10, 0), pady=10)

# 검색 버튼 이미지 로드 및 설정
search_img = Image.open('../Image/search.png')  # 이미지 파일 위치
search_img = search_img.resize((25, 25)) # 이미지 사이즈 조절
search_photo = ImageTk.PhotoImage(search_img)



# 캔버스 생성 및 검색 프레임에 추가
# 캔버스 생성 및 검색 프레임에 추가, 테두리 없음 설정
search_canvas = Canvas(search_frame, width=30, height=30, bg='#68a6fc', highlightthickness=0, bd=0)  # 캔버스 크기 및 배경색, 테두리 설정
search_canvas.pack(side='left', padx=10, pady=10)

# 캔버스 위에 이미지 배치
# 이미지 사이즈 조절이 이미 되어있으므로, 캔버스 크기에 맞게 조절한 이미지 사용
canvas_image = search_canvas.create_image(17, 17, image=search_photo)  # 캔버스 중앙에 이미지 배치

# 캔버스에 마우스 클릭 이벤트 바인딩하여 검색 기능 실행
def on_canvas_click(event):
    handle_search()

search_canvas.bind("<Button-1>", on_canvas_click)  # 마우스 왼쪽 버튼 클릭 시 이벤트 연결

# 엔터 키를 눌렀을 때 검색이 되도록 바인딩, 함수 호출 수정
search_entry.bind('<Return>', handle_search)

# 뉴스 항목을 Canvas 위에 표시하는 함수

# 뉴스 프레임과 스크롤바를 포함한 Canvas 설정



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

