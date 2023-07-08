# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
from resources.lib.util import Unquote


class iHoster:

    def __init__(self, pluginIdentifier, displayName, color='skyblue'):
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

    def getMediaLink(self, autoPlay = False):
        return self._getMediaLinkForGuest(autoPlay)

    # nom du fichier, interessant pour afficher la release
    def getMediaFile(self):
        if not self._url:
            return None
        if self._url[-4:] not in '.mkv.avi.mp4.m4v.iso':
            return None

        sMediaFile = self._url[:-4]
        sMediaFile = Unquote(sMediaFile.split('/')[-1])
        sMediaFile = re.sub('TM\d+TM', '', sMediaFile)
        sMediaFile = re.sub('RES-.+?-RES', '', sMediaFile)
        sMediaFile = sMediaFile.replace('.', ' ')
        sMediaFile = sMediaFile.replace('_', ' ')
        return sMediaFile

    def _getMediaLinkForGuest(self, autoPlay = False):
        raise NotImplementedError()

    def _getMediaLinkByPremiumUser(self, autoPlay = False):
        pass
