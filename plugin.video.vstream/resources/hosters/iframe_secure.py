# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.packer import cPacker
from resources.hosters.hoster import iHoster
from resources.lib.gui.hoster import cHosterGui


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'iframe_secure', 'Iframe-Secure')

    def setUrl(self, url):
        url = url.replace('http://www.iframe-secure.com/embed/', '')
        url = url.replace('//iframe-secure.com/embed/', '')
        url = 'http://www.iframe-secure.com/embed/iframe.php?u=%s' % url
        super(cHoster, self).setUrl(url)


    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        aResult = re.findall(sPattern, sHtmlContent)

        if aResult:
            sUnpacked = cPacker().unpack(aResult[0])
            sHtmlContent = sUnpacked

            if sHtmlContent:

                oParser = cParser()
                sPattern = "replace\(.*'(.+?)'"
                aResult = oParser.parse(sHtmlContent, sPattern)

                if aResult[0] is True:
                    sHosterUrl = aResult[1][0]

                    if not sHosterUrl.startswith('http'):
                        sHosterUrl = 'http:%s' % sHosterUrl

                    sHosterUrl = sHosterUrl.replace('\\', '')
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    oHoster.setUrl(sHosterUrl)
                    api_call = oHoster.getMediaLink()

                    if api_call[0] is True:
                        return True, api_call[1]

        return False, False
