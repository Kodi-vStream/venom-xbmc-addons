#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
## https://userload.co/embed/xxxx

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.aadecode import AADecoder
from resources.lib.packer import cPacker

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

        oRequestHandler = cRequestHandler(urlapi)
        sHtmlContent1 = oRequestHandler.request()

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

        oRequestHandler = cRequestHandler(url)
        sHtmlContent = oRequestHandler.request()

        bvalid, svalue = CheckCpacker(sHtmlContent )
        if bvalid:

            sPattern = 'var\s(.+?)="([^"]*)'
            aResult = oParser.parse(svalue, sPattern)

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
                    oRequest.addHeaderEntry('Referer', url)
                    oRequest.addParametersLine(pdata)#
                    api_call = oRequest.request()
                    if 'mp4' in api_call  and 'uloadcdn.com' in api_call :
                        return True, api_call.strip()

        return False, False


def CheckCpacker(sHtmlContent):
    oParser = cParser()
    sPattern = "(eval\(function\(p,a,c,k,e.+?)\s*<\/script>"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        strpacked = aResult[1][0]
        try:
            result = cPacker().unpack(strpacked)
            return True ,result
        except:
            pass

    return False, False
