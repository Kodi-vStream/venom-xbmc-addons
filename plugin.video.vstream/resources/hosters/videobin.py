# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'VideoBIN'
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
        return 'videobin'

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

        oParser = cParser()
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        #accelère le traitement
        sHtmlContent = oParser.abParse(sHtmlContent, 'var player', 'vvplay')
        # Traitement pour les liens m3u8
        sHtmlContent = sHtmlContent.replace(',', '').replace('master.m3u8', 'index-v1-a1.m3u8')
        sPattern = '"(http[^"]+(?:.m3u8|.mp4))"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            api_call = ''

            # initialisation des tableaux
            url=[]
            qua=[]
            n = 1

            # Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i))
                qua.append('Lien ' + str(n))
                n += 1

            # dialogue qualité
            api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call

        return False, False
