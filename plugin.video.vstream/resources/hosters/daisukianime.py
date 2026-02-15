# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'daisukianime', 'DaisukiAnime')

    def _getMediaLinkForGuest(self):
        api_call = self._url
        
        # Extraire l'ID de l'URL
        aResult = re.search(r'id=(\d+)', api_call)
        if aResult:
            video_id = aResult.group(1)
            api_url = 'https://cdn2.daisukianime.xyz/sib/%s?epid=null' % video_id
            
            oRequest = cRequestHandler(api_url)
            oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            oRequest.addHeaderEntry('Accept', '*/*')
            oRequest.addHeaderEntry('Origin', 'https://lb.daisukianime.xyz')
            oRequest.addHeaderEntry('Referer', 'https://lb.daisukianime.xyz/')
            sHtmlContent = oRequest.request()
            
            # Chercher l'URL mp4 ou m3u8 dans la réponse
            aResult2 = re.findall(r'(https?://[^\s"\'<>]+\.(?:mp4|m3u8)[^\s"\'<>]*)', sHtmlContent)
            if aResult2:
                api_call = aResult2[0]
                return True, api_call

        return False, False
