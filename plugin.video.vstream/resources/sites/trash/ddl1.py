# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
return False  # 09/02/22 - NPAI

import re
import requests
import base64

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
from resources.lib.util import Unquote

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

SITE_IDENTIFIER = 'ddl1'
SITE_NAME = '[COLOR violet]DDL[/COLOR]'
SITE_DESC = 'Films/Séries/Reportages/Concerts'

URL_MAIN = "https://www.ddl-best.net/"
URL_SEARCH = (URL_MAIN + 'index.php?do=search&subaction=search&story=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_EXCLUS = (URL_MAIN + 'films/exclue/', 'showMovies')
MOVIE_BDRIP = (URL_MAIN + 'films/dvdrip/', 'showMovies')
MOVIE_MKV = (URL_MAIN + 'films/dvdrip-mkv-x264/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'films/films-vostfr/', 'showMovies')  # films VOSTFR
MOVIE_VOSTFR_MKV = (URL_MAIN + 'films/films-vostfr-mkv-x264/', 'showMovies')  # films VOSTFR
MOVIE_CAM = (URL_MAIN + 'r5-scr-ts-cam/', 'showMovies')  # films VOSTFR
MOVIE_HD = (URL_MAIN + 'bluray-1080p-720p.html', 'showMovies')
MOVIE_WEBDL = (URL_MAIN + 'web-1080p-720p.html/', 'showMovies')
MOVIE_HDLIGHT = (URL_MAIN + 'films-hdlight/', 'showMovies')
MOVIE_3D = (URL_MAIN + 'films/bluray-3d/', 'showMovies')
MOVIE_DVD = (URL_MAIN + 'films/dvd/', 'showMovies')
OLD_MOVIE = (URL_MAIN + 'vieux-films.html', 'showMovies')
FILM_ANIMATION = (URL_MAIN + 'films/anime-films/', 'showMovies')
MOVIE_VFSTFR = (URL_MAIN + 'films/films-vfstfr/', 'showMovies')

MOVIE_ANNEES = (True, 'showYears')
MOVIE_2010 = (URL_MAIN + 'films-2010-2019.html', 'showMovies')
MOVIE_2000 = (URL_MAIN + 'films-2000-2009.html', 'showMovies')
MOVIE_1990 = (URL_MAIN + 'films-1990-1999.html', 'showMovies')
MOVIE_1980 = (URL_MAIN + 'films-1980-1989.html', 'showMovies')
MOVIE_1970 = (URL_MAIN + 'films-1970-1979.html', 'showMovies')
MOVIE_1960 = (URL_MAIN + 'films-1960-1969.html', 'showMovies')
MOVIE_1950 = (URL_MAIN + 'films-1950-1959.html', 'showMovies')
MOVIE_1900 = (URL_MAIN + 'films-1920-1949.html', 'showMovies')

MOVIE_GENRES = ('films-gratuit/', 'showGenre')
# SERIE_GENRES = ('telecharger-series/', 'showGenre')

SERIE_SERIES = (True, 'showMenuSeries')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_VF = (URL_MAIN + 'series/series-vf/', 'showMovies')
SERIE_VF_720 = (URL_MAIN + 'series/series-vf-720p/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'series/series-vostfr/', 'showMovies')
SERIE_VOSTFRS_720 = (URL_MAIN + 'series/series-vostfr-720p/', 'showMovies')
PACK_SERIE_VOSTFRS = (URL_MAIN + 'series/pack-sries-vf-sd/', 'showMovies')
PACK_SERIE_VOSTFRS_720 = (URL_MAIN + 'series/pack-sries-vf-hd-720p/', 'showMovies')
PACK_SERIE_VOSTFRS_1080 = (URL_MAIN + 'series/pack-sries-vf-hd-1080p/', 'showMovies')

ANIM_ANIMS = (True, 'showMenuMangas')
ANIM_VFS = (URL_MAIN + 'dessin-anime-mangas/animes-vf/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'dessin-anime-mangas/animes-vostfr/', 'showMovies')
FILM_ANIMS = (URL_MAIN + 'dessin-anime-mangas/films-mangas/', 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Animés', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EXCLUS[1], 'Exclus (Films populaires)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showYears', 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (bluray 1080p/720p)', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIP[1], 'Films (BDRIP)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MKV[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MKV[1], 'Films (dvdrip mkv)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films (1080p - Light)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Films (3D)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films en VOSTFR', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR_MKV[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR_MKV[1], 'Films en VOSTFR (format mkv)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CAM[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CAM[1], 'Films (CAM)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_DVD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_DVD[1], 'Films (DVD)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', OLD_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, OLD_MOVIE[1], 'Anciens Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', FILM_ANIMATION[0])
    oGui.addDir(SITE_IDENTIFIER, FILM_ANIMATION[1], 'Films d Animation', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VFSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VFSTFR[1], 'Films en VFSTFR', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VF[1], 'Séries (VF)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF_720[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VF_720[1], 'Séries 720p (VF)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS_720[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS_720[1], 'Séries 720p (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', PACK_SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, PACK_SERIE_VOSTFRS[1], 'Saison complète (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', PACK_SERIE_VOSTFRS_720[0])
    oGui.addDir(SITE_IDENTIFIER, PACK_SERIE_VOSTFRS_720[1], 'Saison complet en 720p (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', PACK_SERIE_VOSTFRS_1080[0])
    oGui.addDir(SITE_IDENTIFIER, PACK_SERIE_VOSTFRS_1080[1], 'Saison complet en 1080p (VOSTFR)', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher Animés', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', FILM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, FILM_ANIMS[1], 'Films d\'animés ', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        sUrl = sUrl + sSearchText + '&search_start=1'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenre():
    oGui = cGui()

    listeGenres = ['action', 'animation', 'arts-martiaux', 'aventure', 'biopic', 'comédie-dramatique',
                   'comédie-musicale', 'comédie', 'divers', 'documentaire', 'drame', 'epouvante-horreur', 'espionnage',
                   'famille', 'fantastique', 'guerre', 'historique', 'musical', 'péplum',
                   'policier', 'romance', 'science-fiction', 'thriller', 'western']

    oOutputParameterHandler = cOutputParameterHandler()
    for genre in listeGenres:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + genre.replace(' ', '%20') + '.html')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', genre.capitalize(), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_2010[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_2010[1], 'Films (2010 à 2019)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_2000[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_2000[1], 'Films (2000 à 2009)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1990[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1990[1], 'Films (1990 à 1999)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1980[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1980[1], 'Films (1980 à 1989)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1970[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1970[1], 'Films (1970 à 1979 )', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1960[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1960[1], 'Films (1960 à 1969)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1950[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1950[1], 'Films (1950 à 1959)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1900[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1900[1], 'Films (1920 à 1949)', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMisc = oInputParameterHandler.getValue('misc')  # Autre contenu

    if sSearch:
        sUrl = sSearch

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'th-in" href="([^"]+).+?src="([^"]+)" alt="([^"]+).+?th-tip-meta.+?(?:|<span>([^\D]+).+?)#aaa;">([^<]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    titles = set()
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            if not sUrl2.startswith('http'):
                sUrl2 = URL_MAIN[:-1] + sUrl2

            sThumb = aEntry[1]
            if not sThumb.startswith('http'):
                sThumb = URL_MAIN[:-1] + sThumb

            sTitle = aEntry[2]
            sYear = aEntry[3]
            sDesc = aEntry[4]

            # On enleve les résultats en doublons (même titre et même année)
            # il s'agit du même dans une autre qualité ils seront proposé à l'étape suivante de nouveau
            key = sTitle + "-" + sYear
            if key in titles:
                continue
            titles.add(key)

            sDesc = re.sub('<[^<]+?>', '', sDesc)
            sDisplayTitle = ('%s (%s)') % (sTitle, sYear)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if sMisc:
                oGui.addMisc(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif 'animes' in sUrl and not 'films' in sUrl:
                oGui.addAnime(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif '/series/' in sUrl or 'emissions-tv' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif '-saison-' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sUrl, sHtmlContent)
        if (sNextPage):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oOutputParameterHandler.addParameter('misc', sMisc)
            sNumPage = re.search('/([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sNumPage, oOutputParameterHandler)

    if not sSearch:  # Le moteur de recherche du site est correct, laisser le nextPage même en globalSearch
        oGui.setEndOfDirectory()


def __checkForNextPage(sUrl, sHtmlContent):
    # Récuperation de la page actuel dans l'url
    try:
        pageNext = int(re.search('page/([0-9]+)', sUrl).group(1)) + 1
    except AttributeError:
        pageNext = 2

    try:
        extractPageList = re.search('<div class="navigation">(.+?)</div>', sHtmlContent, re.MULTILINE | re.DOTALL).group(1)

        oParser = cParser()
        sPattern = '<a href="([^"]+)">' + str(pageNext) + '</a>'
        aResult = oParser.parse(extractPageList, sPattern)

        if aResult[0]:
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

    # Affichage du texte
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles pour ce film:[/COLOR]')

    # récupération du Synopsis
    sPattern = '<span style="color: #aaa;">([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = aResult[1][0]
        sDesc = sDesc.replace('<span>', '').replace('</span>', '')
        sDesc = sDesc.replace('<b>', '').replace('</b>', '')
        sDesc = sDesc.replace('<i>', '').replace('</i>', '')
        sDesc = sDesc.replace('<br>', '').replace('<br />', '')

    # on recherche d'abord la qualité courante
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
    oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    # on regarde si dispo dans d'autres qualités
    sPattern = '<a href="([^"]+)"><span class="ffas js-guest icon-left" title="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
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

    oParser = cParser()

    sPattern = '<i class="fas fa-cloud-download-alt".+?</i>([^<]+)</div>.+?<a href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    # Le site dipose de plusieurs paterne.
    if not aResult[0]:
        sPattern = '<a href="([^"]+)".+?rel="noopener external noreferrer">(?!Partie)([^<]+)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sHoster = aEntry[1]
            sUrl2 = aEntry[0]
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHoster)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addLink(SITE_IDENTIFIER, 'Display_protected_link', sTitle, sThumb, sDesc, oOutputParameterHandler)

    elif aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sHoster = aEntry[0]
            sUrl2 = aEntry[1]
            sTitle = sMovieTitle

            if "protect" not in sUrl2:
                oHoster = cHosterGui().checkHoster(sUrl2)
                if (oHoster):
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sUrl2, sThumb)

            else:

                sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHoster)

                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oGui.addLink(SITE_IDENTIFIER, 'Display_protected_link', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesHosters():
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = getLink(oRequestHandler.request())

    oParser = cParser()
    sPattern = 'download-alt" style="margin-right: 10px;"></i>([^<]+)|href="([^"]+)".+?external noreferrer">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oGui = cGui()
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                sHoster = aEntry[0]
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + re.sub('\.\w+', '', sHoster) + '[/COLOR]')

            else:
                sUrl2 = aEntry[1]
                sEpisode = aEntry[2].replace('pisode ', '').replace('FINAL ', '').replace('Télécharger', '')
                sTitle = sMovieTitle + ' ' + sEpisode

                if 'protect' not in sUrl2:
                    oHoster = cHosterGui().checkHoster(sUrl2)
                    if (oHoster):
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sUrl2, sThumb)

                else:
                    oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sHost', sHoster)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oGui.addEpisode(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        oGui.setEndOfDirectory()
    else:   # certains films mals classés apparaissent dans les séries
        showHosters()


def Display_protected_link():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    # Passage avec requests car la protection a tendance a ne pas fonctionner correctement
    # Solution pas encore touver

    payload = "folder=Continuer"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
               'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': '16'}

    r = requests.post(sUrl.replace('http:', 'https:'), headers=headers, data=payload)
    sHtmlContent = r.content

    oParser = cParser()
    sPattern = '<li style="list-style-type.+?<a href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sHosterUrl = base64.b64decode(Unquote(aResult[1][0].split('?url=')[1]))
    sTitle = sMovieTitle.replace('- Saison ', ' S')

    try:
        sHosterUrl = sHosterUrl.decode('utf-8')
    except:
        pass

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster):
        oHoster.setDisplayName(sTitle)
        oHoster.setFileName(sTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def getLink(sHtmlContent):
    oParser = cParser()
    sPattern = '<div class="link">(.+?)<div class="sect fcomms">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        return aResult[1][0]
    else:
        return sHtmlContent

    return ''
