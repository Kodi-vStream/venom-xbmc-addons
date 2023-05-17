# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# type
# https://www.youtube.com/embed/etc....
# https://www.youtube.com/watch?v=etc...
# http://www.youtube-nocookie.com/v/etc...
# https://youtu.be/etc...

import time

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import VSlog

import xbmcaddon

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'youtube', 'Youtube')

    def _getMediaLinkForGuest(self):

        # 0 = Plugin invidious
        # 1 = Plugin Youtube

        MODE = 0

        api_call = ''

        try:
            xbmcaddon.Addon('plugin.video.invidious')
        except:
            VSlog('Plugin Invidious non installe')
            MODE = 1

        try:
            if (MODE == 1):
                xbmcaddon.Addon('plugin.video.youtube')
        except:
            VSlog('Plugin YouTube non installe')
            return False, False

        if 'plugin'  in self._url:
            api_call = self._url
        else:
            videoID = self.__getIdFromUrl(self._url)
            if MODE == 1:
                api_call = 'plugin://plugin.video.youtube/play/?video_id=' + videoID
            else:
                api_call = 'plugin://plugin.video.invidious/?action=play_video&video_id=' + videoID

        if api_call:
            return True, api_call
        else:
            return False, False

    def __getIdFromUrl(self, sUrl):
        id = ''
        if 'plugin' not in sUrl:
            id = sUrl
            id = id.replace('http:', '')
            id = id.replace('https:', '')
            id = id.replace('//', '')
            id = id.replace('www.youtube.com', '')
            id = id.replace('www.youtube-nocookie.com', '')
            id = id.replace('/embed/', '')
            id = id.replace('/watch?v=', '')
            id = str(id)
        else:
            id = sUrl
 
        return id
