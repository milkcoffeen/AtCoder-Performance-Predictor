import requests
from bs4 import BeautifulSoup
# import re
import json
# import configparser
# import pprint
from collections import defaultdict
import pandas as pd


# テーブルデータの概要作成 (コンテスト数 x ユーザー数)
columns = ["name"]
for i in range(140,162): #カラム(名前,各コンテスト) を作成
    s = 'arc' + str(i)
    columns.append(s)
df = pd.DataFrame(
    index=range(100),
    columns = columns
)

# 対象者(ARCXXX参加者上位N人) を抽出
with open('./contestants.json') as f:
    contestants = json.load(f)

N = 500 #使う参加者数
XXX = 158 #ARCXXX
contest_n = "arc" + str(XXX)
for i, user_name in enumerate(contestants[contest_n]):
    # print(user_name)
    df.at[i,'name'] = user_name
    url = "https://atcoder.jp/users/" + str(user_name) +"/history/json"
    session = requests.session()
    req = session.get(url)
    history = req.json()

    for contest in history:
        contest_name = contest["ContestScreenName"][:-19]
        # if contest["IsRated"] == False:
        #     continue
        if contest_name < "arc140" or "arc161" < contest_name:
            continue
        OldRating = contest["OldRating"]
        NewRating = contest["NewRating"]
        df.at[i,contest_name] = NewRating - OldRating
        # print(contest["ContestScreenName"][:6])
    
    N -= 1
    if N == 0:
        break

df.to_csv("data_arc158.csv")