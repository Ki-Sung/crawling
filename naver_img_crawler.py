# 0. 크롤링에 필요한 패키지 모듈 불러오기 
# 웹드라이버와 옵션등을 위한 패키지 
from bs4 import BeautifulSoup                                 # BeautifulSoup 패키지
from selenium import webdriver                                # Selenium 크롬드라이버 패키지
from selenium.webdriver.common.keys import Keys               # Key 모듈 패키지

# IP 우회를 위한 페이크 유저 모듈
from fake_useragent import UserAgent   # 페이크 유저
import random                          # 랜덤 숫자 출력을 위한 패키지

# 컴퓨터 디렉토리 작업과 url을 받기 위한 패키지들
import os                               # os 모듈
from urllib.parse import quote_plus     # url 아스키코드 변환을 위한 모듈
from urllib.request import urlretrieve  # 이미지 저장을 위한 모듈 

# 작업 진행상황 표시를 위한 패키지 모듈 불러오기 
from tqdm import tqdm_notebook as tq    # 진행표시바를 위한 모듈
import time                             # 시간데이터를 다루기 위한 모듈 
import datetime                         # 날짜와 시간을 다루기 위한 모듈

# 경고 표시 무시 
import warnings
warnings.filterwarnings(action='ignore')

# 1. 크롬 드라이버 옵션 및 url 접속
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

# 크롬 드라이버 옵션 지정 및 url 받기
driver = webdriver.Chrome(chrome_options=options)  # 크롬 드라이버 path 지정 및 옵션 지정
keyword = input("키워드를 입력해주세요: ")   # 키워드 입력 
url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=image&query=" + quote_plus(keyword)  # 검색한 키워드 아스키 코드로 바꾼다음 해당 페이지로 이동
driver.get(url)     # url 받기 
time.sleep(5)   # 로딩 시간 조정

# 2. 스크롤 내리기 
print("스크롤 내리는 중...")
# 우선 봇 의심을 피하기 위해 로딩 시간 random하게 조정 
pause_time = random.randint(3, 9)

# 스크롤 범위 반복횟수 (1번 부터 4번 까지)
for i in range(1,5):
    # 웹창을 클릭 후 END키를 누르는 동작
    driver.find_element_by_xpath('//body').send_keys(Keys.END)
    # 로딩 시간 조정 
    time.sleep(pause_time)

pause_time = random.randint(2, 4)
time.sleep(pause_time)

print("스크롤 완료")

# 3. 폴더 생성
# 폴더 생성 옵션
# 만약 해당 경로에 폴더가 없다면 생성
if not os.path.exists(os.path.abspath('../naver_img/' + f'{keyword}')):
    os.makedirs(os.path.abspath('../naver_img/' + f'{keyword}'))
    print('폴더 생성 완료')
else:
    # 동일한 폴더가 있으면 이미 동일한 폴더가 있다고 안내
    print('이미 동일한 이름의 폴더가 있습니다.')

# 파일 이름에 날짜 시간을 위해 datetime 사용
now = datetime.datetime.now()
now = str(now).replace(' ','')

# 4. 이미지 추출하기
# beautifusoup으로 파싱하여 이미지 'src' 속성값 가져오기 
print("이미지 추출하기")
soup = BeautifulSoup(driver.page_source, 'lxml')
img = soup.select('img._listImage')
img[0]['src']

# src 속성값 가져와서 리스트에 저장
imgSrc = []
for i in img:
    imgSrc.append(i['src'])

# urlretrieve: url로 표시된 네터워크 객체(url 주소의 문서)를 로컬 파일로 저장 (직접 다운로드 가능)
# 파일 이름 생성 후 이미지 저장
fileNo = 0
for i in tq(range(len(imgSrc))):
    urlretrieve(imgSrc[i], os.path.abspath('../naver_img/' + f'{keyword}') + '/' + f"naver{keyword}_{now}_" + str(fileNo)  + ".jpg")
    fileNo += 1
    time.sleep(3)

print("이미지 추출 및 저장 완료")

# 5. 크롬브라우져 닫기
driver.close()