#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.hunter import hunter
from resources.lib.comaddon import VSlog, isMatrix
import re
import base64

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'UpVideo'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'upvideo'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()


    def __getMediaLinkForGuest(self):
        api_call = False
        oParser = cParser()
        sPattern = 'return decodeURIComponent\(escape\(r\)\)}\("([^,]+)",([^,]+),"([^,]+)",([^,]+),([^,]+),([^,\))]+)\)'

        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('Cookie', 'popads2=opened')
        sHtmlContent = oRequest.request()
        
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        #Get decode page
        #oRequest = cRequestHandler("https://upvideo.to/assets/js/tabber.js")
        #oRequest.addHeaderEntry('Referer', self.__sUrl)
        #sHtmlContent2 = oRequest.request()
        #aResult2 = oParser.parse(sHtmlContent2, sPattern)

        #if (aResult2[0] == True):
        #    j = aResult2[1][0]
        #    decoder = hunter(j[0],int(j[1]),j[2],int(j[3]),int(j[4]),int(j[5]))
        #    VSlog("Decoder ok")
            
        if (aResult[0] == True):
            l = aResult[1]
            for j in l:
                data = hunter(j[0],int(j[1]),j[2],int(j[3]),int(j[4]),int(j[5]))
                if "fcbbbdddebad" in data:                    
                    r = re.search('var fcbbbdddebad *= *"([^"]+)" *;', data)
                    if not r:
                        VSlog('er2')
                    v2 = r.group(1).split('aHR0')[1].split('YTk0NT')[0]

                    if isMatrix():
                        api_call = "htt" + (base64.b64decode(v2).decode())
                    else:
                        api_call = "htt" + base64.b64decode(v2)

        if (api_call):
            return True, api_call

        return False, False
