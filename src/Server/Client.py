import requests
from tkinter import messagebox, Tk
from src.GUI.MAINFORM import NewsFeedApp
import tkinter as tk
import sys
import subprocess
class Client:

    def __init__(self, server_url,userid = None,access_token = None):
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



def login_action():
    from src.GUI.LOGIN import entry_id, entry_pw,root
    username = entry_id.get()
    password = entry_pw.get()

    login_url = "http://localhost:5000/login"
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
    """회원가입 등록 로직 클라이언트와 연동"""
    # 서버의 회원가입 엔드포인트 URL
    server_url = "http://localhost:5000/register"

    # 서버로 전송할 데이터
    data = {
        'username': username,
        'password': password,
        'userid': user_id,  # 'name' 필드가 실제 이름이라면, GUI에서 이에 해당하는 별도의 입력 필드를 추가해야 합니다.
        'interests': selected_interests
    }
    print(username, password, user_id, selected_interests)
    try:
        # 서버로 POST 요청 보내기
        response = requests.post(server_url, json=data)

        # 응답 처리
        if response.status_code == 201:
            messagebox.showinfo("회원가입 성공", "정상적으로 회원가입이 완료되었습니다. 로그인 창으로 돌아가 로그인 해주세요 ")
            # 회원가입 성공 메시지 표시, 로그인 페이지로 이동 등의 추가 작업 수행
        else:
            messagebox.showerror("오류", "이미 있는 ID 입니다. 다른 ID를 사용해 주세요")
            # 서버에서 반환한 오류 메시지를 사용자에게 표시
    except requests.exceptions.RequestException as e:
        messagebox.showerror("오류", "서버 연결 실패")
        # 서버 연결 실패 메시지 표시


def open_Myinfo_window():
    from src.GUI.MyInfo import MyInfo
    try:
        user_info = get_user_info()  # get_user_info 함수를 호출하여 사용자 정보를 가져옵니다.
        access_token = Client.access_token

        if user_info:
            # MyInfo 창을 생성하고 초기화합니다.
            my_info_root = tk.Toplevel()  # 새 창을 위한 Toplevel 생성
            my_info_app = MyInfo(my_info_root, user_info,access_token)  # MyInfo 애플리케이션 인스턴스 생성
            my_info_root.mainloop()
        else:
            messagebox.showerror("오류", "사용자 정보를 가져올 수 없습니다.")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("오류", "내 정보 창을 열 수 없습니다.")

def get_user_info():
    access_token = Client.access_token

    userinfo_url = "http://localhost:5000/userinfo"  # f-string은 여기서 필요하지 않습니다.
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers)
    if response.status_code == 200:
        Client.user_info = response.json()
    else:
        print("사용자 정보를 가져오는 데 실패했습니다.")
    return Client.user_info


def update_user_interests(user_id, new_interests, access_token):
    """서버에 관심사 업데이트 요청을 보내는 함수"""
    print(access_token)
    server_url = "http://localhost:5000/update_interests"  # 서버 주소
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'interests': new_interests
    }
    try:
        response = requests.put(server_url, json=data, headers=headers)
        if response.status_code == 200:
            messagebox.showinfo("성공", "관심사가 성공적으로 업데이트 되었습니다.")
        else:
            messagebox.showerror("실패", "관심사 업데이트에 실패했습니다.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("오류", f"서버와의 연결에 실패했습니다: {e}")


def create_gui():
    sys.path.append("../GUI")  # 상위 디렉토리로 올라간 뒤 GUI 폴더로 내려감
    from src.GUI.LOGIN import root
    root.mainloop()


if __name__ == "__main__":
    server_url = "http://localhost:5000"
    client = Client(server_url)

    if client.check_server():
        create_gui()
    else:
        messagebox.showerror("연결 실패", "서버에 연결할 수 없습니다. 서버 상태를 확인하고 다시 시도해주세요.")
