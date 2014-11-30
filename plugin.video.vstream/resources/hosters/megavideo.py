from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.util import cUtil
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
import re

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'MegaVideo.com'
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
        return 'megavideo'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ' errortext="(.+?)"'

    def setUrl(self, sUrl):
        self.__sUrl = str(self.__modifyUrl(sUrl))
        self.__sUrl = self.__sUrl.replace('http://www.megavideo.com/?v=', '')
        self.__sUrl = self.__sUrl.replace('http://megavideo.com/?v=', '')
        self.__sUrl = 'http://www.megavideo.com/?v=' + str(self.__sUrl)
                
    def __modifyUrl(self, sUrl):
        if (sUrl.startswith('http://www.megavideo.com/v/')):
            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.request()
            sRealUrl = oRequestHandler.getRealUrl()
            self.__sUrl = sRealUrl
            return self.__getIdFromUrl()

        return sUrl;

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

    def __getIdFromUrl(self):
        sPattern = "v=([^&]+)"
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def __getMediaLinkForGuest(self):
        sId = self.__getIdFromUrl()

        self.__sUrl = 'http://www.megavideo.com/xml/videolink.php?v=' + str(sId)

        oRequest = cRequestHandler(self.getUrl())
        oRequest.addHeaderEntry('Referer', 'http://www.megavideo.com/')
        sContent = oRequest.request()

        aResult = cParser().parse(sContent, self.getPattern())
        
        if (aResult[0] == False):
            s = re.compile(' s="(.+?)"').findall(sContent)
            k1 = re.compile(' k1="(.+?)"').findall(sContent)
            k2 = re.compile(' k2="(.+?)"').findall(sContent)
            un = re.compile(' un="(.+?)"').findall(sContent)

            sUrl = "http://www" + s[0] + ".megavideo.com/files/" + self.__decrypt(un[0], k1[0], k2[0]) + "/?.flv"

            aResult = []
            aResult.append(True)
            aResult.append(sUrl)
            return aResult

        aResult = []
        aResult.append(False)
        aResult.append('')
        return aResult


    def __getMediaLinkByPremiumUser(self, sUsername, sPassword):
        oRequestHandler = cRequestHandler('http://www.megavideo.com/?s=account')
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParameters('login', '1')
        oRequestHandler.addParameters('username', sUsername)
        oRequestHandler.addParameters('password', sPassword)
        oRequestHandler.request()
      
        aHeader = oRequestHandler.getResponseHeader();
        sReponseCookie = aHeader.getheader("Set-Cookie")

        self.__sUrl = self.__getIdFromUrl()
        
        sPattern = 'user=([^;]+);'
        oParser = cParser()
        aResult = oParser.parse(sReponseCookie, sPattern)
        if (aResult[0] == True):
            sUserId = aResult[1][0]
            sUrl = 'http://www.megavideo.com/xml/player_login.php?u=' + str(sUserId) + '&v=' + str(self.__sUrl)
            oRequestHandler = cRequestHandler(sUrl)
            sXmlContent = oRequestHandler.request()

            sPattern = 'downloadurl="([^"]+)"'
            oParser = cParser()
            aResult = oParser.parse(sXmlContent, sPattern)
            
            if (aResult[0] == True):
                sMediaLink = cUtil().urlDecode(str(aResult[1][0]))
                return True, sMediaLink

        return False, ''

    def __decrypt(self, str1, key1, key2):

	__reg1 = []
	__reg3 = 0
	while (__reg3 < len(str1)):
		__reg0 = str1[__reg3]
		holder = __reg0
		if (holder == "0"):
			__reg1.append("0000")
		else:
			if (__reg0 == "1"):
				__reg1.append("0001")
			else:
				if (__reg0 == "2"):
					__reg1.append("0010")
				else:
					if (__reg0 == "3"):
						__reg1.append("0011")
					else:
						if (__reg0 == "4"):
							__reg1.append("0100")
						else:
							if (__reg0 == "5"):
								__reg1.append("0101")
							else:
								if (__reg0 == "6"):
									__reg1.append("0110")
								else:
									if (__reg0 == "7"):
										__reg1.append("0111")
									else:
										if (__reg0 == "8"):
											__reg1.append("1000")
										else:
											if (__reg0 == "9"):
												__reg1.append("1001")
											else:
												if (__reg0 == "a"):
													__reg1.append("1010")
												else:
													if (__reg0 == "b"):
														__reg1.append("1011")
													else:
														if (__reg0 == "c"):
															__reg1.append("1100")
														else:
															if (__reg0 == "d"):
																__reg1.append("1101")
															else:
																if (__reg0 == "e"):
																	__reg1.append("1110")
																else:
																	if (__reg0 == "f"):
																		__reg1.append("1111")

		__reg3 = __reg3 + 1

	mtstr = self.__ajoin(__reg1)
	__reg1 = self.__asplit(mtstr)
	__reg6 = []
	__reg3 = 0
	while (__reg3 < 384):

		key1 = (int(key1) * 11 + 77213) % 81371
		key2 = (int(key2) * 17 + 92717) % 192811
		__reg6.append((int(key1) + int(key2)) % 128)
		__reg3 = __reg3 + 1

	__reg3 = 256
	while (__reg3 >= 0):

		__reg5 = __reg6[__reg3]
		__reg4 = __reg3 % 128
		__reg8 = __reg1[__reg5]
		__reg1[__reg5] = __reg1[__reg4]
		__reg1[__reg4] = __reg8
		__reg3 = __reg3 - 1

	__reg3 = 0
	while (__reg3 < 128):

		__reg1[__reg3] = int(__reg1[__reg3]) ^ int(__reg6[__reg3 + 256]) & 1
		__reg3 = __reg3 + 1

	__reg12 = self.__ajoin(__reg1)
	__reg7 = []
	__reg3 = 0
	while (__reg3 < len(__reg12)):

		__reg9 = __reg12[__reg3:__reg3 + 4]
		__reg7.append(__reg9)
		__reg3 = __reg3 + 4


	__reg2 = []
	__reg3 = 0
	while (__reg3 < len(__reg7)):
		__reg0 = __reg7[__reg3]
		holder2 = __reg0

		if (holder2 == "0000"):
			__reg2.append("0")
		else:
			if (__reg0 == "0001"):
				__reg2.append("1")
			else:
				if (__reg0 == "0010"):
					__reg2.append("2")
				else:
					if (__reg0 == "0011"):
						__reg2.append("3")
					else:
						if (__reg0 == "0100"):
							__reg2.append("4")
						else:
							if (__reg0 == "0101"):
								__reg2.append("5")
							else:
								if (__reg0 == "0110"):
									__reg2.append("6")
								else:
									if (__reg0 == "0111"):
										__reg2.append("7")
									else:
										if (__reg0 == "1000"):
											__reg2.append("8")
										else:
											if (__reg0 == "1001"):
												__reg2.append("9")
											else:
												if (__reg0 == "1010"):
													__reg2.append("a")
												else:
													if (__reg0 == "1011"):
														__reg2.append("b")
													else:
														if (__reg0 == "1100"):
															__reg2.append("c")
														else:
															if (__reg0 == "1101"):
																__reg2.append("d")
															else:
																if (__reg0 == "1110"):
																	__reg2.append("e")
																else:
																	if (__reg0 == "1111"):
																		__reg2.append("f")

		__reg3 = __reg3 + 1

	endstr = self.__ajoin(__reg2)
	return endstr

    def __ajoin(self, arr):
	strtest = ''
	for num in range(len(arr)):
		strtest = strtest + str(arr[num])
	return strtest

    def __asplit(self, mystring):
	arr = []
	for num in range(len(mystring)):
		arr.append(mystring[num])
	return arr