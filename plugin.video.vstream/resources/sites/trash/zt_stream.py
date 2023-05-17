# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
from resources.lib.util import Quote, cUtil
return false

import re

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
headers = {'User-Agent': UA}

SITE_IDENTIFIER = 'zt_stream'
SITE_NAME = '[COLOR violet]ZT-Stream[/COLOR]'
SITE_DESC = 'Zone Telechargement en Streaming'

URL_MAIN = 'https://www.zone-telechargement.stream/'

URL_SEARCH = (URL_MAIN + 'engine/ajax/controller.php?mod=filter&q=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'engine/ajax/controller.php?mod=filter&catid=0&categorie%5B%5D=2&q=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'engine/ajax/controller.php?mod=filter&catid=0&categorie%5B%5D=15&q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'top-films/', 'showMovies')  # films (derniers ajouts)
MOVIE_EXCLUS = (URL_MAIN + 'nouveaux-films/', 'showMovies')  # exclus (films populaires)
MOVIE_3D = (URL_MAIN + 'film-bluray-3d/', 'showMovies')  # films en 3D
MOVIE_HD = (URL_MAIN + 'film-bluray-hd/', 'showMovies')  # films en HD
MOVIE_HDLIGHT = (URL_MAIN + 'film-x265-x264-hdlight/', 'showMovies')  # films en x265 et x264
MOVIE_VOSTFR = (URL_MAIN + 'filmsenvostfr/', 'showMovies')  # films VOSTFR
MOVIE_4K = (URL_MAIN + 'films-ultra-hd-4k/', 'showMovies')  # films "4k"
MOVIE_GENRES = (URL_MAIN + 'engine/ajax/controller.php?mod=filter&catid=0&q=&genre%5B%5D={}&note=0&categorie%5B%5D=2&art=0&AiffchageMode=0&inputTirePar=0&cstart=1', 'showGenre')
MOVIE_ANIME = (URL_MAIN + 'dessins-animes/', 'showMovies')  # dessins animes
MOVIE_BDRIP = (URL_MAIN + 'film-dvdrip-bdrip/', 'showMovies')
MOVIE_TS_CAM = (URL_MAIN + 'tscam-films-2020/', 'showMovies')
MOVIE_VFSTFR = (URL_MAIN + 'film-vfstfr/', 'showMovies')
MOVIE_MKV = (URL_MAIN + 'film-mkv/', 'showMovies')
MOVIE_VO = (URL_MAIN + 'films-vo/', 'showMovies')
MOVIE_INTEGRAL = (URL_MAIN + 'collections-films-integrale/', 'showMovies')

SERIE_SERIES = ('http://', 'showMenuSeries')
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

SPORT_SPORTS = (URL_MAIN + 'sport/', 'showMovies')  # sports
TV_NEWS = (URL_MAIN + 'emissions-tv/', 'showMovies')  # dernieres emissions tv
SPECT_NEWS = (URL_MAIN + 'spectacles/', 'showMovies')  # derniers spectacles
CONCERT_NEWS = (URL_MAIN + 'concert/', 'showMovies')  # derniers concerts
AUTOFORM_VID = (URL_MAIN + 'autoformations-videos/', 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)

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


def showMenuFilms():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EXCLUS[1], 'Exclus (Films populaires)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Blu-rays (720p & 1080p)', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Films (3D)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films (x265 & x264)', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4K[1], 'Films (4k)', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANIME[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANIME[1], 'Dessins Animés (Derniers ajouts)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIP[1], 'Films (BDRIP)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TS_CAM[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TS_CAM[1], 'Films (TS , CAM, R5 ,DVDSCR)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VFSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VFSTFR[1], 'Films en Francais sous titre Francais (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MKV[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MKV[1], 'Films (dvdrip mkv)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VO[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VO[1], 'Films en Version original (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    # Un seul film est proposé dans les coffrets
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_INTEGRAL[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_INTEGRAL[1], 'Integral de films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF_720[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries 720p (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF_1080[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries 1080p (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS_720[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS_720[1], 'Séries 720p (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS_1080[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS_1080[1], 'Séries 1080p (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VO[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VO[1], 'Séries (VO)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANCIENNE_SERIE[0])
    oGui.addDir(SITE_IDENTIFIER, ANCIENNE_SERIE[1], 'Ancienne series (Derniers)', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animes (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VF_720[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VF_720[1], 'Animes 720p (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VF_1080[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VF_1080[1], 'Animes 1080p (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animes (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS_720[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS_720[1], 'Animes 720p (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS_1080[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS_1080[1], 'Animes 1080p (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', FILM_ANIM[0])
    oGui.addDir(SITE_IDENTIFIER, FILM_ANIM[1], 'Films d\'animes ', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTEN[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTEN[1], 'Animes (VOSTEN)', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuAutres():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', TV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, TV_NEWS[1], 'Emissions TV', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPECT_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SPECT_NEWS[1], 'Spectacles', 'star.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sUrl = sUrl + Quote(sSearchText)
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    UrlGenre = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append(['Action', 'Action'])
    liste.append(['Animation', 'Animation'])
    liste.append(['Arts Martiaux', 'martiaux'])
    liste.append(['Aventure',  'Aventure'])
    liste.append(['Biopic',  'Biopic'])
    liste.append(['Comédie Dramatique',  'Dramatique'])
    liste.append(['Comédie Musicale',  'Musical'])
    liste.append(['Comédie',  'Comedie'])
    liste.append(['Divers',  'Divers'])
    liste.append(['Documentaires', 'Documentaire'])
    liste.append(['Drame', 'Drame'])
    liste.append(['Epouvante Horreur', 'Epouvante'])
    liste.append(['Espionnage', 'Espionnage'])
    liste.append(['Famille', 'Famille'])
    liste.append(['Fantastique', 'Fantastique'])
    liste.append(['Guerre', 'Guerre'])
    liste.append(['Historique', 'Historique'])
    liste.append(['Musical', 'musicale'])
    liste.append(['Péplum', 'Peplum'])
    liste.append(['Policier', 'Policier'])
    liste.append(['Romance', 'Romance'])
    liste.append(['Science Fiction', 'Science'])
    liste.append(['Thriller', 'Thriller'])
    liste.append(['Western', 'Western'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', UrlGenre.format(sUrl))
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl.replace('https', 'http'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="mainimg.+?src="([^"]+).+?href="([^"]+)">([^<]+).+?class=.+?<b>([^<]+)</span.+?">([^<]+)</span'

    aResult = oParser.parse(sHtmlContent, sPattern)

    titles = set()  # filtrer les titres similaires

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[2]
            sUrl2 = aEntry[1]
            sThumb = aEntry[0]
            sQual = aEntry[3]
            sLang = aEntry[4]

            # on vire le tiret des series
            sTitle = sTitle.replace(' - Saison', ' Saison').replace('COMPLETE', 'Complete')
            if not '[Complete]' in sTitle:
                sTitle = sTitle.replace('COMPLETE', '[Complete]')

            # nettoyage du titre
            sDisplayTitle = sTitle.replace('Complete', 'Complète')
            sTitle = re.sub('\[\w+]', '', sTitle)

            # Enlever les films en doublons (même titre et même pochette)
            # il s'agit du même film dans une autre qualité qu'on retrouvera au moment du choix de la qualité
            key = sTitle + "-" + sThumb
            if key in titles:
                continue
            titles.add(key)

            sDisplayTitle = ('%s [%s] %s') % (sTitle, sQual, sLang)

            if not sThumb.startswith('https'):
                sThumb = URL_MAIN[:-1] + sThumb

            if not sUrl2.startswith('https'):
                sUrl2 = URL_MAIN[:-1] + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDisplayTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'anime' in sUrl or 'anime' in sUrl2:
                oGui.addAnime(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, '', sThumb, '', oOutputParameterHandler)
            elif 'serie' in sUrl or 'serie' in sUrl2 or '-saison-' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, '', sThumb, '', oOutputParameterHandler)
            elif 'collection' in sUrl or 'integrale' in sUrl:
                oGui.addMoviePack(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        if sSearch:  # une seule page de résultats
            return

        if 'controller.php' in sUrl:  # par genre
            sPattern = '<a href="#" class="nav" data-cstart="([^"]+)">Suivant</a></div>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', re.sub('cstart=(\d+)', 'cstart=' + str(aResult[1][0]), sUrl))
                number = re.search('([0-9]+)', aResult[1][0]).group(1)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + number + ' >>>[/COLOR]', oOutputParameterHandler)

        else:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                number = re.search('/page/([0-9]+)', sNextPage).group(1)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + number + ' >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'href="([^"]+)">Suivant</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        nextPage = aResult[1][0]
        if not nextPage.startswith('https'):
            nextPage = URL_MAIN[:-1] + nextPage
        return nextPage
    return False


def showMoviesLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDisplayTitle = oInputParameterHandler.getValue('sDisplayTitle')
    if not sDisplayTitle:  # Si on arrive par un marque-page
        sDisplayTitle = sMovieTitle
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl.replace('https', 'http'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    # Affichage du texte
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    # Récupération du Synopsis et de l'année
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

    # la qualité courante est le lien en cours ici-même
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oOutputParameterHandler.addParameter('sDesc', sDesc)
    oOutputParameterHandler.addParameter('sYear', sYear)
    oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    # On regarde si dispo dans d'autres qualités
    sPattern = 'href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)</b></span><span style="color:#.{6}"><b>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = URL_MAIN[:-1] + aEntry[0]
            sQual = aEntry[1]
            sLang = aEntry[2]
            sTitle = ('%s [%s] %s') % (sMovieTitle, sQual, sLang)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sDisplayTitle', sTitle)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl.replace('https', 'http'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    # Affichage du texte
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles :[/COLOR]')

    # Récupération du Synopsis
    sDesc = sMovieTitle   # Ne pas laisser vide sinon un texte faux venant du cache va etre utilisé
    try:
        sPattern = 'synopsis.+(alt="">|<!--dle_image_end-->)(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = cUtil().removeHtmlTags(aResult[1][0][1])
    except:
        pass

    # On recherche d'abord la qualité courante
    sPattern = '<div style="[^"]+?">.+?Qualité (.+?) [|] (.+?)<.+?img src="(([^"]+))"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sQual = ''
    sLang = ''
    if (aResult[1]):
        aEntry = aResult[1][0]
        sQual = aEntry[0]
        sLang = aEntry[1]
        sThumb = aEntry[2]  # Change pour chaque saison, il faut la rechercher si on navigue entre saisons
    sDisplayTitle = ('%s [%s] (%s)') % (sMovieTitle, sQual, sLang)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oOutputParameterHandler.addParameter('sDesc', sDesc)
    oGui.addTV(SITE_IDENTIFIER, 'showSerieEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    # On regarde si dispo dans d'autres qualités
    sHtmlContent1 = CutQual(sHtmlContent)
    sPattern1 = 'href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)</b></span><span style="color:#.{6}"><b>([^<]+)'
    aResult1 = oParser.parse(sHtmlContent1, sPattern1)

    if (aResult1[0] == True):
        for aEntry in aResult1[1]:

            if 'animes' in sUrl:
                sUrl = URL_MAIN + 'animes' + aEntry[0]
            else:
                sUrl = URL_MAIN + 'telecharger-serie' + aEntry[0]
            sQual = aEntry[1]
            sLang = aEntry[2]
            sDisplayTitle = ('%s [%s] %s') % (sMovieTitle, sQual, sLang)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addTV(SITE_IDENTIFIER, 'showSerieEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    # On regarde si dispo d'autres saisons
    # Une ligne par saison, pas besoin d'afficher les qualités ici
    saisons = []
    sHtmlContent2 = CutSais(sHtmlContent)
    sPattern2 = 'href="([^"]+)"><span class="otherquality">([^<]+)<b>([^<]+)<span style="color:#.{6}">([^<]+)</span><span style="color:#.{6}">([^<]+)'
    aResult2 = oParser.parse(sHtmlContent2, sPattern2)

    # Affichage du texte
    if (aResult2[0] == True):
        oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Autres saisons disponibles :[/COLOR]')

        for aEntry in aResult2[1]:

            sSaison = aEntry[2].strip()
            if sSaison in saisons:
                continue
            saisons.append(sSaison)

            if 'animes' in sUrl:
                sUrl = URL_MAIN + 'animes' + aEntry[0]
            else:
                sUrl = URL_MAIN + 'telecharger-serie' + aEntry[0]
            sMovieTitle = aEntry[1] + aEntry[2]
            sTitle = '[COLOR skyblue]' + sMovieTitle + '[/COLOR]'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, 'series.png', sThumb, sMovieTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl.replace('https', 'http'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    # '>Regarder' à la fin permet de ne pas prendre les liens en plusieurs parties
    sPattern = 'class="btnToLink" target="_blank" href="([^"]+)">Regarder'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sUrl = aResult[1][0]  # Un seul lien, on va directement chercher le hoster
        sHosterUrl = get_protected_link(sUrl)
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showSerieEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl.replace('https', 'http'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'class="btnToLink" target="_blank" href="([^"]+)">Episode (.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            numEpisode = aEntry[1]

            sDisplayTitle = 'Episode %s - %s' % (numEpisode, sMovieTitle)
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sDisplayTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sMovieTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sDisplayTitle = oInputParameterHandler.getValue('sDisplayTitle')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sHosterUrl = get_protected_link(sUrl)
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster):
        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()


def get_protected_link(sUrl):
    if not sUrl:
        return ''

    oParser = cParser()

    sHtmlContent = DecryptDlProtecte(sUrl)
    if sHtmlContent:

        # Si redirection
        if sHtmlContent.startswith('http'):
            return sHtmlContent

        sPattern_dlprotecte = '<iframe.+?src="([^"]+)"'
        aResult_dlprotecte = oParser.parse(sHtmlContent, sPattern_dlprotecte)
        if aResult_dlprotecte[0]:
            return aResult_dlprotecte[1][0]


def CutQual(sHtmlContent):
    oParser = cParser()
    sPattern = '<h3>Qualit.+?galement disponibles pour cette saison:</h3>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        return aResult[1][0]
    else:
        return sHtmlContent

    return ''


def CutSais(sHtmlContent):
    oParser = cParser()
    sPattern = '<h3>Saisons.+?galement disponibles pour cette saison:</h3>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        return aResult[1][0]
    return ''


def DecryptDlProtecte(url):

    if not (url):
        return ''

    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'form action="([^"]+).+?type="hidden" name="_token" value="([^"]+).+?input type="hidden" value="([^"]+)'
    result = oParser.parse(sHtmlContent, sPattern)

    if (result[0]):
        restUrl = str(result[1][0][0])
        token = str(result[1][0][1])
        # urlData = str(result[1][0][2])

    else:
        sPattern = '<(.+?)action="([^"]+)" method="([^"]+).+?hidden".+?value="([^"]+)'
        result = oParser.parse(sHtmlContent, sPattern)

        if (result[0]):
            if not "<!-----" in (str(result[1][0][0])):
                restUrl = str(result[1][0][0])
                method = str(result[1][0][1])
                token = str(result[1][0][2])
            else:
                restUrl = str(result[1][1][1]).replace("}", '%7D')
                method = str(result[1][1][2])
                token = str(result[1][1][3])

            if restUrl.startswith('/'):
                restUrl = 'https://' + url.split('/')[2] + restUrl

    oRequestHandler = cRequestHandler(restUrl)
    if method == "post":
        oRequestHandler.setRequestType(1)
    oRequestHandler.addParameters("_token", token)
    sHtmlContent = oRequestHandler.request()

    return sHtmlContent
