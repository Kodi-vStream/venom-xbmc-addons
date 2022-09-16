# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
import json
import re

from resources.lib.comaddon import addon, dialog, progress, siteManager, VSlog
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
headers = {'User-Agent': UA}

SITE_IDENTIFIER = 'extreme_down'
SITE_NAME = '[COLOR violet]Extreme Down[/COLOR]'
SITE_DESC = 'films en streaming, streaming hd, streaming 720p, Films/séries, récent'

# Utiliser ce site pour retrouver le nom de domaine :
# https://www.extreme-down.info/

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH = (URL_MAIN + 'index.php?', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0] + 'do=search&subaction=search&titleonly=3&speedsearch=1&story=', 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0] + 'do=search&subaction=search&titleonly=3&speedsearch=2&story=', 'showMovies')
URL_SEARCH_ANIMS = (URL_SEARCH[0] + 'do=search&subaction=search&titleonly=3&speedsearch=4&story=', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0] + 'do=search&subaction=search&titleonly=3&speedsearch=3&story=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_HD1080 = (URL_MAIN + 'films-new-hd/new-bluray-1080p/', 'showMovies')
MOVIE_NEWS2021 = (URL_MAIN + 'films-new-hd/', 'showMovies')
# MOVIE_GENRES = (True, 'showGenres')
# MOVIE_ANNEES = (True, 'showMovieYears')

MOVIE_VOSTFR = (URL_MAIN + 'films-vostfr/dvdrip-vostfr', 'showMovies')
MOVIE_4K = (URL_MAIN + 'films-new-ultrahd/', 'showMovies')
MOVIE_720 = (URL_MAIN + 'films-new-hd/new-bluray-720p/', 'showMovies')
MOVIE_1080X265 = (URL_MAIN + 'films-hd/films-1080p-x265', 'showMovies')
MOVIE_BLURAYVOSTFR = (URL_MAIN + 'films-vostfr/films-1080p-vostfr', 'showMovies')
MOVIE_3D = (URL_MAIN + 'films-new-hd/new-full-bluray-3d', 'showMovies')
MOVIE_FULL1080P = (URL_MAIN + 'films-new-hd/new-full-bluray', 'showMovies')
MOVIE_FULL4K = (URL_MAIN + 'films-new-ultrahd/new-full-bluray-ultrahd-4k', 'showMovies')
MOVIE_WEBRIP4K = (URL_MAIN + 'films-new-ultrahd/new-webrip-4k', "showMovies")
MOVIE_REMUX4K = (URL_MAIN + 'films-new-ultrahd/new-ultrahd-4k', "showMovies")
MOVIE_LIGHT720 = (URL_MAIN + 'films-hdlight/hdlight-720p', 'showMovies')
MOVIE_LIGHT1080 = (URL_MAIN + 'films-hdlight/hdlight-1080p', 'showMovies')
MOVIE_LIGHTBDRIP = (URL_MAIN + 'films-new-hd/new-bdrip-720p', 'showMovies')
MOVIE_BDRIP = (URL_MAIN + 'films-sd/dvdrip', 'showMovies')
MOVIE_OLDDVD = (URL_MAIN + 'films-sd/ancien-dvdrip', 'showMovies')
MOVIE_FILMO = (URL_MAIN + 'films-sd/filmographie', 'showMovies')
MOVIE_CLASSIQUE_SD = (URL_MAIN + 'films-classique/classiques-sd', 'showMovies')
MOVIE_CLASSIQUE_HD = (URL_MAIN + 'films-classique/classiques-hd', 'showMovies')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_HD = (URL_MAIN + 'series-hd/1080p-series-vf', 'showMovies')
# SERIE_GENRES = (True, 'showGenres')
# SERIE_ANNEES = (True, 'showSerieYears')
SERIE_VOSTFRS = (URL_MAIN + 'series-hd/1080p-series-vostfr/', 'showMovies')
SERIE_720VO = (URL_MAIN + 'series-hd/hd-series-vostfr', 'showMovies')
SERIE_720VF = (URL_MAIN + 'series-hd/hd-series-vf', 'showMovies')
SERIE_4K = (URL_MAIN + 'series-hd/hd-x265-hevc/', 'showMovies')
SERIE_MULTI = (URL_MAIN + 'series-hd/hd-series-multi/', 'showMovies')
SERIE_SDVO = (URL_MAIN + 'series/vostfr/', 'showMovies')
SERIE_SDVF = (URL_MAIN + 'series/vf/', 'showMovies')

