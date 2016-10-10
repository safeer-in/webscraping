#!/usr/bin/env python

import urllib, urllib2
from bs4 import BeautifulSoup

class Scrap(object):

	def __init__(self,url,data,header):
		super(Scrap, self).__init__()
		self.url = url
		self.data = data
		self.header = header

	def scrapData(self):

		req = urllib2.Request(
			self.url,
		    data=urllib.urlencode(self.data),
		    headers=self.header
			)

		try:
			response = urllib2.urlopen(req)
		except Exception as e:
			print "check your network connection "+ e.message

		try:
			soup = BeautifulSoup(response.read(), "lxml")

		except Exception as e:
			soup = {
				'error':{
					'status': 01,
					'status_code':'ERR',
					'message':e.message
				}
			}

		return soup

