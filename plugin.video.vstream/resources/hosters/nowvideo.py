#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster

import re,xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Nowvideo'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'nowvideo'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self,sUrl):
        sPattern = 'v=([^<]+)'
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''
        
    def __modifyUrl(self, sUrl):
        if (sUrl.startswith('http://')):
            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.request()
            sRealUrl = oRequestHandler.getRealUrl()
            self.__sUrl = sRealUrl
            return self.__getIdFromUrl()

        return sUrl;
        
    def __getKey(self):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        
        sPattern =  'http:\/\/(?:www.|embed.)nowvideo.[a-z]{2}\/(?:video\/|embed.+?\?.*?v=)([0-9a-z]+)' 
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)        
        self.__sUrl = 'http://embed.nowvideo.sx/embed.php?v=' + str(aResult[1][0])

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        api_call = ''
        
        oParser = cParser()

        id = self.__getIdFromUrl(self.__sUrl)
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        # 1 er lecteur
        r = re.search('var fkzd="([^"]+)"', sHtmlContent)
        if (r):
            surl = 'http://www.nowvideo.sx/api/player.api.php?key=' + r.group(1) +'&file=' + id
            oRequest = cRequestHandler(surl)
            sHtmlContent = oRequest.request()

            r2 = re.search('url=([^&]+)', sHtmlContent)
            if (r2):
                api_call = r2.group(1)
                
        #second lecteur
        sPattern = '<source src="([^"]+)" type=\'([^"\']+)\'>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
        
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))
                
            #Si au moins 1 url
            if (url):
            #Afichage du tableau
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Quality',qua)
                if (ret > -1):
                    api_call = url[ret]
                
        if (api_call):
            return True, api_call

        return False , False
