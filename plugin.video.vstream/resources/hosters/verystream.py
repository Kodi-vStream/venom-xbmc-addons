#coding: utf-8
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'verystream', 'VeryStream')

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        api_call = ''

        sPattern =  'id="videolink">([^<>]+)<\/p>'
        aResult = re.findall(sPattern, sHtmlContent)

        if (aResult):

            api_call = 'https://verystream.com/gettoken/' + aResult[0] + '?mime=true'

        if api_call:
            return True, api_call

        return False, False
