# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# http://player.vimple.ru/iframe/XXXXXXXXXXXXXXXXXXXXX

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):
    def __init__(self):
        self.__sDisplayName = 'Vimple'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + ' [/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'vimple'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self, sUrl):
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

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        req = urllib2.Request(self.__sUrl, None, headers)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        head = response.headers
        response.close()

        oParser = cParser()

        cookies = ''
        if 'Set-Cookie' in head:
            sPattern = '(?:^|,) *([^;,]+?)=([^;,\/]+?);'
            aResult = oParser.parse(str(head['Set-Cookie']), sPattern)
            if (aResult[0] == True):
                for cook in aResult[1]:
                    cookies = cookies + cook[0] + '=' + cook[1] + ';'
        # Get link
        sPattern = '"video":\[{"default":true,"url":"([^"]+?)"}]'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            url = aResult[1][0]
            url = url.replace('\/', '/')

            api_call = url + '|Cookie=' + cookies

            return True, api_call

        return False, False
