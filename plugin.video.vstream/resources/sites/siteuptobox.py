#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser

from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import MPencode
from resources.lib.config import GestionCookie

from resources.lib.comaddon import progress, dialog, addon, xbmc, xbmcgui,VSlog

import urllib2, re
import json

SITE_IDENTIFIER = 'siteuptobox'
SITE_NAME = '[COLOR dodgerblue]' + 'CompteUptobox' + '[/COLOR]'
SITE_DESC = 'Fichiers sur compte Uptobox'
URL_MAIN = 'https://uptobox.com/'
BURL = URL_MAIN + '?op=my_files'

API_URL = 'https://uptobox.com/api/user/files?token=none&orderBy=file_created&dir=desc&offset=0&limit=100&path=%2F%2F'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'
headers = { 'User-Agent' : UA }

def load():
    oGui = cGui()
    addons = addon()
    oPremiumHandler = cPremiumHandler('uptobox')

    if (addons.getSetting('hoster_uptobox_username') == '') and (addons.getSetting('hoster_uptobox_password') == ''):
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + 'Nécessite Un Compte Uptobox Premium ou Gratuit' + '[/COLOR]')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
        oGui.addDir(SITE_IDENTIFIER,'opensetting', addons.VSlang(30023), 'none.png', oOutputParameterHandler)
    else:
        if (GestionCookie().Readcookie('uptobox') != ''):

            # oOutputParameterHandler = cOutputParameterHandler()
            # oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
            # oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
            oOutputParameterHandler.addParameter('file', 'fileonly')
            oGui.addDir(SITE_IDENTIFIER, 'showFile', 'Mes Fichiers', 'genres.png', oOutputParameterHandler)

            # oOutputParameterHandler = cOutputParameterHandler()
            # oOutputParameterHandler.addParameter('siteUrl', 'http://Dossier/')
            # oGui.addDir(SITE_IDENTIFIER, 'showFolder', 'Mes Dossiers', 'genres.png', oOutputParameterHandler)
        else:
            Connection = oPremiumHandler.Authentificate()
            if (Connection == False):
                dialog().VSinfo('Connexion refusée')
                return

            # oOutputParameterHandler = cOutputParameterHandler()
            # oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
            # oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
            oOutputParameterHandler.addParameter('file', 'fileonly')
            oGui.addDir(SITE_IDENTIFIER, 'showFile', 'Mes Fichiers', 'genres.png', oOutputParameterHandler)

            # oOutputParameterHandler = cOutputParameterHandler()
            # oOutputParameterHandler.addParameter('siteUrl', 'http://Dossier/')
            # oGui.addDir(SITE_IDENTIFIER, 'showFolder', 'Mes Dossiers', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def opensetting():
    addon().openSettings()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_UPTOBOX_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showFile():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oParser = cParser()
    
    sFileonly = ''
    if (oInputParameterHandler.exist('file')):
        sFileonly = oInputParameterHandler.getValue('file')
        
    sToken = ''
    if (oInputParameterHandler.exist('sToken')):
        sToken = oInputParameterHandler.getValue('sToken') 

        
    oPremiumHandler = cPremiumHandler('uptobox')

    if 'uptobox.com' in sUrl:
        sHtmlContent = oPremiumHandler.GetHtml(sUrl)
    else:
        if sToken == '':
           sHtmlContent = oPremiumHandler.GetHtml(BURL)
           sPattern = 'token":"(.+?)",'
           aResult = oParser.parse(sHtmlContent, sPattern)
           if (aResult[0] == True):
                sToken = aResult[1][0]
            
    sHtmlContent = oPremiumHandler.GetHtml(API_URL.replace('none',sToken))
    content = json.loads(sHtmlContent)
    content = content["data"]["files"]
    if content:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for x in content:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
  
            sTitle = x["file_name"]
            sHosterUrl = URL_MAIN + x["file_code"]
 
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory(
