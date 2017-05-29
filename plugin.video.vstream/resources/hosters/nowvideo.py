#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
import re,xbmcgui

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

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

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        # 1 er lecteur
        sDash = re.search("player.src.+?src: *'([^']+)", sHtmlContent,re.DOTALL)
        if (sDash):
            return True, sDash.group(1) 
        else:
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
                return True, api_call #+ '|User-Agent=' + UA  

            return False , False