ANIM_ANIMS = (True, 'showMenuMangas')
ANIM_NEWS = (URL_MAIN + 'mangas/', 'showMovies')
ANIM_FILM = (URL_MAIN + 'mangas/manga-films/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'mangas/series-vostfr/', 'showMovies')
ANIM_VFS = (URL_MAIN + 'mangas/series-vf/', 'showMovies')
ANIM_MULTI = (URL_MAIN + 'mangas/series-multi/', 'showMovies')

DOC_NEWS = (URL_MAIN + 'documentaires/', 'showMovies')
SPECTACLE_NEWS = (URL_MAIN + 'theatre/', 'showMovies')


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
    oGui.addDir(SITE_IDENTIFIER, 'showMenuAutre', 'Autres', 'tv.png', oOutputParameterHandler)

    if not addon().getSetting('hoster_alldebrid_token'):
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
        oGui.addDir(SITE_IDENTIFIER, 'getToken', '[COLOR red]Les utilisateurs d\'Alldebrid cliquez ici.[/COLOR]', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Films)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS2021[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS2021[1], 'Nouveauté 2021 HD', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD1080[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD1080[1], 'Bluray 1080P', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4K[1], 'Bluray 4K', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_720[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_720[1], 'Bluray 720P', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1080X265[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1080X265[1], 'Bluray 1080P H265/HEVC', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BLURAYVOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BLURAYVOSTFR[1], 'Bluray VOSTFR', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Bluray 3D', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FULL1080P[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_FULL1080P[1], 'REMUX 1080P', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FULL4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_FULL4K[1], 'Bluray 4K', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_REMUX4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_REMUX4K[1], 'Remux 4K', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_WEBRIP4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_WEBRIP4K[1], 'Webrip 4K', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIGHT720[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIGHT720[1], 'HD light 720P', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIGHT1080[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIGHT1080[1], 'HD light 1080P', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIGHTBDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIGHTBDRIP[1], 'HD light BDRIP', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIP[1], 'Films BDRIP/DVDRIP', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_OLDDVD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_OLDDVD[1], 'Ancien DVDRIP', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FILMO[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_FILMO[1], 'Filmographie', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASSIQUE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CLASSIQUE_HD[1], 'Films Classique HD', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CLASSIQUE_SD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CLASSIQUE_SD[1], 'Films Classique SD', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Séries)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD[1], 'Séries 1080p VF', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries 1080p VOSTFR', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_720VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_720VF[1], 'Séries 720p VF', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_720VO[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_720VO[1], 'Séries 720p VOSTFR', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_4K[1], 'Séries 4K H265/HEVC', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_MULTI[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_MULTI[1], 'Séries multilangue', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_SDVF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SDVF[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_SDVO[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SDVO[1], 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Animes)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animes (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_FILM[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_FILM[1], "Film d'animation japonais (Derniers ajouts)", 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], "Animés VOSTFR (Derniers ajouts)", 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], "Animés VF (Derniers ajouts)", 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MULTI[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_MULTI[1], "Animés multilangue (Derniers ajouts)", 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuAutre():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MISC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Autres)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oOutputParameterHandler.addParameter('misc', True)
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], "Documentaire (Derniers ajouts)", 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPECTACLE_NEWS[0])
    oOutputParameterHandler.addParameter('misc', True)
    oGui.addDir(SITE_IDENTIFIER, SPECTACLE_NEWS[1], "Spectacle et théatre (Derniers ajouts)", 'buzz.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def getToken():
    oGui = cGui()

    sToken = oGui.showKeyBoard(heading="Entrez votre token alldebrid")
    cPremiumHandler('alldebrid').setToken(sToken)
    dialog().VSinfo('Token ajouté', "Extreme-Download", 5)
    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrl += sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts Martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie Dramatique', 'comedie-dramatique'], ['Comédie Musicale', 'comedie-musicale'],
             ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Epouvante Horreur', 'epouvante-horreur'],
             ['Erotique', 'erotique'], ['Espionnage', 'espionnage'], ['Famille', 'famille'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Historique', 'historique'], ['Musical', 'musical'],
             ['Policier', 'policier'], ['Péplum', 'peplum'], ['Romance', 'romance'],
             ['Science Fiction', 'science-fiction'], ['Spectacle', 'spectacle'], ['Thriller', 'thriller'],
             ['Western', 'western'], ['Divers', 'divers']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1913, 2021)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieYears():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1936, 2021)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    nextPageSearch = oInputParameterHandler.getValue('nextPageSearch')
    siteUrl = oInputParameterHandler.getValue('siteUrl')
    sMisc = oInputParameterHandler.getValue('misc')  # Autre contenu

    if nextPageSearch:
        sSearch = siteUrl

    sCat = None
    if sSearch:
        siteUrl = sSearch

        if nextPageSearch:
            sSearch += '&search_start=' + nextPageSearch
        oRequestHandler = cRequestHandler(siteUrl)
        sHtmlContent = oRequestHandler.request()

        sHtmlContent = oParser.abParse(sHtmlContent, 'de la recherche', 'À propos')

        sCat = int(re.search('speedsearch=(\d)', sSearch).group(1))
        sSearch = re.search('story=(.+?)($|&)', sSearch).group(1)
        oUtil = cUtil()
        sSearch = oUtil.CleanName(sSearch)
    else:
        oRequestHandler = cRequestHandler(siteUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = 'class="top-last thumbnails" href="([^"]+)".+?"img-post" src="([^"]+).+?alt="([^"]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    titles = set()

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)
    else:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # on enleve les softwares
            if 'PC' in aEntry[2]:  # for the search
                continue

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            if ' - ' in aEntry[2]:
                sTitle = aEntry[2].split(' - ')[0]
                sQual = aEntry[2].split(' - ')[1]
                sQual = sQual.replace('Avec TRUEFRENCH', '').replace('TRUEFRENCH', '').replace('FRENCH ', '')

                if 'Saison' in sQual:  # Pour les séries et animes
                    # * et non pas + car parfois "Saison integrale" pas de chiffre
                    saison = re.search('(Saison [0-9]*)', sQual).group(1)
                    sTitle = sTitle + ' ' + saison
                    sQual = re.sub('Saison [0-9]+ ', '', sQual)

                if '(E' in aEntry[2]:
                    res = re.search('\(E([0-9]+ .+? [0-9]+)\)', aEntry[2])
                    try:
                        sTitle = sTitle + ' E' + res.group(1).replace('Ã', ' - ').replace('à', ' - ').split('[')[0]
                    except:
                        pass

            else:
                sTitle = aEntry[2]  # .replace('Avec TRUEFRENCH', '').replace('TRUEFRENCH', '').replace('FRENCH ', '')
                sQual = ''

            # Enlever les films en doublons (même titre et même pochette)
            # il s'agit du même film dans une autre qualité qu'on retrouvera au moment du choix de la qualité
            key = sTitle + "-" + sThumb
            if key in titles:
                continue
            titles.add(key)

            if sSearch and total > 5:
                if not oUtil.CheckOccurence(sSearch, sTitle):
                    continue

            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if sCat == 3 or sMisc:
                oGui.addMisc(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            elif sCat == 1 or '/films' in siteUrl or '/manga-films/' in siteUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            elif sCat == 4 or '/mangas/' in siteUrl:
                oGui.addAnime(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        if sSearch:
            sPattern = 'name="nextlink" id="nextlink" onclick="javascript:list_submit\(([0-9]+)\); return\(false\)" href="#">Suivant'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0] is True:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('misc', sMisc)
                oOutputParameterHandler.addParameter('nextPageSearch', aResult[1][0])
                sNumPage = re.search('([0-9]+)', aResult[1][0]).group(1)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sNumPage, oOutputParameterHandler)

        else:
            sNextPage = __checkForNextPage(sHtmlContent)
            if sNextPage != False:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oOutputParameterHandler.addParameter('misc', sMisc)
                sNumPage = re.search('/page/([0-9]+)', sNextPage).group(1)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sNumPage, oOutputParameterHandler)

    if nextPageSearch:
        oGui.setEndOfDirectory()

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a href="([^"]+)">Suivant &.+?</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        return aResult[1][0]

    return False


def showMoviesLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    sDesc = ''
    try:
        sPattern = '<blockquote.+?>([^<]+)<'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = cUtil().removeHtmlTags(aResult[1][0])
    except:
        pass

    sPattern = '(<title>Télécharger |<title>)([^"]+) - ([^"]+)</title>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sQual = ''
    if aResult[1]:
        sMovieTitle = aResult[1][0][1]
        sQual = aResult[1][0][2].replace('"', '')

    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    sDisplayTitle = ('%s (%s)') % (sMovieTitle, sQual)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oOutputParameterHandler.addParameter('sDesc', sDesc)
    oGui.addLink(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    # on regarde si dispo dans d'autres qualités
    sPattern = '<a class="btn-other" href="([^<]+)">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sQual = aEntry[1]
            sTitle = ('%s [%s]') % (sMovieTitle, sQual)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sDisplayTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addLink(SITE_IDENTIFIER, 'showLinks', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    sDesc = ''
    try:
        sPattern = '<blockquote.+?>([^<]+)<'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = cUtil().removeHtmlTags(aResult[1][0])

    except:
        pass

    sPattern = '(<title>Télécharger |<title>)([^"]+) - ([^"]+)(VOSTFR|VF)*.+?</title>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    # VSlog(aResult)
    if aResult[1]:
        sMovieTitle = aResult[1][0][1]

    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    sPattern = '<meta property="og:title" content=".+? - (.+?)(VOSTFR|VF)*/>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    # VSlog(aResult)

    sQual = ''
    sTitle = sMovieTitle 
    if aResult[0]:
        sQual = aResult[1][0][0].replace('"', '')
        if 'Saison' in sQual:  # N° de saison dans la qualite
            # * et non pas + car parfois "Saison integrale" pas de chiffre
            saison = re.search('(Saison [0-9]*)', sQual).group(1)
            sQual = re.sub('Saison [0-9]+ ', '', sQual)
            sTitle = sMovieTitle + ' ' + saison

    sDisplayTitle = ('%s (%s)') % (sTitle, sQual)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oOutputParameterHandler.addParameter('sDesc', sDesc)
    oGui.addSeason(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    sHtmlContent1 = cutQual(sHtmlContent)
    sPattern1 = '<a class="btn-other" href="([^"]+)">([^<]+)</a>'

    aResult1 = oParser.parse(sHtmlContent1, sPattern1)

    if aResult1[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult1[1]:
            sUrl = aEntry[0]
            sQual = aEntry[1]
            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addSeason(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    sHtmlContent2 = cutSais(sHtmlContent)
    sPattern2 = '<a class="btn-other" href="([^"]+)">([^<]+)<'

    aResult2 = oParser.parse(sHtmlContent2, sPattern2)

    if aResult2[0] is True:
        oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Autres saisons disponibles :[/COLOR]')

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult2[1]:

            sUrl = aEntry[0]
            sTitle = sMovieTitle + ' ' + aEntry[1].replace('Saison ', 'S')

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addSeason(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Detection de la taille des fichier pour separer les fichier premium des parties en .rar
    if 'saison' not in sUrl:
        fileSize = re.findall('<strong>Taille</strong><span style="float: right;">([^<]+)</span></td>', sHtmlContent)
        if 'et' in str(fileSize[0]):
            taille = str(fileSize[:-7])
        else:
            taille = str(fileSize[0])

        if ' Go' in taille:
            size, unite = taille.split(' ')
            if float(size) > 4.85:
                if "1 Lien" in sHtmlContent:
                    VSlog('1 Lien premium')
                    sPattern = '<h2 style="text-align: center;"><span style=.+?>([^<]+)<span style=".+?</h2>|<div class="prez_2">1 Lien Uptobox</div>\s*.+?>\s*.+?<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<]+)*</strong>.+?\s*<div class="showNFO"'
                else:
                    VSlog('Pas lien premium')
                    sPattern = '<h2 style="text-align: center;"><span style=.+?>([^<]+)<span style=".+?</h2>|<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<]+)* Premi*um</strong>'
            else:
                sPattern = '<h2 style="text-align: center;"><span style=.+?>([^<]+)<span style=".+?</h2>|<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<]+)*</strong>'
        else:
            sPattern = '<h2 style="text-align: center;"><span style=.+?>([^<]+)<span style=".+?</h2>|<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<]+)*</strong>'
    else:
        sPattern = '<div class="prez_7">([^<]+)</div>|<a title=".+?" href="([^"]+)" target="_blank"><strong class="hebergeur">([^<]+)</strong>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    # Il n'existe que des fichiers en parties, non fonctionnel
    if (aResult[0] is False) and float(size) > 4.85:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        if 'saison' in sUrl:
            aResult[1].insert(0, ('Episode 1', '', ''))

        ep = ""
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                ep = aEntry[0]
            else:
                sUrl2 = aEntry[1]

                if 'saison' in sUrl:
                    sTitle = sMovieTitle + ' ' + ep
                else:
                    sTitle = sMovieTitle

                if 'saison' in sUrl:
                    sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sTitle, aEntry[2])
                else:
                    sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, str(aEntry[2]))

                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                if 'saison' in sUrl:
                    oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
                else:
                    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    Token_Alldebrid = addon().getSetting('hoster_alldebrid_token')
    if Token_Alldebrid != "":
        sUrl_Bypass = "https://api.alldebrid.com/v4/link/redirector?agent=service&version=1.0-&apikey="
        sUrl_Bypass += Token_Alldebrid + "&link=" + sUrl

        oRequestHandler = cRequestHandler(sUrl_Bypass)
        sHtmlContent = json.loads(oRequestHandler.request())

        HostURL = sHtmlContent["data"]["links"]
        for sHosterUrl in HostURL:

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:
        from resources.lib import librecaptcha
        test = librecaptcha.get_token(api_key="6LeH9lwUAAAAAGgg9ZVf7yOm0zb0LlcSai8t8-2o", site_url=sUrl, user_agent=UA,
                                      gui=False, debug=False)

        if test is None:
            oGui.addText(SITE_IDENTIFIER, '[COLOR red]Resolution du Recaptcha annulé[/COLOR]')

        else:
            # N'affiche pas directement le liens car sinon Kodi crash.
            sDisplayTitle = "Recaptcha passé avec succès, cliquez pour afficher les liens"
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('Token', test)
            oGui.addLink(SITE_IDENTIFIER, 'getHost', sDisplayTitle, sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def getHost():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    test = oInputParameterHandler.getValue('Token')

    data = 'g-recaptcha-response=' + test + '&submit_captcha=1'
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip')
    oRequestHandler.addHeaderEntry('Referer', sUrl)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Content-Length', len(str(data)))
    oRequestHandler.addParametersLine(data)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div><span class="lien"><a target="_blank" href="(.+?)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:

        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()


def cutQual(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="other-qualities">&Eacute;galement disponible en :</span>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    return ''


def cutSais(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="other-qualities">Autres saisons :</span>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    return ''
