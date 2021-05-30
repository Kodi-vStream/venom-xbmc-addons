#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
## https://userload.co/embed/xxxx

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.aadecode import AADecoder
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog

import requests, re 

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

        urlapi = "https://userload.co/api/assets/userload/js/videojs.js"

        #A voir quel encodage il faut pour Kodi 18.
        sHtmlContent1 = requests.get(urlapi).content.decode('utf-8')

        oParser = cParser()
        sPattern = '(ﾟωﾟ.+?\(\'_\'\);)'
        aResult = oParser.parse(sHtmlContent1 , sPattern)

        if (aResult[0]== True):
            sdecode = AADecoder(aResult[1][0]).decode()

            sPattern =  'morocco=".([^\W]+).+?"&mycountry=".([^\W]+)'
            aResult_2 = oParser.parse(sdecode, sPattern)

            if (aResult_2[0] == True):
                keymorocco = aResult_2[1][0][0]
                keymycountry = aResult_2[1][0][1]

        referer = url.split('|Referer=')[1]
        url = url.split('|Referer=')[:-1][0]

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.addHeaderEntry('Referer', referer)
        sHtmlContent1 = oRequestHandler.request()

        sPattern2 = '<script type="text/javascript">(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
        aResult = re.findall(sPattern2, sHtmlContent1)

        if aResult:
            str2 = aResult[0]
            if not str2.endswith(';'):
                str2 = str2 + ';'

            strs = cPacker().unpack(str2)

            oParser = cParser()
            sPattern = 'var\s(.+?)="([^"]*)'
            aResult = oParser.parse(strs, sPattern)

            if (aResult[0]== True):
                for r in aResult[1]:
                    if r[0] == keymorocco:
                        morocco = r[1]
                    if r[0] == keymycountry:
                        mycountry = r[1]

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
