# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# ==>vikki
import re
import xbmcgui

from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'viki', 'Viki')

    def _getMediaLinkForGuest(self, api_call=None):
        # lesite ne fournit plus que du Mdp plus de format ['480p','360p','240p',
        # srtsubs_path = xbmc.translatePath('special://temp/vikir.English.srt')
        # Methode 1 on recoit une liste url=[ urlstream,sub,q1,q2...urlq1,urlq2

        url = tuple(map(str, self._url.split(',')))

        if len(url) <= 2:
            api_call = url[0]
        else:
            link = []
            qual = []
            for a in url:
                q = re.search('max_res=(\d+)',a)
                if q:
                    link.append(a)
                    qu = q.group(1)
                    qual.append(qu)
            if len(link) == 0:
                api_call = a
            elif len(link) == 1:
                api_call = link[1]
            elif len(link) > 1:
                api_call = self.mydialog().VSselect(qual, link, 'Viki Select quality :')

        if api_call:
            return True, api_call
        return False, False

    class mydialog(xbmcgui.Dialog):
        def VSselect(self, list_alias, list_toreturn, sTitle):

            if len(list_toreturn) == 0:
                return ''
            if len(list_toreturn) == 1:
                return list_toreturn[0]

            ret = self.select(sTitle, list_alias)
            if ret > -1:
                return list_toreturn[ret]
            return ''
