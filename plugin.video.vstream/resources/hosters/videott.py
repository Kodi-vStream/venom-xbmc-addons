from resources.lib.handler.requestHandler import cRequestHandler
#from t0mm0.common.net import Net
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import urllib, urllib2,re
import xbmcgui

try:    import json
except: import simplejson as json

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'VideoTT'
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
        return 'videott'

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
        sPattern = 'http:..(?:www.)*video.tt\/e(?:mbed)*\/([^<]+)'
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
        sId = self.__getIdFromUrl(self.__sUrl)
        
        json_url = 'http://www.video.tt/player_control/settings.php?v=%s' % sId
        
        vUrl = False
        
        try:
            print 'debut2'

            reponse = urllib2.urlopen(json_url)
            
            data = json.loads(reponse.read().decode(reponse.info().getparam('charset') or 'utf-8'))

            vids = data['settings']['res']

            if vids:
                
                vUrlsCount = len(vids)

                if (vUrlsCount > 0):
                    if vUrlsCount == 1:
                        vUrl = vids[0][u'u'].decode('base-64')
                    else:
                        vid_list = []
                        url_list = []
                        
                        for index in vids:
                            quality = index[u'l']
                            vid_list.extend(['Video TT - %sp' % quality])
                            url_list.extend([index[u'u']])
                            
                        result = xbmcgui.Dialog().select('Choose a link', vid_list)
                        if result != -1:
                            vUrl = url_list[result].decode('base-64')

        except urllib2.URLError, e:
            print e.read()
            print e.reason
        except Exception, e:
            print e.read()
            print e.reason

        
        if (vUrl):
            api_call = vUrl
            return True, api_call
            
        return False, False
        
