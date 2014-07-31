from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Loaded.it'
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
        return 'loadedit'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '<input type="hidden" name="code" value="(.*?)"'

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
	oRequestHandler = cRequestHandler(self.__sUrl)
	sHtmlContent = oRequestHandler.request();

	oParser = cParser()
        aResult = oParser.parse(sHtmlContent, self.getPattern())
	if (aResult[0] == True):
	    sCode = aResult[1]

	    oRequestHandler = cRequestHandler(self.__sUrl)
	    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
	    oRequestHandler.addParameters('code', sCode)
	    sHtmlContent = oRequestHandler.request();

	    sPattern = "playlist: \[.*?\,.*?},.*?url: '(.*?)'"
	    oParser = cParser()
	    aResult = oParser.parse(sHtmlContent, sPattern)
	    
	    if (aResult[0] == True):		
		return True, aResult[1][0]

	return False, ''
