# -*- coding: utf-8 -*-
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib import util

UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, "ansembed", "AnsEmbed")

    def _getMediaLinkForGuest(self):
        oParser = cParser()

        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', self._url)
        sHtmlContent = oRequest.request()

        sPattern = "sources: *\\[ *\\{ *file: *'([^']+)'"
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            api_call = aResult[1][0]
            api_call = api_call + '|Referer=' + util.urlHostName(self._url)
            return True, api_call

        return False, False
