from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from openpyxl import Workbook
import pandas as pd
import time
import sys
import os

#코드 실행 당시의 시간을 변수에 저장
now = time.localtime()
s = '%04d년 %02d월 %02d일 %02d시 %02d분 %02d초' %(now.tm_year, now.tm_mon, now.tm_mday , now.tm_hour, now.tm_min, now.tm_sec)

# WebDriver 설정
print("웹드라이버 설정 시작")
path = ChromeDriverManager().install()
driver = webdriver.Chrome(path)
print("웹드라이버 설정 완료")

# 사용자 입력 받기
keyword = input("1. 크롤링 할 키워드를 입력하세요(예:여행): ")
print("2. 결과에서 반드시 포함하는 단어를 입력하세요(예:국내,바닷가)")
need_words = input("(여러개일 경우 , 로 구분해서 입력하고 없으면 엔터를 입력하세요): ")
print("3. 결과에서 제외할 단어를 입력하세요(예:분양권,해외)")
ban_words =  input("(여러개일 경우 , 로 구분해서 입력하고 없으면 엔터를 입력하세요): ")
day_start = input("4. 조회 시작일자 입력(예:20190101): ")
day_end = input("5. 조회 종료일자 입력(예:20190430): ")
count = int(input("6. 크롤링 할 건수는 몇건인지 입력하세요: "))
file_path = input("7. 파일을 저장할 경로를 입력하세요: ")
save_txt = (f"{file_path}{s} {keyword}.txt")
save_csv = (f"{file_path}{s} {keyword}.csv")
save_xlsx = (f"{file_path}{s} {keyword}.xlsx")

#입력받은 폴더경로가 없을 경우 생성
if not os.path.exists(file_path):
    print(f"입력하신 폴더경로인 {file_path} 가 존재하지 않아 경로 생성 후 크롤링 작업을 진행합니다.")
    os.makedirs(file_path)
else:
    print(f"입력한 경로인 {file_path} 가 존재하어 바로 크롤링 작업을 시작하겠습니다.")

# 크롤링 시작
# URL 설정
url = f"https://search.naver.com/search.naver?where=blog&query={keyword} +%2B{need_words} -{ban_words}&sm=tab_opt&nso=p%3Afrom{day_start}to{day_end}"

# 검색 결과 페이지 요청
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

#크롤링 결과값을 넣을 리스트 생성
blog_posts = soup.find('ul',class_='lst_total')
num = 0
num2 = [ ]
link = [ ]
title = [ ]
content = [ ]
date = [ ]
nickname = [ ]

#txt파일 저장 과정
orig_stdout = sys.stdout
f = open(save_txt, 'a', encoding='UTF-8')
sys.stdout = f

#데이터 수집 (count값만큼 반복문 실행)
for i in blog_posts.find_all('li', 'bx'):
    num2.append(num)
    print(f"=========={num+1}번째 블로그 데이터를 수집합니다.==========")
    
    title_result =  i.find('a', 'api_txt_lines total_tit').get_text()
    title.append(title_result)
    print(f"1. 제목 : {title_result.strip()}")
    
    link_result = i.find('a').get('data-url')
    link.append(link_result)
    print(f"2. 블로그 링크: {link_result.strip()}")    
    
    nickname_result = i.find('a', 'sub_txt sub_name').get_text()
    nickname.append(nickname_result)
    print(f"3. 작성자 닉네임: {nickname_result.strip()}")
    
    date_result = i.find('span', 'sub_time sub_txt').get_text()
    date.append(date_result)
    print(f"4. 작성 일자: {date_result.strip()}")
    
    content_result = i.find('div', 'api_txt_lines dsc_txt').get_text()
    content.append(content_result)
    print(f'5. 내용: {content_result.strip()}')
    
    print("\n")
    
    num += 1
    if num >= count:
        break
    
#xlsx에 넣을 데이터프레임 생성
data = {
    ' ': num2,
    '블로그 제목': title,
    '블로그 링크': link,
    '작성자 닉네임': nickname,
    '작성 일자': date,
    '블로그 내용': content
}
df = pd.DataFrame(data)

#xlsx파일에 넣을 순서 정의
df = df[[' ', "블로그 제목",'블로그 링크', '작성자 닉네임', '작성 일자', '블로그 내용']]

#txt파일 저장 및 종료
sys.stdout = orig_stdout
f.close()

#DataFrame을 csv파일로 저장
df.to_csv(save_csv, index=False)

# DataFrame을 XLSX 파일로 저장합니다
df.to_excel(save_xlsx, index=False)

#종료
print("크롤링 작업을 완료하였습니다.")
driver.close()