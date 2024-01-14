# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://streamz.cc/xxx
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog
import re

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'


def Getheader(url, c):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.disableRedirect()
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Cookie', c)
    sHtmlContent = oRequestHandler.request()
    return oRequestHandler.getResponseHeader()['Location']


class cHoster(iHoster):
    def __init__(self):
        self.__sDisplayName = 'Streamz'
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
        return 'streamz'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def getPattern(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        api_call = False
        
        oParser = cParser()

        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()
        
        urlDownload = oRequest.getRealUrl()
        host = 'https://' + urlDownload.split('/')[2]

        cookie = oRequest.GetCookies()

        # By-pass fake video
        # Get url
        urlJS = host + '/js/count.js'
        oRequest = cRequestHandler(urlJS)
        oRequest.addHeaderEntry('User-Agent', UA)
        JScode = oRequest.request()
        
        JScode = JScode.replace(' ', '')
        
        r = "if\(\$\.adblock!=null\){\$\.get\('([^']+)',{([^}]+)}"
        aResult = oParser.parse(JScode, r)
        
        if not aResult[0]:
            return False, False
        
        data = aResult[1][0][1].split(':')
        Fakeurl = aResult[1][0][0] + '?' + data[0] + '=' + data[1].replace("'", "")
        
        # Request URL
        oRequest = cRequestHandler(Fakeurl)
        oRequest.addHeaderEntry('User-Agent', UA)
        try:
            tmp = oRequest.request()
        except:
            pass
        sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for i in aResult[1]:
                decoded = cPacker().unpack(i)

                if "videojs" in decoded:
                    decoded = decoded.replace('\\', '')

                    r = re.search("src:'([^']+)'", decoded, re.DOTALL)
                    if r:
                        url = r.group(1)

            VSlog(url)
            url = url.replace("getlink-", "getmp4-")

            api_call = Getheader(url, cookie)

        VSlog(api_call)

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self.__sUrl

        return False, False
