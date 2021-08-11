#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# https://www.pstream.net/e/xxxxx
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSPath, isMatrix, VSlog
from resources.lib.parser import cParser
from resources.lib.util import urlEncode
import base64
import json
import re

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"

headers = {'User-Agent': UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3"}

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Pstream'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'pstream'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self):
        return ''

    def __modifyUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call = ''
        url = self.__sUrl

        oRequest = cRequestHandler(url)  
        oRequest.addHeaderEntry('User-Agent', UA)    
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern =  '<script type="text/javascript" src="(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)[1][1]

        oRequest = cRequestHandler(aResult)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        sHtmlContent = oRequest.request()

        sPattern =  '(?:parseJSON|atob).+?ey(.+?)"'
        code = oParser.parse(sHtmlContent, sPattern)

        for i in code[1]:
            try:
                if isMatrix():
                    code = base64.b64decode("ey" + i).decode('ascii')
                else:
                    code = base64.b64decode("ey" + i)
                break
            except:
                pass

        api_call = json.loads(code)['url']

        if (api_call):
            return True, api_call + '|' + urlEncode(headers)

        return False, False
