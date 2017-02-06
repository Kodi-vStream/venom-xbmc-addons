from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
from resources.lib.gui.gui import cGui

import re,xbmcgui,xbmc,urllib2

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'GoogleDrive'
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
        return 'googledrive'

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
        #sPattern = '\/([a-zA-Z0-9-_]{20,40})\/'
        sPattern = 'drive.google.+?([a-zA-Z0-9-_]{20,40})'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        #reformatage du lien
        sId = self.__getIdFromUrl(self.__sUrl)
        sUrl = 'https://drive.google.com/file/d/' + sId + '/view' #?pli=1

        #xbmc.log(sUrl)
        
        req = urllib2.Request(sUrl)
        response = urllib2.urlopen(req)  
        sHtmlContent = response.read()
        Headers = response.headers
        response.close()
        
        #listage des cookies
        c = Headers['Set-Cookie']
        c2 = re.findall('(?:^|,) *([^;,]+?)=([^;,\/]+?);',c)
        if c2:
            cookies = ''
            for cook in c2:
                cookies = cookies + cook[0] + '=' + cook[1]+ ';'  
                
        #xbmc.log(cookies)

        sPattern = '\["fmt_stream_map","([^"]+)"]\s*,\["fmt_list","([^"]+)"]'
        
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if not aResult[0]:
            #sUrl = 'https://drive.google.com/uc?export=download&id=' + sId + '&confirm=make'
            if '"errorcode","150"]' in sHtmlContent:
                cGui().showInfo("Erreur", "Nombre de lectures max depasse" , 5)
            return False,False
            
        sListUrl = aResult[1][0][0]
        sListRes = aResult[1][0][1]

        #initialisation des tableaux
        url=[]
        qua=[]
        api_call = ''
        
        #liste les qualitee
        r = re.findall('([0-9]+)\|([^\|,]+)',sListUrl,re.DOTALL)
        for item in r:
            r2 = re.search( str(item[0]) + '\/([0-9x]+)\/', sListRes)
            if r2:
                #xbmc.log( r2.group(1) + ' >> ' + item[1].decode('unicode-escape') )
                url.append(item[1].decode('unicode-escape'))
                qua.append(r2.group(1))

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
        
        api_call = api_call + '|User-Agent=' + UA + '&Cookie=' + cookies
        
        #xbmc.log(api_call)
            
        if (api_call):
            return True, api_call
            
        return False, False
