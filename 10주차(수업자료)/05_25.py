from bs4 import BeautifulSoup     
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys

query_txt = input('크롤링할 키워드는 무엇입니까?: ')
f_name = input('검색 결과를 저장할 파일경로와 이름을 지정하세요(ex: c:\\data\\test.txt): ')

#Step 2. 크롬 드라이버를 사용해서 웹 브라우저를 실행합니다.
path = "c:/python_temp/chromedriver/chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("https://korean.visitkorea.or.kr/main/main.do")
time.sleep(2)  #  창이 모두 열릴 때 까지 2초 기다립니다.
driver.implicitly_wait(2)

try:
  driver.find_element(By.XPATH, '/html/body/div[6]/button').click()

except:
  print("팝업창이 없습니다.")

driver.find_element(By.ID,'placeHolder').click()
element = driver.find_element(By.ID,'inp_search')
element.click()
element.send_keys(query_txt)
element.send_keys(Keys.ENTER)

time.sleep(2)

full_html = driver.page_source

soup = BeautifulSoup(full_html, 'html.parser')
content_list = soup.find('ul', class_='list_thumType type1')

for i in content_list:
  print(i.text.strip())
  print('\n')
  
orig_stdout = sys.stdout
f = open(f_name, 'a', encoding='UTF-8')
sys.stdout = f
time.sleep(1)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
content_list = soup.find('ul', class_='list_thumType type1')

if content_list is not None:
  for i in content_list:
    print(i.text.strip())
    print("\n")
  
  else:
    print('Content list is not found')
  
sys.stdout = orig_stdout
f.close()

print("요청하신 데이터 수집 작업이 정상적으로 완료되었습니다.")