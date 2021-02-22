# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# return False
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'k_streaming'
SITE_NAME = 'K-Streaming'
SITE_DESC = 'Regarder Films et Séries en Streaming gratuit'

URL_MAIN = 'https://streaming-films.net/'

# definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle sera affichee.
# LA RECHERCHE GLOBAL N'UTILISE PAS showSearch MAIS DIRECTEMENT LA FONCTION INSCRITE DANS LA VARIABLE URL_SEARCH_*
FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
# recherche global films
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
# recherche global serie
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_MOVIE = ('http://', 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')
# MOVIE_ANNEES = (True, 'showYears')
# MOVIE_LIST = (URL_MAIN, 'showAlpha')

SERIE_SERIES = ('http://', 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'film/serie-gratuit-1/', 'showMovies')
# SERIE_GENRES = (SERIE_NEWS[0], 'showGenres')
# SERIE_ANNEES = (True, 'showSeriesYears')
# SERIE_LIST = (URL_MAIN + 'series', 'showAlpha')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Ordre alphabétique)', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Ordre alphabétique)', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '%20')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append(['Action', sUrl + 'film/action-complet/'])
    liste.append(['Animation', sUrl + 'film/animation-gratuit/'])
    liste.append(['Arts Martiaux', sUrl + 'arts-martiaux-streaming-vf/'])
    liste.append(['Aventure', sUrl + 'film/aventure-streaming-vf/'])
    liste.append(['Comédie', sUrl + 'film/films-comedie-streaming/'])
    liste.append(['Documentaire', sUrl + 'film/documentaire-streaming/'])
    # liste.append(['Biopic', sUrl + '/biopic_1'])
    liste.append(['Drame', sUrl + 'film/film-drame-streaming-vf/'])
    liste.append(['Epouvante Horreur', sUrl + 'film/horreur-streaming-film/'])
    # liste.append(['Erotique', sUrl + '/erotique_1'])
    liste.append(['Espionnage', sUrl + 'film/film-espionnage-streaming/'])
    liste.append(['Famille', sUrl + 'film/famille/'])
    liste.append(['Fantastique', sUrl + 'film/film-fantastique-streaming/'])
    liste.append(['Guerre', sUrl + 'film/film-guerre-streaming/'])
    liste.append(['Historique', sUrl + 'film/film-historique-streaming/'])
    liste.append(['Musical', sUrl + 'film/film-musical-streaming/'])
    liste.append(['Policier', sUrl + 'film/film-policier-streaming/'])
    liste.append(['Romance', sUrl + 'film/film-romance-streaming/'])
    liste.append(['Science Fiction', sUrl + 'film/film-science-fiction-streaming/'])
    liste.append(['Spectacle', sUrl + 'film/film-spectacles-streaming/'])
    liste.append(['Thriller', sUrl + 'film/film-thriller-streaming/'])
    # liste.append(['Comédie Dramatique', sUrl + '/comedie-dramatique_1'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAlpha():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    # on impose le /1 en bout d'url, pb de nextPage
    liste.append(['0', sUrl + '/alphabet/0/1'])
    liste.append(['1', sUrl + '/alphabet/1/1'])
    liste.append(['2', sUrl + '/alphabet/2/1'])
    liste.append(['3', sUrl + '/alphabet/3/1'])
    liste.append(['4', sUrl + '/alphabet/4/1'])
    liste.append(['5', sUrl + '/alphabet/5/1'])
    liste.append(['6', sUrl + '/alphabet/6/1'])
    liste.append(['7', sUrl + '/alphabet/7/1'])
    liste.append(['8', sUrl + '/alphabet/8/1'])
    liste.append(['9', sUrl + '/alphabet/9/1'])
    liste.append(['A', sUrl + '/alphabet/A/1'])
    liste.append(['B', sUrl + '/alphabet/B/1'])
    liste.append(['C', sUrl + '/alphabet/C/1'])
    liste.append(['D', sUrl + '/alphabet/D/1'])
    liste.append(['E', sUrl + '/alphabet/E/1'])
    liste.append(['F', sUrl + '/alphabet/F/1'])
    liste.append(['G', sUrl + '/alphabet/G/1'])
    liste.append(['H', sUrl + '/alphabet/H/1'])
    liste.append(['I', sUrl + '/alphabet/I/1'])
    liste.append(['J', sUrl + '/alphabet/J/1'])
    liste.append(['K', sUrl + '/alphabet/K/1'])
    liste.append(['L', sUrl + '/alphabet/L/1'])
    liste.append(['M', sUrl + '/alphabet/M/1'])
    liste.append(['N', sUrl + '/alphabet/N/1'])
    liste.append(['O', sUrl + '/alphabet/O/1'])
    liste.append(['P', sUrl + '/alphabet/P/1'])
    liste.append(['Q', sUrl + '/alphabet/Q/1'])
    liste.append(['R', sUrl + '/alphabet/R/1'])
    liste.append(['S', sUrl + '/alphabet/S/1'])
    liste.append(['T', sUrl + '/alphabet/T/1'])
    liste.append(['U', sUrl + '/alphabet/U/1'])
    liste.append(['V', sUrl + '/alphabet/V/1'])
    liste.append(['W', sUrl + '/alphabet/W/1'])
    liste.append(['X', sUrl + '/alphabet/X/1'])
    liste.append(['Y', sUrl + '/alphabet/Y/1'])
    liste.append(['Z', sUrl + '/alphabet/Z/1'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1918, 2022)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/films/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesYears():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1980, 2022)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/series/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sSearch:
        sUrl = sSearch.replace(' ', '%20')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # parfois pas d'image et la qualité est une option pour la recherche
    # sPattern = 'class="imagefilm">\s*<a href="([^"]+).+?src="([^"]*)" alt="([^"]+).+?(?:|<span class="([^"]+).+?)</div>'
    sPattern = 'moviefilm".+?href="([^"]+).+?src="([^"]+)" alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]

            sThumb = aEntry[1]

            sTitle = aEntry[2].replace('Streaming', '').replace('Sasion', 'Saison')
            sDisplayTitle = sTitle

            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '-saison-' in sUrl2 or '/series-' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

    if not sSearch:  # Le moteur de recherche du site est correct pour laisser le nextPage même en globalSearch
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    # &raquo; est réécris par vStream en >>
    sPattern = 'pages\'>.age.+?sur (\d+).+?current\'>.+?href="([^"]+)">>>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    # Uniquement saison a chaque fois
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    # récupération du Synopsis
    sDesc = ''
    try:
        sPattern = 'Synopsis</span>:([^<]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    sPattern = '<div class="unepetitesaisons">\s*<a href="([^"]+)" title="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            if sUrl.startswith('/'):
                sUrl = URL_MAIN + sUrl

            sTitle = aEntry[1]
            sTitle = re.sub('- Saison \d+', '', sTitle)  # double affichage de la saison

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    sDesc = ''
    try:
        sPattern = 'Synopsis</span>:([^<]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    # recuperation du premier épisode
    sPattern = 'current" aria-current="page"><span>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    ListeUrl = []
    if (aResult[0] == True):
        ListeUrl = [(sUrl, aResult[1][0])]

    # Recuperation des suivants
    sPattern = '<a href="([^<]+)" class="post-page-numbers"><span>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    ListeUrl = ListeUrl + aResult[1]

    if (aResult[0] == True):
        for aEntry in ListeUrl:

            sUrl = aEntry[0]
            sTitle = sMovieTitle.replace(' - Saison', ' Saison') + aEntry[1].replace('Part', 'Episode')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    # si un seul episode
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle + 'episode 1 ')
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addTV(SITE_IDENTIFIER, 'showHosters', sMovieTitle + ' episode 1 ', '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<iframe (SRC|src)="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[1]
            if '//www.facebook.com/' in sHosterUrl:
                continue

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
