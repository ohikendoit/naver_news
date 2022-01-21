import urllib
import pymysql
from urllib.request import urlopen
from bs4 import BeautifulSoup

#open database connection
db = pymysql.connect(host='192.168.1.134', port=3306, user='ohikendoit', passwd='Wjddbstjd!3', db='hscode', autocommit=True)

#prepare a cursor object using cursor(method)
cursor = db.cursor()

#execute SQL query using execute() method
cursor.execute("SELECT VERSION()")

#Fetch a single row using fetchone() method.
data = cursor.fetchone()

print("Database version : %s " % data)