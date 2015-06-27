from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import urllib, urllib2,re
import xbmcgui

try:    import json
except: import simplejson as json

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'PlayReplay'
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
        return 'playreplay'

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
        sPattern = 'http:..playreplay.net\/framevideo\/(.+?)\?'
        aResult = re.findall(sPattern,sUrl)
        if (aResult):
            return aResult[0]

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
        vUrl = False
        sId = self.__getIdFromUrl(self.__sUrl)

        query_args = {'r':'["tVL0gjqo5",["preview/flv_image",{"uid":"' + sId + '"}],["preview/flv_link",{"uid":"' + sId + '"}]]'}
        
        data = urllib.urlencode(query_args)
        headers = {'User-Agent' : 'Mozilla 5.10'}
        url = 'http://api.letitbit.net'
        request = urllib2.Request(url,data,headers)
        
        try:
            reponse = urllib2.urlopen(request)
        except URLError, e:
            print e.read()
            print e.reason
     
        html = reponse.read()  
        
        sHtmlContent = html.replace('\\','')

        link = re.findall('"link":"(.+?)"',sHtmlContent)
        if link:
            vUrl = link[0]
        
        #print vUrl
        
        if (vUrl):
            api_call = vUrl
            return True, api_call
            
        return False, False
        
        
