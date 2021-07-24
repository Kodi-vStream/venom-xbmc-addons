# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.lib.handler.requestHandler import cRequestHandler

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'

class cHoster(iHoster):
    def __init__(self):
        self.__sDisplayName = 'Megaup'
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
        return 'megaup'

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

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        import requests, re, time

        oRequestHandler = cRequestHandler(self.__sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()
        cookies = oRequestHandler.GetCookies() + ";"

        data = re.search('Mhoa_URL\((.+?)\);',sHtmlContent).group(1)
        data = re.findall("'(.+?)'",data)

        part1 = data[0]
        part2 = data[1]
        file = data[2]
        size = data[3]

        cidken = ''
        d1p1 = part1[0:len(part1)//4]
        cidken += d1p1[::-1]
        d1p2 = part1[len(part1)//4*2:len(part1)//4*3]
        cidken += d1p2[::-1]
        d2p1 = part2[3:(len(part2)+3)//2]
        cidken += d2p1[::-1]

        time.sleep(6)

        oRequestHandler = cRequestHandler("https://download.megaup.net/?idurl=" + cidken + "&idfilename=" + file + "&idfilesize=" + size)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()

        la = re.search('window\.location\.replace\("(.+?)"',sHtmlContent).group(1)

        oRequestHandler = cRequestHandler(la)
        oRequestHandler.disableRedirect()
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry("Referer", "https://download.megaup.net/")
        oRequestHandler.addHeaderEntry("Cookie", cookies)        
        sHtmlContent = oRequestHandler.request()
        api_call = oRequestHandler.getResponseHeader()['Location']

        if api_call:
            return True,  api_call + "|User-Agent="+UA

        return False, False
