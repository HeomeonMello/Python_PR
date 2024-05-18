import tkinter as tk
from tkinter import Canvas, font as tkFont, ttk
from PIL import Image, ImageTk
import requests
import json

class Weather:
    def __init__(self, root, user_Info=None, access_token=None):
        self.root = root
        self.user_Info = user_Info
        self.access_token = access_token
        self.root.title("날씨 정보")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        self.canvas = Canvas(self.root, width=600, height=450)
        self.canvas.pack(fill="both", expand=True)

        self.setup_ui()

    def setup_ui(self):
        # 배경 이미지 설정
        image_path = '..\\Image\\Weather.png'  # 경로를 필요에 따라 조정
        try:
            bg_image = Image.open(image_path)
            bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_image = bg_photo  # 가비지 컬렉션을 방지하기 위해 참조를 유지
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except FileNotFoundError:
            print(f"배경 이미지 파일을 {image_path}에서 찾을 수 없습니다. 경로를 확인하세요.")

        # 폰트 설정
        entryFont = tkFont.Font(family="Arial", size=10, weight="bold")
        buttonFont = tkFont.Font(family="Arial", size=10, weight="bold")

        # 텍스트 아이템 추가
        self.canvas.create_text(260, 30, text="날씨 정보", font=("Arial", 20, "bold"), fill="black", anchor="w")

        # 지역 선택 콤보박스 추가
        self.region_label = tk.Label(self.root, text="지역 선택:", font=entryFont)
        self.region_label.place(x=50, y=100)
        self.region_var = tk.StringVar()
        self.region_combobox = ttk.Combobox(self.root, textvariable=self.region_var, font=entryFont)
        self.region_combobox['values'] = ("서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주")
        self.region_combobox.place(x=150, y=100)
        self.region_combobox.bind("<<ComboboxSelected>>", self.get_weather_info)

        # 날씨 정보 표시 라벨
        self.weather_info_label = tk.Label(self.root, text="", font=entryFont)
        self.weather_info_label.place(x=50, y=150)

    def get_weather_info(self, event=None):
        region = self.region_var.get()
        api_key = "https://api.openweathermap.org/data/2.5/weather?lat=123&lon=56&appid=08c43c90ec5fc93f87098f584b7661c3"  # 여기에 OpenWeatherMap API 키를 입력하세요
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": region,
            "appid": api_key,
            "lang": "kr",
            "units": "metric"
        }

        try:
            response = requests.get(base_url, params=params)
            print(f"API 요청 URL: {response.url}")
            weather_data = response.json()
            print(f"응답 데이터: {json.dumps(weather_data, indent=4, ensure_ascii=False)}")

            if weather_data.get("cod") != 200:
                self.weather_info_label.config(text="날씨 정보를 가져올 수 없습니다.")
                return

            description = weather_data["weather"][0]["description"]
            temp = weather_data["main"]["temp"]
            humidity = weather_data["main"]["humidity"]

            weather_info = f"날씨: {description}\n온도: {temp}°C\n습도: {humidity}%"
            self.weather_info_label.config(text=weather_info)

        except Exception as e:
            self.weather_info_label.config(text=f"날씨 정보를 가져오는 데 실패했습니다. 오류: {e}")
            print(f"Exception: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Weather(root)
    root.mainloop()
