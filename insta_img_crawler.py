# 0. 크롤링에 필요한 패키지 모듈 불러오기 
# 웹드라이버와 옵션등을 위한 패키지 
from bs4 import BeautifulSoup  # BeautifulSoup 패키지
from selenium import webdriver  # Selenium 크롬드라이버 패키지

# IP 우회를 위한 페이크 유저 모듈
from fake_useragent import UserAgent  # 페이크 유저
import random  # 랜덤 숫자 출력을 위한 패키지

# pass word 입력값을 감추기 위한 패키지
import getpass

# 컴퓨터 디렉토리 작업과 url을 받기 위한 패키지들
import os  # os 모듈
import requests  # API 요청을 위한 Requests 모듈
import shutil  # 파일 복사 및 이동을 위한 shutil 모듈
from urllib.parse import quote_plus  # url 아스키코드 변환을 위한 모듈

# 작업 진행상황 표시를 위한 패키지 모듈 불러오기 
from tqdm import tqdm_notebook as tq  # 진행표시바를 위한 모듈
import time  # 시간데이터를 다루기 위한 모듈
import datetime  # 날짜와 시간을 다루기 위한 모듈

# 데이터 판다스로 정리하기 위해 판다스 패키지 불러오기 
import pandas as pd

# 경고 표시 무시 
import warnings

MAX_PHASE = 30000

warnings.filterwarnings(action='ignore')

# 1. 크롬 드라이버 옵션 및 url 접속
# 랜덤으로 생성한 UserAgent 값 출력 
ua = UserAgent()
userAgent = ua.random
print(userAgent)

# chrome dirver 옵션
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={userAgent}')  # fake user 표시
options.add_argument('headless')  # 크롬브라우저 숨기기
options.add_argument('window-size=1920,1080')  # 모니터 해상도 지정
options.add_argument('disable-gpu')  # 불필요한 GPU 기능을 제거해서 셀레니움 작동 속도를 올려주는 옵션

# 크롬드라이버 path 지정 및 옵션 지정 
driver = webdriver.Chrome(chrome_options=options)

# 인스타 url 받아오기
url = 'https://www.instagram.com/'
driver.get(url)
time.sleep(3)

# 인스타 로그인 하기 - ID -> PW -> 로그인 클릭
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(input('ID를 입력하세요: '))
time.sleep(2)
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(
    getpass.getpass('Password를 입력하세요: '))
time.sleep(2)
driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
time.sleep(3)

# 키워드 입력, 검색
pause_time = random.randint(2, 6)
time.sleep(4)
keyword = input('키워드를 입력하세요: ')
url = 'https://www.instagram.com/explore/tags/' + quote_plus(keyword)
driver.get(url)
time.sleep(pause_time)

# 2. 스크롤 내리기 
print('스크롤 내리는 중...')
last_page_height = driver.execute_script("return document.body.scrollHeight")

# 이동 전 스크롤 위치
before_location = driver.execute_script("return window.pageYOffset")
cnt = 0
imglist = []

try:
    for _ in range(MAX_PHASE):
        # 스크롤 내리기 이동 전 위치
        scroll_location = driver.execute_script("return document.body.scrollHeight")

        # 현재 위치 + 300으로 스크롤 이동
        driver.execute_script("window.scrollTo(0,{})".format(scroll_location + 300))

        time.sleep(2)
        # 이동 후 스크롤 위치
        after_location = driver.execute_script("return window.pageYOffset")

        # 이동 후 위치와 이동 후 위치가 같으면(더 이상 스크롤이 늘어나지 않으면) 종료
        if before_location == after_location and cnt != 0:
            # 한번 위로 -200만큼 스크롤 재이동 후 재시도
            # 현재 위치 -200으로 스크롤 이동
            driver.execute_script("window.scrollTo(0,{})".format(after_location - 200))
            time.sleep(3)

            # 이동 후 변경된 스크롤 위치
            after_location = driver.execute_script("return window.pageYOffset")
            time.sleep(3)

            if before_location == after_location:
                break

        # 같지 않으면 다음 조건 실행
        else:
            # 이동여부 판단 기준이 되는 이전 위치 값 수정
            before_location = driver.execute_script("return window.pageYOffset")

        print(f'{cnt}번째 스크롤 진행 중...')
        # 3. 인스타 정보 받기
        print('url 링크 받는 중...')
        html = driver.page_source
        soup = BeautifulSoup(html)

        # url 링크 추출
        insta = soup.select('.v1Nh3.kIKUG._bz0w')

        for idx, i in enumerate(insta):
            print(f'url : https://www.instagram.com{i.a["href"]}')
            imgUrl = i.select_one('.KL4Bh').img['src']
            imglist.append(imgUrl)
        cnt += 1
except:
    pass
finally:
    print('스크롤 완료')
    lmglist = list(set(imglist))

    if not os.path.exists(os.path.abspath('../insta_img/' + f'{keyword}')):
        os.makedirs(os.path.abspath('../insta_img/' + f'{keyword}'))
        print('폴더 생성 완료')
    else:
        # 동일한 폴더가 있으면 이미 동일한 폴더가 있다고 안내
        print('이미 동일한 이름의 폴더가 있습니다.')

    # 파일 이름에 날짜 시간을 위해 datetime 사용
    now = datetime.datetime.now()
    now = str(now).replace(' ', '')

    # 4. 이미지 추출 하기
    print('이미지 추출을 시작합니다.')
    n = 0

    for i in tq(range(len(lmglist))):
        image_url = imglist[n]  # 이미지 url 리스트 받기
        resp = requests.get(image_url, stream=True)  # url 이미지를 열고 스트림을 True로 설정하면 내용이 반환됨
        local_file = open(
            os.path.abspath('../insta_img/' + f'{keyword}') + '/' + f'insta_{keyword}_{now}_' + str(n) + '.jpg',
            'wb')  # 바이너리 쓰기 권한으로 로컬파일 열기
        resp.raw.decode_content = True  # decode_content 값을 True로 설정 (그렇지 않으면 다운로드한 이미지 파일이 0이 됨)
        shutil.copyfileobj(resp.raw, local_file)  # 로두 데이터를 로컬 이미지 파일에 복사
        n += 1
        del resp  # 이미지 url 응답 객체 제거

    print('이미지 추출이 완료되었습니다.')

    # 5. url csv로 저장
    result_df = pd.DataFrame()
    result_df['link'] = imglist

    result_df.to_csv(os.path.abspath('../insta_img') + '/' + f'{keyword}' + '/' + f'키워드_{keyword}instar{now}.csv',
                     index=False)
    driver.close()
