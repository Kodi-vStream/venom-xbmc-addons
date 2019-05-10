#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress, dialog, VSlog, addon
from resources.lib.config import GestionCookie

import urllib, re, urllib2
import random

#from resources.lib.dl_deprotect import DecryptDlProtect

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
headers = { 'User-Agent': UA }

SITE_IDENTIFIER = 'zone_telechargement_ws'
SITE_NAME = '[COLOR violet]Zone-Telechargement[/COLOR]'
SITE_DESC = 'Fichier en DDL, HD'

URL_HOST = 'https://www.annuaire-telechargement.com/'

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
    if not (Sources == 'callpluging' or Sources == 'globalSources' or Sources == 'search') and not ADDON.getSetting('ZT')[6:] in sUrl and not 'dl-protect1.com' in sUrl:
        oRequestHandler = cRequestHandler(URL_HOST)
        sHtmlContent = oRequestHandler.request()
        MemorisedHost = oRequestHandler.getRealUrl()
        if MemorisedHost is not None and MemorisedHost != '':
            ADDON.setSetting('ZT', MemorisedHost)
            VSlog("ZT url  >> " + str(MemorisedHost) + ' sauvegarder >> ' + ADDON.getSetting('ZT'))
        else:
            VSlog("Url non changer car egal a None le site peux etre surchager utilisation de >> ADDON.getSetting('ZT')")

        return ADDON.getSetting('ZT')
    else:
        # si pas de zt dans settings on récup l'url une fois dans le site
        if not ADDON.getSetting('ZT') and not (Sources == 'callpluging' or Sources == 'globalSources' or Sources == 'search'):
            oRequestHandler = cRequestHandler(URL_HOST)
            sHtmlContent = oRequestHandler.request()
            MemorisedHost = oRequestHandler.getRealUrl()
            if MemorisedHost is not None and MemorisedHost != '':
                ADDON.setSetting('ZT', MemorisedHost)
                VSlog("ZT url vide  >> " + str(MemorisedHost) + ' sauvegarder >> ' + ADDON.getSetting('ZT'))
            else:
                VSlog("Url non changer car egal a None le site peux etre surchager utilisation de >> ADDON.getSetting('ZT')")

            return ADDON.getSetting('ZT')
        else:
            VSlog("ZT pas besoin d'url")
            return ADDON.getSetting('ZT')

URL_MAIN = GetURL_MAIN()

URL_DECRYPT =  ''

URL_SEARCH = (URL_MAIN + 'index.php?', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'index.php?', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN  + 'index.php?', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'nouveaute/', 'showMovies') # films (derniers ajouts)
MOVIE_EXCLUS = (URL_MAIN + 'exclus/', 'showMovies') # exclus (films populaires)
MOVIE_3D = (URL_MAIN + 'films-bluray-3d/', 'showMovies') # films en 3D
MOVIE_HD = (URL_MAIN + 'films-bluray-hd/', 'showMovies') # films en HD
MOVIE_HDLIGHT = (URL_MAIN + 'x265-x264-hdlight/', 'showMovies') # films en x265 et x264
MOVIE_VOSTFR = (URL_MAIN + 'filmsenvostfr/', 'showMovies') # films VOSTFR
MOVIE_4K = (URL_MAIN + 'film-ultra-hd-4k/', 'showMovies') # films "4k"
MOVIE_GENRES = (URL_MAIN , 'showGenre')
MOVIE_ANIME = (URL_MAIN + 'dessins-animes/', 'showMovies') # dessins animes
MOVIE_BDRIP = (URL_MAIN + 'films-dvdrip-bdrip/', 'showMovies')
MOVIE_TS_CAM = (URL_MAIN + 'scrr5tscam-films-2017/', 'showMovies')
MOVIE_VFSTFR = (URL_MAIN + 'films-vfstfr/', 'showMovies')
MOVIE_MKV = (URL_MAIN + 'films-mkv/', 'showMovies')
MOVIE_VO = (URL_MAIN + 'films-vo/','showMovies')
MOVIE_INTEGRAL = (URL_MAIN + 'collection-films-integrale/','showMovies')

