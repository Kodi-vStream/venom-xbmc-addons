#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, dialog, VSlog, addon
from resources.lib.config import GestionCookie

import re, random

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

SITE_IDENTIFIER = 'tirexo'
SITE_NAME = '[COLOR violet]Tirexo (ZT lol)[/COLOR]'
SITE_DESC = 'Films/Séries/Reportages/Concerts'
URL_HOST = 'https://www.zone-warez.com/'

def getURL():
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_HOST)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="full-wrap clearfix btn btn-danger" href="([^"]+)">Acc&eacute;der au site</a></div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

def GetURL_MAIN():
    ADDON = addon()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    Sources = oInputParameterHandler.getValue('function')

    # z = oInputParameterHandler.getAllParameter()
    # VSlog(z)

    # quand vstream load tous les sites on passe >> globalSources
    # quand vstream load a partir du menu home on passe >> callplugin
    # quand vstream fabrique une liste de plugin pour menu(load site globalRun and call function search) >> search
    # quand l'url ne contient pas celle déjà enregistrer dans settings et que c'est pas dlprotect on active.
    if not (Sources == 'callpluging' or Sources == 'globalSources' or Sources == 'search') and not ADDON.getSetting('Tirexo')[6:] in sUrl and not 'dl-protect.' in sUrl and not 'zt-protect.' in sUrl:
        MemorisedHost = getURL()
        if MemorisedHost is not None and MemorisedHost != '' :
            if not 'cf_chl_jschl_tk' in MemorisedHost:
                ADDON.setSetting('Tirexo', MemorisedHost)
                VSlog("Tirexo url  >> " + str(MemorisedHost) + ' sauvegarder >> ' + ADDON.getSetting('Tirexo'))
        else:
            ADDON.setSetting('Tirexo', URL_HOST)
            VSlog("Url non changer car égal à None le site peux être surcharger utilisation de >> ADDON.getSetting('Tirexo')")

        return ADDON.getSetting('Tirexo')
    else:
        # si pas de zt dans settings on récup l'url une fois dans le site
        if not ADDON.getSetting('Tirexo') and not (Sources == 'callpluging' or Sources == 'globalSources' or Sources == 'search'):
            MemorisedHost = getURL()
            if MemorisedHost is not None and MemorisedHost != '':
                if not 'cf_chl_jschl_tk' in MemorisedHost:
                    ADDON.setSetting('Tirexo', MemorisedHost)
                    VSlog("Tirexo url vide  >> " + str(MemorisedHost) + ' sauvegarder >> ' + ADDON.getSetting('Tirexo'))
            else:
                ADDON.setSetting('Tirexo', URL_HOST)
                VSlog("Url non changer car égal à None le site peux être surcharger utilisation de >> ADDON.getSetting('Tirexo')")

            return ADDON.getSetting('Tirexo')
        else:
            VSlog("Tirexo pas besoin d'url")
            return ADDON.getSetting('Tirexo')

