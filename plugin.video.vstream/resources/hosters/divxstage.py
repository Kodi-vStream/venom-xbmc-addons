#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
import urllib

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'DivxStage'
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
        return 'divxstage'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def __getIdFromUrl(self,sUrl):
        sPattern = 'v=([^<]+)'
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def __getKey(self,sUrl):
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        sPattern = 'var fkz="([^"]+)";'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            aResult = aResult[1][0].replace('.', '%2E')
            return aResult

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('http://embed.divxstage.eu/', '')
        self.__sUrl = self.__sUrl.replace('http://www.divxstage.to/', '')
        self.__sUrl = self.__sUrl.replace('http://www.cloudtime.to/', '')
        self.__sUrl = self.__sUrl.replace('video/', '')
        self.__sUrl = self.__sUrl.replace('embed.php?v=', '')
        self.__sUrl = self.__sUrl.replace('&width=711&height=400', '')
        self.__sUrl = 'http://embed.divxstage.eu/embed.php?v=' + str(self.__sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        id = self.__getIdFromUrl(self.__sUrl)
        sUrl = 'http://www.cloudtime.to/embed/?v=' + id
        cKey =  self.__getKey(sUrl)

        api_call = 'http://www.cloudtime.to/api/player.api.php?key=' + cKey + '&file=' + id
        
        oRequest = cRequestHandler(api_call)
        sHtmlContent = oRequest.request()
        
        sPattern =  'url=(.+?)&title'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            stream_url = urllib.unquote(aResult[1][0])
            return True, stream_url
        
        return False, False
