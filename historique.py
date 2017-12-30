#-*- coding: utf-8 -*-
url = "https://api.github.com/repos/Kodi-vStream/venom-xbmc-addons/commits?page=3"

import re,urllib, json, time, datetime

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


response = urlopen(url)
data = json.loads(response.read().decode("utf-8"))
response.close()

for i in data:
    date = datetime.datetime.strptime(i['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
    date = date.strftime('%d-%m-%Y')
    autor = i['commit']['author']['name'].replace(' ', '')
    message = i['commit']['message'].replace('\n', ' ').replace('\'', ' ')
    #message = message[0:50]
    print ("%s -- @%s -- %s" % (date, autor, message))
