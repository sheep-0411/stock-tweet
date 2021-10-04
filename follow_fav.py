import os
import tweepy
from dotenv import find_dotenv, load_dotenv
import datetime
import jpholiday
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import time
import random

# .envファイルを探して読み込む
load_dotenv(find_dotenv())

# 環境変数から認証情報を取得する。
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

# 認証情報を設定する。
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def fav(query):
    posts = api.search(q=query, count=20)
    for post in posts:
        try:
            api.create_favorite(post.id)
        except Exception as e:
            print(e)
            pass
    
def follow(screen_name):

    followers = api.followers_ids(screen_name=screen_name)
    ran = random.randint(0,len(followers)-1)
    followers = followers[ran:ran + 100]

    for i in followers:
        try:
            user = api.get_user(id=i)
            followers_count = int(user.followers_count)
            friends_count = int(user.friends_count)

            if followers_count > 100 and friends_count > 100 and followers_count / friends_count < 1 and followers_count / friends_count > 0.5 and int(user.status.created_at.strftime('%Y%m%d')) > 20210610:
                api.create_friendship(id=user.id)
                print('フォロー数',friends_count,'フォロワー数',followers_count,'フォローしました')
            else:
                print('フォロー数',friends_count,'フォロワー数',followers_count,'フォローしませんでした')
            n = n + 1
            time.sleep(1)
        except Exception as e:
            print(e)
            pass

query_list = ['テンバガー','米国株','フルレバ','SBI証券','ドル円','マルケタ','GAFAM','NASDAQ','日経平均','IPO']
for query in query_list:
    fav(query)
    time.sleep(60)

influencer_list = ['komcdspxl','4ki4','Capybara_Stock','Kamada3','PropTrader88']
for screen_name in influencer_list:
    follow(screen_name)
    time.sleep(60)
