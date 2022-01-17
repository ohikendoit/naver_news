from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.newsdb

all_users = list(db.users.find({}))

print(all_users[0])
print(all_users[0]['name'])

for user in all_users:
    print(user)