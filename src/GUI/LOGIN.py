from tkinter import Tk, Label, Entry
from PIL import Image, ImageTk

# 창을 생성하고 설정합니다.
root = Tk()
root.geometry('600x650')
root.title("Login")
# 이미지를 불러옵니다.
image_path = 'NewMyroom.png'
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)

# 배경 이미지 레이블을 생성하고 배치합니다.
background_label = Label(root, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# ID 라벨과 입력란을 생성하고 배치합니다.
label_id = Label(root, text="ID:", bg='lightgrey')  # 배경색 설정
label_id.place(relx=0.05, rely=0.02, anchor='nw')  # 왼쪽 상단에 위치

entry_id = Entry(root)
entry_id.place(relx=0.15, rely=0.02, relwidth=0.3, anchor='nw')  # ID 입력란 배치

# 패스워드 라벨과 입력란을 생성하고 배치합니다.
label_pw = Label(root, text="Password:", bg='lightgrey')  # 배경색 설정
label_pw.place(relx=0.55, rely=0.02, anchor='nw')  # 오른쪽 상단에 위치

entry_pw = Entry(root, show="*")
entry_pw.place(relx=0.65, rely=0.02, relwidth=0.3, anchor='nw')  # 패스워드 입력란 배치

root.mainloop()
