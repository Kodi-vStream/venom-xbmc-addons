#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://playtube.ws/embed-xxxxx.html
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.packer import cPacker

UA = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'playtube', 'Playtube')

    def _getMediaLinkForGuest(self):
        oRequestHandler = cRequestHandler(self._url)
        sHtmlContent = oRequestHandler.request()

        sPattern2 = '(\s*eval\s*\(\s*function(?:.|\s)+?\)\)\))'
        aResult = re.findall(sPattern2, sHtmlContent)
        list_url = []
        list_qua = []
        if aResult:
            str2 = aResult[0]
            if not str2.endswith(';'):
                str2 = str2 + ';'

            strs = cPacker().unpack(str2)
            oParser = cParser()
            sPattern = '(https.+?.m3u8)'
            aResult = re.findall(sPattern, strs)
            if aResult:
                urlhost = aResult[0]
                oRequestHandler = cRequestHandler(urlhost)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', self._url)
                sHtmlContent2 = oRequestHandler.request()
                oParser = cParser()
                sPattern = 'PROGRAM.*?BANDWIDTH.*?RESOLUTION=(\d+x\d+).*?(https.*?m3u8)'
                aResult = oParser.parse(sHtmlContent2, sPattern)
                if aResult[0] is True:
                    for aEntry in aResult[1]:
                        list_url.append(aEntry[1])
                        list_qua.append(aEntry[0])

                    api_call = dialog().VSselectqual(list_qua, list_url)

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url

        return False, False
