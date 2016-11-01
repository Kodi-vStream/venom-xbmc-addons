from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import re,urllib

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Veehd'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'veehd'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call = ''

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        sPattern = 'load_stream.+?{src : "([^"]+)"}' 
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            sUrl = 'http://veehd.com'+ aResult[1][0]
            oRequest = cRequestHandler(sUrl)
            sHtmlContent = oRequest.request()

            #avidivx
            sPattern = '<embed.+?src="([^"]+)"'
            r2 = re.search(sPattern,sHtmlContent)
            if (r2):
                api_call = r2.group(1)

            #mp4
            sPattern = ',"url":"([^"]+)","scaling":"fit"}'
            r3 = re.search(sPattern,sHtmlContent)
            if (r3):
                api_call = urllib.unquote(r3.group(1))

        if (api_call):
            return True, api_call

        return False , False
