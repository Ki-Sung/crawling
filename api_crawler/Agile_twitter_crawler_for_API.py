# 필요한 모듈 불러오기
import tweepy  # 파이썬으로 트위터 API 제어를 위한 트위파이 모듈 불러오기 
from tweepy import OAuthHandler, API  # 트위파이 모듈 중 OAuthHandler, API 함수 불러오기 

import os   # os 모듈 불러오기 
import sys  # sys 모듈 불러오기 
from datetime import datetime  # datetime 모듈 불러오기 

import pandas as pd # 판다스 모듈 불러오기
import openpyxl  # python으로 excel을 조작하기 위한 openpyxl 모듈 불러오기
from tqdm import tqdm  # 상태바 tqdm 모듈 불러오기 

# 경고 표시 무시 설정
import warnings
warnings.filterwarnings(action='ignore')

# 트위터 API Key 정보 
CONSUMER_KEY = "use your twitter Api Key" 
CONSUMER_SECRET = "use your twitter Api Key secret" 
ACCESS_TOKEN = "use your twitter Access Token" 
ACCESS_TOKEN_SECRET = "your twitter Access Toekn Secret" 

# Twitter API와 연결
# API 접근
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# API 호출 
api = API(auth, wait_on_rate_limit=True)

# 받은 정보 담기 
results = []

# 원하는 키워드와 크롤링 개수 입력 변수 만들기 
data = pd.read_csv('keyword.csv')
data = data.reset_index(drop=True)
keyword_list = data['0'].to_list()

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
        
# 위 결과를 토대로 컬럼을 지정하여 데이터 프레임으로 생성
result = pd.DataFrame(columns = ['keyword', 'date', 'time', 'name', 'id', 'mension'])
for i in range(len(results)):
    result.loc[i] = results[i]
    
# excel 파일로 저장 
now = datetime.now()
now = now.strftime('%Y-%m-%d-%H-%M-%S')
path = os.getcwd()
result.to_excel(f'{path}/{now}_keyword_twitter.xlsx', index=True)