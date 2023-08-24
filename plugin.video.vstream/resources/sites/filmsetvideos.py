# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'filmsetvideos'
SITE_NAME = 'FilmS et VideoS'
SITE_DESC = 'films et vidéos'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')

SERIE_NEWS = (URL_MAIN + 'tv/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_VF = (URL_MAIN + 'seriesenstreaming/series-vf/', 'showMovies')
SERIE_VOSTFR = (URL_MAIN + 'seriesenstreaming/series-vostfr/', 'showMovies')

URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'films/?filter=year&q=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'tv/?filter=year&q=', 'showMovies')

# Menu GLOBALE HOME
MOVIE_MOVIE = (True, 'showMenuMovies')
SERIE_SERIES = (True, 'showMenuTvShows')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Séries ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Série (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Séries ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Série (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showMovies(sUrl + sSearchText)
        oGui.setEndOfDirectory()
        return


def showMovieGenres():
    oGui = cGui()

    listeGenre = ['Action', 'Animation', 'Aventure', 'Comedie', 'Crime', 'Documentaire', 'Drame',
                  'Familial', 'Fantastique', 'Guerre', 'Histoire', 'Horreur', 'Musique', 'Mystere', 'Romance',
                  'Science-fiction', 'Telefilm', 'Thriller', 'Western']

    oOutputParameterHandler = cOutputParameterHandler()
    for genre in listeGenre:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/?filter=year&genre=' + genre)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', genre, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieGenres():
    oGui = cGui()

    listeGenre = [('Action et aventure', 'action&adventure'),
                  ('Animation', 'animation'),
                  ('Comédie', 'comedie'),
                  ('Crime', 'crime'),
                  ('Documentaire', 'documentaire'),
                  ('Drame', 'drame'),
                  ('Familial', 'familial'),
                  ('Kids', 'kids'),
                  ('Mystère', 'mystere'),
                  ('News', 'news'),
                  ('Science-fiction', 'science-fiction&Fantastique'),
                  ('Soap', 'soap'),
                  ('Talk', 'talk'),
                  ('Télé réalité', 'reality'),
                  ('Guerre & Politique', 'war&politics'),
                  ('Western', 'western')
                  ]

    oOutputParameterHandler = cOutputParameterHandler()
    for genre_title, genre_url in listeGenre:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'tv/genre/' + genre_url + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', genre_title, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    oUtil = cUtil()

    if sSearch:
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)

        sSearch = sSearch.replace(' ', '+').replace('%20', '+')
        sUrl = sSearch
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = 'fluid card"><a href="\/([^"]+).+?h4>([^<]+).+?(data-ids="([^\"]+)|).+?SYNOPSIS<br>([^<]*).+?src="/([^"]+)'

    series_noms = []

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[1].strip()
            sTitle = oUtil.unescape(sTitle)
            sDesc = aEntry[4]
            sThumb = URL_MAIN + aEntry[5]

            if '/tv' in sUrl:
                if sTitle in series_noms:  # une seule fois la série, filtrer les saisons
                    continue
                series_noms.append(sTitle)

            # Titre recherché
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            sDisplayTitle = sTitle
            sTmdbId = aEntry[3]

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)

            if '/tv' in sUrl:
                sUrl2 = URL_MAIN + 'tv/?filter=year&q=' + sTitle
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                sUrl2 = URL_MAIN + oUtil.unescape(aEntry[0].replace('and#', "&#"))
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oGui.addMovie(SITE_IDENTIFIER, 'showMovieLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    else:
        oGui.addText(SITE_IDENTIFIER)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()

    sPattern = 'pagination menu ">.+?<a class="icon item" href="[^\"]+">(\d+)<\/a><a class="icon item" href="\/(.+?)(\d+)"><i class="right chevron'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNumberNext = aResult[1][0][2]
        sNextPage = URL_MAIN + aResult[1][0][1] + sNumberNext
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sTmdbId = oInputParameterHandler.getValue('sTmdbId')
    if not sTmdbId:
        sTmdbId = ''

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'fluid card"><a href="\/([^"]+)".+?Saison : (\d+).+?(data-ids="([^\"]+)|<div type="Genre")'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in reversed(aResult[1]):

            sUrl2 = aEntry[0]
            if sTmdbId != aEntry[3]:  # filtre des saisons selon l'id de la série
                continue

            sSaison = aEntry[1]
            sTitle = ("%s Saison %s") % (sMovieTitle, sSaison)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sSaison', sSaison)

            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        oGui.addText(SITE_IDENTIFIER)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sSaison = oInputParameterHandler.getValue('sSaison')
    oRequestHandler = cRequestHandler(URL_MAIN + sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '"dropdown icon"><\/i> episode : (\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for sEpisode in aResult[1]:
            sTitle = sMovieTitle + ' Saison ' + sSaison + ' Episode' + sEpisode

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sEpisode', sEpisode)

            oGui.addEpisode(SITE_IDENTIFIER, 'showSerieLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        oGui.addText(SITE_IDENTIFIER)

    oGui.setEndOfDirectory()


def showSerieLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sEpisode = oInputParameterHandler.getValue('sEpisode')

    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN + sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'data-ids="(\d+)"><i class="icon play"><\/i>Voir l\'épisode en VF<\/div><\/div><div class="content"><div class="header">Site : ([^\.]+)[^<]+<br>Episode : %s<' % sEpisode
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = URL_MAIN + 'config/function.php?bandeS=' + aEntry[0]
            sHoster = aEntry[1].capitalize()

            oHoster = cHosterGui().checkHoster(sHoster)
            if not oHoster:
                continue

            sDisplayTitle = ('%s Episode %s [COLOR coral]%s[/COLOR]') % (sTitle, sEpisode, sHoster)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addLink(SITE_IDENTIFIER, 'showMovieHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieLinks():

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    hosters = []
    sPattern = 'data-ids="([^"]+)">.+?"header">Site : ([^\.]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = URL_MAIN + 'config/function.php?bandeF=' + aEntry[0]
            sHoster = aEntry[1].capitalize()

            if sHoster in hosters:
                continue  # un seul lien par hoster
            hosters.append(sHoster)

            oHoster = cHosterGui().checkHoster(sHoster)
            if not oHoster:
                continue

            sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sTitle, sHoster)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addLink(SITE_IDENTIFIER, 'showMovieHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    oParser = cParser()
    sPattern = 'iframe":"([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sHosterUrl = aResult[1][0]
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
