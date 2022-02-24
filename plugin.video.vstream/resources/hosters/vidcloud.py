#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#Vidcloud / vcstream.to
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidcloud', 'VidCloud')

    def __getIdFromUrl(self, sUrl):
        #https://vcstream.to/embed/5bcf5b4c39aff/The.Spy.Who.Dumped.Me.mp4
        sPattern = 'vcstream.to/embed/([^<]+)/'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0]):
            return aResult[1][0]
        return ''

    def _getMediaLinkForGuest(self):
        api_call = False

        sId = self.__getIdFromUrl(self._url)
        url = 'https://vcstream.to/player?fid=%s&page=embed' % sId

        sPattern = 'file.+?\\"([^<]+)\\"\}'
        oRequest = cRequestHandler(url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0]):
            api_call = aResult[1][0].replace('\\\\', '').replace(':\\"', '')

        if api_call:
            return True, api_call

        return False, False
