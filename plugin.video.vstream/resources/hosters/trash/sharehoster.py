from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
import time
import random

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'ShareHoster.com'
	self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName

    def setFileName(self, sFileName):
	self.__sFileName = sFileName

    def getFileName(self):
	return self.__sFileName

    def getPluginIdentifier(self):
        return 'sharehoster'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ""

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
	aSplit = self.__sUrl.split('/')
	sId = aSplit[-1]

	sUrl = 'http://www.sharehoster.com/flowplayer/config.php?movie=' + sId
	
	oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

	sPattern = "playlist': \[.*?},.*?'url': '(.*?)'"
	oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

	if (aResult[0] == True):
            sFileName = aResult[1][0]
	    return True, sFileName

	return False, ''

    def __getPhpSessionId(self, aHeader):
        sReponseCookie = aHeader.getheader("Set-Cookie")
        aResponseCookies = sReponseCookie.split(";")
        return aResponseCookies[0]