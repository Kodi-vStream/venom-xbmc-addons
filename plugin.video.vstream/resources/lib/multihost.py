#-*- coding: utf-8 -*-
#Venom.

import re,urllib2,urllib
import xbmc

def GetHtml(url, postdata = None):
    headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
    #'Referer' : 'http://www.jheberg.net/captcha/les-tinytoons-s01e03-the-wheel-o-comedy/' ,
    #'Host' : 'www.dl-protect.com',
    #'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #'Accept-Language': 'en-gb, en;q=0.9',
    #'Pragma' : '',
    #'Accept-Charset' : '',
    #'Content-Type' : 'application/x-www-form-urlencoded',
    }
        
    if postdata != None:
        headers['X-Requested-With'] = 'XMLHttpRequest'
        headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        headers['Referer'] = 'http://www.jheberg.net/redirect/xxxxxx/yyyyyy/'
    elif 'www.jheberg.net' in url:
        headers['Referer'] = url.replace('http://www.jheberg.net/mirrors','http://www.jheberg.net/captcha')
    
    sHtmlContent = ''
    request = urllib2.Request(url,postdata,headers)

    try: 
        reponse = urllib2.urlopen(request)
        sHtmlContent = reponse.read()
        reponse.close()
        
    except urllib2.URLError, e:
        print e.read()
        print e.reason

    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    return sHtmlContent

class cMultiup:
    def __init__(self):
        self.id = ''
        self.list = []
        
    def GetUrls(self,url):

        NewUrl = url.replace('http://www.multiup.org/fr/download','http://www.multiup.org/fr/mirror')
        
        sHtmlContent = GetHtml(NewUrl)
        
        sPattern = 'nameHost="([^"]+)"\s+validity=([a-z]+).+?href="([^"]+)"'
        r = re.findall(sPattern,sHtmlContent,re.DOTALL)
        if not r:
            return False

        for item in r:
            if item[1] == 'valid':
                self.list.append(item[2])
            
        return self.list

class cJheberg:
    def __init__(self):
        self.id = ''
        self.list = []
        
    def GetUrls(self,url):

        NewUrl = url.replace('http://www.jheberg.net/captcha','http://www.jheberg.net/mirrors')
        
        sHtmlContent = GetHtml(NewUrl)
        
        sPattern = '<a class="hoster-thumbnail" data-hoster="([^"]+)" href="([^"]+)".+?<div class="status success-status">\s+<p>([^><]+)<'
        r = re.findall(sPattern,sHtmlContent,re.DOTALL)
        if not r:
            return False

        for item in r:
            if not 'indisponible' in item[2]:
                hoster = item[0]
                slug = url.split('/')[-2]
                data = { 'slug' : str(slug) , 'hoster' : str(hoster) }
                postdata = urllib.urlencode( data )
                urllink = 'http://www.jheberg.net/get/link/'
                
                sHtmlContent = GetHtml(urllink,postdata)
                
                r = re.search('{"url": "([^"]+)"}', sHtmlContent)
                if r:              
                    self.list.append(r.group(1))
            
        return self.list
        
