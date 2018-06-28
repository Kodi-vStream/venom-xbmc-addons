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

    def getDialogQual(self, list_qual, list_url):
        from resources.lib.comaddon import addon, dialog

        if len(list_url) == 0:
            return ''
        if len(list_url) == 1:
            return list_url[0]
        
        ret = dialog().VSselect(list_qual, addon().VSlang(30448))
        if ret > -1:
            return list_url[ret]
        return ''
