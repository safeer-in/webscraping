#!/usr/bin/env python

import os
import datetime
import urllib, urllib2
import re
from scrap import Scrap
import json
from database import MongoConnection
import time, threading

class RailParser(object):
	"""docstring for RailParser"""
	def __init__(self):
		super(RailParser, self).__init__()
		
	def findStringValuefromTable(self,soup,str):
		try:
			rawHtml = soup.find_all(string=re.compile(str))[0].find_parent('td').find_next('td')
			return self.extractString(rawHtml)
		except Exception as e:
			return self.errorResponse('02','ERR',e.message)
			print "Cannot parse"
		
	def errorResponse(self,status,status_code,message):
		return {
			'error' : {
				'status' : status,
				'status_code' : status_code,
				'message' : message
			}
		}

	def extractString(self,rawHtml):
		result = ''
		try:
			if type(rawHtml) is not None:
				# result = rawHtml.string.extract()
				result = rawHtml.get_text()
			else:
				result = rawHtml
		except Exception as e:
			return self.errorResponse('02','ERR',e.message)
			print "Exception occured "+e.message
			print rawHtml

		return result

	def saveFile(self,data):
		try:

			directory = 'data'
			if not os.path.exists(directory):
				try:
					os.makedirs('data')
				except OSError as e:
					print 'Error in creating dir'+ e.message
			else:
				pass
			trainNo = data['trainNo']	
			with open(directory+'/'+trainNo+'.json','w') as outfile:
				json.dump(data,outfile)

		except Exception as e:
			print "Error in save train files " + e.message


	def saveData(self,json):
		database = MongoConnection('traindata');
		collection = database.createCollection("traindetails")
		query = {'trainNo': json['trainNo']}
		collection.update(query, json, upsert=True)

	def getData(self):
		database = MongoConnection('traindata');
		collection = database.createCollection("traindetails")
		return collection.find()

	def scrapTrainData(self,trainNo,station,startDate,startDay):

		scrapLib = Scrap(
				"http://enquiry.indianrail.gov.in/mntes/MntesServlet?action=TrainRunning&subAction=ShowRunC",
				{'trainNo': trainNo,
		         'jStation': station,
		         'arrDepFlag': 'A',
		         'jDate':startDate,
		         'jDateMap':startDate,
		         'jDateDay':startDay
		         },
		         {
		    	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
		        'Cookie': ''
		        },
			)
		soup = scrapLib.scrapData()

		try:
			trainDetailTable = soup.find_all("table",attrs={'id':'ResTab'})[0]
			trainName = self.findStringValuefromTable(trainDetailTable,'Train Name')
			journeyStation = self.findStringValuefromTable(trainDetailTable,'Journey Station')
			journeyDate = self.findStringValuefromTable(trainDetailTable,'Journey Date')
			scheduledArrival = self.findStringValuefromTable(trainDetailTable,'Scheduled Arrival')
			scheduledDeparture = self.findStringValuefromTable(trainDetailTable,'Scheduled Departure')
			actualArrival = self.findStringValuefromTable(trainDetailTable,'Actual Arrival')
			actualDeparture = self.findStringValuefromTable(trainDetailTable,'Actual Departure')
			expectedArrival = self.findStringValuefromTable(trainDetailTable,'Expected Arrival')
			expectedDeparture = self.findStringValuefromTable(trainDetailTable,'Expected Departure')
			delayInArrival = self.findStringValuefromTable(trainDetailTable,'Delay Arrival')
			lastLocation = self.findStringValuefromTable(trainDetailTable,'Last Location')

			# print trainDetailTable.prettify()
			
			data = {
					'trainNo':trainNo,
					'trainName':trainName,
					'journeyStation':journeyStation,
					'journeyDate':journeyDate,
					'scheduledArrival':scheduledArrival,
					'scheduledDeparture':scheduledDeparture,
					'actualArrival':actualArrival,
					'actualDeparture':actualDeparture,
					'expectedArrival':expectedArrival,
					'expectedDeparture':expectedDeparture,
					'delayInArrival':delayInArrival,
					'lastLocation':lastLocation,
					'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				}

		except Exception as e:
			data = {
				'trainNo':trainNo,
				'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
				'error':{
					'status': 01,
					'status_code':'ERR',
					'message':e.message
				}
			}

		self.saveFile(data)
		self.saveData(data)



if __name__ == '__main__':

	def periodicDataCollection():
		today = datetime.date.today()
		todayFormated = today.strftime('%d-%b-%Y');
		dayofweek = today.strftime('%a')

		trainNoList = ['16630','16341','16303','56308','sasdf']
		queryStation = 'QLN#false'
		queryDate = todayFormated
		queryDay = dayofweek

		parser = RailParser()
		for trainNo in trainNoList:
			parser.scrapTrainData(trainNo,queryStation,queryDate,queryDay)

		for doc in parser.getData():
				print(doc)

	def repeat():
	    print(time.ctime())
	    periodicDataCollection()
	    threading.Timer(10, repeat).start()

repeat()


