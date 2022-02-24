#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vid_ag', 'Vid.ag')

    def getUrl(self, url):
        r = re.search('\/\/((?:www\.)?vid\.ag)\/(?:embed-)?([0-9A-Za-z]+)', url)
        if r:
            return 'http://%s/embed-%s.html' % (r.groups()[0], r.groups()[1])
        else:
            return False

    def _getMediaLinkForGuest(self):
        web_url = self.getUrl(self._url)

        oRequest = cRequestHandler(web_url)
        sHtmlContent = oRequest.request()

        oParser = cParser()

        #Dean Edwards Packer
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            sUnpacked = cPacker().unpack(aResult[1][0])
            sHtmlContent = sUnpacked

        sPattern = 'file\s*:\s*"([^"]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]
            return True, api_call
        else:
            return False, False

        return False, False
