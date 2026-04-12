# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# https://darkibox.com/embed-xxxx.html
# https://darkibox.com/e/xxxx

import json
import re
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.parser import cParser
from resources.lib.packer import cPacker

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0'


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'darkibox', 'DarkiBox')

    def isDownloadable(self):
        return False

    # avec un compte
    def getMediaLink(self):
        oPremiumHandler = cPremiumHandler('darkibox')
        sToken = oPremiumHandler.getToken()

        if not sToken:
            return self._getMediaLinkForGuest()

        file_code = self._url.split('/')[-1].split('.')[0]
        file_code = file_code.replace('embed-', '')
        apiUrl = 'https://darkibox.com/api/file/direct_link?key=%s&file_code=%s' % (sToken, file_code)

        oRequestHandler = cRequestHandler(apiUrl)
        sHtmlContent = oRequestHandler.request()
        content = json.loads(sHtmlContent)
        if content['status'] != 200:
            return self._getMediaLinkForGuest()

        content = content['result']
        if not content:
            return self._getMediaLinkForGuest()

        # plusieurs qualites
        links = content['versions']
        qua = []
        url = []

        for link in links:
            if link['name'] == 'o':
                qua.append('Original [%.1f Go]' % (float(link['size']) / 1073741824))
                url.append(link['url'])
            elif link['name'] == 'x':
                qua.append('Autre [%.1f Go]' % (float(link['size']) / 1073741824))
                url.append(link['url'])

        if len(url) > 1:
            api_call = dialog().VSselectqual(qua, url)
        elif len(url) == 1:
            api_call = url[0]
        else:
            return self._getMediaLinkForGuest()

        return True, api_call

    def _getMediaLinkForGuest(self):

        file_code = self._url.split('/')[-1].split('.')[0]
        file_code = file_code.replace('embed-', '')

        postdata = 'op=embed&auto=1&file_code=%s' % file_code

        oRequest = cRequestHandler('https://darkibox.com/dl')
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', self._url)
        oRequest.addParametersLine(postdata)

        sHtmlContent = oRequest.request()
        oParser = cParser()

        # Le /dl retourne du JavaScript packe (eval(function(p,a,c,k,e,...)))
        # contenant le player PlayerJS avec le parametre file:
        sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            sHtmlContent = cPacker().unpack(aResult[1][0])

        # Format multi-qualite PlayerJS: [label1]url1,[label2]url2
        # ou URL simple (HLS m3u8 ou MP4 direct)
        sPattern = 'file\s*:\s*"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            sFileContent = aResult[1][0]

            # Verifier si c'est un format multi-qualite [label]url
            if '[' in sFileContent and ']' in sFileContent:
                qua = []
                url = []
                # Format: [720p]https://xxx/video720.mp4,[480p]https://xxx/video480.mp4
                entries = re.findall(r'\[([^\]]+)\](https?://[^,\s"]+)', sFileContent)
                for label, link in entries:
                    qua.append(label)
                    url.append(link)

                if len(url) > 1:
                    api_call = dialog().VSselectqual(qua, url)
                elif len(url) == 1:
                    api_call = url[0]
                else:
                    return False, False

                return True, api_call

            # URL simple (HLS m3u8 ou MP4 direct)
            return True, sFileContent

        # Fallback: ancien format sources
        sPattern = 'sources:\s*\[\{(?:src|file):\s*"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            return True, aResult[1][0]

        return False, False
