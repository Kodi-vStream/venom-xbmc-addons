# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
# Code from https://github.com/movieshark/waaw
#

import re

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import urlEncode, Quote
from resources.lib.comaddon import dialog, VSlog

import codecs

from base64 import b64decode
from random import choice

from resources.lib.waaw import captcha_window

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'

def decrypt(strid):
    strid = strid[1:]
    j = 0
    s2 = ''
    while j < len(strid):
        s2 += '\\u0' + strid[j:(j + 3)]
        j += 3
    s2 = codecs.decode(s2, encoding='unicode-escape')
    return s2

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'netu', 'Netu')

    def __getHost(self, url):
        parts = url.split('//', 1)
        host = parts[0] + '//' + parts[1].split('/', 1)[0]
        return host

    def setUrl(self, url):
        host = self.__getHost(url)

        if '&autoplay=' in url:
            url=url.split('&')[:-1][0]
        
        if '=' in url:
            id  = url.split('=')[-1]
        else:
            id  = url.split('/')[-1]

        self._url = host + '/e/' + id

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
        
        #VSlog(self._url)
        api_call = ''
        
        oRequestHandler = cRequestHandler(self._url)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9')
        sHtmlContent = oRequestHandler.request()

        videoid = videokey = adbn = ''
        oParser = cParser()
        
        sPattern = "'videoid':\s*'([^']+)"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            videoid = aResult[1][0]
            
        sPattern = "'videokey':\s*'([^']+)"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            videokey = aResult[1][0]

        sPattern = "adbn\s*=\s*'([^']+)"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            adbn = aResult[1][0]

        if videoid and videokey and adbn:
            url2 = self.__getHost(self._url) + '/player/get_player_image.php'

            oRequestHandler = cRequestHandler(url2)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', self._url)
            oRequestHandler.addHeaderEntry('Origin', self.__getHost(self._url))
            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('Accept', 'application/json')
            oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9')

            oRequestHandler.addJSONEntry('videoid', videoid)
            oRequestHandler.addJSONEntry('videokey', videokey)
            oRequestHandler.addJSONEntry('width', 400)
            oRequestHandler.addJSONEntry('height', 400)
            
            oRequestHandler.setRequestType(1)
            _json = oRequestHandler.request(jsonDecode=True)

            if _json['success'] == True:
                hash_image = _json['hash_image']
                image = _json['image'].replace('data:image/jpeg;base64,', '')
                image = b64decode(image + "==")
                
            window = captcha_window.CaptchaWindow(image, 400, 400)
            window.doModal()

            if window.finished:
            
                x = window.solution_x
                y = window.solution_y
                
                url3 = self.__getHost(self._url) + '/player/get_md5.php'
                oRequestHandler = cRequestHandler(url3)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('accept', 'application/json, text/javascript, */*; q=0.01')
                oRequestHandler.addHeaderEntry('Referer', self._url)
                oRequestHandler.addHeaderEntry('Origin', self.__getHost(self._url))
                oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
                oRequestHandler.addHeaderEntry('accept-language', 'en-US,en;q=0.9')

                oRequestHandler.addJSONEntry('adb', adbn)
                oRequestHandler.addJSONEntry('sh', ''.join([choice('0123456789abcdef') for x in range(40)]))
                oRequestHandler.addJSONEntry('ver', '4')
                oRequestHandler.addJSONEntry('secure', '0')
                oRequestHandler.addJSONEntry('htoken', '')
                oRequestHandler.addJSONEntry('v', videokey)
                oRequestHandler.addJSONEntry('token', '')
                oRequestHandler.addJSONEntry('gt', '')
                oRequestHandler.addJSONEntry('embed_from', '0')
                oRequestHandler.addJSONEntry('wasmcheck', 1)
                oRequestHandler.addJSONEntry('adscore', '')
                oRequestHandler.addJSONEntry('click_hash', Quote(hash_image))
                oRequestHandler.addJSONEntry('clickx', x)
                oRequestHandler.addJSONEntry('clicky', y)

                oRequestHandler.setRequestType(1)
                _json = oRequestHandler.request(jsonDecode=True)
                
                if 'try_again' in _json and _json['try_again'] == '1':
                    VSlog("NETU : Captcha a refaire")
                    if dialog().VSyesno("La sélection n'est pas valide. Recommencer ?"):
                        return self._getMediaLinkForGuest()

                
                link = ''
                if 'obf_link' in _json and _json['obf_link'] != '#':
                    api_call = "https:" + decrypt(_json['obf_link']) + '.mp4.m3u8'

        if api_call:
            headers4 = {'user-agent': UA,
                        #'accept': '*/*',
                        'Referer': self._url,
                        'Origin': self.__getHost(self._url)
                        #'accept-language': 'en-US,en;q=0.9'
                        }
            return True, api_call + '|' + urlEncode(headers4)

        return False, False
