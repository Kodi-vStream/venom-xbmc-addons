# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# http://cloudvid.co/embed-xxxx.html
# https://clipwatching.com/embed-xxx.html

import json
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.parser import cParser


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'darkibox', 'DarkiBox')

    def isDownloadable(self):
        return False

    def setUrl(self, url):
        self._url = str(url)


    # avec un compte
    def getMediaLink(self):
        oPremiumHandler = cPremiumHandler('darkibox')
        sToken = oPremiumHandler.getToken()
        
        if not sToken:
            return self._getMediaLinkForGuest()
        
        file_code = self._url.split('/')[-1].split('.')[0]
        apiUrl = 'https://darkibox.com/api/file/direct_link?key=%s&file_code=%s' % (sToken, file_code)

#liens streaming hls ne se lancent pas
#apiUrl = 'https://darkibox.com/api/file/direct_link?key=%s&file_code=%s&hls=1' % (sToken, file_code)

        oRequestHandler = cRequestHandler(apiUrl)
        sHtmlContent = oRequestHandler.request()
        content = json.loads(sHtmlContent)
        if content['status'] != 200:
            return self._getMediaLinkForGuest()
        
        content = content['result']
        if not content:
            return self._getMediaLinkForGuest()
        
        # plusieurs qualités
        links = content['versions']
        qua=[]
        url=[]

        for link in links:
            if link['name'] == 'o':
                qua.append('Original [%.1f Go]' % (float(link['size'])/1073741824))
                url.append(link['url'])
            elif link['name'] == 'x':
                qua.append('Autre [%.1f Go]' % (float(link['size'])/1073741824))
                url.append(link['url'])
        
        # if 'hls_direct' in content:
        #     qua.append('Streaming')
        #     url.append(content['hls_direct'])


        if len(url)>1:
            #Afichage du tableau
            api_call = dialog().VSselectqual(qua, url)
        else:
            api_call = url[0]
        return True, api_call


    def _getMediaLinkForGuest(self, api_call=None):

        file_code = self._url.split('/')[-1].split('.')[0]

        postdata = 'op=embed&auto=1&file_code=%s' % file_code

        oRequest = cRequestHandler("https://darkibox.com/dl")
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', self._url)
        oRequest.addParametersLine(postdata)

        sHtmlContent = oRequest.request()
        oParser = cParser()
        sPattern = 'sources: *\[{src: "([^"]+)"'#, *type: "video/mp4"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            return True, aResult[1][0]

        return False, False
