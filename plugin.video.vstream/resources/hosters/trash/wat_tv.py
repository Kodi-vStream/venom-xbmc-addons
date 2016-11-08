from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import re,urllib2
import xbmcgui
import md5,time

# ok >> http://2med.wat.tv/get/d4d32aa6402e3434fe328d1dae98f202/5679c3b0/2/H264-384x288/94/95/3729495.h264?bu=WAT&login=ai-yazawa&i=31.38.252.7&u=2a6410b4de355b415dfa41e542cb90f5&sum=eea9050289e876f2c90474e17b04e1bf&st=FbX5GqQMX5tW9IPj55LRdQ&e=1450950128&t=1450820528&seek=wat&start=0
#pas >> http://2med.wat.tv/get/fd810505ba48109f340a301b7bbf133b/5679c4e0/2/H264-384x288/98/49/3729849.h264?bu=&login=ai-yazawa&i=31.38.252.7&u=547bebc3a5d876cb2193f35dcc91b3e1&sum=b981923587ebbd1a88d2399d20882860&st=0Cb4kn2y3OdzmiXNvHFbQg&e=1450950432&t=1450820832&seek=wat&start=0

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Wat'
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
        return 'wat_tv'

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
        sPattern = 'http:\/\/www\.wat\.tv\/embedframe\/[0-9a-zA-Z]{13}([0-9a-zA-Z]{7})'
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
        
    def MakeToken(self,sLoc):
        
        def base36encode(number):
            if not isinstance(number, (int, long)):
                raise TypeError('number must be an integer')
            if number < 0:
                raise ValueError('number must be positive')
            alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            base36 = ''
            while number:
                number, i = divmod(number, 36)
                base36 = alphabet[i] + base36
            return base36 or alphabet[0]
            
        #oRequest = cRequestHandler('http://www.wat.tv/servertime2')
        #stime = oRequest.request()
        #stime = base36encode(int(stime))
            
        stime = base36encode(int(time.time()))

        timesec = hex(int(stime, 36))[2:]
        while(len(timesec)<8):
            timesec = "0" + timesec

        key = '9b673b13fa4682ed14c3cfa5af5310274b514c4133e9b3a81e6e3aba009l2564'
        token = md5.new(key + sLoc + timesec).hexdigest() + '/' + timesec
        return token

    def __getMediaLinkForGuest(self):
        
        print self.__sUrl
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        
        sID = self.__getIdFromUrl(self.__sUrl)
        sLocation = '/web/' + sID
        
        #sUrl1 = 'http://www.wat.tv/interface/contentv3/' + sID
        #oRequest = cRequestHandler(sUrl1)
        #Json1 = oRequest.request()
        
        sToken = self.MakeToken(sLocation)

        sUrl2 = 'http://www.wat.tv/get' + sLocation + '?token=' + sToken + '&context=swf2&getURL=1&version=WIN%2010,3,181,14'
        #print sUrl2
        
        oRequest = cRequestHandler(sUrl2)
        oRequest.addHeaderEntry('User-Agent', UA)
        url3 = oRequest.request()
        
        api_call = url3 + '&start=0|User-Agent=' + UA

        #print api_call
        
        if (api_call):
            return True, api_call
            
        return False, False
