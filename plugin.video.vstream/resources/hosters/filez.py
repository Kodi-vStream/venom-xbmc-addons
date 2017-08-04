#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.config import cConfig 
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Filez'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'filez'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self, sUrl):
        sPattern = 'https*://filez.tv/([^<]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl).replace('embed/', '')
        self.__sUrl = self.__sUrl.replace('www.', '')
        self.__sUrl = self.__sUrl.replace('u=', '')

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
    
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        sId = self.__getIdFromUrl(self.__sUrl)
        
        sUrl = 'http://filez.tv/embed/u=' + sId
        
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = 'file: *"([^"]+)",'
        aResult = oParser.parse(sHtmlContent,sPattern)

        if (aResult[0] == True):
            api_call = aResult[1][0]

        if (api_call):
            return True, api_call
            
        return False, False
