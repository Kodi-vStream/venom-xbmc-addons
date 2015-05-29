from resources.lib.jsunpacker import cJsUnpacker
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import cUtil
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'FileBase.to'
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
        return 'filebase'

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

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
                
        sPattern = '<form action="#" method="post">.*?id="uid" value="([^"]+)" />'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            sUid = aResult[1][0]
            
            oRequest = cRequestHandler(self.__sUrl)
            oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
            oRequest.addParameters('dl_free12','DivX Stream')
            oRequest.addParameters('uid', sUid)
            sHtmlContent = oRequest.request()
            
            sPattern = '<input type="hidden" id="uid" name="uid" value="([^"]+)" />'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)

            if (aResult[0] == True):
                sUid = aResult[1][0]

                oRequest = cRequestHandler(self.__sUrl)
                oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
                oRequest.addParameters('captcha','ok')
                oRequest.addParameters('filetype','divx')
                oRequest.addParameters('submit','Download')
                oRequest.addParameters('uid', sUid)
                sHtmlContent = oRequest.request()
                
                sPattern = '<param value="([^"]+)" name="src" />'
                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern)
                
                if (aResult[0] == True):
                    sMediaFile = aResult[1][0]
                    return True, sMediaFile
                
        return False, aResult

