# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import sys
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
import re

# l'importation de cloudscraper
try:
    import cloudscraper
    _HAS_CLOUDSCRAPER = True
    _IMPORT_MSG = "OK : Module cloudscraper charge avec succes."
except Exception as e:
    _HAS_CLOUDSCRAPER = False
    _IMPORT_MSG = "ECHEC : " + str(e)

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'savefiles', 'SaveFiles')

    def _getMediaLinkForGuest(self):

        match = re.search(r'/(?:e|v)/([0-9a-zA-Z]+)', self._url)
        if not match:
            return False, False

        media_id = match.group(1)
        ref = self._url.split('/e/')[0] + '/' if '/e/' in self._url else self._url.split('/v/')[0] + '/'
        dl_url = ref + 'dl'

        post_data = {
            'op': 'embed',
            'file_code': media_id,
            'auto': '0',
            'referer': ''
        }

        player_html = ""

        if _HAS_CLOUDSCRAPER:
            try:
                scraper = cloudscraper.create_scraper(
                    browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False},
                    delay=4
                )

                response = scraper.post(dl_url, data=post_data, headers={"User-Agent": UA, "Referer": ref, "Origin": ref[:-1]}, timeout=15)
                player_html = response.text

            except Exception as e_cloud:
                player_html = ""
        else:
            try:
                oRequestHandler = cRequestHandler(dl_url)
                oRequestHandler.setRequestType(1)
                for key, value in post_data.items():
                    oRequestHandler.addParameters(key, value)

                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', ref)
                player_html = oRequestHandler.request()
            except Exception as e_native:
                pass

        api_call = False
        sPattern = r'''sources:\s*\[(?:{\s*file\s*:)?\s*['"]([^'"]+)'''
        oParser = cParser()

        aResult = oParser.parse(player_html, sPattern)

        if aResult[0] is True:
            api_call = aResult[1][0] + '|User-Agent=' + UA + '&Referer=' + ref

        else:
            pass

        if api_call:
            return True, api_call

        return False, False
