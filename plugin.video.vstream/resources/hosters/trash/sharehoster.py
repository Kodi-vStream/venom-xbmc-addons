from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
import time
import random

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'sharehoster', 'ShareHoster.com')

    def _getMediaLinkForGuest(self):
        aSplit = self._url.split('/')
        sId = aSplit[-1]

        sUrl = 'http://www.sharehoster.com/flowplayer/config.php?movie=' + sId

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = "playlist': \[.*?},.*?'url': '(.*?)'"
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            sFileName = aResult[1][0]
            return True, sFileName

        return False, ''
