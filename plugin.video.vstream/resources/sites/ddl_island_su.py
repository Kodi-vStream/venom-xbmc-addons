#-*- coding: utf-8 -*-

from resources.lib.config import cConfig
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

from resources.lib.config import GestionCookie

import re, urllib2
import xbmcgui
import xbmc
import xbmcaddon, os

UA = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

SITE_IDENTIFIER = 'ddl_island_su'
SITE_NAME = '[COLOR violet]DDL-Island[/COLOR]'
SITE_DESC = 'Fichier en DDL, HD'

URL_MAIN = 'http://www.ddl-island.su/'
URL_PROTECT = 'http://protect.ddl-island.su'

URL_SEARCH_MOVIES = (URL_MAIN + 'recherche.php?categorie=99&rechercher=Rechercher&fastr_type=ddl&find=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'recherche.php?categorie=98&rechercher=Rechercher&fastr_type=ddl&find=', 'showMovies')

URL_SEARCH_ANIMES = (URL_MAIN + 'recherche.php?categorie=5&rechercher=Rechercher&fastr_type=ddl&find=', 'showMovies')
URL_SEARCH_MANGAS = (URL_MAIN + 'recherche.php?categorie=3&rechercher=Rechercher&fastr_type=ddl&find=', 'showMovies')
URL_SEARCH_EMISSIONS_TV = (URL_MAIN + 'recherche.php?categorie=17&rechercher=Rechercher&fastr_type=ddl&find=', 'showMovies')
URL_SEARCH_SPECTACLES = (URL_MAIN + 'recherche.php?categorie=2&rechercher=Rechercher&fastr_type=ddl&find=', 'showMovies')

URL_SEARCH = (URL_MAIN + 'index.php?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_SD = (URL_MAIN + 'telechargement/films-1.html&order=2', 'showMovies') # derniers films en SD
MOVIE_HD = (URL_MAIN + 'telechargement/films-hd-13.html&order=2', 'showMovies') # derniers films en HD
MOVIE_3D = (URL_MAIN + 'telechargement/films-3d-21.html&order=2', 'showMovies') # derniers films en 3D
MOVIE_SD_VIEWS = (URL_MAIN + 'telechargement/films-1.html&order=3', 'showMovies') # derniers films en SD
MOVIE_HD_VIEWS = (URL_MAIN + 'telechargement/films-hd-13.html&order=3', 'showMovies') # derniers films en HD
MOVIE_3D_VIEWS = (URL_MAIN + 'telechargement/films-3d-21.html&order=3', 'showMovies') # derniers films en 3D
MOVIE_TOP = (URL_MAIN +'telechargement-top-films', 'showMovies') # derniers films en 3D
MOVIE_GENRES_HD = (True, 'showGenreMoviesHD')
MOVIE_GENRES_SD = (True, 'showGenreMoviesSD')

ANIMES = (URL_MAIN + 'telechargement/dessins-animes-5.html&order=2', 'showMovies') # derniers dessins animés

MANGAS = (URL_MAIN + 'telechargement/mangas-3.html&order=2', 'showMovies') # derniers dessins animés

EMISSIONS_TV = (URL_MAIN + 'telechargement/emissions-tv-17.html&order=2', 'showMovies') # dernieres émissions TV

SPECTACLES = (URL_MAIN + 'telechargement/comedies-spectacles-2.html&order=2', 'showMovies') # dernieres émissions TV

SERIES_SD = (URL_MAIN + 'telechargement/series-tv-6.html&order=2', 'showMovies') # derniers films en SD
SERIES_HD = (URL_MAIN + 'telechargement/series-hd-20.html&order=2', 'showMovies') # derniers films en HD
SERIES_SD_VIEWS = (URL_MAIN + 'telechargement/series-tv-6.html&order=3', 'showMovies') # derniers films en SD
SERIES_HD_VIEWS = (URL_MAIN + 'telechargement/series-tv-6.html&order=3', 'showMovies') # derniers films en HD
SERIES_TOP = (URL_MAIN +'telechargement-top-series', 'showMovies') # derniers films en 3D
SERIES_GENRES_SD = (True, 'showGenreSeriesSD')
SERIES_GENRES_HD = (True, 'showGenreSeriesHD')

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
    oGui.addDir(SITE_IDENTIFIER, 'showMenuDessinsAnimes', 'Dessins Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Mangas', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSpectacles', 'Spectacles', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuEmissionsTV', 'Emissions TV', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuFilms():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovies', 'Recherche de films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD[1], 'Films SD (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films HD (Derniers ajouts)', 'films_hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Films en 3D (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_VIEWS[1], 'Films SD (Les plus vus)', 'films_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD_VIEWS[1], 'Films HD (Les plus vus)', 'films_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D_VIEWS[1], 'Films 3D (Les plus vus)', 'films_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP[1], 'Films (Top du Mois)', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES_SD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES_SD[1], 'Films SD (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES_HD[1], 'Films HD (Genres)', 'films_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Recherche de séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_SD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_SD[1], 'Séries SD (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_HD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_HD[1], 'Séries HD (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_SD_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_SD_VIEWS[1], 'Séries SD (Les plus vues)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_HD_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_HD_VIEWS[1], 'Séries HD (Les plus vues)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_TOP[1], 'Séries (Top du Mois)', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_GENRES_SD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_GENRES_SD[1], 'Séries SD (Genres)', 'series_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIES_GENRES_HD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIES_GENRES_HD[1], 'Séries HD (Genres)', 'series_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuDessinsAnimes():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchAnimes', 'Recherche de Dessins Animés', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIMES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIMES[1], 'Dessins Animés (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMangas', 'Recherche de Mangas', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MANGAS[0])
    oGui.addDir(SITE_IDENTIFIER, MANGAS[1], 'Mangas (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuSpectacles():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSpectacles', 'Recherche de Spectacles', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPECTACLES[0])
    oGui.addDir(SITE_IDENTIFIER, SPECTACLES[1], 'Spectacles (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuEmissionsTV():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchEmissionsTV', 'Recherche d\'émissions TV', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', EMISSIONS_TV[0])
    oGui.addDir(SITE_IDENTIFIER, EMISSIONS_TV[1], 'Emissions TV (Derniers ajouts)', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearchMovies():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSearchSeries():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH_SERIES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSearchAnimes():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH_ANIMES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSearchMangas():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH_MANGAS[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSearchSpectacles():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH_SPECTACLES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSearchEmissionsTV():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH_EMISSIONS_TV[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenreMoviesSD():
    showGenres("films-1.html&order=2")

def showGenreMoviesHD():
    showGenres("films-hd-13.html&order=2")

def showGenreSeriesSD():
    showGenres("series-tv-6.html")

def showGenreSeriesHD():
    showGenres("series-hd-20.html")

def showGenres(basePath):
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN + 'telechargement+5/' + basePath] )
    liste.append( ['Animation',URL_MAIN + 'telechargement+4/' + basePath] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'telechargement+64/' + basePath] )
    liste.append( ['Aventure',URL_MAIN + 'telechargement+20/' + basePath] )
    liste.append( ['Biographie',URL_MAIN + 'telechargement+38/' + basePath] )
    liste.append( ['Biopic',URL_MAIN + 'telechargement+28/' + basePath] )
    liste.append( ['Combat',URL_MAIN + 'telechargement+35/' + basePath] )
    liste.append( ['Comédie',URL_MAIN + 'telechargement+1/' + basePath] )
    liste.append( ['Comédie dramatique',URL_MAIN + 'telechargement+12/' + basePath] )
    liste.append( ['Comédie musicale',URL_MAIN + 'telechargement+33/' + basePath] )
    liste.append( ['Comédie romantique',URL_MAIN + 'telechargement+53/' + basePath] )
    liste.append( ['Comique',URL_MAIN + 'telechargement+51/' + basePath] )
    liste.append( ['Court métrage',URL_MAIN + 'telechargement+45/' + basePath] )
    liste.append( ['Criminalité',URL_MAIN + 'telechargement+40/' + basePath] )
    liste.append( ['Dessin animé',URL_MAIN + 'telechargement+27/' + basePath] )
    liste.append( ['Divers',URL_MAIN + 'telechargement+34/' + basePath] )
    liste.append( ['Divertissement',URL_MAIN + 'telechargement+66/' + basePath] )
    liste.append( ['Documentaire',URL_MAIN + 'telechargement+9/' + basePath] )
    liste.append( ['Drame',URL_MAIN + 'telechargement+3/' + basePath] )
    liste.append( ['Epouvante',URL_MAIN + 'telechargement+41/' + basePath] )
    liste.append( ['Epouvante-horreur',URL_MAIN + 'telechargement+17/' + basePath] )
    liste.append( ['Erotique',URL_MAIN + 'telechargement+24/' + basePath] )
    liste.append( ['Espionnage',URL_MAIN + 'telechargement+13/' + basePath] )
    liste.append( ['Famille',URL_MAIN + 'telechargement+31/' + basePath] )
    liste.append( ['Fantastique',URL_MAIN + 'telechargement+16/' + basePath] )
    liste.append( ['Football',URL_MAIN + 'telechargement+32/' + basePath] )
    liste.append( ['Guerre',URL_MAIN + 'telechargement+22/' + basePath] )
    liste.append( ['Historique',URL_MAIN + 'telechargement+21/' + basePath] )
    liste.append( ['Horreur',URL_MAIN + 'telechargement+15/' + basePath] )
    liste.append( ['Humour',URL_MAIN + 'telechargement+44/' + basePath] )
    liste.append( ['Jeunesse',URL_MAIN + 'telechargement+19/' + basePath] )
    liste.append( ['Judiciaire',URL_MAIN + 'telechargement+67/' + basePath] )
    liste.append( ['Karaté',URL_MAIN + 'telechargement+23/' + basePath] )
    liste.append( ['Manga',URL_MAIN + 'telechargement+58/' + basePath] )
    liste.append( ['Médical',URL_MAIN + 'telechargement+47/' + basePath] )
    liste.append( ['Musical',URL_MAIN + 'telechargement+10/' + basePath] )
    liste.append( ['Mystère',URL_MAIN + 'telechargement+26/' + basePath] )
    liste.append( ['Péplum',URL_MAIN + 'telechargement+54/' + basePath] )
    liste.append( ['Policier',URL_MAIN + 'telechargement+2/' + basePath] )
    liste.append( ['Reportage',URL_MAIN + 'telechargement+57/' + basePath] )
    liste.append( ['Romance',URL_MAIN + 'telechargement+6/' + basePath] )
    liste.append( ['Science fiction',URL_MAIN + 'telechargement+7/' + basePath] )
    liste.append( ['Sketches',URL_MAIN + 'telechargement+14/' + basePath] )
    liste.append( ['Spectacle',URL_MAIN + 'telechargement+39/' + basePath] )
    liste.append( ['Sport',URL_MAIN + 'telechargement+68/' + basePath] )
    liste.append( ['Suspense',URL_MAIN + 'telechargement+42/' + basePath] )
    liste.append( ['Téléréalité',URL_MAIN + 'telechargement+18/' + basePath] )
    liste.append( ['Thriller',URL_MAIN + 'telechargement+8/' + basePath] )
    liste.append( ['Western',URL_MAIN + 'telechargement+11/' + basePath] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def getIdFromUrl(sUrl):
    sPattern = "\/(telechargemen.+?\/)"
    oParser = cParser()
    aResult = oParser.parse(sUrl, sPattern)
    if (aResult[0] == True):
       return aResult[1][0]
    return

def showMovies(sSearch = ''):
    oGui = cGui()
    bGlobal_Search = False
    if sSearch:

        #par defaut
        sUrl = sSearch

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

    #print sUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #print sHtmlContent
    sDesc = ''
    sQual = ''
    sSaison = ''
    sLang = ''
    #sEpisode = ''
    if 'top' in sUrl:
        sPattern = '<div class="fiche_top20"><a class="top20" href="([^"]+)"><img src="([^"]+)" title="([^\|]+)\|\|[^\|]+?\|\|([^\|]+)\|\|[^\|]+?\|\|([^"]+)" /></a></div>'
    else:
        sPattern = '<div class="fiche_listing"><a href="([^"]+)"><img src="([^"]+)" alt="Télécharger([^"]+)"[^\|]+?\| *Qualité : ([^<]+)<br /><br />([^<]+)<br /><br />'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            if ('-films-' in sUrl2) or ('-series-' in sUrl2):
                sQual = '(SD)'
                if '-hd-' in aEntry[0]:
                    sQual = '(HD)'
                if '-3d-' in aEntry[0]:
                    sQual = '(3D)'
            else:
                sQual = '(' + aEntry[3] + ')'
            sDesc = str(aEntry[4])
            sTitle = str(aEntry[2])
            #print sUrl2
            #sFanart =aEntry[1]
            sThumb = aEntry[1]
            #Reformatage sDisplayTitle
            sSaison = ''
            sLang = ''
            #sEpisode = ''
            sTitle2 = sTitle.split(" - ")
            sTitle = sTitle2[0]
            if 'top' in sUrl:
                sTitle = ' ' + sTitle2[0]
            #on vire le titre pour rechercher saison dans sTitle2
            del sTitle2[0]
            a = filter(lambda x: 'Saison' in x, sTitle2)
            if a:
                sSaison = a[0]
                sSaison = sSaison.replace('Saison ', 'S')
            if 'VOSTFR' in sTitle2:
                sLang = '[VOSTFR]'
            #Temp test
            sDisplayTitle = '%s %s %s %s' %(sSaison, sTitle, sLang, sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if 'series' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesReleases', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesReleases', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    #tPassage en mode vignette sauf en cas de recherche globale
    # if not bGlobal_Search:
        # xbmc.executebuiltin('Container.SetViewMode(500)')

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oParser = cParser()
    sPattern = '<div class="page">.+?</div></td><td align="center"><a href="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        #print aResult
        if 'recherche.php' in aResult[1][0]:
            return URL_MAIN + aResult[1][0]
        else:
            id = getIdFromUrl(sUrl)
            return URL_MAIN + id + aResult[1][0]

    return False

def showMoviesReleases():
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sUrl = sUrl.replace('.html','')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oGui = cGui()

    oParser = cParser()
    #cut de la zone des releases
    sPattern = 'Toutes</option>(.+?)>Hébergeur'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sHtmlContent = aResult[1][0]

    sPattern = '<option value="([^"]+)"  id="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    #Affichage du menu
    #oGui.addText(SITE_IDENTIFIER,sMovieTitle)
    #oGui.addText2(SITE_IDENTIFIER,'[COLOR olive]Releases disponibles pour ce film :[/COLOR]')

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            if ('rapidgator' not in aEntry[1]) and ('turbobit' not in aEntry[1]) and ('uploaded' not in aEntry[1]) and ('uptobox' not in aEntry[1]):
                #sTitle = '[COLOR skyblue]' + aEntry[1] + '[/COLOR]'
                sTitle = str(aEntry[1])

                sTitle = sTitle.decode("iso-8859-1",'ignore')
                sTitle = sTitle.encode("utf-8",'ignore')

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

            cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showSaisons():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    oParser = cParser()
    sPattern = "<li><a[^<>]+Saison[^<>]+?href='([^']+)'>([^<>]+)<\/a><\/li>"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[1]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addTV(SITE_IDENTIFIER, 'showSeriesReleases', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showSeriesReleases():
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sUrl = sUrl.replace('.html','')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oGui = cGui()

    oParser = cParser()
    #cut de la zone des releases
    sPattern = 'Episode :</span>(.+?)>Hébergeur :'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]==False:
        sPattern = 'Release :</span>(.+?)>Hébergeur :'
        aResult = oParser.parse(sHtmlContent, sPattern)
    sHtmlContent = aResult[1][0]

    sPattern = '<option value="([^"]+)"  id="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    #Affichage du menu
    oGui.addText(SITE_IDENTIFIER,sMovieTitle)
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Episodes disponibles :[/COLOR]')

    #Affichage des autres saisons
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl + '.html')
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oOutputParameterHandler.addParameter('sDesc', sDesc)
    oGui.addMisc(SITE_IDENTIFIER, 'showSaisons', "[COLOR olive]Autres saisons >[/COLOR]", '', sThumb, '',oOutputParameterHandler)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            if ('rapidgator' not in aEntry[1]) and ('turbobit' not in aEntry[1]) and ('uploaded' not in aEntry[1]) and ('uptobox' not in aEntry[1]) :
                sTitle = '[COLOR skyblue]' + aEntry[1] + '[/COLOR]'
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb=oInputParameterHandler.getValue('sThumb')

    #print sUrl
    sUrl = sUrl.replace(' & ','+%26+').replace(' ','+')
    #print sUrl
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #print sHtmlContent
    oParser = cParser()

    sPattern = '<span class=\'providers.+?\' title=\'([^\']+)\'>.+?<a href=\'([^\']+)\' target=\'_blank\' title="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            #sTitle = '[COLOR skyblue]' + aEntry[0] + '[/COLOR] ' + sMovieTitle
            sTitle = '%s (%s)' %(sMovieTitle, aEntry[0])
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def Display_protected_link():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb=oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    sUrl = sUrl.replace(URL_PROTECT,URL_PROTECT + '/other?id=')
    #print sUrl
    #xbmc.log(sUrl)

    #Est ce un lien dl-protect ?
    if URL_PROTECT in sUrl:
        sHtmlContent = DecryptddlProtect(sUrl)
        #print sHtmlContent
        if sHtmlContent:
            #Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotect = (True, [sHtmlContent])
            else:
                sPattern_dlprotect = 'Lien :</b></td><td><a href="(.+?)"'
                aResult_dlprotect = oParser.parse(sHtmlContent, sPattern_dlprotect)

        else:
            oDialog = cConfig().createDialogOK('Désolé, problème de captcha.\n Veuillez en rentrer un directement sur le site, le temps de réparer')
            aResult_dlprotect = (False, False)

    #Si lien normal
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotect = (True, [sUrl])

    #print aResult_dlprotect

    if (aResult_dlprotect[0]):

        episode = 1

        for aEntry in aResult_dlprotect[1]:
            sHosterUrl = aEntry
            #print sHosterUrl

            sTitle = sMovieTitle
            if len(aResult_dlprotect[1]) > 1:
                sTitle = sMovieTitle + ' episode ' + str(episode)

            episode+=1

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def DecryptddlProtect(url):

    if not (url): return ''

    cookies = ''
    #try to get previous cookie
    cookies = GestionCookie().Readcookie('protect_ddl_island.su')

    oRequestHandler = cRequestHandler(url)
    if cookies:
        oRequestHandler.addHeaderEntry('Cookie', cookies)
    sHtmlContent = oRequestHandler.request()

    #Si ca demande le captcha
    if 'value="Submit form"' in sHtmlContent:
        if cookies:
            GestionCookie().DeleteCookie('protect_ddl_island.su')
            oRequestHandler = cRequestHandler(url)
            sHtmlContent = oRequestHandler.request()

        cookies = oRequestHandler.GetCookies()

        #save cookies
        GestionCookie().SaveCookie('protect_ddl_island.su', cookies)

        s = re.findall('<img id="captcha" src="([^<>"]+?)"', sHtmlContent)
        if URL_PROTECT in s[0]:
            image = s[0]
        else:
            image = URL_PROTECT + s[0]

        captcha = get_response(image,cookies)
        id = url[-7:]

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addParameters( 'captcha_code' , captcha)
        oRequestHandler.addParameters( 'submit' , 'Valider')
        oRequestHandler.addHeaderEntry('Cookie', cookies)
        sHtmlContent = oRequestHandler.request()

        #print sHtmlContent
        if 'Erreur : Le code n\'est pas valide' in sHtmlContent:
            cConfig().showInfo("Erreur", 'Mauvais Captcha' , 5)
            return 'rate'

        #si captcha reussi
        #save cookies
        GestionCookie().SaveCookie('protect_ddl_island.su', cookies)

    return sHtmlContent

def get_response(img, cookie):
    #on telecharge l'image
    PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile"))
    filename  = os.path.join(PathCache,'Captcha.raw').decode("utf-8")

    headers2 = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
        #'Referer' : url ,
        'Host' : 'protect.ddl-island.su',
        'Accept' : 'image/png,image/*;q=0.8,*/*;q=0.5',
        'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
        'Accept-Encoding' : 'gzip, deflate',
        #'Content-Type' : 'application/x-www-form-urlencoded',
        'Cookie' : cookie
        }

    try:
        req = urllib2.Request(img,None,headers2)
        image_on_web = urllib2.urlopen(req)
        if image_on_web.headers.maintype == 'image':
            buf = image_on_web.read()
            downloaded_image = file(filename, "wb")
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        else:
            return ''
    except:
        return ''

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
                        xbmcgui.Window(10101).setProperty('captcha', str(solution))
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
                    if action.getId() in ( 9, 10, 11, 30, 92, 216, 247, 257, 275, 61467, 61448):
                        self.close()

            wd = XMLDialog('DialogCaptcha.xml', cConfig().getAddonPath().decode("utf-8"), 'default', '720p')
            wd.doModal()
            del wd
        finally:

            solution = xbmcgui.Window(10101).getProperty('captcha')
            if solution == '':
                cConfig().showInfo("Erreur", 'Vous devez taper le captcha' , 4)

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
                    cConfig().showInfo("Erreur", 'Vous devez taper le captcha' , 4)
            else:
                cConfig().showInfo("Erreur", 'Vous devez taper le captcha' , 4)
        finally:
            wdlg.removeControl(img)
            wdlg.close()

    return solution
