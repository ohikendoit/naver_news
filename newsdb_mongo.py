#import packages
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017) #mongoDB Port
db = client.newsdb #'newsdb'데이터베이스

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20210112', headers=headers)

#Converting into Beautiful Soup
soup = BeautifulSoup(data.text, 'html.parser')

#Select to load tr's
movies = soup.select('#old_content > table > tbody > tr')

#For loop for the movies
for movie in movies:
    a_tag = movie.select_one('td.title > div > a')
    if a_tag is not None:
        rank = movie.select_one('td:nth-child(1) > img')['alt']
        title = a_tag.text
        star = movie.select_one('td.point').text
        print(rank, title, star)

        doc = {
            'rank': rank,
            'title': title,
            'star': star
        }
        db.movies.insert_one(doc)
