import time
import random

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'fullshare', 'FullShare.net')

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        aHeader = oRequest.getResponseHeader()
        sPhpSessionId = self.__getPhpSessionId(aHeader)

        sPattern = 'var time_wait = ([^;]+);'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            sSecondsForWait = int(aResult[1][0]) + 2

            sPattern = '<input type="hidden" name="code" value="([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                sCode = aResult[1][0]

                oGui = cGui()
                oGui.showNofication(sSecondsForWait, 3)
                time.sleep(sSecondsForWait)

                rndX = random.randint(1, 99999999-10000000)+10000000
                rndY = random.randint(1, 999999999-100001000)+100000000
                ts1 = float(time.time())
                ts2 = float(time.time())
                ts3 = float(time.time())
                ts4 = float(time.time())
                ts5 = float(time.time())

                sCookieValue = '__utma=' + str(rndY) + '.' + str(rndX) + '.' + str(ts1) + '.' + str(ts2) + '.' + \
                    str(ts3) + '; '
                sCookieValue = sCookieValue + '__utmz=' + str(rndY) + '.' + str(ts4) + \
                    '.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); '
                sCookieValue = sCookieValue + sPhpSessionId +'; '
                sCookieValue = sCookieValue + '__utmc=' + str(rndY) + "; "
                sCookieValue = sCookieValue + '__utmb=' + str(rndY) + '.7.10.' +  str(ts5) + "; ADBLOCK=1"

                oRequest = cRequestHandler(self._url)
                oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
                oRequest.addHeaderEntry('Cookie', sCookieValue)
                oRequest.addParameters('code', sCode)
                sHtmlContent = oRequest.request()

                sPattern = '<param name="src" value="([^"]+)"'
                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern)

                if aResult[0] is True:
                    return True, aResult[1][0]

        return False, aResult


    def __getPhpSessionId(self, aHeader):
        sReponseCookie = aHeader.getheader("Set-Cookie")
        aResponseCookies = sReponseCookie.split(";")
        return aResponseCookies[0]
