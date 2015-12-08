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

        # ouais je sais mais c'est pour pas oublier
        if (False):
            post_url = web_url

            # get post vars
            form_values = {}
            for i in re.finditer('<input.*?name="(.*?)".*?value="(.*?)">', html):
                form_values[i.group(1)] = i.group(2)

            xbmc.sleep(5000)

            data = urllib.urlencode(form_values) 
            request = urllib2.Request(post_url,data,None)

            try: 
                reponse = urllib2.urlopen(request)
            except URLError, e:
                print e.read()
                print e.reason

            html = reponse.read()

        # get stream url
        pattern = 'streamer:\s*"([^"]+)",'
        file = 'file:\s*"([^"]+)",'
        r = re.search(pattern, html)
        rr = re.search(file, html)
        if r:
            api_call = r.group(1).replace(':1935','') + ' swfUrl=http://streamin.to/player/player.swf live=false swfVfy=1 playpath=' + rr.group(1).replace('.flv','')
        else:
            api_call = rr.group(1)
            
        if (api_call):
            return True, api_call
            
        return False, False
 
