# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

import xbmc

from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog


class cHoster(iHoster):
    def __init__(self):
        self.__sDisplayName = 'Uplea'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR violet]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'uplea'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self,url):
        sPattern = 'http:\/\/uplea\.com\/dl\/([0-9a-zA-Z]+)'
        oParser = cParser()
        aResult = oParser.parse(url, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]
        return ''

    def __modifyUrl(self, sUrl):
        return ''

    def __getKey(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        import sys
        if 'site=cDownload&function' not in sys.argv[2]:
            oDialog = dialog().VSok("ATTENTION, Pas de streaming sans premium\nPour voir le film passer par l'option 'Télécharger et Lire' du menu contextuel.")
            return False, False
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        # http:///dl/12345XXYEEEEREERERE

        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
        headers = {'User-Agent': UA,
                   'Host': 'uplea.com',
                   # 'Referer': self.__sUrl ,
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3'
                   # 'Content-Type': 'application/x-www-form-urlencoded'
                   }

        req = urllib2.Request(self.__sUrl, None, headers)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        head = response.headers
        response.close()

        oParser = cParser()

        # get step
        urlstep = ''
        sPattern = '<a href="(\/step\/[^<>"]+)">'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            urlstep = aResult[1][0]

        # get cookie
        cookies = ''
        if 'Set-Cookie' in head:
            cookies = head['Set-Cookie']
            sPattern = '(__cfduid=[0-9a-z]+;).+?(PHPSESSID=[0-9a-z]+)'
            aResult = oParser.parse(str(cookies), sPattern)
            if (aResult[0] == True):
                cookies = str(aResult[1][0][0]) + str(aResult[1][0][1])

        url = 'http://uplea.com' + urlstep

        headers['Cookie'] = cookies
        headers['Referer'] = self.__sUrl

        req = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        head = response.headers
        response.close()

        # fh = open('c:\\test.txt', "w")
        # fh.write(sHtmlContent)
        # fh.close()

        # waiting time
        waitingtime = 20
        sPattern = "ulCounter\({'timer':([0-9]+)}\);"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            waitingtime = int(aResult[1][0]) + 2

        sPattern = '<a class="button-download" href="([^<>"]+?)">'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            dialog.VSinfo('Waiting time', self.__sDisplayName, waitingtime)
            xbmc.sleep(waitingtime*1000)

            # print(aResult[1][0])

            return True, aResult[1][0] + '|User-Agent=' + UA  # + '&Referer=' + self.__sUrl

        return False, False
