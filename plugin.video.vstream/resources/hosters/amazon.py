from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
import urllib,urllib2
from urllib2 import URLError

#https://github.com/svn2github/jdownloader/blob/master/src/jd/plugins/hoster/AmazonCloud.java

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Amazon'
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
        return 'amazon'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self, sUrl):
        sPattern = '\/share\/(.+?)\?'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''       
       
    def __getKey(self):
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
        cGui().showInfo('Resolve', self.__sDisplayName, 5)
        
        id = ''
        
        sId = self.__getIdFromUrl(self.__sUrl)
        
        Url = 'https://www.amazon.fr/drive/v1/shares/' + sId + '?customerId=&resourceVersion=V2&ContentType=JSON&asset=ALL'
       
        oRequest = cRequestHandler(Url)
        sHtmlContent = oRequest.request()
        
        oParser = cParser()
        
        sPattern = '"id":"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            id = aResult[1][0]            
                   
            url2 = 'https://www.amazon.fr/drive/v1/nodes/' + id + '/children?customerId=&resourceVersion=V2&ContentType=JSON&limit=200&sort=%5B%22kind+DESC%22%2C+%22name+ASC%22%5D&tempLink=true&shareId=' + sId      

            oRequest = cRequestHandler(url2)
            sHtmlContent = oRequest.request()
            
            #fh = open('c:\\test.txt', "w")
            #fh.write(sHtmlContent)
            #fh.close()
            
            sPattern = '"tempLink":"(.+?)"'
            aResult = oParser.parse(sHtmlContent, sPattern)
        
            if (aResult[0] == True):
                return True, aResult[1][0]
            else:
                cGui().showInfo(self.__sDisplayName, 'Fichier introuvable' , 5)
                return False, False
        else:
            cGui().showInfo(self.__sDisplayName, 'Fichier introuvable' , 5)
            return False, False
        
        return False, False
