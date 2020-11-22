# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from requests import Session, Request, HTTPError
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
        self.__aHeaderEntries = {}
        self.removeBreakLines(True)
        self.removeNewLines(True)
        self.__setDefaultHeader()
        self.__timeout = 30
        self.__bRemoveNewLines = False
        self.__bRemoveBreakLines = False
        self.__sResponseHeader = ''
        self.BUG_SSL = False
        self.__enableDNS = False
        self.s = Session()

    def removeNewLines(self, bRemoveNewLines):
        self.__bRemoveNewLines = bRemoveNewLines

    def removeBreakLines(self, bRemoveBreakLines):
        self.__bRemoveBreakLines = bRemoveBreakLines

    def setRequestType(self, cType):
        self.__cType = cType

    def setTimeout(self, valeur):
        self.__timeout = valeur

    def addHeaderEntry(self, sHeaderKey, sHeaderValue):
        for sublist in list(self.__aHeaderEntries):
            if sHeaderKey in sublist:
                self.__aHeaderEntries.pop(sublist)

            if sHeaderKey == "Content-Length":
                sHeaderValue = str(sHeaderValue)

        aHeader = {sHeaderKey: sHeaderValue}
        self.__aHeaderEntries.update(aHeader)

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
        else:
            sParameters = urlEncode(self.__aParamaters)

        if (self.__cType == cRequestHandler.REQUEST_TYPE_GET):
            if (len(sParameters) > 0):
                if (self.__sUrl.find('?') == -1):
                    self.__sUrl = self.__sUrl + '?' + str(sParameters)
                    sParameters = ''
                else:
                    self.__sUrl = self.__sUrl + '&' + str(sParameters)
                    sParameters = ''

        sContent = ''

        if self.__cType == cRequestHandler.REQUEST_TYPE_GET:
            method = "GET"
        else:
            method = "POST"

        try:
            _request = Request(method, self.__sUrl, headers=self.__aHeaderEntries)
            if method in ['POST', 'PATCH', 'PUT']:
                self.__aHeaderEntries['content-type'] = 'application/x-www-form-urlencoded'
                _request.data = sParameters
            prepped = _request.prepare()
            oResponse = self.s.send(prepped, timeout=self.__timeout)

            self.__sResponseHeader = oResponse.headers
            sContent = oResponse.content.decode('unicode-escape')

        except HTTPError as e:
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

        if oResponse.status_code == 503:

            # Protected by cloudFlare ?
            from resources.lib import cloudflare
            if cloudflare.CheckIfActive(sContent):
                cookies = self.GetCookies()
                VSlog('Page protegee par cloudflare')
                CF = cloudflare.CloudflareBypass()
                sContent = CF.GetHtml(self.__sUrl, sContent, cookies, sParameters, oResponse.headers)
                self.__sRealUrl, self.__sResponseHeader = CF.GetReponseInfo()
            else:
                sContent = e.read()
                self.__sRealUrl = e.geturl()
                self.__sResponseHeader = e.headers()

        if not sContent:
            dialog().VSerror("%s (%d),%s" % (addon().VSlang(30205), oResponse.status_code, self.__sUrl))

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
