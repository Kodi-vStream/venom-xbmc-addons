#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, dialog
from resources.lib.config import GestionCookie
from resources.lib.util import Unquote

import re, random, requests, base64

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

SITE_IDENTIFIER = 'ddl1'
SITE_NAME = '[COLOR violet]DDL1[/COLOR]'
SITE_DESC = 'Films/Séries/Reportages/Concerts'

URL_MAIN = "https://www.ddl1.best/"
URL_SEARCH = (URL_MAIN + 'index.php?do=search&subaction=search&story=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS  = (URL_MAIN + 'films/', 'showMovies')
MOVIE_EXCLUS = (URL_MAIN + 'films/exclue/', 'showMovies')
MOVIE_BDRIP = (URL_MAIN + 'films/dvdrip/', 'showMovies')
MOVIE_MKV = (URL_MAIN + 'films/dvdrip-mkv-x264/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'films/films-vostfr/', 'showMovies') # films VOSTFR
MOVIE_VOSTFR_MKV = (URL_MAIN + 'films/films-vostfr-mkv-x264/', 'showMovies') # films VOSTFR
MOVIE_CAM = (URL_MAIN + 'r5-scr-ts-cam/', 'showMovies') # films VOSTFR
MOVIE_HD = (URL_MAIN + 'bluray-1080p-720p.html', 'showMovies')
MOVIE_WEBDL = (URL_MAIN + 'web-1080p-720p.html/', 'showMovies')
MOVIE_HDLIGHT = (URL_MAIN + 'films-hdlight/', 'showMovies')
MOVIE_3D = (URL_MAIN + 'films/bluray-3d/', 'showMovies')
MOVIE_DVD = (URL_MAIN + 'films/dvd/', 'showMovies')
OLD_MOVIE = (URL_MAIN + 'vieux-films.html', 'showMovies')
FILM_ANIMATION = (URL_MAIN + 'dessins-animes/', 'showMovies')
MOVIE_VFSTFR = (URL_MAIN + 'films/films-vfstfr/', 'showMovies')

MOVIE_2010 = (URL_MAIN + 'films-2010-2019.html', 'showMovies')
MOVIE_2000 = (URL_MAIN + 'films-2000-2009.html', 'showMovies')
MOVIE_1990 = (URL_MAIN + 'films-1990-1999.html', 'showMovies')
MOVIE_1980 = (URL_MAIN + 'films-1980-1989.html', 'showMovies')
MOVIE_1970 = (URL_MAIN + 'films-1970-1979.html', 'showMovies')
MOVIE_1960 = (URL_MAIN + 'films-1960-1969.html', 'showMovies')
MOVIE_1950 = (URL_MAIN + 'films-1950-1959.html', 'showMovies')
MOVIE_1900 = (URL_MAIN + 'films-1920-1949.html', 'showMovies')

MOVIE_GENRES = ('films-gratuit/', 'showGenre')
SERIE_GENRES = ('telecharger-series/', 'showGenre')

SERIE_SERIES = (True, 'showMenuSeries')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_VF = (URL_MAIN + 'series/series-vf/', 'showMovies')
SERIE_VF_720 = (URL_MAIN + 'series/series-vf-720p/','showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'series/series-vostfr/', 'showMovies')
SERIE_VOSTFRS_720 = (URL_MAIN + 'series/series-vostfr-720p/','showMovies')
PACK_SERIE_VOSTFRS = (URL_MAIN + 'series/pack-sries-vf-sd/', 'showMovies')
PACK_SERIE_VOSTFRS_720 = (URL_MAIN + 'series/pack-sries-vf-hd-720p/','showMovies')
PACK_SERIE_VOSTFRS_1080 = (URL_MAIN + 'series/pack-sries-vf-hd-1080p/','showMovies')

ANIM_ANIMS = (True, 'showMenuMangas')
ANIM_VFS = (URL_MAIN + 'dessin-anime-mangas/animes-vf/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'dessin-anime-mangas/animes-vostfr/', 'showMovies')
FILM_ANIM = (URL_MAIN + 'dessin-anime-mangas/films-mangas/', 'showMovies')

DOC_NEWS = (URL_MAIN + 'documentaires/', 'showMovies')
TV_NEWS = (URL_MAIN + 'emissions-tv/', 'showMovies')
SPECT_NEWS = (URL_MAIN + 'spectacles/', 'showMovies')
CONCERT_NEWS = (URL_MAIN + 'concerts/', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuAutres', 'Autres', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EXCLUS[1], 'Exclus (Films populaires)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (bluray 1080p/720p)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIP[1], 'Films (BDRIP)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MKV[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MKV[1], 'Films (dvdrip mkv)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films (1080p - Light)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Films (3D)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films en VOSTFR', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR_MKV[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR_MKV[1], 'Films en VOSTFR (format mkv)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CAM[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CAM[1], 'Films (CAM)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_DVD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_DVD[1], 'Films (DVD)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', OLD_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, OLD_MOVIE[1], 'Anciens Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', FILM_ANIMATION[0])
    oGui.addDir(SITE_IDENTIFIER, FILM_ANIMATION[1], 'Films d Animation', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VFSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VFSTFR[1], 'Films en VFSTFR', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_2010[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_2010[1], 'Films (2010)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_2000[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_2000[1], 'Films (2000)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1990[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1990[1], 'Films (1990)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1980[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1980[1], 'Films (1980)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1970[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1970[1], 'Films (1970)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1960[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1960[1], 'Films (1960)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1950[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1950[1], 'Films (1950)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1900[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1900[1], 'Films (1900)', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VF[1], 'Séries (VF)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF_720[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VF_720[1], 'Séries 720p (VF)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS_720[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS_720[1], 'Séries 720p (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', PACK_SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, PACK_SERIE_VOSTFRS[1], 'Saison complet (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', PACK_SERIE_VOSTFRS_720[0])
    oGui.addDir(SITE_IDENTIFIER, PACK_SERIE_VOSTFRS_720[1], 'Saison complet en 720p (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', PACK_SERIE_VOSTFRS_1080[0])
    oGui.addDir(SITE_IDENTIFIER, PACK_SERIE_VOSTFRS_1080[1], 'Saison complet en 1080p (VOSTFR)', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher Animes', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animes (VF)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animes (VOSTFR)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', FILM_ANIM[0])
    oGui.addDir(SITE_IDENTIFIER, FILM_ANIM[1], 'Films d\'animes ', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuAutres():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MISC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher autres', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPECT_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SPECT_NEWS[1], 'Spectacles', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', CONCERT_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, CONCERT_NEWS[1], 'Concerts', 'music.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', TV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, TV_NEWS[1], 'Emissions TV', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sUrl + sSearchText + '&search_start=1'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    listeGenres = ['action', 'animation', 'arts-martiaux', 'aventure', 'biopic', 'comédie-dramatique',
                   'comédie-musicale', 'comédie', 'divers', 'documentaire', 'drame', 'epouvante-horreur', 'espionnage',
                   'famille', 'fantastique', 'guerre', 'historique', 'musical', 'péplum',
                   'policier', 'romance', 'science-fiction', 'thriller', 'western']
    for genre in listeGenres:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + genre.replace(' ', '%20')+ '.html')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', genre, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if sSearch:
        sUrl = sSearch

    sPattern = '<a class="th-in" href="([^"]+)">.+?<img src="([^"]+)".+?" title="([^"]+)".+?<div class="th-tip-meta.+?<span>([^<]+)</span>.+?style="color: #aaa;">([^<]+)</span>'

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    aResult = oParser.parse(sHtmlContent, sPattern)

    titles = set()
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]
            sYear = aEntry[3]
            sDesc = aEntry[4]

            # Enlever les films en doublons (même titre et même année)
            # il s'agit du même film dans une autre qualité qu'on retrouvera au moment du choix de la qualité
            key = sTitle + "-" + sYear
            if key in titles :
                continue;
            titles.add(key)

            sDesc = re.sub('<[^<]+?>', '', sDesc)
            sDisplayTitle = sTitle

            if not sThumb.startswith('http'):
                sThumb = URL_MAIN[:-1] + sThumb

            if not sUrl2.startswith('http'):
                sUrl2 = URL_MAIN[:-1] + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if '/series/' in sUrl or ('animes' in sUrl and not 'films' in sUrl) or 'emissions-tv' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sUrl, sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sUrl, sHtmlContent):
    #Récupeartion de la page actuel dans l'url
    try:
        pageNext = int(re.search('page/([0-9]+)',sUrl).group(1)) + 1
    except AttributeError:
        pageNext = 2

    try:
        extractPageList = re.search('<div class="navigation">(.+?)</div>', sHtmlContent, re.MULTILINE|re.DOTALL).group(1)

        oParser = cParser()
        sPattern = '<a href="([^"]+)">' + str(pageNext) + '</a>'
        aResult = oParser.parse(extractPageList, sPattern)

        if (aResult[0] == True):
            nextPage = aResult[1][0]
            if not nextPage.startswith('https'):
                nextPage = URL_MAIN[:-1] + nextPage
            return nextPage
        return False

    except AttributeError:
        return False

def showMoviesLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    #Affichage du texte
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles pour ce film:[/COLOR]')

    #récupération du Synopsis
    sPattern = '<span style="color: #aaa;">([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = aResult[1][0]
        sDesc = sDesc.replace('<span>', '').replace('</span>', '')
        sDesc = sDesc.replace('<b>', '').replace('</b>', '')
        sDesc = sDesc.replace('<i>', '').replace('</i>', '')
        sDesc = sDesc.replace('<br>', '').replace('<br />', '')

    #on recherche d'abord la qualité courante
    sPattern = '<span><h2 style="font-size: 16px;font-weight: lighter;">([^"]+)</h2></span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sTitle = sMovieTitle
    if (aResult[0]):
        sLang = aResult[1][1]
        sTitle = ('%s (%s)') % (sMovieTitle, sLang)

    # On ajoute le lien même si on n'a pas réussi à déterminer la qualité
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oOutputParameterHandler.addParameter('sDesc', sDesc)
    oOutputParameterHandler.addParameter('sYear', sYear)

    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    #on regarde si dispo dans d'autres qualités
    sPattern = '<a href="([^"]+)"><span class="ffas js-guest icon-left" title="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb=oInputParameterHandler.getValue('sThumb')
    sDesc=oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sPattern = '<i class="fas fa-cloud-download-alt".+?</i>([^<]+)</div>.+?<a href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    #Le site dipose de plusieurs paterne.
    if (aResult[0] == False):
        sPattern = '<a href="([^"]+)".+?rel="noopener external noreferrer">(?!Partie)([^<]+)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sHoster = aEntry[1]
            sUrl2 = aEntry[0]
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHoster)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addMovie(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    elif (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sHoster = aEntry[0]
            sUrl2 = aEntry[1]
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHoster)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addMovie(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showSeriesHosters():
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb=oInputParameterHandler.getValue('sThumb')
    sDesc=oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = GetLink(oRequestHandler.request())

    oParser = cParser()
    sPattern = '<i class="fas fa-cloud-download-alt" style="margin-right: 10px;"></i>([^<]+)</div></b>|<a href="([^"]+)".+?rel="noopener external noreferrer">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oGui = cGui()
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + re.sub('\.\w+', '', aEntry[0]) + '[/COLOR]')

            else:
                sUrl2 = aEntry[1]
                sTitle = sMovieTitle + ' ' + aEntry[2].replace('pisode ','').replace('FINAL ', '')
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        oGui.setEndOfDirectory()
    else:   # certains films mals classés apparaissent dans les séries
        showHosters()

def Display_protected_link():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    #Passage avec requests car la protection a tendance a ne pas fonctionner correctement
    #Solution pas encore touver

    payload = "folder=Continuer"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Content-Type':'application/x-www-form-urlencoded',
            'Content-Length':'16'}

    r = requests.post(sUrl.replace('http','https'), headers=headers, data=payload)
    sHtmlContent = r.content

    oParser = cParser()
    sPattern = '<h4>Vos liens prot&eacute;g&eacute;es</h4></center>.+?<a href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sHosterUrl = base64.b64decode(Unquote(aResult[1][0].split('?url=')[1]))
    sTitle = sMovieTitle

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sTitle)
        oHoster.setFileName(sTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def GetLink(sHtmlContent):
    oParser = cParser()
    sPattern = '<div class="link">(.+?)<div class="sect fcomms">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        return aResult[1][0]
    else:
        return sHtmlContent

    return ''
