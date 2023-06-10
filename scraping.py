import requests
from bs4 import BeautifulSoup
import json
from collections import defaultdict
session = requests.session()

# ランキング
# url_ranking = 'https://atcoder.jp/ranking?contestType=algo&f.Affiliation=&f.BirthYearLowerBound=0&f.BirthYearUpperBound=9999&f.CompetitionsLowerBound=0&f.CompetitionsUpperBound=9999&f.Country=JP&f.HighestRatingLowerBound=0&f.HighestRatingUpperBound=9999&f.RatingLowerBound=2200&f.RatingUpperBound=2600&f.UserScreenName=&f.WinsLowerBound=0&f.WinsUpperBound=9999&page=1'

# req = session.get(url_ranking)
# soup = BeautifulSoup(req.content, "html.parser")
# # print(type(soup))
# page = soup.find_all(class_="table-responsive")
# page = soup.find_all(class_="username")
# N = len(page)
# for i, name in enumerate(range(N)):
#     print(page[i].text)

# ARCXXX のRated日本人上位1000人を contestants に入れる
XXX = 158
json_file = "./arc" + str(XXX) + ".json"
contest_n = "arc" + str(XXX)
with open(json_file) as f:
    contest = json.load(f)

with open('./contestants.json') as f:
    contestants = json.load(f)

count = 0
for i, name in enumerate(contest["StandingsData"]):
    if name["Country"] == "JP" and name["IsRated"] == True:
        print(count,name["UserScreenName"])
        contestants[contest_n].append(name["UserScreenName"])
        count += 1
    if count == 1000:
        break

with open('./contestants.json', 'w') as f:
    json.dump(contestants,f,sort_keys=True)