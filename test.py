#!/usr/bin/env python

import urllib2
from bs4 import BeautifulSoup 
import re 

page = urllib2.urlopen('http://www.google.co.in/trends/hottrends')

content = page.read()
soup = BeautifulSoup(content,"lxml")

print soup.head.title


