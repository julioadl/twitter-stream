import json
import requests
import pymongo
import datetime
import time
from requests_oauthlib import OAuth1
from credentials import CLIENT_KEY, CLIENT_SECRET

class searchTwitter:
    def __init__(self, mongoDB = None):
        self.url = 'https://api.twitter.com/1.1/search/tweets.json'
        self.client_key = CLIENT_KEY
        self.client_secret = CLIENT_SECRET
        if mongoDB:
            self.conn = pymongo.MongoClient('mongodb://localhost:27017')

    def request(self, query):
        oauth = OAuth1(self.client_key, client_secret=self.client_secret)
        r = requests.get(self.url, auth=oauth, params=query)
        return json.loads(r.text)

    def saveData(self, data, file_name):
        json.dump(data, open(file_name, 'w'))
        print('Data saved')

    def loadData(self, file_name):
        data = json.load(open(file_name))
        return data

    def saveQuery(self, data, file_name):
        json.dump(data, open(file_name, 'w'))
        print('Query saved')

    def loadQuery(self, file_name):
        query = json.load(open(file_name))
        return query

    def saveToMongo(self, name_db, name_collection, data):
        db = self.conn[name_db]
        for result in data['statuses']:
            db[name_collection].insert(result)
        #print('All values saved to mongo')

    def _toDatetime(self, date):
        yy = int(date[0:4])
        mm = int(date[4:6])
        dd = int(date[6:8])
        return datetime.datetime(yy, mm, dd)
