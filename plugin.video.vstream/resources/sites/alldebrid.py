# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Ovni-crea
import requests

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, addon

SITE_IDENTIFIER = 'alldebrid'
SITE_NAME = '[COLOR violet]Alldebrid[/COLOR]'
SITE_DESC = 'Débrideur de lien premium'

ITEM_PAR_PAGE = 20


def load():
    oGui = cGui()
    oAddon = addon()

    URL_HOST = oAddon.getSetting('urlmain_alldebrid')
    ALL_ALL = (URL_HOST + 'links/', 'showLiens')
    ALL_MAGNETS = (URL_HOST + 'magnets/', 'showMagnets')
    ALL_INFORMATION = ('https://alldebrid.fr', 'showInfo')

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ALL_ALL[0])
    oGui.addDir(SITE_IDENTIFIER, ALL_ALL[1], 'Liens', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ALL_MAGNETS[0])
    oGui.addDir(SITE_IDENTIFIER, ALL_MAGNETS[1], 'Magnets', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ALL_INFORMATION[0])
    oGui.addDir(SITE_IDENTIFIER, ALL_INFORMATION[1], 'Information sur les hébergeurs ', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLiens(sSearch=''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    numItem = oInputParameterHandler.getValue('numItem')
    numPage = oInputParameterHandler.getValue('numPage')
    if not numItem:
        numItem = 0
        numPage = 1
    numItem = int(numItem)
    numPage = int(numPage)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('</h1><hr><pre><a href="../">../</a>', '')
    sPattern = '<a href="(.+?)">([^<>]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        nbItem = 0
        index = 0
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:

            index += 1
            if index <= numItem:
                continue

            numItem += 1
            nbItem += 1
            progress_.VSupdate(progress_, ITEM_PAR_PAGE)
            if progress_.iscanceled():
                break

            sTitle = aEntry[1]
            sUrl2 = sUrl + aEntry[0]
            sThumb = ''
            sDesc = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            progress_.VSclose(progress_)

            if not sSearch:
                if nbItem % ITEM_PAR_PAGE == 0:  # cherche la page suivante
                    numPage += 1
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sUrl)
                    oOutputParameterHandler.addParameter('numItem', numItem)
                    oOutputParameterHandler.addParameter('numPage', numPage)
                    oGui.addNext(SITE_IDENTIFIER, 'showLiens', 'Page ' + str(numPage), oOutputParameterHandler)
                    break

        oGui.setEndOfDirectory()


def showMagnets(sSearch=''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    numItem = oInputParameterHandler.getValue('numItem')
    numPage = oInputParameterHandler.getValue('numPage')
    if not numItem:
        numItem = 0
        numPage = 1
    numItem = int(numItem)
    numPage = int(numPage)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('</h1><hr><pre><a href="../">../</a>', '')
    # Pattern servant à retrouver les éléments dans la page
    sPattern = '<a href="(.+?)">([^<]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        nbItem = 0
        index = 0

        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:

            index += 1
            if index <= numItem:
                continue

            numItem += 1
            nbItem += 1
            progress_.VSupdate(progress_, ITEM_PAR_PAGE)
            if progress_.iscanceled():
                break

            sTitle = aEntry[0]
            sUrl2 = sUrl + aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if not sSearch:
                if nbItem % ITEM_PAR_PAGE == 0:  # cherche la page suivante
                    numPage += 1
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sUrl)
                    oOutputParameterHandler.addParameter('numItem', numItem)
                    oOutputParameterHandler.addParameter('numPage', numPage)
                    oGui.addNext(SITE_IDENTIFIER, 'showLiens', 'Page ' + str(numPage), oOutputParameterHandler)
                    break

            if 'mp4' in sUrl2 or 'avi' in sUrl2 or 'mkv' in sUrl2:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showseriesHoster', sTitle, 'movies.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showseriesHoster(sSearch=''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    numItem = oInputParameterHandler.getValue('numItem')
    numPage = oInputParameterHandler.getValue('numPage')
    if not numItem:
        numItem = 0
        numPage = 1
    numItem = int(numItem)
    numPage = int(numPage)

    try:  # Dans le cas ou le mot mp4/avi/mkv n'est pas présent quand c'est un seul fichier
        s = requests.Session()
        resp = s.head(sUrl)
        result = resp.headers['location']
        sHosterUrl = result
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster is not False:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sMovieTitle)
            oGui.setEndOfDirectory()
    except:
        pass

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('</h1><hr><pre><a href="../">../</a>', '')

    sPattern = '<a href="(.+?)">([^<>]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        nbItem = 0
        index = 0
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:

            index += 1
            if index <= numItem:
                continue
            numItem += 1
            nbItem += 1

            progress_.VSupdate(progress_, ITEM_PAR_PAGE)
            if progress_.iscanceled():
                break

            sTitle = aEntry[1]
            sUrl2 = sUrl + aEntry[0]
            sThumb = ''
            sDesc = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

            if not sSearch:
                if nbItem % ITEM_PAR_PAGE == 0:  # cherche la page suivante
                    numPage += 1
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sUrl)
                    oOutputParameterHandler.addParameter('numItem', numItem)
                    oOutputParameterHandler.addParameter('numPage', numPage)
                    oGui.addNext(SITE_IDENTIFIER, 'showLiens', 'Page ' + str(numPage), oOutputParameterHandler)
                    break

            progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    sHosterUrl = sUrl
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster is not False:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sMovieTitle)

    oGui.setEndOfDirectory()


def showInfo():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<li class="([^"]+)">.+?<i alt=".+?" title="([^"]+)".+?</li>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sDisponible = aEntry[0].replace('downloaders_available', 'Disponible')\
                                   .replace('downloaders_unavailable', 'Non Disponible')
            sHebergeur = aEntry[1]

            sDisplayTitle = ('%s (%s)') % (sHebergeur, sDisponible)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)

            oGui.addText(SITE_IDENTIFIER, sDisplayTitle)

        progress_.VSclose(progress_)

        oGui.setEndOfDirectory()
