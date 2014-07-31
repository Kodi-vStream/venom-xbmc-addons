import re
import urllib
import xbmc
import xbmcgui

class cUtil:

    def removeHtmlTags(self, sValue, sReplace = ''):
        p = re.compile(r'<.*?>')
        return p.sub(sReplace, sValue)


    def formatTime(self, iSeconds):
        iSeconds = int(iSeconds)

        iMinutes = int(iSeconds / 60)
        iSeconds = iSeconds - (iMinutes * 60)
        if (iSeconds < 10):
            iSeconds = '0' + str(iSeconds)

        if (iMinutes < 10):
            iMinutes = '0' + str(iMinutes)

        return str(iMinutes) + ':' + str(iSeconds)

    def urlDecode(self, sUrl):
        return urllib.unquote(sUrl)

    def urlEncode(self, sUrl):
        return urllib.quote(sUrl)

    def unquotePlus(self, sUrl):
        return urllib.unquote_plus(sUrl)

    def quotePlus(self, sUrl):
        return urllib.quote_plus(sUrl)
        
    def dialog(self, sName):
        oDialog = xbmcgui.DialogProgress()
        oDialog.create(sName)
        return oDialog
