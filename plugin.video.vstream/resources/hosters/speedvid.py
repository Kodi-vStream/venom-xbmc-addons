# coding: utf-8
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.jsparser import JsParser
from resources.lib.packer import cPacker
from resources.lib.parser import cParser

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'


class cHoster(iHoster):
    def __init__(self):
        iHoster.__init__(self, 'speedvid', 'Speedvid')

    def __getHost(self):
        parts = self._url.split('//', 1)
        host = parts[0] + '//' + parts[1].split('/', 1)[0]
        return host

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url.replace('sn', 'embed'))
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Host', 'www.speedvid.net')
        sHtmlContent = oRequest.request()

        # suppression commentaires
        sHtmlContent = re.sub(r'<!--.*?-->', '', sHtmlContent)

        oParser = cParser()

        # fh = open('c:\\test0.txt', "w")
        # fh.write(sHtmlContent)
        # fh.close()

        # decodage de la page html
        sHtmlContent3 = sHtmlContent
        code = ''
        maxboucle = 10
        while maxboucle > 0:
            VSlog('loop : ' + str(maxboucle))
            sHtmlContent3 = checkCpacker(sHtmlContent3)
            sHtmlContent3 = checkAADecoder(sHtmlContent3)

            maxboucle = maxboucle - 1

        sHtmlContent = sHtmlContent3

        VSlog('fini')

        # fh = open('c:\\test.txt', "w")
        # fh.write(sHtmlContent)
        # fh.close()

        realurl = ''

        red = re.findall('location.href *= *[\'"]([^\'"]+)', sHtmlContent)
        if red:
            realurl = red[0]
        else:
            VSlog("2")
            red = re.findall('location\.assign *\( *"([^"]+)" \)', sHtmlContent)
            if red:
                realurl = red[0]

        if 'speedvid' not in realurl:
            realurl = self.__getHost() + realurl

        if not realurl.startswith('http'):
            realurl = 'http:' + realurl

        if not realurl:
            VSlog("mauvaise redirection")
            return False, False

        VSlog('Real url>> ' + realurl)

        oRequest = cRequestHandler(realurl)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', self._url)

        sHtmlContent = oRequest.request()

        # fh = open('c:\\test.txt', "w")
        # fh.write(sHtmlContent)
        # fh.close()

        api_call = ''

        sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\)\))<'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0] is True:
            for packed in aResult[1]:
                sHtmlContent = cPacker().unpack(packed)
                sHtmlContent = sHtmlContent.replace('\\', '')
                if "jwplayer('vplayer').setup" in sHtmlContent:
                    sPattern2 = "{file:.([^']+.mp4)"
                    aResult2 = oParser.parse(sHtmlContent, sPattern2)
                    if aResult2[0] is True:
                        api_call = aResult2[1][0]
                        break

        else:
            sPattern = "file\s*:\s*\'([^\']+.mp4)"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                api_call = aResult[1][0]

        VSlog('API_CALL: ' + api_call)

        if api_call:
            api_call = api_call + '|User-Agent=' + UA  # + #'|Host=' + api_call.replace('http://','').rsplit('/', 2)[0]

            return True, api_call

        return False, False
# *********************************************************************************************************************


def checkCpacker(strToPack):
    sPattern = '>([^>]+\(p,a,c,k,e(?:.|\s)+?\)\)\s*)<'
    aResult = re.search(sPattern, strToPack, re.DOTALL | re.UNICODE)
    if aResult:
        # VSlog('Cpacker encryption')
        str2 = aResult.group(1)

        if not str2.endswith(';'):
            str2 = str2 + ';'

        # if not str2.startswith('eval'):
           # str2 = 'eval(function' + str2[4:]

        # Me demandez pas pourquoi mais si je l'affiche pas en log, ca freeze ?????
        # VSlog(str2)

        try:
            tmp = cPacker().unpack(str2)
            # tmp = tmp.replace("\\'", "'")
        except:
            tmp = ''

        # VSlog(tmp)

        return strToPack[:(aResult.start() + 1)] + tmp + strToPack[(aResult.end()-1):]

    return strToPack


# def checkJJDecoder(str):

#     sPattern = '([a-z]=.+?\(\)\)\(\);)'
#     aResult = re.search(sPattern, str, re.DOTALL | re.UNICODE)
#     if (aResult):
#         VSlog('JJ encryption')
#         tmp = JJDecoder(aResult.group(0)).decode()

#         return str[:aResult.start()] + tmp + str[aResult.end():]

#     return str


def checkAADecoder(stringToDecode):
    aResult = re.search('([>;]\s*)(ﾟωﾟ.+?\(\'_\'\);)', str, re.DOTALL | re.UNICODE)
    if aResult:
        VSlog('AA encryption')

        # tmp = aResult.group(1) + AADecoder(aResult.group(2)).decode()

        JP = JsParser()
        liste_var = []

        try:
            js_code = aResult.group(2)

            try:
                js_code = unicode(js_code, "utf-8")
            except Exception:
                js_code = str(js_code)

            tmp = JP.ProcessJS(js_code, liste_var)
            tmp = JP.LastEval.decode('string-escape').decode('string-escape')

            return stringToDecode[:aResult.start()] + tmp + stringToDecode[aResult.end():]
        except Exception:
            return ''
    return stringToDecode
