#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.lib.parser import cParser
from resources.lib.config import GestionCookie

import urllib2,urllib
import xbmc
import xbmcaddon
import re,os

UA = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
headers = { 'User-Agent' : UA }

class cPremiumHandler:

    def __init__(self, sHosterIdentifier):
        self.__sHosterIdentifier = sHosterIdentifier.lower()
        self.__sDisplayName = 'Premium mode'
        self.isLogin = False
        self.__LoginTry = False
        self.__ssl = False
        
        self.__Ispremium = False
        bIsPremium = cConfig().getSetting('hoster_' + str(self.__sHosterIdentifier) + '_premium')        
        if (bIsPremium == 'true'):
            cConfig().log("Utilise compte premium pour hoster " +  str(self.__sHosterIdentifier))
            self.__Ispremium = True
        else:
            cConfig().log("Utilise compte gratuit pour hoster: " + str(self.__sHosterIdentifier))

    def isPremiumModeAvailable(self):
        return self.__Ispremium

    def getUsername(self):
        sUsername = cConfig().getSetting('hoster_' + str(self.__sHosterIdentifier) + '_username')
        return sUsername

    def getPassword(self):
        sPassword = cConfig().getSetting('hoster_' + str(self.__sHosterIdentifier) + '_password')
        return sPassword
        
    def AddCookies(self):
        cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
        return 'Cookie=' + cookies
        
    def Checklogged(self,code):
        if 'uptobox' in self.__sHosterIdentifier:
            if '//uptobox.com/?op=logout">Logout</a>' in code:
                return True
        return False
        
    def CheckCookie(self):
        cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
        if cookies != '':
            return True
        return False

    def Authentificate(self):

        #un seul essais par session, pas besoin de bombarder le serveur
        if self.__LoginTry:
            return False
        self.__LoginTry = True
        
        if not self.__Ispremium:
            return False
        
        post_data = {}
        
        if 'uptobox' in self.__sHosterIdentifier:
            url = 'https://login.uptobox.com/logarithme'
            post_data['op'] = 'login'
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
            
        #si aucun de trouve on retourne
        else:
            return False
        
        #print url
        #print post_data
        if (self.__ssl):
            try:
                import ssl
                context = ssl._create_unverified_context()
            except:
                self.__ssl = False
        
        req = urllib2.Request(url, urllib.urlencode(post_data), headers)
        
        try:
            if (self.__ssl):
                response = urllib2.urlopen(req,context=context)
            else:
                response = urllib2.urlopen(req)       
        except urllib2.URLError, e:
            if getattr(e, "code", None) == 403:
                #login denied
                cGui().showInfo(self.__sDisplayName, 'Authentification rate' , 5)
            elif getattr(e, "code", None) == 502:
                #login denied
                cGui().showInfo(self.__sDisplayName, 'Authentification rate' , 5)
            elif getattr(e, "code", None) == 234:
                #login denied
                cGui().showInfo(self.__sDisplayName, 'Authentification rate' , 5)
            else:
                cConfig().log("debug" + str(getattr(e, "code", None)))
                cConfig().log("debug" + str(getattr(e, "reason", None)))

            self.isLogin = False
            return False
        
        sHtmlContent = response.read()
        head = response.headers
        response.close()
        
        #print head
        
        #fh = open('c:\\prem.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        if 'uptobox' in self.__sHosterIdentifier:
            if 'OK' in sHtmlContent:
                self.isLogin = True
            else:
                cGui().showInfo(self.__sDisplayName, 'Authentification rate' , 5)
                return False
        elif 'onefichier' in self.__sHosterIdentifier:
            if 'You are logged in. This page will redirect you.' in sHtmlContent:
                self.isLogin = True
            else:
                cGui().showInfo(self.__sDisplayName, 'Authentification rate' , 5)
                return False
        elif 'uploaded' in self.__sHosterIdentifier:
            if sHtmlContent == '':
                self.isLogin = True
            else:
                cGui().showInfo(self.__sDisplayName, 'Authentification rate' , 5)
                return False     
        else:
            return False
        
        #get cookie
        cookies = ''
        if 'Set-Cookie' in head:
            oParser = cParser()
            sPattern = '(?:^|,) *([^;,]+?)=([^;,\/]+?);'
            aResult = oParser.parse(str(head['Set-Cookie']), sPattern)
            #print aResult
            if (aResult[0] == True):
                for cook in aResult[1]:
                    cookies = cookies + cook[0] + '=' + cook[1]+ ';'

        #save cookie
        GestionCookie().SaveCookie(self.__sHosterIdentifier,cookies)
        
        cGui().showInfo(self.__sDisplayName, 'Authentification reussie' , 5)
        cConfig().log( 'Auhentification reussie' )
        
        return True
        
    def GetHtmlwithcookies(self,url,data,cookies):
        
        req = urllib2.Request(url, data, headers)
        
        if not (data == None):
            req.add_header('Referer', url)
        
        req.add_header('Cookie', cookies)

        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            xbmc.log( str(e.code))
            xbmc.log( e.reason )
            return ''
        
        sHtmlContent = response.read()
        response.close()
        return sHtmlContent
        
    def GetHtml(self,url,data = None):
        cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
        
        #aucun ne marche sans cookies
        if (cookies== '') and not (self.__LoginTry) and self.__Ispremium:
            self.Authentificate()
            if not (self.isLogin):
                return ''
            cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)          
        
        sHtmlContent = self.GetHtmlwithcookies(url,data,cookies)
        
        #fh = open('c:\\premium.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        #Les cookies ne sont plus valables, mais on teste QUE si la personne n'a pas essaye de s'authentifier
        if not(self.Checklogged(sHtmlContent)) and not self.__LoginTry and self.__Ispremium :
            cConfig().log('Cookies non valables')
            self.Authentificate()
            if (self.isLogin):
                cookies = GestionCookie().Readcookie(self.__sHosterIdentifier)
                sHtmlContent = self.GetHtmlwithcookies(url,data,cookies)
            else:
                return ''
        
        return sHtmlContent
