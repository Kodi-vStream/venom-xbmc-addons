#-*- coding: utf8 -*-
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
import urllib, urllib2, re

#pris a urlresolver
class Base36:
    def __init__(self,ls=False):
        self.ls = False
        if ls :
            self.ls = ls
    
    def base36encode(self,number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
        """Converts an integer to a base36 string."""
        if not isinstance(number, (int, long)):
            raise TypeError('number must be an integer')
        base36 = ''
        sign = ''
        if number < 0:
            sign = '-'
            number = -number
        if 0 <= number < len(alphabet):
            return sign + alphabet[number]
        while number != 0:
            number, i = divmod(number, len(alphabet))
            base36 = alphabet[i] + base36
        return sign + base36
     
    def base36decode(self,number):
        return int(number, 36)
    
    def param36decode(self,match_object) :
        if self.ls :
            param = int(match_object.group(0), 36)
            return str(self.ls[param])
        else :
            return False

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Youwatch'
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
        return 'youwatch'

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
        sPattern = "http://youwatch.org/([^<]+)"
        oParser = cParser()

        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def setUrl(self, sUrl):
        if 'embed' not in sUrl:
            self.__sUrl = str(self.__getIdFromUrl(sUrl))
            self.__sUrl = 'http://youwatch.org/embed-'+str(self.__sUrl)+'.html'
            if not re.match('[0-9]+x[0-9]+.html',self.__sUrl,re.IGNORECASE):
                 self.__sUrl =  self.__sUrl.replace('.html','-640x360.html')
        else:
            self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()
        
    #fonction speciale pour decrytptage venant de urlresolver
    def exec_javascript(self,lsParam) :
        return re.sub('[a-zA-Z0-9]+',Base36(lsParam[3]).param36decode,str(lsParam[0]))

    def __getMediaLinkForGuest(self): 
        
        #print self.__sUrl
                    
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
        
        #1 er test en cas de fausse page
        sPattern ='<iframe[^<>]+?src="(.+?)" [^<>]+?> *<\/iframe>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
            headers = {'User-Agent': UA ,
            #'Host' : 'i93.whies.info',
            'Referer': aResult[1][0]}
            #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            #'Content-Type': 'text/html; charset=utf-8'}
            
            req = urllib2.Request(aResult[1][0],None,headers)
            try:
                response = urllib2.urlopen(req)
                
            except urllib2.URLError, e:
                print e.read()
                print e.reason
            
            sHtmlContent = response.read()
            response.close()
              
        #2 eme test, le vrai
        html = sHtmlContent.decode('utf-8')
        jscript = re.findall("""function\(p,a,c,k,e,d\).*return p\}(.*)\)""", html)
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()

        if (jscript):

            lsParam = eval(jscript[0].encode('utf-8'))
            flashvars = self.exec_javascript(lsParam)
            r = re.findall('file:"(.*)",provider', flashvars)
            if r:
                return True, r[0]

        #3 eme test
        sPattern ='\[{file:"(.+?)",label:"(.+?)"}\]'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            return True , aResult[1][0][0] + '|Referer=' + self.__sUrl
        
        cGui().showInfo(self.__sDisplayName, 'Fichier introuvable' , 5)
        
        return False, False
        
        
