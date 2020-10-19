# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError
    from urllib2 import HTTPError as HttpError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError
    from urllib.error import HTTPError as HttpError

import xbmc

from resources.lib.util import urlEncode
from resources.lib.comaddon import addon, dialog, VSlog, VSPath


class cRequestHandler:
    REQUEST_TYPE_GET = 0
    REQUEST_TYPE_POST = 1

    def __init__(self, sUrl):
        self.__sUrl = sUrl
        self.__sRealUrl = ''
        self.__cType = 0
        self.__aParamaters = {}
        self.__aParamatersLine = ''
        self.__aHeaderEntries = []
        self.removeBreakLines(True)
        self.removeNewLines(True)
        self.__setDefaultHeader()
        self.__timeout = 30
        self.__bRemoveNewLines = False
        self.__bRemoveBreakLines = False
        self.__sResponseHeader = ''
        self.BUG_SSL = False
        self.__enableDNS = False

    def removeNewLines(self, bRemoveNewLines):
        self.__bRemoveNewLines = bRemoveNewLines

    def removeBreakLines(self, bRemoveBreakLines):
        self.__bRemoveBreakLines = bRemoveBreakLines

    def setRequestType(self, cType):
        self.__cType = cType

    def setTimeout(self, valeur):
        self.__timeout = valeur

    def disableRedirection(self):
        class NoRedirection(urllib2.HTTPErrorProcessor):
            def http_response(self, request, response):
                code, msg, hdrs = response.code, response.msg, response.info()

                return response
            
            https_response = http_response

        opener = urllib2.build_opener(NoRedirection)
        urllib2.install_opener(opener)

    def addHeaderEntry(self, sHeaderKey, sHeaderValue):
        for sublist in self.__aHeaderEntries:
            if sHeaderKey in sublist:
                self.__aHeaderEntries.remove(sublist)
        aHeader = {sHeaderKey: sHeaderValue}
        self.__aHeaderEntries.append(aHeader)

    def addParameters(self, sParameterKey, mParameterValue):
        self.__aParamaters[sParameterKey] = mParameterValue

    def addParametersLine(self, mParameterValue):
        self.__aParamatersLine = mParameterValue

    # egg addMultipartFiled({'sess_id': sId, 'upload_type': 'url', 'srv_tmp_url': sTmp})
    def addMultipartFiled(self, fields):
        mpartdata = MPencode(fields)
        self.__aParamatersLine = mpartdata[1]
        self.addHeaderEntry('Content-Type', mpartdata[0] )
        self.addHeaderEntry('Content-Length', len(mpartdata[1]))

    # Je sais plus si elle gere les doublons
    def getResponseHeader(self):
        return self.__sResponseHeader

    # url after redirects
    def getRealUrl(self):
        return self.__sRealUrl

    def GetCookies(self):
        if not self.__sResponseHeader:
            return ''
        if 'Set-Cookie' in self.__sResponseHeader:
            import re

            c = self.__sResponseHeader.get('set-cookie')

            c2 = re.findall('(?:^|,) *([^;,]+?)=([^;,]+?);', c)
            if c2:
                cookies = ''
                for cook in c2:
                    cookies = cookies + cook[0] + '=' + cook[1] + ';'
                cookies = cookies[:-1]
                return cookies
        return ''

    def request(self):
        # Supprimee car deconne si url contient ' ' et '+' en meme temps
        # self.__sUrl = self.__sUrl.replace(' ', '+')
        return self.__callRequest()

    def getRequestUri(self):
        return self.__sUrl + '?' + urlEncode(self.__aParamaters)

    def __setDefaultHeader(self):
        self.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
        self.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        self.addHeaderEntry('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')

    def __callRequest(self):
        if self.__enableDNS:
            import socket
            self.save_getaddrinfo = socket.getaddrinfo
            socket.getaddrinfo = self.new_getaddrinfo

        if self.__aParamatersLine:
            sParameters = self.__aParamatersLine
            if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                sParameters = self.__aParamatersLine.encode("utf-8")
            else:
                sParameters = self.__aParamatersLine                
        else:
            sParameters = urlEncode(self.__aParamaters)
            if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                sParameters = sParameters.encode()

        if (self.__cType == cRequestHandler.REQUEST_TYPE_GET):
            if (len(sParameters) > 0):
                if (self.__sUrl.find('?') == -1):
                    self.__sUrl = self.__sUrl + '?' + str(sParameters)
                    sParameters = ''
                else:
                    self.__sUrl = self.__sUrl + '&' + str(sParameters)
                    sParameters = ''

        if (len(sParameters) > 0):
            oRequest = urllib2.Request(self.__sUrl, sParameters)
        else:
            oRequest = urllib2.Request(self.__sUrl)

        for aHeader in self.__aHeaderEntries:
            for sHeaderKey, sHeaderValue in aHeader.items():
                oRequest.add_header(sHeaderKey, sHeaderValue)

        sContent = ''
        try:

            if self.BUG_SSL:
                VSlog('Retrying with SSL bug')
                import ssl
                gcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
                oResponse = urllib2.urlopen(oRequest, timeout=self.__timeout, context=gcontext)
            else:
                oResponse = urllib2.urlopen(oRequest, timeout=self.__timeout)

            self.__sResponseHeader = oResponse.info()

            #En python 3 on doit décoder la reponse
            if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19' and not self.__sResponseHeader.get('Content-Encoding') == 'gzip':
                sContent = decodeHTML(oResponse, self.__sResponseHeader, zlibMode = False)

            else:
                sContent = oResponse.read()

            # compressed page ?
            if self.__sResponseHeader.get('Content-Encoding') == 'gzip':
                import zlib
                sContent = zlib.decompress(sContent, zlib.MAX_WBITS | 16)
                
                if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                    sContent = decodeHTML(sContent, self.__sResponseHeader, zlibMode = True)

            # https://bugs.python.org/issue4773
            self.__sRealUrl = oResponse.geturl()
            self.__sResponseHeader = oResponse.info()

            oResponse.close()

        except HttpError as e:
            if e.code == 503:

                # Protected by cloudFlare ?
                from resources.lib import cloudflare
                if cloudflare.CheckIfActive(e.read()):
                    self.__sResponseHeader = e.hdrs
                    cookies = self.GetCookies()
                    VSlog('Page protegee par cloudflare')
                    CF = cloudflare.CloudflareBypass()
                    sContent = CF.GetHtml(self.__sUrl, e.read(), cookies, sParameters, oRequest.headers)
                    self.__sRealUrl, self.__sResponseHeader = CF.GetReponseInfo()
                else:
                    sContent = e.read()
                    self.__sRealUrl = e.geturl()
                    self.__sResponseHeader = e.headers()

            else:
                try:
                    VSlog("%s (%d),%s" % (addon().VSlang(30205), e.code, self.__sUrl))
                    self.__sRealUrl = e.geturl()
                    self.__sResponseHeader = e.headers
                    sContent = e.read()
                except:
                    sContent = ''

            if not sContent:
                dialog().VSerror("%s (%d),%s" % (addon().VSlang(30205), e.code, self.__sUrl))

        except UrlError as e:
            if 'CERTIFICATE_VERIFY_FAILED' in str(e.reason) and self.BUG_SSL == False:
                self.BUG_SSL = True
                return self.__callRequest()
            elif 'getaddrinfo failed' in str(e.reason) and self.__enableDNS == False:
                # Retry with DNS only if addon is present
                import xbmcvfs
                if xbmcvfs.exists('special://home/addons/script.module.dnspython/'):
                    self.__enableDNS = True
                    return self.__callRequest()
                else:
                    error_msg = addon().VSlang(30470)
            else:
                error_msg = "%s (%s),%s" % (addon().VSlang(30205), e.reason, self.__sUrl)

            dialog().VSerror(error_msg)
            sContent = ''

        if sContent:
            if (self.__bRemoveNewLines == True):
                sContent = sContent.replace("\n", "")
                sContent = sContent.replace("\r\t", "")

            if (self.__bRemoveBreakLines == True):
                sContent = sContent.replace("&nbsp;", "")

        if self.__enableDNS:
            socket.getaddrinfo = self.save_getaddrinfo
            self.__enableDNS = False

        return sContent

    def getHeaderLocationUrl(self):        
        opened = urllib2.urlopen(self.__sUrl)
        return opened.geturl()

    def new_getaddrinfo(self, *args):
        try:
            import sys
            import dns.resolver

            path = VSPath('special://home/addons/script.module.dnspython/lib/').decode('utf-8')
            if path not in sys.path:
                sys.path.append(path)
            host = args[0]
            port = args[1]
            # Keep the domain only: http://example.com/foo/bar => example.com
            if "//" in host:
                host = host[host.find("//"):]
            if "/" in host:
                host = host[:host.find("/")]
            resolver = dns.resolver.Resolver(configure=False)
            # Résolveurs DNS ouverts: https://www.fdn.fr/actions/dns/
            resolver.nameservers = ['80.67.169.12', '2001:910:800::12', '80.67.169.40', '2001:910:800::40']
            answer = resolver.query(host, 'a')
            host_found = str(answer[0])
            VSlog("new_getaddrinfo found host %s" % host_found)
            # Keep same return schema as socket.getaddrinfo (family, type, proto, canonname, sockaddr)
            return [(2, 1, 0, '', (host_found, port)), (2, 1, 0, '', (host_found, port))]
        except Exception as e:
            VSlog("new_getaddrinfo ERROR: {0}".format(e))
            return self.save_getaddrinfo(*args)

