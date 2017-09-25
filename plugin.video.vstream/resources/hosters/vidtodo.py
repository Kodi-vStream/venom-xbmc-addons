from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import time,re

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'

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
        
    def __getIdFromUrl(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)  
        self.__sUrl = self.__sUrl.replace('embed-', '')
        self.__sUrl = self.__sUrl.replace('.html', '')
        if not self.__sUrl.startswith('https'):
            self.__sUrl = self.__sUrl.replace('http', 'https')
        

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()
        
    def extractSmil(self,smil):
        oRequest = cRequestHandler(smil)
        oRequest.addParameters('referer', self.__sUrl)
        sHtmlContent = oRequest.request()
        Base = re.search('<meta base="(.+?)"',sHtmlContent)
        Src = re.search('<video src="(.+?)"',sHtmlContent)
        return Base.group(1) + Src.group(1)

    def __getMediaLinkForGuest(self):
        api_call = ''
        
        oParser = cParser()
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        sPattern =  '<input type="(?:hidden|submit)" name="([^"]+)" value="([^"]+)"'

        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True): 
            time.sleep(3)
            oRequest = cRequestHandler(self.__sUrl)
            oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
            for aEntry in aResult[1]:
                oRequest.addParameters(aEntry[0], aEntry[1])

            oRequest.addParameters('referer', self.__sUrl)
            oRequest.addHeaderEntry('User-Agent', UA)
            
            sHtmlContent = oRequest.request()

            sPattern = '{file: *"([^"]+smil)"}'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                api_call = self.extractSmil(aResult[1][0])
    
            else:
                sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    sHtmlContent = cPacker().unpack(aResult[1][0])

                    sPattern = '{file: *"([^"]+smil)"}'
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    if (aResult[0] == True):
                        api_call = self.extractSmil(aResult[1][0])
                    else:
                        sPattern = '{file: *"([^"]+mp4)"'
                        aResult = oParser.parse(sHtmlContent, sPattern)
                        if (aResult[0] == True):
                            api_call = aResult[1][0]
  
        if (api_call):
            return True, api_call
            
        return False, False
