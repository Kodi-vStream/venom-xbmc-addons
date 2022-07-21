# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.util import urlEncode, Quote


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'lien_direct', 'Lien direct')

    def setUrl(self, url):
        self._url = str(url).replace('+', '%20')  # un lien direct n'est pas forcement urlEncoded

    def _getMediaLinkForGuest(self):
        api_call = self._url

        if ('hds.' in api_call) or ('bidzen' in api_call):
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'
            api_call = api_call + '|User-Agent=' + UA + '&referer=' + self._url

        # full moviz lien direct final nowvideo
        if 'zerocdn.to' in api_call:
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
            api_call = api_call + '|User-Agent=' + UA

        # Special pour mangacity
        if 'pixsil' in api_call:
            api_call = api_call.split('|')[0] + '|Referer=http://www.mangacity.org/jwplayer/player.swf'

        # Modif pr aliez
        if 'aplayer1.me' in api_call:
            UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
            api_call = api_call + '|User-Agent=' + UA

        if 'sport7' in api_call:
            UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
            api_call = api_call + '|User-Agent=' + UA + '&referer=' + self._url

        # Special pour toonanime.
        if 'toonanime' in api_call:
            oRequest = cRequestHandler(api_call)
            oRequest.addHeaderEntry('Referer', 'https://lb.toonanime.xyz/')
            sHtmlContent = oRequest.request()

            aResult = re.findall(',RESOLUTION=(.+?)\n(.+?).m3u8', sHtmlContent)
            # initialisation des tableaux
            url = []
            qua = []
            # Remplissage des tableaux
            for i in aResult:
                url.append(str(i[1]) + '.m3u8')
                qua.append(str(i[0]))

            headers = {
                       "User-Agent": Quote("Mozilla/5.0 (Linux; Android 6.0.1; SM-G930V Build/MMB29M) " +
                                           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36"),
                       "Referer": "https://lb.toonanime.xyz/"
                       }

            # Affichage du tableau
            api_call = "http://127.0.0.1:2424?u=https://lb.toonanime.xyz" + dialog().VSselectqual(qua, url) + \
                       "@" + urlEncode(headers)

        if api_call:
            return True, api_call

        return False, False
