from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import sys
import time

keyword = "동서대학교"

path = ChromeDriverManager().install()
driver = webdriver.Chrome(path)

driver.get("https://www.naver.com")
driver.implicitly_wait(10)

search_bar = driver.find_element(By.ID, "query")
search_bar.send_keys(keyword)
driver.find_element(By.ID, "search_btn").click()
driver.implicitly_wait(10)

driver.find_element(By.LINK_TEXT,"VIEW").click()
driver.implicitly_wait(10)

driver.find_element(By.LINK_TEXT, "블로그").click()
driver.implicitly_wait(10)

full_html = driver.page_source

soup = BeautifulSoup(full_html, 'html.parser')

content_title = soup.find('ul',class_='total_area')

#content_title = driver.find_elements(By.CSS_SELECTOR,'.total_wrap api_ani_send')


f_name = ("c:\\py_temp\\test123.txt")

orig_stdout = sys.stdout
f = open(f_name, 'a' , encoding='UTF-8')
sys.stdout = f
time.sleep(1)

for i in content_title:
    #title = content_title.find_element(By.CSS_SELECTOR, 'total_area').text
    print(i.text.strip())
    print("\n")

sys.stdout = orig_stdout
f.close()


input()