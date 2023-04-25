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

driver.find_element(By.ID, "search_btn").click()

input() #브라우저 종료 방지