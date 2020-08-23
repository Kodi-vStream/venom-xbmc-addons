#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#Votre pseudo
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog

import time, random, base64

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'

def compute(s):
    a = s.replace("/","1")
    a = base64.b64decode(a)
    a = a.replace("/","Z")
    a = base64.b64decode(a)
    a = a.replace("@","a")
    a = base64.b64decode(a)
    return a

class cHoster(iHoster):

    def __init__(self):

        self.__sDisplayName = 'Dood'
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
        return 'dood'

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
        sPattern = "id=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        self.__sUrl = self.__sUrl.replace('/d/','/e/')

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getHost(self):
        parts = self.__sUrl.split('//', 1)
        host = parts[0] + '//' + parts[1].split('/', 1)[0]
        return host        

    def __getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()
        
        urlDonwload = oRequest.getRealUrl()
        
        oParser = cParser()
        
        possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        fin_url = ''.join(random.choice(possible) for _ in range(10))
        
        sPattern = 'return a\+"(\?token=[^"]+)"'
        d = oParser.parse(sHtmlContent, sPattern)[1][0]
        
        fin_url = fin_url + d + str(int(1000*time.time()))
        
        sPattern = "\$\.get\('(\/pass_md5[^']+)"
        aResult = oParser.parse(sHtmlContent, sPattern)
        url2 = 'https://' + urlDonwload.split('/')[2] + aResult[1][0]
        
        #VSlog(url2)
        
        oRequest = cRequestHandler(url2)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', urlDonwload)
        sHtmlContent = oRequest.request()
        
        #VSlog(sHtmlContent)
        
        #api_call = compute(sHtmlContent) + fin_url
        api_call = sHtmlContent + fin_url
        
        #VSlog(api_call)

        if (api_call):
            api_call = api_call + '|Referer=' + urlDonwload
            return True, api_call

        return False, False
