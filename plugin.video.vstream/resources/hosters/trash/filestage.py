from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.util import cUtil
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'filestage', 'FileStage.to')

    def getPattern(self):
        return 's1.addVariable\("file".*?"([^"]+)"'

    def _getMediaLinkForGuest(self):
        oHosterHandler = cHosterHandler()
        aResult = oHosterHandler.getUrl(self)
        if aResult[0] is True:
            return True, cUtil().urlDecode(aResult[1])

        return False, ''
