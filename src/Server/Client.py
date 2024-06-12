import requests
from tkinter import messagebox, Tk
import threading
import tkinter as tk
import sys
import os
import asyncio
class Client:
    def __init__(self, server_url, userid=None, access_token=None):
        self.server_url = server_url
        self.userid = userid
        self.access_token = access_token
        self.user_info = None  # user_info 초기화

    def check_server(self):
        try:
            response = requests.get(f"{self.server_url}/ping")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def save_user_click(self, news_title, news_description, news_url, publish_time):
        save_url = f"{self.server_url}/save_click"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "user_id": self.userid,
            "news_title": news_title,
            "news_description": news_description,
            "news_url": news_url,
            "publish_time": publish_time
        }
        try:
            print(data)
            response = requests.post(save_url, json=data, headers=headers)
            if response.status_code == 200:
                print("Click saved successfully")
            else:
                print("Failed to save click")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def get_user_data(self):
        url = f"{self.server_url}/user_data"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.user_info = data
                return data
            else:
                print("Failed to get user data")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def scrape_and_store(self):
        scrape_url = f"{self.server_url}/scrape_and_store"
        try:
            response = requests.post(scrape_url)
            if response.status_code == 200:
                print("News articles scraped and stored successfully")
            else:
                print("Failed to scrape and store news articles")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

def login_action():
    from src.GUI.MAINFORM import NewsFeedApp
    from src.GUI.LOGIN import entry_id, entry_pw, root
    username = entry_id.get()
    password = entry_pw.get()

    login_url = f"{os.getenv('SERVER_URL', 'http://localhost:5000')}/login"
    data = {'username': username, 'password': password}

    try:
        response = requests.post(login_url, json=data)
        if response.status_code == 200:
            # 로그인 성공 시, 로그인 창 숨기기
            root.withdraw()
            response_data = response.json()
            access_token = response_data['access_token']

            # 메인 폼 생성 및 사용자 정보 전달
            main_root = tk.Toplevel()  # 메인 폼을 위한 새로운 창 생성
            app = NewsFeedApp(main_root, username, access_token)
            Client.userid = app.userid
            Client.access_token = access_token
            get_user_info()

            # 사용자 데이터 확인 및 알고리즘 실행
            client = Client(f"{os.getenv('SERVER_URL', 'http://localhost:5000')}", username, access_token)
            user_data = client.get_user_data()

            def run_algorithm():
                if user_data:
                    from src.main.Algorithm import recommend_articles  # TensorFlow를 사용하는 모듈 동적으로 불러오기
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    recommended_articles = loop.run_until_complete(recommend_articles(user_data, access_token, client.server_url))
                    app.display_recommended_articles(recommended_articles)  # 추천된 기사를 알고리즘 프레임에 표시

            # 알고리즘을 백그라운드 스레드에서 실행
            threading.Thread(target=run_algorithm).start()

            def on_close():
                root.destroy()  # 전체 애플리케이션 종료

            main_root.protocol("WM_DELETE_WINDOW", on_close)  # 닫힘 이벤트 핸들러 등록

            main_root.mainloop()
        else:
            # 로그인 실패 (서버에서 200 이외의 상태 코드 반환)
            messagebox.showerror("로그인 실패", "ID 또는 비밀번호가 잘못되었습니다.")
    except requests.exceptions.RequestException as e:
        # 서버 연결 실패 등의 네트워크 오류 처리
        messagebox.showerror("서버 연결 실패", "서버에 연결할 수 없습니다. 네트워크 상태를 확인해주세요.")

def submit_register(username, password, user_id, selected_interests):
    server_url = f"{os.getenv('SERVER_URL', 'http://localhost:5000')}/register"
    data = {
        'username': username,
        'password': password,
        'userid': user_id,
        'interests': selected_interests
    }
    try:
        response = requests.post(server_url, json=data)
        if response.status_code == 201:
            messagebox.showinfo("회원가입 성공", "정상적으로 회원가입이 완료되었습니다. 로그인 창으로 돌아가 로그인 해주세요.")
        else:
            messagebox.showerror("오류", "이미 있는 ID 입니다. 다른 ID를 사용해 주세요")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("오류", "서버 연결 실패")

def open_Myinfo_window():
    from src.GUI.MyInfo import MyInfo
    try:
        user_info = get_user_info()
        access_token = Client.access_token

        if user_info:
            my_info_root = tk.Toplevel()
            my_info_app = MyInfo(my_info_root, user_info, access_token)
            my_info_root.mainloop()
        else:
            messagebox.showerror("오류", "사용자 정보를 가져올 수 없습니다.")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("오류", "내 정보 창을 열 수 없습니다.")

def get_user_info():
    access_token = Client.access_token
    userinfo_url = f"{os.getenv('SERVER_URL', 'http://localhost:5000')}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(userinfo_url, headers=headers)
        if response.status_code == 200:
            Client.user_info = response.json()
        else:
            print("사용자 정보를 가져오는 데 실패했습니다.")
        return Client.user_info
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def update_user_interests(user_id, new_interests, access_token):
    server_url = f"{os.getenv('SERVER_URL', 'http://localhost:5000')}/update_interests"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'interests': new_interests
    }
    try:
        response = requests.put(server_url, json=data, headers=headers)
        if response.status == 200:
            messagebox.showinfo("성공", "관심사가 성공적으로 업데이트 되었습니다.")
        else:
            messagebox.showerror("실패", "관심사 업데이트에 실패했습니다.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("오류", f"서버와의 연결에 실패했습니다: {e}")

def create_gui():
    sys.path.append("../GUI")
    from src.GUI.LOGIN import root
    root.mainloop()

def start_scrape_and_store(client):
    scrape_thread = threading.Thread(target=client.scrape_and_store)
    scrape_thread.start()

if __name__ == "__main__":
    server_url = os.getenv('SERVER_URL', 'http://localhost:5000')
    client = Client(server_url)

    if client.check_server():
        start_scrape_and_store(client)  # 서버 연결 시 스크래핑 시작
        create_gui()
    else:
        messagebox.showerror("연결 실패", "서버에 연결할 수 없습니다. 서버 상태를 확인하고 다시 시도해주세요.")
