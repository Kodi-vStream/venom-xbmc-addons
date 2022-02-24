#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#stream elite
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.gui.hoster import cHosterGui

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'iframe_secured', 'Iframe-Secured')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        #http://iframe-secured.com/embed/evovinec
        #http://iframe-secured.com/embed/iframe.php?u=evovinec
        self._url = url.replace('http://iframe-secured.com/embed/', '')
        self._url = self._url.replace('//iframe-secured.com/embed/', '')
        self._url = 'http://iframe-secured.com/embed/iframe.php?u=%s' % self._url

    def _getMediaLinkForGuest(self):
        api_call = ''

        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', self._url.replace('iframe.php?u=', ''))
        sHtmlContent = oRequest.request()

        sPattern = '<input  id=".+?name="([^"]+)" type="hidden" value="([^"]+)"/><input  id="challenge" ' + \
            'name="([^"]+)" type="hidden" value="([^"]+)"/>'

        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            postdata = aResult[1][0][0] + '=' + aResult[1][0][1] + '&' + aResult[1][0][2] + '=' + aResult[1][0][3]

            oRequest = cRequestHandler(self._url)
            oRequest.setRequestType(1)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Referer', self._url)
            oRequest.addParametersLine(postdata)

            sHtmlContent = oRequest.request()

            sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
            aResult = re.findall(sPattern, sHtmlContent)

            if (aResult):
                sUnpacked = cPacker().unpack(aResult[0])
                sHtmlContent = sUnpacked
                if (sHtmlContent):
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
