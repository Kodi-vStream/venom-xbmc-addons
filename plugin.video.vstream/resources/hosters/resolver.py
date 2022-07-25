# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.hosters.hoster import iHoster
import urlresolver


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'resolver', 'RSLVR-')
        self.__sRealHost = '???'

    def setDisplayName(self, displayName):
        self._displayName = displayName + ' [COLOR violet]'+ self._defaultDisplayName + self.__sRealHost + '[/COLOR]'

    def setRealHost(self, sName):
        self.__sRealHost = sName

    def _getMediaLinkForGuest(self):
        hmf = urlresolver.HostedMediaFile(url=self._url)
        if hmf.valid_url():
            stream_url = hmf.resolve()
            if stream_url:
                return True, stream_url

        return False, False
