# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# french-stream /18117-la-frontire-verte-saison-1.html
# liens FVS io
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'frenchvid', 'Frenchvid')

    def setUrl(self, url):
        self._url = str(url)

    def _getMediaLinkForGuest(self):
        # Get Redirection
        if 'fembed' in self._url:
            oRequest = cRequestHandler(self._url)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.request()
            self._url = oRequest.getRealUrl()

        if 'french-vid' in self._url:
            baseUrl = 'https://www.fembed.com/api/source/'
        elif 'fembed' in self._url or "femax20" in self._url:
            baseUrl = 'https://www.diasfem.com/api/source/'
        elif 'fem.tohds' in self._url:
            baseUrl = 'https://feurl.com/api/source/'
        else:
            baseUrl = 'https://' + self._url.split('/')[2] + '/api/source/'

        if 'fem.tohds' in self._url:
            oRequestHandler = cRequestHandler(self._url)
            sHtmlContent = oRequestHandler.request()

            sPattern = '<iframe src="([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)

            url = baseUrl + aResult[1][0].rsplit('/', 1)[1]
            postdata = 'r=""' + '&d=' + self._url.split('/')[2]
        else:
            url = baseUrl + self._url.rsplit('/', 1)[1]
            postdata = "r=''" + "&d=" + self._url.split('/')[2]

        oRequest = cRequestHandler(url)
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', self._url)
        oRequest.addParametersLine(postdata)
        page = oRequest.request(jsonDecode=True)
        if page:
            url = []
            qua = []
            for x in page['data']:
                url.append(x['file'])
                qua.append(x['label'])
    
            api_call = dialog().VSselectqual(qua, url)
    
            oRequest = cRequestHandler(api_call)
            oRequest.addHeaderEntry('Host', 'fvs.io')
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.request()
            api_call = oRequest.getRealUrl()
    
            if api_call:
                return True, api_call + '|User-Agent=' + UA


        oRequestHandler = cRequestHandler(self._url)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'var video_source = "([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult:
            return True, aResult[1][0] + '|User-Agent=' + UA

        return False, False
