#-*- coding: utf8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://thevideo.cc/embed-xxx.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
import xbmcgui


#UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'thevid', 'Thevid')

    def __getIdFromhtml(self, html):
        sPattern = "var thief='([^']+)';"
        oParser = cParser()
        aResult = oParser.parse(html, sPattern)
        if aResult[0] is True:
            return aResult[1][0]

        return ''

    def _getMediaLinkForGuest(self):

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        oParser = cParser()

        api_call = ''

        sId = self.__getIdFromhtml(sHtmlContent)
        if sId == '':
            return False, False

        oRequest = cRequestHandler('https://thevideo.cc/vsign/player/' + sId)
        sHtmlContent2 = oRequest.request()
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?\)\))"
        aResult = oParser.parse(sHtmlContent2, sPattern)
        if aResult[0] is True:
            sUnpacked = cPacker().unpack(aResult[1][0])
            sPattern = 'vt=([^"]+)";'
            aResult = oParser.parse(sUnpacked, sPattern)
            if aResult[0] is True:
                sVt =  aResult[1][0]

        sPattern = '"file":"([^"]+)","label":"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            #initialisation des tableaux
            url=[]
            qua=[]

            #Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            #Si une seule url
            if len(url) == 1:
                api_call = url[0]
            #si plus de une
            elif len(url) > 1:
            #Affichage du tableau
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Quality', qua)
                if (ret > -1):
                    api_call = url[ret]

        if api_call:
            return True, api_call + '?direct=false&ua=1&vt=' + sVt

        return False, False
