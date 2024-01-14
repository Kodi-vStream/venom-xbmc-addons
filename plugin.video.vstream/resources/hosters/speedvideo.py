# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Speedvideo'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR] [COLOR khaki]' + self.__sHD + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'speedvideo'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return False

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

        sPattern = 'https*:\/\/speedvideo.[a-z]{3}\/(?:embed-)?([0-9a-zA-Z]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            self.__sUrl = 'https://speedvideo.net/embed-' + aResult[1][0] + '.html'
        else:
            VSlog('ID error')

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        sPattern = 'var linkfile\s*=\s*"([^"]+)"'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sUrl = aResult[1][0]

            class NoRedirection(urllib2.HTTPErrorProcessor):
                def http_response(self, request, response):
                    return response

                https_response = http_response

            opener = urllib2.build_opener(NoRedirection)
            opener.addheaders = [('User-Agent', UA)]
            opener.addheaders = [('Referer', self.__sUrl)]
            response = opener.open(sUrl)
            if response.code == 301 or response.code == 302:
                api_call = response.headers['Location']

            response.close()

        if (api_call):
            return True, api_call

        return False, False
