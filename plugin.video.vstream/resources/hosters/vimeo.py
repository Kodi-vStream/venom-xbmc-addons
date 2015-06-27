from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import re,urllib2
import xbmcgui
import json

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Vimeo'
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
        return 'vimeo'

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
        sPattern = 'https*:\/\/(?:.+)?vimeo\.com\/(?:video\/)?([0-9]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
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

        api_call = ''
    
        id = self.__getIdFromUrl(self.__sUrl)

        if id:
            vid_sel = ''
            
            web_url = 'https://player.vimeo.com/video/' + id + '/config?autoplay=0&byline=0&bypass_privacy=1&context=clip.main&default_to_hd=1&portrait=0&title=0'
            
            #https://player.vimeo.com/video/131759737/config?autoplay=0&byline=0&bypass_privacy=1&context=clip.main&default_to_hd=1&portrait=0&title=0&s=141e12c8893bf681900e198a59c42394af6e02f0
            #http://player.vimeo.com/v2/video/131759737/config?type=moogaloop&referrer=&player_url=player.vimeo.com&v=1.0.0&cdn_url=http://a.vimeocdn.com        

            headers = {'Referer': web_url}
            
            request = urllib2.Request(web_url,None,headers)
                
            try: 
                reponse = urllib2.urlopen(request)
            except URLError, e:
                print e.read()
                print e.reason
  
            resp = reponse.read()
            data = json.loads(resp)
            
            if data:
                vid_list = []
                url_list = []
                best = 0
                quality = 0
                
                h264 = data["request"]["files"]["h264"]

                for quality in h264.iterkeys():
                    vid_list.extend(['[ %s ]' % quality])
                    url_list.extend([ h264[quality]['url'] ])
                
                if len(vid_list) == 1: vid_sel = videos[0]
                else:
                    result = xbmcgui.Dialog().select('Choose a link', vid_list)
                    if result != -1:
                        vid_sel = url_list[result]
                        
            if vid_sel:
                api_call = vid_sel
                
        
        #print api_call

        if (api_call):
            return True, api_call
            
        return False, False
