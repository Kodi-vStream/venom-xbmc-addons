#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'azerfile', 'Azerfile')

    def setUrl(self, url):
        self._url = str(url)

        sPattern =  'http://(?:www.|embed.|)azerfile.(?:com)/(?:video/|embed\-|)?([0-9a-z]+)'

        oParser = cParser()
        aResult = oParser.parse(self._url, sPattern)
        self._url = 'http://azerfile.com/'+str(aResult[1][0])

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = 'file=([^<]+)&image';

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)


        if aResult[0] is True:
            file = aResult[1][0]

            liste = file.split('/')

            #api_call = ('http://azerfile.com:%s/d/%s/video.mp4') % (liste[-1], liste[-2])
            api_call = aResult[1][0]
            return True, api_call

        return False, False
