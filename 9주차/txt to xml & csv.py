from bs4 import BeautifulSoup     
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import xlwt
import time
import sys

#키워드 및 파일이름 & 파일경로 지정
keyword = input("크롤링할 키워드는 무엇입니까?: ")
f_name = input("검색 결과를 저장할 txt 파일경로와 이름을 지정하세요(c:\\py_temp\\파일이름.txt): ")
fc_name = input("검색 결과를 저장할 csv 파일경로와 이름을 지정하세요(c:\\py_temp\\파일이름.csv): ")
fx_name = input("검색 결과를 저장할 xls 파일경로와 이름을 지정하세요(c:\\py_temp\\파일이름.xlsx): ")

#크롬드리아버 자동업데이트 및 지정
path = ChromeDriverManager().install()
driver = webdriver.Chrome(path)

#네이버 호출
driver.get("https://www.naver.com")
driver.implicitly_wait(10)

#검색창에 키워드 입력 및 검색
search_bar = driver.find_element(By.ID, "query")
search_bar.send_keys(keyword)
driver.find_element(By.ID, "search-btn").click()
driver.implicitly_wait(10)

#블로그탭으로 이동
driver.find_element(By.LINK_TEXT,"VIEW").click()
driver.implicitly_wait(10)

driver.find_element(By.LINK_TEXT, "블로그").click()
driver.implicitly_wait(10)

#텍스트부분을 BeautifulSoup으로 추출
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
content_list = soup.find('ul',class_='lst_total')


# 각 항목별로 분리하여 추출하고 변수에 할당하기
num = 1
num2 = [ ]
title2 = [ ]
content2 = [ ]
date2 = [ ]
nickname2 = [ ]

for i in content_list.find_all('li', 'bx'):
    num2.append(num)
    print('1.번호:',num)
    
    title = i.find('a', 'api_txt_lines total_tit').get_text()
    title2.append(title)
    print('2.제목:',title.strip())
    
    content = i.find('div', 'api_txt_lines dsc_txt').get_text()
    content2.append(content)
    print('3.내용:',content.strip())
    
    date = i.find('span', 'sub_time sub_txt').get_text()
    date2.append(date)
    print('4.작성날짜:',date.strip())
    
    nickname = i.find('a', 'sub_txt sub_name').get_text()
    nickname2.append(nickname)
    print('5.닉네임:',nickname.strip())
    print("\n")
    
    num += 1
    if num >= 10:
        break

#데이터형태를 표로 변환
result = pd.DataFrame()
result['번호'] = num2
result['내용'] = content2
result['작성날짜'] = date2
result['닉네임'] = nickname2

# txt 파일로 저장하기
f = open(f_name, 'a',encoding='UTF-8')
f.write(str(title2))
f.write(str(content2))
f.write(str(date2))
f.write(str(nickname2))
f.close( )
print(" txt 파일 저장 경로: %s" %f_name)  

# csv 형태로 저장하기
result.to_csv(fc_name, encoding="utf-8-sig",index=False)
print(" csv 파일 저장 경로: %s" %fc_name)

# 엑셀 형태로 저장하기
result.to_excel(fx_name,index=False)
print(" xls 파일 저장 경로: %s" %fx_name)

