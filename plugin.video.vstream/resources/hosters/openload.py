#coding: utf-8
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib.jjdecode import JJDecoder
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil


import re,urllib2, base64, math

import xbmc

def parseInt(sin):
    return int(''.join([c for c in re.split(r'[,.]',str(sin))[0] if c.isdigit()])) if re.match(r'\d+', str(sin), re.M) and not callable(sin) else None

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Openload'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'#[COLOR khaki]'+self.__sHD+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'openload'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('openload.io','openload.co')
        #self.__sUrl = self.__sUrl.replace('/embed/', '/f/')

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
        
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
        
        api_call = ''
        
        oParser = cParser()        
        
        #recuperation de la page
        xbmc.log('url teste : ' + self.__sUrl)
        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('User-Agent',UA)
        sHtmlContent = oRequest.request()
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        sPattern = '<span id="hiddenurl">(.+?)<\/span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if not (aResult[0]):
            return False,False

        string = aResult[1][0]
        
        string = cUtil().unescape(string)
        
        url = ''
        
        for c in string:
            v = ord(c)
            if v >= 33 and v <= 126:
                v = ((v + 14) % 94) + 33
            url = url + chr(v)
        

        
        api_call = "https://openload.co/stream/" + url + "?mime=true"
        
        xbmc.log(api_call)
        
        if (api_call):
            
            if 'openload.co/stream' in api_call:
                
                headers = {'User-Agent': UA }
                          
                req = urllib2.Request(api_call,None,headers)
                res = urllib2.urlopen(req)
                finalurl = res.geturl()
                #xbmc.log(finalurl)
                api_call = finalurl

            return True, api_call
            
        return False, False
 
