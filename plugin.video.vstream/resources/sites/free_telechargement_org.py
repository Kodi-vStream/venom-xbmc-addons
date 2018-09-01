#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.cloudflare import CloudflareBypass
from resources.lib.cloudflare import NoRedirection
from resources.lib.config import GestionCookie
from resources.lib.comaddon import progress, dialog, xbmc, xbmcgui

import re

UA = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

SITE_IDENTIFIER = 'free_telechargement_org'
SITE_NAME = '[COLOR violet]Free-Téléchargement[/COLOR]'
SITE_DESC = 'Fichiers en DDL, HD, Films, Séries, Mangas Etc...'

URL_MAIN = 'http://www.free-telechargement.co/'
URL_PROTECT = 'http://liens.free-telechargement.'

#URL_SEARCH_MOVIES_SD = (URL_MAIN + '1/recherche/1.html?rech_cat=video&rech_fiche=', 'showMovies')
#URL_SEARCH_MOVIES_HD = (URL_MAIN + '1/recherche/1.html?rech_cat=Films+HD&rech_fiche=', 'showMovies')

#URL_SEARCH_SERIE_SD = (URL_MAIN + '1/recherche1/1.html?rech_cat=serie&rech_fiche=', 'showMovies')
#URL_SEARCH_SERIE_HD = (URL_MAIN + '1/recherche1/1.html?rech_cat=seriehd&rech_fiche=', 'showMovies')
URL_SEARCH_EMISSIONS_TV = (URL_MAIN, 'showMovies')
URL_SEARCH_SPECTACLES = (URL_MAIN, 'showMovies')
URL_SEARCH = (URL_MAIN + '1/recherche/1.html?rech_fiche=', 'showSearchResult')
URL_SEARCH_MOVIES = (URL_MAIN + '1/recherche/1.html?rech_fiche=', 'showSearchResult')
URL_SEARCH_SERIES = (URL_MAIN + '1/recherche/1.html?rech_fiche=', 'showSearchResult')
FUNCTION_SEARCH = 'showSearchResult'

MOVIE_SD_DVDRIP = (URL_MAIN + '1/categorie-Films+DVDRiP+et+BDRiP/1.html', 'showMovies')
MOVIE_SD_CAM = (URL_MAIN + '1/categorie-Films+CAM+TS+R5+et+DVDSCR/1.html', 'showMovies')
MOVIE_SD_VOSTFR = (URL_MAIN + '1/categorie-Films+VOSTFR+et+VO/1.html', 'showMovies')
MOVIE_SD_CLASSIQUE = (URL_MAIN + '1/categorie-Films+Classiques/1.html', 'showMovies')
MOVIE_SD_VIEWS = (URL_MAIN + '1/films/affichage', 'showMovies')
MOVIE_GENRES_SD = (True, 'showGenreMoviesSD')
MOVIE_HD = (URL_MAIN + '1/categorie-Films+BluRay+720p+et+1080p/1.html', 'showMovies')
MOVIE_HDLIGHT = (URL_MAIN + '1/films-hdlight/1.html', 'showMovies')
MOVIE_3D = (URL_MAIN + '1/categorie-Films+BluRay+3D/1.html', 'showMovies')
MOVIE_HD_VIEWS = (URL_MAIN + '1/films-bluray/affichage', 'showMovies')
MOVIE_GENRES_HD = (True, 'showGenreMoviesHD')
MOVIE_ANNEES = (True, 'showMovieYears')

ANIM_ANIMS = (URL_MAIN + '1/animations/1', 'showMovies')
ANIM_VFS = (URL_MAIN + '1/categorie-Mangas+VF/1.html', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + '1/categorie-Mangas+VOST/1.html', 'showMovies')

EMISSIONS_TV = (URL_MAIN + '1/categorie-Emissions/1.html', 'showMovies')

SPECTACLES = (URL_MAIN + '1/categorie-Spectacles/1.html', 'showMovies')

