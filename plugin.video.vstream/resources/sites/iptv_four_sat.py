#-*- coding: utf-8 -*-
#vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.gui import cGui
# from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser

from resources.sites.freebox import getHtml, showWeb, play__
from resources.lib.comaddon import progress#, VSlog
import re

SITE_IDENTIFIER = 'iptv_four_sat'
SITE_NAME = 'Iptv4Sat'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = 'https://www.iptv4sat.com/'
IPTV_WOLRDWiDE = URL_MAIN + 'category/world/iptv-worldwide-m3u/'
SPORT_LISTE = URL_MAIN + 'category/world/free-iptv-sports/'
SMART_IPTV = URL_MAIN + 'category/world/smart-free-iptv/'

IPTV_AMERICAIN = URL_MAIN + 'category/world/america-m3u-iptv/'
IPTV_ARABE = URL_MAIN + 'category/world/free-iptv-arabic/'
IPTV_BELGE = URL_MAIN + 'category/european/belgique-iptv/'
IPTV_CANADA = URL_MAIN + 'category/world/canada-iptv-m3u/'
IPTV_FRENCH = URL_MAIN + 'category/european/france-m3u-iptv/'
IPTV_PAYSBAS = URL_MAIN + 'category/european/netherland-iptv/'
IPTV_POLOGNE = URL_MAIN + 'category/european/poland-iptv/'
IPTV_PORTUGAl = URL_MAIN + 'category/european/portugal-iptv-m3u/'
IPTV_ROUMANIE = URL_MAIN + 'category/european/iptv-romania/'
IPTV_TURC = URL_MAIN + 'category/european/m3u-turkey-iptv/'
# IPTV_AUTRE = URL_MAIN + 'category/other-list/'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Derniere liste', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_WOLRDWiDE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Derniere liste mondial', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LISTE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste Sport', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SMART_IPTV)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Smart Iptv', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'listePerContry', 'Liste par Pays', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def listePerContry():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_AMERICAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Amerique', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_ARABE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Arabe', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_BELGE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Belgique', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_CANADA)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Canada', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_FRENCH)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines France', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_PAYSBAS)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Pays-bas', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_POLOGNE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Pologne', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_PORTUGAl)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Portugal', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_ROUMANIE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Roumanie', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_TURC)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines Turc', 'tv.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', IPTV_AUTRE)
    # oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Liste chaines des autres pays', 'tv.png', oOutputParameterHandler)

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

            sUrl2 = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showAllPlaylist', sTitle, 'listes.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showDailyList', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = ' class="last".+?href="([^"]+)"'
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

    url = re.search('<a href="([^"]+)".+class="da-download-link da-download-attachment', sHtmlContent).group(1)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', url)

    oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()
