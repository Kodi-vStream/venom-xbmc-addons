#coding: utf-8
import re
import xbmcgui

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'easyvid', 'EasyVid')

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()
        if 'File was deleted' in sHtmlContent:
            return False, False

        api_call = ''

        oParser = cParser()
        sPattern = '{file: *"([^"]+(?<!smil))"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            api_call = aResult[1][0]

        else:
            sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
            aResult = re.findall(sPattern, sHtmlContent)
            if (aResult):
                sUnpacked = cPacker().unpack(aResult[0])
                sHtmlContent = sUnpacked

                sPattern = '{file:"(.+?)",label:"(.+?)"}'
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
            return True, api_call

        return False, False
