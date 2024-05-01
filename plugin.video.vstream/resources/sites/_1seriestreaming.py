# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager
from resources.lib.util import cUtil

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

SITE_IDENTIFIER = '_1seriestreaming'
SITE_NAME = '1 Serie Streaming'
SITE_DESC = 'Séries & Animés en Streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_SERIES = ('http://', 'load')
SERIE_NEWS = ('series/tendances-s/', 'showSeries')
SERIE_VIEWS = ('series/populaires-s/', 'showSeries')
SERIE_GENRES = (True, 'showGenres')
#SERIE_ANNEES = (True, 'showSerieYears')

URL_SEARCH = ('index.php?do=search&subaction=search&search_start=0&full_search=1&titleonly=3&sortby=date&catlist%5B%5D&story=', 'showSeries')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showSeries')
FUNCTION_SEARCH = 'showSeries'

ANIM_ANIMS = ('series/animation-s', 'showAnimes')
ANIM_NEWS = ('series/animation-s', 'showSeries')
URL_SEARCH_ANIMS = ('index.php?do=search&subaction=search&search_start=0&full_search=1&titleonly=3&sortby=date&catlist%5B%5D=12&story=', 'showSeries')

DRAMA_DRAMAS = (True, 'showDramas')
DRAMA_VIEWS = ('enstream/country/south-korea/', 'showSeries')
URL_SEARCH_DRAMAS = ('index.php?do=search&subaction=search&search_start=0&full_search=1&titleonly=3&sortby=date&catlist%5B%5D=3&story=', 'showSeries')




def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher (Séries)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher (Japanimes)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_DRAMAS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher (Dramas)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', '/series/series')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Nouveautés)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Populaires)', 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_VIEWS[1], 'Séries (Dramas)', 'dramas.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)


    # Non, les séries sont mélangées
    # oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAnimes():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearchAnim', 'Rechercher (Japanimes)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Japanimes (Nouveautés)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showDramas():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_DRAMAS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher (Dramas)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_VIEWS[1], 'Dramas (Nouveautés)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sUrl += sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return


def showSerieYears():
    # for i in itertools.chain(range(5, 7), [8, 9]): afficher dans l'ordre (pense bete ne pas effacer)
    oGui = cGui()
    from itertools import chain
    generator = chain([1955], range(1957, 2024))

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(list(generator)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'enstream/year/' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()

    liste = [
            ['Animation', 'animation-s'], ['Action & Adventure', 'action-adventure-s'],
            ['Comédie', 'comédie-s'], ['Documentaire', 'documentaire-s'],
            ['Drame', 'drame-s'], ['Enfants', 'kids-s'], ['Famille', 'familial-s'],
            ['Feuilleton', 'soap-s'], ['Guerre et Politique', 'war-politics-s'], 
            ['Historique', 'historique-s'], ['Horreur', 'horreur-s'],
            ['Musique', 'musique-s'], ['Mystère', 'mystère-s'], ['Policier', 'policier-s'],
            ['Romance', 'romance-s'], ['Science-Fiction', 'science-fiction-fantastique-s'], ['Thriller', 'thriller-s'],
            ['Talk-show', 'talk-s'], ['Télé-réalité', 'reality-s'], ['Western', 'western-s']]
    
    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', 'series/' + sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeries(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.split('=')[-1]
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'http' not in sUrl:
        sUrl = URL_MAIN + sUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'label-3">([^<]+).+?>(\d+)<.+?" href="([^"]+).+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            if 'no-poster.svg' in aEntry[2]:
                continue
            sTitle = aEntry[0]
            sYear = aEntry[1]
            sUrl2 = aEntry[2]
            if sUrl2.startswith('/'):
                sUrl2 = URL_MAIN[:-1] + sUrl2
            sThumb = re.sub('/w\d+/', '/w342/', aEntry[3])

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue    # Filtre de recherche

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, '', oOutputParameterHandler)

        if not sSearch:
            sNextPage, sPaging = __checkForNextPage(sHtmlContent)
            if sNextPage:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showSeries', 'Page ' + sPaging, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'div class="navigation".+?<\/span> <a href="([^"]+)">(\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = aResult[1][0][0]
        sNumberNext = aResult[1][0][1]
        sPaging = sNumberNext
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    sDesc = ''
    try:
        sPattern = 'h2><div class="head-desc body-2"><p>([^<]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    sPattern = '><a href="([^"]+)" title="[^"]+" class="season_link".+?season_name">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1][::-1]:

            sUrl = aEntry[0]
            sTitle = sMovieTitle + ' ' + aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '([^"]+)" title="([^"]+)" class="epsiode_link'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear')
    sDesc = oInputParameterHandler.getValue('sDesc')
    videoId = re.search('\/(\d+)', sUrl).group(1)
    referer = sUrl

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.request()
    cook = oRequestHandler.GetCookies()

    pdata = 'newsId=%s&action=showPlayers' % videoId
    sUrl = "https://app.1seriestreaming.io/engine/ajax/controller.php?mod=players&newsid=" + videoId

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('Referer', referer)
    oRequestHandler.addHeaderEntry('Cookie', cook)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addParametersLine(pdata)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = 'id="([^"]+)" *data-hash="([^"]+)".+?alt="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = '?action=player&url=' + aEntry[1]
            sHostName = aEntry[0]
            # sHost = re.sub('\..+', '', sHost).capitalize()
            hoster = cHosterGui().checkHoster(sHostName) 
            if not hoster:
                continue
            
            sHostName = hoster.getPluginIdentifier()

            sLang = aEntry[2].replace('default', '').upper()
            sTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHostName)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sHost', sHostName)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', sUrl)

    sHtmlContent = oRequest.request()
    sHosterUrl = oRequest.getRealUrl()

    oParser = cParser()
    sPattern = 'src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sHosterUrl = aResult[1][0]
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
