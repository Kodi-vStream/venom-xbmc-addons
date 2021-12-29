#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import VSlog, xbmc
from resources.lib.handler.requestHandler import cRequestHandler
from resources.hosters.hoster import iHoster

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'

class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mystream', 'MyStream')

    def setUrl(self, url):
        self._url = str(url).replace('https://mystream.to/watch/', 'https://embed.mystream.to/')

    def _getMediaLinkForGuest(self):
        oRequest = cRequestHandler(self._url)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        sHtmlContent = oRequest.request()

        api_call = False

        sPattern =  '(\$=.+?;)\s*<'
        aResult = re.search(sPattern, sHtmlContent, re.DOTALL)
        if aResult:
            decoded = temp_decode(aResult.group(1))
            if decoded:
                r = re.search("setAttribute\(\'src\', *\'([^']+)\'\)", decoded, re.DOTALL)
                if r:
                    api_call = r.group(1)

        if api_call:
            return True, api_call + '|User-Agent=' + UA + '&Referer=' + self._url + '&Origin=https://embed.mystream.to'

        return False, False

def temp_decode(data):
    startpos = data.find('"\\""+') + 5
    endpos = data.find('"\\"")())()')

    first_group = data[startpos:endpos]

    pos = re.search(r"(\(!\[\]\+\"\"\)\[.+?\]\+)", first_group)
    if pos:
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

            first_group = first_group.replace('\\"', '\\').replace("\"\\\\\\\\\"", "\\\\")\
                                     .replace('\\"', '\\').replace('"', '').replace("+", "")
            first_group = re.sub('(\(\!\[\]\)\[.+?\]+)','l',first_group)
        try:
            final_data = first_group.encode('ascii').decode('unicode-escape').encode('ascii')\
                .decode('unicode-escape')
            return final_data
        except:
            return False
