#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import VSlog

import xbmc

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filemoon', 'FileMoon')

    def _getMediaLinkForGuest(self):
        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        #oRequest.addHeaderEntry('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
        #oRequest.addHeaderEntry('Accept-Language', "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3")
        sHtmlContent = oRequest.request()

        #lien indirect
        sPattern = '<iframe.+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if aResult[0]:
            url2 = aResult[1][0]
            oRequest = cRequestHandler(url2)
            oRequest.addHeaderEntry('Referer', self._url)
            oRequest.addHeaderEntry('User-Agent', UA)
            #oRequest.addHeaderEntry('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
            #oRequest.addHeaderEntry('Accept-Language', "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3")
            #oRequest.addHeaderEntry('Accept-Encoding', "gzip, deflate, br, zstd")
            oRequest.addHeaderEntry('Sec-Fetch-Dest', "iframe")
            #oRequest.addHeaderEntry("Cookie", "file_id=xxxx; aff=44000; ref_url=xxx.com; _ym_uid=xxxxxx; _ym_d=xxxxx; _ym_isad=1")
            sHtmlContent = oRequest.request()
            
            #ici je sais pas pourquoi mais cela ne marche que si je fais 2 requetes avec un delais
            xbmc.sleep(1000)
            oRequest = cRequestHandler(self._url)
            oRequest.addHeaderEntry('User-Agent', UA)
            sHtmlContent2 = oRequest.request()
            
            oRequest.addHeaderEntry('Referer', self._url)
            oRequest.addHeaderEntry('User-Agent', UA)
            #oRequest.addHeaderEntry('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
            #oRequest.addHeaderEntry('Accept-Language', "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3")
            #oRequest.addHeaderEntry('Accept-Encoding', "gzip, deflate, br, zstd")
            oRequest.addHeaderEntry('Sec-Fetch-Dest', "iframe")
            #oRequest.addHeaderEntry("Cookie", "file_id=xxxx; aff=44000; ref_url=xxx.com; _ym_uid=xxxxxx; _ym_d=xxxxx; _ym_isad=1")
            sHtmlContent2 = oRequest.request()

            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0]:
                sHtmlContent = cPacker().unpack(aResult[1][0])
                #VSlog(sHtmlContent)
                sPattern = '{file:"([^"]+)"}]'
                aResult = oParser.parse(sHtmlContent, sPattern)

                if aResult[0]:
                    return True, aResult[1][0] # + '|User-Agent=' + UA

        # 2eme méthode
        else:
            url2 = self._url.replace('/e/', '/api/videos/') + '/embed/details'
            oRequest = cRequestHandler(url2)
            sHtmlContent2 = oRequest.request()
            sPattern = '"embed_frame_url":"([^"]+)"'
            aResult = oParser.parse(sHtmlContent2, sPattern)
            if aResult[0]:
                return True, aResult[1][0] # + '|User-Agent=' + UA
  

        return False, False
