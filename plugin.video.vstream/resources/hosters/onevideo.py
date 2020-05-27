# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.util import Unquote


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Onevideo'
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
        return 'onevideo'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self):
        sPattern = "id=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def __modifyUrl(self, sUrl):
        if (sUrl.startswith('http://')):
            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.request()
            sRealUrl = oRequestHandler.getRealUrl()
            self.__sUrl = sRealUrl
            return self.__getIdFromUrl()

        return sUrl

    def __getKey(self):
        oRequestHandler = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'key: "(.+?)";'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            aResult = aResult[1][0].replace('.', '%2E')
            return aResult

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('http://www.onevideo.to/', '')
        self.__sUrl = self.__sUrl.replace('embed.php?id=', '')
        self.__sUrl = 'http://www.onevideo.to/embed.php?id=' + str(self.__sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        #api_call = ('http://www.nowvideo.sx/api/player.api.php?key=%s&file=%s') % (self.__getKey(), self.__getIdFromUrl())
        api_call = ('http://www.onevideo.to/api/player.api.php?user=undefined&codes=1&file=%s&pass=undefined&key=%s') % (self.__getIdFromUrl(), self.__getKey())

        oRequest = cRequestHandler(api_call)
        sHtmlContent = oRequest.request()

        sPattern =  'url=(.+?)&title'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            stream_url = Unquote(aResult[1][0])
            return True, stream_url
        else:
            return False, False

        return False, False
