from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
from resources.hosters.hoster import iHoster
import time
import random

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Duckload.com'
	self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName

    def setFileName(self, sFileName):
	self.__sFileName = sFileName

    def getFileName(self):
	return self.__sFileName

    def getPluginIdentifier(self):
        return 'duckload'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ""

    def setUrl(self, sUrl):
        self.__sUrl = sUrl.replace('/divx/', '/play/').replace('.html', '')

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        oPremiumHandler = cPremiumHandler(self.getPluginIdentifier())
        if (oPremiumHandler.isPremiumModeAvailable()):
            sUsername = oPremiumHandler.getUsername()
            sPassword = oPremiumHandler.getPassword()
            return self.__getMediaLinkByPremiumUser(sUsername, sPassword);

        return self.__getMediaLinkForGuest();

    def __getMediaLinkByPremiumUser(self, sUsername, sPassword):
        oRequestHandler = cRequestHandler('http://www.duckload.com/api/public/login&user=' + sUsername + '&pw=' + sPassword + '&fmt=json&source=WEB')
        sHtmlContent = oRequestHandler.request()

        aHeader = oRequestHandler.getResponseHeader()
        sReponseCookie = aHeader.getheader("Set-Cookie")

        oRequestHandler = cRequestHandler(self.__sUrl)
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParameters('stream', '')
        oRequestHandler.addHeaderEntry('Cookie', sReponseCookie)
        sHtmlContent = oRequestHandler.request()
        
        sPattern = '<param name="src" value="([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
       
        if (aResult[0] == True):
            return True, aResult[1][0]

        return False, aResult

    def __getMediaLinkForGuest(self):
        sSecondsForWait = 10

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        aHeader = oRequest.getResponseHeader()
        sPhpSessionId = self.__getPhpSessionId(aHeader)
        
        sPostName = '';
        sPostValue = '';
        sPostButtonName = ""
        sPattern = '<form onsubmit="return checkTimer.*?<input type="hidden" name="([^"]+)" value="([^"]+)".*?<button name="([^"]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sPostName = aEntry[0]
                sPostValue = aEntry[1]
                sPostButtonName = aEntry[2]        

        sPattern = 'var tick.*?=(.*?);'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
                sTicketValue = str(aResult[1][0]).replace(' ', '');
                sSecondsForWait = int(sTicketValue) + 2

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

                sCookieValue = sPhpSessionId +'; '
		sCookieValue = sCookieValue + '__utma=' + str(rndY) + '.' + str(rndX) + '.' + str(ts1) + '.' + str(ts2) + '.' + str(ts3) + '; '
                sCookieValue = sCookieValue + '__utmb=' + str(rndY) + '.1.10.' + str(ts3) + '; '
                sCookieValue = sCookieValue + '__utmc=' + str(rndY) + "; "
                sCookieValue = sCookieValue + '__utmz=' + str(rndY) + '.' + str(ts4) + '.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); '
                
                oRequest = cRequestHandler(self.__sUrl)
                oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
                oRequest.addHeaderEntry('Cookie', sCookieValue)
                oRequest.addParameters(sPostName, sPostValue)
                oRequest.addParameters(sPostButtonName, '')

		sHtmlContent = oRequest.request()

		sPattern = '<param name="src" value="([^"]+)"'
                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern)

                if (aResult[0] == True):
                    return True, aResult[1][0]

        return False, aResult

    def __getPhpSessionId(self, aHeader):       
        sReponseCookie = aHeader.getheader("Set-Cookie")       
	aResponseCookies = sReponseCookie.split(";")
        return aResponseCookies[0]
