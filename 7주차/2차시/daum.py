#BeautifulSoup & selenium 호출
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#Webdriver 호출
path = "C:\Python_temp\chromedriver\chromedriver"
driver = webdriver.Chrome(path)

query_txt = "동서대학교"

driver.get("https://www.daum.net/")
time.sleep(2)

element = driver.find_element(By.ID,"q")

element.send_keys(query_txt)

driver.find_element(By.CSS_SELECTOR,"#daumSearch > fieldset > div > div > button.ico_pctop.btn_search").click()

input() #브라우저 종료 방지
