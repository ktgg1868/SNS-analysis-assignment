#BeautifulSoup & selenium 호출
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#Webdriver 호출
path = "C:\Python_temp\chromedriver\chromedriver"
driver = webdriver.Chrome(path)

query_txt = "동서대학교" 

driver.get("https://www.naver.com/")
time.sleep(2)

element = driver.find_element(By.ID,"query")

element.send_keys(query_txt)

driver.find_element(By.ID, "search_btn").click() #검색버튼

driver.find_element(By.CSS_SELECTOR,"#lnb > div.lnb_group > div > ul > li:nth-child(3) > a").click() #View탭 접근

driver.find_element(By.CSS_SELECTOR,"#snb > div.api_group_option_filter._search_option_simple_wrap > div > div.option_area.type_sort > a:nth-child(2)").click() #블로그탭에 접근

#text출력
form = driver.page_source
soup = BeautifulSoup(form,'html.parser')
title = soup.find('ul',class_="lst_total")

for i in title:
    print(i.text.strip())
    print("\n")

input() #브라우저 종료 방지