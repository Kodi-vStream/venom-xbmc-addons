#-*- coding: utf-8 -*-
# From Anonymous author modified by Tmpname
# https://github.com/Kodi-vStream/venom-xbmc-addons

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
        self.__sUrl = sUrl.replace('https','http')
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
        
    #def GetIP(self):
    #    req = urllib2.Request('http://hqq.tv/player/ip.php?type=json')
    #    response = urllib2.urlopen(req)  
    #    data = response.read()
    #    response.close()
    #    result = json.loads(data)
    #    ip =  result[u'ip']
    #    ip = urllib.quote(ip)
    #    return ip

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
        
        req = urllib2.Request(player_url, None, headers)
        try:
            response = urllib2.urlopen(req)
            html = response.read()
            response.close()
        except urllib2.URLError, e:
            #xbmc.log( e.read())
            #xbmc.log(e.reason)
            html = e.read()
            
            
        #fh = open('c:\\netu.txt', "w")
        #fh.write(html)
        #fh.close()

        data = ''
        code_crypt = re.search('(;eval\(function\(w,i,s,e\){.+?\)\);)\s*<', html, re.DOTALL)
        if code_crypt:
            data = unwise_process(code_crypt.group(1))
        else:
            xbmc.log('prb1')

        #xbmc.log('data :' + data)
            
        if data:
            
            iss = GetIp()
            vid = re.search('var vid *= *"([^"]+)";', data, re.DOTALL).group(1)
            at = re.search('var at = "([^"]+)";', data, re.DOTALL).group(1)
            http_referer = re.search('var http_referer *= *"([^"]+)";', data, re.DOTALL).group(1)
            _pass = ''
            
            url2 = "http://hqq.tv/sec/player/embed_player.php?iss="+iss+"&vid="+vid+"&at="+at+"&autoplayed=yes&referer=on&http_referer="+http_referer+"pass="+_pass+"&embed_from=&need_captcha=0"
            
            #xbmc.log(url2)
            
            req = urllib2.Request(url2,None,headers)
            
            try:
                response = urllib2.urlopen(req)
                data = response.read()
                response.close()
            except urllib2.URLError, e:
                #xbmc.log( e.read())
                #xbmc.log(e.reason)
                data = e.read()

            data = urllib.unquote(data)

            at = re.search(r'var\s*at\s*=\s*"([^"]*?)"', data)
            
            l = re.search(r'link_1: ([a-zA-Z]+), server_1: ([a-zA-Z]+)', data)
            
            vid_server = re.search(r'var ' + l.group(2) + ' = "([^"]+)"', data).group(1)
            vid_link = re.search(r'var ' + l.group(1) + ' = "([^"]+)"', data).group(1)
            
            #new video id, not really usefull
            m = re.search(r' vid: "([a-zA-Z0-9]+)"}', data)
            if m:
                id = m.group(1)
            
            #id = '9QQrbdts6wNA'
            
            if vid_server and vid_link and at:

                #get_data = {'server': vid_server.group(1), 'link': vid_link.group(1), 'at': at.group(1), 'adb': '0/','b':'1','vid':id} #,'iss':'MzEuMz'
                get_data = {'server_1': vid_server, 'link_1': vid_link, 'at': at.group(1), 'adb': '0/','b':'1','vid':id}
                
                #xbmc.log(str(get_data))

                headers['x-requested-with'] = 'XMLHttpRequest'

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

                #xbmc.log(list_url)

                #Now faut tout remettre dans l'ordre
                #plus besoin maintenant
                #url = re.search(r'(^.+)secip(.+?\/)(http.+$)', list_url)
                #list_url = url.group(3) + '/secip' + url.group(2) + url.group(1)
        
        api_call = list_url
        #api_call = list_url.replace('?socket=','.mp4Frag1Num0.ts')
        
        #use a fake headers
        Header = 'User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 5_0_1 like Mac OS X)'
        api_call = api_call + '|' + Header
        
        #print api_call
        
        if not (api_call == False):
            return True, api_call          
            
        return False, False

#*******************************************************************************
# all this part is from a file taken in UrlResolver
# https://github.com/tknorris/script.module.urlresolver/blob/master/lib/urlresolver/plugins/lib/unwise.py
# the completed file will be intact in the future version of vstream, but for the automatic update
# I need to put an extract in this file.

