from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  

query_text: str = input("크롤링 할 키워드는 무엇입니까?: ").strip()
while True:
    filename: str = input("검색 결과를 저장할 파일 이름을 입력해주세요 (파일 확장자 포함, 예시: file): ").strip()
    if len(filename) > 0:
        break

chrome_driver_path = ChromeDriverManager().install()
driver = webdriver.Chrome(chrome_driver_path)

driver.maximize_window()

driver.get("https://korean.visitkorea.or.kr/main/main.do")
driver.implicitly_wait(30)

# 검색창 포커싱
driver.find_element(By.CSS_SELECTOR, "#inp_search").click()
driver.find_element(By.CSS_SELECTOR, "#inp_search").send_keys(query_text, Keys.ENTER)

driver.implicitly_wait(30)

# 목록 로딩 대기 (원하는 엘리먼트의 노출을 대기할 수 있음)
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#listBody > ul > li"))
)

soup = BeautifulSoup(driver.page_source, 'html.parser')
content_list = soup.select('#listBody > ul > li')
text_result = '\n'.join(list(map(
    lambda v: v.text.strip(),
    content_list
    )))

if content_list is not None:
    print(text_result)
else:
    print('Content list not found')

with open(f"{filename}.txt", "w", encoding="utf8",) as fp:
    fp.write(text_result)