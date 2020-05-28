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

import re

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.packer import cPacker
from resources.lib.parser import cParser

# Remarque : meme code que vodlocker

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'


def ASCIIDecode(string):

    i = 0
    l = len(string)
    ret = ''
    while i < l:
        c = string[i]
        if string[i:(i + 2)] == '\\x':
            c = chr(int(string[(i + 2):(i + 4)], 16))
            i += 3
        if string[i:(i + 2)] == '\\u':
            cc = int(string[(i + 2):(i + 6)], 16)
            if cc > 256:
                # ok c'est de l'unicode, pas du ascii
                return ''
            c = chr(cc)
            i += 5
        ret = ret + c
        i = i + 1

    return ret


def GetHtml(url, headers):
    request = urllib2.Request(url, None, headers)
    reponse = urllib2.urlopen(request)
    sCode = reponse.read()
    reponse.close()

    return sCode


def UnlockUrl(url2=None):
    headers9 = {
        'User-Agent': UA,
        'Referer': 'https://www.flashx.co/dl?playthis'
    }

    url1 = 'https://www.flashx.co/js/code.js'
    if url2:
        url1 = url2

    if not url1.startswith('http'):
        url1 = 'https:' + url1

    VSlog('Test unlock url :' + url1)

    oRequest = cRequestHandler(url1)
    oRequest.addParameters('User-Agent', UA)
    # oRequest.addParameters('Accept', '*/*')
    # oRequest.addParameters('Accept-Encoding', 'gzip, deflate, br')
    # oRequest.addParameters('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addParameters('Referer', 'https://www.flashx.co/dl?playthis')
    code = oRequest.request()

    url = ''
    if not code:
        url = oRequest.getRealUrl()
        VSlog('Redirection :' + url)
    else:
        # VSlog(code)
        aResult = re.search("!= null\){\s*\$.get\('([^']+)', *{(.+?)}", code, re.DOTALL)
        if aResult:
            dat = aResult.group(2)
            dat = dat.replace("'", '')
            dat = dat.replace(" ", '')

            dat2 = dict(x.split(':') for x in dat.split(','))

            dat3 = aResult.group(1) + '?'
            for i, j in dat2.items():
                dat3 = dat3 + str(i) + '=' + str(j) + '&'

            url = dat3[:-1]

    # url = 'https://www.flashx.tv/flashx.php?fxfx=6'

    if url:
        VSlog('Good Url :' + url1)
        VSlog(url)
        GetHtml(url, headers9)
        return True

    VSlog('Bad Url :' + url1)

    return False


def LoadLinks(htmlcode):
    VSlog('Scan des liens')

    host = 'https://www.flashx.tv'
    sPattern = '[\("\'](https*:)*(\/[^,"\'\)\s]+)[\)\'"]'
    aResult = re.findall(sPattern, htmlcode, re.DOTALL)

    # VSlog(str(aResult))
    for http, urlspam in aResult:
        sUrl = urlspam

        if http:
            sUrl = http + sUrl

        sUrl = sUrl.replace('/\/', '//')
        sUrl = sUrl.replace('\/', '/')

        # filtrage mauvaise url
        if (sUrl.count('/') < 2) or ('<' in sUrl) or ('>' in sUrl) or (len(sUrl) < 15):
            continue
        if '[' in sUrl or ']' in sUrl:
            continue
        if '.jpg' in sUrl or '.png' in sUrl:
            continue

        # VSlog('test : ' + sUrl)

        if '\\x' in sUrl or '\\u' in sUrl:
            sUrl = ASCIIDecode(sUrl)
            if not sUrl:
                continue

        if sUrl.startswith('//'):
            sUrl = 'http:' + sUrl

        if sUrl.startswith('/'):
            sUrl = host + sUrl

        # Url ou il ne faut pas aller
        if 'dok3v' in sUrl:
            continue

        # pour test
        if ('.js' not in sUrl) or ('.cgi' not in sUrl):
            continue
        # if 'flashx' in sUrl:
            # continue

        headers8 = {'User-Agent': UA,
                    'Referer': 'https://www.flashx.tv/dl?playthis'
                    }

        try:
            request = urllib2.Request(sUrl, None, headers8)
            reponse = urllib2.urlopen(request)
            sCode = reponse.read()
            reponse.close()
            # VSlog('Worked ' + sUrl)
        except HttpError as e:
            if not e.geturl() == sUrl:
                try:
                    headers9 = {
                        'User-Agent': UA,
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate, br'
                        }
                    request = urllib2.Request(e.geturl().replace('https', 'http'), None, headers9)
                    reponse = urllib2.urlopen(request)
                    sCode = reponse.read()
                    reponse.close()
                    # VSlog('Worked ' + sUrl)
                except HttpError as e:
                    VSlog(str(e.code))
                    # VSlog(e.read())
                    VSlog('Redirection Blocked ' + sUrl + ' Red ' + e.geturl())
                    pass
            else:
                # VSlog('Blocked ' + sUrl)
                VSlog(str(e.code))
                VSlog('>>' + e.geturl())
                VSlog(e.read())

    VSlog('fin des unlock')


