# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import time
import requests

from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog, VSlog
from resources.lib.handler.requestHandler import cRequestHandler

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'megaup', 'Megaup')

    def _getMediaLinkForGuest(self):
        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()
        cookies = oRequestHandler.GetCookies() + ";"

        data = re.search('Mhoa_URL\((.+?)\);',sHtmlContent).group(1)
        data = re.findall("'(.+?)'",data)

        part1 = data[0]
        part2 = data[1]
        file = data[2]
        size = data[3]

        cidken = ''
        d1p1 = part1[0:len(part1)//4]
        cidken += d1p1[::-1]
        d1p2 = part1[len(part1)//4*2:len(part1)//4*3]
        cidken += d1p2[::-1]
        d2p1 = part2[3:(len(part2)+3)//2]
        cidken += d2p1[::-1]

        time.sleep(6)

        oRequestHandler = cRequestHandler("https://download.megaup.net/?idurl=" + cidken + "&idfilename=" + file + \
            "&idfilesize=" + size)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()

        la = re.search('window\.location\.replace\("(.+?)"',sHtmlContent).group(1)

        oRequestHandler = cRequestHandler(la)
        oRequestHandler.disableRedirect()
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry("Referer", "https://download.megaup.net/")
        oRequestHandler.addHeaderEntry("Cookie", cookies)
        sHtmlContent = oRequestHandler.request()
        api_call = oRequestHandler.getResponseHeader()['Location']

        if api_call:
            return True,  api_call + "|User-Agent="+UA

        return False, False
