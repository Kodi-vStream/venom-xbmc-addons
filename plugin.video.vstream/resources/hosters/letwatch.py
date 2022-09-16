# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'letwatch', 'LetWatch')

    def __getUrlFromJavascriptCode(self, sHtmlContent):
        # oParser = cParser()
        # sPattern = "(eval\(function.*?)(.+?)</script>"
        # aResult = oParser.parse(sHtmlContent, sPattern)

        aResult = re.search('(eval\(function.*?)\s*</script>', sHtmlContent, re.DOTALL)

        if aResult.group(1):
            sJavascript = aResult.group(1)

            # sUnpacked = cJsUnpacker().unpackByString(sJavascript)
            sUnpacked = cPacker().unpack(sJavascript)

            return sUnpacked

        return False

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sUnpacked = self.__getUrlFromJavascriptCode(sHtmlContent)

        # jwplayer("vplayer").setup({sources:[
        # {file:"http://94.242.57.154/l7z7fz25dmnhgn4vfkbbeauaqogvhaabb62mkm4zvaxq3iodhdvlahybe6sa/v.flv",label:"SD"}],
        # image:"http://94.242.57.154/i/03/00249/d8g74g00wtuv.jpg",skin:"",duration:"5314",width:680,height:390,
        # primary:"flash",startparam:"start",plugins:{"http://letwatch.us/player6/lightsout.js

        sPattern = 'sources:\[{file:"(.+?)"'

        oParser = cParser()
        aResult = oParser.parse(sUnpacked, sPattern)

        if aResult[0] is True:
            api_call = aResult[1][0]
            return True, api_call

        return False, False
