# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser
from resources.sites.freebox import getHtml, showWeb, play__
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'iptv_four_sat'
SITE_NAME = 'Iptv4Sat'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = 'https://www.iptv4sat.com/'
IPTV_WORLDWiDE = URL_MAIN + 'category/m3u-list-world-iptv/iptv-worldwide-m3u/'
SPORT_LISTE = URL_MAIN + 'category/m3u-list-world-iptv/free-iptv-sports/'
SMART_IPTV = URL_MAIN + 'category/m3u-list-world-iptv/smart-free-iptv/'

IPTV_AMERICAIN = URL_MAIN + 'category/m3u-list-world-iptv/america-m3u-iptv/'
IPTV_ARABE = URL_MAIN + 'category/m3u-list-world-iptv/free-iptv-arabic/'
IPTV_BELGE = URL_MAIN + 'category/european-iptv/belgique-iptv/'
IPTV_CANADA = URL_MAIN + 'category/m3u-list-world-iptv/canada-iptv-m3u/'
IPTV_FRENCH = URL_MAIN + 'category/european-iptv-iptv/france-m3u-iptv/'
IPTV_PAYSBAS = URL_MAIN + 'category/european-iptv/netherland-iptv/'
IPTV_POLOGNE = URL_MAIN + 'category/european-iptv/poland-iptv/'
IPTV_PORTUGAl = URL_MAIN + 'category/european-iptv/portugal-iptv-m3u/'
IPTV_ROUMANIE = URL_MAIN + 'category/european-iptv/iptv-romania/'
IPTV_TURC = URL_MAIN + 'category/european-iptv/m3u-turkey-iptv/'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Dernière liste', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', IPTV_WORLDWiDE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Dernière liste mondial', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_LISTE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste Sport', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SMART_IPTV)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Smart Iptv', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'listePerContry', 'Liste par Pays', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def listePerContry():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_AMERICAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Américaine', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', IPTV_ARABE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Arabe', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', IPTV_BELGE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Belgique', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', IPTV_CANADA)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Canada', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', IPTV_FRENCH)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines France', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', IPTV_PAYSBAS)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Pays-bas', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', IPTV_POLOGNE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Pologne', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', IPTV_PORTUGAl)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Portugal', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', IPTV_ROUMANIE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Roumanie', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', IPTV_TURC)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Turc', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showDailyList():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    sHtmlContent = getHtml(sUrl)
    sPattern = '<div class="td-module-thumb"><a href="([^"]+)" rel="bookmark".+?title="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showAllPlaylist', sTitle, 'listes.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            sNumPage = re.search('/page/([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showDailyList', 'Page ' + sNumPage, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = ' class="last".+?href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showAllPlaylist():  # On recupere les differentes playlist si il y en a
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    sHtmlContent = getHtml(sUrl)

    url = re.search('<a href="([^"]+)".+class="da-download-link da-download-attachment', sHtmlContent).group(1)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', url)

    oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()
