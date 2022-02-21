from resources.lib.jsunpacker import cJsUnpacker
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'dankfile', 'DankFile.com')

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        return self.__getUrlFromJavascriptCode(sHtmlContent)

    def __getUrlFromJavascriptCode(self, sHtmlContent):
        sPattern = "<script type='text/javascript'>eval.*?return p}\((.*?)</script>"
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            sJavascript = aResult[1][0]

            sUnpacked = cJsUnpacker().unpackByString(sJavascript)
            sPattern = ".addVariable\('file','([^']+)'"
            oParser = cParser()
            aResultLink = oParser.parse(sUnpacked, sPattern)

            if aResultLink[0] is True:
                aResult = []
                aResult.append(True)
                aResult.append(aResultLink[1][0])
                return aResult

        return False, ''

