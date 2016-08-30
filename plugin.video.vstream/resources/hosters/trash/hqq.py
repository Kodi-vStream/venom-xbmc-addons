from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import urllib
import urllib2
import re, base64
import htmlentitydefs
import cookielib
try:
    from StringIO import StringIO
    import gzip
except:
    pass


class cHoster(iHoster):

    HOST   = 'Mozilla/5.0 (Windows NT 6.1; rv:17.0) Gecko/20100101 Firefox/17.0'
    HEADER = None
    
    def __init__(self):
        self.__sDisplayName = 'Netu'
        self.__sFileName = self.__sDisplayName
        self.proxyURL = ''
        self.useProxy = False

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
	self.__sFileName = sFileName

    def getFileName(self):
	return self.__sFileName

    def getPluginIdentifier(self):
        return 'hqq'

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''
        
    def __getIdFromUrl(self, sUrl):
        sPattern = "http://exashare.com/([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    def __getPhpSessionId(self, aHeader):       
        sReponseCookie = aHeader.getheader("Set-Cookie")       
        aResponseCookies = sReponseCookie.split(";")
        return aResponseCookies[0]
        
    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        
        # sPattern =  'http://(?:www.|embed.)exashare.(?:com)/(?:video/|embed\-)?([0-9a-z]+)'
         
        # oParser = cParser()
        # aResult = oParser.parse(sUrl, sPattern)
        # self.__sUrl = 'http://exashare.com/embed-'+str(aResult[1][0])+'.html'


    def checkUrl(self, sUrl):
        return True

    def getUrl(self):
        return self.__sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()
    
    def getURLRequestData(self, params = {}, post_data = None):
        
        def urlOpen(req, customOpeners):
            if len(customOpeners) > 0:
                opener = urllib2.build_opener( *customOpeners )
                response = opener.open(req)
            else:
                response = urllib2.urlopen(req)
                
            return response
        
        cj = cookielib.LWPCookieJar()
        response = None
        req = None
        out_data = None
        opener = None
        
        if 'host' in params:
            host = params['host']
        else:
            host = self.HOST
 
        if 'header' in params:
            headers = params['header']
        elif None != self.HEADER:
            headers = self.HEADER
        else:
            headers = { 'User-Agent' : host }
 
        
        print 'pCommon - getURLRequestData() -> params: ' + str(params)
        #print 'pCommon - getURLRequestData() -> headers: ' + str(headers)
 
        customOpeners = []
        #cookie support
        if params.get('use_cookie', False):
            customOpeners.append( urllib2.HTTPCookieProcessor(cj) )
            if params.get('load_cookie', False):
                cj.load(params['cookiefile'], ignore_discard = True)
        
        #proxy support
        # if self.useProxy == True:
            # print 'getURLRequestData USE PROXY'
            # customOpeners.append( urllib2.ProxyHandler({"http":self.proxyURL}) )
        
        if None != post_data:
            #print 'pCommon - getURLRequestData() -> post data: ' + str(post_data)
            if params.get('raw_post_data', False):
                dataPost = post_data
            else:
                dataPost = urllib.urlencode(post_data)
            req = urllib2.Request(params['url'], dataPost, headers)
        else:
            req = urllib2.Request(params['url'], None, headers)
 
        #print req
        if not params.get('return_data', False):
            out_data = urlOpen(req, customOpeners)
        else:
            gzip_encoding = False
            try:
                response = urlOpen(req, customOpeners)
                if response.info().get('Content-Encoding') == 'gzip':
                    gzip_encoding = True
                data = response.read()
                print response.info()
                response.close()
            except urllib2.HTTPError, e:
                print "out"
                if e.code == 404:
                    print '!!!!!!!! 404: getURLRequestData - page not found handled'
                    if e.fp.info().get('Content-Encoding') == 'gzip':
                        gzip_encoding = True
                    data = e.fp.read()
                    #e.msg
                    #e.headers
                else:
                    if e.code in [300, 302, 303, 307] and params.get('use_cookie', False) and params.get('save_cookie', False):
                        new_cookie = e.fp.info().get('Set-Cookie', '')
                        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> new_cookie[%s]" % new_cookie
                        #for cookieKey in params.get('cookie_items', {}).keys():
                        #    cj.clear('', '/', cookieKey)
                        cj.save(params['cookiefile'], ignore_discard = True)
                    raise e
    
            try:
                if gzip_encoding:
                    print 'Content-Encoding == gzip'
                    buf = StringIO(data)
                    f = gzip.GzipFile(fileobj=buf)
                    out_data = f.read()
                else:
                    out_data = data
            except:
                out_data = data
 
        if params.get('use_cookie', False) and params.get('save_cookie', False):
            cj.save(params['cookiefile'], ignore_discard = True)

        return out_data 
        
        
    def getPage(self, url, addParams = {}, post_data = None):
        
        try:
            
            addParams['url'] = url
            if 'return_data' not in addParams:
                addParams['return_data'] = True
            response = self.getURLRequestData(addParams, post_data)
            status = True
        except:
            printExc()
            response = None
            status = False
        print responde
        return (status, response)
     
    def getDataBeetwenReMarkers(self, data, pattern1, pattern2, withMarkers=True):
        match1 = pattern1.search(data)
        if None == match1 or -1 == match1.start(0): return False, ''
        match2 = pattern2.search(data[match1.end(0):])
        if None == match2 or -1 == match2.start(0): return False, ''
        
        if withMarkers:
            return True, data[match1.start(0): (match1.end(0) + match2.end(0)) ]
        else:
            return True, data[match1.end(0): (match1.end(0) + match2.start(0)) ]
        
    def parseNETUTV(self, url):
        #print("parserDIVEXPRESS url[%s]" % url)
        # example video: http://netu.tv/watch_video.php?v=WO4OAYA4K758
        
        def OIO(data, _0x84de):
            _0lllOI = _0x84de[0];
            enc = _0x84de[1];
            i = 0;
            while i < len(data):
                h1 = _0lllOI.find(data[i]);
                h2 = _0lllOI.find(data[i+1]);
                h3 = _0lllOI.find(data[i+2]);
                h4 = _0lllOI.find(data[i+3]);
                i += 4;
                bits = h1 << 18 | h2 << 12 | h3 << 6 | h4;
                o1 = bits >> 16 & 0xff;
                o2 = bits >> 8 & 0xff;
                o3 = bits & 0xff;
                if h3 == 64:
                    enc += chr(o1);
                else:
                    if h4 == 64:
                        enc += chr(o1) + chr(o2);
                    else:
                        enc += chr(o1) + chr(o2) + chr(o3);
            return enc
        
        def _0ll(string, _0x84de):
            ret = _0x84de[1]
            
            i = len(string) - 1
            while i >= 0:
                ret += string[i]
                i -= 1
            return ret
    
        #printDBG("parseNETUTV url[%s]\n" % url)
        #http://netu.tv/watch_video.php?v=ODM4R872W3S9
        match = re.search("=([0-9A-Z]+?)[^0-9^A-Z]", url + '|' )
        playerUrl = "http://hqq.tv/player/embed_player.php?vid=%s&autoplay=no" % match.group(1)
        print playerUrl
        HTTP_HEADER= { 'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:21.0) Gecko/20100101 Firefox/21.0',
                       'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' }
        #HTTP_HEADER['Referer'] = url
        #data = self.getPage(playerUrl, {'header' : HTTP_HEADER})
        
        oRequestHandler = cRequestHandler(self.__sUrl)
        data = oRequestHandler.request()
        data = base64.b64decode(re.search('base64\,([^"]+?)"', data).group(1))
        
        l01 = re.search("='([^']+?)'", data).group(1)
        _0x84de = re.search("var _0x84de=\[([^]]+?)\]", data).group(1)
        _0x84de = re.compile('"([^"]*?)"').findall(_0x84de)
        
        data = OIO( _0ll(l01, _0x84de), _0x84de )
        data = re.search("='([^']+?)'", data).group(1).replace('%', '\\').decode('unicode-escape').encode('UTF-8')
        
        data = re.compile('<input name="([^"]+?)" [^>]+? value="([^"]+?)">').findall(data)
        post_data = {}
        for idx in range(len(data)):
            post_data[ data[idx][0] ] = data[idx][1]
        
        oRequest = cRequestHandler(playerUrl)
        oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequest.addHeaderEntry('Referer', playerUrl)
        for aEntry in data:
            oRequest.addParameters(aEntry[0], aEntry[1])
        
        data = oRequest.request()
        aHeader = oRequest.getResponseHeader();
        RealUrl = oRequest.getRealUrl()
        #sReponseCookie = aHeader.getheader("Set-Cookie")
        sPhpSessionId = self.__getPhpSessionId(aHeader)
        #data = self.getPage(playerUrl, {'header' : HTTP_HEADER}, post_data)
        #CParsingHelper.writeToFile('/home/sulge/test.html', data)
        print aHeader
        print data.read()
        
        def getUtf8Str(st):
            idx = 0
            st2 = ''
            while idx < len(st):
                st2 += '\\u0' + st[idx:idx + 3]
                idx += 3
            return st2.decode('unicode-escape').encode('UTF-8')
        
        file_vars = self.getDataBeetwenMarkers(data, 'Uppod(', ')', False)[1]
        print "lalala"
        print file_vars
        file_vars = self.getDataBeetwenMarkers(data, 'file:', ',', False)[1].strip()
        file_vars = file_vars.split('+')
 
        file_url = ''
        for file_var in file_vars:
            file_var = file_var.strip()
            if 0 < len(file_var):
                match = re.search('''["']([^"]*?)["']''', file_var)
                if match:
                    file_url += match.group(1)
                else:
                    file_url += re.search('''var[ ]+%s[ ]*=[ ]*["']([^"]*?)["']''' % file_var, data).group(1)
                
        if file_url.startswith('#') and 3 < len(file_url):
            file_url = getUtf8Str(file_url[1:])
        
        print "[[[[[[[[[[[[[[[[[[[[[[%r]" % file_url
        
        if file_url.startswith('http'):
            return file_url
        return False     
    
    def __getMediaLinkForGuest(self):
        
        
        #host = self.parseNETUTV(self.__sUrl)
        
        
        oRequest = cRequestHandler('http://netu.tv/watch_video.php?v=S7DGB15KBN6N')
        sHtmlContent = oRequest.request()
        aHeader = oRequest.getResponseHeader()
        sPhpSessionId = self.__getPhpSessionId(aHeader)
        
        
        sPattern = '<meta property="og:image" content="([^"]+)" />'
        
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        print sHtmlContent

        if (aResult[0] == True):
            api_call = aResult[1][0]
            return True, api_call          
            
        return False, False
        
        
