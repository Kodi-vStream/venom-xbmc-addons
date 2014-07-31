from hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Bild.de'
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
        return 'bild'

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

        sPattern = '<enclosure url="([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            sRtmpFile = aResult[1][0]

            aSplitt = sRtmpFile.split('/ondemand/')

            aSplitt2 = aSplitt[1].split('?')
            sPlayPath = aSplitt2[0]
            sAuth = aSplitt2[1]

            sStreamUrl = aSplitt[0] + '/ondemand/?' + sAuth + ' playpath=' + sPlayPath

            return True, sStreamUrl

        return False, ''