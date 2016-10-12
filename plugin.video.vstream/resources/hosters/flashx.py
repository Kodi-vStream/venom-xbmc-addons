#-*- coding: utf-8 -*-
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster

import re,urllib2
import xbmcgui

from resources.lib.packer import cPacker

import xbmc

#meme code que vodlocker

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'FlashX'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR] [COLOR khaki]'+self.__sHD+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'flashx'

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
        
    def GetRedirectHtml(self,web_url,sId):
        headers = {
        #'Host' : HOST,
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer':'http://embed.flashx.tv/embed.php?c=' + sId,
        #'Accept-Encoding':'gzip, deflate'
        }
        
        MaxRedirection = 3
        while MaxRedirection > 0:
            
            #generation headers
            headers2 = headers
            headers2['Host'] = self.GetHost(web_url)
            
            xbmc.log('Test sur : ' + web_url)
            request = urllib2.Request(web_url,None,headers)
      
            redirection_target = ''
        
            try:
                #ok ca a enfin marche
                reponse = urllib2.urlopen(request)
                sHtmlContent = reponse.read()
                reponse.close()
                break
            except urllib2.URLError, e:
                #print e.code
                #print e.headers
                #print e.read()
                if (e.code == 301) or  (e.code == 302):
                    redirection_target = e.headers['Location']
                    #xbmc.log('Redirection : ' + web_url)
         
            #pas de redirection on annulle
            if not (redirection_target):
                return False
                
            web_url = redirection_target
            
            MaxRedirection = MaxRedirection - 1
            
        return sHtmlContent       

    def __getIdFromUrl(self, sUrl):
        sPattern = "http://((?:www.|play.)?flashx.tv)/(?:embed-)?([0-9a-zA-Z]+)(?:.html)?"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0][1]

        return ''
        
    def GetHost(self,sUrl):
        oParser = cParser()
        sPattern = 'http:\/\/(.+?)\/'
        aResult = oParser.parse(sUrl, sPattern)
        if aResult[0]:
            return aResult[1][0]
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = 'http://' + self.GetHost(sUrl) + '/embed.php?c=' + self.__getIdFromUrl(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return ''

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()
        
    def __getMediaLinkForGuest(self):
        
        oParser = cParser()
        
        #on recupere le host atuel
        HOST = self.GetHost(self.__sUrl)
 
        #on recupere l'ID
        sId = self.__getIdFromUrl(self.__sUrl)
        
        #on ne garde que les chiffres
        sId = re.sub(r'-.+', '', sId)
        
        #on cherche la vraie url
        #web_url = 'http://' + HOST + '/playit-' + sId + '.html'
        sHtmlContent = self.GetRedirectHtml(self.__sUrl,sId)
        
        sPattern = 'href="(http:\/\/www\.flashx[^"]+)'
        aResult = re.findall(sPattern,sHtmlContent)
        if aResult:
            web_url = aResult[0]
        else:
            return False,False
        
        sHtmlContent = self.GetRedirectHtml(web_url,sId)
        
        if not sHtmlContent:
            return False,False 
            
        #A t on le lien code directement?
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        aResult = re.findall(sPattern,sHtmlContent)
        
        if not aResult:
            xbmc.log("page bloquee")

            #On recupere la bonne url
            sGoodUrl = web_url

            #on recupere la page de refresh
            sPattern = 'reload the page! <a href="([^"]+)">!! <b>'
            aResult = re.findall(sPattern,sHtmlContent)
            if not aResult:
                return False,False
            sRefresh = aResult[0]
            
            #on recupere le script de debloquage
            sPattern = 'type="text\/javascript" src="([^"]+checkembed[^"]+)"><\/script>'
            aResult = re.findall(sPattern,sHtmlContent)
            if not aResult:
                return False,False
            
            #on debloque la page (en test ca a l'air inutile)
            #sHtmlContent = self.GetRedirectHtml(aResult[0],sId)
            
            #lien speciaux ?
            if sRefresh.startswith('./'):
                sRefresh = 'http://' + self.GetHost(sGoodUrl) + sRefresh[1:]
            
            #on rafraichit la page
            sHtmlContent = self.GetRedirectHtml(sRefresh,sId)
            
            #et on re-recupere la page
            sHtmlContent = self.GetRedirectHtml(sGoodUrl,sId)
            
            #fh = open('c:\\test.txt', "w")
            #fh.write(sHtmlContent)
            #fh.close() 
                
            #et on recherche le lien code
            sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
            aResult = re.findall(sPattern,sHtmlContent)
        
        if (aResult):
            xbmc.log( "lien code")
            sUnpacked = cPacker().unpack(aResult[0])
            sHtmlContent = sUnpacked
            
            #xbmc.log(sHtmlContent)
  
        #decodage classique
        sPattern = '{file:"([^",]+)",label:"([^"<>,]+)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)

        api_call = ''
        
        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
        
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

        #print api_call
        
        if (api_call):
            return True, api_call
            
        return False, False
        
