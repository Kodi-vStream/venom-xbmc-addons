# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
# alors la j'ai pas le courage
from resources.lib.comaddon import VSlog
from resources.lib.config import GestionCookie
from requests.adapters import HTTPAdapter
from collections import OrderedDict
import re, ssl, requests  #, os, time, json, random
from requests.sessions import Session
from resources.lib.util import urlEncode

try:  # Python 2
    from urlparse import urlparse
except ImportError:  # Python 3
    from urllib.parse import urlparse

# old version
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

# #####################################################################################################################
#
# Ok so a big thx to VeNoMouS for this code
# From this url https://github.com/VeNoMouS/cloudscraper
# Franchement si vous etes content de voir revenir vos sites allez mettre une etoile sur son github.
#
# #####################################################################################################################


class CipherSuiteAdapter(HTTPAdapter):

    def __init__(self, cipherSuite=None, **kwargs):
        self.cipherSuite = cipherSuite

        if hasattr(ssl, 'PROTOCOL_TLS'):
            self.ssl_context = create_urllib3_context(
                    ssl_version=getattr(ssl, 'PROTOCOL_TLSv1_3', ssl.PROTOCOL_TLSv1_2),
                    ciphers=self.cipherSuite
                    )
        else:
            self.ssl_context = create_urllib3_context(ssl_version=ssl.PROTOCOL_TLSv1)

        super(CipherSuiteAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super(CipherSuiteAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super(CipherSuiteAdapter, self).proxy_manager_for(*args, **kwargs)

#######################################################################################################################


Mode_Debug = True

if (False):
    Mode_Debug = True
    import logging
    # These two lines enable debugging at httplib level (requests->urllib3->http.client)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # The only thing missing will be the response.body which is not logged.
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger('requests.packages.urllib3')
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

# ---------------------------------------------------------
# Gros probleme, mais qui a l'air de passer
# Le headers 'Cookie' apparait 2 fois, il faudrait lire la precedente valeur
# la supprimer et remettre la nouvelle avec les 2 cookies
# Non conforme au protocole, mais ca marche (pour le moment)
# -----------------------------------------------------------

# Cookie path
# C:\Users\BRIX\AppData\Roaming\Kodi\userdata\addon_data\plugin.video.vstream\

# Light method
# Ne marche que si meme user-agent
    # req = urllib.request.Request(sUrl, None, headers)
    # try:
        # response = urllib.request.urlopen(req)
        # sHtmlContent = response.read()
        # response.close()

    # except urllib.error.HTTPError as e:

        # if e.code == 503:
            # if CloudflareBypass().check(e.headers):
                # cookies = e.headers['Set-Cookie']
                # cookies = cookies.split(';')[0]
                # sHtmlContent = CloudflareBypass().GetHtml(sUrl, e.read(), cookies)

# Heavy method
# sHtmlContent = CloudflareBypass().GetHtml(sUrl)

# For memory
# http://www.jsfuck.com/

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'


class CloudflareBypass(object):
    def __init__(self):
        self.state = False
        self.HttpReponse = None
        self.Memorised_Headers = None
        self.Memorised_PostData = None
        self.Memorised_Cookies = None
        self.Header = None
        self.RedirectionUrl = None

    # Return param for head
    def GetHeadercookie(self, url):
        Domain = re.sub(r'https*:\/\/([^/]+)(\/*.*)', '\\1', url)
        cook = GestionCookie().Readcookie(Domain.replace('.', '_'))
        if cook == '':
            return ''

        return '|' + urlEncode({'User-Agent': UA, 'Cookie': cook})

    def ParseCookies(self, data):
        list = {}

        sPattern = '(?:^|[,;]) *([^;,]+?)=([^;,\/]+)'
        aResult = re.findall(sPattern, data)
        # VSlog(str(aResult))
        if (aResult):
            for cook in aResult:
                if 'deleted' in cook[1]:
                    continue
                list[cook[0]] = cook[1]
                # cookies = cookies + cook[0] + '=' + cook[1]+ ';'

        # VSlog(str(list))

        return list

    def SetHeader(self):
        head = OrderedDict()
        # Need to use correct order
        h = ['User-Agent', 'Accept', 'Accept-Language', 'Accept-Encoding', 'Connection', 'Upgrade-Insecure-Requests']
        v = [UA, 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'en-US,en;q=0.5', 'gzip, deflate', 'close', '1']
        for i in enumerate(h):
            k = checklowerkey(i[1], self.Memorised_Headers)
            if k:
                head[i[1]] = self.Memorised_Headers[k]
            else:
                head[i[1]] = v[i[0]]

        # optional headers
        if 'Referer' in self.Memorised_Headers:
            head['Referer'] = self.Memorised_Headers['Referer']

        if (False):
            # Normalisation because they are not case sensitive:
            Headers = ['User-Agent', 'Accept', 'Accept-Language', 'Accept-Encoding', 'Cache-Control', 'Dnt', 'Pragma', 'Connexion']
            Headers_l = [x.lower() for x in Headers]
            head2 = dict(head)
            for key in head2:
                if not key in Headers and key.lower() in Headers_l:
                    p = Headers_l.index(key.lower())
                    head[Headers[p]] = head[key]
                    del head[key]

        return head

    def GetReponseInfo(self):
        return self.RedirectionUrl, self.Header

    def GetHtml(self, url, htmlcontent='', cookies='', postdata=None, Gived_headers=''):

        # Memorise headers
        self.Memorised_Headers = Gived_headers

        # Memorise postdata
        self.Memorised_PostData = postdata

        # Memorise cookie
        self.Memorised_Cookies = cookies
        # VSlog(cookies)

        # cookies in headers?
        if Gived_headers != '':
            if Gived_headers.get('Cookie', None):
                if cookies:
                    self.Memorised_Cookies = cookies + '; ' + Gived_headers.get('Cookie')
                else:
                    self.Memorised_Cookies = Gived_headers['Cookie']

        # For debug
        if (Mode_Debug):
            VSlog('Headers present ' + str(Gived_headers))
            VSlog('url ' + url)
            if (htmlcontent):
                VSlog('code html ok')
            VSlog('cookies passés : ' + self.Memorised_Cookies)
            VSlog('post data :' + str(postdata))

        self.hostComplet = re.sub(r'(https*:\/\/[^/]+)(\/*.*)', '\\1', url)
        self.host = re.sub(r'https*:\/\/', '', self.hostComplet)
        self.url = url

        cookieMem = GestionCookie().Readcookie(self.host.replace('.', '_'))
        if not (cookieMem == ''):
            if (Mode_Debug):
                VSlog('cookies present sur disque :' + cookieMem )
            if not (self.Memorised_Cookies):
                cookies = cookieMem
            else:
                cookies = self.Memorised_Cookies + '; ' + cookieMem
        else:
            if (Mode_Debug):
                VSlog('Pas de cookies présent sur disque' )

        data = {}
        if postdata:
            method = 'POST'
            # Need to convert data to dictionnary
            d = postdata.split('&')
            for dd in d:
                ddd = dd.split('=')
                data[ddd[0]] = ddd[1]
        else:
            method = 'GET'

        from resources.lib import cloudscrape

        s = cloudscrape.create_scraper(browser={'custom': 'ScraperBot/1.0'})

        r = s.request(method, url, headers=self.SetHeader(), cookies=self.ParseCookies(cookies), data=data)
        # r = s.request(method, url)
        MemCookie = r.cookies.get_dict()

        if r:
            sContent = r.text.encode('utf-8')
            self.RedirectionUrl = r.url
            self.Header = r.headers
            VSlog('Page ok')
        else:
            VSlog('Erreur, delete cookie')
            sContent = ''
            # self.RedirectionUrl = r.url
            # self.Header = r.headers
            MemCookie = {}
            # r.cookies.clear()
            GestionCookie().DeleteCookie(self.host.replace('.', '_'))

        # fh = open('c:\\test.txt', 'w')
        # fh.write(sContent)
        # fh.close()

        # Memorisation des cookies
        c = ''
        cookie = MemCookie
        if cookie:
            for i in cookie:
                c = c + i + '=' + cookie[i] + ';'
            # Write them
            GestionCookie().SaveCookie(self.host.replace('.', '_'), c)
            if Mode_Debug:
                VSlog('Sauvegarde cookies: ' + str(c))

        return sContent


def checklowerkey(key, dict):
    for i in dict:
        if str(i.lower()) == str(key.lower()):
            return i
    return False


def checkpart(s, end='+'):
    p = 0
    pos = 0

    try:
        while (1):
            c = s[pos]

            if (c == '('):
                p = p + 1
            if (c == ')'):
                p = p - 1

            pos = pos + 1

            if (c == end) and (p == 0) and (pos > 1):
                break
    except:
        pass

    return s[:pos]


def CheckIfActive(data):
    if 'Checking your browser before accessing' in str(data):
        return True
    return False


def showInfo(sTitle, sDescription, iSeconds=0):
    if (iSeconds == 0):
        iSeconds = 1000
    else:
        iSeconds = iSeconds * 1000
