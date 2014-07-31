from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'SkyLoad.net'
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
        return 'skyload'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return "<param name='src' value='(.*?)'";

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        sPattern = 'var targetURL="([^"]+)"'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)        
        if (aResult[0] == True):
            self.__sUrl = aResult[1][0]
            
            oHosterHandler = cHosterHandler()
            return oHosterHandler.getUrl(self)

        return False, aResult



