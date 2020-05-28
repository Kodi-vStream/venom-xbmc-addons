# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError

from resources.lib.comaddon import addon, dialog, VSlog
from resources.lib.config import GestionCookie
from resources.lib.parser import cParser
from resources.lib.util import urlEncode

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
headers = {'User-Agent': UA}


class NoRedirection(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        code, msg, hdrs = response.code, response.msg, response.info()

        return response

    https_response = http_response


class cPremiumHandler:
    ADDON = addon()
    DIALOG = dialog()

    def __init__(self, sHosterIdentifier):
        self.__sHosterIdentifier = sHosterIdentifier.lower()
        self.__sDisplayName = 'Premium mode'
        self.isLogin = False
        self.__LoginTry = False
        self.__ssl = False

        self.__Ispremium = False
        bIsPremium = self.ADDON.getSetting('hoster_' + str(self.__sHosterIdentifier) + '_premium')
        if (bIsPremium == 'true'):
            VSlog("Utilise compte premium pour hoster " + str(self.__sHosterIdentifier))
            self.__Ispremium = True
        else:
            VSlog("Utilise compte gratuit pour hoster: " + str(self.__sHosterIdentifier))

    def isPremiumModeAvailable(self):
        return self.__Ispremium

    def getUsername(self):
        sUsername = self.ADDON.getSetting('hoster_' + str(self.__sHosterIdentifier) + '_username')
        return sUsername

    def getPassword(self):
        sPassword = self.ADDON.getSetting('hoster_' + str(self.__sHosterIdentifier) + '_password')
        return sPassword

    def AddCookies(self):
        cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
        return 'Cookie=' + cookies

    def Checklogged(self, code):
        if 'uptobox' in self.__sHosterIdentifier:
            if '//uptobox.com/?op=logout&' in code or 'Success' in code:
                return True

        if 'onefichier' in self.__sHosterIdentifier:
            if 'premium' in code or 'jqueryFileTree' in code or '1fichier.com/logout' in code:  # test ok mais pas convaincu....
                return True

        return False

    def CheckCookie(self):
        cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
        if cookies != '':
            return True
        return False

    def Authentificate(self):

        # un seul essais par session, pas besoin de bombarder le serveur
        if self.__LoginTry:
            return False
        self.__LoginTry = True

        if not self.__Ispremium:
            return False

        post_data = {}

        if 'uptobox' in self.__sHosterIdentifier:
            url = 'https://uptobox.com/?op=login&referer=homepage'
            post_data['login'] = self.getUsername()
            post_data['password'] = self.getPassword()

        elif 'onefichier' in self.__sHosterIdentifier:
            url = 'https://1fichier.com/login.pl'
            post_data['mail'] = self.getUsername()
            post_data['pass'] = self.getPassword()
            post_data['lt'] = 'on'
            post_data['purge'] = 'on'
            post_data['valider'] = 'Send'
            self.__ssl = True

        elif 'uploaded' in self.__sHosterIdentifier:
            url = 'http://uploaded.net/io/login'
            post_data['id'] = self.getUsername()
            post_data['pw'] = self.getPassword()

        # si aucun de trouve on retourne
        else:
            return False

        if (self.__ssl):
            try:
                import ssl
                context = ssl._create_unverified_context()
            except:
                self.__ssl = False

        if 'uptobox' in self.__sHosterIdentifier:
            data = urlEncode(post_data)

            opener = urllib2.build_opener(NoRedirection)

            opener.addheaders = [('User-Agent', UA)]
            opener.addheaders.append(('Content-Type', 'application/x-www-form-urlencoded'))
            opener.addheaders.append(('Referer', str(url)))
            opener.addheaders.append(('Content-Length', str(len(data))))

            try:
                response = opener.open(url, data)
                head = response.info()
            except UrlError:
                return ''
        else:
            req = urllib2.Request(url, urlEncode(post_data), headers)

            try:
                if (self.__ssl):
                    response = urllib2.urlopen(req, context=context)
                else:
                    response = urllib2.urlopen(req)
            except UrlError as e:
                if getattr(e, "code", None) == 403:
                    # login denied
                    self.DIALOG.VSinfo('Authentification rate', self.__sDisplayName)
                elif getattr(e, "code", None) == 502:
                    # login denied
                    self.DIALOG.VSinfo('Authentification rate', self.__sDisplayName)
                elif getattr(e, "code", None) == 234:
                    # login denied
                    self.DIALOG.VSinfo('Authentification rate', self.__sDisplayName)
                else:
                    VSlog("debug" + str(getattr(e, "code", None)))
                    VSlog("debug" + str(getattr(e, "reason", None)))

                self.isLogin = False
                return False

            sHtmlContent = response.read()
            head = response.headers
            response.close()

        if 'uptobox' in self.__sHosterIdentifier:
            if 'xfss' in head['Set-Cookie']:
                self.isLogin = True
            else:
                self.DIALOG.VSinfo('Authentification rate', self.__sDisplayName)
                return False
        elif 'onefichier' in self.__sHosterIdentifier:
            if 'You are logged in. This page will redirect you.' in sHtmlContent:
                self.isLogin = True
            else:
                self.DIALOG.VSinfo('Authentification rate', self.__sDisplayName)
                return False
        elif 'uploaded' in self.__sHosterIdentifier:
            if sHtmlContent == '':
                self.isLogin = True
            else:
                self.DIALOG.VSinfo('Authentification rate', self.__sDisplayName)
                return False
        else:
            return False

        # get cookie
        cookies = ''
        if 'Set-Cookie' in head:
            oParser = cParser()
            sPattern = '(?:^|,) *([^;,]+?)=([^;,\/]+?);'
            aResult = oParser.parse(str(head['Set-Cookie']), sPattern)
            # print(aResult)
            if (aResult[0] == True):
                for cook in aResult[1]:
                    if 'deleted' in cook[1]:
                        continue
                    cookies = cookies + cook[0] + '=' + cook[1] + ';'

        # save cookie
        GestionCookie().SaveCookie(self.__sHosterIdentifier, cookies)

        self.DIALOG.VSinfo('Authentification reussie', self.__sDisplayName)
        VSlog('Auhentification reussie')

        return True

    def GetHtmlwithcookies(self, url, data, cookies):

        req = urllib2.Request(url, data, headers)
        if not (data == None):
            req.add_header('Referer', url)

        req.add_header('Cookie', cookies)

        try:
            response = urllib2.urlopen(req)
        except UrlError:
            return ''

        sHtmlContent = response.read()
        response.close()
        return sHtmlContent

    def GetHtml(self, url, data=None):
        cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)

        # aucun ne marche sans cookies
        if (cookies == '') and not self.__LoginTry and self.__Ispremium:
            self.Authentificate()
            if not self.isLogin:
                return ''
            cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)

        sHtmlContent = self.GetHtmlwithcookies(url, data, cookies)

        # Les cookies ne sont plus valables, mais on teste QUE si la personne n'a pas essaye de s'authentifier
        if not self.Checklogged(sHtmlContent) and not self.__LoginTry and self.__Ispremium:
            VSlog('Cookies non valables')
            self.Authentificate()
            if self.isLogin:
                cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
                sHtmlContent = self.GetHtmlwithcookies(url, data, cookies)
            else:
                return ''

        return sHtmlContent
