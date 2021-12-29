#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#Arias800
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog#, VSlog

# import re

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'freshstream', 'Freshstream')

    def _getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern =  "var vsuri = \'(.+?)\'"
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0]):
            oRequest = cRequestHandler(aResult[1][0])
            sHtmlContent1 = oRequest.request()

            sPattern1 =  '"([^"]+)":"([^"]+)"'
            aResult1 = oParser.parse(sHtmlContent1, sPattern1)

        if (aResult1[0]):

            url=[]
            qua=[]
            api_call = False

            for aEntry in aResult1[1]:
                url.append(aEntry[1])
                qua.append(aEntry[0])

            api_call = dialog().VSselectqual(qua, url)

            if api_call:
                return True, api_call

        return False, False
