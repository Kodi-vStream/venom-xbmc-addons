#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#Votre pseudo
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, isMatrix

import time

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):

        self.__sDisplayName = 'Dood'
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
        return 'dood'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self, sUrl):
        sPattern = "id=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl).replace('/e/','/d/')

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getHost(self):
        parts = self.__sUrl.split('//', 1)
        host = parts[0] + '//' + parts[1].split('/', 1)[0]
        return host        

    def __getMediaLinkForGuest(self):
        api_call = False

        headers = {'User-Agent': UA}
        if isMatrix():
            import urllib.request as urllib
        else:
            import urllib

        req = urllib.Request(self.__sUrl, None, headers)
        with urllib.urlopen(req) as response:
           sHtmlContent = response.read()

        oParser = cParser()
        
        time.sleep(6)
        sPattern = 'Download video.+?a href="([^"]+)"'
        d = "https://" + self.__sUrl.split('/')[2] + oParser.parse(sHtmlContent, sPattern)[1][0]

        oRequest = cRequestHandler(d)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', self.__sUrl)
        sHtmlContent = oRequest.request() 

        sPattern = "window\.open\('(.+?)'"
        api_call = oParser.parse(sHtmlContent, sPattern)[1][0]

        if (api_call):
            return True, api_call + '|Referer=https://dood.la/'

        return False, False
