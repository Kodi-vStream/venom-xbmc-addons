# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
import re
import urllib3

from resources.hosters.hoster import iHoster
from resources.lib.comaddon import dialog, VSlog
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'


class cHoster(iHoster):
    def __init__(self):
        self.__sDisplayName = '1Fichier'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR violet]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return '1fichier'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def __getIdFromUrl(self, sUrl):
        # http://kzu0y3.1fichier.com/
        # https://1fichier.com/?s6gdceia9y
        sId = sUrl.replace('https://', '')
        sId = sId.replace('http://', '')
        sId = sId.replace('1fichier.com/?', '')
        sId = sId.replace('.1fichier.com', '')
        sId = sId.replace('/', '')

        return sId

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return

    def getMediaLink(self):
        self.oPremiumHandler = cPremiumHandler(self.getPluginIdentifier())
        print(self.oPremiumHandler.isPremiumModeAvailable())

        import sys
        if ('site=cDownload&function' not in sys.argv[2]) and not (self.oPremiumHandler.isPremiumModeAvailable()):
            oDialog = dialog().VSok("Pas de streaming sans premium.\nPour voir le film passer par l'option 'Télécharger et Lire' du menu contextuel.")
            return False, False

        if self.oPremiumHandler.isPremiumModeAvailable():
            return self.__getMediaLinkByPremiumUser()
        else:
            return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
        import random

        api_call = False
        url = 'https://1fichier.com/?' + self.__getIdFromUrl(self.__sUrl)

        adcode = random.uniform(000.000000000, 999.999999999)

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Host', url.split('/')[2])
        oRequestHandler.addHeaderEntry('Referer', url)
        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')

        oRequestHandler.addParameters('dl_no_ssl', 'on')
        oRequestHandler.addParameters('adz', adcode)
        sHtmlContent = oRequestHandler.request()

        # fh = open('c:\\test.txt', "w")
        # fh.write(sHtmlContent)
        # fh.close

        api_call = self.GetMedialinkDL(sHtmlContent)

        if api_call:
            if isPremium:
                api_call = api_call + '&' + self.oPremiumHandler.AddCookies()
            return True, api_call

        return False, False

    def GetMedialinkDL(self, sHtmlContent):

        oParser = cParser()
        api_call = False

        sPattern = 'Vous devez attendre encore [0-9]+ minutes'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            dialog().VSinfo('Erreur - Limitation %s' % aResult[1][0])
            return False

        sPattern = '<a href="([^<>"]+?)"  style="float:none;margin:auto;font-weight:bold;padding: 10px;margin: 10px;font-size:\+1\.6em;border:2px solid red" class="ok btn-general btn-orange">'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            # xbmc.sleep(1*1000)
            # VSlog(  aResult[1][0] )
            api_call = aResult[1][0] + '|User-Agent=' + UA  # + '&Referer=' + self.__sUrl
            return api_call

        return False

    def __getMediaLinkByPremiumUser(self):
        api_call = False

        if not self.oPremiumHandler.Authentificate():
            return False, False

        url = 'https://1fichier.com/?' + self.__getIdFromUrl(self.__sUrl)

        '''
        La partie ci-dessous permet d'utiliser l'option "Forcer l'affichage du menu pour les téléchargements" permettant
        notamment de choisir depuis l'interface web de télécharger ou d'ajouter un fichier.
        Pour cela, on va ajouter le paramètre e=1 (cf. https://1fichier.com/hlp.html#dev ) à la requête permettant
        d'obtenir le lien direct
        '''

        sHtmlContent = self.oPremiumHandler.GetHtml('%s' % url + '&e=1')
        if sHtmlContent:
            # L'option est désactivée : la réponse sera de type "text/plain; charset=utf-8", exemple :
            # https://serveur-2b.1fichier.com/lelienactif;Film.de.Jacquie.et.Michel.a.la.montagne.mkv;1234567890;0
            m = re.search('^(.*);.*;.*;.*$', sHtmlContent)
            if (m):
                url = m.group(1)
            # L'option est activée : pour récupérer le lien direct il faut POSTer le formulaire demandant le download
            else:
                cookie = self.oPremiumHandler.AddCookies().replace('Cookie=', '', 1)
                data = {
                    'submit': 'download'
                }
                # Seul le Cookie est nécessaire, néanmoins autant rendre les headers cohérents
                headers = {'User-Agent': UA,
                           'Host': '1fichier.com',
                           'Referer': url,
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                           'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
                           'Cookie': cookie,
                           'Content-Length': '15',
                           'Content-Type': 'application/x-www-form-urlencoded'
                           }
                try:
                    http = urllib3.PoolManager()
                    response = http.request(method='POST', url=url, fields=data, headers=headers)
                except urllib3.exceptions.HTTPError as e:
                    VSlog(e.read())
                    VSlog(e.reason)
                # Par défaut on suit la redirection (code: 302 + entête 'Location') dans la réponse
                # on peut ainsi récupérer le lien direct
                url = response.geturl()
                response.release_conn()
        else:
            return False, False

        # Mode = ''
        # Mode = {'dl_no_ssl': 'on' , 'dlinline': 'on'}
        # Mode = {'dl_no_ssl': 'on'}
        # postdata = urlEncode(Mode)

        # Pas de page html mais lien direct
        # sHtmlContent = self.oPremiumHandler.GetHtml(url, postdata)
        # fh = open('c:\\test.txt', "w")
        # fh.write(sHtmlContent)
        # fh.close()

        # mode inline
        # url = url + '&inline'

        api_call = url + '|' + self.oPremiumHandler.AddCookies()

        VSlog(api_call)

        if api_call:
            return True, api_call

        return False, False
