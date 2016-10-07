#!/usr/bin/env python

import os
import datetime
import urllib, urllib2
import re
from bs4 import BeautifulSoup
import json
from database import MongoConnection


def findStringValuefromTable(soup,str):
	try:
		rawHtml = soup.find_all(string=re.compile(str))[0].find_parent('td').find_next('td')
		return extractString(rawHtml)
	except:
		print "Cannot parse"
	

def extractString(rawHtml):
	result = ''
	try:
		if type(rawHtml) is not None:
			result = rawHtml.string.extract()
	except Exception as e:
		print "Exception occured "+e.message
		print rawHtml

	return result

def saveData(json):
	database = MongoConnection('traindata');
	collection = database.createCollection("traindetails")
	collection.insert(json)

def getData():
	database = MongoConnection('traindata');
	collection = database.createCollection("traindetails")
	return collection.find()



def scrapTrainData(trainNo,station,startDate,startDay):

	req = urllib2.Request(
		"http://enquiry.indianrail.gov.in/mntes/MntesServlet?action=TrainRunning&subAction=ShowRunC",
	    data=urllib.urlencode({'trainNo': trainNo,
	         'jStation': station,
	         'arrDepFlag': 'A',
	         'jDate':startDate,
	         'jDateMap':startDate,
	         'jDateDay':startDay
	         }),
	    headers={
	    	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
	        'Cookie': ''
	        })

	response = urllib2.urlopen(req)

	soup = BeautifulSoup(response.read(),"lxml")

	try:
		trainDetailTable = soup.find_all("table",attrs={'id':'ResTab'})[0]
		trainName = findStringValuefromTable(trainDetailTable,'Train Name')
		journeyStation = findStringValuefromTable(trainDetailTable,'Journey Station')
		journeyDate = findStringValuefromTable(trainDetailTable,'Journey Date')
		# print findStringValuefromTable(trainDetailTable,'Scheduled Arrival')
		# print findStringValuefromTable(trainDetailTable,'Actual Arrival')
		# print findStringValuefromTable(trainDetailTable,'Delay Arrival')
		# print findStringValuefromTable(trainDetailTable,'Last Location')

		# print trainDetailTable.prettify()
		
		data = {
				'trainName':trainName,
				'journeyStation':journeyStation,
				'journeyDate':journeyDate,
				'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			}

	except Exception as e:
		data = {
			'error':{
				'status': 01,
				'status_code':'ERR',
				'message':e.message
			}
		}

	try:

		directory = 'data'
		if not os.path.exists(directory):
			try:
				os.makedirs('data')
			except OSError as e:
				print 'Error in creating dir'+ e.message
		else:
			pass

		with open(directory+'/'+trainNo+'.json','w') as outfile:
			json.dump(data,outfile)

	except Exception as e:
		print "Error in save train files " + e.message

	saveData(data)
	print getData()




today = datetime.date.today()
todayFormated = today.strftime('%d-%b-%Y');
dayofweek = today.strftime('%a')

trainNoList = ['16630','16341','16303','56308','sasdf']
queryStation = 'QLN#false'
queryDate = todayFormated
queryDay = dayofweek

for trainNo in trainNoList:
	scrapTrainData(trainNo,queryStation,queryDate,queryDay)


