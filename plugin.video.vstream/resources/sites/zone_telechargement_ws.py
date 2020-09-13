# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import random
import re
import string
import unicodedata

from resources.lib.comaddon import progress, dialog, VSlog, addon
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
# Fonction de vStream qui remplace urllib.quote, pour simplifier le passage en python 3
from resources.lib.util import Quote, cUtil

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
headers = {'User-Agent': UA}

SITE_IDENTIFIER = 'zone_telechargement_ws'
SITE_NAME = '[COLOR violet]Zone-Telechargement[/COLOR]'
SITE_DESC = 'Fichier en DDL, HD'

URL_HOST = 'https://wwvw.ZT-ZA.com/'


def GetURL_MAIN():
    ADDON = addon()
    MemorisedHost = ''
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    Sources = oInputParameterHandler.getValue('function')

    # z = oInputParameterHandler.getAllParameter()
    # VSlog(z)

    # quand vstream load tous les sites on passe >> globalSources
    # quand vstream load a partir du menu home on passe >> callplugin
    # quand vstream fabrique une liste de plugin pour menu(load site globalRun and call function search) >> search
    # quand l'url ne contient pas celle déjà enregistrer dans settings et que c'est pas dlprotect on active.
    if not (Sources == 'callpluging' or Sources == 'globalSources' or Sources == 'search') and not ADDON.getSetting('ZT')[6:] in sUrl and not 'dl-protect1.' in sUrl and not 'zt-protect.' in sUrl:
        oRequestHandler = cRequestHandler(URL_HOST)
        oRequestHandler.request()
        MemorisedHost = oRequestHandler.getRealUrl()
        if MemorisedHost is not None and MemorisedHost != '':
            if not 'cf_chl_jschl_tk' in MemorisedHost:
                ADDON.setSetting('ZT', MemorisedHost)
                VSlog("ZT url  >> " + str(MemorisedHost) + ' sauvegarder >> ' + ADDON.getSetting('ZT'))
        else:
            ADDON.setSetting('ZT', URL_HOST)
            VSlog("Url non changer car egal a None le site peux etre surchager utilisation de >> ADDON.getSetting('ZT')")

        return ADDON.getSetting('ZT')
    else:
        # si pas de zt dans settings on récup l'url une fois dans le site
        if not ADDON.getSetting('ZT') and not (Sources == 'callpluging' or Sources == 'globalSources' or Sources == 'search'):
            oRequestHandler = cRequestHandler(URL_HOST)
            oRequestHandler.request()
            MemorisedHost = oRequestHandler.getRealUrl()
            if MemorisedHost is not None and MemorisedHost != '':
                if not 'cf_chl_jschl_tk' in MemorisedHost:
                    ADDON.setSetting('ZT', MemorisedHost)
                    VSlog("ZT url vide  >> " + str(MemorisedHost) + ' sauvegarder >> ' + ADDON.getSetting('ZT'))
            else:
                ADDON.setSetting('ZT', URL_HOST)
                VSlog("Url non changer car egal a None le site peux etre surcharger utilisation de >> ADDON.getSetting('ZT')")

            return ADDON.getSetting('ZT')
        else:
            VSlog("ZT pas besoin d'url")
            return ADDON.getSetting('ZT')


