from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.newsdb

#MongDB insert the following data
db.users.insert_one({'name': 'alpha', 'age':116})
db.users.insert_one({'name': 'beta', 'age':1})
db.users.insert_one({'name': 'omega', 'age':136})
db.users.insert_one({'name': 'trilion', 'age':115})
db.users.insert_one({'name': 'quadruple', 'age':216})
