from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import time

#웹드라이버 설정
print("웹드라이버 설정 시작")
path = ChromeDriverManager().install()
driver = webdriver.Chrome(path)
print("웹드라이버 설정 완료")

print("================================================================")
print("pixabay 사이트에서 이미지를 검색하여 수집하는 크롤러 입니다")
print("================================================================")

#변수 선언
search_query = input('1. 크롤링할 이미지의 키워드는 무엇입니까?: ')
num_images = int(input('2. 크롤링 할 건수는 몇건입니까?: '))
file_path = input('3. 파일이 저장도리 경로를 입력하세요(예: c:\data\): ')

#입력받은 폴더경로가 없을 경우 생성
if not os.path.exists(file_path):
    print(f"입력하신 폴더경로인 {file_path} 가 존재하지 않아 경로 생성 후 다운로드 진행합니다.")
    os.makedirs(file_path)
else:
    print(f"입력한 경로인 {file_path} 가 존재하어 바로 이미지를 다운로드하겠습니다.")

#pixabay 개인으로 할당된 API key 입력
api_key = "37047723-0c361e630de66c41f0139d791"

#pixabay 검색 url 선언
url = f"https://pixabay.com/api/?key={api_key}&q={search_query}&image_type=photo"

#다운받는 시간입력 및 폴더 생성
now = time.localtime()
s = '%04d년 %02d월 %02d일 %02d시 %02d분 %02d초' %(now.tm_year, now.tm_mon, now.tm_mday , now.tm_hour, now.tm_min, now.tm_sec)

os.chdir(file_path)
os.makedirs(file_path + s + ' - ' + search_query)
os.chdir(file_path + s + ' - ' + search_query)
f_path = file_path + s + ' - ' + search_query

#다운받을 이미지 개수만큼 다운받기
response = requests.get(url)
data = response.json()
hits = data['hits'][:num_images]

#다운로드 시작
for i, hit in enumerate(hits):
    image_url = hit['webformatURL']
    image_filename = f'image_{i+1}.jpg'
    image_path = os.path.join(f_path, image_filename)

    image_response = requests.get(image_url)
    with open(image_path, 'wb') as image_file:
        image_file.write(image_response.content)
        
    print(f'{image_filename} 다운로드 완료')
    