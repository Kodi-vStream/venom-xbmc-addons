#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

class iHoster:

    def __init__(self, pluginIdentifier, displayName, color = 'skyblue'):
        self._defaultDisplayName = displayName
        self._displayName = self._defaultDisplayName
        self._fileName = displayName
        self._pluginIdentifier = pluginIdentifier
        self.color = color
        self._url = None

    def getPluginIdentifier(self):
        return self._pluginIdentifier

    def setFileName(self, fileName):
        self._fileName = fileName

    def getFileName(self):
        return self._fileName

    def getDisplayName(self):
        return self._displayName

    def setDisplayName(self, displayName):
        self._displayName = displayName + ' [COLOR ' + self.color + ']' + self._defaultDisplayName + '[/COLOR]'

    def isDownloadable(self):
        return True

    def setUrl(self, url):
        self._url = str(url)

    def getUrl(self):
        return self._url

    def getMediaLink(self):
        return self._getMediaLinkForGuest()

    def _getMediaLinkForGuest(self):
        raise NotImplementedError()

    def _getMediaLinkByPremiumUser(self):
        pass
