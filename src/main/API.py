#API.py
import urllib.request
from urllib.parse import quote
import json
from bs4 import BeautifulSoup
from html import unescape
import requests

client_id = "pk58dq7tnbpRqjUTnE51"
client_secret = "deoKEIaIyh"
# 네이버 Open API URL 정보
base_url = "https://openapi.naver.com/v1/search"
node = "/news.json"

def clean_html(raw_html):
    if not raw_html or '<' not in raw_html:  # HTML 태그가 없거나 비어 있는 경우
        return unescape(raw_html)  # HTML 엔티티를 변환

    try:
        soup = BeautifulSoup(raw_html, "html.parser")
        text = soup.get_text()
        return unescape(text)  # HTML 엔티티를 변환 후 반환
    except Exception as e:
        print("HTML 클리닝 중 오류 발생:", e)
        return unescape(raw_html)  # 예외 발생 시 HTML 엔티티 변환 후 원본 문자열 반환

def get_request_url(api_url):
    req = urllib.request.Request(api_url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            return response.read().decode('UTF-8')
    except Exception as e:
        print("API 요청 중 오류 발생:", e)
        return None

def get_news_search_result(src_text, start=1, display=10):
    api_url = f"{base_url}{node}?query={quote(src_text)}&start={start}&display={display}"
    response_decode = get_request_url(api_url)
    if response_decode:
        return json.loads(response_decode)
    return None

def get_politics_headlines():
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100"  # 정치 섹션 URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 각 뉴스 항목의 구조에 따라 적절한 선택자 사용
            news_items = soup.select('div.sa_text a')

            headlines = []
            for item in news_items:
                title = clean_html(item.text)  # HTML 태그 및 엔티티를 제거
                link = item['href']
                headlines.append({'title': title, 'link': link})
            return headlines
        else:
            print("뉴스 페이지 요청 실패:", response.status_code)
    except Exception as e:
        print("뉴스 페이지 요청 중 오류 발생:", e)
    return []
def get_Economy_headlines():
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101"  # 정치 섹션 URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 각 뉴스 항목의 구조에 따라 적절한 선택자 사용
            news_items = soup.select('div.sa_text a')

            headlines = []
            for item in news_items:
                title = clean_html(item.text)  # HTML 태그 및 엔티티를 제거
                link = item['href']
                headlines.append({'title': title, 'link': link})
            return headlines
        else:
            print("뉴스 페이지 요청 실패:", response.status_code)
    except Exception as e:
        print("뉴스 페이지 요청 중 오류 발생:", e)
    return []
def get_Society_headlines():
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102"  # 정치 섹션 URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 각 뉴스 항목의 구조에 따라 적절한 선택자 사용
            news_items = soup.select('div.sa_text a')

            headlines = []
            for item in news_items:
                title = clean_html(item.text)  # HTML 태그 및 엔티티를 제거
                link = item['href']
                headlines.append({'title': title, 'link': link})
            return headlines
        else:
            print("뉴스 페이지 요청 실패:", response.status_code)
    except Exception as e:
        print("뉴스 페이지 요청 중 오류 발생:", e)
    return []
def get_Life_headlines():
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=103"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 'sh_text_headline' 클래스를 포함하는 <a> 태그 선택
            news_items = soup.select('div.sa_text a')

            headlines = []
            for item in news_items:
                title = clean_html(item.text)  # HTML 태그 및 엔티티 제거하여 제목 추출
                link = item['href']  # 링크 추출
                headlines.append({'title': title, 'link': link})

            return headlines
        else:
            print("뉴스 페이지 요청 실패:", response.status_code)
    except Exception as e:
        print("뉴스 페이지 요청 중 오류 발생:", e)
    return []

def get_Car_headlines():
    # "자동차/시승기" 섹션 URL 수정 필요
    url = "https://news.naver.com/breakingnews/section/103/239"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # "자동차/시승기" 섹션의 뉴스 항목을 찾기 위한 적절한 선택자 사용
            # 페이지 구조에 따라 선택자 수정 필요
            news_items = soup.select('div.sa_text a')

            reviews = []
            for item in news_items:
                title = item.text.strip()  # 제목에서 불필요한 공백 제거
                link = item['href']  # 링크 추출
                reviews.append({'title': title, 'link': link})
            return reviews
        else:
            print("뉴스 페이지 요청 실패:", response.status_code)
    except Exception as e:
        print("뉴스 페이지 요청 중 오류 발생:", e)
    return []
def get_IT_headlines():
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105"  # 정치 섹션 URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 각 뉴스 항목의 구조에 따라 적절한 선택자 사용
            news_items = soup.select('div.sa_text a')

            headlines = []
            for item in news_items:
                title = clean_html(item.text)  # HTML 태그 및 엔티티를 제거
                link = item['href']
                headlines.append({'title': title, 'link': link})
            return headlines
        else:
            print("뉴스 페이지 요청 실패:", response.status_code)
    except Exception as e:
        print("뉴스 페이지 요청 중 오류 발생:", e)
    return []
def get_World_headlines():
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=104"  # 정치 섹션 URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 각 뉴스 항목의 구조에 따라 적절한 선택자 사용
            news_items = soup.select('div.sa_text a')

            headlines = []
            for item in news_items:
                title = clean_html(item.text)  # HTML 태그 및 엔티티를 제거
                link = item['href']
                headlines.append({'title': title, 'link': link})
            return headlines
        else:
            print("뉴스 페이지 요청 실패:", response.status_code)
    except Exception as e:
        print("뉴스 페이지 요청 중 오류 발생:", e)
    return []