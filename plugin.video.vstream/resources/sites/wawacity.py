#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
return False
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, dialog, xbmc, xbmcgui, VSlog
from resources.lib.config import GestionCookie

import re, urllib, urllib2
import random

UA = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

SITE_IDENTIFIER = 'wawacity'
SITE_NAME = '[COLOR violet]Wawacity[/COLOR]'
SITE_DESC = 'Fichier en DDL, HD'

URL_MAIN = 'https://wawacity.ec/'
URL_PROTECT = 'https://wlnk.ec/'

URL_SEARCH = (URL_MAIN + '?search=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
URL_SEARCH_MOVIES = (URL_SEARCH, 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH, 'showMovies')
URL_SEARCH_ANIMES = (URL_SEARCH, 'showMovies')
URL_SEARCH_MANGAS = (URL_SEARCH, 'showMovies')
URL_SEARCH_SPECTACLES = (URL_SEARCH, 'showMovies')

MOVIE_MOVIE = ('http://', 'showMenuMovies')
MOVIE_EXCLU = (URL_MAIN + '?p=films&s=exclus', 'showMovies')
MOVIE_HD = (URL_MAIN + '?p=films&s=blu-ray_1080p-720p', 'showMovies')
MOVIE_3D = (URL_MAIN + '?p=films&s=blu-ray_3d', 'showMovies')
MOVIE_4K = (URL_MAIN + '?p=films&s=ultra-hd-4k', 'showMovies')
MOVIE_ANIMATION = (URL_MAIN + '?p=films&s=dessins_animes', 'showMovies')
MOVIE_BDRIP = (URL_MAIN + '?p=films&s=dvdrip-dbrip', 'showMovies')
MOVIE_BDRIP_MKV = (URL_MAIN + '?p=films&s=dvdrip-hq', 'showMovies')
MOVIE_CAM = (URL_MAIN + '?p=films&s=dvdsrc-r5-ts-cam', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + '?p=films&s=film-vostfr', 'showMovies')
MOVIE_VO = (URL_MAIN + '?p=films&s=_film-vo', 'showMovies')
VIEUX_FILM = (URL_MAIN + '?p=films&s=vieux-films', 'showMovies')
MOVIE_MALENTENDANTS = (URL_MAIN + '?p=films&s=film-sourds-et-malentendants', 'showMovies')
MOVIE_LIST= (URL_MAIN + '?p=films', 'showMovies')
MOVIE_GENRES = (True, 'showGenresMovies')

ANIM_ANIMS = ('http://', 'showMenuMangas')
ANIM_VF = (URL_MAIN + '?p=mangas&s=vf', 'showMovies')
ANIM_VOSTFR = (URL_MAIN + '?p=mangas&s=vostfr', 'showMovies')
ANIM_LIST = (URL_MAIN + '?p=mangas', 'showMovies')
ANIM_GENRES = (True, 'showGenreAnime')

DIVERTISSEMENTS = (URL_MAIN + '?p=autres-videos&s=divertissements', 'showMovies')
SPECTACLES = (URL_MAIN + '?p=autres-videos&s=spectacles', 'showMovies')
DOC_DOCS = (URL_MAIN + '?p=autres-videos&s=documentaires','showMovies')
DIVERS_LIST = (URL_MAIN + '?p=autres-videos','showMovies')
DIVERS_GENRES = (True, 'showGenreDivers')

SERIE_SERIES = ('http://', 'showMenuSeries')
SERIE_VF_SD = (URL_MAIN + '?p=series&s=vf', 'showMovies')
SERIE_VF_HD = (URL_MAIN + '?p=series&s=vf-hq', 'showMovies')
SERIE_VOSTFR_SD = (URL_MAIN + '?p=series&s=vostfr', 'showMovies')
SERIE_VOSTFR_HD = (URL_MAIN + '?p=series&s=vostfr-hq', 'showMovies')
SERIE_LIST = (URL_MAIN + '?p=series', 'showMovies')
SERIE_GENRES = (True, 'showGenreSeries')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Mangas', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuDivers', 'Divers', 'buzz.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovies', 'Recherche de Film', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EXCLU[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EXCLU[1], 'Films Exclus', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (HD)', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Films en 3D', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4K[1], 'Films (4K)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANIMATION[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANIMATION[1], 'Films D\'animation', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIP[1], 'Films (BDRip)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIP_MKV[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIP_MKV[1], 'Films (BDRip MKV)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CAM[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CAM[1], 'Films (Cam)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VO[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VO[1], 'Films (VO)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', VIEUX_FILM[0])
    oGui.addDir(SITE_IDENTIFIER, VIEUX_FILM[1], 'Films ancien', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MALENTENDANTS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MALENTENDANTS[1], 'Films sourds et malentendants', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Liste des films', 'listes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Recherche de Série', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF_SD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VF_SD[1], 'Séries (VF SD)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF_HD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VF_HD[1], 'Séries (VF HD)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFR_SD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFR_SD[1], 'Séries (VOSTFR SD)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFR_HD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFR_HD[1], 'Séries (VOSTFR HD)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Liste des séries', 'listes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMangas', 'Recherche de Manga', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VF[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VF[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFR[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_LIST[1], 'Liste des animés', 'listes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuDivers():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchDivers', 'Recherche Divers', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DIVERTISSEMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, DIVERTISSEMENTS[1], 'Divertissements', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPECTACLES[0])
    oGui.addDir(SITE_IDENTIFIER, SPECTACLES[1], 'Spectacles', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_DOCS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_DOCS[1], 'Documentaire', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DIVERS_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, DIVERS_LIST[1], 'Liste divers', 'listes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DIVERS_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, DIVERS_GENRES[1], 'Divers (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearchMovies():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText + '&p=films'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSearchSeries():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText + '&p=series'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSearchMangas():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText + '&p=mangas'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSearchDivers():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText + '&p=autres-videos'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenresMovies():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + '?p=films&genre=action'] )
    liste.append( ['Animation', URL_MAIN + '?p=films&genre=animation'] )
    liste.append( ['Arts Martiaux', URL_MAIN + '?p=films&genre=arts_martiaux'] )
    liste.append( ['Aventure', URL_MAIN + '?p=films&genre=aventure'] )
    liste.append( ['Biographie', URL_MAIN + '?p=films&genre=biographie'] )
    liste.append( ['Biopic', URL_MAIN + '?p=films&genre=biopic'] )
    liste.append( ['Comédie', URL_MAIN + '?p=films&genre=_comedie'] )
    liste.append( ['Comédie dramatique', URL_MAIN + '?p=films&genre=comedie_dramatique'] )
    liste.append( ['Comédie musicale', URL_MAIN + '?p=films&genre=comedie_musical'] )
    liste.append( ['Documentaire', URL_MAIN + '?p=films&genre=documentaire'] )
    liste.append( ['Drame', URL_MAIN + '?p=films&genre=drame'] )
    liste.append( ['Espionnage', URL_MAIN + '?p=films&genre=espionnage'] )
    liste.append( ['Famille', URL_MAIN + '?p=films&genre=en_famille'] )
    liste.append( ['Fantastique', URL_MAIN + '?p=films&genre=fantastique'] )
    liste.append( ['Guerre', URL_MAIN + '?p=films&genre=guerre'] )
    liste.append( ['Historique', URL_MAIN + '?p=films&genre=historique'] )
    liste.append( ['Horreur', URL_MAIN + '?p=films&genre=horreur-epouvante'] )
    liste.append( ['Musical', URL_MAIN + '?p=films&genre=musical'] )
    liste.append( ['Péplum', URL_MAIN + '?p=films&genre=peplum'] )
    liste.append( ['Policier', URL_MAIN + '?p=films&genre=policier'] )
    liste.append( ['Romance', URL_MAIN + '?p=films&genre=romance'] )
    liste.append( ['Science fiction', URL_MAIN + '?p=films&genre=science-fiction'] )
    liste.append( ['Spectacle', URL_MAIN + '?p=films&genre=spectacle'] )
    liste.append( ['Thriller', URL_MAIN + '?p=films&genre=thriller'] )
    liste.append( ['Western', URL_MAIN + '?p=films&genre=western'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenreSeries():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + '?p=series&genre=action'] )
    liste.append( ['Animation', URL_MAIN + '?p=series&genre=animation'] )
    liste.append( ['Arts Martiaux', URL_MAIN + '?p=series&genre=arts_martiaux'] )
    liste.append( ['Aventure', URL_MAIN + '?p=series&genre=aventure'] )
    liste.append( ['Biographie', URL_MAIN + '?p=series&genre=biographie'] )
    liste.append( ['Biopic', URL_MAIN + '?p=series&genre=biopic'] )
    liste.append( ['Comédie', URL_MAIN + '?p=series&genre=_comedie'] )
    liste.append( ['Comédie dramatique', URL_MAIN + '?p=series&genre=comedie_dramatique'] )
    liste.append( ['Comédie musicale', URL_MAIN + '?p=series&genre=comedie_musical'] )
    liste.append( ['Documentaire', URL_MAIN + '?p=series&genre=documentaire'] )
    liste.append( ['Drame', URL_MAIN + '?p=series&genre=drame'] )
    liste.append( ['Espionnage', URL_MAIN + '?p=series&genre=espionnage'] )
    liste.append( ['Famille', URL_MAIN + '?p=series&genre=en_famille'] )
    liste.append( ['Fantastique', URL_MAIN + '?p=series&genre=fantastique'] )
    liste.append( ['Guerre', URL_MAIN + '?p=series&genre=guerre'] )
    liste.append( ['Historique', URL_MAIN + '?p=series&genre=historique'] )
    liste.append( ['Horreur', URL_MAIN + '?p=series&genre=horreur-epouvante'] )
    liste.append( ['Musical', URL_MAIN + '?p=series&genre=musical'] )
    liste.append( ['Péplum', URL_MAIN + '?p=series&genre=peplum'] )
    liste.append( ['Policier', URL_MAIN + '?p=series&genre=policier'] )
    liste.append( ['Romance', URL_MAIN + '?p=series&genre=romance'] )
    liste.append( ['Science fiction', URL_MAIN + '?p=series&genre=science-fiction'] )
    liste.append( ['Spectacle', URL_MAIN + '?p=series&genre=spectacle'] )
    liste.append( ['Thriller', URL_MAIN + '?p=series&genre=thriller'] )
    liste.append( ['Western', URL_MAIN + '?p=series&genre=western'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenreAnime():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + '?p=mangas&genre=action'] )
    liste.append( ['Arts Martiaux', URL_MAIN + '?p=mangas&genre=arts_martiaux'] )
    liste.append( ['Aventure', URL_MAIN + '?p=mangas&genre=aventure'] )
    liste.append( ['Combat', URL_MAIN + '?p=mangas&genre=combat'] )
    liste.append( ['Comédie', URL_MAIN + '?p=mangas&genre=comedie'] )
    liste.append( ['Cyberpunk', URL_MAIN + '?p=mangas&genre=cyberpunk'] )
    liste.append( ['Dark Fantasy', URL_MAIN + '?p=mangas&genre=dark-fantasy'] )
    liste.append( ['Drame', URL_MAIN + '?p=mangas&genre=drame'] )
    liste.append( ['Ecchi', URL_MAIN + '?p=mangas&genre=ecchi'] )
    liste.append( ['Ecole', URL_MAIN + '?p=mangas&genre=ecole'] )
    liste.append( ['Fantastique', URL_MAIN + '?p=mangas&genre=fantastique'] )
    liste.append( ['Gastronomie', URL_MAIN + '?p=mangas&genre=gastronomie'] )
    liste.append( ['Harem', URL_MAIN + '?p=mangas&genre=_harem'] )
    liste.append( ['Harem Inversé', URL_MAIN + '?p=mangas&genre=harem-inverse'] )
    liste.append( ['Heroic Fantasy', URL_MAIN + '?p=mangas&genre=heroïc-fantasy'] )
    liste.append( ['Historique', URL_MAIN + '?p=mangas&genre=historique'] )
    liste.append( ['Horreur', URL_MAIN + '?p=mangas&genre=horreur'] )
    liste.append( ['Magical Girl', URL_MAIN + '?p=mangas&genre=magical-girl'] )
    liste.append( ['Mature', URL_MAIN + '?p=mangas&genre=mature'] )
    liste.append( ['Mecha', URL_MAIN + '?p=mangas&genre=mecha'] )
    liste.append( ['Musical', URL_MAIN + '?p=mangas&genre=musical'] )
    liste.append( ['Mystère', URL_MAIN + '?p=mangas&genre=mystere'] )
    liste.append( ['Policier', URL_MAIN + '?p=mangas&genre=policier'] )
    liste.append( ['Psychologie', URL_MAIN + '?p=mangas&genre=psychologie'] )
    liste.append( ['Romance', URL_MAIN + '?p=mangas&genre=romance'] )
    liste.append( ['Science Fiction', URL_MAIN + '?p=mangas&genre=science-fiction'] )
    liste.append( ['Space Opera', URL_MAIN + '?p=mangas&genre=space-opera'] )
    liste.append( ['Sport', URL_MAIN + '?p=mangas&genre=sport'] )
    liste.append( ['Steampunk', URL_MAIN + '?p=mangas&genre=steampunk'] )
    liste.append( ['Surnaturel', URL_MAIN + '?p=mangas&genre=surnaturel'] )
    liste.append( ['Suspense', URL_MAIN + '?p=mangas&genre=suspense'] )
    liste.append( ['Tranche de Vie', URL_MAIN + '?p=mangas&genre=tranche-de-vie'] )
    liste.append( ['Thriller', URL_MAIN + '?p=mangas&genre=thriller'] )
    liste.append( ['Tournois', URL_MAIN + '?p=mangas&genre=tournois'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenreDivers():
    oGui = cGui()

    liste = []
    liste.append( ['Actualités', URL_MAIN + '?p=autres-videos&genre=actualites'] )
    liste.append( ['Animaux', URL_MAIN + '?p=autres-videos&genre=animaux'] )
    liste.append( ['Concerts', URL_MAIN + '?p=autres-videos&genre=concerts'] )
    liste.append( ['Emission TV', URL_MAIN + '?p=autres-videos&genre=emissions-tv'] )
    liste.append( ['Géographie', URL_MAIN + '?p=autres-videos&genre=geographie'] )
    liste.append( ['High-tech', URL_MAIN + '?p=autres-videos&genre=high-tech'] )
    liste.append( ['Histoire', URL_MAIN + '?p=autres-videos&genre=histoire'] )
    liste.append( ['Humour', URL_MAIN + '?p=autres-videos&genre=humour'] )
    liste.append( ['Nature', URL_MAIN + '?p=autres-videos&genre=nature'] )
    liste.append( ['Sport', URL_MAIN + '?p=autres-videos&genre=sport'] )
    liste.append( ['Autres', URL_MAIN + '?p=autres-videos&genre=autres'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    bGlobal_Search = False
    if sSearch:

        #par defaut
        sUrl = sSearch.replace(' ', '+')

        if URL_SEARCH[0] in sSearch:
            bGlobal_Search = True

        #partie en test
        oInputParameterHandler = cInputParameterHandler()
        sType = oInputParameterHandler.getValue('type')

        if sType:
            if sType == "film":
                sUrl = sUrl.replace(URL_SEARCH[0], URL_SEARCH_MOVIES[0])
            if sType == "serie":
                sUrl = sUrl.replace(URL_SEARCH[0], URL_SEARCH_SERIES[0])
            if sType == "anime":
                sUrl = sUrl.replace(URL_SEARCH[0], URL_SEARCH_ANIMS[0])

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    #VSlog(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #VSlog(sHtmlContent)

    sQual = ''
    sSaison = ''
    sLang = ''

    if not 'films' in sUrl:
        sPattern = '<a href="([^"]+)"><img alt="([^"]+)" src="([^"]+)" class="img-responsive"></a>'
    else:
        sPattern = '<a href="([^"]+)"><img alt="([^"]+) (\[.+?)" src="([^"]+)" class="img-responsive"></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = URL_MAIN + aEntry[0]

            if not 'films' in sUrl:
                sTitle = aEntry[1].split(' - ')[0]
                sSaison = aEntry[1].split(' - ')[1]
                sLang = aEntry[1].split(' - ')[2].upper()
                sThumb = URL_MAIN + aEntry[2]
                sQual = ''
            else:
                sTitle = aEntry[1]
                # sQual = aEntry[2]
                sQual = aEntry[2].split(' - ')[0]
                sLang = aEntry[2].split(' - ')[1]
                sThumb = URL_MAIN + aEntry[3]

            sDisplayTitle = ('%s %s (%s)') % (sSaison + sTitle, sQual, sLang)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'p=series' in sUrl or 'p=mangas' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'href=\'([^"]+)\' rel=\'next\'>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]

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

    #Affichage du texte
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles pour ce film:[/COLOR]')

    #récupération du Synopsis
    sDesc = ''
    try:
        sPattern = '<p>(.+?)<br /></p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
            sDesc = sDesc.replace('<span>', '').replace('<b><i>', '').replace('</i></b>', '').replace('</span>', '')
            sDesc = sDesc.replace('<br>', ' ').replace('<br /><br />', ' ')
    except:
        pass

    #on recherche d'abord la qualité courante
    sPattern = '<i class="fa fa-folder-open"></i>\s*.+?<i>([^"]+)</i>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sQual = ''
    if (aResult[0]):
        # sQual = aResult[1][0]
        sQual = aResult[1][0].split(' - ')[0]
        sLang = aResult[1][0].split(' - ')[1]
        sTitle = ('%s %s (%s)') % (sMovieTitle, sQual, sLang)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)

        oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    #on regarde si dispo dans d'autres qualités
    sPattern = '<li><a href="([^"]+)"><button class=".+?>([^<]+)<i>([^<]+)</i> <i class=".+?"></i></button></a></li>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = URL_MAIN + aEntry[0]
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
        sPattern = '<p>(.+?)<br /></p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
            sDesc = sDesc.replace('<span>', '').replace('<b><i>', '').replace('</i></b>', '').replace('</span>', '').replace('<br>', ' ')
    except:
        pass

    #Mise àjour du titre
    sPattern = '<title>(?:Télecharger|)(.+?)-(.+?) (.+?) .+?</title>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0]):
        sSaison = aResult[1][0][2]
        sMovieTitle = (aResult[1][0][0].replace('&amp;', '') + aResult[1][0][1] + ' ' + aResult[1][0][2]).replace('Télécharger', '')

    #on recherche d'abord la langue courante
    sPattern = '<i class="fa fa-folder-open"></i>\s*.+?<i>([^"]+)</i>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sLang = ''
    if (aResult[1]):
        sLang = aResult[1][0].replace(' - ', '')

    sDisplayTitle = ('%s [%s]') % (sMovieTitle, sLang.replace('|', ''))

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    #on regarde si dispo dans d'autres langues
    sPattern1 = '<li><a href="([^"]+)"><button class="btn btn-default" style="width:100%">([^"]+)' + sSaison + '<i> - ([^"]+)</i></button></a></li'
    aResult1 = oParser.parse(sHtmlContent, sPattern1)

    if (aResult1[0] == True):
        total = len(aResult1[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult1[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = URL_MAIN + aEntry[0]
            sQual = ''
            sLang = aEntry[2]
            sDisplayTitle = ('%s [%s] (%s)') % (sMovieTitle, sQual, sLang)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    #on regarde si dispo d'autres saisons
    sPattern2 = '<li><a href="([^"]+)"><button class="btn btn-default" style="width:100%">([^"]+)((?!' + sSaison + ').)<i> -([^"]+)</i></button></a></li'
    aResult2 = oParser.parse(sHtmlContent, sPattern2)

    #Affichage du texte
    if (aResult2[0] == True):
        oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Autres Saisons disponibles pour cette série:[/COLOR]')

        for aEntry in aResult2[1]:

            sUrl = URL_MAIN + aEntry[0]
            sTitle = '[COLOR skyblue]' + aEntry[1] + aEntry[2] + aEntry[3] + '[/COLOR]'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
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
    #VSlog(sHtmlContent)

    oParser = cParser()

    sPattern = '<a rel="external nofollow" href="([^"]+)" target="_blank" class="link">\s*<.+?a>\s*</td>\s*.+?>(.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle =  sMovieTitle + ' [COLOR coral]' + aEntry[1] + '[/COLOR] '
            sUrl = aEntry[0]
            oOutputParameterHandler = cOutputParameterHandler()

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
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

    sPattern = '<p>.+?</i> - (.+?)<span class="pull-right">|<a rel="external nofollow" href="([^"]+)" target="_blank" class="link">\s*<.+?b>.+?\s*</a>\s*<.+?>\s*<.+?>([^"]+)</td>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')

            sTitle = sMovieTitle + ' ' + aEntry[2]
            sUrl2 = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def Display_protected_link():
    #print 'entering Display_protected_link'
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    #Est ce un lien dl-protect ?
    if URL_PROTECT in sUrl:
        sHtmlContent = DecryptddlProtect(sUrl)

        if sHtmlContent:
            #Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotect = (True, [sHtmlContent])
            else:
                sPattern_dlprotect = '<a href="([^<]+)" rel="external nofollow">'
                aResult_dlprotect = oParser.parse(sHtmlContent, sPattern_dlprotect)

        else:
            oDialog = dialog().VSok('Désolé, problème de captcha.\n Veuillez en rentrer un directement sur le site, le temps de réparer')
            aResult_dlprotect = (False, False)

    #Si lien normal
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotect = (True, [sUrl])

    if (aResult_dlprotect[0]):
        for aEntry in aResult_dlprotect[1]:
            sHosterUrl = aEntry

            sTitle = sMovieTitle

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def DecryptddlProtect(url):
    #print 'entering DecryptddlProtect'
    if not (url): return ''

    #Get host
    tmp = url.split('/')
    host = tmp[0] + '//' + tmp[2] + '/'
    #VSlog(host)

    cookies = ''
    dialogs = dialog()
    #try to get previous cookie
    cookies = GestionCookie().Readcookie('wawacity')

    oRequestHandler = cRequestHandler(url)
    if cookies:
        oRequestHandler.addHeaderEntry('Cookie', cookies)
    sHtmlContent = oRequestHandler.request()
    #VSlog(sHtmlContent)

    #A partir de la on a les bon cookies pr la protection cloudflare

    #Si ca demande le captcha
    if 'Recopiez :' in sHtmlContent:
        if cookies:
            GestionCookie().DeleteCookie('wawacity')
            oRequestHandler = cRequestHandler(url)
            sHtmlContent = oRequestHandler.request()

        s = re.findall('<label for=".+? >.+?</label><img src="(.+?)"', sHtmlContent)
        if host in s[0]:
            image = s[0]
        else:
            image = host + s[0]

        captcha,cookies2 = get_response(image, cookies)
        cookies = cookies + '; ' + cookies2

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('Cookie', cookies)
        oRequestHandler.addHeaderEntry('Referer', url)

        oRequestHandler.addParameters('submit', 'unlock')
        oRequestHandler.addParameters('cr-nvar', captcha.upper())

        sHtmlContent = oRequestHandler.request()

        if 'Code de securite incorrect' in sHtmlContent:
            dialogs.VSinfo("Mauvais Captcha")
            return 'rate'

        if 'Veuillez recopier le captcha ci-dessus' in sHtmlContent:
            dialogs.VSinfo("Rattage")
            return 'rate'

        #si captcha reussi
        #save cookies
        GestionCookie().SaveCookie('wawacity', cookies)

    return sHtmlContent

def get_response(img,cookie):
    #on telecharge l'image
    import xbmcvfs

    dialogs = dialog()

    filename = "special://home/userdata/addon_data/plugin.video.vstream/Captcha.raw"
    #PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile"))
    #filename  = os.path.join(PathCache, 'Captcha.raw')

    hostComplet = re.sub(r'(https*:\/\/[^/]+)(\/*.*)', '\\1', img)
    host = re.sub(r'https*:\/\/', '', hostComplet)
    url = img

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent' , UA)
    #oRequestHandler.addHeaderEntry('Referer', url)
    oRequestHandler.addHeaderEntry('Cookie', cookie)

    htmlcontent = oRequestHandler.request()

    NewCookie = oRequestHandler.GetCookies()

    downloaded_image = xbmcvfs.File(filename, 'wb')
    #downloaded_image = file(filename, "wb")
    downloaded_image.write(htmlcontent)
    downloaded_image.close()

#on affiche le dialogue
    solution = ''

    if (True):
        ####nouveau captcha
        try:
            ##affichage du dialog perso
            class XMLDialog(xbmcgui.WindowXMLDialog):
                #"""
                #Dialog class for captcha
                #"""
                def __init__(self, *args, **kwargs):
                    xbmcgui.WindowXMLDialog.__init__(self)
                    pass

                def onInit(self):
                    #image background captcha
                    self.getControl(1).setImage(filename.encode("utf-8"), False)
                    #image petit captcha memory fail
                    self.getControl(2).setImage(filename.encode("utf-8"), False)
                    self.getControl(2).setVisible(False)
                    ##Focus clavier
                    self.setFocus(self.getControl(21))

                def onClick(self, controlId):
                    if controlId == 20:
                        #button Valider
                        solution = self.getControl(5000).getLabel()
                        xbmcgui.Window(10101).setProperty('captcha', solution)
                        self.close()
                        return

                    elif controlId == 30:
                        #button fermer
                        self.close()
                        return

                    elif controlId == 21:
                        #button clavier
                        self.getControl(2).setVisible(True)
                        kb = xbmc.Keyboard(self.getControl(5000).getLabel(), '', False)
                        kb.doModal()

                        if (kb.isConfirmed()):
                            self.getControl(5000).setLabel(kb.getText())
                            self.getControl(2).setVisible(False)
                        else:
                            self.getControl(2).setVisible(False)

                def onFocus(self, controlId):
                    self.controlId = controlId

                def _close_dialog(self):
                    self.close()

                def onAction(self, action):
                    #touche return 61448
                    if action.getId() in (9, 10, 11, 30, 92, 216, 247, 257, 275, 61467, 61448):
                        self.close()

            path = "special://home/addons/plugin.video.vstream"
            #path = cConfig().getAddonPath().decode("utf-8")
            wd = XMLDialog('DialogCaptcha.xml', path, 'default', '720p')
            wd.doModal()
            del wd
        finally:

            solution = xbmcgui.Window(10101).getProperty('captcha')
            if solution == '':
                dialogs.VSinfo("Vous devez taper le captcha")

    else:
        #ancien Captcha
        try:
            img = xbmcgui.ControlImage(450, 0, 400, 130, filename.encode("utf-8"))
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
            #xbmc.sleep(3000)
            kb = xbmc.Keyboard('', 'Tapez les Lettres/chiffres de l\'image', False)
            kb.doModal()
            if (kb.isConfirmed()):
                solution = kb.getText()
                if solution == '':
                    dialogs.VSinfo("Vous devez taper le captcha")
            else:
                dialogs.VSinfo("Vous devez taper le captcha")
        finally:
            wdlg.removeControl(img)
            wdlg.close()

    return solution, NewCookie
