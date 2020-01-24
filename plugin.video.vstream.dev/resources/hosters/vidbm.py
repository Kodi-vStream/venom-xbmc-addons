#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://www.vidbm.com/emb.html?xxx=img.vidbm.com/xxx
#https://www.vidbm.com/embed-xxx.html?auto=1
#https://www.vidbm.com/embed-xxx.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
#from resources.lib.comaddon import VSlog
import re
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'VidBM'
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
        return 'vidbm'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return False

    def setUrl(self, sUrl):
        self.__sUrl = re.sub('=img.vidbm.com/.+?','',str(sUrl))
        self.__sUrl = self.__sUrl.replace('https://www.vidbm.com/', '')
        self.__sUrl = self.__sUrl.replace('embed-', '')
        self.__sUrl = self.__sUrl.replace('emb.html?', '')
        self.__sUrl = self.__sUrl.replace('.html?auto=1','')
        self.__sUrl = self.__sUrl.replace('.html','')
  
    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        sUrl = 'https://www.vidbm.com/embed-' + self.__sUrl + '.html?auto=1'

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        oParser = cParser()

        sPattern = "as.src *= *'([^']+)';"
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            oRequest = cRequestHandler('https://www.vidbm.com' + aResult[1][0])
            oRequest.addHeaderEntry('Referer', sUrl)
            sHtmlContent = oRequest.request()

            sPattern = "document.cookie *= *'([^']+)';"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                cookie = aResult[1][0]

                oRequest = cRequestHandler(sUrl)
                oRequest.addHeaderEntry('Cookie', cookie)
                sHtmlContent = oRequest.request()

                sPattern = 'sources: *\[{file:"([^"]+)"'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    api_call = aResult[1][0] + '|User-Agent=' + UA #+ '&Referer=' + self.__sUrl

        if (api_call):
            return True, api_call

        return False, False
