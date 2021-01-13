# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
return False
import re

from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser
from resources.sites.freebox import getHtml, showWeb, play__
from resources.lib.comaddon import progress, VSlog

SITE_IDENTIFIER = 'iptv_gratuit'
SITE_NAME = 'IptvGratuit'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = 'https://iptvgratuit.com/'

IPTV_WORLD = URL_MAIN + 'iptv-world/'
IPTV_FRANCE = URL_MAIN + 'france/'
IPTV_AFRIQUE = URL_MAIN + 'iptv-afrique/'
IPTV_ALLEMAGNE = URL_MAIN + 'iptv-allemagne/'
IPTV_ANGLETERRE = URL_MAIN + 'iptv-uk/'
IPTV_ARABIC = URL_MAIN + 'iptv-arabic/'
# IPTV_AUTRICHE = URL_MAIN + 'iptv-autriche/'
IPTV_BELGIQUE = URL_MAIN + 'iptv-belgique/'
IPTV_BRESIL = URL_MAIN + 'iptv-bresil/'
IPTV_CANADA = URL_MAIN + 'iptv-canada/'
IPTV_CHINE = URL_MAIN + 'iptv-chine/'
IPTV_ESPAGNE = URL_MAIN + 'iptv-espagne/'
IPTV_HOLLANDE = URL_MAIN + 'iptv-hollande/'
IPTV_ITALIE = URL_MAIN + 'iptv-italie/'
IPTV_PORTUGAL = URL_MAIN + 'iptv-portugal/'
IPTV_SUISSE = URL_MAIN + 'iptv-suisse/'
IPTV_RUSSIE = URL_MAIN + 'iptv-russie/'
IPTV_TURK = URL_MAIN + 'iptv-turk/'
IPTV_USA = URL_MAIN + 'iptv-usa/'
IPTV_SPORT = URL_MAIN + 'iptv-sport/'
IPTV_VOD = URL_MAIN + 'iptv-vod/'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Dernieres listes', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_WORLD)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Dernieres listes mondial', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_FRANCE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes France', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_AFRIQUE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Afrique', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_ALLEMAGNE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Allemande', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_ANGLETERRE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Anglaise', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_ARABIC)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Arabe', 'tv.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', IPTV_AUTRICHE)
    # oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Autriche', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_BELGIQUE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Belgique', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_BRESIL)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Brésil', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_CANADA)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Canada', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_CHINE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Chine', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_ESPAGNE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Espagne', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_HOLLANDE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Hollande', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_ITALIE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Italie', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_PORTUGAL)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Portugal', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_SUISSE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Suisse', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_SUISSE)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Russie', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_TURK)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes Turque', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_USA)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes USA', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_SPORT)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes SPORT', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', IPTV_VOD)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'listes VOD', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showDailyList():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    sHtmlContent = getHtml(sUrl)
    sPattern = '<h2 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
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
            sNumPage = re.search('pages/([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showDailyList', 'Page ' + sNumPage, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'class="next page-numbers" href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        return aResult[1][0]

    return False


def showAllPlaylist():  # On recupere les differentes playlist si il y en a
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    oParser = cParser()
    sHtmlContent = getHtml(sUrl)
    sPattern = '<a class="more-link" title="(.+?)".+?href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        sTitleTest = ''
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[0]
            sUrl2 = aEntry[1]

            if (sTitle == sTitleTest):
                continue
            else:
                sTitleTest = sTitle

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showAllPlaylist2():  # On recupere les differentes playlist si il y en a
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    sHtmlContent = getHtml(sUrl)
    sUrl2 = getDownloadLink(sHtmlContent)

    for url in sUrl2:

        if 'download' in url:
            VSlog('Redirect')
            url = getRealLink(url)
            oGui.addText(SITE_IDENTIFIER, url)
        else:
            oGui.addText(SITE_IDENTIFIER, 'rien')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)

        oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()
