from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import time
class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Vidtodo'
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
        return 'vidtodo'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)  
        self.__sUrl = self.__sUrl.replace('embed-', '')
        self.__sUrl = self.__sUrl.replace('.html', '')
        
    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = ''
        
        oParser = cParser()
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        sPattern =  '<input type="hidden" name="([^"]+)" value="([^"]+)"'

        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True): 
            time.sleep(3)
            oRequest = cRequestHandler(self.__sUrl)
            oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
            for aEntry in aResult[1]:
                oRequest.addParameters(aEntry[0], aEntry[1])

            oRequest.addParameters('referer', self.__sUrl)
            sHtmlContent = oRequest.request()

            sPattern = '{file: *"([^"]+(?<!smil))"}'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                api_call = aResult[1][0]
    
            else:
                sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    sHtmlContent = cPacker().unpack(aResult[1][0])
                    sPattern = '{file: *"([^"]+(?<!smil))"}'
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    if (aResult[0] == True):
                        api_call = aResult[1][0]

        if (api_call):
            return True, api_call
            
        return False, False
