#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import base64

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.hunter import hunter
from resources.lib.comaddon import VSlog, isMatrix

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'upvideo', 'UpVideo')

    def _getMediaLinkForGuest(self):
        api_call = False
        oParser = cParser()
        sPattern = 'return decodeURIComponent\(escape\(r\)\)}\("([^,]+)",([^,]+),"([^,]+)",([^,]+),([^,]+),([^,\))]+)\)'

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Cookie', 'popads2=opened')
        sHtmlContent = oRequest.request()

        aResult = oParser.parse(sHtmlContent, sPattern)

        #Get decode page
        #oRequest = cRequestHandler("https://upvideo.to/assets/js/tabber.js")
        #oRequest.addHeaderEntry('Referer', self._url)
        #sHtmlContent2 = oRequest.request()
        #aResult2 = oParser.parse(sHtmlContent2, sPattern)

        #if (aResult2[0] == True):
        #    j = aResult2[1][0]
        #    decoder = hunter(j[0],int(j[1]),j[2],int(j[3]),int(j[4]),int(j[5]))
        #    VSlog("Decoder ok")

        if aResult[0] is True:
            l = aResult[1]
            for j in l:
                data = hunter(j[0],int(j[1]),j[2],int(j[3]),int(j[4]),int(j[5]))
                if "fcbbbdddebad" in data:
                    r = re.search('var fcbbbdddebad *= *"([^"]+)" *;', data)
                    if not r:
                        VSlog('er2')
                    v2 = r.group(1).split('aHR0')[1].split('YTk0NT')[0]

                    if isMatrix():
                        api_call = "htt" + (base64.b64decode(v2).decode())
                    else:
                        api_call = "htt" + base64.b64decode(v2)

        if api_call:
            return True, api_call

        return False, False
