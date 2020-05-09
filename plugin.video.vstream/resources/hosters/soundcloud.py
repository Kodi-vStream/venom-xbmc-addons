#-*- coding: utf-8 -*-
#https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog#, dialog

try:
    import json
except:
    import simplejson as json

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Soundcloud'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'soundcloud'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self):
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
        
        url2 = ''

        VSlog(self.__sUrl)

        oRequest = cRequestHandler(self.__sUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()

        oParser = cParser()
        
        #Magic number
        sPattern =  'soundcloud:\/\/sounds:([0-9]+)">'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            n = aResult[1][0]
        else:
            VSlog('err magic number')
            return False
        
        #First need client id
        sPattern =  '<script crossorigin src="([^"]+)"><\/script>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for i in aResult[1]:
                #Bon evidement la jai pris "48-" mais ca change surement
                if '48-' in i:
                    url2 = i
                    break
        else:
            VSlog('err id1')
            return False
            
        if not url2:
            VSlog('err url2')
            return False
            
        oRequest = cRequestHandler(url2)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()

        sPattern =  'client_id:"([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sId = aResult[1][0]
        else:
            VSlog('err id2')
            return False

        #Need track
        TrackUrl = 'https://api-v2.soundcloud.com/tracks?ids=' + n +' &client_id=' + sId
        oRequest = cRequestHandler(TrackUrl)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()
        sPattern = 'soundcloud:tracks:([^"]+\/)stream'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sTrack = aResult[1][0]
        else:
            VSlog('err tracks')
            return False
            
        jsonurl = 'https://api-v2.soundcloud.com/media/soundcloud:tracks:' + sTrack + 'stream/hls?client_id=' + sId
        VSlog(jsonurl)
        
        oRequest = cRequestHandler(jsonurl)
        oRequest.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequest.request()

        #fh = open('c:\\test.txt', 'w')
        #fh.write(sHtmlContent)
        #fh.close()

        json_string = json.loads(sHtmlContent)
        api_call = json_string['url']

        if (api_call):
            return True, api_call + '|User-Agent=' + UA

        return False, False
