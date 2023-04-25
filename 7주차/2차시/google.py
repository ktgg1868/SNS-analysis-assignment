#BeautifulSoup & selenium 호출
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#Webdriver 호출
path = "C:\Python_temp\chromedriver\chromedriver"
driver = webdriver.Chrome(path)

query_txt = "동서대학교"

driver.get("https://www.google.com/")
time.sleep(2)

element = driver.find_element(By.CLASS_NAME,"gLFyf")

element.send_keys(query_txt)

driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[1]").click()

input() #브라우저 종료 방지