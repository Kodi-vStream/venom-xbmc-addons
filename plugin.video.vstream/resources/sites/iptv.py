# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser
from resources.sites.freebox import getHtml, showWeb, play__, decodeEmail
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'iptv'
SITE_NAME = 'Iptv'
SITE_DESC = 'Regarder la télévision'

URL_MAIN = 'https://www.extinf.com/'
FREE_M3U = URL_MAIN + 'home-passion-for-iptv-free-m3u-links-working-and-updated/'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', FREE_M3U)
    oGui.addDir(SITE_IDENTIFIER, 'showDailyList', 'Derniere liste', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showPays', 'Choix du pays', 'lang.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showPays():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    sHtmlContent = getHtml(sUrl)
    sPattern = '<li class="cat-item cat-item-.+?"><a href="([^"]+)"(?:>([^<]+)</a>|([^<]+)includes)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if str(aEntry[1]) != '':
                sTitle = aEntry[1]
            else:
                sTitle = aEntry[2].replace('"', '')
            sUrl2 = aEntry[0].replace(' title=', '')

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showDailyList', sTitle, 'tv.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showDailyList():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    sHtmlContent = getHtml(sUrl)
    sPattern = '<div class="news-thumb col-md-6">\s*<a href=([^"]+) title="([^"]+)".+?\s*<img src=.+?uploads/.+?/.+?/([^"]+)\..+?'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[1]
            sUrl2 = aEntry[0]
            if 'extinf' in sUrl:
                flag = aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            if str(flag) == 'm3u-playlist-720x405':
                oGui.addDir(SITE_IDENTIFIER, 'showDailyIptvList', sTitle, 'listes.png', oOutputParameterHandler)
            else:
                oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, 'tv.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            sNumPage = re.search('/page/([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showDailyList', 'Page ' + sNumPage, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a class="next page-numbers" href=([^>]+)>Next</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        return aResult[1][0]

    return False


def showDailyIptvList():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sHtmlContent = getHtml(sUrl)
    clearHtml = re.search('null>([\s*\S*]+)</pre>', sHtmlContent).group(1)
    line = re.compile('http(.+?)\n').findall(clearHtml)

    for sUrl2 in line:
        if '/cdn-cgi/l/email-protection' in str(sUrl2):
            sUrl2 = 'http' + decodeEmail(sUrl2).replace('<', '').replace('&amp;', '&')
        else:
            sUrl2 = 'http' + sUrl2.replace('&amp;', '&')

        sTitle = 'Lien: ' + sUrl2.replace('&amp;', '&')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

        oGui.addDir(SITE_IDENTIFIER, 'showWeb', sTitle, 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
