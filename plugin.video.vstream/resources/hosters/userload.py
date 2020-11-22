#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
## https://userload.co/embed/xxxx

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.aadecode import AADecoder
from resources.lib.packer import cPacker
from resources.lib.comaddon import progress#, VSlog
import re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Userload'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'userload'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return False

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call = False
        url = self.__sUrl

        keymorocco = ''
        keymycountry= ''
        morocco = ''
        mycountry = ''

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        sHtmlContent1 = oRequestHandler.request()

        sPattern2 = '<script type="text/javascript">(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
        aResult = re.findall(sPattern2, sHtmlContent1)

        if aResult:
            str2 = aResult[0]
            if not str2.endswith(';'):
                str2 = str2 + ';'

            strs = cPacker().unpack(str2)
            sPattern3 = 'cfdcebbdaacf="([^"]+)".+?ffddacea="([^"]+)"'
            mycountry = re.search(sPattern3, strs).group(1)
            morocco = re.search(sPattern3, strs).group(2)

        if morocco and mycountry:
            url2 = 'https://userload.co/api/request/'
            pdata = 'morocco=' + morocco + '&mycountry=' + mycountry
            oRequest = cRequestHandler(url2)
            oRequest.setRequestType(1)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
            oRequest.addHeaderEntry('Content-Length', len(str(pdata)))
            oRequest.addHeaderEntry('Referer', url)
            oRequest.addParametersLine(pdata)
            api_call = oRequest.request()

            if 'mp4' in api_call  and 'uloadcdn.com' in api_call :
                return True, api_call.strip()

        return False, False
