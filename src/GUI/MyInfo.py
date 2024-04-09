import requests
from tkinter import messagebox
from tkinter import Tk, Canvas, Entry, Button, font as tkFont, messagebox
from PIL import Image, ImageTk
import sys

def submit():
    selected_interests = [interest for interest, (_, state) in interest_check_states.items() if state]
    if len(selected_interests) == 0:
        messagebox.showerror("오류", "최소 한 개 이상의 관심사를 선택해야 합니다.")
        return

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
                fill_color = "#e7ff4a" if new_state else ""
                canvas.itemconfig(item_id, fill=fill_color)
                interest_check_states[tag] = (item_id, new_state)
                break

root = Tk()                      # 창을 생성
root.geometry("600x450")         # 창 크기설정
root.title("내 정보")            # 창 제목설정
root.resizable(False, False)     # x, y 창 크기 변경 불가

# 폰트 설정
entryFont = tkFont.Font(family="Arial", size=10,weight="bold")
buttonFont = tkFont.Font(family="Arial", size=10, weight="bold")

image_path = '..\\Image\\me.png'  # 이미지 경로 (Windows 경로 구분자 주의)
bg_image = Image.open(image_path)
bg_photo = ImageTk.PhotoImage(bg_image)

# Canvas 생성 및 배치
canvas = Canvas(root, width=600, height=600)
canvas.pack(fill="both", expand=True)

# 배경 이미지 설정
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

canvas.create_text(30, 25, text="I'm", font=("Arial", 20, "bold"), fill="black")
canvas.create_text(30, 50, text="ID" # ID가 들어갈 자리
                                 ,font=("Arial", 20, "bold"), fill="black")
canvas.create_text(190, 110, text="뉴스와 파이썬을 좋아하는 나의 관심사는" #관심사가 들어갈 자리
                                 , font=("Arial", 15, "bold"), fill="black")
canvas.create_text(100, 140, text="#ㅇㅇ, #ㅇㅇ, #ㅇㅇ" #관심사가 들어갈 자리
                                 , font=("Arial", 15, "bold"), fill="#aa7dff")
# "관심사를 최대 3개까지 골라주세요." 문구 추가
canvas.create_text(290, 195, text="관심사를 수정할 수 있습니다.(최대 3개)", font=entryFont, fill="black")

interests = ["정치", "경제", "사회", "자동차", "IT/과학", "세계", "건강", "여행/레저", "음식/맛집", "패션/뷰티", "공연/전시", "책", "종교", "날씨"]
interest_check_states = {}

checkbox_start_x = 50
checkbox_start_y = 220
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
    check_id = canvas.create_rectangle(x_position, y_position, x_position + 20, y_position + 20, outline="#8175ff", fill="", tags=("check", interest))  # 배경색을 채우지 않음
    canvas.create_text(x_position + 35, y_position + 10, text=interest, anchor="w", font=entryFont, tags=("check", interest))
    # 내부 사각형 추가
    # 내부 사각형의 fill을 ""로 설정하여 투명하게 만듭니다. 여기서는 예시로 배경색을 적용하지 않았습니다만,
    # 실제 사용 환경에서는 적절한 배경색을 적용할 수 있습니다.
    canvas.create_rectangle(x_position, y_position, x_position + 20, y_position + 20, outline="", fill="", tags=("check", interest))
    interest_check_states[interest] = (check_id, False)
canvas.tag_bind("check", "<Button-1>", on_check)

register_button = Button(root, text=" 정보 변경", command=submit,
                         bg="#ada6ff", fg="black", font=buttonFont,
                         activebackground="#7c70ff", activeforeground="white",
                         borderwidth=0, relief='flat')
canvas.create_window(210, 400, window=register_button, anchor="nw", width=160, height=28)


root.mainloop()
