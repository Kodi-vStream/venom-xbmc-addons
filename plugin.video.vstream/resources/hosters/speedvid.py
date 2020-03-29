#coding: utf-8
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
# from resources.lib.aadecode import AADecoder
from resources.lib.jjdecode import JJDecoder
from resources.lib.packer import cPacker
from resources.lib.jsparser import JsParser
from resources.lib.comaddon import VSlog

import re

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Speedvid'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR] [COLOR khaki]' + self.__sHD + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'speedvid'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def __getHost(self):
        parts = self.__sUrl.split('//', 1)
        host = parts[0] + '//' + parts[1].split('/', 1)[0]
        return host

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        oRequest = cRequestHandler(self.__sUrl.replace('sn', 'embed'))
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Host', 'www.speedvid.net')
        sHtmlContent = oRequest.request()

        #suppression commentaires
        sHtmlContent = re.sub( r'<!--.*?-->', '', sHtmlContent )

        oParser = cParser()

        #fh = open('c:\\test0.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()

        #decodage de la pahe html
        sHtmlContent3 = sHtmlContent
        code = ''
        maxboucle = 10
        while (maxboucle > 0):
            VSlog('loop : ' + str(maxboucle))
            sHtmlContent3 = CheckCpacker(sHtmlContent3)
            #sHtmlContent3 = CheckJJDecoder(sHtmlContent3)
            sHtmlContent3 = CheckAADecoder(sHtmlContent3)

            maxboucle = maxboucle - 1

        sHtmlContent = sHtmlContent3

        VSlog('fini')

        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()

        #Desactive pour le moment
        if (True):
            Realurl = ''

            red = re.findall('location.href *= *[\'"]([^\'"]+)', sHtmlContent)
            if red:
                Realurl = red[0]
            else:
                VSlog("2")
                red = re.findall('location\.assign *\( *"([^"]+)" \)', sHtmlContent)
                if red:
                    Realurl = red[0]

            if 'speedvid' not in Realurl:
                Realurl = self.__getHost() + Realurl

            if not Realurl.startswith('http'):
                Realurl = 'http:' + Realurl

            if not Realurl:
                VSlog("mauvaise redirection")
                return False, False

            VSlog('Real url>> ' + Realurl)

            oRequest = cRequestHandler(Realurl)
            oRequest.addHeaderEntry('User-Agent', UA)
            oRequest.addHeaderEntry('Referer', self.__sUrl)

            sHtmlContent = oRequest.request()

        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()

        api_call = ''

        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\)\))<'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for packed in aResult[1]:
                sHtmlContent = cPacker().unpack(packed)
                sHtmlContent = sHtmlContent.replace('\\', '')
                if "jwplayer('vplayer').setup" in sHtmlContent:
                    sPattern2 = "{file:.([^']+.mp4)"
                    aResult2 = oParser.parse(sHtmlContent, sPattern2)
                    if (aResult2[0] == True):
                        api_call = aResult2[1][0]
                        break

        else:
            sPattern = "file\s*:\s*\'([^\']+.mp4)"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                api_call = aResult[1][0]

        VSlog('API_CALL: ' + api_call )

        if (api_call):
            api_call = api_call + '|User-Agent=' + UA  #+ #'|Host=' + api_call.replace('http://','').rsplit('/', 2)[0]

            return True, api_call

        return False, False
#********************************************************************************************************************************

def CheckCpacker(str):

    sPattern = '>([^>]+\(p,a,c,k,e(?:.|\s)+?\)\)\s*)<'
    aResult = re.search(sPattern, str, re.DOTALL | re.UNICODE)
    if (aResult):
        #VSlog('Cpacker encryption')
        str2 = aResult.group(1)

        if not str2.endswith(';'):
            str2 = str2 + ';'

        #if not str2.startswith('eval'):
        #    str2 = 'eval(function' + str2[4:]

        #Me demandez pas pourquoi mais si je l'affiche pas en log, ca freeze ?????
        #VSlog(str2)

        try:
            tmp = cPacker().unpack(str2)
            #tmp = tmp.replace("\\'", "'")
        except:
            tmp = ''

        #VSlog(tmp)

        return str[:(aResult.start() + 1)] + tmp + str[(aResult.end()-1):]

    return str

def CheckJJDecoder(str):

    sPattern = '([a-z]=.+?\(\)\)\(\);)'
    aResult = re.search(sPattern, str, re.DOTALL | re.UNICODE)
    if (aResult):
        VSlog('JJ encryption')
        tmp = JJDecoder(aResult.group(0)).decode()

        return str[:aResult.start()] + tmp + str[aResult.end():]

    return str

def CheckAADecoder(str):
    aResult = re.search('([>;]\s*)(ﾟωﾟ.+?\(\'_\'\);)', str, re.DOTALL | re.UNICODE)
    if (aResult):
        VSlog('AA encryption')

        #tmp = aResult.group(1) + AADecoder(aResult.group(2)).decode()

        JP = JsParser()
        Liste_var = []

        try:
            JScode = aResult.group(2)
            JScode = unicode(JScode, "utf-8")

            tmp = JP.ProcessJS(JScode, Liste_var)
            tmp = JP.LastEval.decode('string-escape').decode('string-escape')

            return str[:aResult.start()] + tmp + str[aResult.end():]
        except:
            return ''
    return str
