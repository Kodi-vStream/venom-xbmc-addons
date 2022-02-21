# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Votre pseudo
from resources.lib.handler.requestHandler import cRequestHandler  # requete url
from resources.lib.parser import cParser  # recherche de code
from resources.hosters.hoster import iHoster
# from resources.lib.util import cUtil #Autres fonctions utiles
# et comaddon, exemple
# from resources.lib.comaddon import addon, dialog, VSlog, xbmcgui, xbmc

# AAdecoder
# from resources.lib.aadecode import AADecoder
# Cpaker decoder
# from resources.lib.packer import cPacker
# Jdecoder
# from resources.lib.jjdecode import JJDecoder
# Si premium
# from resources.lib.handler.premiumHandler import cPremiumHandler

# Ne garder que celles qui vous servent
import re
import urllib
import urllib2


class cHoster(iHoster):

    def __init__(self):
        # Permet de créé le hoster, vous devez passer les informations suivantes:
        # <nom fichier> = nom exact du fichier sans le .py
        # <nom affiché> = nom qui sera affiché à l'utilisateur (exemple: "Nouvel hebergeur")
        # [couleur] = argument facultatif (n'oubliez pas de supprimé la virgule avant 
        #             si vous ne mettez rien), il s'agit de la couleur avec laquelle
        #             le hoster sera affiché. Par défaut il s'agit du "skyblue"
        iHoster.__init__(self, '<nom fichier>', '<nom affiché>', '[couleur]')

    # Supprimer s'il est possible de télécharger avec ce host
    def isDownloadable(self):
        return False

    # facultatif mais a laisser pour compatibilitee
    def getPattern(self):
        return ''

    # Extraction du lien et decodage si besoin
    def __getMediaLinkForGuest(self):
        api_call = False

        oRequest = cRequestHandler(self._url)
        # oRequest.addHeaderEntry('Referer', 'http://www.google.fr/')  # Rajoute un header
        sHtmlContent = oRequest.request()

        oParser = cParser()
        sPattern =  'file: *"([^<>"]+?mp4)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0]):
            api_call = aResult[1][0]

        if (api_call):
            # Rajout d'un header ?
            # api_call = api_call + '|User-Agent=Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
            return True, api_call

        return False, False


# Attention : Pour fonctionner le nouvel hebergeur doit être rajouté dans le corps de vStream, fichier Hosters.py.
#----------------------------------------------------------------------------------------------------------------
#
# Code pour selection de plusieurs liens
#--------------------------------------
#
#            from resources.lib.comaddon import dialog
#
#            url = []
#            qua = []
#            api_call = False
#
#            for aEntry in aResult[1]:
#                url.append(aEntry[0])
#                qua.append(aEntry[1])
#
#            # Affichage du tableau
#            api_call = dialog().VSselectqual(qua, url)
#
#             if (api_call):
#                  return True, api_call

#             return False, False
