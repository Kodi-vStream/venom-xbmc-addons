# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError

from resources.hosters.hoster import iHoster
from resources.lib.parser import cParser
from resources.lib.comaddon import dialog


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'mailru', 'MailRu')

    def _getMediaLinkForGuest(self):
        api_call = False

        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

        headers = {"User-Agent": UA}

        req1 = urllib2.Request(self._url, None, headers)
        resp1 = urllib2.urlopen(req1)
        sHtmlContent = resp1.read()
        resp1.close()

        sPattern = '{"metadataUrl":"([^"]+)",'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        vurl = 'http://my.mail.ru/' + aResult[1][0]

        req = urllib2.Request(vurl, None, headers)

        try:
            response = urllib2.urlopen(req)
        except UrlError as e:
            print(e.read())
            print(e.reason)

        data = response.read()
        head = response.headers
        response.close()

        # get cookie
        cookies = ''
        if 'Set-Cookie' in head:
            oParser = cParser()
            sPattern = '(?:^|,) *([^;,]+?)=([^;,\/]+?);'
            aResult = oParser.parse(str(head['Set-Cookie']), sPattern)
            # print(aResult)
            if aResult[0] is True:
                for cook in aResult[1]:
                    cookies = cookies + cook[0] + '=' + cook[1] + ';'

        sPattern = '{"url":"([^"]+)",.+?"key":"(\d+p)"}'
        aResult = oParser.parse(data, sPattern)
        if aResult[0] is True:
            # initialisation des tableaux
            url = []
            qua = []
            # Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            # Affichage du tableau
            api_call = dialog().VSselectqual(qua, url)

        if api_call:
            return True, 'http:' + api_call + '|User-Agent=' + UA + '&Cookie=' + cookies

        return False, False
