# 0. 필요한 패키지 불러오기 
# youtube API 관련 모듈 
from googleapiclient.discovery import build   # google API 클라이언트 라이브러리 discovery의 build 함수 불러오기
from googleapiclient.errors import HttpError  # google API 클라이언트 라이브러리 errors의 HttpError 함수 불러오기 
from oauth2client.tools import argparser   # OAuth2 클라이언트 라이브러리 tools의 argparser 함수 불러오기 

# twitter API 관련 모듈 
import tweepy  # 파이썬으로 트위터 API 제어를 위한 트위파이 모듈 불러오기 
from tweepy import OAuthHandler, API  # 트위파이 모듈 중 OAuthHandler, API 함수 불러오기 

# 기본으로 필요한 모듈 
import os             # os 모듈 불러오기 
import sys            # sys 모듈 불러오기 
import re             # 정규 표현식을 위한 re 모듈 불러오기 
import pandas as pd   # 판다스 모듈 불러오기 
import openpyxl       # python으로 excel을 조작하기 위한 openpyxl 모듈 불러오기
import time           # time 모듈 불러오기 
from datetime import datetime       # datetime 모듈 불러오기 
from tqdm import tqdm # 상태바 tqdm 모듈 불러오기

# 경고 표시 무시 설정 
import warnings
warnings.filterwarnings(action='ignore')

# 1. youtube crawler class
class youtube_crawler:
    def __init__(self):
        self.DEVELOPER_KEY = 'input your youtube API Key' # 본인이 할당 받은 youtube API key
        self.YOUTUBE_API_SERVICE_NAME = 'youtube'       # 이용할 서비스 이름 
        self.YOUTUBE_API_VERSION = 'v3'                 # 이용할 서비스 버전 
    
    # youtube 게시물 크롤링 매서드 
    def youtube_post(self):
        # youtube API 접근하기
        youtube = build(self.YOUTUBE_API_SERVICE_NAME, 
                        self.YOUTUBE_API_VERSION,
                        developerKey=self.DEVELOPER_KEY)
        
        # 원하는 키워드와 크롤링 개수 입력 변수 만들기 
        file_path = os.getcwd() + '/keyword.csv'   # keyword 파일 경로 설정 
        data = pd.read_csv(file_path)              # keyword.csv 파일 불러오기
        data = data.reset_index(drop=True)         # 인덱스 재설정하여 불러오기 
        keyword_list = data['0'].to_list()         # 불러온 데이터 list로 변환
        
        # API를 이용하여 정보 모으기 
        results = []
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
            
        return results
    
    # 크롤링한 youtube 게시물 결과 데이터 프레임 변환 메서드     
    def post_to_df(self, results):
        # 위 결과를 토대로 컬럼을 지정하여 데이터 프레임으로 생성
        result = pd.DataFrame(columns = ['keyword', 'date', 'channel', 'title', 'description'])

        # 크롤링 결과를 지정한 컬럼에 맞게 배열 
        for i in range(len(results)):
            result.loc[i] = results[i]
        
        return result
    
    # 엑셀파일 저장 메서드 
    def save_to_excel(self, result):
        # excel 파일로 저장 
        now = datetime.now()
        now = now.strftime('%Y-%m-%d-%H-%M-%S')
        path = os.getcwd()
        result.to_excel(f'{path}/{now}_keyword_youtube.xlsx', index=True)

# 2. twitter crawler Class        
class twitter_crawler:
    def __init__(self):
        # 트위터 API Key 정보 
        self.CONSUMER_KEY = "input your twitter Api Key" 
        self.CONSUMER_SECRET = "input your twitter Api Key secret" 
        self.ACCESS_TOKEN = "input your twitter Access Token" 
        self.ACCESS_TOKEN_SECRET = "input your twitter Access Toekn Secret" 
    
    # twitter 게시물 크롤링 매서드     
    def twitter_post(self):
        # Twitter API와 연결
        # API 접근
        auth = OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)

        # API 호출 
        api = API(auth, wait_on_rate_limit=True)
        
        # 원하는 키워드와 크롤링 개수 입력 변수 만들기 
        file_path = os.getcwd() + '/keyword.csv'   # keyword 파일 경로 설정 
        data = pd.read_csv(file_path)              # keyword.csv 파일 불러오기
        data = data.reset_index(drop=True)         # 인덱스 재설정하여 불러오기 
        keyword_list = data['0'].to_list()         # 불러온 데이터 list로 변환
        
        # 받은 정보 담기 
        results = []
        
        for keyword in tqdm(keyword_list):
            max_tweets = 6   # 최대 검색 트윗수 -> 키워드당 6개 (부족하면 추후 원하는 수로 지정 가능하나 하루에 정보를 받을 수 있는 수가 한정되어 있음)
            searched_tweets = []  # 검색된 트윗 저장 
            
            # 반복문으로 트위터 데이터 받는 횟수 제어 
            while len(searched_tweets) < max_tweets: # searched_tweets의 값이 max_tweets에 도달할 때 까지 반복 
                count = max_tweets - len(searched_tweets)
                
                # 키워드 기준으로 데이터 받기 
                try:
                    new_tweets = api.search(q=keyword, count=count)  # 쿼리와 횟수를 API 기준으로 찾기
                    if not new_tweets:   # 만약 최신글이 아닐 경우 
                        break            # 정지
                    searched_tweets.extend(new_tweets)    # searched_tweets에 new_tweets 넣기 
                except tweepy.TweepError as e:    # 트위터 정보를 받다가 에러가 나오면
                    break                         # 정지

            # 트윗에서 정보 추출 
            for tweet in searched_tweets:
                creat_time = str(tweet.created_at)  # 트위터 작성 날짜 지정 
                time_split = creat_time.split()     # 트위터 작성 시간 지정
                
                twt_name = tweet.user.name  # 트위터 닉네임
                twt_id = '@' + tweet.user.screen_name  # 트위터 아이디
                twt_mension = tweet.text    # 트위터 내용
                twt_date = time_split[0]    # 트위터 작성 날짜
                twt_time = time_split[1]     # 트위터 작성 시간
                
                results.append([keyword, twt_date, twt_time, twt_name, twt_id, twt_mension])
                
        return results
    
    # 크롤링한 youtube 게시물 결과 데이터 프레임 변환 메서드     
    def post_to_df(self, results):
        # 위 결과를 토대로 컬럼을 지정하여 데이터 프레임으로 생성
        result = pd.DataFrame(columns = ['keyword', 'date', 'time', 'name', 'id', 'mension'])

        # 크롤링 결과를 지정한 컬럼에 맞게 배열 
        for i in range(len(results)):
            result.loc[i] = results[i]
        
        return result
    
    # 엑셀파일 저장 메서드 
    def save_to_excel(self, result):
        # excel 파일로 저장 
        now = datetime.now()
        now = now.strftime('%Y-%m-%d-%H-%M-%S')
        path = os.getcwd()
        result.to_excel(f'{path}/{now}_keyword_twitter.xlsx', index=True)

