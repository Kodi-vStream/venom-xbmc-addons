#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#test film strem vk 1er page dark higlands & tous ces enfants m'appartiennent
import re

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:72.0) Gecko/20100101 Firefox/72.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'netu', 'Netu')

    def setUrl(self, url):
        self._url = url.replace('https', 'http')
        self._url = self._url.replace('http://netu.tv/', 'http://hqq.tv/')
        self._url = self._url.replace('http://waaw.tv/', 'http://hqq.tv/')
        self._url = self._url.replace('http://vizplay.icu/', 'http://hqq.tv/')
        self._url = self._url.replace('http://hqq.tv/player/hash.php?hash=',
            'http://hqq.tv/player/embed_player.php?vid=')
        self._url = self._url.replace('http://hqq.tv/watch_video.php?v=', 'http://hqq.tv/player/embed_player.php?vid=')

    def __getIdFromUrl(self):
        sPattern = 'https*:\/\/hqq\.(?:tv|player|watch)\/player\/embed_player\.php\?vid=([0-9A-Za-z]+)'
        oParser = cParser()
        aResult = oParser.parse(self._url, sPattern)

        if aResult[0] is True:
            return aResult[1][0]
        return ''

    def isDownloadable(self):
        return False

    def _getMediaLinkForGuest(self):
        api_call = ''

        ids = self.__getIdFromUrl()

        hqqUrl = 'http://hqq.tv/player/embed_player.php?vid=' + ids + '&autoplay=no'

        oRequestHandler = cRequestHandler(hqqUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        html = oRequestHandler.request()

        vid = re.search("videokeyorig *= *\'(.+?)\'", html, re.DOTALL).group(1)

        url = "time=1&ver=0&secure=0&adb=0%2F&v={}&token=&gt=&embed_from=0&wasmcheck=1".format(vid)

        oRequestHandler = cRequestHandler('https://hqq.tv/player/get_md5.php?' + url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Accept', '*/*')
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('Referer', hqqUrl)
        #ok

        oRequestHandler.request()
        api_call = oRequestHandler.getRealUrl()

        if api_call:
            return True, api_call + '.mp4.m3u8' + '|User-Agent=' + UA

        return False, False
