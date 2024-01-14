# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# ==>vikki
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
import xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Viki'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'viki'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()


    
    def __getMediaLinkForGuest(self, api_call=None):
        
        # lesite ne fournit plus que du Mdp plus de format ['480p','360p','240p',
        sUrl = self.__sUrl
        # srtsubs_path = xbmc.translatePath('special://temp/vikir.English.srt')
        # Methode 1 on recoit une liste sUrl=[ urlstream,sub,q1,q2...urlq1,urlq2

        sUrl = tuple(map(str, sUrl.split(',')))

        if len(sUrl) == 2:
            api_call = sUrl[0]
        else:
            url = []
            qual = []
            for a in sUrl:
                url.append(a)
                qu = re.search('max_res=(\d+)',a).group(1)
                qual.append(qu)
            api_call = self.mydialog().VSselect(qual, url, 'Viki Select quality :')

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
