from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import time

#웹드라이버 설치
print("웹드라이버 설정 시작")
path = ChromeDriverManager().install()
driver = webdriver.Chrome(path)
print("웹드라이버 설정 완료")

#키워드 및 날짜 입력 && 저장위치 받아오기
#search_name = input("1. 공고명으로 검색하 키워드는 무엇입니까? ")
#date_start = input("2. 조회 시작일자 입력(ex: 2019/01/01): ")
#date_end = input("3. 조회 종료일자 입력(ex: 2019/03/31): ")
#folder_directory = input("4. 저장할 폴더를 입력하세요(ex: c:\data\): ")

search_name = "캠프"
date_start = "2019/01/01"
date_end = "2019/03/31"

#페이지 접속
url = "https://www.g2b.go.kr/index.jsp"
driver.get(url)
driver.implicitly_wait(5)

#키워드 및 날짜 입력 후 검색
searchbar = driver.find_element(By.ID, "bidNm")
searchbar.clear()    
searchbar.send_keys(search_name)

s_date = driver.find_element(By.ID, "fromBidDt")
s_date.send_keys(date_start)

e_date = driver.find_element(By.ID, "toBidDt")
e_date.send_keys(date_end)

driver.find_element(By.CLASS_NAME, "btn_dark").click()

#검색 후 로딩 대기
driver.implicitly_wait(3)

soup = bs(driver.page_source, "html.parser")
content_list = soup.find_all("tr", class_="results")

if not content_list:
    print("자료가 없습니다.")
else:
    for content in content_list:
        print(content.text.strip())
        print("\n")



input()
