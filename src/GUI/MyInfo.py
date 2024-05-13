from tkinter import Tk, Canvas, Entry, Button, font as tkFont, messagebox
from PIL import Image, ImageTk


class MyInfo:
    def __init__(self, root, user_Info = None, access_token= None):
        self.root = root
        self.user_Info = user_Info
        self.access_token = access_token
        self.root.title("내 정보")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        self.canvas = Canvas(self.root, width=600, height=600)
        self.canvas.pack(fill="both", expand=True)

        self.setup_ui()

    def setup_ui(self):
        # 배경 이미지 설정
        image_path = '..\\Image\\me.png'  # 이미지 경로 (Windows 경로 구분자 주의)
        bg_image = Image.open(image_path)
        bg_photo = ImageTk.PhotoImage(bg_image)
        self.bg_image = bg_photo  # 배경 이미지가 garbage collection되지 않도록 참조를 유지
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # 폰트 설정
        entryFont = tkFont.Font(family="Arial", size=10, weight="bold")
        buttonFont = tkFont.Font(family="Arial", size=10, weight="bold")

        # 텍스트 아이템 추가
        self.canvas.create_text(10, 25, text="I'm", font=("Arial", 20, "bold"), fill="black",anchor="w")
        self.user_id_text_item = self.canvas.create_text(60, 45, text="", font=("Arial", 20, "bold"), fill="#aa7dff",anchor="w")
        self.canvas.create_text(10, 80, text="제 이름은 ", font=("Arial", 15, "bold"), fill="black",anchor="w")
        self.user_name_text_item = self.canvas.create_text(105, 80, text="", font=("Arial", 15, "bold"), fill="#aa7dff",anchor="w")
        self.canvas.create_text(10, 110, text="뉴스와 파이썬을 좋아하는 나의 관심사는", font=("Arial", 15, "bold"), fill="black",anchor="w")
        self.interests_text_item = self.canvas.create_text(10, 140, text="", font=("Arial", 15, "bold"), fill="#aa7dff", anchor="w")
        self.canvas.create_text(290, 195, text="관심사를 수정할 수 있습니다.(최대 3개)", font=entryFont, fill="black")

        # 관심사 목록 및 체크박스 상태
        self.interests = ["정치", "경제", "사회", "자동차", "IT/과학", "세계", "건강", "여행/레저", "음식/맛집", "패션/뷰티", "공연/전시", "책", "종교",
                          "날씨"]
        self.interest_check_states = {}
        self.setup_interests()

        register_button = Button(self.root, text=" 정보 변경", command=self.submit,
                                 bg="#ada6ff", fg="black", font=buttonFont,
                                 activebackground="#7c70ff", activeforeground="white",
                                 borderwidth=0, relief='flat')
        self.canvas.create_window(210, 400, window=register_button, anchor="nw", width=160, height=28)

        self.load_user_info()  # 사용자 정보 로드 및 GUI 업데이트

    def setup_interests(self):
        checkbox_start_x = 50
        checkbox_start_y = 220
        checkbox_interval_x = 140
        checkbox_interval_y = 40
        num_columns = 4

        for i, interest in enumerate(self.interests):
            col = i % num_columns
            row = i // num_columns
            x_position = checkbox_start_x + col * checkbox_interval_x
            y_position = checkbox_start_y + row * checkbox_interval_y
            check_id = self.canvas.create_rectangle(x_position, y_position, x_position + 20, y_position + 20,
                                                    outline="#faa0a0", tags=("check", interest))
            self.canvas.create_text(x_position + 35, y_position + 10, text=interest, anchor="w",
                                    font=tkFont.Font(family="Arial", size=10, weight="bold"), tags=("check", interest))
            self.interest_check_states[interest] = (check_id, False)

            self.canvas.tag_bind("check", "<Button-1>", self.on_check)

    def load_user_info(self):

        user_info = self.user_Info
        if user_info:
            user_id = user_info.get('UserID', '')
            user_name = user_info.get('username', '')
            interests_list = user_info.get('interests', [])

            self.canvas.itemconfig(self.user_id_text_item, text=f"{user_id}")
            self.canvas.itemconfig(self.user_name_text_item, text=f"#{user_name}")
            interests_text = ", ".join(["#" + interest for interest in interests_list])
            self.canvas.itemconfig(self.interests_text_item, text=f"{interests_text}")

            for interest in self.interests:
                item_id, _ = self.interest_check_states[interest]
                if interest in interests_list:
                    self.canvas.itemconfig(item_id, fill="#e7ff4a")  # 선택된 관심사에 대해 체크 표시
                    self.interest_check_states[interest] = (item_id, True)
                else:
                    self.canvas.itemconfig(item_id, fill="")  # 선택되지 않은 관심사는 체크 해제
                    self.interest_check_states[interest] = (item_id, False)

    def submit(self):
        from src.Server.Client import update_user_interests
        selected_interests = [interest for interest, (_, state) in self.interest_check_states.items() if state]
        if len(selected_interests) == 0:
            messagebox.showerror("오류", "최소 한 개 이상의 관심사를 선택해야 합니다.")
            return
            # 서버에 관심사 업데이트 요청 보내기
        update_user_interests(self.user_Info['UserID'], selected_interests, self.access_token)

    def on_check(self, event):
        clicked_items = self.canvas.find_withtag("current")
        for item in clicked_items:
            tags = self.canvas.gettags(item)
            for tag in tags:
                if tag in self.interests:
                    item_id, state = self.interest_check_states[tag]
                    selected_count = sum(st for _, st in self.interest_check_states.values())
                    if not state and selected_count >= 3:
                        messagebox.showinfo("제한", "관심사는 최대 3개까지만 선택할 수 있습니다.")
                        return
                    new_state = not state
                    fill_color = "#e7ff4a" if new_state else ""
                    self.canvas.itemconfig(item_id, fill=fill_color)
                    self.interest_check_states[tag] = (item_id, new_state)
                    break


if __name__ == "__main__":
    root = Tk()
    myInfo = {'UserID': 'kkr', 'id': 6, 'interests': ['음식/맛집', '공연/전시', 'IT/과학'], 'username': '김기령'}
    access_token = 'access_token'
    app = MyInfo(root, myInfo,access_token)
    root.mainloop()
