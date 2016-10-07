#! /usr/bin/env python
##
## MongoDB Database connection
##

from pymongo import MongoClient

class MongoConnection(object):

	def __init__(self, dbname):
		self.client = MongoClient()
		self.db = self.client[dbname]

	def createCollection(self,name=""):
		return self.db[name]


if __name__ == '__main__':
	database = MongoConnection('safeertest')
	collection  = database.createCollection('safcollection')
	collection.insert({"name":"tutorials point"})