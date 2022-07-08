# 필요한 패키지 불러오기 
from googleapiclient.discovery import build   # google API 클라이언트 라이브러리 discovery의 build 함수 불러오기
from googleapiclient.errors import HttpError  # google API 클라이언트 라이브러리 errors의 HttpError 함수 불러오기 
from oauth2client.tools import argparser   # OAuth2 클라이언트 라이브러리 tools의 argparser 함수 불러오기 

import os              # 운영체제에서 제공되는 기능을 파이썬에 사용기위해 os 모듈 불러오기 
import sys             # 파이썬 인터프리터 제어를 위한 sys 모듈 불러오기 
import re              # 정규 표현식을 위한 re 모듈 불러오기 
import pandas as pd    # 판다스 모듈 불러오기 
from datetime import datetime       # datetime 모듈 불러오기 
import time            # time 모듈 불러오기 
from tqdm import tqdm  # 진행바 표시를 위한 tqdm 모듈 

# API key 값 설정 및 사용할 서비스 설정 
DEVELOPER_KEY = 'use your youtube API Key'   # youtube API key 
YOUTUBE_API_SERVICE_NAME = 'youtube'   # 이용할 서비스 이름 
YOUTUBE_API_VERSION = 'v3'    # 이용할 서비스 버전 

# youtube API 접근하기
youtube = build(YOUTUBE_API_SERVICE_NAME, 
                YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)

# API를 이용하여 정보 모으기 
results = []

# 원하는 키워드와 크롤링 개수 입력 변수 만들기 
data = pd.read_csv('keyword.csv')
data = data.reset_index(drop=True)
keyword_list = data['0'].to_list()

# 각 키워드 별로 정보 모으기
for keyword in tqdm(keyword_list):
    
    # 지정된 키워드를 기준으로 response 받기
    search_response = youtube.search().list(
        q = keyword,           # 검색하고자 하는 검색어 = 키워드
        order = 'relevance',   # 정렬 방법 - relevance(연관성) (그 외 date, rating 등이 있다.)
        part = 'snippet',      # 필수 매개변수로 변환되는 결과 구조
        maxResults=10          # 최대 검색 결과 개수
    ).execute()

    # response 받은 정보를 바탕으로 results에 저장 
    for i in search_response['items']:
        date = i['snippet']['publishedAt']         # 게시 날짜 및 시간
        channel = i['snippet']['channelTitle']     # 채널명
        title = i['snippet']['title']              # 게시물 제목
        description = i['snippet']['description']  # 게시물 설명글
        
        # 위에 지정된 정보들 results 리스트에 저장
        results.append([keyword, date, channel, title, description])
        
# 위 결과를 토대로 컬럼을 지정하여 데이터 프레임으로 생성
result = pd.DataFrame(columns = ['keyword', 'date', 'channel', 'title', 'description'])
for i in range(len(results)):
    result.loc[i] = results[i]
    
# excel 파일로 저장 
now = datetime.now()
now = now.strftime('%Y-%m-%d-%H-%M-%S')
path = os.getcwd()
result.to_excel(f'{path}/{now}_keyword_youtube.xlsx', index=True)