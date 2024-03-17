# register.py 파일 내용
from tkinter import Tk, Canvas, Entry, Button, font as tkFont
from PIL import Image, ImageTk

def submit_register():
    # 회원 가입 처리 로직
    print("회원 가입 로직 실행")

root = Tk()
root.geometry('600x650')
root.title("회원가입")
root.resizable(False, False)

# 폰트 설정
entryFont = tkFont.Font(family="Arial", size=10,weight="bold")
buttonFont = tkFont.Font(family="Arial", size=10, weight="bold")
# 배경 이미지 설정
bg_image_path = 'register.png'
bg_image = Image.open(bg_image_path).resize((600, 650), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# 캔버스 설정 및 배경 이미지 추가
canvas = Canvas(root, width=600, height=650)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# 회원가입 폼 (사용자 이름, ID, 비밀번호, 비밀번호 확인)
entry_y_start = 200  # 시작 y 위치
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

# 회원가입 버튼
# 회원가입 버튼 추가 및 스타일 꾸미기
register_button = Button(root, text="회원가입", command=submit_register,
                         bg="#d5f7d7", fg="black", font=buttonFont,
                         activebackground="lightgreen", activeforeground="white", borderwidth=1)
canvas.create_window(170, 425, window=register_button, anchor="nw", width=260, height=28)

root.mainloop()