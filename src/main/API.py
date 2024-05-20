#src/main/API.py
import urllib.request
from urllib.parse import quote
import json
from bs4 import BeautifulSoup
from html import unescape
import requests
from PIL import Image, ImageTk
from io import BytesIO
import queue
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


def get_news_search_result(src_text, start=1, display=10, sort="date"):  # sort 파라미터 추가
    api_url = f"{base_url}{node}?query={quote(src_text)}&start={start}&display={display}&sort={sort}"
    response_text = get_request_url(api_url)
    if response_text:
        response_json = json.loads(response_text)
        news_items = response_json.get('items', [])
        filtered_news = remove_duplicates(news_items)  # 중복 제거 함수 호출

        detailed_news = []
        for item in filtered_news:
            title = clean_html(item.get('title', 'No title found'))
            originallink = item.get('originallink', 'No original link found')
            link = item.get('link', 'No link found')
            description = clean_html(item.get('description', 'No description found'))
            pubDate = item.get('pubDate', 'No publication date found')

            detailed_news.append({
                'title': title,
                'originallink': originallink,
                'link': link,
                'description': description,
                'pubDate': pubDate,
                # 'image_url': image_url  # 메인 사진 URL 제거
            })

        return detailed_news
    return None




def remove_duplicates(news_items):
    seen_titles = set()
    unique_news = []
    for item in news_items:
        title = item['title']  # 기사의 제목
        if title not in seen_titles:
            seen_titles.add(title)
            unique_news.append(item)
    return unique_news


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
                summary_tag = item.select_one('.sa_text_lede')  # 요약 내용 태그

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)
                summary = summary_tag.text.strip() if summary_tag else "No summary available"

                headlines.append({'title': title, 'link': link, 'image_url': image_url, 'summary': summary})

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
                summary_tag = item.select_one('.sa_text_lede')  # 요약 내용 태그

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)
                summary = summary_tag.text.strip() if summary_tag else "No summary available"

                headlines.append({'title': title, 'link': link, 'image_url': image_url, 'summary': summary})

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
                summary_tag = item.select_one('.sa_text_lede')  # 요약 내용 태그

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)
                summary = summary_tag.text.strip() if summary_tag else "No summary available"

                headlines.append({'title': title, 'link': link, 'image_url': image_url, 'summary': summary})

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
                summary_tag = item.select_one('.sa_text_lede')  # 요약 내용 태그

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)
                summary = summary_tag.text.strip() if summary_tag else "No summary available"

                headlines.append({'title': title, 'link': link, 'image_url': image_url, 'summary': summary})

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
                summary_tag = item.select_one('.sa_text_lede')  # 요약 내용 태그

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)
                summary = summary_tag.text.strip() if summary_tag else "No summary available"

                headlines.append({'title': title, 'link': link, 'image_url': image_url, 'summary': summary})

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
                summary_tag = item.select_one('.sa_text_lede')  # 요약 내용 태그

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)
                summary = summary_tag.text.strip() if summary_tag else "No summary available"

                headlines.append({'title': title, 'link': link, 'image_url': image_url, 'summary': summary})

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
                summary_tag = item.select_one('.sa_text_lede')  # 요약 내용 태그

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)
                summary = summary_tag.text.strip() if summary_tag else "No summary available"

                headlines.append({'title': title, 'link': link, 'image_url': image_url, 'summary': summary})

            return headlines
        else:
            print("News page request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred during news page request:", e)
    return []

def get_Health_headlines():
    # "자동차/시승기" 섹션 URL 수정 필요
    url = "https://news.naver.com/breakingnews/section/103/241"
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
                summary_tag = item.select_one('.sa_text_lede')  # 요약 내용 태그

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)
                summary = summary_tag.text.strip() if summary_tag else "No summary available"

                headlines.append({'title': title, 'link': link, 'image_url': image_url, 'summary': summary})

            return headlines
        else:
            print("News page request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred during news page request:", e)
    return []

def get_Travel_headlines():
    # "자동차/시승기" 섹션 URL 수정 필요
    url = "https://news.naver.com/breakingnews/section/103/237"
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
                summary_tag = item.select_one('.sa_text_lede')  # 요약 내용 태그

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)
                summary = summary_tag.text.strip() if summary_tag else "No summary available"

                headlines.append({'title': title, 'link': link, 'image_url': image_url, 'summary': summary})

            return headlines
        else:
            print("News page request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred during news page request:", e)
    return []
def get_Food_headlines():
    # "자동차/시승기" 섹션 URL 수정 필요
    url = "https://news.naver.com/breakingnews/section/103/238"
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
                summary_tag = item.select_one('.sa_text_lede')  # 요약 내용 태그

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)
                summary = summary_tag.text.strip() if summary_tag else "No summary available"

                headlines.append({'title': title, 'link': link, 'image_url': image_url, 'summary': summary})

            return headlines
        else:
            print("News page request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred during news page request:", e)
    return []
