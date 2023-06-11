from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time
import base64 #google검색엔진에 있는 사진은 base64인코딩된 사진이어서 다운받을때 디코딩 필요

# WebDriver로 Chrome을 실행합니다. (크롬 드라이버가 필요합니다)
print("웹드라이버 설정 시작")
path = ChromeDriverManager().install()
driver = webdriver.Chrome(path)
print("웹드라이버 설정 완료")

# 다운받는 시간입력 및 폴더 생성
now = time.localtime()
s = '%04d년 %02d월 %02d일 %02d시 %02d분 %02d초' % (
    now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

# 정보 입력받기
keyword = input("구글에서 다운받을 이미지의 주제를 입력하세요: ")
count = int(input("다운받을 이미지의 개수를 입력하세요: "))
folder_path = input("저장 폴더 경로: ")

url = f"https://www.google.com/search?q={keyword}&tbm=isch"

driver.get(url)
time.sleep(2)

# 이미지 링크 추출을 위해 스크롤 다운
prev_height = driver.execute_script("return document.body.scrollHeight")
while len(driver.find_elements(By.CSS_SELECTOR, 'img.rg_i')) < count:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == prev_height:
        break
    prev_height = new_height

# 이미지 링크 가져오기
image_elements = driver.find_elements(By.CSS_SELECTOR, 'img.rg_i')
image_links = [element.get_attribute("src") for element in image_elements]

# 입력한 폴더 경로가 없을 경우 생성
if not os.path.exists(folder_path):
    print(f"입력하신 폴더 경로인 {folder_path} 가 존재하지 않아 경로를 생성합니다.")
    os.makedirs(folder_path)
else:
    print(f"입력한 경로인 {folder_path} 가 존재하여 이미지를 다운로드합니다.")

# 이미지 다운로드
for index, image_link in enumerate(image_links[:count]):
    try:
        if image_link.startswith('data:image'):
            # 이미지가 base64로 인코딩된 경우 디코딩하여 저장
            image_data = image_link.split(',')[1]
            image_data = base64.b64decode(image_data)
            file_extension = image_link.split(';')[0].split('/')[-1]
            file_path = os.path.join(folder_path, f"{keyword}_{index+1}.{file_extension}")
            with open(file_path, "wb") as file:
                file.write(image_data)
        else:
            # 이미지 링크가 일반 URL인 경우 다운로드
            response = requests.get(image_link)
            image_extension = image_link.split(".")[-1]
            file_path = os.path.join(folder_path, f"{keyword}_{index+1}.{image_extension}")
            with open(file_path, "wb") as file:
                file.write(response.content)

        print(f"이미지 {index+1} 저장 완료")
    except Exception as e:
        print(f"이미지 다운로드 실패: {image_link}")
        print(f"에러 메시지: {str(e)}")

# 크롤링 종료
print("크롤링 작업을 완료하여 종료합니다.")
driver.close()
