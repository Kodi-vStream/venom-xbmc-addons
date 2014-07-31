from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'ZShare.net'
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
        return 'zshare'

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
        sPattern = '<iframe src="([^"]+)" '

        oRequest = cRequestHandler(self.getUrl())
        sHtmlContent = oRequest.request()

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sUrl = aResult[1][0]

            oRequest = cRequestHandler(sUrl)
            sHtmlContent = oRequest.request()

            sPattern = '<a href="([^"]+)" style="color: #666666; text-decoration: none;font-size:10px" target=_top>Download Video</a>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sUrl = aResult[1][0]

                oRequest = cRequestHandler(sUrl)
                oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
                oRequest.addParameters('referer2', '')
                oRequest.addParameters('download', 1)
                oRequest.addParameters('imageField.x', 76)
                oRequest.addParameters('imageField.y', 28)
                sHtmlContent = oRequest.request()

                sPattern = 'new Array.(.+?).;'
                aResult = oParser.parse(sHtmlContent, sPattern)

                if (aResult[0] == True):
                    sUrl = aResult[1][0]
                    sUrl = sUrl.replace("'","").replace(",","")

                    aResult = []
                    aResult.append(True)
                    aResult.append(sUrl)
                    return aResult

        return False, ''

