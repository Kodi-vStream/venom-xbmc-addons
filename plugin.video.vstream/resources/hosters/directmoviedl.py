# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'DirectMovieDl'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'directmoviedl'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self, sUrl):
        sPattern = "id=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = False

        if 'movie.directmoviedl' in self.__sUrl:
            oRequest = cRequestHandler(self.__sUrl)
            sHtmlContent = oRequest.request()
            oParser = cParser()
            sPattern = '="([^"]+)" type="video/mp4'
            aResult = oParser.parse(sHtmlContent, sPattern)
            api_call = aResult[1][0]
        else:
            oRequest = cRequestHandler(self.__sUrl)
            sHtmlContent = oRequest.request()
            oParser = cParser()
            sPattern = 'src="(http.+?)"'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0] is True:
                for aEntry in aResult[1]:
                    sHoster = aEntry
                    oRequest = cRequestHandler(sHoster)
                    sHtmlContent1 = oRequest.request()
                    sPattern1 = '="([^"]+)" type="video/mp4'
                    aResult1 = oParser.parse(sHtmlContent1, sPattern1)
                    api_call = aResult1[1][0]

        if api_call:
            return True, api_call

        return False, False