def unwise1(w):
    int1 = 0
    result = ""
    while int1 < len(w):
        result = result + chr(int(w[int1:int1 + 2], 36))
        int1 += 2
    return result

def unwise(w, i, s, e, wi, ii, si, ei):
    int1 = 0
    int2 = 0
    int3 = 0
    int4 = 0
    string1 = ""
    string2 = ""
    while True:
        if w != "":
            if int1 < wi:
                string2 = string2 + w[int1:int1 + 1]
            elif int1 < len(w):
                string1 = string1 + w[int1:int1 + 1]
            int1 += 1
        if i != "":
            if int2 < ii:
                string2 = string2 + i[int2:int2 + 1]
            elif int2 < len(i):
                string1 = string1 + i[int2:int2 + 1]
            int2 += 1
        if s != "":
            if int3 < si:
                string2 = string2 + s[int3:int3 + 1]
            elif int3 < len(s):
                string1 = string1 + s[int3:int3 + 1]
            int3 = int3 + 1
        if e != "":
            if int4 < ei:
                string2 = string2 + e[int4:int4 + 1]
            elif int4 < len(e):
                string1 = string1 + e[int4:int4 + 1]
            int4 = int4 + 1
        if len(w) + len(i) + len(s) + len(e) == len(string1) + len(string2):
            break
    int1 = 0
    int2 = 0
    result = ""
    while int1 < len(string1):
        flag = -1
        if ord(string2[int2:int2 + 1]) % 2:
            flag = 1
        result = result + chr(int(string1[int1:int1 + 2], 36) - flag)
        int2 += 1
        if int2 >= len(string2):
            int2 = 0
        int1 += 2
    return result

def unwise_process(result):
    while True:
        a = re.compile(r';?eval\s*\(\s*function\s*\(\s*w\s*,\s*i\s*,\s*s\s*,\s*e\s*\).+?[\"\']\s*\)\s*\)(?:\s*;)?').search(result)
        if not a:
            break
        a = a.group()
        tmp = re.compile(r'\}\s*\(\s*[\"\'](\w*)[\"\']\s*,\s*[\"\'](\w*)[\"\']\s*,\s*[\"\'](\w*)[\"\']\s*,\s*[\"\'](\w*)[\"\']').search(a)
        if not tmp:
            result = result.replace(a, "")
        else:
            wise = ["", "", "", ""]
            wise = tmp.groups()
            if a.find("while") == -1:
                result = result.replace(a, unwise1(wise[0]))
            else:
                c = 0
                wisestr = ["", "", "", ""]
                wiseint = [0, 0, 0, 0]
                b = re.compile(r'while(.+?)var\s*\w+\s*=\s*\w+\.join\(\s*[\"\'][\"\']\s*\)').search(a).group(1)
                for d in re.compile(r'if\s*\(\s*\w*\s*\<\s*(\d+)\)\s*\w+\.push').findall(b):
                    wisestr[c] = wise[c]
                    wiseint[c] = int(d)
                    c += 1
                result = result.replace(a, unwise(wisestr[0], wisestr[1], wisestr[2], wisestr[3], wiseint[0], wiseint[1], wiseint[2], wiseint[3]))
    return result

def resolve_var(HTML, key):  # this should probably be located elsewhere
    key = re.escape(key)
    tmp1 = HTML.replace("\r", "")
    tmp1 = tmp1.replace("\n", ";")
    tmp2 = re.compile(r'[^\w\.]' + key + '\s*=\s*([^\"\']*?)[;,]').search(tmp1)  # expect var first, movshare
    if tmp2:
        tmp2 = resolve_var(HTML, tmp2.group(1))
    else:
        tmp2 = re.compile(r'[^\w\.]' + key + '\s*=\s*[\"\'](.*?)[\"\']').search(tmp1)
        if tmp2:
            tmp2 = tmp2.group(1)
        else:
            key = key.split("\\.")
            if len(key) == 2:
                tmp2 = re.compile(r'[^\w\.]' + key[0] + '\s*=\s*\{.*[^\w\.]' + key[1] + '\s*\:\s*[\"\'](.*?)[\"\']').search(tmp1)  # for 'vars = { key: "value" }', cloudy
            if tmp2:
                tmp2 = tmp2.group(1)
            else:
                tmp2 = ""  # oops, should not happen in the variable is valid
    return tmp2
