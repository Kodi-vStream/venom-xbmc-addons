#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'pixsil', 'Pixsil')

    def _getMediaLinkForGuest(self):
        api_call = self._url
        api_call = api_call + '|Referer=http://www.mangacity.org/jwplayer/player.swf'

        if api_call:
            return True, api_call

        return False, False
