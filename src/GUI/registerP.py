# registerP.py 파일 내용
import requests
from tkinter import messagebox
from tkinter import Tk, Canvas, Entry, Button, font as tkFont, messagebox
from PIL import Image, ImageTk
import sys

import src.Server.Client

sys.path.append("../Server")  # 상위 디렉토리로 올라간 뒤 GUI 폴더로 내려감
from src.Server.Client import submit_register

def on_check(event):
    clicked_items = canvas.find_withtag("current")
    for item in clicked_items:
        tags = canvas.gettags(item)
        for tag in tags:
            if tag in interests:
                item_id, state = interest_check_states[tag]
                # 상태 변경 전에 선택된 관심사의 수를 검사123
                selected_count = sum(st for _, st in interest_check_states.values())
                if not state and selected_count >= 3:
                    messagebox.showinfo("제한", "관심사는 최대 3개까지만 선택할 수 있습니다.")
                    return
                new_state = not state
                fill_color = "#faa0a0" if new_state else ""
                canvas.itemconfig(item_id, fill=fill_color)
                interest_check_states[tag] = (item_id, new_state)
                break


def submit():
    username = entry_username.get()
    user_id = entry_id.get()
    password = entry_password.get()
    password_confirm = entry_password_confirm.get()
    selected_interests = [interest for interest, (_, state) in interest_check_states.items() if state]

    # 입력 필드가 비어 있는지 검사
    if not username.strip():
        messagebox.showerror("오류", "사용자 이름을 입력해주세요.")
        return
    if not user_id.strip():
        messagebox.showerror("오류", "ID를 입력해주세요.")
        return
    if not password.strip():
        messagebox.showerror("오류", "비밀번호를 입력해주세요.")
        return
    if not password_confirm.strip():
        messagebox.showerror("오류", "비밀번호 확인을 입력해주세요.")
        return
    # 비밀번호 일치 여부 검사
    if password != password_confirm:
        messagebox.showerror("오류", "비밀번호가 일치하지 않습니다.")
        return
    if len(selected_interests) == 0:
        messagebox.showerror("오류", "최소 한 개 이상의 관심사를 선택해야 합니다.")
        return
    # submit_register 함수를 수정하여 매개변수로 필요한 데이터를 전달합니다.
        # 입력 검증 로직 후
    if password == password_confirm:
        src.Server.Client.submit_register(username, password, user_id, selected_interests)
    else:
        messagebox.showerror("오류", "비밀번호가 일치하지 않습니다.")


root = Tk()
root.geometry('600x650')
root.title("회원가입")
root.resizable(False, False)

# 폰트 설정
entryFont = tkFont.Font(family="Arial", size=10,weight="bold")
buttonFont = tkFont.Font(family="Arial", size=10, weight="bold")
# 배경 이미지 설정
bg_image_path = '../Image/Register.png'
bg_image = Image.open(bg_image_path).resize((600, 650), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# 캔버스 설정 및 배경 이미지 추가
canvas = Canvas(root, width=600, height=650)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# 회원가입 폼 (사용자 이름, ID, 비밀번호, 비밀번호 확인)
entry_y_start = 210  # 시작 y 위치
entry_height = 20  # 엔트리 박스 높이
entry_interval = 50  # 엔트리 간격

# 사용자 이름
canvas.create_text(150, entry_y_start, text="사용자 이름:", fill="black", font=entryFont, anchor="e")
entry_username = Entry(root, font=entryFont)
canvas.create_window(160, entry_y_start - entry_height/2, window=entry_username, anchor="nw", width=330, height=entry_height)

# ID
canvas.create_text(150, entry_y_start + entry_interval, text="ID:", fill="black", font=entryFont, anchor="e")
entry_id = Entry(root, font=entryFont)
canvas.create_window(160, entry_y_start + entry_interval - entry_height/2, window=entry_id, anchor="nw", width=330, height=entry_height)

# 비밀번호
canvas.create_text(150, entry_y_start + 2*entry_interval, text="비밀번호:", fill="black", font=entryFont, anchor="e")
entry_password = Entry(root, show="●", font=entryFont)
canvas.create_window(160, entry_y_start + 2*entry_interval - entry_height/2, window=entry_password, anchor="nw", width=330, height=entry_height)

# 비밀번호 확인
canvas.create_text(150, entry_y_start + 3*entry_interval, text="비밀번호 확인:", fill="black", font=entryFont, anchor="e")
entry_password_confirm = Entry(root, show="●", font=entryFont)
canvas.create_window(160, entry_y_start + 3*entry_interval - entry_height/2, window=entry_password_confirm, anchor="nw", width=330, height=entry_height)

# "관심사를 최대 3개까지 골라주세요." 문구 추가
canvas.create_text(295, 407, text="관심사를 골라주세요(최대 3개)", font=entryFont, fill="black")

interests = ["정치", "경제", "사회", "자동차", "IT/과학", "세계", "건강", "여행/레저", "음식/맛집", "패션/뷰티", "공연/전시", "책", "종교", "날씨"]
interest_check_states = {}

checkbox_start_x = 50
checkbox_start_y = 433
checkbox_interval_x = 140
checkbox_interval_y = 40
num_columns = 4

for i, interest in enumerate(interests):
    col = i % num_columns
    row = i // num_columns
    x_position = checkbox_start_x + col * checkbox_interval_x
    y_position = checkbox_start_y + row * checkbox_interval_y
    check_id = canvas.create_rectangle(x_position, y_position, x_position + 20, y_position + 20, outline="#faa0a0", tags=("check", interest))
    canvas.create_text(x_position + 35, y_position + 10, text=interest, anchor="w", font=entryFont, tags=("check", interest))
    interest_check_states[interest] = (check_id, False)

canvas.tag_bind("check", "<Button-1>", on_check)

# 회원가입 버튼
# 회원가입 버튼 추가 및 스타일 꾸미기
register_button = Button(root, text="회원가입", command=submit,
                         bg="#d5f7d7", fg="black", font=buttonFont,
                         activebackground="lightgreen", activeforeground="white", borderwidth=1)
canvas.create_window(170, 600, window=register_button, anchor="nw", width=260, height=28)

root.mainloop()