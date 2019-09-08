#-*- coding: utf-8 -*-
#vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser

from resources.sites.freebox import getHtml, showWeb, play__
from resources.lib.comaddon import progress, VSlog

import re

SITE_IDENTIFIER = 'iptv_four_sat'
SITE_NAME = 'Iptv4Sat'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = 'https://www.iptv4sat.com/'
IPTV_WOLRDWiDE = URL_MAIN + 'category/worldwide-iptv/'
LISTE_GRATUIT = URL_MAIN + 'category/free-list/'
SPORT_LISTE = URL_MAIN + 'category/free-list/sports-m3u/'
IPTV_ARABE = URL_MAIN + 'category/free-list/iptv-arabic/'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Derniere liste', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_WOLRDWiDE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Derniere liste mondial', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', LISTE_GRATUIT)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste Gratuite', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LISTE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste Sport', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_ARABE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste Chaine Arabe', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showDailyList():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    sHtmlContent = getHtml(sUrl)
    sPattern = '<div class="td-module-thumb"><a href="([^"]+)" rel="bookmark".+?title="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[1]
            sUrl2 = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showAllPlaylist', sTitle, 'listes.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showDailyList', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    # oInputParameterHandler = cInputParameterHandler()
    # sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    sPattern = ' class="last" title=".+?">.+?</a><a href="([^"]+)"><i class="td-icon-menu-right"></i>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return  aResult[1][0]

    return False

def showAllPlaylist():#On recupere les differentes playlist si il y en a
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    sHtmlContent = getHtml(sUrl)

    sUrl2 = getDownloadLink(sHtmlContent)

    for url in sUrl2:

        if 'dl' in url:
            VSlog('Redirect')
            url = getRealLink(url)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', url)

        oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def getRealLink(sUrl):
    sHtmlContent = getHtml(sUrl)
    return re.search('<a href="([^"]+)" class="attachment-link"', sHtmlContent).group(1)

def getDownloadLink(sHtmlContent):
    sUrl2 = []
    urlDirect = re.search('<a href=".+?download(.+?)"', sHtmlContent)
    if urlDirect:
        urlDirect = URL_MAIN + 'download' + urlDirect.group(1)
        sUrl2.append(urlDirect)

    urlRedirect = re.search('<a href=".+?dl([^"]+)"', sHtmlContent)
    if urlRedirect:
        urlRedirect = URL_MAIN + 'dl' + urlRedirect.group(1)
        sUrl2.append(urlRedirect)
    return sUrl2