URL_MAIN = GetURL_MAIN()

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
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'films.png', oOutputParameterHandler)

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
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EXCLUS[1], 'Exclus (Films populaires)', 'news.png', oOutputParameterHandler)

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
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

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
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VFSTFR[1], 'Films en francais sous titre francais (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MKV[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MKV[1], 'Films (dvdrip mkv)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VO[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VO[1], 'Films en Version original (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_INTEGRAL[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_INTEGRAL[1], 'Integral de films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuSeries():
    oGui = cGui()

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
    if (sSearchText != False):
        sSearchText = Quote(sSearchText)
        sUrl = URL_SEARCH[0] + sSearchText + '&note=0&art=0&AiffchageMode=0&inputTirePar=0&cstart=0'
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
    liste.append(['Aventure', 'Aventure'])
    liste.append(['Biopic', 'Biopic'])
    liste.append(['Comédie Dramatique', 'Dramatique'])
    liste.append(['Comédie Musicale', 'Musical'])
    liste.append(['Comédie', 'Comedie'])
    liste.append(['Divers', 'Divers'])
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
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if sSearch:
        sUrl = sSearch

    oRequestHandler = cRequestHandler(sUrl.replace('https', 'http'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    sPattern = '<img class="mainimg.+?src="([^"]+)"(?:.|\s)+?<a href="([^"]+)">([^"]+)</a>.+?<span class=".+?<b>([^"]+)</span>.+?">([^<]+)</span>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    titles = set()

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
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
            if not '[Complete]' in sTitle:
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

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDisplayTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'anime' in sUrl or 'anime' in sUrl2:
                oGui.addAnime(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, '', sThumb, '', oOutputParameterHandler)
            elif 'serie' in sUrl or 'serie' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, '', sThumb, '', oOutputParameterHandler)
            elif DOC_NEWS[0] in sUrl or TV_NEWS[0] in sUrl or SPECT_NEWS[0] in sUrl or CONCERT_NEWS[0] in sUrl :
                oGui.addMisc(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, '', sThumb, '', oOutputParameterHandler)
            elif 'collection' in sUrl or 'integrale' in sUrl:
                oGui.addMoviePack(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        if 'controller.php' in sUrl:
            sPattern = '<a href="#" class="nav" data-cstart="([^"]+)">Suivant</a></div>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', re.sub('cstart=(\d+)', 'cstart=' + str(aResult[1][0]), sUrl))
                number = re.search('([0-9]+)', aResult[1][0]).group(1)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + number + ' >>>[/COLOR]', oOutputParameterHandler)

        else:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
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
    if (aResult[0] == True):
        nextPage = aResult[1][0]
        if not nextPage.startswith('https'):
            nextPage = URL_MAIN + nextPage
        return nextPage
    return False

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

    oRequestHandler = cRequestHandler(sUrl.replace('https', 'http'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
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

    try:
        sDesc = sDesc.encode('latin-1')
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

    # on regarde si dispo dans d'autres qualités
    sPattern = '<a href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)</b></span><span style="color:#.{6}"><b>([^<]+)</b></span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
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
    # VSlog('mode serie')
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

    # récupération du Synopsis
    sDesc = sMovieTitle   # Ne pas laisser vide sinon un texte automatique faux va être calculé
    try:
        sPattern = 'synopsis.+(alt="">|<!--dle_image_end-->)(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = cUtil().removeHtmlTags(aResult[1][0][1])
    except:
        pass

    try:
        sDesc = sDesc.encode('latin-1')
    except:
        pass

    # on recherche d'abord la qualité courante
    sPattern = '<div style="[^"]+?">.+?Qualité (.+?) [|] (.+?)<.+?img src="(([^"]+))"'
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    sQual = ''
    sLang = ''
    if (aResult[1]):    
        aEntry = aResult[1][0]
        sQual = aEntry[0]
        sLang = aEntry[1]
        sThumb = aEntry[2]  # change pour chaque saison, il faut la rechercher si on navigue entre saisons
    sDisplayTitle = ('%s [%s] (%s)') % (sMovieTitle, sQual, sLang)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oOutputParameterHandler.addParameter('sDesc', sDesc)
    oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    # on regarde si dispo dans d'autres qualités
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
            oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    # on regarde si dispo d'autres saisons
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
            oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, 'series.png', sThumb, sMovieTitle, oOutputParameterHandler)

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

    try:
        sDesc = unicodedata.normalize('NFD', sDesc).encode('ascii', 'ignore').decode('unicode_escape')
        sDesc = sDesc.encode('latin-1')
    except:
        pass
        
    oRequestHandler = cRequestHandler(sUrl.replace('https', 'http'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    # Si ca ressemble aux lien premiums on vire les liens non premium
    if 'Premium' in sHtmlContent or 'PREMIUM' in sHtmlContent:
        sHtmlContent = CutNonPremiumlinks(sHtmlContent)

    oParser = cParser()

    sPattern = '<font color=red>([^<]+?)</font>|<b><div style=".+?">([^<]+)</div>.+?class="btnToLink".+?href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if aEntry[0]:
                if ('Interchangeables' not in aEntry[0]):
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            else:
                sDisplayTitle = sMovieTitle + ' [COLOR coral]' + aEntry[1] + '[/COLOR] '
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', aEntry[2])
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

    oRequestHandler = cRequestHandler(sUrl.replace('https', 'http'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    # Pour les series on fait l'inverse des films on vire les liens premiums
    if 'Premium' in sHtmlContent or 'PREMIUM' in sHtmlContent or 'premium' in sHtmlContent:
        sHtmlContent = CutPremiumlinks(sHtmlContent)

    sPattern = '<div style="font-weight:bold;color:.+?">(.+?)</div>|<a class="btnToLink".+?href="(.+?)">(.+?)</a></b>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if aEntry[0]:
                if 'Télécharger' in aEntry[0]:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]' + aEntry[0] + '[/COLOR]')
                else:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            else:
                sName = aEntry[2]
                sName = sName.replace('Télécharger', '')
                sName = sName.replace('pisodes', 'pisode')
                sUrl2 = aEntry[1]
                sTitle = sMovieTitle + ' ' + sName

                oOutputParameterHandler = cOutputParameterHandler()
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

    # Ne marche pas
    if (False):
        code = {'123455600123455602123455610123455615': 'http://uptobox.com/',
                '1234556001234556071234556111234556153': 'http://turbobit.net/',
                '123455600123455605123455615': 'http://ul.to/',
                '123455600123455608123455610123455615': 'http://nitroflare.com/',
                '123455601123455603123455610123455615123455617': 'https://1fichier.com/?',
                '123455600123455606123455611123455615': 'http://rapidgator.net/'}

        for k in code:
            match = re.search(k + '(.+)$', sUrl)
            if match:
                sHosterUrl = code[k] + match.group(1)
                sHosterUrl = sHosterUrl.replace('123455615', '/')
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                oGui.setEndOfDirectory()
                return

    # Est ce un lien dl-protect ?
    if sUrl:

        sHtmlContent = DecryptDlProtecte(sUrl)

        if sHtmlContent:
            # Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotecte = (True, [sHtmlContent])
            else:
                sPattern_dlprotecte = '<div class="alert alert-primary".+?href="(.+?)"'
                aResult_dlprotecte = oParser.parse(sHtmlContent, sPattern_dlprotecte)

        else:
            dialog().VSok('Erreur décryptage du lien')
            aResult_dlprotecte = (False, False)

    # Si lien normal
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotecte = (True, [sUrl])

    if (aResult_dlprotecte[0]):

        episode = 1

        for aEntry in aResult_dlprotecte[1]:
            sHosterUrl = aEntry

            sTitle = sMovieTitle
            if len(aResult_dlprotecte[1]) > 1:
                sTitle = sMovieTitle + ' episode ' + episode

            episode += 1

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


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


def CutNonPremiumlinks(sHtmlContent):
    oParser = cParser()
    sPattern = '(?:Lien.+?Premium - 1 lien|Lien.+?Premium)(.+?)</b></font></a></center>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        return aResult[1][0]

    # Si ca marche pas on renvois le code complet
    return sHtmlContent


def CutPremiumlinks(sHtmlContent):
    oParser = cParser()
    sPattern = '(?i) par .{1,2}pisode(.+?)$'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        sHtmlContent = aResult[1][0]

    # Si ca marche pas on renvois le code complet
    return sHtmlContent


def DecryptDlProtecte(url):

    if not (url):
        return ''

    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request()
    # Cookie = oRequestHandler.GetCookies()

    oParser = cParser()
    sPattern = '<form action="(.+?)".+?type="hidden" name="_token" value="(.+?)">.+?<input type="hidden" value="(.+?)"'
    result = oParser.parse(sHtmlContent, sPattern)

    if (result[0]):
        RestUrl = str(result[1][0][0])
        token = str(result[1][0][1])
        urlData = str(result[1][0][2])
        
    else:
        sPattern = '<(.+?)action="([^"]+)" method="([^"]+)">.+?hidden".+?value="([^"]+)"'
        result = oParser.parse(sHtmlContent, sPattern)

        if not "<!-----" in (str(result[1][0][0])):
            RestUrl = str(result[1][0][0])
            method = str(result[1][0][1])
            token = str(result[1][0][2])
        else:
            RestUrl = str(result[1][1][1]).replace("}", '%7D')
            method = str(result[1][1][2])
            token = str(result[1][1][3])

        # VSlog(token)
        # VSlog(method)
        # VSlog(RestUrl)

        if RestUrl.startswith('/'):
            RestUrl = 'https://' + url.split('/')[2] + RestUrl

    # f = {'_token': token}
    # data = urlEncode(f)

    oRequestHandler = cRequestHandler(RestUrl)
    if method == "post":
        oRequestHandler.setRequestType(1)
    # oRequestHandler.addHeaderEntry('User-Agent', UA)
    # oRequestHandler.addHeaderEntry('Host', url.split('/')[2])
    # oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    # oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    # oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    # oRequestHandler.addHeaderEntry('Referer', url)
    # oRequestHandler.addHeaderEntry('Content-Type',  'application/x-www-form-urlencoded')
    # oRequestHandler.addHeaderEntry('Content-Length', len(str(data)))
    # oRequestHandler.addHeaderEntry('Cookie', Cookie)
    oRequestHandler.addParameters('_token', token)
    # oRequestHandler.addParametersLine(data)
    sHtmlContent = oRequestHandler.request()
    
    # fh = open('c:\\test.txt', 'w')
    # fh.write(sHtmlContent)
    # fh.close()
    
    return sHtmlContent


# ******************************************************************************
# from http://code.activestate.com/recipes/578668-encode-multipart-form-data-for-uploading-files-via/

"""Encode multipart form data to upload files via POST."""


def encode_multipart(fields, files, typeUrl, param, boundary=None):
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

    _BOUNDARY_CHARS = string.digits

    def escape_quote(s):
        return s.replace('"', '\\"')

    if boundary is None:
        boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(27))
    lines = []

    for name, value in fields.items():
        lines.extend((
            '-----------------------------{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"'.format(escape_quote(typeUrl)),
            '',
            '{0}'.format(param),
            '-----------------------------{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name)),
            '',
            str(value),
            '-----------------------------{0}--'.format(boundary),
            '',
        ))

    for name, value in files.items():
        filename = value['filename']
        if 'mimetype' in value:
            mimetype = value['mimetype']
        else:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        lines.extend((
            '--{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"'.format(
                    escape_quote(name), escape_quote(filename)),
            'Content-Type: {0}'.format(mimetype),
            '',
            value['content'],
        ))

    body = '\r\n'.join(lines)

    headers = {'Content-Type': 'multipart/form-data; boundary=---------------------------{0}'.format(boundary),
               'Content-Length': str(len(body))}

    return body, headers
