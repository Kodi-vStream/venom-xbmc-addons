#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser 
import re,xbmcgui,urllib

URL_MAIN = 'http://keepvid.com/?url='

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Youtube'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName
        
    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'youtube'
        
    def setHD(self, sHD):
        self.__sHD = ''
        
    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
    
    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, sUrl):
        return
    
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        oParser = cParser()
        
        sUrl = urllib.quote_plus(self.__sUrl)
        
        oRequest = cRequestHandler('%s%s' % (URL_MAIN,sUrl))
        sHtmlContent = oRequest.request()

        sPattern = 'Full Video<\/dt>(.+?)Video Only<\/dt><dd>'
        sHtmlContent2 = re.search(sPattern,sHtmlContent,re.DOTALL)
        if not sHtmlContent2:
            return False,False
            
        oParser = cParser()
        
        sPattern = '<a href="([^"]+)".+?alt=""/>([^<]+)<\/span>' 
        aResult = oParser.parse(sHtmlContent2.group(1),sPattern)

        if (aResult[0] == True):
            # initialisation des tableaux
            url=[]
            qua=[]
            # Replissage des tableaux
            for i in aResult[1]:
                b = re.sub('&title=.+','',i[0]) #testé xx fois ok
                #xbmc.log(str(b))
                url.append(str(b))
                qua.append(str(i[1]))   
            # Si une seule url
            if len(url) == 1:
                api_call = url[0]
            # si plus de une
            elif len(url) > 1:
            # Afichage du tableau
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Quality',qua)
                if (ret > -1):
                    api_call = url[ret]

        if (api_call):
            return True, api_call
            
        return False, False
