# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# type
# https://www.youtube.com/embed/etc....
# https://www.youtube.com/watch?v=etc...
# http://www.youtube-nocookie.com/v/etc...
# https://youtu.be/etc...

import time
import xbmcaddon

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'youtube', 'Youtube')

    def _getMediaLinkForGuest(self):
        
        # 0 = site yt1s
        # 1 = Plugin Youtube
        MODE = 1
        
        api_call = ''
        
        if MODE == 1 and not xbmcaddon.Addon('plugin.video.youtube'):
            VSlog('Plugin Youtube non installe')
            MODE = 0
        
        if MODE == 0:
            api_call = self._getMediaLinkForGuest0(self._url)
        elif MODE == 1:
            if 'plugin' in self._url:
                api_call = self._url
            else:
                videoID = self.__getIdFromUrl(self._url)
                api_call = 'plugin://plugin.video.youtube/play/?video_id=' + videoID
        
        if api_call:
            return True, api_call
        else:
            return False, False

    def __getIdFromUrl(self, sUrl):

        if 'plugin' not in sUrl:
            id = sUrl
            id = id.replace('http:', '')
            id = id.replace('https:', '')
            id = id.replace('//', '')
            id = id.replace('www.youtube.com', '')
            id = id.replace('www.youtube-nocookie.com', '')
            id = id.replace('/embed/', '')
            id = id.replace('?feature=oembed', '')
            id = id.replace('/watch?v=', '')
            id = str(id)
        else:
            id = sUrl
 
        return id

    def _getMediaLinkForGuest0(self, sUrl):
        UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' + \
            'Chrome/53.0.2785.143 Safari/537.36'

        oRequestHandler = cRequestHandler("https://yt1s.com/api/ajaxSearch/index")
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('Origin', 'https://yt1s.com')
        oRequestHandler.addHeaderEntry('Referer', 'https://yt1s.com/fr13')
        oRequestHandler.addParameters("q", sUrl)
        oRequestHandler.addParameters("vt", "home")
        sHtmlContent = oRequestHandler.request(jsonDecode=True)

        oRequestHandler = cRequestHandler("https://yt1s.com/api/ajaxConvert/convert")
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry('Origin', 'https://yt1s.com')
        oRequestHandler.addHeaderEntry('Referer', 'https://yt1s.com/fr13')
        oRequestHandler.addParameters("vid", sUrl.split("v=")[1])
        oRequestHandler.addParameters("k", sHtmlContent['links']["mp4"]["auto"]["k"])
        try:
            api_call = oRequestHandler.request(jsonDecode=True)['dlink']
        except:
            time.sleep(3)
            oRequestHandler = cRequestHandler("https://yt1s.com/api/ajaxConvert/convert")
            oRequestHandler.setRequestType(1)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
            oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            oRequestHandler.addHeaderEntry('Origin', 'https://yt1s.com')
            oRequestHandler.addHeaderEntry('Referer', 'https://yt1s.com/fr13')
            oRequestHandler.addParameters("vid", sUrl.split("v=")[1])
            oRequestHandler.addParameters("k", sHtmlContent['links']["mp4"]["auto"]["k"])
            api_call = oRequestHandler.request(jsonDecode=True)['dlink']

        return api_call
