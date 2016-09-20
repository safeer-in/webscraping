#!/usr/bin/env python

# import mechanize
import datetime
import urllib, urllib2
import re
from bs4 import BeautifulSoup


# browser = mechanize.Browser()
# browser.open('http://www.mohammedsafeer.in')
# browser.select_form(name='contact-form')
# browser['name'] = "mechanize"
# browser['email'] = "safeer.ar@inapp.com"
# browser['phone'] = "871-44-250-96"
# browser.submit()

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


req = urllib2.Request("http://enquiry.indianrail.gov.in/mntes/MntesServlet?action=TrainRunning&subAction=ShowRunC",
                      data=urllib.urlencode({'trainNo': trainNo,
                                             'jStation': queryStation,
                                             'arrDepFlag': 'A',
                                             'jDate':queryDate,
                                             'jDateMap':queryDate,
                                             'jDateDay':queryDay
                                             }),

                      headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
                               'Cookie': 'JSESSIONID=eUP2Upcl2p-aSIzpPueMKRlNQpEpqyN07G90diYS.ntes_host2:host2_server1; SERVERID=cch7fw87sfs4; _gat=1; _ga=GA1.3.263681154.1461936530'})
response = urllib2.urlopen(req)

soup = BeautifulSoup(response.read(),"lxml")

trainDetailTable = soup.find_all("table",attrs={'id':'ResTab'})[0];

# trainName = findStringValuefromTable(trainDetailTable,'Train Name')

# journeyStation = findStringValuefromTable(trainDetailTable,'Journey Station')

# print trainName

# print journeyStation

print findStringValuefromTable(trainDetailTable,'Train Name')
print findStringValuefromTable(trainDetailTable,'Journey Station')
print findStringValuefromTable(trainDetailTable,'Journey Date')
# print findStringValuefromTable(trainDetailTable,'Scheduled Arrival')
# print findStringValuefromTable(trainDetailTable,'Actual Arrival')
# print findStringValuefromTable(trainDetailTable,'Delay Arrival')
# print findStringValuefromTable(trainDetailTable,'Last Location')


# print trainDetailTable.prettify()





