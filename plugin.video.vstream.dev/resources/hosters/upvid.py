#-*- coding: utf-8 -*-
#https://upvid.co/embed-xxx.html
#https://upvid.co/xxx.html
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.aadecode import AADecoder
import base64, re
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
sPattern1 = '<iframe id="iframe" src="([^"]+)"'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'UpVid'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'upvid'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        #lien embed obligatoire
        if not 'embed-' in self.__sUrl:
            self.__sUrl = self.__sUrl.rsplit('/', 1)[0] + '/embed-' + self.__sUrl.rsplit('/', 1)[1]

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()


    def __getMediaLinkForGuest(self):
        api_call = ''
        oParser = cParser()

        oRequest = cRequestHandler(self.__sUrl)
        sHtmlContent = oRequest.request()

        aResult = oParser.parse(sHtmlContent, sPattern1)
        if (aResult[0] == True):
            sUrl = aResult[1][0]

            oRequest = cRequestHandler(sUrl)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Referer', self.__sUrl)
            sHtmlContent = oRequest.request()

            aResult = oParser.parse(sHtmlContent, sPattern1)
            if (aResult[0] == True):
                sUrl2 = aResult[1][0]

                oRequest = cRequestHandler(sUrl2)
                oRequest.addHeaderEntry('User-Agent', UA)
                oRequest.addHeaderEntry('Referer', sUrl)
                sHtmlContent = oRequest.request()
                sHtmlContent = sHtmlContent.replace('\n', '')

                aResult = re.search('id="code".+?value="(.+?)"', sHtmlContent, re.DOTALL)
                if (aResult):
                    sFunc = base64.b64decode(aResult.group(1))

                aResult = re.search('(ﾟωﾟ.+?\(\'_\'\);)', sHtmlContent, re.DOTALL | re.UNICODE)
                if (aResult):
                    sHtmlContent = AADecoder(aResult.group(1)).decode()
                    if sHtmlContent:
                        aResult = re.search("func.innerHTML.+?\('(.+?)',", sHtmlContent, re.DOTALL)
                        if (aResult):
                            chars = aResult.group(1)
                            final = sDecode(chars, sFunc)
                            sPattern = "source\.setAttribute\('src', '([^']+)'\)"
                            aResult = oParser.parse(final, sPattern)
                            if (aResult[0] == True):
                                api_call = aResult[1][0]

        if (api_call):
            return True, api_call

        return False, False

def sDecode(r, o):
    t = []
    e = []
    n = 0
    a = ""
    for f in range(256):
        e.append(f)

    for f in range(256):
        n = (n + e[f] + ord(r[f % len(r)])) % 256
        t = e[f]
        e[f] = e[n]
        e[n] = t

    f = 0
    n = 0
    for h in range(len(o)):
        f = f + 1
        n = (n + e[f % 256]) % 256
        if not f in e:
            f = 0
            t = e[f]
            e[f] = e[n]
            e[n] = t
            a += chr(ord(o[h]) ^ e[(e[f] + e[n]) % 256])
        else:
            t = e[f]
            e[f] = e[n]
            e[n] = t
            a += chr(ord(o[h]) ^ e[(e[f] + e[n]) % 256])

    return a

