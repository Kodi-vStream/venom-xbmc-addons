#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#test film strem vk 1er page dark higlands & tous ces enfants m'appartiennent
from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
import re

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:72.0) Gecko/20100101 Firefox/72.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Netu'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def setUrl(self, sUrl):
        self.__sUrl = sUrl.replace('https', 'http')
        self.__sUrl = self.__sUrl.replace('http://netu.tv/', 'http://hqq.tv/')
        self.__sUrl = self.__sUrl.replace('http://waaw.tv/', 'http://hqq.tv/')
        self.__sUrl = self.__sUrl.replace('http://vizplay.icu/', 'http://hqq.tv/')
        self.__sUrl = self.__sUrl.replace('http://hqq.tv/player/hash.php?hash=', 'http://hqq.tv/player/embed_player.php?vid=')
        self.__sUrl = self.__sUrl.replace('http://hqq.tv/watch_video.php?v=', 'http://hqq.tv/player/embed_player.php?vid=')

    def __getIdFromUrl(self):
        sPattern = 'https*:\/\/hqq\.(?:tv|player|watch)\/player\/embed_player\.php\?vid=([0-9A-Za-z]+)'
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)

        if (aResult[0] == True):
            return aResult[1][0]
        return ''

    def getPluginIdentifier(self):
        return 'netu'

    def isDownloadable(self):
        return False

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def GetHost(self,sUrl):
        oParser = cParser()
        sPattern = 'https*:\/\/(.+?)\/'
        aResult = oParser.parse(sUrl, sPattern)
        if aResult[0]:
            return aResult[1][0]
        return ''

    def __getMediaLinkForGuest(self):

        api_call = ''

        ids = self.__getIdFromUrl()

        self.__sUrl = 'http://hqq.tv/player/embed_player.php?vid=' + ids + '&autoplay=no'


        oRequestHandler = cRequestHandler(self.__sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        html = oRequestHandler.request()

        vid = re.search("videokeyorig *= *\'(.+?)\'", html, re.DOTALL).group(1)

        url = "time=1&ver=0&secure=0&adb=0%2F&v={}&token=&gt=&embed_from=0&wasmcheck=1".format(vid)

        oRequestHandler = cRequestHandler('https://hqq.tv/player/get_md5.php?' + url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Accept', '*/*')
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('Referer', self.__sUrl)
        #ok

        oRequestHandler.request()
        api_call = oRequestHandler.getRealUrl()

        if (api_call):
            return True, api_call + '.mp4.m3u8' + '|User-Agent=' + UA

        return False, False
