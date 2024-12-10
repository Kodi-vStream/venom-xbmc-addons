# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
from resources.lib.util import Unquote


class iHoster(object):

    def __init__(self, pluginIdentifier, displayName, color='skyblue'):
        self._defaultDisplayName = displayName
        self._displayName = self._defaultDisplayName
        self._fileName = displayName
        self._pluginIdentifier = pluginIdentifier
        self.__sRealHost = pluginIdentifier
        self.color = color
        self._res = None    # La résolution du lien
        self._url = None
        self._mediaFile = None
        self._mediaInfo = None

    def getPluginIdentifier(self):
        return self._pluginIdentifier

    # peut être différent lorsque surchargé par un debrideur
    def setRealHost(self, host):
        self.__sRealHost = host

    def getRealHost(self):
        return self.__sRealHost

    def setFileName(self, fileName):
        self._fileName = fileName

    def getFileName(self):
        return self._fileName

    def getDisplayName(self):
        return self._displayName

    def setDisplayName(self, displayName):
        self._displayName = displayName + ' [COLOR ' + self.color + ']' + self._defaultDisplayName + '[/COLOR]'

    def setMediaFile(self, mediaFile):
        self._mediaFile = mediaFile

    def isDownloadable(self):
        return True

    def setRes(self, res):
        self._res = res

    def getRes(self):
        return self._res

    def setUrl(self, url):
        if not url.startswith('http'):
            url = ('https://' + url).replace('////', '//')
        self._url = str(url)

    def getUrl(self):
        return self._url

    def getMediaLink(self):
        return self._getMediaLinkForGuest()

    # nom du fichier, interessant pour afficher la release
    def setMediaInfo(self, mediaInfo):
        self._mediaInfo = mediaInfo
        
    # nom du fichier, interessant pour afficher la release
    def getMediaFile(self):
        
        if self._mediaInfo:
            return self._mediaInfo

        mediaFile = self._mediaFile
        if not mediaFile: 
            mediaFile = self._url
            if not mediaFile:
                return None
        if mediaFile[-4:] not in '.mkv.avi.mp4.m4v.iso':
            return None
        
        sMediaFile = mediaFile[:-4]
        sMediaFile = Unquote(sMediaFile.split('/')[-1])
        sMediaFile = re.sub('TM\d+TM', '', sMediaFile)
        sMediaFile = re.sub('RES-.+?-RES', '', sMediaFile)
        sMediaFile = sMediaFile.replace('-', ' ')
        sMediaFile = sMediaFile.replace('.', ' ')
        sMediaFile = sMediaFile.replace('_', ' ')
        
        self._mediaInfo = sMediaFile
        
        return sMediaFile

    def _getMediaLinkForGuest(self):
        raise NotImplementedError()

    def _getMediaLinkByPremiumUser(self):
        pass

    def testPremium(self):
        return

