#-*- coding: utf-8 -*-
url = "https://api.github.com/repos/Kodi-vStream/venom-xbmc-addons/commits?page=1"

import re,urllib, json, time, datetime


response = urllib.urlopen(url)
data = json.loads(response.read())
response.close()

for i in data:
    date = datetime.datetime.strptime(i['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
    date = date.strftime('%d-%m-%Y')
    autor = i['commit']['author']['name'].replace(' ', '')
    message = i['commit']['message'].replace('\n', ' ').replace('\'', ' ')
    #message = message[0:50]
    print "%s -- @%s -- %s" % (date, autor, message)
