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
                # 상태 변경 전에 선택된 관심사의 수를 검사
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

    if len(selected_interests) == 0:
        messagebox.showerror("오류", "최소 한 개 이상의 관심사를 선택해야 합니다.")
        return

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
for i, interest in enumerate(interests):
    col = i % num_columns
    row = i // num_columns
    x_position = checkbox_start_x + col * checkbox_interval_x
    y_position = checkbox_start_y + row * checkbox_interval_y
    check_id = canvas.create_rectangle(x_position, y_position, x_position + 20, y_position + 20, outline="#faa0a0", fill="", tags=("check", interest))  # 배경색을 채우지 않음
    canvas.create_text(x_position + 35, y_position + 10, text=interest, anchor="w", font=entryFont, tags=("check", interest))
    # 내부 사각형 추가
    # 내부 사각형의 fill을 ""로 설정하여 투명하게 만듭니다. 여기서는 예시로 배경색을 적용하지 않았습니다만,
    # 실제 사용 환경에서는 적절한 배경색을 적용할 수 있습니다.
    canvas.create_rectangle(x_position, y_position, x_position + 20, y_position + 20, outline="", fill="", tags=("check", interest))
    interest_check_states[interest] = (check_id, False)
canvas.tag_bind("check", "<Button-1>", on_check)

# 회원가입 버튼
# 회원가입 버튼 추가 및 스타일 꾸미기
register_button = Button(root, text="회원가입", command=submit,
                         bg="#d5f7d7", fg="black", font=buttonFont,
                         activebackground="lightgreen", activeforeground="white", borderwidth=1)
canvas.create_window(170, 600, window=register_button, anchor="nw", width=260, height=28)

root.mainloop()