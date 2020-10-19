#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster
import re

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'MyStream'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'mystream'

    def isDownloadable(self):
        return True

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        url = self.__sUrl

        oRequest = cRequestHandler(url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        sHtmlContent = oRequest.request()

        api_call = False

        sPattern =  '([$]=.+?\(\)\)\(\);)'
        aResult = re.search(sPattern, sHtmlContent, re.DOTALL)
        if aResult:
            decoded = temp_decode(aResult.group(1))
            if decoded:
                r = re.search("setAttribute\(\'src\', *\'([^']+)\'\)", decoded, re.DOTALL)
                if r:
                    api_call = r.group(1)

        if (api_call):
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self.__sUrl + '&Origin=https://embed.mystream.to'

        return False, False

def temp_decode(data):
    startpos = data.find('"\\""+') + 5
    endpos = data.find('"\\"")())()')

    first_group = data[startpos:endpos]
    first_group = first_group.replace('$.__+', 't').replace('$._+', 'u').replace('$._$+', 'o')

    tmplist = []
    js = re.search(r'(\$={.+?});', data)
    if js:
        js_group = js.group(1)[3:][:-1]
        second_group = js_group.split(',')

        i = -1
        for x in second_group:
            a, b = x.split(':')

            if b == '++$':
                i += 1
                tmplist.append(("$.{}+".format(a), i))

            elif b == '(![]+"")[$]':
                tmplist.append(("$.{}+".format(a), 'false'[i]))

            elif b == '({}+"")[$]':
                tmplist.append(("$.{}+".format(a), '[object Object]'[i]))

            elif b == '($[$]+"")[$]':
                tmplist.append(("$.{}+".format(a), 'undefined'[i]))

            elif b == '(!""+"")[$]':
                tmplist.append(("$.{}+".format(a), 'true'[i]))

        tmplist = sorted(tmplist, key=lambda z: str(z[1]))
        for x in tmplist:
            first_group = first_group.replace(x[0], str(x[1]))

        first_group = first_group.replace('\\"', '\\').replace("\"\\\\\\\\\"", "\\\\") \
                                 .replace('\\"', '\\').replace('"', '').replace("+", "")

        pos = re.findall(r"\(!\[\]\)\[.+?\]", first_group)
        for p in pos:
            first_group = first_group.replace(p,"l")

    try:
        final_data = first_group.encode('ascii').decode('unicode-escape')
        return final_data
    except:
        return False
