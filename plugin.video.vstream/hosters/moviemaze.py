from hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'MovieMaze.de'
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
        return 'moviemaze'

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
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        #FLASH
        sPattern = 's1.addVariable\("file","([^"]+)"\);'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sFile = aResult[1][0]

            sFile = 'http://www.moviemaze.de' + str(sFile)
            return True, sFile

        #NO FLASH
        sPattern = '<PARAM NAME="src" VALUE="([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            sFile = 'http://www.moviemaze.de' + str(aResult[1][0])
            return True, sFile

        return False, False