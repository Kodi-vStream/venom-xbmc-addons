from resources.lib.jsunpacker import cJsUnpacker
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'VidBux.com'
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
        return 'vidbux'

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
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        sPattern = '<input name="([^"]+)".*?value=([^>]+)>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            oRequest = cRequestHandler(self.__sUrl)
            oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)

            for aEntry in aResult[1]:
                oRequest.addParameters(str(aEntry[0]), str(aEntry[1]).replace('"',''))

            sHtmlContent = oRequest.request()
            return self.__getUrlFromJavascriptCode(sHtmlContent)

        return self.__getUrlFromJavascriptCode(sHtmlContent)

    def __getUrlFromJavascriptCode(self, sHtmlContent):
        sPattern = "<script type='text/javascript'>eval.*?return p}\((.*?)</script>"
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            sJavascript = aResult[1][0]
            
            sUnpacked = cJsUnpacker().unpackByString(sJavascript)
            sPattern = ".addVariable\('file','([^']+)'"
            oParser = cParser()
            aResultLink = oParser.parse(sUnpacked, sPattern)
            
            if (aResultLink[0] == True):
                aResult = []
                aResult.append(True)
                aResult.append(aResultLink[1][0])
                return aResult

        return False, ''

