from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.lib.parser import cParser

import urllib2,urllib
import xbmc
import xbmcaddon
import re,os

PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile"))
UA = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
headers = { 'User-Agent' : UA }

class cPremiumHandler:

    def __init__(self, sHosterIdentifier):
        self.__sHosterIdentifier = sHosterIdentifier.lower()
        self.__sDisplayName = 'Premium mode'
        self.isLogin = False

    def isPremiumModeAvailable(self):
        bIsPremium = cConfig().getSetting('hoster_' + str(self.__sHosterIdentifier) + '_premium')        
        if (bIsPremium == 'true'):
            cConfig().log("Utilise compte premium pour hoster " +  str(self.__sHosterIdentifier))
            return True

        cConfig().log("Utilise compte gratuit pour hoster: " + str(self.__sHosterIdentifier))
        return False

    def getUsername(self):
        sUsername = cConfig().getSetting('hoster_' + str(self.__sHosterIdentifier) + '_username')
        return sUsername

    def getPassword(self):
        sPassword = cConfig().getSetting('hoster_' + str(self.__sHosterIdentifier) + '_password')
        return sPassword

    #-----------------------
    #     Cookies gestion
    #------------------------
    
    def DeleteCookie(self,Domain):
        print 'Effacement cookies'
        file = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')
        os.remove(os.path.join(PathCache,file))
    
    def SaveCookie(self,Domain,data):
        Name = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')

        #save it
        file = open(Name,'w')
        file.write(data)

        file.close()
        
    def Readcookie(self,Domain):
        Name = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')
        
        try:
            file = open(Name,'r')
            data = file.read()
            file.close()
        except:
            return ''
        
        return data
        
    def AddCookies(self):
        cookies = self.Readcookie(self.__sHosterIdentifier)
        return 'Cookie=' + cookies

    def Authentificate(self):

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
            
        #si aucun de trouve on retourne
        else:
            return False
        
        #print url
        #print post_data
        
        req = urllib2.Request(url, urllib.urlencode(post_data), headers)
        
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            if e.code == 403:
                #login denied
                cGui().showInfo(self.__sDisplayName, 'Authentification rate' , 5)
            elif e.code == 502:
                #login denied
                cGui().showInfo(self.__sDisplayName, 'Authentification rate' , 5)
            elif e.code == 234:
                #login denied
                cGui().showInfo(self.__sDisplayName, 'Authentification rate' , 5)
            else:
                print e.code
                print e.reason

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
        self.SaveCookie(self.__sHosterIdentifier,cookies)
        
        cGui().showInfo(self.__sDisplayName, 'Authentification reussie' , 5)
        print 'Auhentification reussie'
        
        return True
        
    def GetHtml(self,url,data = None):
        cookies = self.Readcookie(self.__sHosterIdentifier)
        
        req = urllib2.Request(url, data, headers)
        
        if not (data == None):
            req.add_header('Referer', url)
        
        req.add_header('Cookie', cookies)

        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            print e.code
            print e.reason
            return ''

        
        sHtmlContent = response.read()
        response.close()
        
        return sHtmlContent

        
