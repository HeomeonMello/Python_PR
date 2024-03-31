from tkinter import Tk, Canvas, Entry, Button, font as tkFont
from PIL import Image, ImageTk
import subprocess
import sys
sys.path.append("../Server")  # 상위 디렉토리로 올라간 뒤 GUI 폴더로 내려감
from src.Server.Client import login_action

def open_register_window():
    # 로그인 창 숨기기
    root.withdraw()
    # 회원가입 파일 실행
    subprocess.run(["python", "..\\GUI\\registerP.py"], check=True)
    root.deiconify()  # subprocess 실행이 완료된 후, 로그인 창 다시 보이기

root = Tk()
root.geometry('600x650')
root.title("Login")
root.resizable(False, False)

# 폰트를 'Arial'로 변경하고, 크기와 굵기를 조정
buttonFont = tkFont.Font(family="Arial", size=10, weight="bold")

#상대경로로 배경사진을 지정후 600X650창의 크기로 설정
image_path = '..\\Image\\NewMyroom.png'
image = Image.open(image_path).resize((600, 650), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)

#canvas 메소드를 이용해서 배경화면을 설정
canvas = Canvas(root, width=600, height=650)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=photo, anchor="nw")

#id 라벨을 만들고, id 입력 칸을 생성합니다.
id_text_x, id_text_y = 27, 535
password_text_x, password_text_y = 325, 535
canvas.create_text(id_text_x, id_text_y, text="ID:", fill="black", anchor="nw")
canvas.create_text(password_text_x, password_text_y, text="Password:", fill="black", anchor="nw")

#비밀번호 라벨을 만들고, 비밀번호 칸을 생성합니다. ++ 비밀번호는 보안상 화면에 보여지면 안되기 때문에 ●로 표시합니다.
entry_id = Entry(root)
entry_pw = Entry(root, show="●")
canvas.create_window(id_text_x + 30, id_text_y - 2, window=entry_id, anchor="nw", width=180)
canvas.create_window(password_text_x + 70, password_text_y - 2, window=entry_pw, anchor="nw", width=180)

#로그인 버튼설정입니다. 로그인 버튼의 배경화면 색깔을"#e6f4ff"로 지정하고 글씨색깔을 검은 색으로 지정하고 폰트는 위에서 정의된것 처럼 폰트를 지정
login_button = Button(root, text="로그인", command=login_action,
                      bg="#e6f4ff", fg="black", font=buttonFont, #클릭 하지 않았을 때 버튼의 색깔
                      activebackground="lightblue", activeforeground="white", borderwidth=1) #클릭 했을 때 변경되는 색깔

#회원가입 버튼의 설정 "d5f7d7"로 지정, 글씨체 검은색, 폰트 설정까지.
register_button = Button(root, text="회원가입", command=open_register_window,
                         bg="#d5f7d7", fg="black", font=buttonFont,
                         activebackground="lightgreen", activeforeground="white", borderwidth=1)#클릭 했을 때 변경되는 색깔

#설정이 완료된 로그인 버튼을 좌표 170,388에 배치, 회원가입 버튼을 170,425에 배치.
canvas.create_window(170, 388, window=login_button, anchor="nw", width=260, height=28)
canvas.create_window(170, 425, window=register_button, anchor="nw", width=260, height=28)

root.mainloop()