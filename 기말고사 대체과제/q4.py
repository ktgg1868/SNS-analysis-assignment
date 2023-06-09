from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time

# WebDriver로 Chrome을 실행합니다. (크롬 드라이버가 필요합니다)
print("웹드라이버 설정 시작")
path = ChromeDriverManager().install()
driver = webdriver.Chrome(path)
print("웹드라이버 설정 완료")

#정보 입력받기
keyword = input("구글에서 다운받을 pdf의 주제를 입력하세요: ")
count = int(input("다운받을 pdf파일의 개수를 입력하세요: "))
folder_path = input("저장폴더경로: ")

url = "https://www.google.com/search?q=" + keyword

driver.get(url)
html = driver.page_source
soup = bs(html, 'html.parser')
elements = soup.find_all('span', class_='ZGwO7 s4H5Cf C0kchf NaCKVc yUTMj VDgVie')
href_list = []

#검색결과에서 pdf파일로 연결되는 하이퍼링크 찾아서 리스트에 추가하기
while len(href_list) < count:
    time.sleep(3)
    html = driver.page_source
    soup = bs(html, 'html.parser')
    elements = soup.find_all('a')
    for element in elements:
        href = element.get('href')
        if href and href.endswith('.pdf'):
            href_list.append(href)
            if len(href_list) == count:
                break
    driver.find_element(By.TAG_NAME,'body').send_keys(Keys.END)
    
    next_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#pnnext'))  # 다음 페이지 버튼을 찾음
    )
    next_button.click()
    
    continue


#입력받은 폴더경로가 없을 경우 생성
if not os.path.exists(folder_path):
    print(f"입력하신 폴더경로인 {folder_path} 가 존재하지 않아 경로 생성 후 다운로드 진행합니다.")
    os.makedirs(folder_path)
else:
    print(f"입력한 경로인 {folder_path} 가 존재하어 바로 PDF 다운로드하겠습니다.")

#리스트의 주로에서 파일 받아오기
for index, href in enumerate(href_list):
    response = requests.get(href)
    file_path = os.path.join(folder_path, f"{keyword} 검색결과 {index+1}.pdf")
    with open(file_path, 'wb') as f:
        f.write(response.content)
    print(f"PDF 파일 {index+1} 저장 완료")

print("크롤링 작업을 완료하여 종료합니다.")
driver.close()