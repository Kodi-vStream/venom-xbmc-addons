#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#test sur http://vshare.eu/embed-wuqinr62cpn6-703x405.html
#         http://vshare.eu/embed-cxmr4o8l2waa-703x405.html
#         http://vshare.eu/embed-cxmr4o8l2waa703x405.html erreur code streambb

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
import re, xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Vshare'
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
        return 'vshare'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return False

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = re.sub('-*\d{3,4}x\d{3,4}', '', self.__sUrl)
        self.__sUrl = self.__sUrl.replace('https', 'http')

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        sUrl = self.__sUrl

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        if '<div id="deleted">' in sHtmlContent:
            return False, False

        oParser = cParser()
        sPattern = '<source src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            api_call = aResult[1][0]
        else:
            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sHtmlContent = cPacker().unpack(aResult[1][0])
                sPattern = '{file:"(http.+?vid.mp4)"'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    api_call = aResult[1][0]

        if (api_call):
            return True, api_call

        return False, False
