#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'allvid', 'Allvid')

    def _getMediaLinkForGuest(self):
        #print self._url
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()

        #lien indirect
        sPattern = '<iframe.+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            oRequest = cRequestHandler(aResult[1][0])
            sHtmlContent = oRequest.request()

        #test pour voir si code
        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\))<\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            sHtmlContent = cPacker().unpack(aResult[1][0])

        sPattern = 'file:"([^"]+\.mp4)"(?:,label:"([^"]+)")*'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:

            #initialisation des tableaux
            url=[]
            qua=[]

            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            #Afichage du tableau
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, api_call

        return False, False
