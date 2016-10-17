#!/usr/bin/env python

import datetime
from railparser import RailParser
import time, threading


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


