# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog

SITE_IDENTIFIER = 'tirexo'
SITE_NAME = 'Tirexo'
SITE_DESC = 'Films, Séries, Animés, Documentaires en streaming'

URL_MAIN = 'https://www.tirexo.zone/'

# Recherche globale
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
MY_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
MY_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')
MY_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

# Menus films
MOVIE_MOVIE = (URL_MAIN, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_VF = (URL_MAIN + 'films/vf/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'films/vostfr/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')

# Menus séries
SERIE_SERIES = (URL_MAIN, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_VFS = (URL_MAIN + 'series/vf/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'series/vostfr/', 'showMovies')
SERIE_GENRES = (True, 'showGenres')
SERIE_ANNEES = (True, 'showSerieYears')

# Menus animés
ANIM_ANIMS = (URL_MAIN, 'showMenuAnims')
ANIM_NEWS = (URL_MAIN + 'animes/', 'showMovies')
ANIM_VFS = (URL_MAIN + 'animes/vf/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'animes/vostfr/', 'showMovies')
ANIM_GENRES = (True, 'showGenres')

# Documentaires
DOC_NEWS = (URL_MAIN + 'documentaires/', 'showMovies')

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

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'docs.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + 'films/action/'])
    liste.append(['Animation', URL_MAIN + 'films/animation/'])
    liste.append(['Aventure', URL_MAIN + 'films/aventure/'])
    liste.append(['Biopic', URL_MAIN + 'films/biopic/'])
    liste.append(['Comédie', URL_MAIN + 'films/comedie/'])
    liste.append(['Documentaire', URL_MAIN + 'documentaires/'])
    liste.append(['Drame', URL_MAIN + 'films/drame/'])
    liste.append(['Epouvante Horreur', URL_MAIN + 'films/horreur/'])
    liste.append(['Fantastique', URL_MAIN + 'films/fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'films/guerre/'])
    liste.append(['Historique', URL_MAIN + 'films/historique/'])
    liste.append(['Policier', URL_MAIN + 'films/policier/'])
    liste.append(['Romance', URL_MAIN + 'films/romance/'])
    liste.append(['Science Fiction', URL_MAIN + 'films/science-fiction/'])
    liste.append(['Thriller', URL_MAIN + 'films/thriller/'])
    liste.append(['Western', URL_MAIN + 'films/western/'])
    liste.append(['Divers', URL_MAIN + 'films/divers/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