SERIE_VFS = (URL_MAIN + 'series-vf/', 'showMovies')
SERIE_VF_720 = (URL_MAIN + 'series-vf-en-hd/','showMovies')
SERIE_VF_1080 = (URL_MAIN + 'series-vf-1080p/','showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'series-vostfr/', 'showMovies')
SERIE_VOSTFRS_720 = (URL_MAIN + 'series-vostfr-hd/','showMovies')
SERIE_VOSTFRS_1080 = (URL_MAIN + 'series-vostfr-1080p/','showMovies')
SERIE_VO = (URL_MAIN + 'series-vo/', 'showMovies')
ANCIENNE_SERIE = (URL_MAIN + 'telecharger-series/ancienne-serie/', 'showMovies')

ANIME_VFS = (URL_MAIN + 'animes-vf/', 'showMovies')
ANIME_VF_720 = (URL_MAIN + 'animes-vf-720p/','showMovies')
ANIME_VF_1080 = (URL_MAIN + 'animes-vf-1080p/','showMovies')
ANIME_VOSTFRS = (URL_MAIN + 'animes-vostfr/', 'showMovies')
ANIME_VOSTFRS_720 = (URL_MAIN + 'animes-vostfr-720p/','showMovies')
ANIME_VOSTFRS_1080 = (URL_MAIN + 'animes-vostfr-1080p/','showMovies')
ANIME_VOSTEN = (URL_MAIN + 'animes-vosten/', 'showMovies')
FILM_ANIME = (URL_MAIN + 'films-mangas/','showMovies')
OAV = (URL_MAIN + 'oav/','showMovies')

DOC_NEWS = (URL_MAIN + 'documentaires-gratuit/', 'showMovies') # docs
DOC_DOCS = ('http://', 'load')

SPORT_SPORTS = (URL_MAIN + 'sport/', 'showMovies') # sports
TV_NEWS = (URL_MAIN + 'emissions-tv/', 'showMovies') # dernieres emissions tv
SPECT_NEWS = (URL_MAIN + 'spectacles/', 'showMovies') # derniers spectacles
CONCERT_NEWS = (URL_MAIN + 'concerts/', 'showMovies') # derniers concerts
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
    oOutputParameterHandler.addParameter('siteUrl', ANIME_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIME_VFS[1], 'Animes (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIME_VF_720[0])
    oGui.addDir(SITE_IDENTIFIER, ANIME_VF_720[1], 'Animes 720p (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIME_VF_1080[0])
    oGui.addDir(SITE_IDENTIFIER, ANIME_VF_1080[1], 'Animes 1080p (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIME_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIME_VOSTFRS[1], 'Animes (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIME_VOSTFRS_720[0])
    oGui.addDir(SITE_IDENTIFIER, ANIME_VOSTFRS_720[1], 'Animes 720p (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIME_VOSTFRS_1080[0])
    oGui.addDir(SITE_IDENTIFIER, ANIME_VOSTFRS_1080[1], 'Animes 1080p (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', FILM_ANIME[0])
    oGui.addDir(SITE_IDENTIFIER, FILM_ANIME[1], 'Films d\'animes ', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIME_VOSTEN[0])
    oGui.addDir(SITE_IDENTIFIER, ANIME_VOSTEN[1], 'Animes (VOSTEN)', 'series.png', oOutputParameterHandler)

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
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenre():
    oGui = cGui()


    liste = []
    liste.append( ['Action', URL_MAIN + 'genres/action/'] )
    liste.append( ['Animation', URL_MAIN + 'genres/animation/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'genres/martiaux/'] )
    liste.append( ['Aventure', URL_MAIN + 'genres/aventure/'] )
    liste.append( ['Biopic', URL_MAIN + 'genres/biographie/'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'genres/dramatique/'] )
    liste.append( ['Comédie Musicale', URL_MAIN + 'genres/musicale/'] )
    liste.append( ['Comédie', URL_MAIN + 'genres/comedie/'] )
    liste.append( ['Divers', URL_MAIN + 'genres/divers/'] )
    liste.append( ['Documentaires', URL_MAIN + 'genres/documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'genres/drame/'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'genres/epouvante/'] )
    liste.append( ['Espionnage', URL_MAIN + 'genres/espionnage/'] )
    liste.append( ['Famille', URL_MAIN + 'genres/famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'genres/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'genres/guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'genres/historique/'] )
    liste.append( ['Musical', URL_MAIN + 'genres/musical/'] )
    liste.append( ['Péplum', URL_MAIN + 'genres/peplum/'] )
    liste.append( ['Policier', URL_MAIN + 'genres/policier/'] )
    liste.append( ['Romance', URL_MAIN + 'genres/romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'genres/science/'] )
    liste.append( ['Thriller', URL_MAIN + 'genres/thriller/'] )
    liste.append( ['Western', URL_MAIN + 'genres/western'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)

        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    ancienAffichage = False
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    Nextpagesearch = oInputParameterHandler.getValue('Nextpagesearch')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    bGlobal_Search = False

    if Nextpagesearch:
        sSearch = sUrl

    if sSearch:

        if URL_SEARCH[0] in sSearch:
            bGlobal_Search = True
            sSearch=sSearch.replace(URL_SEARCH[0], '')

        if Nextpagesearch:
            query_args = (('do', 'search'), ('subaction', 'search'), ('search_start', Nextpagesearch), ('story', sSearch) , ('titleonly', '3'))
        else:
            query_args = (('do', 'search'), ('subaction', 'search'), ('story', sSearch), ('titleonly', '3'))

        #sPattern = '<a href="(.+?)" *><img class=".+?" src="(.+?)".+?\s*<.+?>\s*<div style=".+?">\s*<.+?>\s*<div style=".+?"><div class=".+?">\s*<div class=".+?\s*<a href=".+?" *>(.+?)<'
        sPattern = '<a href="([^"]+)" *><img class="mainimg.+?src="([^"]+)"(?:.|\s)+?<a href=".+?" *>([^"]+)</a>'

        data = urllib.urlencode(query_args)

        oRequestHandler = cRequestHandler(URL_SEARCH[0])
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParametersLine(data)
        oRequestHandler.addParameters('User-Agent', UA)
        oRequestHandler.addParameters('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        oRequestHandler.addParameters('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequestHandler.addParameters('Accept-Encoding','gzip, deflate, br')
        oRequestHandler.addParameters('Referer', URL_MAIN)
        oRequestHandler.addParameters('Content-Type','application/x-www-form-urlencoded')
        sHtmlContent = oRequestHandler.request()
        aResult = oParser.parse(sHtmlContent, sPattern)

    else:
        #sPattern = '<div style="height:[0-9]{3}px;"> *<a href="([^"]+)"><img class="[^"]+?" data-newsid="[^"]+?" src="([^<"]+)".+?<div class="[^"]+?" style="[^"]+?"> *<a href="[^"]+?"> ([^<]+?)<'
        if 'genres' in sUrl:
            sPattern = '<a href="([^"]+)" *><img class="mainimg.+?src="([^"]+)"(?:.|\s)+?<a href=".+?" *>([^"]+)</a>'
        else:
            sPattern = '<a title="([^"]+)" href="([^"]+)"><img class="mainimg".+?src="([^"]+)".+?</a>'

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        sPattern = '<a href="([^"]+)" *><img class="mainimg.+?src="([^"]+)"(?:.|\s)+?<a href=".+?" *>([^"]+)</a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        ancienAffichage = True #Si le site utile l'ancienne affichage

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if sSearch or 'genres' in sUrl or ancienAffichage == True:
                sTitle = aEntry[2]
                sUrl2 = aEntry[0]
                sThumb = aEntry[1]
            else:
                sTitle = aEntry[0]
                sUrl2 = aEntry[1]
                sThumb = aEntry[2]

            #on vire le tiret des series
            sTitle = sTitle.replace(' - Saison', ' Saison').replace('COMPLETE', 'Complete')
            if not '[Complete]' in sTitle:
                sTitle = sTitle.replace('COMPLETE', '[Complete]')
            sDisplayTitle = sTitle.replace('Complete', 'Complète')
            #nettoyage du titre
            sTitle = re.sub('\[\w+]', '', sTitle)

            #traite les qualités
            liste = ['4k', '1080p', '720p', 'bdrip', 'hdrip', 'dvdrip', 'cam-md']
            for i in liste:
                if i in sUrl2:
                    sDisplayTitle = ('%s [%s]') % (sTitle, i.upper())

            #Si recherche et trop de resultat, on nettoye
            #31/12/17 Ne fonctionne plus?
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch, sTitle) == 0:
                    continue

            if not sThumb.startswith('https'):
                sThumb = URL_MAIN + sThumb

            if not sUrl2.startswith('https'):
                sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'series' in sUrl or 'animes' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            elif 'series' in sUrl2 or 'animes' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        if sSearch:
            sPattern = '<a name="nextlink" id="nextlink" onclick="javascript:list_submit\(([0-9]+)\); return\(false\)" href="#">Suivant'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sSearch)
                oOutputParameterHandler.addParameter('Nextpagesearch', aResult[1][0])
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

        else:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if Nextpagesearch:
        oGui.setEndOfDirectory()

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
    #VSlog('mode film')
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #Affichage du texte
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles pour ce film:[/COLOR]')

    #récupération du Synopsis
    sDesc = ''
    try:
        sPattern = '<i>(.+?)</i>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
            sDesc = sDesc.replace('<span>', '').replace('<b><i>', '').replace('</i></b>', '').replace('</span>', '')
            sDesc = sDesc.replace('<br>', ' ').replace('<br /><br />', ' ')
    except:
        pass

    #on recherche d'abord la qualité courante
    sPattern = '<div style=".+?">.+?Qualité (.+?) [|] (.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    sQual = ''
    if (aResult[0]):
        sQual = aResult[1][0]
        sTitle = ('%s [%s]') % (sMovieTitle, sQual)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)

        oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    #on regarde si dispo dans d'autres qualités
    sPattern = '<a href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)<\/b><\/span><span style="color:#.{6}"><b>([^<]+)<\/b><\/span>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = URL_MAIN[:-1] + aEntry[0]
            sQual = aEntry[1]
            sLang = aEntry[2]
            sTitle = ('%s [%s] %s') % (sMovieTitle, sQual, sLang)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showSeriesLinks():
    #VSlog('mode serie')
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #Affichage du texte
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles pour cette saison:[/COLOR]')

    #récupération du Synopsis
    sDesc = ''
    try:
        if 'animes' in sUrl:
            sPattern = '<!--dle_image_end--><br /><br /><br />(.+?)</center>'
        else:
            sPattern = '(?:<br><i>|<p><strong>|<i><span>)([^<]+)(?:</i>|</strong>|</span></i>)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
            sDesc = sDesc.replace('<span>', '').replace('<b><i>', '').replace('</i></b>', '').replace('</span>', '').replace('<br>', ' ')
    except:
        pass

    #Mise àjour du titre
    sPattern = '<title>(?:Télecharger|)(.+?)-(.+?) (.+?) .+?</title>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        if '&raquo; Annuaire Telechargement' in str(aResult[1][0][0]):
            sMovieTitle = aResult[1][0][0].replace('&amp;', '').replace('&raquo; Annuaire Telechargement', '')
        else:
            sMovieTitle = aResult[1][0][0].replace('&amp;', '') + aResult[1][0][1] + ' ' + aResult[1][0][2]

    #on recherche d'abord la qualité courante
    sPattern = '<div style="[^"]+?">.+?Qualité (.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    sQual = ''
    if (aResult[1]):
        sQual = aResult[1][0]

    sDisplayTitle = ('%s [%s]') % (sMovieTitle, sQual.replace('|', ''))

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    #on regarde si dispo dans d'autres qualités
    sHtmlContent1 = CutQual(sHtmlContent)
    sPattern1 = '<a href="([^"]+)"><span class="otherquality"><span style="color:#.{6}"><b>([^<]+)<\/b><\/span><span style="color:#.{6}"><b>([^<]+)<\/b><\/span>'

    aResult1 = oParser.parse(sHtmlContent1, sPattern1)
    #print aResult1

    if (aResult1[0] == True):
        total = len(aResult1[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult1[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = URL_MAIN + 'telecharger-series' + aEntry[0]
            sQual = aEntry[1]
            sLang = aEntry[2]
            sDisplayTitle = ('%s [%s] %s') % (sMovieTitle, sQual, sLang)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    #on regarde si dispo d'autres saisons
    sHtmlContent2 = CutSais(sHtmlContent)
    sPattern2 = '<a href="([^"]+)"><span class="otherquality">([^<]+)<b>([^<]+)<span style="color:#.{6}">([^<]+)<\/span><span style="color:#.{6}">([^<]+)<\/b><\/span>'
    aResult2 = oParser.parse(sHtmlContent2, sPattern2)

    #Affichage du texte
    if (aResult2[0] == True):
        oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Autres Saisons disponibles pour cette série:[/COLOR]')

        for aEntry in aResult2[1]:

            sUrl = URL_MAIN + 'telecharger-series' + aEntry[0]
            sTitle = '[COLOR skyblue]' + aEntry[1] + aEntry[2] + aEntry[3] + aEntry[4] + '[/COLOR]'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    #VSlog('showHosters')
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb=oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()

    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n', ''))
    #fh.close()

    #Fonction pour recuperer uniquement les liens
    #sHtmlContent = Cutlink(sHtmlContent)

    #Si ca ressemble aux lien premiums on vire les liens non premium
    if 'Premium' in sHtmlContent or 'PREMIUM' in sHtmlContent:
        oParser = cParser()
        sPattern = '<font color=red>([^<]+?)</font>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        sHtmlContent = CutNonPremiumlinks(sHtmlContent)

        #print sHtmlContent
    oParser = cParser()

    sPattern = '<font color=red>([^<]+?)</font>|<div style="font-weight:bold.+?">([^>]+?)</div></b><b><a target="_blank" href="([^<>"]+?)">T.+?charger<\/a>|>\[(Liens Premium) \]<|<span style="color:#FF0000">(.+?)</div></b><b><a target="_blank" href=href="https://([^"]+)/([^"]+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                if ('Interchangeables' not in aEntry[0]):
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')

            #elif aEntry[1]:
                #oOutputParameterHandler = cOutputParameterHandler()
                #oOutputParameterHandler.addParameter('siteUrl', sUrl)
                #oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                #oOutputParameterHandler.addParameter('sThumb', sThumb)
                #if 'Télécharger' in aEntry[1]:
                    #oGui.addText(SITE_IDENTIFIER, '[COLOR olive]' + aEntry[1] + '[/COLOR]')
                #else:
                    #oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[1] + '[/COLOR]')

            else:

                sTitle =  sMovieTitle + ' [COLOR coral]' + aEntry[1] + '[/COLOR] '
                URL_DECRYPT = aEntry[3]
                oOutputParameterHandler = cOutputParameterHandler()
                if sUrl.startswith('https'):
                    oOutputParameterHandler.addParameter('siteUrl', aEntry[2])
                else:
                    sUrl2 = 'https://' + aEntry[3] + '/' + aEntry[4]
                    oOutputParameterHandler.addParameter('siteUrl', sUrl2)

                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addMovie(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showSeriesHosters():
    #VSlog('showSeriesHosters')
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb=oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #Fonction pour recuperer uniquement les liens
    #sHtmlContent = Cutlink(sHtmlContent)

    #Pour les series on fait l'inverse des films on vire les liens premiums
    if 'Premium' in sHtmlContent or 'PREMIUM' in sHtmlContent or 'premium' in sHtmlContent:
        sHtmlContent = CutPremiumlinks(sHtmlContent)

    sPattern = '<div style="font-weight:bold;color:[^"]+?">([^<]+)</div>|<a target="_blank" href="https://([^"]+)/([^"]+?)">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                if 'Télécharger' in aEntry[0]:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]' + aEntry[0] + '[/COLOR]')
                else:
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            else:
                sName = aEntry[3]
                sName = sName.replace('Télécharger', '')
                sName = sName.replace('pisodes', 'pisode')
                sUrl2 = 'https://' + aEntry[1] +  '/' + aEntry[2]

                sTitle = sMovieTitle + ' ' + sName
                URL_DECRYPT = aEntry[1]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def Display_protected_link():
    #VSlog('Display_protected_link')
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb=oInputParameterHandler.getValue('sThumb')

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

    #Est ce un lien dl-protect ?
    if URL_DECRYPT in sUrl:
        sHtmlContent = DecryptDlProtecte(sUrl)

        if sHtmlContent:
            #Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotecte = (True, [sHtmlContent])
            else:
                sPattern_dlprotecte = '<div class="lienet"><a href="(.+?)">'
                aResult_dlprotecte = oParser.parse(sHtmlContent, sPattern_dlprotecte)

        else:
            oDialog = dialog().VSok('Erreur décryptage du lien')
            aResult_dlprotecte = (False, False)

    #Si lien normal
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotecte = (True, [sUrl])

    #print aResult_dlprotecte

    if (aResult_dlprotecte[0]):

        episode = 1

        for aEntry in aResult_dlprotecte[1]:
            sHosterUrl = aEntry
            #print sHosterUrl

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
    sPattern = '<h3>Qualit.+?galement disponibles pour cette saison:</h3>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        return aResult[1][0]
    else:
        return sHtmlContent

    return ''

def CutSais(sHtmlContent):
    oParser = cParser()
    sPattern = '<h3>Saisons.+?galement disponibles pour cette saison:</h3>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        return aResult[1][0]
    return ''

def CutNonPremiumlinks(sHtmlContent):
    oParser = cParser()
    sPattern = 'Lien Premium(.+?)Publie le '
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        return aResult[1][0]

    #Si ca marche pas on renvois le code complet
    return sHtmlContent

def CutPremiumlinks(sHtmlContent):
    oParser = cParser()
    sPattern = '(?i) par .{1,2}pisode(.+?)$'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        sHtmlContent = aResult[1][0]

    #Si ca marche pas on renvois le code complet
    return sHtmlContent

def DecryptDlProtecte(url):

    VSlog('DecryptDlProtecte : ' + url)
    dialogs = dialog()

    if not (url):
        return ''
    #VSlog(url)

    # 1ere Requete pour recuperer le cookie
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request()

    cookies = GestionCookie().Readcookie('www_dl-protect1_com')
    #VSlog( 'cookie'  + str(cookies))

    #Tout ca a virer et utiliser oRequestHandler.addMultipartFiled('sess_id':sId,'upload_type':'url','srv_tmp_url':sTmp) quand ca marchera
    import string
    _BOUNDARY_CHARS = string.digits
    boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(15))
    multipart_form_data = {'submit':'continuer','submit':'Continuer'}
    data, headersMulti = encode_multipart(multipart_form_data, {}, boundary)

    #2 eme requete pour avoir le lien
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('Host', 'www.dl-protect1.com')
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

    #fh = open('d:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    return sHtmlContent

#******************************************************************************
#from http://code.activestate.com/recipes/578668-encode-multipart-form-data-for-uploading-files-via/

"""Encode multipart form data to upload files via POST."""

def encode_multipart(fields, files, boundary = None):
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
    import random
    import string

    _BOUNDARY_CHARS = string.digits

    def escape_quote(s):
        return s.replace('"', '\\"')

    if boundary is None:
        boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(15))
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
