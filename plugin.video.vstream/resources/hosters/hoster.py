#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

class iHoster:

    def getDisplayName(self):
        raise NotImplementedError()

    def setDisplayName(self, sDisplayName):
        raise NotImplementedError()

    def setFileName(self, sFileName):
        raise NotImplementedError()

    def getFileName(self):
        raise NotImplementedError()

    def getPluginIdentifier(self):
        raise NotImplementedError()

    def isDownloadable(self):
        raise NotImplementedError()

    def isJDownloaderable(self):
        raise NotImplementedError()

    def getPattern(self):
        raise NotImplementedError()

    def setUrl(self, sUrl):
        raise NotImplementedError()

    def checkUrl(self, sUrl):
        raise NotImplementedError()

    def getUrl(self):
        raise NotImplementedError()

    def getMediaLink(self):
        raise NotImplementedError()
