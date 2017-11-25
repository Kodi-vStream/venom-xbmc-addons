#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#http://uqload.com/embed-xxx.html
from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

sPattern1 = 'sources.+?"([^"]+mp4)"'

    
class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Uqload'
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
        return 'uqload'
        
    def setHD(self, sHD):
        self.__sHD = ''
        
    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()
    
    def __getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        aResult = oParser.parse(sHtmlContent, sPattern1)
        if (aResult[0] == True):
            api_call = aResult[1][0]

        if (api_call):
            return True, api_call
            
        return False, False

        
