#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import xbmcgui, dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'raptu', 'Rapidvideo')

    def _getMediaLinkForGuest(self):
        api_call = False

        sUrl = self._url

        oParser = cParser()
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        if 'rapidvideo' in sUrl:#qual site film illimite
            sPattern = '<a href="([^"]+&q=\d+p)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                url=[]
                qua=[]
                for i in aResult[1]:
                    url.append(str(i))
                    qua.append(str(i.rsplit('&q=', 1)[1]))

                if len(url) == 1:
                    sPattern = '<source src="([^"]+)" type="video/.+?"'
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    if aResult[0] is True:
                        api_call = aResult[1][0]


                elif len(url) > 1:
                    dialog2 = xbmcgui.Dialog()
                    ret = dialog2.select('Select Quality', qua)
                    if (ret > -1):
                        oRequest = cRequestHandler(url[ret])
                        sHtmlContent = oRequest.request()
                        sPattern = '<source src="([^"]+)" type="video/.+?"'
                        aResult = oParser.parse(sHtmlContent, sPattern)
                        if aResult[0] is True:
                            api_call = aResult[1][0]

            else:
                oRequest = cRequestHandler(sUrl)
                sHtmlContent = oRequest.request()
                sPattern = '<source src="([^"]+)" type="video/.+?" label="([^"]+)"'
                aResult = oParser.parse(sHtmlContent, sPattern)

                url=[]
                qua=[]
                api_call = False

                for aEntry in aResult[1]:
                    url.append(aEntry[0])
                    qua.append(aEntry[1])

                #Affichage du tableau
                api_call = dialog().VSselectqual(qua, url)

        else:
            sPattern = '{"file":"([^"]+)","label":"([^"]+)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                url=[]
                qua=[]
                for i in aResult[1]:
                    url.append(str(i[0]))
                    qua.append(str(i[1]))

                if len(url) == 1:
                    api_call = url[0]

                elif len(url) > 1:
                    dialog2 = xbmcgui.Dialog()
                    ret = dialog2.select('Select Quality', qua)
                    if (ret > -1):
                        api_call = url[ret]

        if api_call:
            return True, api_call

        return False, False
