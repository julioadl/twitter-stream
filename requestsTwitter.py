'''
Class to handle requests to Twitter's Premium API v1.1
To handle requests see: https://developer.twitter.com/en/docs/twitter-api/premium/search-api/api-reference/premium-search
For authentication see: https://developer.twitter.com/en/docs/authentication/oauth-2-0; Need to get a bearer tpken and submit it
in the headers
'''
import json
import requests
import pymongo
import datetime
from credentials import AUTH_TOKEN

'''
Class that handles object for requesting data to Twitter Premium API v1.1
Takes in the "url" as a string -- endpoint where the data is to be requested,
Takes in the "AUTH_TOKEN"
Takes in the "query" as a string
Prepares the object "data" as a dict of list
Prepares the connection with MongoDb
'''
class requestTwitter:
	def __init__(self, url, query, mongoDB = None):
		self.url = url
		self.auth_token = AUTH_TOKEN
		self.query = query
		self.data = {'data': []}
		if mongoDB:
			self.conn = pymongo.MongoClient('mongodb://localhost:27017')

	'''
	Takes in the 'data' to be sent in the post and returns a JSON response.
	For the case of Twitter 1.1 premium API, data stands for the request to be sent.
	'''

	def request(self, data):
		headers = {
			'authorization': self.auth_token,
			'content-type': 'application/json'
			}
		dta = json.dumps(data)
		r = requests.post(self.url, headers=headers, data=dta)
		return json.loads(r.text)

	'''
	Handles requests involving pagination.
	When calling pagination, this function takes the class request and
	appends the reponses to the object data within the class.
	'''

	def pagination(self):
		next = True
		data = self.query
		page_no = 0
		while next == True:
			response = self.request(data)
			try:
				data['next'] = response['next']
			except:
				next = False
			self.data['data'].append(response)
			page_no += 1
			print(f'Page number: {page_no}')
		print('Done!')

	'''
	Saves data as a JSON.
	Takes in the name of the file as a string.
	Returns a string if the data was correctly saved.
	'''

	def saveData(self, file_name):
		json.dump(self.data, open(file_name, 'w'))
		print('Data saved')

	'''
	Loads a JSON with the data
	Takes in a string indicating the name of the directory of the data.
	Returns a JSON with the data.
	'''

	def loadData(self, file_name):
		data = json.load(open(file_name))
		return data

	'''
	Saves query as a JSON.
	Takes in a string indicating the name of the file where the query is to be saved.
	Returns a string if the data was correctly saved.
	'''

	def saveQuery(self, file_name):
		json.dump(self.query, open(file_name, 'w'))
		print('Query saved')

	'''
	Loads a JSON with the query
	Takes in a string indicating the name of the directory of the query.
	Returns a JSON with the query.
	'''

	def loadQuery(self, file_name):
		query = json.load(open(file_name))
		return query

	'''
	Saves the object within the class in MongoDb.
	Takes in a string indicating the name of db "name_db" and the collection "name_collection"
	Returns a string if the data was correctly saved.
	'''

	def saveToMongo(self, name_db, name_collection):
		db = self.conn[name_db]
		for page in self.data['data']:
			for result in page['results']:
				date = self._toDatetime(result['timePeriod'])
				count = result['count']
				db[name_collection].insert({'date': date, 'count': count})
		print('All values saved to mongo')

	def _toDatetime(self, date):
		yy = int(date[0:4])
		mm = int(date[4:6])
		dd = int(date[6:8])
		return datetime.datetime(yy, mm, dd)
