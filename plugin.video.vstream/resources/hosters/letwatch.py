#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.hosters.hoster import iHoster
import re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'LetWatch'
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
        return 'letwatch'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self, sUrl):
        sPattern = "http://exashare.com/([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):

        return self.__getMediaLinkForGuest()

    def __getUrlFromJavascriptCode(self, sHtmlContent):

        # oParser = cParser()
        # sPattern = "(eval\(function.*?)(.+?)</script>"
        #aResult = oParser.parse(sHtmlContent, sPattern)

        aResult = re.search('(eval\(function.*?)\s*</script>', sHtmlContent, re.DOTALL)

        if (aResult.group(1)):
            sJavascript = aResult.group(1)

            #sUnpacked = cJsUnpacker().unpackByString(sJavascript)
            sUnpacked = cPacker().unpack(sJavascript)

            return sUnpacked

        return False

    def __getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        sUnpacked = self.__getUrlFromJavascriptCode(sHtmlContent)

        # jwplayer("vplayer").setup({sources:[{file:"http://94.242.57.154/l7z7fz25dmnhgn4vfkbbeauaqogvhaabb62mkm4zvaxq3iodhdvlahybe6sa/v.flv",label:"SD"}],image:"http://94.242.57.154/i/03/00249/d8g74g00wtuv.jpg",skin:"",duration:"5314",width:680,height:390,primary:"flash",startparam:"start",plugins:{"http://letwatch.us/player6/lightsout.js

        sPattern = 'sources:\[{file:"(.+?)"'

        oParser = cParser()
        aResult = oParser.parse(sUnpacked, sPattern)


        if (aResult[0] == True):
            api_call = aResult[1][0]
            return True, api_call

        return False, False

