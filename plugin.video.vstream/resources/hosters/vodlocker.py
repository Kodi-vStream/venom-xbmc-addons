from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import re,urllib2,urllib

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Vodlocker'
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
        return 'vodlocker'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def __getIdFromUrl(self, sUrl):
        oParser = cParser()
        
        sPattern = 'http://((?:www.)?vodlocker.com)/(?:embed-)?([0-9a-zA-Z]+)(?:-\d+x\d+.html)?'
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0][1]
            
        sPattern = 'http://vodlocker.com/([^<]+)'
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]
            
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self,media_id):
        return 'http://vodlocker.com/embed-%s-640x400.html' % (media_id)

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        sId = self.__getIdFromUrl(self.__sUrl)
        sUrl = self.getUrl(sId)

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
        
        # merci de laisser cette partie, elle me servira plus tard
        # sPattern = '<Form method="POST" action='
        # aResult = oParser.parse(sHtmlContent, sPattern)


        # if (aResult[0] == True):
            # url = self.__sUrl
        
            # op = oParser.parse(sHtmlContent, 'name="op" value="(.+?)">')
            # id = oParser.parse(sHtmlContent, 'name="id" value="(.+?)">')
            # fname = oParser.parse(sHtmlContent, 'name="fname" value="(.+?)">')
            # hash = oParser.parse(sHtmlContent, 'name="hash" value="(.+?)">')
            # #ameliorer op pattern, pour le moment je force a download1
            # query_args = { 'op' : 'download1' , 'usr_login' : '' , 'id' : str(id[1][0]), 'fname' : str(fname[1][0]) , 'referer' :'', 'hash' : str(hash[1][0]), 'imhuman' : 'Proceed to video'}
            # data = urllib.urlencode(query_args)
      
            # headers = {'User-Agent' : 'Mozilla 5.10', 'Referer' : str(url)}
            
            # request = urllib2.Request(url,data,headers)
          
            # try: 
                # reponse = urllib2.urlopen(request)
            # except URLError, e:
                # print e.read()
                # print e.reason
          
            # html = reponse.read()
            # sHtmlContent = html
        
        sPattern = 'file: "([^"]+)"'
        
        sHtmlContent=sHtmlContent.replace('|','/')
        aResult = oParser.parse(sHtmlContent, sPattern)

        
        if (aResult[0] == True):
            api_call = aResult[1][0]
            return True, api_call
            
        return False, False
        
       
        
