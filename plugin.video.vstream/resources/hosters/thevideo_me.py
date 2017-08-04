#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#http://www.video.tt/embed/xxx
#http://thevideo.me/embed-xxx-xxx.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.util import VScreateDialogSelect
from resources.lib.packer import cPacker
import re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'TheVideo'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR] [COLOR khaki]' + self.__sHD + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'thevideo_me'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def __getIdFromUrl(self,sUrl):
        sPattern = 'http://www.thevideo.me/embed-([^\.]+)'
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl.replace('video.tt/embed/', 'thevideo.me/embed-')
        if not self.__sUrl.endswith('.html'):
           self.__sUrl = self.__sUrl + '.html'

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        api_call = False

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        
        sPattern = "var lets_play_a_game='([^']+)'"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if not (aResult[0]):
            return False , False
            
        key = aResult[1][0]
            
        sPattern = "'rc=[^<>]+?\/(.+?)'\.concat"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if not (aResult[0]):
            return False , False
            
        ee = aResult[1][0]
            
        url2 = 'http://thevideo.me/' + ee + '/' + key

        oRequest = cRequestHandler(url2)
        sHtmlContent2 = oRequest.request()
        
        code = cPacker().unpack(sHtmlContent2)
        sPattern = '"vt=([^"]+)'
        r2 = re.search(sPattern,code)
        if not (r2):
            return False,False
            
        sPattern = '{"file":"([^"]+)","label":"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
        
            #Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))
                
            #Si  1 url
            if len(url) == 1:
                api_call = url[0]
            #Affichage du tableau
            elif len(url) > 1:
                ret = VScreateDialogSelect(qua)
                if (ret > -1):
                    api_call = url[ret]

        if (api_call):
            return True, api_call + '?direct=false&ua=1&vt=' + r2.group(1)
            
        return False, False
