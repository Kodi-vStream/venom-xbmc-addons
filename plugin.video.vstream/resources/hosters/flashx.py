from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import re,urllib2
import xbmcgui
from resources.lib.packer import cPacker

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
        
    def __getIdFromUrl(self, sUrl):
        sPattern = "http://((?:www.|play.)?flashx.tv)/(?:embed-)?([0-9a-zA-Z/-]+)(?:.html)?"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0][1]

        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return ''

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        HOST = 'www.flashx.host'
 
        sId = self.__getIdFromUrl(self.__sUrl)
        #web_url = 'http://' + HOST + '/fxplay-%s.html' % sId
        web_url = 'http://' + HOST + '/fxplaynew-%s.html' % sId
        
        sId = re.sub(r'-.+', '', sId)
        
        print web_url

        headers = {
        'Host' : HOST,
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer':'http://embed.flashx.tv/embed.php?c=' + sId,
        #'Accept-Encoding':'gzip, deflate'
        }
        
        request = urllib2.Request(web_url,None,headers)
      
        redirection_target = ''
        
        try:
            reponse = urllib2.urlopen(request)
        except urllib2.URLError, e:
            #print e.code
            #print e.headers
            #print e.read()
            if (e.code == 301) or  (e.code == 302):
                redirection_target = e.headers['Location']
                print redirection_target
         
        if (redirection_target):
            #get new hoster
            oParser = cParser()
            sPattern = 'http:\/\/(.+?)\/'
            aResult = oParser.parse(redirection_target, sPattern)
            HOST = aResult[1][0]

            headers2 = {
            'Host' : HOST,
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer':'http://embed.flashx.tv/embed.php?c=' + sId,
            #'Accept-Encoding':'gzip, deflate'
            }
            
            request2 = urllib2.Request(redirection_target,None,headers2)
            try:
                reponse = urllib2.urlopen(request2)
            except urllib2.URLError, e:
                print e.code
                print e.headers
                
        sHtmlContent = reponse.read()

        #Lien code ??
        sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
        aResult = re.findall(sPattern,sHtmlContent)
        #aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult):
            print "lien code"
            sUnpacked = cPacker().unpack(aResult[0])
            sHtmlContent = sUnpacked
            
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()    
  
        #decodage classique
        oParser = cParser()
        sPattern = '{file:"(.+?)",label:"(.+?)"}'
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
                
            #Si au moins 1 url
            if (url):
            #Afichage du tableau
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Quality',qua)
                if (ret > -1):
                    api_call = url[ret]

        #print api_call
        
        if (api_call):
            return True, api_call
            
        return False, False
