# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog  # , VSlog

# import re


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Freshstream'
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
        return 'freshstream'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    # Ne sert plus
    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self, sUrl):
        sPattern = 'id=([^"]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0]):
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

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = "var vsuri = \'(.+?)\'"
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0]):
            oRequest = cRequestHandler(aResult[1][0])
            sHtmlContent1 = oRequest.request()

            sPattern1 = '"([^"]+)":"([^"]+)"'
            aResult1 = oParser.parse(sHtmlContent1, sPattern1)

        if (aResult1[0]):

            url = []
            qua = []
            api_call = False

            for aEntry in aResult1[1]:
                url.append(aEntry[1])
                qua.append(aEntry[0])

            api_call = dialog().VSselectqual(qua, url)

            if (api_call):
                return True, api_call

        return False, False
