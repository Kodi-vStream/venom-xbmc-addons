from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
import urllib, urllib2, re
import xbmc

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Streamin.to'
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
        self.__sUrl = sUrl
    
    def __getIdFromUrl(self,sUrl):
        sPattern = 'http://((?:www.)?streamin.to)/(.*)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        
        if (aResult[0] == True):
            return aResult[1][0][1]

        return ''
        
    def __modifyUrl(self, sUrl):
        return

    def getPluginIdentifier(self):
        return 'streaminto'

    def isDownloadable(self):
        return False

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';

    def checkUrl(self, sUrl):
        return True

    def getUrl(self,media_id):
        return 'http://streamin.to/%s' % (media_id)

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        sId = self.__getIdFromUrl(self.__sUrl)
        web_url = self.getUrl(sId)

        api_call =''

        oRequest = cRequestHandler(web_url)
        html = oRequest.request()

        # get stream url
        try:
            api_call = re.compile("file\s*:\s*[\'|\"](http.+?)[\'|\"]").findall(html)[0]
            r = urllib2.Request(stream_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'})
            r = urllib2.urlopen(r, timeout=15).headers['Content-Length']
        except:
            pass

        if api_call == '':
            try:
                streamer = re.search('streamer:\s*"([^"]+)",', html).group(1).replace(':1935', '')
                playpath = re.search('file:\s*"([^"]+)",', html).group(1).replace('.flv', '')
                api_call = streamer + ' playpath=' + playpath
            except:
                pass
            
        if (api_call):
            return True, api_call
            
        return False, False
 
