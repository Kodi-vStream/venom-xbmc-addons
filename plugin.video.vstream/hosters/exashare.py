from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Exashare'
	self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
	self.__sFileName = sFileName

    def getFileName(self):
	return self.__sFileName

    def getPluginIdentifier(self):
        return 'exashare'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self, sUrl):
        sPattern = "http://exashare.com/([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        if 'embed' not in sUrl:
            self.__sUrl = str(self.__getIdFromUrl(sUrl))
            self.__sUrl = 'http://exashare.com/embed-'+str(self.__sUrl)+'.html'
        else:
            self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        cGui().showInfo('Resolve', self.__sDisplayName, 5)
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        sPattern = 'file: "([^"]+)"';
        
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            api_call = aResult[1][0]
            return True, api_call             
            
        return False, False
        
        