from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.lib.config import cConfig
import cookielib
#import simplejson
import urllib2,urllib,re
#from t0mm0.common.net import Net
import unicodedata
import xbmcgui

try:    import json
except: import simplejson as json

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'MailRu'
	self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
	self.__sFileName = sFileName

    def getFileName(self):
	return self.__sFileName
    
    def setUrl(self, sUrl):
        self.__sUrl = sUrl.replace('/my.mail.ru/video/', '/api.video.mail.ru/videos/embed/')
        self.__sUrl = self.__sUrl.replace('/my.mail.ru/mail/', '/api.video.mail.ru/videos/embed/mail/')
        self.__sUrl = self.__sUrl.replace('/videoapi.my.mail.ru/', '/api.video.mail.ru/')
    
    def __getIdFromUrl(self):
        pass
        #sPattern = 'http:..www.purevid.com.\?m=embed&id=([^<]+)'
        #oParser = cParser()
        #aResult = oParser.parse(self.__sUrl, sPattern)
        #if (aResult[0] == True):
        #    return aResult[1][0]
        #return ''
        
    def __modifyUrl(self, sUrl):
        api = ('http://rutube.ru/api/play/trackinfo/%s/?format=json') % (self.__getIdFromUrl())

        oRequest = cRequestHandler(api)
        sHtmlContent = oRequest.request()
        sHtmlContent = sHtmlContent.replace('\\', '').replace('//', '')
        
        sPattern = 'src="(.+?)"'
        
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            self.__sUrl = 'http://' + aResult[1][0]
            return self.__sUrl
            
        return


    def getPluginIdentifier(self):
        return 'mailru'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        
        referer='http://img.mail.ru/r/video2/uvpv3.swf?3'
        UA='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

        #cookie = getUrl(url, output='cookie').result
        cookie='VID=2SlVa309oFH4; mrcu=EE18510E964723319742F901060A; p=IxQAAMr+IQAA; video_key=203516; s='
        h = "|Cookie=%s" % urllib.quote(cookie)
        
        result = []
        headers = { "User-Agent":UA, "Referer":referer , "Cookie":cookie }
        # header "Cookie" with parameters need to be set for your download/playback
        
        #recuperation du lien
        oRequestHandler = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequestHandler.request();
        sPattern = '"metadataUrl":"(.+?)","autoplay"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        vurl = aResult[1][0]
        
        #req = urllib2.Request('http://api.video.mail.ru/videos/' + vurl + '.json',headers)
        req = urllib2.Request(vurl,None,headers)
        
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            print e.read()
            print e.reason
        
        data=response.read()
        response.close()
        result = json.loads(data)
        
        url=[]
        qua=[]
        
        for i in result[u'videos']:
            url.append(str(i['url']))
            qua.append(str(i['key']))
        
        if (url):
            #cConfig().showInfo(self.__sDisplayName, 'fgdgfds')
             
            dialog2 = xbmcgui.Dialog()
            ret = dialog2.select('Select Quality',qua)
            return True, url[ret] + h
        else:
            cConfig().showInfo(self.__sDisplayName, 'Fichier introuvable')
            return False, False
        
        return False, False