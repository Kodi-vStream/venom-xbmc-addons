from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster

import xbmc,re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Nowvideo'
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
        return 'nowvideo'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self):
        sPattern = "v=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)

        if (aResult[0] == True):
            return aResult[1][0]

        return ''
        
    def __modifyUrl(self, sUrl):
        if (sUrl.startswith('http://')):
            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.request()
            sRealUrl = oRequestHandler.getRealUrl()
            self.__sUrl = sRealUrl
            return self.__getIdFromUrl()

        return sUrl;
        
    def __getKey(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        
        sPattern =  'http:\/\/(?:www.|embed.)nowvideo.[a-z]{2}\/(?:video\/|embed.php\?.*?v=)([0-9a-z]+)'
         
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)        
        self.__sUrl = 'http://embed.nowvideo.sx/embed.php?v=' + str(aResult[1][0])

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        #xbmc.log(self.__sUrl)
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
        sPattern =  '<script type="text\/javascript" src="([^"]+)"><\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult):
            url1 = 'http://embed.nowvideo.sx' + aResult[1][0]
            
            oRequest = cRequestHandler(url1)
            sHtmlContent2 = oRequest.request()
            #a continuer quand ca va bloquer
            
        
        sPattern =  '<source src="([^"]+)" type=\'video\/mp4\'>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        #xbmc.log(str(aResult))

        if (aResult[0] == True):
            api_call = aResult[1][0]
            #xbmc.log(api_call)
            return True, api_call
        
        return False, False
