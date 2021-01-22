import re
import time

from resources.lib.comaddon import VSlog, dialog
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import GestionCookie
from resources.lib.util import QuotePlus

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'


class Stormwall(object):
    def __init__(self):
        self.state = False
        self.hostComplet = ''
        self.host = ''
        self.url = ''
        self.cook = ''

    def get_jhash(self, b):
        x = 123456789
        i = 0
        k = 0

        while (i < 1677696):
            x = (x + b ^ x + x % 3 + x % 17 + b ^ i) % (16776960)
            if (x % 117 == 0):
                k = (k + 1) % 1111
            i = i + 1

        return k

    def CheckIfActive(self, html):
        if 'stormwall' in str(html):
            return True
        return False

    def DecryptCookie(self, content):
        jhash = int(re.search('get_jhash\((.+?)\);', str(content)).group(1))
        Jhash = self.get_jhash(jhash)

        return Jhash

    def GetHtml(self, url, data=None):
        self.hostComplet = re.sub('(https*:\/\/[^/]+)(\/*.*)', '\\1', url)
        self.host = re.sub('https*:\/\/', '', self.hostComplet)
        self.url = url

        # on cherche des precedents cookies
        cookies = GestionCookie().Readcookie(self.host.replace('.', '_'))
        htmlcontent = self.htmlrequest(url, cookies, data)

        if not self.CheckIfActive(htmlcontent):
            return htmlcontent
        elif "recaptcha3key" in htmlcontent:
            dialog().VSok('Recaptcha active, reessayer plus tard')
            return htmlcontent

        # on cherche le nouveau cookie
        try:
            cookies = str(self.DecryptCookie(htmlcontent))
        except:
            VSlog('Erreur decodage Stormwall')
            return ''

        VSlog('Protection Stormwall active')

        GestionCookie().SaveCookie(self.host.replace('.', '_'), cookies)

        time.sleep(5)
        htmlcontent = self.htmlrequest(url, cookies, data)

        return htmlcontent

    def htmlrequest(self, url, cookies, data):
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.disableSSL()
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
        oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
        if cookies:
            oRequestHandler.addHeaderEntry("Cookie", self.cook + "; _JHASH__=" + cookies + "; _JUA__=" + QuotePlus(UA))
        oRequestHandler.addHeaderEntry('Referer', url)
        sHtmlContent = oRequestHandler.request()
        self.cook = oRequestHandler.GetCookies()
        return sHtmlContent
