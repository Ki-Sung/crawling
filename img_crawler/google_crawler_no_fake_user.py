# 0. 크롤링에 필요한 패키지 모듈 불러오기 
# 웹드라이버와 옵션등을 위한 패키지
from selenium import webdriver  # Selenium 크롬드라이버 패키지
from selenium.webdriver.common.keys import Keys  # Key 모듈 패키지
from webdriver_manager.chrome import ChromeDriverManager  # 웹드라이버 매니저 패키지

# 랜덤 숫자 출력을 위한 패키지
import random

# 컴퓨터 디렉토리 작업과 url을 받기 위한 패키지들
import os  # os 모듈
import urllib  # url 파싱 및 호출을 위한 urllib 모듈
from urllib.request import urlopen  # url을 가져오기 위한 모듈

# 작업 진행상황 표시를 위한 패키지 모듈 불러오기 
from tqdm import tqdm_notebook as tq  # 진행표시바를 위한 모듈
import time  # 시간데이터를 다루기 위한 모듈
import datetime  # 날짜와 시간을 다루기 위한 모듈

# 경고 표시 무시 
import warnings

warnings.filterwarnings(action='ignore')

# 1. 크롬드라이버 옵션 설정 및 url 접속 
# chrome dirver 옵션
options = webdriver.ChromeOptions()  # 크롬 드라이버 옵션 설정
options.add_argument('headless')     # 크롬브라우저 숨기기
options.add_argument('window-size=1920,1080')  # 모니터 해상도 지정
options.add_argument('disable-gpu')  # 불필요한 GPU 기능을 제거해서 셀레니움 작동 속도를 올려주는 옵션

# 구글 옵션
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)  # 크롬 드라이버를 따로 설치하지 않고 사용할 수 있는 방법
url = 'https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl'  # 구글 이미지 검색 url
driver.get(url)  # url 받기
elem = driver.find_element_by_name('q')  # 구글 검색창 선택
keyword = input("키워드를 입력하세요: ")  # 검색 키워드 입력
elem.send_keys(keyword)  # 카워드 받기
elem.send_keys(Keys.RETURN)  # 검색 버튼 누르기

# 2. 스크롤 옵션 
print("스크롤 내리는 중")
pause_time = random.randint(3, 9)
time.sleep(pause_time)
last_height = driver.execute_script('return document.body.scrollHeight')  # 스크롤 높이 가져오기

while True:
    pause_time = random.randint(2, 8)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')  # 끝까지 스크롤 내리기
    time.sleep(pause_time)
    new_height = driver.execute_script('return document.body.scrollHeight')  # 스크롤 내린 후 스크롤 높이 다시 가져오기

    pause_time = random.randint(3, 6)
    if new_height == last_height:
        try:
            driver.find_element_by_css_selector(".mye4qd").click()  # 새로운 높이가 이전 높이와 같다면, 결과 더보기 클릭하기
        except:
            break
    last_height = new_height
time.sleep(pause_time)
print("스크롤 완료")

# 3. 폴더 생성 옵션과 날짜 시간 설정
# 만약 해당 경로에 폴더가 없다면 생성
if not os.path.exists(os.path.abspath('../google_img/' + f'{keyword}')):
    os.mkdir(os.path.abspath('../google_img/' + f'{keyword}'))
    print('폴더 생성 완료')
else:
    # 동일한 폴더가 있으면 이미 동일한 폴더가 있다고 안내
    print('이미 동일한 이름의 폴더가 있습니다.')

# 파일 이름에 날짜 시간을 위해 datetime 사용
now = datetime.datetime.now()
now = str(now).replace(' ', '')

# 4. 이미지 추출
print("이미지를 추출 합니다.")
img_url = []
imges = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
cnt = 1
for img in tq(imges):
    try:
        pause_time = random.randint(2, 8)
        img.click()
        time.sleep(pause_time)
        imgUrl = driver.find_element_by_xpath(
            "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div/a/img").get_attribute(
            'src')
        img_url.append(imgUrl)
        urllib.request.urlretrieve(imgUrl, os.path.abspath(
            '../google_img/' + f'{keyword}') + '/' + f"google_{keyword}_{now}_" + str(cnt) + ".jpg")
        cnt += 1
    except:
        pass
print("이미지 추출 및 저장이 완료되었습니다.")

# 5. 크롬드라이버 닫기
driver.close()
