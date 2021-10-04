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
import numpy as np

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

Tickers = {
'Materials':'XLB', #素材
'Energy':'XLE', #エネルギー
'Financial':'XLF', #金融
'Industrial':'XLI', #資本財
'Technology':'XLK', #テクノロジー
'Consumer Staples':'XLP', #生活必需品
'Utilities':'XLU', #公益事業
'Health Care':'XLV', #ヘルスケア
'Consumer Discretionary':'XLY' #一般消費財
}

figsize_px = np.array([1200, 675])
dpi = 100
figsize_inch = figsize_px / dpi
fig, ax = plt.subplots(figsize=figsize_inch, dpi=dpi) #ベースを作る
ax.set_ylabel('%') #y軸のラベルを設定する


# 株価増加率を取得する関数
def get_data(ticker,start_date,end_date,name):
    data = yf.download(ticker, start = start_date, end = end_date)
    stn = data['Close'][0] #一番古い日の株価を基準にする
    rate = data['Close']*100/stn #基準からの増加率を%で計算
    result = data.tail(1)['Close']*100/stn #基準からの増加率を%で計算
    text1 = name + ' ' + str(round(result[0],2)) + '%'
    ax.plot(rate,label=name) #グラフを重ねて描写していく
    return text1

def graph(start_date,end_date,num):
    text = ''
    for name,ticker in Tickers.items():
        text1 = get_data(ticker,start_date,end_date,name)
        text = text + text1 + '\n'
    ax.set_title(start_date + '~')
    ax.legend()
    ax.grid()
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, fontsize=10)
    fig.savefig('img' + num + '.png', bbox_inches='tight')
    return text

today = datetime.date.today()
start = '2021-' + str(today.month -1 ) + '-1'
text = graph(start, str(today.year) + '-12-31',str(1))

file_names = ['img1.png']
media_ids = []

for filename in file_names:
    res = api.media_upload(filename)
    media_ids.append(res.media_id)
print(media_ids)

tag = ''
for name,ticker in Tickers.items():
    tag = tag + '#' + ticker + ' '

api.update_status(
    status= 'セクター別パファーマンス'+ '(' + start + '~' + ')' +  '\n' + text + tag,
    media_ids= media_ids,
)