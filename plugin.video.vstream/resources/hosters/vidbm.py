# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://www.vidbm.com/emb.html?xxx=img.vidbm.com/xxx
# https://www.vidbm.com/embed-xxx.html?auto=1
# https://www.vidbm.com/embed-xxx.html

import re

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:72.0) Gecko/20100101 Firefox/72.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidbm', 'VidBM')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        url = re.sub('=img.vidbm.com/.+?', '', str(url))
        url = url.replace('https://www.vidbm.com/', '')
        url = url.replace('embed-', '')
        url = url.replace('emb.html?', '')
        url = url.replace('.html?auto=1', '')
        url = url.replace('.html', '')
        super(cHoster, self).setUrl(url)


    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern = 'sources: *\[{file:"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        api_call = aResult[1][0] + '|User-Agent=' + UA

        if api_call:
            return True, api_call

        return False, False
