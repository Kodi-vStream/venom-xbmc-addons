# -*- coding: utf-8 -*-
# vStream source pour Xalaflix

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog

SITE_IDENTIFIER = 'xalaflix'
SITE_NAME = 'Xalaflix'
SITE_DESC = 'Films et Séries en streaming HD'

URL_MAIN = 'https://xalaflix.io/'

URL_SEARCH = (URL_MAIN + 'search/?s=', 'showMovies')
URL_SEARCH_MOVIES = URL_SEARCH
MY_SEARCH_MOVIES = URL_SEARCH
URL_SEARCH_SERIES = URL_SEARCH
MY_SEARCH_SERIES = URL_SEARCH
URL_SEARCH_ANIMS = URL_SEARCH
MY_SEARCH_ANIMS = URL_SEARCH
URL_SEARCH_DRAMAS = URL_SEARCH
MY_SEARCH_DRAMAS = URL_SEARCH
URL_SEARCH_MISC = URL_SEARCH
FUNCTION_SEARCH = 'showMovies'

MOVIE_MOVIE = (URL_MAIN + 'films/', 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_HD = (URL_MAIN + 'films/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
MOVIE_VF = (URL_MAIN + 'films/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'films/', 'showMovies')

SERIE_SERIES = (URL_MAIN + 'series/', 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_VIEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_HD = (URL_MAIN + 'series/', 'showMovies')
SERIE_GENRES = (True, 'showGenres')
SERIE_ANNEES = (True, 'showSerieYears')
SERIE_VFS = (URL_MAIN + 'series/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'series/', 'showMovies')

ANIM_ANIMS = (URL_MAIN + 'animes/', 'showMenuAnims')
ANIM_NEWS = (URL_MAIN + 'animes/', 'showMovies')
ANIM_VIEWS = (URL_MAIN + 'animes/', 'showMovies')
ANIM_GENRES = (True, 'showGenres')
ANIM_ANNEES = (True, 'showAnimesYears')
ANIM_VFS = (URL_MAIN + 'animes/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'animes/', 'showMovies')
ANIM_ENFANTS = (URL_MAIN + 'animes/', 'showMovies')

DOC_NEWS = (URL_MAIN + 'documentaires/', 'showMovies')
DOC_DOCS = (URL_MAIN + 'documentaires/', 'showMovies')
DOC_GENRES = (True, 'showGenres')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF[1], 'Films (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()

    genres_list = [
        ['Action', URL_MAIN + 'genre/action/'],
        ['Animation', URL_MAIN + 'genre/animation/'],
        ['Aventure', URL_MAIN + 'genre/aventure/'],
        ['Biopic', URL_MAIN + 'genre/biopic/'],
        ['Comédie', URL_MAIN + 'genre/comedie/'],
        ['Documentaire', URL_MAIN + 'genre/documentaire/'],
        ['Drame', URL_MAIN + 'genre/drame/'],
        ['Epouvante-Horreur', URL_MAIN + 'genre/epouvante-horreur/'],
        ['Erotique', URL_MAIN + 'genre/erotique/'],
        ['Espionnage', URL_MAIN + 'genre/espionnage/'],
        ['Famille', URL_MAIN + 'genre/famille/'],
        ['Fantastique', URL_MAIN + 'genre/fantastique/'],
        ['Guerre', URL_MAIN + 'genre/guerre/'],
        ['Historique', URL_MAIN + 'genre/historique/'],
        ['Musical', URL_MAIN + 'genre/musical/'],
        ['Policier', URL_MAIN + 'genre/policier/'],
        ['Péplum', URL_MAIN + 'genre/peplum/'],
        ['Romance', URL_MAIN + 'genre/romance/'],
        ['Science-Fiction', URL_MAIN + 'genre/science-fiction/'],
        ['Thriller', URL_MAIN + 'genre/thriller/'],
        ['Western', URL_MAIN + 'genre/western/']
    ]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in genres_list:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sSearch:
        sUrl = sSearch

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="movie movie-block"><img src="([^"]+)".+?title="([^"]+)".+?onclick="window.location.href=\'([^\']+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        progress_ = progress().VScreate(SITE_NAME)
        total = len(aResult[1])
        oOutputParameterHandler = cOutputParameterHandler()

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            sTitle = aEntry[1].replace('En streaming', '').strip()
            sUrl2 = aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/series/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
            elif '/animes/' in sUrl2:
                oGui.addAnime(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
