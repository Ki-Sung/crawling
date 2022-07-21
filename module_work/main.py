# 만든 클래스 모듈 불러오기 
from agile_crawler import youtube_crawler
from agile_crawler import twitter_crawler

# 1. youtube 크롤링 방법
# 최초 youtube 클래스 선언
youtube = youtube_crawler()

# youtube 게시물 크롤링 
youtube_post = youtube.youtube_post()

# 크롤링 결과 데이터 프레임으로 전환 
youtube_post_df = youtube_post.post_to_df(youtube_post)

# 크롤링 결과 저장
save_to_excel = youtube.save_to_excel(youtube_post_df)

# 2. twitter 크로링 방법 
# 최초 twitter 클래스 선언
twitter = twitter_crawler()

# youtube 게시물 크롤링 
twitter_post = twitter.twitter_post()

# 크롤링 결과 데이터 프레임으로 전환 
twitter_post_df = twitter_post.post_to_df(twitter_post)

# 크롤링 결과 저장
save_to_excel = twitter.save_to_excel(twitter_post_df)