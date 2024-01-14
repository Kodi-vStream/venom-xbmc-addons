# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# https://aparat.cam/embed-xxxxx.html

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Aparat'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'aparat'

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        url = self.__sUrl
        VideoType = 2  # dl mp4 lien existant non utilisé ici
        VideoType = 1  # m3u8

        list_q = []
        list_url = []

        if VideoType == 1:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent = oRequestHandler.request()

            oParser = cParser()
            sPattern = 'src:\s+"([^"]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if (aResult[0] == True):
                url2 = aResult[1][0]
                oRequestHandler = cRequestHandler(url2)
                sHtmlContent2 = oRequestHandler.request()

                # prend tous les formats  (peu créer problemes CODECS avc1)
                # sPattern = 'RESOLUTION=(\w+).+?(https.+?m3u8)'

                # limite les formats
                sPattern = 'PROGRAM-ID.+?RESOLUTION=(\w+).+?(https.+?m3u8)'
                aResult = oParser.parse(sHtmlContent2, sPattern)
                for aEntry in aResult[1]:
                    list_q.append(aEntry[0])
                    list_url.append(aEntry[1])  # parfois lien de meme qualité avec url diffrentes

            if list_url:
                api_call = dialog().VSselectqual(list_q, list_url)
                if api_call:
                    return True, api_call

        if VideoType == 2:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent = oRequestHandler.request()

            oParser = cParser()
            sPattern = 'file_code=(\w+)&hash=([^&]+)'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if (aResult[0] == True):
                id = aResult[1][0][0]
                hash = aResult[1][0][1]
                url = 'https://aparat.cam/dl?op=download_orig&id=' + id + '&mode=0&hash=' + hash  # + '&embed=1&adb=0'
                data = 'op=download_orig&id=' + id + '&mode=n&hash=' + hash
                oRequestHandler = cRequestHandler(url)
                oRequestHandler.setRequestType(1)
                oRequestHandler.addHeaderEntry('Referer', url)
                oRequestHandler.addParametersLine(data)
                sHtmlContent = oRequestHandler.request()

                sPattern = 'href="([^"]+.mp4)'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    api_call = aResult[1][0]
                    if api_call:
                        return True, api_call

        return False, False
