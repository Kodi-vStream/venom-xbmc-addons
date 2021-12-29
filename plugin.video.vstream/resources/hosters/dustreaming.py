#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
import json

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'dustreaming', 'Dustreaming')

    def _getMediaLinkForGuest(self):
        api_call = ''

        url = self._url.replace('/v/', '/api/source/')
        oRequest = cRequestHandler(url)
        oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequest.addHeaderEntry('Referer', self._url)
        oRequest.addParameters('r', '')
        oRequest.addParameters('d', 'dustreaming.fr')
        sHtmlContent = oRequest.request()

        page = json.loads(sHtmlContent)
        if page:
            url = []
            qua = []
            for x in page['data']:
                url.append(x['file'])
                qua.append(x['label'])

            if (url):
                api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
