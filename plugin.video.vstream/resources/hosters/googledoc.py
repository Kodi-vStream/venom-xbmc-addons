#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

import re, urllib, urllib2

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'GoogleDoc'
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
        return 'googledoc'

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
        sPattern = 'docs.google.+?([a-zA-Z0-9-_]{20,40})'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call = ''

        #reformatage du lien
        sId = self.__getIdFromUrl(self.__sUrl)
        sUrl = 'https://drive.google.com/file/d/' + sId + '/view' #?pli=1

        #VSlog(sUrl)

        req = urllib2.Request(sUrl)
        response = urllib2.urlopen(req)
        sHtmlContent = response.read()
        Headers = response.headers
        response.close()

        #listage des cookies
        c = Headers['Set-Cookie']
        c2 = re.findall('(?:^|,) *([^;,]+?)=([^;,\/]+?);', c)
        if c2:
            cookies = ''
            for cook in c2:
                cookies = cookies + cook[0] + '=' + cook[1] + ';'

        #VSlog(cookies)
        

        sPattern = 'url_encoded_fmt_stream_map".+?url\\\u003d([^"]+)'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)


        if not aResult[0]:
            #sUrl = 'https://drive.google.com/uc?export=download&id=' + sId + '&confirm=make'
            if '"errorcode","150"]' in sHtmlContent:
                dialog().VSinfo("Nombre de lectures max dépassé")
            return False,False

        api_call = urllib.unquote(aResult[1][0]).decode('unicode-escape')

        #VSlog(api_call)

        if (api_call):
            return True, api_call + '|User-Agent=' + UA + '&Cookie=' + cookies

        return False, False
