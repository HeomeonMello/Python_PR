from tkinter import Tk, Canvas, Entry, Button, font as tkFont
from PIL import Image, ImageTk
import subprocess
import os

# register.py 파일의 절대 경로
script_path = os.path.abspath("register.py")
def login_action():
    print("로그인 시도")  # 실제 로그인 로직으로 대체해야 함

def register_action():
    subprocess.run(["python", script_path], check=True)

root = Tk()
root.geometry('600x650')
root.title("Login")
root.resizable(False, False)

# 폰트를 더 현대적인 'Arial'로 변경하고, 크기와 굵기를 조정합니다.
buttonFont = tkFont.Font(family="Arial", size=10, weight="bold")

image_path = 'NewMyroom.png'
image = Image.open(image_path).resize((600, 650), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)

canvas = Canvas(root, width=600, height=650)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=photo, anchor="nw")

id_text_x, id_text_y = 27, 535
password_text_x, password_text_y = 325, 535
canvas.create_text(id_text_x, id_text_y, text="ID:", fill="black", anchor="nw")
canvas.create_text(password_text_x, password_text_y, text="Password:", fill="black", anchor="nw")

entry_id = Entry(root)
entry_pw = Entry(root, show="●")
canvas.create_window(id_text_x + 30, id_text_y - 2, window=entry_id, anchor="nw", width=180)
canvas.create_window(password_text_x + 70, password_text_y - 2, window=entry_pw, anchor="nw", width=180)

login_button = Button(root, text="로그인", command=login_action,
                      bg="#e6f4ff", fg="black", font=buttonFont,
                      activebackground="lightblue", activeforeground="white", borderwidth=1)
register_button = Button(root, text="회원가입", command=register_action,
                         bg="#d5f7d7", fg="black", font=buttonFont,
                         activebackground="lightgreen", activeforeground="white", borderwidth=1)
canvas.create_window(170, 388, window=login_button, anchor="nw", width=260, height=28)
canvas.create_window(170, 425, window=register_button, anchor="nw", width=260, height=28)

root.mainloop()
