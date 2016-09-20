#!/usr/bin/env python

import datetime
import urllib, urllib2
import re
from bs4 import BeautifulSoup


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
	except:
		print "Exception Handled"
		print rawHtml

	return result


today = datetime.date.today()
todayFormated = today.strftime('%d-%b-%Y');
dayofweek = today.strftime('%a')

trainNo = '16630'
queryStation = 'QLN#false'
queryDate = todayFormated
queryDay = dayofweek


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
		print findStringValuefromTable(trainDetailTable,'Train Name')
		print findStringValuefromTable(trainDetailTable,'Journey Station')
		print findStringValuefromTable(trainDetailTable,'Journey Date')
		# print findStringValuefromTable(trainDetailTable,'Scheduled Arrival')
		# print findStringValuefromTable(trainDetailTable,'Actual Arrival')
		# print findStringValuefromTable(trainDetailTable,'Delay Arrival')
		# print findStringValuefromTable(trainDetailTable,'Last Location')

		# print trainDetailTable.prettify()
	except Exception as e:
		print "Error in parsing train data Error: " + e.message



scrapTrainData(trainNo,queryStation,queryDate,queryDay)


