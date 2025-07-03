# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'cpasmieux'
SITE_NAME = 'Cpasmieux'
SITE_DESC = 'Films & Séries en streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = ('films/', 'showMenuMovies')
MOVIE_NEWS = ('films/', 'showMovies')
MOVIE_GENRES = (MOVIE_MOVIE[0] , 'showGenres')

SERIE_SERIES = ('series/', 'showMenuTvShows')
SERIE_NEWS = ('series/', 'showMovies')

ANIM_ANIMS = ('animes/', 'showMenuAnimes')
ANIM_NEWS = ('animes/', 'showMovies')

URL_SEARCH = (False, 'showMovies')
URL_SEARCH_MOVIES = ('?do=search&subaction=search&catlist[]=8&story=', 'showMovies')
URL_SEARCH_SERIES = ('?do=search&subaction=search&catlist[]=30&story=', 'showMovies')
URL_SEARCH_ANIMS = ('?do=search&subaction=search&catlist[]=41&story=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuAnimes', 'Animés', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search-films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search-series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuAnimes():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search-series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl += sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Action', 'action-1'], ['Animation', 'animation-1'], ['Aventure', 'aventure'], ['biopic', 'biopic'],
             ['Comédie', 'comedie-2'], ['crime', 'crime'], ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Familial', 'famille'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Histoire', 'historique'], ['Horreur', 'epouvante-horreur'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science-Fiction', 'science-fiction'],
             ['Thriller', 'thriller'], ['Western', 'western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0] + sUrl + '/')
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oUtil = cUtil()
    oParser = cParser()
    bMovie = bShow = isSerie = False
    if sSearch:
        sUrl = sSearch.replace(' ', '%20')
        if URL_SEARCH_MOVIES[0] in sSearch:
            bMovie = True
            sSearch = oUtil.CleanName(sSearch.replace(URL_SEARCH_MOVIES[0], ''))
        else:
            isSerie = bShow = True
            sSearch = oUtil.CleanName(sSearch.replace(URL_SEARCH_SERIES[0], ''))
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        bShow = isSerie = SERIE_SERIES[0] in sUrl or ANIM_ANIMS[0] in sUrl 
        bMovie = not bShow

    if not 'http' in sUrl:
        sUrl = URL_MAIN + sUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # url img title
    sPattern = 'th-item th-short">.+? href="([^"]+).+?data-src="([^"]+).+?alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    # en cas de recherche vide, deuxieme tentative avec le mot le plus long
    if sSearch and not aResult[0]:
        if ' ' in sSearch:
            termes = sSearch.split(' ')
            termes = sorted(termes, key=lambda terme: len(terme))[::-1]
            sUrl = URL_MAIN + URL_SEARCH[0] + termes[0]
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()
            aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        titles = set()
        total = len(aResult[1])
        oOutputParameterHandler = cOutputParameterHandler()
        
        results = aResult[1]
        if bShow:
            results = results[::-1] # trier les saisons
        
        
        for aEntry in results:
            sUrl = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]

            # tri des doublons
            cleanTitle = oUtil.CleanName(sTitle).replace(' ', '')
            if cleanTitle in titles:
                continue
            titles.add(cleanTitle)

            # non fonctionnel
            if 'F1 2024' in sTitle or 'F1 2025' in sTitle:
                continue

            # filtre search
            if bMovie:
                if '/series/' in sUrl or '/animes/' in sUrl:
                    continue
                if 'saison' in sTitle and 'episode' in sTitle:
                    continue
            
            if bShow and '/series/' not in sUrl and '/animes/' not in sUrl:
                continue
            if sSearch and total > 5:
                if not oUtil.CheckOccurence(sSearch, sTitle):
                    continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            if isSerie:
                sMovieTitle = re.sub('  S\d+', '', sTitle)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oGui.addMovie(SITE_IDENTIFIER, 'showMovieHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>(\d+)</a> *</span><span class="pnext"><a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sDesc = ''

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # url  /  thumb  /  title
    sPattern = 'th-item th-rel th-ses">.+?href="([^"]+)">.+?<img src="([^"]+)".+?th-title nowrap">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            sThumb = aEntry[1]
            sTitle = sMovieTitle + ' ' + aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        oGui.setEndOfDirectory()
    else:
        showMovieHosters()


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
    sHtmlContent = oParser.abParse(sHtmlContent, '<div class="season-main">', '</div></div>')

    # url numEp
    sPattern = 'href="([^"]+).+?span>(\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = sMovieTitle + " E%s" % aEntry[1]
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        oGui.setEndOfDirectory()
    else:
        showMovieHosters()


def showMovieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<li data-id="(\d+)" data-name="([^"]+)" data-hash="([^"]+)">'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sId = aEntry[0]
            sHoster = aEntry[1]
            sHash = aEntry[2]

            oHoster = 'episode' in sHoster or cHosterGui().checkHoster(sHoster)
            if oHoster:
                sUrl = '%sengine/ajax/controller.php?mod=xfield_ajax&id=%s&name=%s&hash=%s' % (URL_MAIN, sId, sHoster, sHash)
                sHoster = sHoster.replace('iframe_', '')
                if 'episode' in sHoster:
                    sDisplayTitle = '%s %s' % (sMovieTitle, sHoster.replace('-', ' '))
                    oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
                else:
                    sDisplayTitle = '%s (%s)' % (sMovieTitle, sHoster)
                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addLink(SITE_IDENTIFIER, 'showMovieLink', sDisplayTitle, sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(URL_MAIN + sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'li data-playerlink="([^"]+)'#.+?"serv">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for sHosterUrl in aResult[1]:
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()



def showMovieLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sUrl, params = sUrl.split('?')
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addParametersLine(params)
    sHosterUrl = oRequestHandler.request()

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster:
        if sHosterUrl.startswith('//'):
            sHosterUrl = 'https:' + sHosterUrl
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sPattern = 'data-playerlink="([^"]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for sHosterUrl in aResult[1]:
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'https:' + sHosterUrl

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()



