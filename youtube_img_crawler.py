# 크롤링에 필요한 패키지 모듈 불러오기 
from bs4 import BeautifulSoup
from selenium import webdriver

from fake_useragent import UserAgent
import random

import os
from urllib.parse import quote_plus

import time
import datetime

# 데이터 판다스로 정리하기 위해 판다스 패키지 불러오기 
import pandas as pd

import warnings
warnings.filterwarnings(action='ignore')

# 랜덤으로 생성한 UserAgent 값 출력 
ua = UserAgent()
userAgent = ua.random
print(userAgent)

# chrome dirver 옵션
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={userAgent}')  # fake user 표시
options.add_argument('headless')                 # 크롬브라우저 숨기기
options.add_argument('window-size=1920,1080')    # 모니터 해상도 지정
options.add_argument('disable-gpu')              # CPU 부담을 줄이고 GPU로 그래픽 가속

# 유튜브 접속, 검색 
driver = webdriver.Chrome(chrome_options=options)
url = 'https://www.youtube.com/'
driver.get(url)
time.sleep(3)
driver.find_element_by_xpath('//*[@id="return-to-youtube"]').click() # 버전호환 문제로 최신 업데이트 팝업이 뜸, '나중에' 버튼 클릭 
time.sleep(3)
keyword = input("키워드를 입력해주세요: ")
url = "https://www.youtube.com/results?search_query=" + quote_plus(keyword)  # 검색한 키워드 아스키 코드로 바꾼다음 해당 페이지로 이동
driver.get(url)
time.sleep(3)

# 스크롤바 내리기 
last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    time_sleep = random.randint(1, 8)
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(time_sleep)
    new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    time_sleep = random.randint(2, 9)
    if new_page_height == last_page_height:
        time.sleep(time_sleep)
        if new_page_height == driver.execute_script("return document.documentElement.scrollHeight"):
            break
    else:
        last_page_height = new_page_height

# 폴더 생성 옵션
# 폴더의 존재유무파악 (같은 이름 X)
# os: 파일 경로를 찾아줌
# 만약 해당 경로에 폴더가 없다면 생성
if not os.path.exists(os.path.abspath('../youtube_img/' + f'{keyword}')):
    os.makedirs(os.path.abspath('../youtube_img/' + f'{keyword}'))
    print('폴더 생성 완료')
else:
    # 동일한 폴더가 있으면 이미 동일한 폴더가 있다고 안내
    print('이미 동일한 이름의 폴더가 있습니다.')


# 파일 이름에 날짜 시간을 위해 datetime 사용
now = datetime.datetime.now()
now = str(now).replace(' ','')

# 정보 가져오기 
html_source = driver.page_source
soup = BeautifulSoup(html_source, 'lxml')

elem = soup.find_all("ytd-video-renderer", attrs={"class":'style-scope ytd-item-section-renderer'})

# 필요한 정보 가져오기
df = []
for t in elem:
    title = t.find("yt-formatted-string", attrs={"class":'style-scope ytd-video-renderer'}).get_text()
    name = t.find("a", attrs={"class":'yt-simple-endpoint style-scope yt-formatted-string'}).get_text()
    thumbnail = t.find('img', attrs={'class':'style-scope yt-img-shadow'}).get('src')
    content_url = t.find("a", attrs={"class":'yt-simple-endpoint style-scope ytd-video-renderer'})["href"]
    df.append([name, title , thumbnail,  'https://www.youtube.com/'+content_url])

driver.close()

df_list = pd.DataFrame(columns=['title', 'name', 'thumbnail_link', 'url_link'])

# 자료 넣기 
for i in range(len(df)):
    df_list.loc[i] = df[i]

df_dir = '../youtube_img/'
df_list.to_csv(df_dir + f"{keyword}" + '/' + f"youtube{keyword}_{now}_df.csv")
