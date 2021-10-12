# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# type
# https://www.youtube.com/embed/etc....
# https://www.youtube.com/watch?v=etc...
# http://www.youtube-nocookie.com/v/etc...
# https://youtu.be/etc...

import re
import requests
import time

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, isMatrix
from resources.lib.config import GestionCookie
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import Unquote, Quote


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

        if first_test != False:
            return first_test
        else:
            return self.__getMediaLinkForGuest2()

    def deescape(self, escaped):
        if isMatrix():
            return escaped.encode().decode('unicode_escape')
        else:
            return escaped.decode('string_escape')

    def __getMediaLinkForGuest(self):
        api_call = ''
        UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'

        oRequestHandler = cRequestHandler("https://yt1s.com/api/ajaxSearch/index")
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('Origin', 'https://yt1s.com')
        oRequestHandler.addHeaderEntry('Referer', 'https://yt1s.com/fr13')
        oRequestHandler.addParameters("q", self.__sUrl)
        oRequestHandler.addParameters("vt","home")
        sHtmlContent = oRequestHandler.request(jsonDecode=True)

        aResult = sHtmlContent['links']["mp4"]["auto"]["k"]

        oRequestHandler = cRequestHandler("https://yt1s.com/api/ajaxConvert/convert")
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('Origin', 'https://yt1s.com')
        oRequestHandler.addHeaderEntry('Referer', 'https://yt1s.com/fr13')
        oRequestHandler.addParameters("vid", self.__sUrl.split("v=")[1])
        oRequestHandler.addParameters("k",aResult)
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
            oRequestHandler.addParameters("k",aResult)
            api_call = oRequestHandler.request(jsonDecode=True)['dlink']

        if api_call:
            return True, api_call
        else:
            return False

    def __getMediaLinkForGuest2(self):
        api_call = ''

        oRequest = cRequestHandler('https://ytoffline.net/fr1')
        oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        sHtmlContent = oRequest.request()

        tok = re.search('id="token" value="(.+?)"', sHtmlContent).group(1)
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

        oParser = cParser()
        pdata = 'url=' + Quote(self.__sUrl) + '&token=' + tok

        oRequest = cRequestHandler('https://ytoffline.net/fr1/download/')
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        oRequest.addHeaderEntry('Content-Length', len(pdata))
        oRequest.addHeaderEntry('Referer', 'https://ytoffline.net/fr1/')
        oRequest.addParametersLine(pdata)

        sHtmlContent = oRequest.request()

        sStart = '<div id="mp4" class="display-block tabcontent">'
        sEnd = '<div id="audio" class="tabcontent">'
        sHtmlContent1 = oParser.abParse(sHtmlContent, sStart, sEnd)
        sPattern = '<td>([^<]+)<small>.+?data-href="([^"]+)"'
        aResult = oParser.parse(sHtmlContent1, sPattern)

        if (aResult[0] == True):
            # initialisation des tableaux
            url = []
            qua = []
            # Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[1]))
                qua.append(str(i[0]))

            # dialogue qualité
            api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call

        return False, False
