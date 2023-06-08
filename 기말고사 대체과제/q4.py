##구글에서 pdf파일 다운로드 받기

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

def download_pdf(url, save_dir):
    response = requests.get(url, stream=True)
    filename = unquote(url.split("/")[-1])  # URL에서 파일명 추출 및 디코딩
    save_path = os.path.join(save_dir, filename)
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

def download_pdf_from_googleSearch(keyword, save_dir):
    # Google 검색 URL
    search_url = f"https://www.google.com/search?q={keyword}&btnI"

    # 검색 결과 페이지 요청
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # PDF 파일 링크 추출
    pdf_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.endswith('.pdf'):
            pdf_links.append(href)

    # PDF 파일 다운로드
    if pdf_links:
        for i, link in enumerate(pdf_links):
            pdf_url = link
            download_pdf(pdf_url, save_dir)
            print(f"다운로드 완료: {pdf_url}")
    else:
        print("PDF 파일을 찾을 수 없습니다.")

# 키워드 입력
keyword = input("검색할 키워드를 입력하세요: ")
save_dir = input("파일을 저장할 디렉토리를 입력하세요: ")

# 크롤링 시작
download_pdf_from_googleSearch(keyword, save_dir)