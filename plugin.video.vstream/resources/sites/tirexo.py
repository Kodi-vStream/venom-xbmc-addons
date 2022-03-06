# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# import random
# import time
# import xbmc
import re
import requests

from resources.lib.comaddon import progress, dialog
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
# from resources.lib.config import GestionCookie
from resources.lib.util import cUtil

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

SITE_IDENTIFIER = 'tirexo'
SITE_NAME = '[COLOR violet]Tirexo[/COLOR]'
SITE_DESC = 'Films/Séries/Reportages/Concerts'

# Teste pour le moment avec une url fixe.
URL_MAIN = "https://www2.tirexo.art/"

URL_SEARCH_MOVIES = (URL_MAIN + 'index.php?do=search&subaction=search&search_start=0&full_search=1&result_from=1&story=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'index.php?do=search&subaction=search&search_start=0&catlist=15&story=', 'showMovies')
URL_SEARCH_ANIMS = (URL_MAIN + 'index.php?do=search&subaction=search&search_start=0&catlist=32&story=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + 'index.php?do=search&subaction=search&search_start=0&catlist[]=75&catlist[]=76&catlist[]=77&catlist[]=79&catlist[]=101&story=', 'showMovies')

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_COLLECTION = (URL_MAIN + 'collections/', 'showMovies')
MOVIE_EXCLUS = (URL_MAIN + 'exclus/', 'showMovies')
MOVIE_3D = (URL_MAIN + 'films-bluray-3d/', 'showMovies')
MOVIE_SD = (URL_MAIN + 'films-bluray-hd/', 'showMovies')
MOVIE_MKV = (URL_MAIN + 'films-mkv/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'films-bluray-hd-1080/', 'showMovies')
MOVIE_BDRIP = (URL_MAIN + 'films-dvdrip-bdrip/', 'showMovies')
MOVIE_SDLIGHT = (URL_MAIN + 'hdlight-720/', 'showMovies')
MOVIE_HDLIGHT = (URL_MAIN + 'hdlight-1080/', 'showMovies')
MOVIE_4KL = (URL_MAIN + 'film-ultra-hdlight-x265/', 'showMovies')
MOVIE_4K = (URL_MAIN + 'film-ultra-hd-x265/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'films-gratuit/', 'showMovies')
MOVIE_ANNEES = (URL_MAIN + 'films-gratuit/', 'showYears')

MOVIE_2020 = (URL_MAIN + 'films-2020-2030/', 'showMovies')
MOVIE_2010 = (URL_MAIN + 'films-2010-2019/', 'showMovies')
MOVIE_2000 = (URL_MAIN + 'films-2000-2009/', 'showMovies')
MOVIE_1990 = (URL_MAIN + 'films-1990-1999/', 'showMovies')
MOVIE_1980 = (URL_MAIN + 'films-1980-1989/', 'showMovies')
MOVIE_1970 = (URL_MAIN + 'films-1970-1979/', 'showMovies')
MOVIE_1960 = (URL_MAIN + 'films-1960-1969/', 'showMovies')
MOVIE_1950 = (URL_MAIN + 'films-1950-1959/', 'showMovies')
MOVIE_1900 = (URL_MAIN + 'films-1900-1950/', 'showMovies')

MOVIE_GENRES = ('films-gratuit/', 'showGenres')
SERIE_GENRES = ('telecharger-series/', 'showGenres')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_VFS = (URL_MAIN + 'series-vf/', 'showMovies')
SERIE_VF_720 = (URL_MAIN + 'series-vf-en-hd/', 'showMovies')
SERIE_VF_1080 = (URL_MAIN + 'series-vf-1080p/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'series-vostfr/', 'showMovies')
SERIE_VOSTFRS_720 = (URL_MAIN + 'series-vostfr-hd/', 'showMovies')
SERIE_VOSTFRS_1080 = (URL_MAIN + 'series-vostfr-1080p/', 'showMovies')
SERIE_VO = (URL_MAIN + 'series-vo/', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'telecharger-series/', 'showMovies')

ANIM_ANIMS = (True, 'showMenuMangas')
ANIM_VFS = (URL_MAIN + 'animes-vf/', 'showMovies')
ANIM_VF_720 = (URL_MAIN + 'animes-vf-720p/', 'showMovies')
ANIM_VF_1080 = (URL_MAIN + 'animes-vf-1080p/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'animes-vostfr/', 'showMovies')
ANIM_VOSTFRS_720 = (URL_MAIN + 'animes-vostfr-720p/', 'showMovies')
ANIM_VOSTFRS_1080 = (URL_MAIN + 'animes-vostfr-1080p/', 'showMovies')
FILM_ANIM = (URL_MAIN + 'films-animes/', 'showMovies')
ANIM_NEWS = (URL_MAIN + 'animes/', 'showMovies')

DOC_NEWS = (URL_MAIN + 'emissions-tv-documentaires/documentaire', 'showMovies')
SPORT_REPLAY = (URL_MAIN + 'emissions-tv-documentaires/sport', 'showMovies')
TV_NEWS = (URL_MAIN + 'emissions-tv-documentaires/emissions-tv/', 'showMovies')
SPECT_NEWS = (URL_MAIN + '?do=cat&category=emissions-tv-documentaires/spectacle&epoque=2022', 'showMovies')
CONCERT_NEWS = (URL_MAIN + '?do=cat&category=musiques-mp3-gratuite/concerts&epoque=2022', 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuAutres', 'Autres', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COLLECTION[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_COLLECTION[1], 'Les collections', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EXCLUS[1], 'Exclus (Films populaires)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD[1], 'Films (720p)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (1080p)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIP[1], 'Films (BDRIP)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4K[1], 'Films (4K)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MKV[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MKV[1], 'Films (dvdrip mkv)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SDLIGHT[1], 'Films (720p - Light)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films (1080p - Light)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4KL[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4KL[1], 'Films (4K - light)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Films (3D)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF_720[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries 720p (VF)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF_1080[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries 1080p (VF)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS_720[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS_720[1], 'Séries 720p (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS_1080[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS_1080[1], 'Séries 1080p (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VO[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VO[1], 'Séries (VO)', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher Animes', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animes (VF)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VF_720[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VF_720[1], 'Animes 720p (VF)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VF_1080[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VF_1080[1], 'Animes 1080p (VF)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animes (VOSTFR)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS_720[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS_720[1], 'Animes 720p (VOSTFR)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS_1080[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS_1080[1], 'Animes 1080p (VOSTFR)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', FILM_ANIM[0])
    oGui.addDir(SITE_IDENTIFIER, FILM_ANIM[1], 'Films d\'animes ', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_2020[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_2020[1], 'Films (2020)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_2010[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_2010[1], 'Films (2010)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_2000[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_2000[1], 'Films (2000)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1990[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1990[1], 'Films (1990)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1980[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1980[1], 'Films (1980)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1970[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1970[1], 'Films (1970)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1960[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1960[1], 'Films (1960)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1950[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1950[1], 'Films (1950)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1900[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1900[1], 'Films (1900)', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuAutres():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MISC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher autres', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_REPLAY[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_REPLAY[1], 'Sports', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPECT_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SPECT_NEWS[1], 'Spectacles', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', CONCERT_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, CONCERT_NEWS[1], 'Concerts', 'music.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', TV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, TV_NEWS[1], 'Emissions TV', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if sSearchText is not False:
        sUrl = sUrl + sSearchText  # + '&search_start=0'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    URL_MOVIES = URL_MAIN + sUrl + '?do=cat&category=telecharger-series&genre='

    listeGenres = ['Action', 'Animation', 'Arts Martiaux', 'Aventure', 'Biopic', 'Bollywood', 'Comédie Dramatique',
                   'Comédie Musicale', 'Comédie', 'Documentaire', 'Drame', 'Epouvante-horreur', 'Espionnage',
                   'Famille', 'Fantastique', 'Guerre', 'Historique', 'Horreur', 'Musical', 'Péplum', 'Policier',
                   'Romance', 'Science Fiction', 'Thriller', 'Western']

    oOutputParameterHandler = cOutputParameterHandler()
    for genre in listeGenres:
        oOutputParameterHandler.addParameter('siteUrl', URL_MOVIES + genre.replace(' ', '%20'))
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', genre, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_ANIMS[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_MISC[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch

    if sSearch or "index" in sUrl:  # en mode recherche
        sPattern = 'mov"><a class="mov-t nowrap" href="([^"]+)" title="([^"]+).+?data-content="(.*?)" class="mov-i img-box"><img src="([^"]+)'
        validUrl = ['films', 'series', 'animes', 'concerts', 'emissions-tv-documentaires']
    elif 'collections/' in sUrl:
        sPattern = 'tcarusel-item.+?href="([^"]+).+?title="([^"]+)" data-content="([^"]*).+?src="([^"]+)'
    else:
        sPattern = 'data-content="([^"]*).+?img src="([^"]+).+?title="([^"]+).+?mov-t nowrap" href="([^"]+)'

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    aResult = oParser.parse(sHtmlContent, sPattern)

    titles = set()
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if sSearch or 'index' in sUrl:
                # On exclus tout ce qui n'est pas lisible par Kodi.
                if any(x in aEntry[0] for x in validUrl):
                    sUrl2 = aEntry[0]
                    sTitle = aEntry[1]
                    sDesc = aEntry[2]
                    sThumb = URL_MAIN[:-1] + aEntry[3]
                    if sSearch:
                        if not oUtil.CheckOccurence(sSearchText, sTitle):
                            continue    # Filtre de recherche
                else:
                    continue
            elif 'collections/' in sUrl:
                sUrl2 = aEntry[0]
                sTitle = aEntry[1].replace(' - Saga', '')
                sDesc = aEntry[2]
                sThumb = URL_MAIN[:-1] + aEntry[3]
            else:
                sUrl2 = aEntry[3]
                sDesc = aEntry[0]
                sThumb = URL_MAIN[:-1] + aEntry[1]
                sTitle = aEntry[2]

            # Enlever les films en doublons (même titre)
            # il s'agit du même film dans une autre qualité qu'on retrouvera au moment du choix de la qualité
            if sTitle in titles:
                continue
            titles.add(sTitle)

            # sDesc = re.sub('<[^<]+?>', '', sDesc)
            sDisplayTitle = sTitle

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if any(x in sUrl2 for x in ['series', 'animes', 'saison']):
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif 'collections/' in sUrl:
                oGui.addMoviePack(SITE_IDENTIFIER, 'showCollec', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        if not sSearch:
            if 'index' in sUrl:
                sPattern = '<a name="nextlink".+?javascript:list_submit\((.+?)\)'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0] is True:
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', re.sub('search_start=(\d+)', 'search_start=' + str(aResult[1][0]), sUrl))
                    number = re.search('([0-9]+)', aResult[1][0]).group(1)
                    oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + number, oOutputParameterHandler)
            else:
                sNextPage, sPaging = __checkForNextPage(sHtmlContent)
                if sNextPage is not False:
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                    oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>(\d+)</a></li><li><a href="([^"]+)"><span class="fa fa-arrow-right">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return URL_MAIN[:-1] + sNextPage, sPaging

    return False, 'none'


def showCollec():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sPattern = 'class="mov-t nowrap" href="([^"]+).+?data-content="([^"]*).+?<img src="([^"]+).+?title="([^"]+)'

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    aResult = oParser.parse(sHtmlContent, sPattern)

    titles = set()
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sDesc = aEntry[1]
            sThumb = aEntry[2]
            sTitle = aEntry[3]

            # Enlever les films en doublons (même titre)
            # il s'agit du même film dans une autre qualité qu'on retrouvera au moment du choix de la qualité
            if sTitle in titles:
                continue
            titles.add(sTitle)

            sDesc = re.sub('<[^<]+?>', '', sDesc)
            sDisplayTitle = sTitle

            if not sThumb.startswith('http'):
                sThumb = URL_MAIN[:-1] + sThumb

            if not sUrl2.startswith('http'):
                sUrl2 = URL_MAIN[:-1] + sUrl2

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showMoviesLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    if not sDesc:
        try:
            sPattern = '<h3 class="">Description</h3>(.+?)</div>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sDesc = aResult[1][0]
        except:
            pass

    # liens download
    sPattern = "domain=(.+?)'(.+?)/tbody"
    aResult = oParser.parse(sHtmlContent, sPattern)
    oOutputParameterHandler = cOutputParameterHandler()
    if aResult[0] is True:
        sPattern = "target='_blank' data-id='.+?' href='([^']+)"
        for aEntry in aResult[1]:
            sHost = aEntry[0]
            aResult = oParser.parse(aEntry[1], sPattern)
            if aResult[0] is True:
                for aEntry in aResult[1]:
                    sUrl2 = URL_MAIN[:-1] + aEntry
                    sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
            
                    oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sDesc', sDesc)
                    oGui.addLink(SITE_IDENTIFIER, 'Display_protected_link', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)
    
    # lien STREAMING
    sPattern = 'rel=.nofollow. class=.download. href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        sUrl2 = URL_MAIN[:-1] + aResult[1][0]
        sDisplayTitle = ('%s [Streaming]') % (sMovieTitle)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oGui.addLink(SITE_IDENTIFIER, 'showHostersLink', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    # on regarde si dispo dans d'autres qualités
    sPattern = "value='(.+?)'.+?<b>(.+?)</b>.+?<b> \((.+?)\)"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        # Affichage du texte
        oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Autres qualités disponibles :[/COLOR]')
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sQual = aEntry[1]
            sLang = aEntry[2]
            sDisplayTitle = ('%s [%s] (%s)') % (sMovieTitle, sQual, sLang)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    # Affichage du texte
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles pour cette saison :[/COLOR]')

    # récupération du Synopsis
    try:
        sPattern = '<h3 class="">Description</h3>(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    # Mise à jour du titre
    sPattern = '<h3 class="p-2">(.+?)</h3>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sTitle = sMovieTitle

    # on regarde si dispo dans d'autres qualités
    sHtmlContent1 = CutQual(sHtmlContent)

    sPattern1 = "value='(.+?)'.+?>(.+?)</b>.+?<b>(.+?)</b>.+?<b> \((.+?)\)"
    aResult1 = oParser.parse(sHtmlContent1, sPattern1)

    if aResult1[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult1[1]:
            if "Saison" not in aEntry[1]:
                sTitle = sMovieTitle + ' Saison ' + aEntry[1]
            else:
                sTitle = sMovieTitle + ' ' + aEntry[1].replace('<b>', '')

            sQual = aEntry[2]
            sLang = aEntry[3]
            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang)

            sUrl = URL_MAIN + "?subaction=get_links&version=" + aEntry[0]
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addSeason(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

    # Affichage du titre
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Autres saisons disponibles pour cette série :[/COLOR]')

    # on regarde si dispo dans d'autres saison
    sHtmlContent1 = CutSais(sHtmlContent)

    sPattern1 = '<option value="([^"]+)">([^<]+)<'
    aResult1 = oParser.parse(sHtmlContent1, sPattern1)

    if aResult1[0] is True:
        # Une ligne par saison, pas besoin d'afficher les qualités ici
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult1[1]:

            sSaison = aEntry[1]
            sDisplayTitle = ('%s %s') % (sMovieTitle, sSaison)

            sUrl = aEntry[0]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sSaison', sSaison)
            oGui.addSeason(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = "domain=(.+?)\.|'download' target='_blank' data-id='.+?' href='([^']+)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:

        for aEntry in aResult[1]:
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + re.sub('\.\w+', '', aEntry[0]) + '[/COLOR]')

            else:
                if URL_MAIN not in aEntry[1]:
                    sUrl2 = URL_MAIN[:-1] + aEntry[1]
                    sTitle = sMovieTitle
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oGui.addLink(SITE_IDENTIFIER, 'Display_protected_link', sTitle, sThumb, sDesc, oOutputParameterHandler)

        oGui.setEndOfDirectory()
    else:
        showHosters()


def showHostersLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    sPattern = '<iframe.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        if not aResult[1][0].startswith('http'):
            sHosterUrl = "https:" + aResult[1][0]
        else:
            sHosterUrl = aResult[1][0]

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster is not False:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showSeriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = "\?domain=(.+?)\.|'download' rel=.+?>([^<]+).+?href=([^']+)\""
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:

        for aEntry in aResult[1]:
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + re.sub('\.\w+', '', aEntry[0]) + '[/COLOR]')
            else:
                if URL_MAIN not in aEntry[2]:
                    sUrl2 = URL_MAIN[:-1] + aEntry[2].replace('\\', '').replace('"', '')
                    sTitle = sMovieTitle + ' ' + aEntry[1].replace('FINAL ', '')
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oGui.addEpisode(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        oGui.setEndOfDirectory()
    else:
        showHosters()


def Display_protected_link():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl').replace('\\', '').replace('"', '')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if not sUrl.startswith('http'):
        sUrl = 'http://' + sUrl

    oRequestHandler = cRequestHandler(sUrl.replace('link', 'streaming').replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<iframe.+?src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:

        for aEntry in aResult[1]:
            sHosterUrl = aEntry.replace('uptostream', 'uptobox')

            sTitle = sMovieTitle
            if len(aResult[1]) > 1:
                sTitle = sMovieTitle

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster is not False:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def CutQual(sHtmlContent):
    oParser = cParser()
    sPattern = '<select id="qualite" name="qualite" class="form-control">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    else:
        return sHtmlContent

    return ''


def CutSais(sHtmlContent):
    oParser = cParser()
    sPattern = '<select id="saison".+?class="form-control">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    return ''


def DecryptDlProtecte(url):

    """ Nouvelle méthode pour dl protect qui passe par requests"""
    s = requests.Session()

    response = s.get(url)
    sHtmlContent = str(response.content)
    cookie_string = "; ".join([str(x) + "=" + str(y) for x, y in s.cookies.items()])

    sPattern = 'type="hidden" name="_token" value="(.+?)">'
    aResult = re.search(sPattern, sHtmlContent).group(1)

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('Host', url.split('/')[2])
    oRequestHandler.addHeaderEntry('Referer', url)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Content-Length', len(str("_token=" + aResult + "&getlink=1")))
    oRequestHandler.addHeaderEntry('Content-Type', "application/x-www-form-urlencoded")
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    oRequestHandler.addHeaderEntry('Cookie', cookie_string)
    oRequestHandler.addParameters("_token", aResult)
    oRequestHandler.addParametersLine("_token=" + aResult + "&getlink=1")

    sHtmlContent = oRequestHandler.request()

    return sHtmlContent

# ******************************************************************************
# from http://code.activestate.com/recipes/578668-encode-multipart-form-data-for-uploading-files-via/


"""Encode multipart form data to upload files via POST."""


def encode_multipart(fields, files, boundary):
    r"""Encode dict of form fields and dict of files as multipart/form-data.
    Return tuple of (body_string, headers_dict). Each value in files is a dict
    with required keys 'filename' and 'content', and optional 'mimetype' (if
    not specified, tries to guess mime type or uses 'application/octet-stream').

    >>> body, headers = encode_multipart({'FIELD': 'VALUE'},
    ...                                  {'FILE': {'filename': 'F.TXT', 'content': 'CONTENT'}},
    ...                                  boundary='BOUNDARY')
    >>> print('\n'.join(repr(l) for l in body.split('\r\n')))
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FIELD"'
    ''
    'VALUE'
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FILE"; filename="F.TXT"'
    'Content-Type: text/plain'
    ''
    'CONTENT'
    '--BOUNDARY--'
    ''
    >>> print(sorted(headers.items()))
    [('Content-Length', '193'), ('Content-Type', 'multipart/form-data; boundary=BOUNDARY')]
    >>> len(body)
    193
    """

    import mimetypes
    import string

    _BOUNDARY_CHARS = string.digits

    def escape_quote(s):
        return s.replace('"', '\\"')

    lines = []

    for name, value in fields.items():
        lines.extend(('-----------------------------{0}'.format(boundary),
                      'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name)), '', str(value),
                      '-----------------------------{0}--'.format(boundary), ''))

    for name, value in files.items():
        filename = value['filename']
        if 'mimetype' in value:
            mimetype = value['mimetype']
        else:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        lines.extend((
            '--{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name), escape_quote(filename)),
            'Content-Type: {0}'.format(mimetype),
            '',
            value['content']))

    body = '\r\n'.join(lines)

    headers = {'Content-Type': 'multipart/form-data; boundary=---------------------------{0}'.format(boundary),
               'Content-Length': str(len(body))}

    return body, headers
