from resources.lib.jsunpacker import cJsUnpacker
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import cUtil
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filebase', 'FileBase.to')

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        sPattern = '<form action="#" method="post">.*?id="uid" value="([^"]+)" />'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            sUid = aResult[1][0]

            oRequest = cRequestHandler(self._url)
            oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
            oRequest.addParameters('dl_free12','DivX Stream')
            oRequest.addParameters('uid', sUid)
            sHtmlContent = oRequest.request()

            sPattern = '<input type="hidden" id="uid" name="uid" value="([^"]+)" />'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)

            if aResult[0] is True:
                sUid = aResult[1][0]

                oRequest = cRequestHandler(self._url)
                oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
                oRequest.addParameters('captcha','ok')
                oRequest.addParameters('filetype','divx')
                oRequest.addParameters('submit','Download')
                oRequest.addParameters('uid', sUid)
                sHtmlContent = oRequest.request()

                sPattern = '<param value="([^"]+)" name="src" />'
                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern)

                if aResult[0] is True:
                    sMediaFile = aResult[1][0]
                    return True, sMediaFile

        return False, aResult

