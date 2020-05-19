# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import requests

from resources.hosters.hoster import iHoster


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Allow_redirects'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'allow_redirects'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getIdFromUrl(self):
        return ''

    def __modifyUrl(self, sUrl):
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = sUrl

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        url = self.__sUrl

        session = requests.Session()  # so connections are recycled
        resp = session.head(url, allow_redirects=True)
        sHosterUrl = resp.url

        if sHosterUrl:

            from resources.lib.gui.hoster import cHosterGui

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            oHoster.setUrl(sHosterUrl)
            api_call = oHoster.getMediaLink()

            if (api_call[0] == True):
                return True, api_call[1]

        else:
            return False, False

        return False, False