def get_Fashion_headlines():
    # "자동차/시승기" 섹션 URL 수정 필요
    url = "https://news.naver.com/breakingnews/section/103/376"
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
                summary_tag = item.select_one('.sa_text_lede')  # 요약 내용 태그

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)
                summary = summary_tag.text.strip() if summary_tag else "No summary available"

                headlines.append({'title': title, 'link': link, 'image_url': image_url, 'summary': summary})

            return headlines
        else:
            print("News page request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred during news page request:", e)
    return []

def get_Exhibition_headlines():
    # "자동차/시승기" 섹션 URL 수정 필요
    url = "https://news.naver.com/breakingnews/section/103/242"
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
                summary_tag = item.select_one('.sa_text_lede')  # 요약 내용 태그

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)
                summary = summary_tag.text.strip() if summary_tag else "No summary available"

                headlines.append({'title': title, 'link': link, 'image_url': image_url, 'summary': summary})

            return headlines
        else:
            print("News page request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred during news page request:", e)
    return []

def get_Book_headlines():
    # "자동차/시승기" 섹션 URL 수정 필요
    url = "https://news.naver.com/breakingnews/section/103/243"
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
                summary_tag = item.select_one('.sa_text_lede')  # 요약 내용 태그

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)
                summary = summary_tag.text.strip() if summary_tag else "No summary available"

                headlines.append({'title': title, 'link': link, 'image_url': image_url, 'summary': summary})

            return headlines
        else:
            print("News page request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred during news page request:", e)
    return []

def get_Religion_headlines():
    # "자동차/시승기" 섹션 URL 수정 필요
    url = "https://news.naver.com/breakingnews/section/103/244"
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
                summary_tag = item.select_one('.sa_text_lede')  # 요약 내용 태그

                title = clean_html(title_tag.text) if title_tag else "No title found"
                link = link_tag['href'] if link_tag else "No link found"
                image_url = get_image_url(image_tag)
                summary = summary_tag.text.strip() if summary_tag else "No summary available"

                headlines.append({'title': title, 'link': link, 'image_url': image_url, 'summary': summary})

            return headlines
        else:
            print("News page request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred during news page request:", e)
    return []


def get_entertainment_headlines():
    url = "https://entertain.naver.com/now"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Selecting news items based on the 'li' within class 'news_lst news_lst2'
    news_items = soup.select('.news_lst.news_lst2 li')

    headlines = []
    for item in news_items:
        # Check if necessary elements exist to avoid errors
        title_element = item.find('a', class_='tit')
        image_element = item.find('img')
        summary_element = item.find('p', class_='summary')

        if title_element and image_element and summary_element:
            title = title_element.get_text(strip=True)
            link = title_element['href']
            image_url = image_element['src'] if image_element.has_attr('src') else None
            summary = summary_element.get_text(strip=True)

            headlines.append({
                'title': title,
                'link': link,
                'image_url': image_url,
                'summary': summary
            })

    return headlines

def get_trending_keywords():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    keyword_url = "https://coinpan.com/free"
    try:
        response = requests.get(keyword_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        keyword_list = soup.select('.realtimeranking_widget_content.popular ul li a')

        if not keyword_list:
            print("No keywords found on the page.")
            return ["테스트 키워드1", "테스트 키워드2"], [10, 9]  # 테스트 데이터 반환

        keywords = []
        popularity = []

        for index, keyword in enumerate(keyword_list, start=1):
            rank = keyword.find('span').text.strip()
            keyword_text = keyword.get_text().strip().replace(rank, '').strip()
            keywords.append(keyword_text)
            popularity.append(11 - index)

        return keywords, popularity
    except requests.RequestException as e:
        print(f"Failed to load page: {e}")
        return ["테스트 키워드1", "테스트 키워드2"], [10, 9]

class ImageLoader:
    def __init__(self, root, image_queue):
        self.root = root
        self.image_queue = image_queue

    def load_image_async(self, image_url, image_label):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                img_data = BytesIO(response.content)
                image = Image.open(img_data).resize((100, 100))
                photo = ImageTk.PhotoImage(image)
                self.image_queue.put((image_label, photo))  # 큐에 (레이블, 이미지) 튜플 추가
            else:
                print(f"Failed to load image, status code: {response.status_code}")
        except Exception as e:
            print(f"Error loading image: {e}")

    def start_image_update_loop(self):
        try:
            while not self.image_queue.empty():
                image_label, photo = self.image_queue.get_nowait()
                image_label.configure(image=photo)
                image_label.image = photo  # 참조 유지
        except queue.Empty:
            pass
        finally:
            # 100ms 후에 이 메소드를 다시 호출하여 큐를 확인
            self.root.after(100, self.start_image_update_loop)

    def load_image(self, image_url):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                img_data = BytesIO(response.content)
                pil_image = Image.open(img_data).resize((100, 100))
                return ImageTk.PhotoImage(pil_image)
            else:
                print(f"Failed to load image, status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