URL_MAIN = "https://www2.zone-warez.org/"
URL_SEARCH_MOVIES = (URL_MAIN + 'index.php?do=search&subaction=search&catlist=2&story=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'index.php?do=search&subaction=search&catlist=15&story=', 'showMovies')
URL_SEARCH_ANIMS = (URL_MAIN + 'index.php?do=search&subaction=search&catlist=32&story=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + 'index.php?do=search&subaction=search&catlist=39&story=', 'showMovies')

MOVIE_MOVIE = (True, 'showMenuMovies')
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

MOVIE_2010 = (URL_MAIN + 'films-2010-2019/', 'showMovies')
MOVIE_2000 = (URL_MAIN + 'films-2000-2009/', 'showMovies')
MOVIE_1990 = (URL_MAIN + 'films-1990-1999/', 'showMovies')
MOVIE_1980 = (URL_MAIN + 'films-1980-1989/', 'showMovies')
MOVIE_1970 = (URL_MAIN + 'films-1970-1979/', 'showMovies')
MOVIE_1960 = (URL_MAIN + 'films-1960-1969/', 'showMovies')
MOVIE_1950 = (URL_MAIN + 'films-1950-1959/', 'showMovies')
MOVIE_1900 = (URL_MAIN + 'films-1900-1950/', 'showMovies')

MOVIE_GENRES = ('films-gratuit/', 'showGenre')
SERIE_GENRES = ('telecharger-series/', 'showGenre')

SERIE_SERIES = (True, 'showMenuSeries')
SERIE_VFS = (URL_MAIN + 'series-vf/', 'showMovies')
SERIE_VF_720 = (URL_MAIN + 'series-vf-en-hd/','showMovies')
SERIE_VF_1080 = (URL_MAIN + 'series-vf-1080p/','showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'series-vostfr/', 'showMovies')
SERIE_VOSTFRS_720 = (URL_MAIN + 'series-vostfr-hd/','showMovies')
SERIE_VOSTFRS_1080 = (URL_MAIN + 'series-vostfr-1080p/','showMovies')
SERIE_VO = (URL_MAIN + 'series-vo/', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'telecharger-series/', 'showMovies')

ANIM_ANIMS = (True, 'showMenuMangas')
ANIM_VFS = (URL_MAIN + 'animes-vf/', 'showMovies')
ANIM_VF_720 = (URL_MAIN + 'animes-vf-720p/', 'showMovies')
ANIM_VF_1080 = (URL_MAIN + 'animes-vf-1080p/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'animes-vostfr/', 'showMovies')
ANIM_VOSTFRS_720 = (URL_MAIN + 'animes-vostfr-720p/', 'showMovies')
ANIM_VOSTFRS_1080 = (URL_MAIN + 'animes-vostfr-1080p/', 'showMovies')
FILM_ANIM = (URL_MAIN + 'films-mangas/', 'showMovies')
ANIM_NEWS = (URL_MAIN + 'animes/', 'showMovies')

DOC_NEWS = (URL_MAIN + 'emissions-tv-documentaires/souscate_doc-Documentaire/', 'showMovies')
SPORT_SPORTS = (URL_MAIN + 'emissions-tv-documentaires/souscate_doc-Sport/', 'showMovies')
TV_NEWS = (URL_MAIN + 'emissions-tv-documentaires/souscate_doc-Émissions+TV/', 'showMovies')
SPECT_NEWS = (URL_MAIN + 'emissions-tv-documentaires/souscate_doc-Spectacle/', 'showMovies')
CONCERT_NEWS = (URL_MAIN + 'musiques-mp3-gratuite/souscat_music-Concerts/', 'showMovies')

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
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD[1], 'Films (720p)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (1080p)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIP[1], 'Films (BDRIP)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4K[1], 'Films (4K)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MKV[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MKV[1], 'Films (dvdrip mkv)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SDLIGHT[1], 'Films (720p - Light)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films (1080p - Light)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4KL[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4KL[1], 'Films (4K - light)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Films (3D)', 'films.png', oOutputParameterHandler)

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
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF_720[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries 720p (VF)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF_1080[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries 1080p (VF)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS_720[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS_720[1], 'Séries 720p (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS_1080[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS_1080[1], 'Séries 1080p (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VO[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VO[1], 'Séries (VO)', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher Animes', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animes (VF)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VF_720[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VF_720[1], 'Animes 720p (VF)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VF_1080[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VF_1080[1], 'Animes 1080p (VF)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animes (VOSTFR)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS_720[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS_720[1], 'Animes 720p (VOSTFR)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS_1080[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS_1080[1], 'Animes 1080p (VOSTFR)', 'animes.png', oOutputParameterHandler)

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
    oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1], 'Sports', 'sport.png', oOutputParameterHandler)

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
    URL_MOVIES = URL_MAIN + sUrl + 'genre-'

    listeGenres = ['Action', 'Animation', 'Arts Martiaux', 'Aventure', 'Biopic', 'Bollywood', 'Comédie Dramatique',
                   'Comédie Musicale', 'Comédie', 'Documentaire', 'Drame', 'Epouvante-horreur', 'Espionnage',
                   'Famille', 'Fantastique', 'Guerre', 'Historique', 'Horreur', 'Musical', 'Péplum',
                   'Policier', 'Romance', 'Science Fiction', 'Thriller', 'Western']
    for genre in listeGenres:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MOVIES + genre.replace(' ', '%20')+ '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', genre, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sSearch:
        sUrl = sSearch

    if sSearch or "index" in sUrl: # en mode recherche
        sPattern = '<a class="mov-t nowrap" href="([^"]+)" title="[^"]+"> *<div data-toggle=.+?data-content="([^"]+)".+?<img src="([^"]+)".+?alt="([^"]+)".+?<a href="([^"]+)">(.+?)<'
    else:
        sPattern = '<a class="mov-t nowrap" href="([^"]+)"> *<div data-toggle=.+?data-content="([^"]+)".+?<img src="([^"]+)".+?title="([^"]+)".+?(> *<\/a>|annee-de-sortie\/(.+?)\/)'

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
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
            sDesc = aEntry[1]
            sThumb = aEntry[2]
            sTitle = aEntry[3]
            sYear = aEntry[5]

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

            if 'series' in sUrl2 or 'animes' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif 'collection' in sUrl2 or 'integrale' in sUrl2:
                oGui.addMoviePack(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        if 'index' in sUrl:
            sPattern = '<a name="nextlink".+?javascript:list_submit\((.+?)\)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', re.sub('search_start=(\d+)', 'search_start=' + str(aResult[1][0]), sUrl))
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)
        else:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'href="([^"]+)"><span class="fa fa-arrow-right">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
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
    sPattern = '<span data-slice="200" itemprop="description">(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = aResult[1][0]
        sDesc = sDesc.replace('<span>', '').replace('</span>', '')
        sDesc = sDesc.replace('<b>', '').replace('</b>', '')
        sDesc = sDesc.replace('<i>', '').replace('</i>', '')
        sDesc = sDesc.replace('<br>', '').replace('<br />', '')

    #on recherche d'abord la qualité courante
    sPattern = 'couleur-qualitesz"> *Qualité (.+?) <.+?"couleur-languesz">(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sTitle = sMovieTitle
    sQual = ''
    if (aResult[0]):
        sQual = aResult[1][0][0]
        sLang = aResult[1][0][1]
        sTitle = ('%s [%s] (%s)') % (sMovieTitle, sQual, sLang)

    # On ajoute le lien même si on n'a pas réussi à déterminer la qualité
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oOutputParameterHandler.addParameter('sDesc', sDesc)
    oOutputParameterHandler.addParameter('sYear', sYear)

    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    #on regarde si dispo dans d'autres qualités
    sPattern = '<a href="([^"]+)"><span class="otherquality">.+?<b>([^"]+)<\/b>.+?<b>([^"]+)<\/b>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sQual = aEntry[1]
            sLang = aEntry[2]
            sTitle = ('%s [%s] %s') % (sMovieTitle, sQual, sLang)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    #  Qualité STREAMING
    sPattern = '<th .+?<img src=.+?>([^>]+?)<\/th>.+?class=\'streaming\' href=\'#\' data-text=.+? data-lien=\'([^>]+?)\' data-id=\'([^>]+?)\''
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            data_lien = aEntry[1]
            data_id = aEntry[2]
            sUrl2 = URL_MAIN + "?do=streaming&id_lien="+data_id+"&lien="+data_lien
            sTitle = ('%s [STREAMING]') % (sMovieTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addMovie(SITE_IDENTIFIER, 'showHostersLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showSeriesLinks():
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
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles pour cette saison :[/COLOR]')

    #récupération du Synopsis
    try:
        sPattern = '<span data-slice="200" itemprop="description">(.+?)</span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
            sDesc = sDesc.replace('<span>', '').replace('</span>', '')
            sDesc = sDesc.replace('<b>', '').replace('</b>', '')
            sDesc = sDesc.replace('<i>', '').replace('</i>', '')
            sDesc = sDesc.replace('<br>', '').replace('<br />', '')
    except:
        pass

    #Mise à jour du titre
    sPattern = '<h2>Télécharger <b itemprop="name">(.+?)</b>.+?>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sTitle = sMovieTitle
    if (aResult[0]):
        sTitle = aResult[1][0][0] + " " + aResult[1][0][1]

    numSaison = str(aResult[1][0][1]).lower().replace("saison", "").strip()
    saisons = []
    saisons.append(numSaison)

    #on recherche d'abord la qualité courante
    sPattern = 'couleur-qualitesz">Qualité (.+?) <.+?couleur-languesz">(.+?)</span><br>.+?"couleur-seriesz">(.+?)\['
    aResult = oParser.parse(sHtmlContent, sPattern)

    sDisplayTitle = sTitle
    sQual = ''
    if (aResult[0]):
        sQual = aResult[1][0][0]
        sLang = aResult[1][0][1]
        sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oOutputParameterHandler.addParameter('sDesc', sDesc)
    oOutputParameterHandler.addParameter('sYear', sYear)
    oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    #on regarde si dispo dans d'autres qualités
    sHtmlContent1 = CutQual(sHtmlContent)
    sPattern1 = '<a href="([^"]+)"><span class="otherquality">.+?<b>([^"]+)<\/b>.+?<b>([^"]+)<\/b>.+?<b> (.+?)<'
    aResult1 = oParser.parse(sHtmlContent1, sPattern1)

    otherSaison = False

    if (aResult1[0] == True):
        total = len(aResult1[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult1[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # Si saison différente
            sSaison = aEntry[1].strip()
            if numSaison != sSaison:
                otherSaison = True
                continue

            sQual = aEntry[2]
            sLang = aEntry[3]
            sDisplayTitle = ('%s [%s] %s') % (sTitle, sQual, sLang)

            sUrl = aEntry[0]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    #on regarde si dispo d'autres saisons
    if (otherSaison):

        #Affichage du titre
        oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Autres saisons disponibles pour cette série :[/COLOR]')

        # Une ligne par saison, pas besoin d'afficher les qualités ici
        for aEntry in aResult1[1]:

            sSaison = aEntry[1].strip()
            if sSaison in saisons:
                continue
            saisons.append(sSaison)
            sSaison = 'Saison ' + sSaison
            sDisplayTitle = ('%s %s') % (sMovieTitle, sSaison)

            sUrl = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

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

    # Ajout des liens DL
    # Gere si un Hoster propose plusieurs liens
    # Retire les resultats proposés en plusieurs parties (ce sont des .rar)
    sPattern = '<th scope="col" class="no-sort"><img src=.+?>(.+?)<\/th>|class=\'download\'.+?href=\'([^>]+?)\'>Télécharger <'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                sHoster = re.sub('\.\w+', '', aEntry[0])
                continue;

            sUrl2 = URL_MAIN[:-1] + aEntry[1]
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

def showHostersLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        if not aResult[1][0].startswith('http'):
            sHosterUrl = "https:" + aResult[1][0]
        else:
            sHosterUrl = aResult[1][0]
            
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

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
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<th scope="col" class="no-sort"><img alt=.+?>(.+?)<\/th>|href=\'([^>]+?)\'>Episode ([^>]+)<'
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
                sUrl2 = URL_MAIN[:-1] + aEntry[1]
                sTitle = sMovieTitle + ' E' + aEntry[2].replace('FINAL ', '')
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
    #VSlog('Display_protected_link')
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    #Ne marche pas
    if (False):
        code = {
            '123455600123455602123455610123455615': 'http://uptobox.com/',
            '1234556001234556071234556111234556153': 'http://turbobit.net/',
            '123455600123455605123455615': 'http://ul.to/',
            '123455600123455608123455610123455615': 'http://nitroflare.com/',
            '123455601123455603123455610123455615123455617': 'https://1fichier.com/?',
            '123455600123455606123455611123455615': 'http://rapidgator.net/'
        }

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

    if 'link' in sUrl:
        #Temporairement car la flemme de ce battre avec les redirection
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()
        sUrl = oRequestHandler.getRealUrl()

    if "dl-protect" in sUrl:
        sHtmlContent = DecryptDlProtecte(sUrl)

        if sHtmlContent:
            #Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotecte = (True, [sHtmlContent])
            else:
                sPattern_dlprotecte = '<div class="lienet"><a href="(.+?)">'
                aResult_dlprotecte = oParser.parse(sHtmlContent, sPattern_dlprotecte)

        else:
            oDialog = dialog().VSok('Erreur de décryptage du lien')
            aResult_dlprotecte = (False, False)

    #Si lien normal
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

            episode+= 1

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def CutQual(sHtmlContent):
    oParser = cParser()
    sPattern = 'Qualit.+?galement disponibles pour cette saison:</span><br>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        return aResult[1][0]
    else:
        return sHtmlContent

    return ''

def CutSais(sHtmlContent):
    oParser = cParser()
    sPattern = '"otherversionsspan">Saisons.+?galement disponibles pour cette série:(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        return aResult[1][0]
    return ''

def DecryptDlProtecte(url):
    VSlog('DecryptDlProtecte : ' + url)

    if not (url):
        return ''

    passe = 0

    # 1ere Requete on tente de voir si ca passe du 1er coup
    cookies = GestionCookie().Readcookie('www_dl-protect1_co')
    sHtmlContent = exectProtect(cookies, url)

    while (re.search('<input type="submit" class="continuer" name="submit" value="Continuer" />', sHtmlContent)):
        if passe == 0:
            cookies = GestionCookie().Readcookie('www_dl-protect1_co')
            passe = passe + 1

        elif passe <= 3:
            #On brute force pour voir
            sHtmlContent = exectProtect(cookies, url)
            passe = passe + 1

        else:
            break

    #fh = open('d:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    return sHtmlContent

def exectProtect(cookies, url):
    #Tout ca a virer et utiliser oRequestHandler.addMultipartFiled('sess_id': sId, 'upload_type': 'url', 'srv_tmp_url': sTmp) quand ca marchera
    import string
    _BOUNDARY_CHARS = string.digits
    boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(30))
    multipart_form_data = {'submit': 'continuer', 'submit': 'Continuer'}
    data, headersMulti = encode_multipart(multipart_form_data, {}, boundary)

    #2 eme requete pour avoir le lien
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('Host', url.split('/')[2])
    oRequestHandler.addHeaderEntry('Referer', url)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Content-Length', headersMulti['Content-Length'])
    oRequestHandler.addHeaderEntry('Content-Type', headersMulti['Content-Type'])
    oRequestHandler.addHeaderEntry('Cookie', cookies)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')

    oRequestHandler.addParametersLine(data)

    sHtmlContent = oRequestHandler.request()
    return sHtmlContent

#******************************************************************************
#from http://code.activestate.com/recipes/578668-encode-multipart-form-data-for-uploading-files-via/

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
        lines.extend((
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

    headers = {
        'Content-Type': 'multipart/form-data; boundary=---------------------------{0}'.format(boundary),
        'Content-Length': str(len(body)),
    }

    return (body, headers)
