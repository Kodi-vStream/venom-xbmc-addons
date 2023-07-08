# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#

try:  # Python 2
    import urllib2
except ImportError:  # Python 3
    import urllib.request as urllib2

import json
import requests

from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.util import cUtil


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'ok_ru', 'Ok.ru')

    def getHostAndIdFromUrl(self, sUrl):
        sPattern = 'https*:\/\/.*?((?:(?:ok)|(?:odnoklassniki))\.ru)\/.+?\/([0-9]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if aResult[0] is True:
            return aResult[1][0]
        return ''

    def _getMediaLinkForGuest(self, autoPlay = False):
        v = self.getHostAndIdFromUrl(self._url)
        sId = v[1]
        sHost = v[0]
        web_url = 'http://' + sHost + '/videoembed/' + sId

        HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

        St=requests.Session()
        sHtmlContent = St.get(web_url).content.decode('utf-8')
        oParser = cParser()

        sHtmlContent = oParser.abParse(sHtmlContent, 'data-options=', '" data-player-container', 14)
        sHtmlContent = cUtil().removeHtmlTags(sHtmlContent)
        sHtmlContent = cUtil().unescape(sHtmlContent)

        page = json.loads(sHtmlContent)
        page = json.loads(page['flashvars']['metadata'])
        if page:
            url = []
            qua = []
            for x in page['videos']:
                url.append(x['url'])
                qua.append(x['name'])

            # Si au moins 1 url
            if url:
                # dialogue qualité
                api_call = dialog().VSselectqual(qua, url)

        if api_call:
            api_call = api_call + '|Referer=' + self._url
            return True, api_call

        return False, False
