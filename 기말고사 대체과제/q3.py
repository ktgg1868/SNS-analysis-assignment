from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import requests

def down_images(search_query, download_path, num_images):
    # Pixabay API 정보 입력
    api_key = '37047723-0c361e630de66c41f0139d791' #개인 pixabay api key
    api_url = f'https://pixabay.com/api/?key={api_key}&q={search_query}&image_type=photo'

    # 요청한 개수만큼 이미지 다운로드
    response = requests.get(api_url)
    data = response.json()
    hits = data['hits'][:num_images]

    # 다운로드 경로가 없다면 생성
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # 이미지 다운로드 및 저장
    for i, hit in enumerate(hits):
        image_url = hit['webformatURL']
        image_filename = f'image_{i+1}.jpg'
        image_path = os.path.join(download_path, image_filename)

        # 이미지 다운로드 요청
        image_response = requests.get(image_url)
        with open(image_path, 'wb') as image_file:
            image_file.write(image_response.content)

        print(f'{image_filename} 다운로드 완료')

#변수 선언
search_query = input('검색어를 입력하세요: ')
num_images = int(input('다운로드할 이미지의 개수를 입력하세요: '))
download_path = input('이미지를 저장할 경로를 입력하세요: ')

#함수 실행
down_images(search_query, download_path, num_images)