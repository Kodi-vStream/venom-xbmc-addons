# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from requests import post, Session, Request, RequestException, ConnectionError
from resources.lib.comaddon import addon, dialog, VSlog, VSPath, isMatrix
from json import loads, dumps
from resources.lib.util import urlEncode

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
        self.__Cookie = {}
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
        self.redirects = True
        self.verify = True
        self.json = {}

    #Desactive le ssl
    def disableSSL(self):
        self.verify = False

    #Empeche les redirections 
    def disableRedirect(self):
        self.redirects = False

    def removeNewLines(self, bRemoveNewLines):
        self.__bRemoveNewLines = bRemoveNewLines

    def removeBreakLines(self, bRemoveBreakLines):
        self.__bRemoveBreakLines = bRemoveBreakLines

    #Defini le type de requete
    #0 : pour un requete GET
    #1 : pour une requete POST
    def setRequestType(self, cType):
        self.__cType = cType

    #Permets de definir un timeout
    def setTimeout(self, valeur):
        self.__timeout = valeur

    #Ajouter un cookie dans le headers de la requete
    def addCookieEntry(self, sHeaderKey, sHeaderValue):
        aHeader = {sHeaderKey: sHeaderValue}
        self.__Cookie.update(aHeader)

    #Ajouter des parametre JSON
    def addJSONEntry(self, sHeaderKey, sHeaderValue):
        aHeader = {sHeaderKey: sHeaderValue}
        self.json.update(aHeader)

    #Ajouter un elements dans le headers de la requete
    def addHeaderEntry(self, sHeaderKey, sHeaderValue):
        for sublist in list(self.__aHeaderEntries):
            if sHeaderKey in sublist:
                self.__aHeaderEntries.pop(sublist)

            if sHeaderKey == "Content-Length":
                sHeaderValue = str(sHeaderValue)

        aHeader = {sHeaderKey: sHeaderValue}
        self.__aHeaderEntries.update(aHeader)

    #Ajout un parametre dans la requete
    def addParameters(self, sParameterKey, mParameterValue):
        self.__aParamaters[sParameterKey] = mParameterValue

    #Ajoute une ligne de parametre
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

    def request(self,jsonDecode=False):
        # Supprimee car deconne si url contient ' ' et '+' en meme temps
        # self.__sUrl = self.__sUrl.replace(' ', '+')
        return self.__callRequest(jsonDecode)

    #Recupere les cookies de la requete
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

    def __setDefaultHeader(self):
        self.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
        self.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        self.addHeaderEntry('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')

    def __callRequest(self, jsonDecode=False):
        if self.__enableDNS:
            import socket
            self.save_getaddrinfo = socket.getaddrinfo
            socket.getaddrinfo = self.new_getaddrinfo

        if self.__aParamatersLine:
            sParameters = self.__aParamatersLine            
        else:
            sParameters = self.__aParamaters

        if (self.__cType == cRequestHandler.REQUEST_TYPE_GET):
            if (len(sParameters) > 0):
                if (self.__sUrl.find('?') == -1):
                    self.__sUrl = self.__sUrl + '?' + str(sParameters)
                    sParameters = ''
                else:
                    self.__sUrl = self.__sUrl + '&' + str(sParameters)
                    sParameters = ''

        sContent = ''

        if self.BUG_SSL == True:
            self.verify = False

        if self.__cType == cRequestHandler.REQUEST_TYPE_GET:
            method = "GET"
        else:
            method = "POST"


        oResponse = None
        try:
            _request = Request(method, self.__sUrl, headers=self.__aHeaderEntries)
            if method in ['POST']:
                _request.data = sParameters

            if self.__Cookie:
                _request.cookies = self.__Cookie

            if self.json:
                _request.json = self.json

            prepped = _request.prepare()
            self.s.headers.update(self.__aHeaderEntries)

            oResponse = self.s.send(prepped, timeout=self.__timeout, allow_redirects=self.redirects, verify=self.verify)
            self.__sResponseHeader = oResponse.headers
            self.__sRealUrl = oResponse.url

            if jsonDecode == False:
                sContent = oResponse.content

                #Necessaire pour Python 3
                if isMatrix() and not 'youtube' in oResponse.url:
                    try:
                       sContent = sContent.decode('unicode-escape')
                    except:
                        try:
                            sContent = sContent.decode()
                        except:
                            pass
            else:
                sContent = oResponse.json()

        except ConnectionError as e:
            # Retry with DNS only if addon is present
            import xbmcvfs
            if xbmcvfs.exists('special://home/addons/script.module.dnspython/') and self.__enableDNS == False:
                self.__enableDNS = True
                return self.__callRequest()
            else:
                error_msg = addon().VSlang(30470)

        except RequestException  as e:
            if 'CERTIFICATE_VERIFY_FAILED' in str(e) and self.BUG_SSL == False:
                self.BUG_SSL = True
                return self.__callRequest()
            elif 'getaddrinfo failed' in str(e) and self.__enableDNS == False:
                # Retry with DNS only if addon is present
                import xbmcvfs
                if xbmcvfs.exists('special://home/addons/script.module.dnspython/'):
                    self.__enableDNS = True
                    return self.__callRequest()
                else:
                    error_msg = addon().VSlang(30470)
            else:
                error_msg = "%s (%s),%s" % (addon().VSlang(30205), e, self.__sUrl)

            dialog().VSerror(error_msg)
            sContent = ''

        if oResponse:
            if oResponse.status_code in [503,403]:
                if not "Forbidden" in sContent:
                    #Default
                    CLOUDPROXY_ENDPOINT = 'http://localhost:8191/v1'

                    json_session = False

                    try:
                        json_session = post(CLOUDPROXY_ENDPOINT, headers=self.__aHeaderEntries, data=dumps({
                            'cmd': 'sessions.list'
                        }))
                    except:
                        dialog().VSerror("%s" % ("Page protege par Cloudflare, veuillez executer  FlareSolverr."))

                    if json_session:
                        #On regarde si une session existe deja.
                        if json_session.json()['sessions']:
                            cloudproxy_session = json_session.json()['sessions'][0]
                        else:
                            json_session = post(CLOUDPROXY_ENDPOINT, headers=self.__aHeaderEntries, data=dumps({
                                'cmd': 'sessions.create'
                            }))
                            response_session = loads(json_session.text)
                            cloudproxy_session = response_session['session']

                        self.__aHeaderEntries['Content-Type'] = 'application/x-www-form-urlencoded' if (method == 'post') else 'application/json'

                        #Ont fait une requete.
                        json_response = post(CLOUDPROXY_ENDPOINT, headers=self.__aHeaderEntries, data=dumps({
                            'cmd': 'request.%s' % method.lower(),
                            'url': self.__sUrl,
                            'session': cloudproxy_session,
                            'postData': '%s' % urlEncode(sParameters) if (method.lower() == 'post') else ''
                        }))

                        http_code = json_response.status_code
                        response = loads(json_response.text)
                        if 'solution' in response:
                            if self.__sUrl != response['solution']['url']:
                                self.__sRealUrl = response['solution']['url']

                            sContent = response['solution']['response']

            if oResponse and not sContent:
                #Ignorer ces deux codes erreurs.
                ignoreStatus = [200,302]
                if oResponse.status_code not in ignoreStatus:
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

    def new_getaddrinfo(self, *args):
        try:
            import sys
            import dns.resolver

            if isMatrix():
                path = VSPath('special://home/addons/script.module.dnspython/lib/')
            else:
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
        try:
            data = fields.iteritems()
        except:
            data = fields.items()

        for (key, value) in data:
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

    if isMatrix():
        character_string = string.ascii_letters + string.digits
    else:
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