class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'FlashX'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR] [COLOR khaki]' + self.__sHD + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'flashx'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return ''

    def GetRedirectHtml(self, web_url, sId, NoEmbed=False):

        headers = {
            # 'Host': 'www.flashx.tv',
            'User-Agent': UA,
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            # 'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'http://embed.flashx.tv/embed.php?c=' + sId,
            'Accept-Encoding': 'identity'
            }

        MaxRedirection = 3
        while MaxRedirection > 0:

            # generation headers
            # headers2 = headers
            # headers2['Host'] = self.GetHost(web_url)

            VSlog(str(MaxRedirection) + ' Test sur : ' + web_url)
            request = urllib2.Request(web_url, None, headers)

            redirection_target = web_url

            try:
                # ok ca a enfin marche
                reponse = urllib2.urlopen(request)
                sHtmlContent = reponse.read()
                reponse.close()

                if not (reponse.geturl() == web_url) and not (reponse.geturl() == ''):
                    redirection_target = reponse.geturl()
                else:
                    break
            except UrlError as e:
                if (e.code == 301) or (e.code == 302):
                    redirection_target = e.headers['Location']
                else:
                    # VSlog(str(e.code))
                    # VSlog(str(e.read()))
                    return False

            web_url = redirection_target

            if 'embed' in redirection_target and NoEmbed:
                # rattage, on a pris la mauvaise url
                VSlog('2')
                return False

            MaxRedirection = MaxRedirection - 1

        return sHtmlContent

    def __getIdFromUrl(self, sUrl):
        sPattern = "https*:\/\/((?:www.|play.)?flashx.+?)\/(?:playvid-)?(?:embed-)?(?:embed.+?=)?(-*[0-9a-zA-Z]+)?(?:.html)?"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0][1]

        return ''

    def GetHost(self, sUrl):
        oParser = cParser()
        sPattern = 'https*:\/\/(.+?)\/'
        aResult = oParser.parse(sUrl, sPattern)
        if aResult[0]:
            return aResult[1][0]
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = 'http://' + self.GetHost(sUrl) + '/embed.php?c=' + self.__getIdFromUrl(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return ''

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def CheckGoodUrl(self, url):

        # VSlog('test de ' + url)
        headers = {'User-Agent': UA
                   # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   # 'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                   # 'Accept-Encoding': 'gzip, deflate, br',
                   # 'Host': 'openload.co',
                   # 'Referer': referer
                   }

        req = urllib2.Request(url)
        res = urllib2.urlopen(req)
        # pour afficher contenu
        # VSlog(res.read())
        # pour afficher header
        # VSlog(str(res.info()))
        # Pour afficher redirection
        # VSlog('red ' + res.geturl())

        if 'embed' is res.geturl():
            return False

        html = res.read()

        res.close()

        return res

    def __getMediaLinkForGuest(self):
        api_call = False

        oParser = cParser()

        # on recupere le host actuel
        HOST = self.GetHost(self.__sUrl)

        # on recupere l'ID
        sId = self.__getIdFromUrl(self.__sUrl)
        if sId == '':
            VSlog("Id prb")
            return False, False

        # on ne garde que les chiffres
        # sId = re.sub(r'-.+', '', sId)

        # on cherche la vraie url
        sHtmlContent = self.GetRedirectHtml(self.__sUrl, sId)

        # fh = open('c:\\test.txt', "w")
        # fh.write(sHtmlContent)
        # fh.close()

        sPattern = 'href=["\'](https*:\/\/www\.flashx[^"\']+)'
        AllUrl = re.findall(sPattern, sHtmlContent, re.DOTALL)
        # VSlog(str(AllUrl))

        # Disabled for the moment
        if (False):
            if AllUrl:
                # Need to find which one is the good link
                # Use the len don't work
                for i in AllUrl:
                    if i[0] == '':
                        web_url = i[1]
            else:
                return False,False
        else:
            web_url = AllUrl[0]

        web_url = AllUrl[0]

        # Requests to unlock video
        # unlock fake video
        LoadLinks(sHtmlContent)
        # unlock bubble
        unlock = False
        url2 = re.findall('["\']([^"\']+?\.js\?cache.+?)["\']', sHtmlContent, re.DOTALL)
        if not url2:
            VSlog('No special unlock url find')
        for i in url2:
            unlock = UnlockUrl(i)
            if unlock:
                break

        if not unlock:
            VSlog('No special unlock url working')
            return False, False

        # get the page
        sHtmlContent = self.GetRedirectHtml(web_url, sId, True)

        if sHtmlContent == False:
            VSlog('Passage en mode barbare')
            # ok ca a rate on passe toutes les url de AllUrl
            for i in AllUrl:
                if not i == web_url:
                    sHtmlContent = self.GetRedirectHtml(i, sId, True)
                    if sHtmlContent:
                        break

        if not sHtmlContent:
            return False, False

        if 'reload the page!' in sHtmlContent:
            # VSlog("page bloquée")

            # On recupere la bonne url
            sGoodUrl = web_url

            # on recupere la page de refresh
            sPattern = 'reload the page! <a href="([^"]+)">!! <b>'
            aResult = re.findall(sPattern, sHtmlContent)
            if not aResult:
                return False, False
            sRefresh = aResult[0]

            # on recupere le script de debloquage
            sPattern = "<script type='text/javascript' src='([^']+)'><\/script>"
            aResult = re.findall(sPattern, sHtmlContent)
            if not aResult:
                return False, False

            deblockurl = aResult[0]
            if deblockurl.startswith('//'):
                deblockurl = 'http:' + deblockurl

            # on debloque la page
            sHtmlContent = self.GetRedirectHtml(deblockurl, sId)

            # lien speciaux ?
            if sRefresh.startswith('./'):
                sRefresh = 'http://' + self.GetHost(sGoodUrl) + sRefresh[1:]

            # on rafraichit la page
            sHtmlContent = self.GetRedirectHtml(sRefresh, sId)

            # et on re-recupere la page
            sHtmlContent = self.GetRedirectHtml(sGoodUrl, sId)

        if (False):

            # A t on le lien code directement?
            sPattern = "(\s*eval\s*\(\s*function(?:.|\s)+?)<\/script>"
            aResult = re.findall(sPattern, sHtmlContent)

            if (aResult):
                # VSlog("lien code")

                AllPacked = re.findall('(eval\(function\(p,a,c,k.*?)\s+<\/script>', sHtmlContent, re.DOTALL)
                if AllPacked:
                    for i in AllPacked:
                        sUnpacked = cPacker().unpack(i)
                        sHtmlContent = sUnpacked
                        if "file" in sHtmlContent:
                            break
                else:
                    return False, False

        # decodage classique
        sPattern = '{file:"([^",]+)",label:"([^"<>,]+)"}'
        sPattern = '{src: *\'([^"\',]+)\'.+?label: *\'([^"<>,\']+)\''
        aResult = oParser.parse(sHtmlContent, sPattern)

        # VSlog(str(aResult))

        if (aResult[0] == True):
            # initialisation des tableaux
            url = []
            qua = []

            # Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))

            # Affichage du tableau
            api_call = dialog().VSselectqual(qua, url)

        if (api_call):
            return True, api_call

        return False, False
