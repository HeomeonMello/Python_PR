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
    response_text = get_request_url(api_url)
    if response_text:
        response_json = json.loads(response_text)
        # 여기에서 이미지 URL 대신 뉴스 기사의 제목, 링크, 요약된 내용을 출력합니다.
        for item in response_json.get('items', []):
            print(item.get('title'), item.get('link'))  # 예시 출력
        return response_json
    return None


def get_image_url(image_tag):
    if not image_tag:
        return "No image found"

    # 이미지 URL이 'src' 속성에 있는지 확인
    if image_tag.has_attr('src'):
        return image_tag['src']

    # 'src' 속성이 없는 경우, 다른 속성들을 확인
    for attr in ['data-src', 'data-lazy-src']:
        if image_tag.has_attr(attr):
            return image_tag[attr]

    # 위 조건들에 모두 해당하지 않는 경우
    return "No image found"
def get_politics_headlines():
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100"  # 정치 섹션 URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = soup.select('li.sa_item._SECTION_HEADLINE')

            headlines = []
            for item in news_items:
                title_tag = item.select_one('.sa_text_title .sa_text_strong')
                link_tag = item.select_one('.sa_text_title')
                image_tag = item.select_one('.sa_thumb_link img')

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)

                headlines.append({'title': title, 'link': link, 'image_url': image_url})

            return headlines
        else:
            print("News page request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred during news page request:", e)
    return []

def get_Economy_headlines():
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101"  # 정치 섹션 URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = soup.select('li.sa_item._SECTION_HEADLINE')

            headlines = []
            for item in news_items:
                title_tag = item.select_one('.sa_text_title .sa_text_strong')
                link_tag = item.select_one('.sa_text_title')
                image_tag = item.select_one('.sa_thumb_link img')

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)

                headlines.append({'title': title, 'link': link, 'image_url': image_url})

            return headlines
        else:
            print("News page request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred during news page request:", e)
    return []

def get_Society_headlines():
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102"  # 정치 섹션 URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = soup.select('li.sa_item._SECTION_HEADLINE')

            headlines = []
            for item in news_items:
                title_tag = item.select_one('.sa_text_title .sa_text_strong')
                link_tag = item.select_one('.sa_text_title')
                image_tag = item.select_one('.sa_thumb_link img')

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)

                headlines.append({'title': title, 'link': link, 'image_url': image_url})

            return headlines
        else:
            print("News page request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred during news page request:", e)
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
            news_items = soup.select('li.sa_item._SECTION_HEADLINE')

            headlines = []
            for item in news_items:
                title_tag = item.select_one('.sa_text_title .sa_text_strong')
                link_tag = item.select_one('.sa_text_title')
                image_tag = item.select_one('.sa_thumb_link img')

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)

                headlines.append({'title': title, 'link': link, 'image_url': image_url})

            return headlines
        else:
            print("News page request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred during news page request:", e)
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
            news_items = soup.select('li.sa_item._LAZY_LOADING_WRAP')

            headlines = []
            for item in news_items:
                title_tag = item.select_one('.sa_text_title .sa_text_strong')
                link_tag = item.select_one('.sa_text_title')
                image_tag = item.select_one('.sa_thumb_link img')

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)

                headlines.append({'title': title, 'link': link, 'image_url': image_url})

            return headlines
        else:
            print("News page request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred during news page request:", e)
    return []

def get_IT_headlines():
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105"  # 정치 섹션 URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = soup.select('li.sa_item._SECTION_HEADLINE')

            headlines = []
            for item in news_items:
                title_tag = item.select_one('.sa_text_title .sa_text_strong')
                link_tag = item.select_one('.sa_text_title')
                image_tag = item.select_one('.sa_thumb_link img')

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)

                headlines.append({'title': title, 'link': link, 'image_url': image_url})

            return headlines
        else:
            print("News page request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred during news page request:", e)
    return []

def get_World_headlines():
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=104"  # 정치 섹션 URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = soup.select('li.sa_item._SECTION_HEADLINE')

            headlines = []
            for item in news_items:
                title_tag = item.select_one('.sa_text_title .sa_text_strong')
                link_tag = item.select_one('.sa_text_title')
                image_tag = item.select_one('.sa_thumb_link img')

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)

                headlines.append({'title': title, 'link': link, 'image_url': image_url})

            return headlines
        else:
            print("News page request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred during news page request:", e)
    return []

if __name__ == '__main__':
    if __name__ == "__main__":
        get_news_search_result("Python")