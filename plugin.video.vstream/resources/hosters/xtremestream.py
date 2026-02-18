# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'xtremestream', 'XtremeStream')

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        oRequest.addHeaderEntry('Referer', str(self._url))
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
        
        # Récupérer les paramètres
        sPattern = "var m3u8_loader_url = `([^`]+)`"
        aResult1 = oParser.parse(sHtmlContent, sPattern)
        sPattern = "var video_id = `([^`]+)`"
        aResult2 = oParser.parse(sHtmlContent, sPattern)
        
        # Construire l'URL de base et récupérer le M3U8
        base_url = aResult1[1][0] + aResult2[1][0]
        oRequest2 = cRequestHandler(base_url)
        oRequest2.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        oRequest2.addHeaderEntry('Referer', str(self._url))
        sM3u8 = oRequest2.request()
        
        # Extraire le paramètre q
        sPattern = '&q=(\d+)'
        aResult3 = oParser.parse(sM3u8, sPattern)
        
        api_call = base_url + '&q=' + aResult3[1][0]
        api_call += '|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        api_call += '&Referer=' + str(self._url)

        return True, api_call
