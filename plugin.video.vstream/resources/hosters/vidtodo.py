#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#http://vidtodo.com/embed-xxx.html
#http://vidtodo.com/xxx
#http://vidtodo.com/xxx.html
#com,me
import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
#from resources.lib.comaddon import VSlog

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:69.0) Gecko/20100101 Firefox/69.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidtodo', 'VidToDo')

    def setUrl(self, url):
        self._url = str(url)
        if 'embed-' in self._url:
            self._url = self._url.replace('embed-','')
#        if not 'embed-' in self._url:
#            self._url = self._url.rsplit('/', 1)[0] + '/embed-' + self._url.rsplit('/', 1)[1]

        if not self._url.startswith('https'):
            self._url = self._url.replace('http', 'https')

        if not self._url.endswith('.html'):
            self._url = self._url + '.html'

    def extractSmil(self,smil):
        oRequest = cRequestHandler(smil)
        oRequest.addParameters('referer', self._url)
        sHtmlContent = oRequest.request()
        Base = re.search('<meta base="(.+?)"', sHtmlContent)
        Src = re.search('<video src="(.+?)"', sHtmlContent)
        return Base.group(1) + Src.group(1)

    def _getMediaLinkForGuest(self):
        api_call = ''

        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('Referer', self._url)
        oRequest.addParameters('User-Agent', UA)
        sHtmlContent = oRequest.request()

        sPattern = 'sources:* \[(?:{file:)*"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]

        else:
            sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                sHtmlContent = cPacker().unpack(aResult[1][0])

                sPattern = '{file: *"([^"]+smil)"}'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0] is True:
                    api_call = self.extractSmil(aResult[1][0])
                else:
                    sPattern = 'src:"([^"]+.mp4)"'
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    if aResult[0] is True:
                        api_call = aResult[1][0] #.decode('rot13')

        if api_call:
            return True, api_call

        return False, False
