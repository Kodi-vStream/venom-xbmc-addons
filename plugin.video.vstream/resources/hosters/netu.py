#-*- coding: utf-8 -*-
#From Anonymous author modified by Tmpname

from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.gui import cGui
import urllib, urllib2

import xbmc

import re
import base64

try:    import json
except: import simplejson as json


def _decode(data):
    def O1l(string):
        ret = ""
        i = len(string) - 1
        while i >= 0:
            ret += string[i]
            i -= 1
        return ret

    def l0I(string):
        enc = ""
        dec = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        i = 0
        while True:
            h1 = dec.find(string[i])
            i += 1
            h2 = dec.find(string[i])
            i += 1
            h3 = dec.find(string[i])
            i += 1
            h4 = dec.find(string[i])
            i += 1
            bits = h1 << 18 | h2 << 12 | h3 << 6 | h4
            o1 = bits >> 16 & 0xff
            o2 = bits >> 8 & 0xff
            o3 = bits & 0xff
            if h3 == 64:
                enc += unichr(o1)
            else:
                if h4 == 64:
                    enc += unichr(o1) + unichr(o2)
                else:
                    enc += unichr(o1) + unichr(o2) + unichr(o3)
            if i >= len(string):
                break
        return enc

    escape = re.search("var _escape=\'([^\']+)", l0I(O1l(data))).group(1)
    return escape.replace('%', '\\').decode('unicode-escape')


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
        self.__sDisplayName = 'netu'
	self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
	self.__sFileName = sFileName

    def getFileName(self):
	return self.__sFileName
    
    def setUrl(self, sUrl):
        self.__sUrl = sUrl.replace('http://netu.tv/','http://hqq.tv/')
        self.__sUrl = self.__sUrl.replace('http://waaw.tv/','http://hqq.tv/')
        self.__sUrl = self.__sUrl.replace('http://hqq.tv/watch_video.php?v=','http://hqq.tv/player/embed_player.php?vid=')       
    
    def __getIdFromUrl(self):
        sPattern = 'http:..hqq.tv.player.embed_player.php\?vid=([0-9A-Z]+)'
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)
        
        if (aResult[0] == True):
            return aResult[1][0]
        return ''
        
    def __modifyUrl(self, sUrl):
        api = ('http://rutube.ru/api/play/trackinfo/%s/?format=json') % (self.__getIdFromUrl())

        oRequest = cRequestHandler(api)
        sHtmlContent = oRequest.request()
        sHtmlContent = sHtmlContent.replace('\\', '').replace('//', '')
        
        sPattern = 'src="(.+?)"'
        
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            self.__sUrl = 'http://' + aResult[1][0]
            return self.__sUrl
            
        return


    def getPluginIdentifier(self):
        return 'netu'

    def isDownloadable(self):
        return False

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';

    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()
        
    def GetIP(self):
        req = urllib2.Request('http://hqq.tv/player/ip.php?type=json')
        response = urllib2.urlopen(req)  
        data = response.read()
        response.close()
        result = json.loads(data)
        ip =  result[u'ip']
        ip = urllib.quote(ip)
        return ip

    def __getMediaLinkForGuest(self):
    
        api_call = ''
    
        id = self.__getIdFromUrl()
        
        self.__sUrl = 'http://hqq.tv/player/embed_player.php?vid=' + id + '&autoplay=no'

        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
        #UA = 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us)'
        headers = {'User-Agent': UA ,
                   'Host' : 'hqq.tv',
                   'Referer': 'http://hqq.tv/',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Content-Type': 'text/html; charset=utf-8'}
        
        player_url = self.__sUrl
        
        #import xbmc

        req = urllib2.Request(player_url, None, headers)
        try:
            response = urllib2.urlopen(req)
            data = response.read()
            response.close()
        except urllib2.URLError, e:
            #xbmc.log( e.read())
            #xbmc.log(e.reason)
            data = e.read()
        
        b64enc = re.search('base64([^\"]+)', data, re.DOTALL)
        b64dec = b64enc and base64.decodestring(b64enc.group(1))
        enc = b64dec and re.search("\'([^']+)\'", b64dec).group(1)
   
        
        if enc:
            data = re.findall('<input name="([^"]+?)" [^>]+? value="([^"]+?)">', _decode(enc))
            post_data = {}
            for idx in range(len(data)):
                post_data[data[idx][0]] = data[idx][1]

            postdata = urllib.urlencode(post_data)
            
            req = urllib2.Request(player_url,postdata,headers)
            try:
                response = urllib2.urlopen(req)
                data = response.read()
                response.close()
            except urllib2.URLError, e:
                #xbmc.log( e.read())
                #xbmc.log(e.reason)
                data = e.read()
            
            b64enc = re.search('base64([^\"]+)', data, re.DOTALL)
            b64dec = b64enc and base64.decodestring(b64enc.group(1))
            enc = b64dec and re.search("\'([^']+)\'", b64dec).group(1)
            
            if enc:
                data = re.findall('<input name="([^"]+?)" [^>]+? value="([^"]*)">', _decode(enc))

                post_data = {}
                for idx in range(len(data)):
                    post_data[data[idx][0]] = data[idx][1]
                    
                #correction de bug
                #if post_data['vid'] == '':
                #    post_data['vid'] = 'pmpmp'#str(id)

                    
                #post_data['http_referer'] = 'http%3A%2F%2Ffull-stream.me%2Fmovies%2Ffilms-en-streaming%2F9699-diversion.html'
                
                req = urllib2.Request("http://hqq.tv/sec/player/embed_player.php?" + urllib.urlencode(post_data),None,headers)
                
                try:
                    response = urllib2.urlopen(req)
                    data = response.read()
                    response.close()
                except urllib2.URLError, e:
                    #xbmc.log( e.read())
                    #xbmc.log(e.reason)
                    data = e.read()

                data = urllib.unquote(data)
                
                #fh = open('c:\\netu.txt', "w")
                #fh.write(data)
                #fh.close()
                
                at = re.search(r'var\s*at\s*=\s*"([^"]*?)"', data)
                
                l = re.search(r'link_1: ([a-zA-Z]+), server_1: ([a-zA-Z]+)', data)
                
                vid_server = re.search(r'var ' + l.group(1) + ' = "([^"]+)"', data).group(1)
                vid_link = re.search(r'var ' + l.group(2) + ' = "([^"]+)"', data).group(1)
                
                if vid_server and vid_link and at:

                    #get_data = {'server': vid_server.group(1), 'link': vid_link.group(1), 'at': at.group(1), 'adb': '0/','b':'1','vid':id} #,'iss':'MzEuMz'
                    get_data = {'server_1': vid_server, 'link_1': vid_link, 'at': at.group(1), 'adb': '0/','b':'1','vid':id}
                    
                    req = urllib2.Request("http://hqq.tv/player/get_md5.php?" + urllib.urlencode(get_data),None,headers)
                    try:
                        response = urllib2.urlopen(req)
                    except urllib2.URLError, e:
                        xbmc.log(str(e.read()))
                        xbmc.log(str(e.reason))
                        
                    data = response.read()
                    response.close()
                    
                    #fh = open('c:\\netu2.txt', "w")
                    #fh.write(data)
                    #fh.close()
                    
                    file_url = re.search(r'"file"\s*:\s*"([^"]*?)"', data)
                   
                    if file_url:
                        list_url = _decode2(file_url.group(1).replace('\\', ''))
                        
                    #Now faut tout remettre dans l'ordre
                    url = re.search(r'(^.+)secip(.+?\/)(http.+$)', list_url)
                    list_url = url.group(3) + '/secip' + url.group(2) + url.group(1)
        
        api_call = list_url
        #api_call = list_url.replace('?socket=','.mp4Frag1Num0.ts')
        
        #use a fake headers
        Header = 'User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X)'
        api_call = api_call + '|' + Header
        
        #print api_call
        
        if not (api_call == False):
            return True, api_call          
            
        return False, False
