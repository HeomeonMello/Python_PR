import urllib.request
from urllib.parse import quote
import json
from bs4 import BeautifulSoup
from html import unescape

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