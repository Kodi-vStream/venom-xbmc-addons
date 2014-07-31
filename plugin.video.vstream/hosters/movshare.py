from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'MovShare.net'
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
        return 'movshare'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '<param name="src" value="(.*?)"';

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
        
        sPattern = '<form id="watch" name="watch" method="post" action=""><input type="hidden" name="wm" value="([^"]+)">'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            sUid = aResult[1][0]

            oRequest = cRequestHandler(self.__sUrl)
            oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
            oRequest.addParameters('submit.x','149')
            oRequest.addParameters('submit.y', '19')
            oRequest.addParameters('wm', sUid)
            sHtmlContent = oRequest.request()

            aMediaLink = cParser().parse(sHtmlContent, self.getPattern())
            
            if (aMediaLink[0] == True):
                return True, str(aMediaLink[1][0])

        return False, False


