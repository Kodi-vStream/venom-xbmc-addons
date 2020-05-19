# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'ClipWatching'
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

    def isDownloadable(self):
        return False

    def getPluginIdentifier(self):
        return 'clipwatching'

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self, api_call=None):

        oParser = cParser()
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        # accelère le traitement
        sHtmlContent = oParser.abParse(sHtmlContent, 'var holaplayer', 'vvplay')
        # Traitement pour les liens m3u8
        sHtmlContent = sHtmlContent.replace(',', '').replace('master.m3u8', 'index-v1-a1.m3u8')
        sPattern = '"(http[^"]+(?:.m3u8|.mp4))"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            # initialisation des tableaux
            url = []
            qua = []
            n = 1

            # Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i))
                qua.append('Lien ' + str(n))
                n += 1

            # dialogue Lien si plus d'une url
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
