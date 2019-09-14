#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Streamax'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'streamax'

    def isDownloadable(self):
        return True
        
    def __getIdFromUrl(self, sUrl):
        sPattern = 'id=([a-zA-Z0-9]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)

        if (aResult[0] == True):
            return aResult[1][0]
        return ''
        
    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        oParser = cParser()

        id = self.__getIdFromUrl(self.__sUrl)

        sUrl = 'https://streamax.club/hls/' + id + '/' + id + '.playlist.m3u8'
        
        url = []
        qua = []

        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer','https://streamax.club/public/dist/index.html?id=' + id)
        sHtmlContent = oRequest.request()

        sPattern = 'RESOLUTION=(\d+x\d+)(.+?.m3u8)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                url.append('https://streamax.club' + aEntry[1])
                qua.append(aEntry[0])

            if (url):
                api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call

        return False, False
