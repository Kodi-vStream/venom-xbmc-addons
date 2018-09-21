#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
#from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Vidbom'
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
        return 'vidbom'

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

        sPattern = 'sources: *\[{file:"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0]
        else:
            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\)\)\))'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sHtmlContent = cPacker().unpack(aResult[1][0])
                sPattern = '{file:"([^"]+.mp4)"'
                aResult = oParser.parse(sHtmlContent,sPattern)
                if (aResult[0] == True):
                    api_call = aResult[1][0]

        if (api_call):
            return True, api_call

        return False, False
