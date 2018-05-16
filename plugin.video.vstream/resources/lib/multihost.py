#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#Venom.
from resources.lib.handler.requestHandler import cRequestHandler
import re,urllib
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
#modif cloudflare
def GetHtml(url, postdata = None):

    sHtmlContent = ''
    oRequest = cRequestHandler(url)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    
    if postdata != None:
        oRequest.addHeaderEntry('X-Requested-With','XMLHttpRequest')
        oRequest.addHeaderEntry('Content-Type','application/x-www-form-urlencoded; charset=UTF-8')
        oRequest.addHeaderEntry('Referer','http://www.jheberg.net/redirect/xxxxxx/yyyyyy/')
        
    elif 'www.jheberg.net' in url:
        oRequest.addHeaderEntry('Referer', url.replace('http://www.jheberg.net/mirrors','http://www.jheberg.net/captcha').replace('\r',''))
    
    oRequest.addParametersLine(postdata)

    sHtmlContent = oRequest.request()

    return sHtmlContent

class cMultiup:
    def __init__(self):
        self.id = ''
        self.list = []
        
    def GetUrls(self,url):

        NewUrl = url.replace('http://www.multiup.org/fr/download','http://www.multiup.eu/fr/mirror').replace('http://www.multiup.eu/fr/download','http://www.multiup.eu/fr/mirror').replace('http://www.multiup.org/download', 'http://www.multiup.eu/fr/mirror')
        
        sHtmlContent = GetHtml(NewUrl)

        sPattern = 'nameHost="([^"]+)"\s+link="([^"]+)"\s+validity="([a-z]+)"'
        r = re.findall(sPattern,sHtmlContent,re.DOTALL)

        if not r:
            return False

        for item in r:

            if item[2] == 'valid' and not 'download-fast' in item[1]:
                self.list.append(item[1])
            
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
                postdata = urllib.urlencode(data)
                urllink = 'http://www.jheberg.net/get/link/'
                
                sHtmlContent = GetHtml(urllink,postdata)
                
                r = re.search('{"url": "([^"]+)"}', sHtmlContent)
                if r:              
                    self.list.append(r.group(1))
            
        return self.list
        
