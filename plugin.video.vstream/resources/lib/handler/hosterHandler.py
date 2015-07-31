from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler

class cHosterHandler:

    def getUrl(self, oHoster):
        sUrl = oHoster.getUrl()
        cConfig().log("hosterhandler " + sUrl)
        if (oHoster.checkUrl(sUrl)):
            oRequest = cRequestHandler(sUrl)            
            sContent = oRequest.request()
            
            aMediaLink = cParser().parse(sContent, oHoster.getPattern())           
            if (aMediaLink[0] == True):               
                return True, aMediaLink[1][0]
        return False, ''

    def getHoster(self, sHosterFileName):
        exec "from resources.hosters." + sHosterFileName + " import cHoster"

        return cHoster()
    