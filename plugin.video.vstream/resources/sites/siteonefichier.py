# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import xbmc
import xbmcgui

from resources.lib.comaddon import progress, addon
from resources.lib.config import GestionCookie
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'siteonefichier'
SITE_NAME = '[COLOR %s]%s[/COLOR]' % ('dodgerblue', 'Compte1fichier')

SITE_DESC = 'Fichiers sur compte 1Fichier'
URL_MAIN = 'https://1fichier.com/'
URL_FILE = URL_MAIN + 'console/files.pl'
URL_REMOTE = URL_MAIN + 'console/remote.pl'
URL_VERIF = URL_MAIN + 'check_links.pl?links[]='


def load():
    addons = addon()

    if (addons.getSetting('hoster_onefichier_username') == '') and (addons.getSetting('hoster_onefichier_password') == ''):
        oGui = cGui()
        oGui.addText(SITE_IDENTIFIER, '[COLOR %s]%s[/COLOR]' % ('red', 'Nécessite un Compte 1Fichier Premium ou Gratuit'))

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
        oGui.addDir(SITE_IDENTIFIER, 'opensetting', addons.VSlang(30023), 'none.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()
    else:
        if (GestionCookie().Readcookie('onefichier') != ''):
            showFile(URL_FILE)

        else:
            oPremiumHandler = cPremiumHandler('onefichier')
            Connection = oPremiumHandler.Authentificate()
            if (Connection == False):
                oGui = cGui()
                oGui.addText(SITE_IDENTIFIER, '[COLOR %s]%s[/COLOR]' % ('red', 'Connexion refusée'))
                oGui.setEndOfDirectory()

            else:
                showFile(URL_FILE)


def opensetting():
    addon().openSettings()


def showFile(sFileTree=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    # sUrl = oInputParameterHandler.getValue('siteUrl')
    if (oInputParameterHandler.exist('siteUrl')):
        sUrl = oInputParameterHandler.getValue('siteUrl')

    if sFileTree:
        sUrl = sFileTree

    oPremiumHandler = cPremiumHandler('onefichier')

    sHtmlContent = oPremiumHandler.GetHtml(sUrl)

    oParser = cParser()
    sPattern = '((?:|directory")) *rel="([^"]+)"><div class="dF"><a href="#" onclick="return false">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                oOutputParameterHandler.addParameter('siteUrl', '%s%s%s%s' % (URL_FILE, '?dir_id=', aEntry[1], '&oby=0&search='))
                oOutputParameterHandler.addParameter('sCode', '')
                oOutputParameterHandler.addParameter('sTitle', aEntry[2])
                oGui.addDir(SITE_IDENTIFIER, 'showFile', aEntry[2], 'genres.png', oOutputParameterHandler)

            else:
                oOutputParameterHandler.addParameter('siteUrl', '%s%s' % (URL_MAIN, 'console/link.pl'))
                oOutputParameterHandler.addParameter('sCode', aEntry[1])
                oOutputParameterHandler.addParameter('sTitle', aEntry[2])
                oGui.addDir(SITE_IDENTIFIER, 'showHosters', aEntry[2], 'genres.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sCode = oInputParameterHandler.getValue('sCode')

    oPremiumHandler = cPremiumHandler('onefichier')
    sHtmlContent = oPremiumHandler.GetHtml(sUrl, 'selected%5B%5D=' + sCode)

    sPattern = '<a href="([^"]+)">(.+?)</a></td>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHosterUrl = aResult[1][0][0]
        sTitle = aResult[1][0][1]

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sTitle)
            oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()


def UptomyAccount():
    oInputParameterHandler = cInputParameterHandler()
    sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')

    oPremiumHandler = cPremiumHandler('onefichier')
    # verif du lien
    sHtmlContent = oPremiumHandler.GetHtml('%s' % (URL_VERIF + sMediaUrl))
    if (sHtmlContent):
        sCheck = sHtmlContent.find('NOT FOUND')
        if sCheck != -1:
            # penible ce dialog auth
            xbmc.executebuiltin('Dialog.Close(all,true)')
            xbmcgui.Dialog().notification('Info upload', 'Fichier introuvable', xbmcgui.NOTIFICATION_INFO, 2000, False)

        else:
            # si liens ok >> requete
            sHtmlContent = oPremiumHandler.GetHtml(URL_REMOTE, '%s%s%s' % ('links=', sMediaUrl, '&did=0'))
            if (sHtmlContent):
                sCheck = sHtmlContent.find('1 liens')
                if sCheck != -1:
                    # penible ce dialog auth
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmcgui.Dialog().notification('Info upload', 'Ajouter à votre compte', xbmcgui.NOTIFICATION_INFO, 2000, False)
