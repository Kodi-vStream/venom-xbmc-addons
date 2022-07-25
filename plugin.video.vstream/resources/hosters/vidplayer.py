# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# https://vidplayer.cz/v/xxxxxxx
import json

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'vidplayer', 'Vidplayer')

    def _getMediaLinkForGuest(self):
        req = self._url.replace('/v/', '/api/source/')
        pdata = 'r'
        oRequestHandler = cRequestHandler(req)
        oRequestHandler.setRequestType(1)

        oRequestHandler.addParametersLine(pdata)
        sHtmlContent = oRequestHandler.request()
        jsonrsp = json.loads(sHtmlContent)

        list_url = []
        list_q = []

        for idata in range(len(jsonrsp['data'])):
            url = jsonrsp['data'][idata]['file']
            stype = jsonrsp['data'][idata]['type']
            q = jsonrsp['data'][idata]['label']
            list_url.append(url + '.' + stype)
            list_q.append(q)

        if list_url:
            api_call = dialog().VSselectqual(list_q, list_url)

        if api_call:
            return True, api_call

        return False, False
