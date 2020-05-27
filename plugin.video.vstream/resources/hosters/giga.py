# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# 2 hoster giga & 2gigalink
# from resources.lib.handler.requestHandler import cRequestHandler

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

import ssl

from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Giga'
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
        return 'giga'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return False

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        the_url = self.__sUrl
        myContext = ssl._create_unverified_context()

        req = urllib2.Request(the_url)
        handle = urllib2.urlopen(req, context=myContext)
        sHtmlContent = handle.read()
        handle.close()

        oParser = cParser()
        sPattern = "var mp4v = '(.+?)'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            return True, aResult[1][0]
        else:
            # streamgk
            sPattern = '<a id="downloadb" class="btn btn-default.+?href="([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                return True, aResult[1][0]

        return False, False
