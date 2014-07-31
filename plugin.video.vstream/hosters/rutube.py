from hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import urllib

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'RuTube'
	self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
	self.__sFileName = sFileName

    def getFileName(self):
	return self.__sFileName
    
    def __getIdFromUrl(self, sUrl):
        sPattern = "http://.+?/.+?/([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''
    
    
    def setUrl(self, sUrl):
        if 'embed' not in sUrl:
            self.__sUrl = str(self.__getIdFromUrl(sUrl))
            self.__sUrl = 'http://rutube.ru/video/embed/' + str(self.__sUrl)
        else:
            self.__sUrl = sUrl

    def getPluginIdentifier(self):
        return 'rutube'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        #sId = self.__sUrl.replace('http://rutube.ru/video/embed/', '')
        sDialog = cUtil().dialog(self.__sDisplayName)
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        sPattern = '"m3u8": "(.+?)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):       
            return True, aResult[1][0]
            
        self.__oDialog.close()
        return False, False