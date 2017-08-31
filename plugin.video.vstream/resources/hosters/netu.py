#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import unwise
from resources.lib.util import cUtil,VSlog
import urllib, urllib2
import re
import base64

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
#UA = 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25'
    
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
        self.__sUrl = sUrl.replace('https','http')
        self.__sUrl = sUrl.replace('http://netu.tv/','http://hqq.tv/')
        self.__sUrl = self.__sUrl.replace('http://waaw.tv/','http://hqq.tv/')
        self.__sUrl = self.__sUrl.replace('http://hqq.tv/watch_video.php?v=','http://hqq.tv/player/embed_player.php?vid=')
    
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

    def __getMediaLinkForGuest(self):
    
        api_call = ''
    
        id = self.__getIdFromUrl()
        
        self.__sUrl = 'http://hqq.tv/player/embed_player.php?vid=' + id + '&autoplay=no'

        headers = {'User-Agent': UA ,
                   #'Host' : 'hqq.tv',
                   'Referer': 'http://hqq.tv/',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   #'Accept-Encoding':'gzip, deflate, br',
                   #'Content-Type': 'text/html; charset=utf-8'
                   }
        
        player_url = self.__sUrl
        
        req = urllib2.Request(player_url,None,headers)
        try:
            response = urllib2.urlopen(req)
            html = response.read()
            response.close()
        except urllib2.URLError, e:
            VSlog(e.read())
            VSlog(e.reason)
            html = e.read()

        Host = 'https://hqq.watch/'

        data = ''
        code_crypt = re.search('(;eval\(function\(w,i,s,e\){.+?\)\);)\s*<', html, re.DOTALL)
        if code_crypt:
            data = unwise.unwise_process(code_crypt.group(1))
        else:
            VSlog('prb1')       
            
        if data:
            http_referer = ''
            _pass = ''
            
            iss = GetIp()
            vid = re.search('var vid *= *"([^"]+)";', data, re.DOTALL).group(1)
            at = re.search('var at *= *"([^"]+)";', data, re.DOTALL).group(1)
            r = re.search('var http_referer *= *"([^"]+)";', data, re.DOTALL)
            if r:
                http_referer = r.group(1)
            
            url2 = Host + "sec/player/embed_player.php?iss=" + iss + "&vid=" + vid + "&at=" + at + "&autoplayed=yes&referer=on&http_referer=" + http_referer + "&pass=" + _pass + "&embed_from=&need_captcha=0"
            #VSlog( url2 )
            
            req = urllib2.Request(url2,None,headers)
            
            try:
                response = urllib2.urlopen(req)
                data = response.read()
                response.close()
            except urllib2.URLError, e:
                VSlog(e.read())
                VSlog(e.reason)
                data = e.read()

            data = urllib.unquote(data)

            data = DecodeAllThePage(data)

            at = re.search(r'var\s*at\s*=\s*"([^"]*?)"', data)
            
            l = re.search(r'link_1: ([a-zA-Z]+), server_1: ([a-zA-Z]+)', data)
            
            vid_server = re.search(r'var ' + l.group(2) + ' = "([^"]+)"', data).group(1)
            vid_link = re.search(r'var ' + l.group(1) + ' = "([^"]+)"', data).group(1)
            
            #new video id, not really usefull
            m = re.search(r' vid: "([a-zA-Z0-9]+)"}', data)
            if m:
                id = m.group(1)
            
            if vid_server and vid_link and at:

                #get_data = {'server': vid_server.group(1), 'link': vid_link.group(1), 'at': at.group(1), 'adb': '0/','b':'1','vid':id} #,'iss':'MzEuMz'
                get_data = {'server_1': vid_server, 'link_1': vid_link, 'at': at.group(1), 'adb': '0/','b':'1','vid':id}

                headers['x-requested-with'] = 'XMLHttpRequest'

                req = urllib2.Request(Host + "/player/get_md5.php?" + urllib.urlencode(get_data),None,headers)
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    VSlog(str(e.read()))
                    VSlog(str(e.reason))
                    
                data = response.read()
                VSlog(data)
                response.close()

                file_url = re.search(r'"file"\s*:\s*"([^"]*?)"', data)
               
                if file_url:
                    list_url = _decode2(file_url.group(1).replace('\\', ''))

                #Hack, je sais pas si ca va durer longtemps, mais indispensable sur certains fichiers
                list_url = list_url.replace("?socket", ".mp4.m3u8")
                
            else:
                VSlog('prb2')
        
        api_call = list_url
        #api_call = list_url.replace('?socket=','.mp4Frag1Num0.ts')
        
        #use a fake headers
        Header = 'User-Agent=' + UA
        api_call = api_call + '|' + Header

        if not (api_call == False):
            return True, api_call
            
        return False, False

#*******************************************************************************

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
