#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://playtube.ws/embed-xxxxx.html
import re
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.packer import cPacker

UA = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Playtube'
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
        return 'playtube'

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

        url = self.__sUrl
        oRequestHandler = cRequestHandler(url)
        sHtmlContent = oRequestHandler.request()

        sPattern2 = '(\s*eval\s*\(\s*function(?:.|\s)+?\)\)\))'
        aResult = re.findall(sPattern2, sHtmlContent)
        list_url = []
        list_qua = []
        if aResult:
            str2 = aResult[0]
            if not str2.endswith(';'):
                str2 = str2 + ';'

            strs = cPacker().unpack(str2)
            oParser = cParser()
            sPattern = '(https.+?.m3u8)'
            aResult = re.findall(sPattern, strs)
            if aResult:
                urlhost = aResult[0]
                oRequestHandler = cRequestHandler(urlhost)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', url)
                sHtmlContent2 = oRequestHandler.request()
                oParser = cParser()
                sPattern = 'PROGRAM.*?BANDWIDTH.*?RESOLUTION=(\d+x\d+).*?(https.*?m3u8)'
                aResult = oParser.parse(sHtmlContent2, sPattern)
                if (aResult[0] == True):
                    for aEntry in aResult[1]:
                        list_url.append(aEntry[1])
                        list_qua.append(aEntry[0])

                    api_call = dialog().VSselectqual(list_qua, list_url)

        if (api_call):
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + url

        return False, False
