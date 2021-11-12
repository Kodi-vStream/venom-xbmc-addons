# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# type
# https://www.youtube.com/embed/etc....
# https://www.youtube.com/watch?v=etc...
# http://www.youtube-nocookie.com/v/etc...
# https://youtu.be/etc...

import time

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler


class cHoster(iHoster):
    def __init__(self):
        self.__sDisplayName = 'Youtube'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''
        self.__res = False

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'youtube'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def setResolution(self, res):
        self.__res = res

    def isDownloadable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, sUrl):
        return

    def getMediaLink(self):
        first_test = self.__getMediaLinkForGuest()
        return first_test

    def __getMediaLinkForGuest(self):
        UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'

        oRequestHandler = cRequestHandler("https://yt1s.com/api/ajaxSearch/index")
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('Origin', 'https://yt1s.com')
        oRequestHandler.addHeaderEntry('Referer', 'https://yt1s.com/fr13')
        oRequestHandler.addParameters("q", self.__sUrl)
        oRequestHandler.addParameters("vt", "home")
        sHtmlContent = oRequestHandler.request(jsonDecode=True)

        oRequestHandler = cRequestHandler("https://yt1s.com/api/ajaxConvert/convert")
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('Origin', 'https://yt1s.com')
        oRequestHandler.addHeaderEntry('Referer', 'https://yt1s.com/fr13')
        oRequestHandler.addParameters("vid", self.__sUrl.split("v=")[1])
        oRequestHandler.addParameters("k", sHtmlContent['links']["mp4"]["auto"]["k"])
        try:
            api_call = oRequestHandler.request(jsonDecode=True)['dlink']
        except:
            time.sleep(3)
            oRequestHandler = cRequestHandler("https://yt1s.com/api/ajaxConvert/convert")
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('Origin', 'https://yt1s.com')
            oRequestHandler.addHeaderEntry('Referer', 'https://yt1s.com/fr13')
            oRequestHandler.addParameters("vid", self.__sUrl.split("v=")[1])
            oRequestHandler.addParameters("k", sHtmlContent['links']["mp4"]["auto"]["k"])
            api_call = oRequestHandler.request(jsonDecode=True)['dlink']

        if api_call:
            return True, api_call
        else:
            return False