#Decode le contenu de la page html sous Python 3
def decodeHTML(oResponse, ResponseHeader, zlibMode=False):
    image_formats = ("image/png", "image/jpeg", "image/jpg", "application/download")

    #Ne pas décoder les contenu en bytes.
    if not ResponseHeader.get('Content-Type') in image_formats:
        if zlibMode == False:
            sContent = oResponse.read()

        else:
            #Unique maniere de formatter la page apres le passage de zlib.
            sContent = str(oResponse, encoding="utf8", errors='ignore').encode("utf-8").decode('unicode-escape')
            return sContent

        #Corrige l'affichage des accentes, malheureusement il n'y a pas de solution unique.
        if ResponseHeader.get_content_charset():
            encoding = ResponseHeader.get_content_charset()

        else:
            encoding = 'utf-8'
        try:
            try:
                sContent = sContent.decode()
            except:
                pass
            sContent = str(sContent, encoding)
        except:
            sContent = str(sContent)
        else:
            pass

        #Formatter correctement le contenu de la page.
        try:
            sContent = sContent.encode().decode('unicode-escape')
        except:
            pass

    else:
        sContent = oResponse.read()

    return sContent

# ******************************************************************************
# from https://github.com/eliellis/mpart.py
# ******************************************************************************
def MPencode(fields):
    import mimetypes
    random_boundary = __randy_boundary()
    content_type = "multipart/form-data, boundary=%s" % random_boundary

    form_data = []

    if fields:
        for (key, value) in fields.iteritems():
            if not hasattr(value, 'read'):
                itemstr = '--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (random_boundary, key, value)
                form_data.append(itemstr)
            elif hasattr(value, 'read'):
                with value:
                    file_mimetype = mimetypes.guess_type(value.name)[0] if mimetypes.guess_type(value.name)[0] else 'application/octet-stream'
                    itemstr = '--%s\r\nContent-Disposition: form-data; name="%s"; filename="%s"\r\nContent-Type: %s\r\n\r\n%s\r\n' % (random_boundary, key, value.name, file_mimetype, value.read())
                form_data.append(itemstr)
            else:
                raise Exception(value, 'Field is neither a file handle or any other decodable type.')
    else:
        pass

    form_data.append('--%s--\r\n' % random_boundary)

    return content_type, ''.join(form_data)


def __randy_boundary(length=10, reshuffle=False):
    import string
    import random

    character_string = string.letters + string.digits
    boundary_string = []
    for i in range(0, length):
        rand_index = random.randint(0, len(character_string) - 1)
        boundary_string.append(character_string[rand_index])
    if reshuffle:
        random.shuffle(boundary_string)
    else:
        pass
    return ''.join(boundary_string)
