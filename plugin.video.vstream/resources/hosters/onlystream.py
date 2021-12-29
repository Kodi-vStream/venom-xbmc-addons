#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'onlystream', 'OnlyStream')

    def _getMediaLinkForGuest(self):
        api_call = False

        oParser = cParser()
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern =  '(?:file|src): *"([^"]+)"[^{}<>]+?(?:, *label: *"([^"]+)")*}'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            api_call = aResult[1][0][0]

        else:
            sPattern = '(\s*eval\s*\(\s*function\(p,a,c,k,e(?:.|\s)+?)<\/script>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                sHtmlContent = cPacker().unpack(aResult[1][0])

                sPattern =  '(?:file|src): *"([^"]+)"[^{}<>]+?(?:, *label: *"([^"]+)")*}'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0] is True:
                    url=[]
                    qua=[]
                    for i in aResult[1]:
                        url.append(str(i[0]))
                        if len(i) > 1:
                            q = str(i[1])
                        else:
                            q = "Inconnu"
                            qua.append(q)

                    api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
