#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

from resources.lib.aadecode import AADecoder
import re

#from resources.lib.comaddon import VSlog

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'MyStream'
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
        return 'mystream'

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

        # sPattern =  '(?:https*:\/\/|\/\/)(?:www.|embed.|)mystream.(?:la|com|to)\/(?:video\/|external\/|embed-|)([0-9a-zA-Z]+)'
        # oParser = cParser()
        # aResult = oParser.parse(sUrl, sPattern)
        # self.__sUrl = 'https://mysembed.net/' + str(aResult[1][0])

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        #VSlog(self.__sUrl)

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        #VSlog(sHtmlContent)
        oParser = cParser()
        
        api_call = False
        
        sPattern =  '(?:[>;]\s*)(ﾟωﾟ.+?\(\'_\'\);)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for i in aResult[1]:
                decoded = AADecoder(i).decode()
                r = re.search("\('src', '([^']+)'\);", decoded, re.DOTALL | re.UNICODE)
                if r:
                    api_call = r.group(1)
                    break
        
        #VSlog(api_call)

        if (api_call):
            return True, api_call

        return False, False