SERIE_SD_EN_COURS_VF = (URL_MAIN + '1/categorie-Saisons+en+cours+VF+/1.html', 'showMovies')
SERIE_SD_EN_COURS_VOSTFR = (URL_MAIN + '1/categorie-Saisons+en+cours+VOST/1.html', 'showMovies')
SERIE_SD_TERMINE_VF = (URL_MAIN + '1/categorie-Saison+Terminée+VF/1.html', 'showMovies')
SERIE_SD_TERMINE_VOSTFR = (URL_MAIN + '1/categorie-Saison+Terminée+VOST/1.html', 'showMovies')
SERIE_HD_EN_COURS_VF = (URL_MAIN + '1/categorie-Saisons+en+cours+VF+HD/1.html', 'showMovies')
SERIE_HD_EN_COURS_VOSTFR = (URL_MAIN + '1/categorie-Saisons+en+cours+VOST+HD/1.html', 'showMovies')
SERIE_HD_TERMINE_VF = (URL_MAIN + '1/categorie-Saison+Terminée+VF+HD/1.html', 'showMovies')
SERIE_HD_TERMINE_VOSTFR = (URL_MAIN + '1/categorie-Saison+Terminée+VOST+HD/1.html', 'showMovies')

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
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Mangas', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSpectacles', 'Spectacles', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuEmissionsTV', 'Emissions TV', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuFilms():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oOutputParameterHandler.addParameter('type', 'film')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche de films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_VIEWS[1], 'Films SD (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_DVDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_DVDRIP[1], 'Films SD DVDRIP & BDRIP (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_CAM[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_CAM[1], 'Films SD CAM & DVDScr (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_VOSTFR[1], 'Films SD VOSTFR (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_CLASSIQUE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_CLASSIQUE[1], 'Films SD Classiques (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films HD 720p & 1080p (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films HDLight (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Films 3D (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD_VIEWS[1], 'Films HD (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES_SD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES_SD[1], 'Films SD (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES_HD[1], 'Films HD (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oOutputParameterHandler.addParameter('type', 'serie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche de séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SD_EN_COURS_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SD_EN_COURS_VF[1], 'Séries SD VF en cours', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SD_EN_COURS_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SD_EN_COURS_VOSTFR[1], 'Séries SD VOSTFR en cours', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SD_TERMINE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SD_TERMINE_VF[1], 'Séries SD VF terminées', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SD_TERMINE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SD_TERMINE_VOSTFR[1], 'Séries SD VOSTFR terminées', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD_EN_COURS_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD_EN_COURS_VF[1], 'Séries HD VF en cours', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD_EN_COURS_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD_EN_COURS_VOSTFR[1], 'Séries HD VOSTFR en cours', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD_TERMINE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD_TERMINE_VF[1], 'Séries HD VF terminées', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD_TERMINE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD_TERMINE_VOSTFR[1], 'Séries HD VOSTFR terminées', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oOutputParameterHandler.addParameter('type', 'anime')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMangas', 'Recherche d\'animés', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Dessins Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Mangas VF (Derniers ajouts)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Mangas VOSTFR (Derniers ajouts)', 'vostfr.png', oOutputParameterHandler)

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
    oGui.addDir(SITE_IDENTIFIER, 'showSearchEmissionsTV', 'Recherche émissions TV', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', EMISSIONS_TV[0])
    oGui.addDir(SITE_IDENTIFIER, EMISSIONS_TV[1], 'Dernières émissions TV', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showSearchResult(sUrl)
        oGui.setEndOfDirectory()
        return

def showSearchSpectacles():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH_SPECTACLES[0] + sSearchText
        showSearchResult(sUrl)
        oGui.setEndOfDirectory()
        return

def showSearchEmissionsTV():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH_EMISSIONS_TV[0] + sSearchText
        showSearchResult(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenreMoviesSD():
    showGenre("films+dvdrip+et+bdrip/")

def showGenreMoviesHD():
    showGenre("Films+BluRay+720p+et+1080p/")

def showMovieYears():
    oGui = cGui()

    for i in reversed (xrange(1950, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '1/annee/?rech_year=' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenre(basePath):
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + '1/genre-Action/' + basePath] )
    liste.append( ['Animation', URL_MAIN + '1/genre-Animation/' + basePath] )
    liste.append( ['Arts Martiaux', URL_MAIN + '1/genre-Arts%20Martiaux/' + basePath] )
    liste.append( ['Aventure', URL_MAIN + '1/genre-Aventure/' + basePath] )
    liste.append( ['Biographies', URL_MAIN + '1/genre-Biographies/' + basePath] )
    liste.append( ['Comédie', URL_MAIN + '1/genre-Comedie/' + basePath] )
    liste.append( ['Comédie dramatique', URL_MAIN + '1/genre-Comedie+Dramatique/' + basePath] )
    liste.append( ['Comédie musicale', URL_MAIN + '1/genre-Comedie+Musicale/' + basePath] )
    liste.append( ['Divers', URL_MAIN + '1/genre-Divers/' + basePath] )
    liste.append( ['Drame', URL_MAIN + '1/genre-Drame/' + basePath] )
    liste.append( ['Espionnage', URL_MAIN + '1/genre-Espionnage/' + basePath] )
    liste.append( ['Famille', URL_MAIN + '1/genre-Famille/' + basePath] )
    liste.append( ['Fantastique', URL_MAIN + '1/genre-Fantastique/' + basePath] )
    liste.append( ['Guerre', URL_MAIN + '1/genre-Guerre/' + basePath] )
    liste.append( ['Historique', URL_MAIN + '1/Historique/' + basePath] )
    liste.append( ['Horreur', URL_MAIN + '1/genre-Horreur-Epouvante/' + basePath] )
    liste.append( ['Péplum', URL_MAIN + '1/genre-Peplum/' + basePath] )
    liste.append( ['Policier', URL_MAIN + '1/genre-Policiers/' + basePath] )
    liste.append( ['Romance', URL_MAIN + '1/genre-Romance/' + basePath] )
    liste.append( ['Science fiction', URL_MAIN + '1/genre-Science-Fiction/' + basePath] )
    liste.append( ['Thriller', URL_MAIN + '1/genre-Thriller/' + basePath] )
    liste.append( ['Western', URL_MAIN + '1/genre-Westerns/' + basePath] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearchResult(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    sUrl = sSearch

    HD = 0
    SD = 0

    #uniquement si c'est la premiere page
    if sSearch:
        sType = oInputParameterHandler.getValue('type')

        loop = 1

        if sType:
            if sType == "film":
                sUrl = sUrl + '&rech_cat=video'
                loop = 2
            if sType == "serie":
                sUrl = sUrl + '&rech_cat=serie'
                loop = 2
            if sType == "anime":
                sUrl = sUrl + '&rech_cat=Animations'

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
        loop = 1
        SD = HD = -1

    oParser = cParser()
    aResult = []
    NextPage = []

    while (loop):
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sHtmlContent = sHtmlContent.replace('<span style="background-color: yellow;"><font color="red">', '')
        sPattern = '<b><p style="font-size: 18px;"><A href="([^"]+)">(.+?)<\/A.+?<td align="center">\s*<img src="([^"]+)".+?<b>Description : <\/b><\/br><\/br>(.+?)<'
        aResult1 = oParser.parse(sHtmlContent, sPattern)

        if (aResult1[0] == False):
            oGui.addText(SITE_IDENTIFIER)

        if aResult1[0]:
            aResult = aResult + aResult1[1]

            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                n = '[COLOR teal]Next >>>[/COLOR]'
                if sSearch:
                    n = '[COLOR teal]Next SD >>>[/COLOR]'
                if loop == 2:
                    n ='[COLOR teal]Next HD >>>[/COLOR]'
                NextPage.append((n, sNextPage))

        loop = loop - 1
        if (loop == 1):
            HD = len(aResult)
            if sUrl.endswith('video'):
                sUrl = sUrl.replace('=video', '=Films+HD')
            if sUrl.endswith('serie'):
                sUrl = sUrl.replace('=serie', '=seriehd')

    if (aResult):
        i = 0
        for aEntry in aResult:

            #titre ?
            if i == SD:
                oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Qualitee SD[/COLOR]')
            if i == HD:
                oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Qualitee HD[/COLOR]')
            i = i + 1

            sQual = 'SD'
            if '-hd/' in aEntry[0] or 'bluray' in aEntry[0] or 'hdlight' in aEntry[0]:
                sQual = 'HD'
            if '-3d/' in aEntry[0]:
                sQual = '3D'

            sTitle = str(aEntry[1])
            sTitle = cUtil().removeHtmlTags(sTitle)
            sUrl2 = URL_MAIN + aEntry[0]

            sDesc = aEntry[3]
            sDesc = sDesc.decode("unicode_escape").encode("latin-1")
            sThumb = aEntry[2]

            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if 'series-' in sUrl or '-Saison' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        for n, u in NextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', u)
            oGui.addNext(SITE_IDENTIFIER, 'showSearchResult', n, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showMovies():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    sQual = ''

    sPattern = '<table style="float:left;padding-left:8px"> *<td> *<div align="left"> *<a href="([^"]+)" onmouseover="Tip\(\'<b>([^"]+?)<\/b>.+?Description :</b> <i>([^<]+?)<.+?<img src="([^"]+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sQual = 'SD'
            if '-hd/' in aEntry[0] or 'bluray' in aEntry[0] or 'hdlight' in aEntry[0]:
                sQual = 'HD'
            if '-3d/' in aEntry[0]:
                sQual = '3D'

            sUrl2 = URL_MAIN + aEntry[0]
            sTitle = aEntry[1].replace(' - Saison', ' Saison').replace(' - saison', ' saison')
            sDesc = aEntry[2]
            sDesc = sDesc.decode("unicode_escape").encode("latin-1")
            sThumb = aEntry[3]

            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if 'series-' in sUrl or '-Saison' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="courante">[^<]+</span> <a href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #recuperation nom de la release
    if 'elease :' in sHtmlContent:
        sPattern = 'elease :([^<]+)<'
    else:
        sPattern = '<br /> *([^<]+)</p></center>'

    aResult1 = oParser.parse(sHtmlContent, sPattern)
    #print aResult1
    
    if (aResult1[0] == True):
        if 'Forced' in aResult1[1][0]:
            aResult1[1][0]=''

    #cut de la zone des liens
    if 'Lien Premium' in sHtmlContent:
        sPattern = 'Lien Premium(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if not aResult[0]:
            return
        sHtmlContent = aResult[1][0]

        if 'Interchangeables' in sHtmlContent:
            #cut de restes de liens non premiums
            sPattern = '--(.+?)Interchangeables'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if not aResult[0]:
                return
            sHtmlContent = aResult[1][0]

    else:
        sPattern = '<div id="link">(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if not aResult[0]:
            return
        sHtmlContent = aResult[1][0]
        sHtmlContent = sHtmlContent.replace('&nbsp;', '')

    if '-multi' in sHtmlContent:
        sPattern = '<a href="link.php\?lien\=([^"]+)"'
    else:
        sPattern = '<b>(.+?)<\/b>.+?<a href="link.php\?lien\=([^"]+)" target="_blank" *><b>Cliquer ici pour Télécharger'

    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if '-multi' in aEntry:
                sHostName = 'Liens Multi'
            else:
                sHostName = aEntry[0]
                sHostName = cUtil().removeHtmlTags(sHostName)
            
            oOutputParameterHandler = cOutputParameterHandler()
            sTitle = '[COLOR skyblue]' + sHostName + '[/COLOR]'
            if '-multi' in aEntry:
                oOutputParameterHandler.addParameter('siteUrl', aEntry)
            else:
                oOutputParameterHandler.addParameter('siteUrl', aEntry[1])

            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addLink(SITE_IDENTIFIER, 'Display_protected_link', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    #recuperation nom de la release
    sPattern = '</span> ([^<]+)</strong> :.'
    aResult1 = oParser.parse(sHtmlContent, sPattern)

    #cut de la zone des liens
    if 'Lien Premium' in sHtmlContent:
        sPattern = 'Lien Premium *--(.+?)</div>'
    else:
        sPattern = '<div id="link">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sHtmlContent = aResult[1][0]
    sHtmlContent = re.sub('<font color="[^"]+">', '', sHtmlContent)
    sHtmlContent = re.sub('</font>', '', sHtmlContent)
    #sHtmlContent = re.sub('link.php\?lien\=', '', sHtmlContent)

    if '-multi' in sHtmlContent:
        sPattern = '<a href="link.php\?lien\=([^"]+)"'
    else:
        sPattern = '<b>(.+?)</b> </br> <a href="link.php\?lien\=([^"]+)" target="_blank" ><b>Cliquer ici pour Télécharger</b></a>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oGui.addText(SITE_IDENTIFIER, sMovieTitle + aResult1[1][0])

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

                oOutputParameterHandler = cOutputParameterHandler()
            if total == 1:
                sTitle = '[COLOR skyblue]' + 'Liens Premium' + '[/COLOR]'
                oOutputParameterHandler.addParameter('siteUrl', aEntry)
            else:
                sTitle = '[COLOR skyblue]' + aEntry[0] + '[/COLOR]'
                oOutputParameterHandler.addParameter('siteUrl', aEntry[1])

            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addLink(SITE_IDENTIFIER, 'Display_protected_link', sTitle, sThumb, sDesc, oOutputParameterHandler)

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
                sPattern_dlprotect = 'target=_blank>([^<]+)<'
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

    cookies = ''
    dialogs = dialog()
    #try to get previous cookie
    cookies = GestionCookie().Readcookie('liens_free-telechargement_org')

    oRequestHandler = cRequestHandler(url)
    if cookies:
        oRequestHandler.addHeaderEntry('Cookie', cookies)
    sHtmlContent = oRequestHandler.request()

    #A partir de la on a les bon cookies pr la protection cloudflare

    #Si ca demande le captcha
    if 'Veuillez recopier le captcha ci-dessus' in sHtmlContent:
        if cookies:
            GestionCookie().DeleteCookie('liens_free-telechargement_org')
            oRequestHandler = cRequestHandler(url)
            sHtmlContent = oRequestHandler.request()

        s = re.findall('src=".\/([^<>"]+?)" alt="CAPTCHA Image"', sHtmlContent)
        if host in s[0]:
            image = s[0]
        else:
            image = host + s[0]

        captcha,cookies2 = get_response(image, cookies)
        cookies = cookies + '; ' + cookies2

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4')
        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('Cookie', cookies)
        oRequestHandler.addHeaderEntry('Referer', url)

        oRequestHandler.addParameters('do', 'contact')
        oRequestHandler.addParameters('ct_captcha', captcha)

        sHtmlContent = oRequestHandler.request()

        if 'Code de securite incorrect' in sHtmlContent:
            dialogs.VSinfo("Mauvais Captcha")
            return 'rate'

        if 'Veuillez recopier le captcha ci-dessus' in sHtmlContent:
            dialogs.VSinfo("Rattage")
            return 'rate'

        #si captcha reussi
        #save cookies
        GestionCookie().SaveCookie('liens_free-telechargement_org', cookies)

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
