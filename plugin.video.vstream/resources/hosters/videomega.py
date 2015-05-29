from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.hosters.hoster import iHoster
import xbmcgui,xbmc
import urllib2
import re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'VideoMega'
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
        return 'videomega'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self):
        sPattern = "ref=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
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
        
        headers = {'Host' : 'videomega.tv',
                   'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
                   #'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   #'Accept-Language' : 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                   #'Accept-Encoding' : 'gzip, deflate',
                   'Referer' : self.__sUrl
                   }
        
        url = self.__sUrl
        request = urllib2.Request(url,None,headers)
        
        #print url
      
        try: 
            reponse = urllib2.urlopen(request)
        except URLError, e:
            print e.read()
            print e.reason
        
        sHtmlContent = reponse.read()
        
        api_call = False
        
        #si on passe pr le hash code
        if 'validatehash.php?hashkey=' in url:
            if 'ref=' in sHtmlContent:
                a = re.compile('.*?ref="(.+?)".*').findall(sHtmlContent)[0]
                url = 'http://videomega.tv/cdn.php?ref=' + a
                
                request = urllib2.Request(url,None,headers)
             
                try: 
                    reponse = urllib2.urlopen(request)
                except URLError, e:
                    print e.read()
                    print e.reason
             
                sHtmlContent = reponse.read()
                
        #Premier test, lien ok
        sPattern =  '<source src="([^"]+)" type="video[^"]*"\/>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            api_call = aResult[1][0]
            
        #Deuxieme test, lien code
        if not api_call:
            #troisieme test
            sPattern =  'unescape.+?"(.+?)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)

            if (aResult[0] == True):
                decoder = cUtil().urlDecode(aResult[1][0])
                
                sPattern =  'file: "(.+?)"'
                oParser = cParser()
                aResult = oParser.parse(decoder, sPattern)
                
                if (aResult[0] == True):
                    api_call = aResult[1][0]
                 

        #print 'url : ' + api_call

        if (api_call):
            xbmc.sleep(6000)
            return True, api_call
            
        return False, False
