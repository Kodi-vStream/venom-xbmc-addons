# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# http://uqload.com/embed-xxx.html

import re
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
UA = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'


class cHoster(iHoster):
    def __init__(self):
        self.__sDisplayName = 'Plynow'
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
        return 'plynow'

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
        try:
            import urllib.parse as urllib
        except:
            import urllib

        # On récupere l'array
        sPattern = '<script>\s*\(function\(\).+?=(.+?)var player'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult):
            for aEntry in aResult[1]:
                uHv4sb = aEntry

        # uHv4sb = re.search('<script>\s*\(function\(\).+?=(.+?);','f', re.DOTALL).group(1)

        # On récupere chaque element de l'array et ont le mets dans un tuple que Python gere
        b = re.findall('"(.+?)"', str(uHv4sb))
        x = []

        for a in b:
            # Unquote decode les elements qui sont en unicode.
            x.append(urllib.unquote(a.replace('\\x', '%')))

        # On inverse le resultat et l'assemble en un string.
        result = ''.join(x)[::-1]
        sHosterUrl = re.findall('src="([^"]+)', result)
        sHosterUrl = str(sHosterUrl).replace('[', '').replace(']', '').replace("'", '')
        api_call = sHosterUrl

        if (api_call):
            return True, api_call  # + '|User-Agent=' + UA + '&Referer=' + self.__sUrl

        return False, False
