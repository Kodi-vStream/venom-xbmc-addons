# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import unicodedata

from resources.lib.comaddon import progress, dialog, siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
# Fonction de vStream qui remplace urllib.quote, pour simplifier le passage en python 3
from resources.lib.util import Quote, cUtil

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}

SITE_IDENTIFIER = 'zone_telechargement_ws'
SITE_NAME = '[COLOR violet]Zone-Telechargement[/COLOR]'
SITE_DESC = 'Fichier en DDL, HD'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH = (URL_MAIN + 'engine/ajax/controller.php?mod=filter&q=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'engine/ajax/controller.php?mod=filter&q=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'engine/ajax/controller.php?mod=filter&q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'top-films/', 'showMovies')  # films (derniers ajouts)
MOVIE_EXCLUS = (URL_MAIN + 'nouveaux-films/', 'showMovies')  # exclus (films populaires)
MOVIE_3D = (URL_MAIN + 'film-bluray-3d/', 'showMovies')  # films en 3D
MOVIE_HD = (URL_MAIN + 'film-bluray-hd/', 'showMovies')  # films en HD
MOVIE_HDLIGHT = (URL_MAIN + 'film-x265-x264-hdlight/', 'showMovies')  # films en x265 et x264
MOVIE_VOSTFR = (URL_MAIN + 'filmsenvostfr/', 'showMovies')  # films VOSTFR
MOVIE_4K = (URL_MAIN + 'films-ultra-hd-4k/', 'showMovies')  # films "4k"
MOVIE_GENRES = (URL_MAIN + 'engine/ajax/controller.php?mod=filter&catid=0&q=&genre%5B%5D={}&note=0&art=0&AiffchageMode=0&inputTirePar=0&cstart=1', 'showGenre')
MOVIE_ANIME = (URL_MAIN + 'dessins-animes/', 'showMovies')  # dessins animes
MOVIE_BDRIP = (URL_MAIN + 'film-dvdrip-bdrip/', 'showMovies')
MOVIE_TS_CAM = (URL_MAIN + 'tscam-films-2020/', 'showMovies')
MOVIE_VFSTFR = (URL_MAIN + 'film-vfstfr/', 'showMovies')
MOVIE_MKV = (URL_MAIN + 'film-mkv/', 'showMovies')
MOVIE_VO = (URL_MAIN + 'films-vo/', 'showMovies')
MOVIE_INTEGRAL = (URL_MAIN + 'collections-films-integrale/', 'showMovies')

SERIE_SERIES = ('http://', 'showMenuTvShows')
SERIE_VFS = (URL_MAIN + 'serie-vf/', 'showMovies')
SERIE_VF_720 = (URL_MAIN + 'serie-vf-en-hd/', 'showMovies')
SERIE_VF_1080 = (URL_MAIN + 'serie-vf-1080p/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'serie-vostfr/', 'showMovies')
SERIE_VOSTFRS_720 = (URL_MAIN + 'serie-vostfr-hd/', 'showMovies')
SERIE_VOSTFRS_1080 = (URL_MAIN + 'serie-vostfr-1080p/', 'showMovies')
SERIE_VO = (URL_MAIN + 'serie-vo/', 'showMovies')
ANCIENNE_SERIE = (URL_MAIN + 'telecharger-serie/ancienne-serie/', 'showMovies')

ANIM_ANIMS = ('http://', 'showMenuMangas')
ANIM_VFS = (URL_MAIN + 'animes-vf/', 'showMovies')
ANIM_VF_720 = (URL_MAIN + 'animes-vf-720p/', 'showMovies')
ANIM_VF_1080 = (URL_MAIN + 'animes-vf-1080p/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'animes-vostfr/', 'showMovies')
ANIM_VOSTFRS_720 = (URL_MAIN + 'animes-vostfr-720p/', 'showMovies')
ANIM_VOSTFRS_1080 = (URL_MAIN + 'animes-vostfr-1080p/', 'showMovies')
ANIM_VOSTEN = (URL_MAIN + 'animes-vosten/', 'showMovies')
FILM_ANIM = (URL_MAIN + 'films-mangas/', 'showMovies')
OAV = (URL_MAIN + 'oav/', 'showMovies')

DOC_NEWS = (URL_MAIN + 'documentaire-gratuit/', 'showMovies')  # docs
DOC_DOCS = ('http://', 'load')

SPORT_REPLAY = (URL_MAIN + 'sport/', 'showMovies')  # sports
SPORT_SPORTS = SPORT_REPLAY
TV_NEWS = (URL_MAIN + 'emissions-tv/', 'showMovies')  # dernieres emissions tv
SPECT_NEWS = (URL_MAIN + 'spectacles/', 'showMovies')  # derniers spectacles
CONCERT_NEWS = (URL_MAIN + 'concert/', 'showMovies')  # derniers concerts
AUTOFORM_VID = (URL_MAIN + 'autoformations-videos/', 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuAutres', 'Autres', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuFilms():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EXCLUS[1], 'Exclus (Films populaires)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Blu-rays (720p & 1080p)', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Films (3D)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films (x265 & x264)', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4K[1], 'Films (4k)', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANIME[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANIME[1], 'Dessins Animés (Derniers ajouts)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIP[1], 'Films (BDRIP)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TS_CAM[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TS_CAM[1], 'Films (TS, CAM, R5, DVDSCR)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VFSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VFSTFR[1], 'Films en francais sous titre francais (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MKV[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MKV[1], 'Films (dvdrip mkv)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VO[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VO[1], 'Films en Version original (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_INTEGRAL[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_INTEGRAL[1], 'Intégral de films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF_720[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries 720p (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF_1080[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries 1080p (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS_720[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS_720[1], 'Séries 720p (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS_1080[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS_1080[1], 'Séries 1080p (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VO[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VO[1], 'Séries (VO)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANCIENNE_SERIE[0])
    oGui.addDir(SITE_IDENTIFIER, ANCIENNE_SERIE[1], 'Ancienne séries (Derniers)', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animes (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VF_720[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VF_720[1], 'Animés 720p (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VF_1080[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VF_1080[1], 'Animés 1080p (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS_720[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS_720[1], 'Animés 720p (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS_1080[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS_1080[1], 'Animés 1080p (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', FILM_ANIM[0])
    oGui.addDir(SITE_IDENTIFIER, FILM_ANIM[1], 'Films d\'animés ', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTEN[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTEN[1], 'Animés (VOSTEN)', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuAutres():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', TV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, TV_NEWS[1], 'Emissions TV', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPECT_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SPECT_NEWS[1], 'Spectacles', 'star.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sSearchText = Quote(sSearchText)
        sUrl = URL_SEARCH[0] + sSearchText + '&note=0&art=0&AiffchageMode=0&inputTirePar=0&cstart=0'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    UrlGenre = oInputParameterHandler.getValue('siteUrl')

    liste = [['Action', 'Action'], ['Animation', 'Animation'], ['Arts Martiaux', 'martiaux'], ['Aventure', 'Aventure'],
             ['Biopic', 'Biopic'], ['Comédie Dramatique', 'Dramatique'], ['Comédie Musicale', 'Musical'],
             ['Comédie', 'Comedie'], ['Divers', 'Divers'], ['Documentaires', 'Documentaire'], ['Drame', 'Drame'],
             ['Epouvante Horreur', 'Epouvante'], ['Espionnage', 'Espionnage'], ['Famille', 'Famille'],
             ['Fantastique', 'Fantastique'], ['Guerre', 'Guerre'], ['Historique', 'Historique'], ['Musical', 'musicale'],
             ['Péplum', 'Peplum'], ['Policier', 'Policier'], ['Romance', 'Romance'], ['Science Fiction', 'Science'],
             ['Thriller', 'Thriller'], ['Western', 'Western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', UrlGenre.format(sUrl))
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl').replace('index.php', '')
    if sSearch:
        sUrl = sSearch

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<img class="mainimg.+?src="([^"]+).+?href="([^"]+)">([^<]+)<.+?<b>([^<]+)<.+?">([^<]+)<'

    oParser = cParser()
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

            sThumb = aEntry[0]
            sUrl2 = aEntry[1]
            sTitle = aEntry[2]
            sQual = aEntry[3]
            sLang = aEntry[4]

            # on vire le tiret des series
            sTitle = sTitle.replace(' - Saison', ' Saison').replace('COMPLETE', 'Complete')
            sMovieTitle = sTitle.split('Saison')[0]

            if '[Complete]' not in sTitle:
                sTitle = sTitle.replace('COMPLETE', '[Complete]')

            # nettoyage du titre
            sTitle = sTitle.replace('Complete', 'Complète')
            sTitle = re.sub('\[\w+]', '', sTitle)

            try:
                sTitle = str(sTitle.encode('latin-1'), encoding="utf-8")
            except:
                pass

            # Enlever les films en doublons (même titre et même pochette)
            # il s'agit du même film dans une autre qualité qu'on retrouvera au moment du choix de la qualité
            key = sTitle + "-" + sThumb
            if key in titles:
                continue
            titles.add(key)

            sDisplayTitle = ('%s [%s] %s') % (sTitle, sQual, sLang)

            if not sThumb.startswith('https'):
                sThumb = URL_MAIN + sThumb

            if not sUrl2.startswith('https'):
                sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sDisplayTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'anime' in sUrl or 'anime' in sUrl2:
                oGui.addAnime(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, '', sThumb, '', oOutputParameterHandler)
            elif 'serie' in sUrl or 'serie' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, '', sThumb, '', oOutputParameterHandler)
            elif DOC_NEWS[0] in sUrl or TV_NEWS[0] in sUrl or SPECT_NEWS[0] in sUrl or CONCERT_NEWS[0] in sUrl:
                oGui.addMisc(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, '', sThumb, '', oOutputParameterHandler)
            elif 'collection' in sUrl or 'integrale' in sUrl:
                oGui.addMoviePack(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            elif ' Saison ' in sTitle:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        if 'controller.php' in sUrl:
            sPattern = '<a href="#" class="nav" data-cstart="([^"]+)">Suivant</a></div>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', re.sub('cstart=(\d+)', 'cstart=' + str(aResult[1][0]), sUrl))
                number = re.search('([0-9]+)', aResult[1][0]).group(1)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + number, oOutputParameterHandler)

        else:
            sNextPage, sPaging = __checkForNextPage(sHtmlContent)
            if sNextPage:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>([^<]+)</a> *<a href="([^"]+)">Suivant</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        if not sNextPage.startswith('https'):
            sNextPage = URL_MAIN + sNextPage
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showMoviesLinks():
    # VSlog('mode film')
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDisplayTitle = oInputParameterHandler.getValue('sDisplayTitle')
    if not sDisplayTitle:   # Si on arrive par un marque-page
        sDisplayTitle = sMovieTitle
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if "onaregarde" in sUrl:
        oParser = cParser()
        sPattern = '<a type="submit".+?href="([^"]+)"'
        sUrl = oParser.parse(sHtmlContent, sPattern)[1][0]

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # Affichage du texte
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    # récupération du Synopsis et de l'année
    sDesc = ''
    sYear = ''
    try:
        sPattern = '(<u>Date de .+</u>.+(\d{4}(-| *<))|<u>Critiques.+?</u>).+synopsis.+?>(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            aEntry = aResult[1][0]
            sYear = aEntry[1]
            sDesc = cUtil().removeHtmlTags(aEntry[3])
    except:
        pass

    # la qualité courante est le lien en cours ici même
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oOutputParameterHandler.addParameter('sDesc', sDesc)
    oOutputParameterHandler.addParameter('sYear', sYear)
    oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    # on regarde si dispo dans d'autres qualités
    sPattern = '<a href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)</b></span><span style="color:#.{6}"><b>([^<]+)</b></span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = URL_MAIN[:-1] + aEntry[0]
            sQual = aEntry[1]
            sLang = aEntry[2]
            sTitle = ('%s [%s] %s') % (sMovieTitle, sQual, sLang)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sDisplayTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addLink(SITE_IDENTIFIER, 'showMoviesLinks', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesLinks():
    # VSlog('mode serie')
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if "onaregarde" in sUrl:
        oParser = cParser()
        sPattern = '<a type="submit".+?href="([^"]+)"'
        sUrl = oParser.parse(sHtmlContent, sPattern)[1][0]

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # Affichage du texte
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    # récupération du Synopsis
    sDesc = sMovieTitle   # Ne pas laisser vide sinon un texte automatique faux va être calculé
    try:
        sPattern = 'synopsis.+(alt="">|<!--dle_image_end-->)(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = cUtil().removeHtmlTags(aResult[1][0][1])
    except:
        pass

    # on recherche d'abord la qualité courante
    sPattern = 'smallsep.+?Qualité([^<]+)<.+?img src="([^"]+)".+?alt=.+?- Saison ([0-9]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    # sQual = ''
    # sLang = ''
    if aResult[1] is True:
        aEntry = aResult[1][0]
        sQual = aEntry[0].split('|')[0]
        sLang = aEntry[0].split('|')[1]
        sThumb = aEntry[1]  # change pour chaque saison, il faut la rechercher si on navigue entre saisons
        sTitle = sMovieTitle + ' S' + aEntry[2]

        sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oGui.addSeason(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    # on regarde si dispo dans d'autres qualités
    sHtmlContent1 = CutQual(sHtmlContent)
    sPattern1 = 'href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)</b></span><span style="color:#.{6}"><b>([^<]+)'
    aResult1 = oParser.parse(sHtmlContent1, sPattern1)

    if aResult1[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult1[1]:
            if 'animes' in sUrl:
                sUrl = URL_MAIN + 'animes' + aEntry[0]
            else:
                sUrl = URL_MAIN + 'telecharger-serie' + aEntry[0]
            sQual = aEntry[1]
            sLang = aEntry[2]
            sDisplayTitle = ('%s [%s] %s') % (sTitle, sQual, sLang)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addSeason(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    # on regarde si dispo d'autres saisons
    # Une ligne par saison, pas besoin d'afficher les qualités ici
    saisons = []
    sHtmlContent2 = CutSais(sHtmlContent)
    sPattern2 = 'href="([^"]+)"><span class="otherquality">([^<]+)<b>([^<]+)<span style="color:#.{6}">([^<]+)</span><span style="color:#.{6}">([^<]+)'
    aResult2 = oParser.parse(sHtmlContent2, sPattern2)

    # Affichage du texte
    if aResult2[0] is True:
        oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Autres saisons disponibles :[/COLOR]')
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult2[1]:
            sSaison = aEntry[2].strip()
            if sSaison in saisons:
                continue
            saisons.append(sSaison)

            if 'animes' in sUrl:
                sUrl = URL_MAIN + 'animes' + aEntry[0]
            else:
                sUrl = URL_MAIN + 'telecharger-serie' + aEntry[0]

            sTitle = sMovieTitle + ' ' + aEntry[1] + aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oGui.addSeason(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, 'series.png', sThumb, sMovieTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    # VSlog('showHosters')
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if "zt-protect" in sUrl:
        # Dl Protect present aussi a cette étape.
        sHtmlContent = DecryptDlProtecte(sUrl)
    else:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # Si ça ressemble aux liens premiums on vire les liens non premium
    if 'Premium' in sHtmlContent or 'PREMIUM' in sHtmlContent:
        sHtmlContent = CutNonPremiumlinks(sHtmlContent)

    oParser = cParser()

    sPattern = '<div style="font-weight:bold;color:.+?</span>(.+?)</div>|<a class="btnToLink".+?href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                if 'Interchangeables' not in aEntry[0]:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            else:
                sDisplayTitle = sMovieTitle

                oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
                oOutputParameterHandler.addParameter('baseUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sYear', sYear)
                oGui.addLink(SITE_IDENTIFIER, 'Display_protected_link', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesHosters():
    # VSlog('showSeriesHosters')
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    try:
        sDesc = unicodedata.normalize('NFD', sDesc).encode('ascii', 'ignore').decode('unicode_escape')
        sDesc = sDesc.encode('latin-1')
    except:
        pass

    if "zt-protect" in sUrl:
        # Dl Protect present aussi a cette étape.
        sHtmlContent = DecryptDlProtecte(sUrl)
    else:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # Pour les series on fait l'inverse des films on vire les liens premiums
    if 'Premium' in sHtmlContent or 'PREMIUM' in sHtmlContent or 'premium' in sHtmlContent:
        sHtmlContent = CutPremiumlinks(sHtmlContent)

    sPattern = '<div style="font-weight.+?>([^<]+)</div>|<a class="btnToLink".+?href="([^"]+)".+?Episode ([0-9]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                if 'Télécharger' in aEntry[0]:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]' + aEntry[0] + '[/COLOR]')
                else:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            else:
                sName = 'E' + aEntry[2]
                sName = sName.replace('Télécharger', '')
                sUrl2 = aEntry[1]
                sTitle = sMovieTitle + ' ' + sName

                oOutputParameterHandler.addParameter('baseUrl', sUrl)
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def Display_protected_link():
    # VSlog('Display_protected_link')
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    # baseUrl = oInputParameterHandler.getValue('baseUrl')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    # Est-ce un lien dl-protect ?
    if sUrl:

        sHtmlContent = DecryptDlProtecte(sUrl)

        if sHtmlContent:
            # Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotecte = (True, [sHtmlContent])
            else:
                sPattern_dlprotecte = 'class="alert alert-primary".+?href="(.+?)"'
                aResult_dlprotecte = oParser.parse(sHtmlContent, sPattern_dlprotecte)

        else:
            dialog().VSok('Erreur décryptage du lien')
            aResult_dlprotecte = (False, False)

    # Si lien normal
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotecte = (True, [sUrl])

    if aResult_dlprotecte[0]:

        episode = 1

        for aEntry in aResult_dlprotecte[1]:
            sHosterUrl = aEntry

            sTitle = sMovieTitle
            if len(aResult_dlprotecte[1]) > 1:
                sTitle = sMovieTitle + ' episode ' + episode

            episode += 1

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def CutQual(sHtmlContent):
    oParser = cParser()
    sPattern = '<h3>Qualit.+?galement disponibles pour cette saison:</h3>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    else:
        return sHtmlContent

    return ''


def CutSais(sHtmlContent):
    oParser = cParser()
    sPattern = '<h3>Saisons.+?galement disponibles.+?</h3>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    return ''


def CutNonPremiumlinks(sHtmlContent):
    oParser = cParser()
    sPattern = '(?:Lien.+?Premium - 1 lien|Lien.+?Premium)(.+?)</b></font></a></center>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    # Si ça ne marche pas on renvoie le code complet
    return sHtmlContent


def CutPremiumlinks(sHtmlContent):
    oParser = cParser()
    sPattern = '(?i) par .{1,2}pisode(.+?)$'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sHtmlContent = aResult[1][0]

    # Si ça ne marche pas on renvoie le code complet
    return sHtmlContent


def DecryptDlProtecte(url):

    if not url:
        return ''

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.setRequestType(1)
    sHtmlContent = oRequestHandler.request()

    return str(sHtmlContent)
