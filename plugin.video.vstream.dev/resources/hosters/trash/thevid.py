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
        self.__sDisplayName = 'Thevid'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'thevid'

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
        
    def __getIdFromhtml(self, html):
        sPattern = "var thief='([^']+)';"
        oParser = cParser()
        aResult = oParser.parse(html, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self): 
  
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        oParser = cParser()

        api_call = ''
        
        sId = self.__getIdFromhtml(sHtmlContent)
        if sId == '':
            return False,False
            
        oRequest = cRequestHandler('https://thevideo.cc/vsign/player/' + sId)
        sHtmlContent2 = oRequest.request()
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?\)\))"
        aResult = oParser.parse(sHtmlContent2, sPattern)
        if (aResult[0] == True):
            sUnpacked = cPacker().unpack(aResult[1][0])
            sPattern = 'vt=([^"]+)";'
            aResult = oParser.parse(sUnpacked, sPattern)
            if (aResult[0] == True):
                sVt =  aResult[1][0]
        
        sPattern = '"file":"([^"]+)","label":"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
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
        
        if (api_call):
            return True, api_call + '?direct=false&ua=1&vt=' + sVt 
            
        return False, False
        
        
