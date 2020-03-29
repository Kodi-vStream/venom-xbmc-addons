#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#Wholecloud-Movshare
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
import re


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Wholecloud'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'wholecloud'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self, sUrl):
        sPattern = 'v=([^<]+)'
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def __getKey(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = False

        sId = self.__getIdFromUrl(self.__sUrl)

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        r = re.search('var fkzd="([^"]+)"', sHtmlContent)
        if (r):
            url = 'http://www.wholecloud.net/api/player.api.php?key=' + r.group(1) + '&file=' + sId
            oRequest = cRequestHandler(url)
            sHtmlContent = oRequest.request()
            r2 = re.search('^url=([^&]+)&', sHtmlContent)
            if (r2):
                api_call = r2.group(1)

        if (api_call):
            return True, api_call

        return False, False

