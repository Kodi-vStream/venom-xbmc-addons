from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
from resources.lib.gui.gui import cGui

from resources.lib.handler.premiumHandler import cPremiumHandler

import urllib,urllib2
import xbmc

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = '1Fichier'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR violet]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'onefichier'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True
        
    def __getIdFromUrl(self, sUrl):
        #http://kzu0y3.1fichier.com/
        #https://1fichier.com/?s6gdceia9y
        id = sUrl.replace('https://','')
        id = id.replace('http://','')
        id = id.replace('1fichier.com/?','')
        id = id.replace('.1fichier.com','')
        id = id.replace('/','')
        
        return id

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return
        
    def getMediaLink(self):
        
        self.oPremiumHandler = cPremiumHandler(self.getPluginIdentifier())
        print self.oPremiumHandler.isPremiumModeAvailable()
        
        import sys
        if ('site=cDownload&function' not in sys.argv[2]) and not (self.oPremiumHandler.isPremiumModeAvailable()):
            oDialog = cConfig().createDialogOK('ATTENTION, Pas de streaming sans premium\nPour voir le film passer par l\'option "DL et Visualiser" du menu contextuel.')
            return False,False

        cGui().showInfo('Resolve', self.__sDisplayName, 5)
        
        if (self.oPremiumHandler.isPremiumModeAvailable()):
            return self.__getMediaLinkByPremiumUser()

        return self.__getMediaLinkForGuest()

        
    def __getMediaLinkByPremiumUser(self):
        
        if not self.oPremiumHandler.Authentificate():
            return False, False

        url = 'https://1fichier.com/?' + self.__getIdFromUrl(self.__sUrl)
        
        #Mode = ''
        #Mode = {'dl_no_ssl' : 'on' , 'dlinline' : 'on'}
        #Mode = {'dl_no_ssl' : 'on' }
        #postdata = urllib.urlencode( Mode )
        
        #Pas de page html mais lien direct
        #sHtmlContent = self.oPremiumHandler.GetHtml(url,postdata)
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()        
        
        #mode inline
        #url = url + '&inline'
        
        api_call = url + '|' + self.oPremiumHandler.AddCookies()
        
        #print api_call
        
        if (api_call):
            return True, api_call
            
        return False, False
        
    def __getMediaLinkForGuest(self):

        url = 'https://1fichier.com/?' + self.__getIdFromUrl(self.__sUrl)
        
        headers = {'User-Agent': UA ,
                   'Host' : '1fichier.com',
                   'Referer' : self.__sUrl ,
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language' : 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3'
                   #'Content-Type': 'application/x-www-form-urlencoded'
                   }
        
        Mode = ''
        #Mode = {'dl_no_ssl' : 'on' , 'dlinline' : 'on'}
        Mode = {'dl_no_ssl' : 'on' }
        postdata = urllib.urlencode( Mode )
        
        req = urllib2.Request(url,postdata,headers)
        
        try:
            response = urllib2.urlopen(req)
        except URLError, e:
            print e.read()
            print e.reason
        
        sHtmlContent = response.read()
        response.close()        
        
        api_call = GetMedialinkDL(sHtmlContent)
        
        if (api_call):
            return True, api_call
            
        return False, False
        
    def GetMedialinkDL(self,sHtmlContent):
        
        oParser = cParser()
        
        sPattern = 'Vous devez attendre encore [0-9]+ minutes'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            cGui().showInfo('Erreur - Limitation', aResult[1][0] , 5)
            return False
        
        sPattern = '<a href="([^<>"]+?)"  style="float:none;margin:auto;font-weight:bold;padding: 10px;margin: 10px;font-size:\+1\.6em;border:2px solid red" class="ok btn-general btn-orange">'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        #print aResult
        
        if (aResult[0] == True):
            #xbmc.sleep(1*1000)
            print aResult[1][0]
            api_call = aResult[1][0] + '|User-Agent=' + UA# + '&Referer=' + self.__sUrl
            return api_call
        
        return False
        
