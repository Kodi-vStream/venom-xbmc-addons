#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import unwise
from resources.lib.util import cUtil
from resources.lib.recaptcha import ResolveCaptcha
#from resources.lib.comaddon import VSlog
import urllib,re,base64

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/66.0'

def GetIp():
    if (False):
        oRequest = cRequestHandler('http://hqq.tv/player/ip.php?type=json')
        oRequest.addHeaderEntry
        sHtmlContent = oRequest.request()
        ip = re.search('"ip":"([^"]+)"', sHtmlContent, re.DOTALL).group(1)
    else:
        import random
        for x in xrange(1,100):
            ip = "192.168."
            ip += ".".join(map(str, (random.randint(0, 255) for _ in range(2))))
        ip = base64.b64encode(ip)

    return ip

def _decode2(file_url):
    def K12K(a, typ='b'):
        codec_a = ["G", "L", "M", "N", "Z", "o", "I", "t", "V", "y", "x", "p", "R", "m", "z", "u",
                   "D", "7", "W", "v", "Q", "n", "e", "0", "b", "="]
        codec_b = ["2", "6", "i", "k", "8", "X", "J", "B", "a", "s", "d", "H", "w", "f", "T", "3",
                   "l", "c", "5", "Y", "g", "1", "4", "9", "U", "A"]
        if 'd' == typ:
            tmp = codec_a
            codec_a = codec_b
            codec_b = tmp
        idx = 0
        while idx < len(codec_a):
            a = a.replace(codec_a[idx], "___")
            a = a.replace(codec_b[idx], codec_a[idx])
            a = a.replace("___", codec_b[idx])
            idx += 1
        return a

    def _xc13(_arg1):
        _lg27 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        _local2 = ""
        _local3 = [0, 0, 0, 0]
        _local4 = [0, 0, 0]
        _local5 = 0
        while _local5 < len(_arg1):
            _local6 = 0
            while _local6 < 4 and (_local5 + _local6) < len(_arg1):
                _local3[_local6] = _lg27.find(_arg1[_local5 + _local6])
                _local6 += 1
            _local4[0] = ((_local3[0] << 2) + ((_local3[1] & 48) >> 4))
            _local4[1] = (((_local3[1] & 15) << 4) + ((_local3[2] & 60) >> 2))
            _local4[2] = (((_local3[2] & 3) << 6) + _local3[3])

            _local7 = 0
            while _local7 < len(_local4):
                if _local3[_local7 + 1] == 64:
                    break
                _local2 += chr(_local4[_local7])
                _local7 += 1
            _local5 += 4
        return _local2

    return _xc13(K12K(file_url, 'e'))

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Netu'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def setUrl(self, sUrl):
        self.__sUrl = sUrl.replace('https', 'http')
        self.__sUrl = self.__sUrl.replace('http://netu.tv/', 'http://hqq.tv/')
        self.__sUrl = self.__sUrl.replace('http://waaw.tv/', 'http://hqq.tv/')
        self.__sUrl = self.__sUrl.replace('http://hqq.tv/player/hash.php?hash=', 'http://hqq.tv/player/embed_player.php?vid=')
        self.__sUrl = self.__sUrl.replace('http://hqq.tv/watch_video.php?v=', 'http://hqq.tv/player/embed_player.php?vid=')

    def __getIdFromUrl(self):
        sPattern = 'https*:\/\/hqq\.(?:tv|player|watch)\/player\/embed_player\.php\?vid=([0-9A-Za-z]+)'
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)

        if (aResult[0] == True):
            return aResult[1][0]
        return ''

    def getPluginIdentifier(self):
        return 'netu'

    def isDownloadable(self):
        return False

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def GetHost(self,sUrl):
        oParser = cParser()
        sPattern = 'https*:\/\/(.+?)\/'
        aResult = oParser.parse(sUrl, sPattern)
        if aResult[0]:
            return aResult[1][0]
        return ''

    def __getMediaLinkForGuest(self):

        api_call = ''

        ids = self.__getIdFromUrl()

        self.__sUrl = 'http://hqq.tv/player/embed_player.php?vid=' + ids + '&autoplay=no'

        player_url = self.__sUrl

        headers = {'User-Agent': UA ,
                   #'Host': 'hqq.tv',
                   'Referer': 'http://hqq.tv/',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   #'Accept-Encoding': 'gzip, deflate, br',
                   #'Content-Type': 'text/html; charset=utf-8'
                   }

        oRequestHandler = cRequestHandler(player_url)
        oRequestHandler.addHeaderEntry('User-Agent',UA)
        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('Referer', 'http://hqq.tv/')
        html = oRequestHandler.request()

        Host = 'https://' + self.GetHost(player_url) + '/'

        data = ''
        data = DecodeAllThePage(html)

        #data = ''
        #code_crypt = re.search('(;eval\(function\(w,i,s,e\){.+?\)\);)\s*<', html, re.DOTALL)
        #if code_crypt:
        #    data = unwise.unwise_process(code_crypt.group(1))
        #else:
        #    VSlog('prb1')

        if data:
            http_referer = ''
            _pass = ''

            iss = GetIp()
            vid = re.search("videokeyorig=\'(.+?)\'", data, re.DOTALL).group(1)
            at = re.search("attoken=\'(.+?)\'", data, re.DOTALL).group(1)
            r = re.search('var referer = "([^"]+)"', data, re.DOTALL)
            if r:
                http_referer = r.group(1)

            import string, random
            _BOUNDARY_CHARS = string.digits
            boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(17))

            url2 = "https://hqq.tv/sec/player/embed_player_"+boundary+".php?iss="+iss+"=&vid="+vid+"&at="+at+"&autoplayed=yes&referer=on&http_referer="+http_referer+"&pass=&embed_from=&need_captcha=0&secure=0&g-recaptcha-response="
            oRequestHandler = cRequestHandler(url2)
            oRequestHandler.addHeaderEntry('User-Agent',UA)
            oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            oRequestHandler.addHeaderEntry('Referer', 'http://hqq.tv/')
            sHtmlContent = oRequestHandler.request()

            key = re.search("\'sitekey\' : \'(.+?)\'",str(sHtmlContent)).group(1)
            gToken = ResolveCaptcha(key,self.__sUrl)

            url2 = url2 + gToken

            oRequestHandler = cRequestHandler(url2)
            oRequestHandler.addHeaderEntry('User-Agent',UA)
            oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
            oRequestHandler.addHeaderEntry('Referer', 'http://hqq.tv/')
            data = oRequestHandler.request()

            data = urllib.unquote(data)

            data = DecodeAllThePage(data)
            #VSlog(data)

            at = re.search(r'var\s*at\s*=\s*"([^"]*?)"', data).group(1)



        nameVar = re.search('true.+?\s*.+?link_1="\+encodeURIComponent\((.+?)\)\+"&server_2="\+encodeURIComponent\((.+?)\)\+"&vid="\+encodeURIComponent\("(.+?)"\)',data)
        var1 = re.search('var '+nameVar.group(1)+' = "(.+?)"', data).group(1)
        var2 = re.search('var '+nameVar.group(2)+' = "(.+?)"', data).group(1)

        #bricolage
        api_call = "https://hqq.tv/player/get_md5.php?ver=2&at="+urllib.quote(at, safe='~()*!.\'')+"&adb="+urllib.quote("1/", safe='~()*!.\'')+"&b=1&link_1="+urllib.quote(var1, safe='~()*!.\'')+"&server_2="+urllib.quote(var2, safe='~()*!.\'')+"&vid="+urllib.quote(nameVar.group(3), safe='~()*!.\'')+"&ext=.mp4.m3u8"

        #use a fake headers
        Header = "Accept-Language= fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3&Accept-Encoding= gzip, deflate, br"
        api_call = api_call + '|' + Header

        if not (api_call == False):
            return True, api_call

        return False, False

#*******************************************************************************
def decodeUN(a):
    a = a[1:]
    s2 = ""

    i = 0
    while i < len(a):
      s2 += ('\u0' + a[i:i+3])
      i = i + 3

    s3 = s2.decode('unicode-escape')
    if not s3.startswith('http'):
        s3 = 'http:' + s3

    return s3

def DecodeAllThePage(html):

    #html = urllib.unquote(html)

    Maxloop = 10

    #unescape
    while (Maxloop > 0):
        Maxloop = Maxloop - 1

        r = re.search(r'unescape\("([^"]+)"\)', html, re.DOTALL | re.UNICODE)
        if not r:
            break

        tmp = cUtil().unescape(r.group(1))
        html = html[:r.start()] + tmp + html[r.end():]

    #unwise
    while (Maxloop > 0):
        Maxloop = Maxloop - 1

        r = re.search(r'(;eval\(function\(w,i,s,e\){.+?\)\);)\s*<', html, re.DOTALL | re.UNICODE)
        if not r:
            break

        tmp = data = unwise.unwise_process(r.group(1))
        html = html[:r.start()] + tmp + html[r.end():]

    return html
