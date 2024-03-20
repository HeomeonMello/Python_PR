import requests
import tkinter as tk
from tkinter import messagebox
import sys

class Client:
    def __init__(self, server_url):
        self.server_url = server_url

    def check_server(self):
        """서버 연결을 확인합니다."""
        try:
            response = requests.get(f"{self.server_url}/ping")  # 서버 상태 확인을 위한 엔드포인트
            if response.status_code == 200:
                print("서버 연결 성공")
                return True
            else:
                print("서버 연결 실패:", response.text)
                return False
        except requests.exceptions.RequestException as e:
            print("서버 연결 실패:", e)
            return False


    def login(self, username, password):
        """서버에 로그인을 시도하고 결과를 반환합니다."""
        login_endpoint = f"{self.server_url}/login"
        data = {'username': username, 'password': password}
        try:
            response = requests.post(login_endpoint, json=data)
            if response.status_code == 200:
                print("로그인 성공")
                return True
            else:
                print("로그인 실패:", response.text)
                return False
        except requests.exceptions.RequestException as e:
            print("서버 연결 실패:", e)
            return False

def login_action():
    sys.path.append("../GUI")  # 상위 디렉토리로 올라간 뒤 GUI 폴더로 내려감
    from src.GUI.LOGIN import entry_id, entry_pw
    username = entry_id.get()  # 사용자가 입력한 ID를 가져옵니다.
    password = entry_pw.get()  # 사용자가 입력한 비밀번호를 가져옵니다.

    # 서버의 로그인 엔드포인트 URL
    login_url = "http://localhost:5000/login"

    # 로그인 요청을 위한 데이터
    data = {'username': username, 'password': password}

    try:
        # 서버로 POST 요청을 보냅니다.
        response = requests.post(login_url, json=data)

        if response.status_code == 200:
            # 로그인 성공
            messagebox.showinfo("로그인 성공", "성공적으로 로그인되었습니다.")
            # 여기에 로그인 성공 후의 로직을 추가할 수 있습니다. 예: 메인 화면으로 전환
        else:
            # 로그인 실패 (서버에서 200 이외의 상태 코드 반환)
            messagebox.showerror("로그인 실패", "ID 또는 비밀번호가 잘못되었습니다.")
    except requests.exceptions.RequestException as e:
        # 서버 연결 실패 등의 네트워크 오류 처리
        messagebox.showerror("서버 연결 실패", "서버에 연결할 수 없습니다. 네트워크 상태를 확인해주세요.")

def create_gui():
    sys.path.append("../GUI")  # 상위 디렉토리로 올라간 뒤 GUI 폴더로 내려감
    from src.GUI.LOGIN import root
    root.mainloop()

if __name__ == "__main__":
    server_url = "http://localhost:5000"
    client = Client(server_url)

    if client.check_server():
        print("서버와 연결되었습니다.")
        create_gui()  # 서버에 연결되면 로그인 GUI를 생성하고 표시
    else:
        print("서버에 연결할 수 없습니다.")
        messagebox.showerror("연결 실패", "서버에 연결할 수 없습니다. 서버 상태를 확인하고 다시 시도해주세요.")
        sys.exit(1)