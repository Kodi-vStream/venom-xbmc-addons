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
from resources.lib.comaddon import addon

SITE_IDENTIFIER = 'alldebrid'
SITE_NAME = '[COLOR violet]Alldebrid[/COLOR]'
SITE_DESC = 'Débrideur de lien premium'

ITEM_PAR_PAGE = 25


def load():
    oGui = cGui()
    oAddon = addon()

    URL_MAIN = 'https://alldebrid.fr'
    URL_HOST = oAddon.getSetting('urlmain_alldebrid')
    ALL_ALL = (URL_HOST + 'links/', 'showLiens')
    ALL_MAGNETS = (URL_HOST + 'magnets/', 'showMagnetsVideos')
    ALL_HISTO = (URL_HOST + 'history/', 'showLiens')
    ALL_INFORMATION = (URL_MAIN, 'showInfo')

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ALL_ALL[0])
    oGui.addDir(SITE_IDENTIFIER, ALL_ALL[1], 'Liens', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ALL_MAGNETS[0])
    oGui.addDir(SITE_IDENTIFIER, ALL_MAGNETS[1], 'Magnets', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ALL_HISTO[0])
    oGui.addDir(SITE_IDENTIFIER, ALL_HISTO[1], 'Historique', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ALL_INFORMATION[0])
    oGui.addDir(SITE_IDENTIFIER, ALL_INFORMATION[1], 'Informations sur les hébergeurs ', 'host.png', oOutputParameterHandler)

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

    oHoster = cHosterGui()
    hosterLienDirect = oHoster.getHoster('lien_direct')
 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        nbItem = 0
        index = 0

        for aEntry in aResult[1]:
            index += 1
            if index <= numItem:
                continue

            numItem += 1
            nbItem += 1
            sTitle = aEntry[1]
            sUrl2 = sUrl + aEntry[0]
            
            hosterLienDirect.setDisplayName(sTitle)
            hosterLienDirect.setFileName(sTitle)
            oHoster.showHoster(oGui, hosterLienDirect, sUrl2, sTitle)
            
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



def showMagnetsVideos(sSearch=''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovie', 'Recherche (Films)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showSearchTV', 'Recherche (Séries)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showMagnetsMovie', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showMagnetsTV', 'Séries', 'series.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showMagnetsTV(sSearch=''):
    showMagnets(True, sSearch)
    
def showMagnetsMovie(sSearch=''):
    showMagnets(False, sSearch)


def showSearchMovie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showMagnetsMovie(sSearchText)
        oGui.setEndOfDirectory()
        return
    
def showSearchTV():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showMagnetsTV(sSearchText)
        oGui.setEndOfDirectory()
        return
    
def showMagnets(series, sSearch=''):
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
    sPattern = '<a href="(.+?)">([^<]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        nbItem = 0
        index = 0

        for aEntry in aResult[1]:

            index += 1
            if index <= numItem:
                continue

            numItem += 1
            nbItem += 1
            sTitle = aEntry[1]
            sUrl2 = sUrl + aEntry[0]

            if sSearch and sSearch.upper() not in sTitle.upper():
                continue    # Filtre de recherche

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
                    if series:
                        oGui.addNext(SITE_IDENTIFIER, 'showMagnetsTV', 'Page ' + str(numPage), oOutputParameterHandler)
                    else:
                        oGui.addNext(SITE_IDENTIFIER, 'showMagnetsMovie', 'Page ' + str(numPage), oOutputParameterHandler)
                    break

            isMovie = 'mp4' in sUrl2 or 'avi' in sUrl2 or 'mkv' in sUrl2
                
            if not series and isMovie:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumb, sDesc, oOutputParameterHandler)
            elif series and not isMovie:
                oGui.addTV(SITE_IDENTIFIER, 'showseriesHoster', sTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showseriesHoster(sSearch=''):
    oGui = cGui()
    oHosterGui = cHosterGui()

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
        oHoster = oHosterGui.checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sMovieTitle)
            oGui.setEndOfDirectory()
    except:
        pass

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('</h1><hr><pre><a href="../">../</a>', '')

    sPattern = '<a href="(.+?)">([^<>]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oHoster = oHosterGui.getHoster('lien_direct')
        for aEntry in aResult[1]:
            sHosterUrl = sUrl + aEntry[0]
            sTitle = aEntry[1]
            oHoster.setDisplayName(sTitle)
            oHoster.setFileName(sTitle)
            oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sTitle)

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

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        for aEntry in sorted(aResult[1], key=lambda host: host[1]):
            sDisponible = aEntry[0].replace('downloaders_available', '[COLOR green]Disponible[/COLOR]')\
                                   .replace('downloaders_unavailable', '[COLOR red]Non Disponible[/COLOR]')
            sHebergeur = aEntry[1]

            sDisplayTitle = ('%s - %s') % (sHebergeur, sDisponible)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)

            oGui.addText(SITE_IDENTIFIER, sDisplayTitle)

    oGui.setEndOfDirectory()
