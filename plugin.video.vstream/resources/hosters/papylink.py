from resources.lib.handler.requestHandler import cRequestHandler 
from resources.lib.config import cConfig 
from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser 
import re,xbmc

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Papylink'
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
        return 'papylink'
        
    def setHD(self, sHD):
        self.__sHD = ''
        
    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return False

    def isJDownloaderable(self):
        return False

    def getPattern(self):
        return ''
    
    def __getIdFromUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
    
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
    
        sUrl = self.__sUrl
        
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        sPattern =  '<iframe.+?src="([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            web_url = aResult[1][0]
            if 'drive.google' in web_url:
                from resources.hosters.googledrive import cHoster as cHoster2
                web_url = web_url.replace('open?id=','file/d/').replace('@','/view') 
                c = cHoster2()
                c.setUrl(web_url)
                api_call = c.getMediaLink()[1]

            else: 
                #au cas ou ancienne methode
                oRequest = cRequestHandler(web_url)
                sHtmlContent = oRequest.request()

                sPattern = "{file: '([^']+)',.+?label : '([^']+)'}],"
                oParser = cParser()
                aResult = oParser.parse(sHtmlContent,sPattern)
                if (aResult[0] == True):
                    #initialisation des tableaux
                    url=[]
                    qua=[]
                    api_call = ''
                    #Replissage des tableaux
                    for i in aResult[1]:
                        url.append(str(i[0]))
                        qua.append(str(i[1]))
                    #Si une seule url
                    if len(url) == 1:
                       api_call = url[0]
                    #si plus de une
                    elif len(url) > 1:
                    #Afichage du tableau
                       dialog2 = xbmcgui.Dialog()
                       ret = dialog2.select('Select Quality',qua)
                       if (ret > -1):
                           api_call = url[ret]
                       else: 
                           return False, False

            if (api_call):
                return True, api_call
            
            return False, False
                
