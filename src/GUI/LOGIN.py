from tkinter import Tk, Canvas, Entry, Button, font as tkFont
from PIL import Image, ImageTk
import subprocess
import os  # 운영체제에 독립적인 경로 처리를 위해 추가
from src.Server.Client import login_action

# 상수 정의
WINDOW_SIZE = '600x650'
LOGIN_IMAGE_PATH = os.path.join('..', 'Image', 'NewMyroom.png')  # 운영체제에 독립적인 경로 처리
BUTTON_FONT = ("Arial", 10, "bold")
LABEL_FONT = ("Arial", 11)  # 라벨 폰트 추가
BUTTON_COLORS = {
    "login": {"bg": "#e6f4ff", "fg": "black", "activebg": "lightblue", "activefg": "white"},
    "register": {"bg": "#d5f7d7", "fg": "black", "activebg": "lightgreen", "activefg": "white"}
}

def create_button(text, command, color_key, x, y, w, h):
    """버튼을 생성하고 배치하는 함수"""
    return Button(root, text=text, command=command, font=BUTTON_FONT,
                  bg=BUTTON_COLORS[color_key]["bg"], fg=BUTTON_COLORS[color_key]["fg"],
                  activebackground=BUTTON_COLORS[color_key]["activebg"],
                  activeforeground=BUTTON_COLORS[color_key]["activefg"],
                  borderwidth=1).place(x=x, y=y, width=w, height=h)

def open_register_window():
    root.withdraw()
    subprocess.run(["python", os.path.join("..", "GUI", "registerP.py")], check=True)
    root.deiconify()

root = Tk()
root.geometry(WINDOW_SIZE)
root.title("Login")
root.resizable(False, False)

# 배경 이미지 설정
image = Image.open(LOGIN_IMAGE_PATH).resize((600, 650), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)
canvas = Canvas(root, width=600, height=650)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=photo, anchor="nw")

# 라벨 추가
canvas.create_text(27, 535, text="ID :", fill="black", anchor="nw", font=LABEL_FONT)
canvas.create_text(307, 535, text="Password :", fill="black", anchor="nw", font=LABEL_FONT)

# 입력 필드 배치
entry_id = Entry(root)
entry_pw = Entry(root, show="●")
canvas.create_window(60, 533, window=entry_id, anchor="nw", width=180)
canvas.create_window(390, 533, window=entry_pw, anchor="nw", width=180)

# 버튼 배치
create_button("로그인", login_action, "login", 170, 388, 260, 28)
create_button("회원가입", open_register_window, "register", 170, 425, 260, 28)

root.mainloop()
