from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import re,urllib2,urllib,time
import xbmcgui

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'ZStream'
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
        return 'zstream'

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
        
    def __getIdFromUrl(self):
        sPattern = 'http:\/\/zstream.+?\/(.+)'
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        
        if (aResult[0] == True):
            return aResult[1][0]
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
        
        #print self.__sUrl
   
        api_call = False
        
        #print self.__sUrl
        
        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()
        
        # id = self.__getIdFromUrl()
        
        # oParser = cParser()
        # sPattern = 'name="op" value="(.+?)">.+?name="fname" value="(.+?)">.+?name="hash" value="(.+?)">'
        # aResult = oParser.parse(sHtmlContent, sPattern)

        # if (aResult[0] == True):
            
            # #Need to wait
            # time.sleep( 5 )
            
            # UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
            # headers = {'User-Agent': UA ,
                   # 'Host' : 'zstream.to',
                   # 'Referer': self.__sUrl,
                   # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   # #'Content-Type' : 'application/x-www-form-urlencoded',
                   # #'Content-Length': '218',
                   # 'Connection': 'keep-alive' }

            # postdata = {'id': id , 'imhuman' : 'Proceed to video' , 'op' : aResult[1][0][0] , 'fname' : aResult[1][0][1] , 'hash' : aResult[1][0][2] }
            
            # req = urllib2.Request(self.__sUrl,urllib.urlencode(postdata),headers)
            
            
            # try:
                # response = urllib2.urlopen(req)
            # except urllib2.URLError, e:
                # print e.read()
                # print e.reason
            
            # sHtmlContent = response.read()
            # response.close()
            
        #fh = open('c:\\zstream.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        oParser = cParser()
        sPattern = '{file:"(.+?)",label:"(.+?)"}'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        #print aResult

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
