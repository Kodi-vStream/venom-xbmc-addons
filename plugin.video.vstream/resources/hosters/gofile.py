# -*- coding: utf-8 -*-
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import dialog
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster

class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'gofile', 'GoFile')

    def _getMediaLinkForGuest(self):
        # guest token
        oRequest = cRequestHandler('https://api.gofile.io/accounts')
        oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        data = oRequest.request(jsonDecode=True)
        token = data.get("data", {}).get("token")
        
        # web token
        oRequest = cRequestHandler('https://gofile.io/dist/js/config.js')
        sHtmlContent = oRequest.request()
        aResult = cParser().parse(sHtmlContent, 'appdata.wt = "([^"]+)')
        if not aResult[0]:
            return False, False
        
        webToken = aResult[1][0]
        mediaId = self._url.split('/')[-1]
        urlAPI = 'https://api.gofile.io/contents/%s?wt=%s&cache=true' % (mediaId, webToken)
        oRequest = cRequestHandler(urlAPI)
        oRequest.addHeaderEntry('x-website-token', webToken)
        oRequest.addHeaderEntry('authorization', 'Bearer %s' % token)
        data = oRequest.request(jsonDecode=True)

        status = data.get('status')
        if status != 'ok':
            dialog().VSinfo(status, 'gofile')
            return False, False

        # le lien du premier fichier
        childs = data['data']['children']
        for file in childs:       
            return True, childs.get(file).get('link') + '|cookie=accountToken%3D' + token
        
        return False, False
