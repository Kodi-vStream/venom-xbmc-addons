# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import xbmc
import xbmcgui

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil, Quote
from resources.lib.config import GestionCookie
from resources.lib.comaddon import progress, dialog, siteManager

UA = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

SITE_IDENTIFIER = 'free_telechargement_org'
SITE_NAME = '[COLOR violet]Free-Téléchargement[/COLOR]'
SITE_DESC = 'Fichiers en DDL, HD, Films, Séries, Mangas Etc...'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_PROTECT = 'liens.free-telecharg'  # ne pas mettre 'er' ou 'ement' à la fin, perte de hosters

FUNCTION_SEARCH = 'showSearchResult'
URL_SEARCH = (URL_MAIN + '1/recherche/1.html?rech_fiche=', FUNCTION_SEARCH)
URL_SEARCH_MOVIES = (URL_MAIN + '1/recherche/1.html?rech_cat=video&rech_fiche=', FUNCTION_SEARCH)
URL_SEARCH_SERIES = (URL_MAIN + '1/recherche/1.html?rech_cat=serie&rech_fiche=', FUNCTION_SEARCH)
URL_SEARCH_ANIMS = (URL_MAIN + '1/recherche/1.html?rech_cat=Animations&rech_fiche=', FUNCTION_SEARCH)
URL_SEARCH_MISC = (URL_MAIN + '1/recherche/1.html?rech_cat=videos&rech_fiche=', FUNCTION_SEARCH)

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_SD_DVDRIP = (URL_MAIN + '1/categorie-Films+DVDRiP+et+BDRiP/1.html', 'showMovies')
MOVIE_SD_CAM = (URL_MAIN + '1/categorie-Films+CAM+TS+R5+et+DVDSCR/1.html', 'showMovies')
MOVIE_SD_VOSTFR = (URL_MAIN + '1/categorie-Films+VOSTFR+et+VO/1.html', 'showMovies')
MOVIE_SD_CLASSIQUE = (URL_MAIN + '1/categorie-Films+Classiques/1.html', 'showMovies')
MOVIE_SD_VIEWS = (URL_MAIN + '1/films/affichage', 'showMovies')
MOVIE_GENRES_SD = (True, 'showGenreMoviesSD')
MOVIE_HD = (URL_MAIN + '1/categorie-Films+BluRay+720p+et+1080p/1.html', 'showMovies')
MOVIE_4K = (URL_MAIN + '1/categorie-Films+Bluray+4K/1.html', 'showMovies')
MOVIE_HDLIGHT = (URL_MAIN + '1/films-hdlight/1.html', 'showMovies')
MOVIE_3D = (URL_MAIN + '1/categorie-Films+BluRay+3D/1.html', 'showMovies')
MOVIE_HD_VIEWS = (URL_MAIN + '1/films-bluray/affichage', 'showMovies')
MOVIE_GENRES_HD = (True, 'showGenreMoviesHD')
MOVIE_ANNEES = (True, 'showMovieYears')
MOVIE_SAGA = (URL_MAIN + '1/categorie-Sagas+Films/1.html', 'showMovies')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_SD_EN_COURS_VF = (URL_MAIN + '1/categorie-Saisons+en+cours+VF+/1.html', 'showMovies')
SERIE_SD_EN_COURS_VOSTFR = (URL_MAIN + '1/categorie-Saisons+en+cours+VOST/1.html', 'showMovies')
SERIE_SD_TERMINE_VF = (URL_MAIN + '1/categorie-Saison+Termin%E9e+VF/1.html', 'showMovies')
SERIE_SD_TERMINE_VOSTFR = (URL_MAIN + '1/categorie-Saison+Termin%E9e+VOST/1.html', 'showMovies')
SERIE_HD_EN_COURS_VF = (URL_MAIN + '1/categorie-Saisons+en+cours+VF+HD/1.html', 'showMovies')
SERIE_HD_EN_COURS_VOSTFR = (URL_MAIN + '1/categorie-Saisons+en+cours+VOST+HD/1.html', 'showMovies')
SERIE_HD_TERMINE_VF = (URL_MAIN + '1/categorie-Saison+Termin%E9e+VF+HD/1.html', 'showMovies')
SERIE_HD_TERMINE_VOSTFR = (URL_MAIN + '1/categorie-Saison+Termin%E9e+VOST+HD/1.html', 'showMovies')

ANIM_ANIMS = (True, 'showMenuMangas')
ANIM_NEWS = (URL_MAIN + '1/animations/1', 'showMovies')
ANIM_VFS = (URL_MAIN + '1/categorie-Mangas+VF/1.html', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + '1/categorie-Mangas+VOST/1.html', 'showMovies')

EMISSIONS_TV = (URL_MAIN + '1/categorie-Emissions/1.html', 'showMovies')

SPECTACLES = (URL_MAIN + '1/categorie-Spectacles/1.html', 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Mangas', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSpectacles', 'Spectacles', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuEmissionsTV', 'Emissions TV', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche de films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_VIEWS[1], 'Films SD (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_DVDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_DVDRIP[1], 'Films SD DVDRIP & BDRIP (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_CAM[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_CAM[1], 'Films SD CAM & DVDScr (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_VOSTFR[1], 'Films SD VOSTFR (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_CLASSIQUE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_CLASSIQUE[1], 'Films SD Classiques (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films HD 720p & 1080p (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4K[1], 'Films UHD 4K (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films HDLight (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Films 3D (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD_VIEWS[1], 'Films HD (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES_SD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES_SD[1], 'Films SD (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES_HD[1], 'Films HD (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SAGA[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SAGA[1], 'Films (Sagas)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche de séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_SD_EN_COURS_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SD_EN_COURS_VF[1], 'Séries SD VF en cours', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_SD_EN_COURS_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SD_EN_COURS_VOSTFR[1], 'Séries SD VOSTFR en cours', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_SD_TERMINE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SD_TERMINE_VF[1], 'Séries SD VF terminées', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_SD_TERMINE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SD_TERMINE_VOSTFR[1], 'Séries SD VOSTFR terminées', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD_EN_COURS_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD_EN_COURS_VF[1], 'Séries HD VF en cours', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD_EN_COURS_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD_EN_COURS_VOSTFR[1], 'Séries HD VOSTFR en cours', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD_TERMINE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD_TERMINE_VF[1], 'Séries HD VF terminées', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD_TERMINE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD_TERMINE_VOSTFR[1], 'Séries HD VOSTFR terminées', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche d\'animés', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Dessins Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Mangas VF (Derniers ajouts)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Mangas VOSTFR (Derniers ajouts)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuSpectacles():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MISC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche de Spectacles', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPECTACLES[0])
    oGui.addDir(SITE_IDENTIFIER, SPECTACLES[1], 'Spectacles (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuEmissionsTV():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MISC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche émissions TV', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', EMISSIONS_TV[0])
    oGui.addDir(SITE_IDENTIFIER, EMISSIONS_TV[1], 'Dernières émissions TV', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sSearchText = Quote(sSearchText)
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sUrl = sUrl + sSearchText
        showSearchResult(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenreMoviesSD():
    showGenre("films+dvdrip+et+bdrip/")


def showGenreMoviesHD():
    showGenre("Films+BluRay+720p+et+1080p/")


def showGenre(basePath):
    oGui = cGui()

    liste = [['Action', 'Action'], ['Animation', 'Animation'], ['Arts Martiaux', 'Arts%20Martiaux'],
             ['Aventure', 'Aventure'], ['Biographies', 'Biographies'], ['Comédie', 'Comedie'],
             ['Comédie dramatique', 'Comedie+Dramatique'], ['Comédie musicale', 'Comedie+Musicale'],
             ['Divers', 'Divers'], ['Drame', 'Drame'], ['Espionnage', 'Espionnage'], ['Famille', 'Famille'],
             ['Fantastique', 'Fantastique'], ['Guerre', 'Guerre'], ['Historique', 'Historiques'],
             ['Horreur', 'Horreur-Epouvante'], ['Péplum', 'Peplum'], ['Policier', 'Policiers'], ['Romance', 'Romance'],
             ['Science fiction', 'Science-Fiction'], ['Thriller', 'Thriller'], ['Western', 'Westerns']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '1/genre-' + sUrl + '/' +  + basePath)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1950, 2022)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '1/annee/?rech_year=' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearchResult(sSearch=''):
    oUtil = cUtil()
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
    sSearchText = sSearchText.replace(URL_SEARCH_SERIES[0], '')
    sSearchText = sSearchText.replace(URL_SEARCH_MISC[0], '')
    sSearchText = sSearchText.replace(URL_SEARCH_ANIMS[0], '')
    sSearchText = oUtil.CleanName(sSearchText)

    loop = 2

    if sSearch:
        SD = HD = 0
        sUrl = sSearch
    else:
        SD = HD = -1
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    aResult = []
    NextPage = []

    while loop:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sHtmlContent = sHtmlContent.replace('<span style="background-color: yellow;"><font color="red">', '')
        sPattern = '<b><p style="font-size: 18px;"><A href="([^"]+)">(.+?)<\/A.+?<td align="center">\s*<img src="([^"]+)".+?<b>Description : (.+?)<br /><br />'
        aResult1 = oParser.parse(sHtmlContent, sPattern)

        if aResult1[0] is False:
            oGui.addText(SITE_IDENTIFIER)

        if aResult1[0]:
            aResult = aResult + aResult1[1]

            sNextPage = __checkForNextPage(sHtmlContent)
            if sNextPage != False:
                n = ' >>>'
                if sSearch:
                    n = ' SD >>>'
                if loop == 2:
                    n = ' HD >>>'
                NextPage.append((n, sNextPage))

        loop = loop - 1
        if loop == 1:
            HD = len(aResult)
            if sUrl.find('=video') > 0:
                sUrl = sUrl.replace('=video', '=Films+HD')
            elif sUrl.find('=serie') > 0:
                sUrl = sUrl.replace('=serie', '=seriehd')
            else:
                loop = 0

    if aResult:
        i = 0
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult:

            # titre ?
            if i == SD:
                oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Qualitée SD[/COLOR]')
            if i == HD:
                oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Qualitée HD[/COLOR]')
            i = i + 1

            sQual = 'SD'
            if '-hd/' in aEntry[0] or 'bluray' in aEntry[0] or 'hdlight' in aEntry[0]:
                sQual = 'HD'
            if '-3d/' in aEntry[0]:
                sQual = '3D'

            sTitle = str(aEntry[1]).replace(' - Saison', ' Saison').replace(' - saison', ' Saison')
            sTitle = cUtil().removeHtmlTags(sTitle)
            
            # Filtre recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            sUrl2 = URL_MAIN + aEntry[0]

            sDesc = aEntry[3]
            sDesc = re.sub('<[^<]+?>', '', sDesc)  # retrait des balises html
            sThumb = aEntry[2]

            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if '/mangas' in sUrl:
                oGui.addAnime(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif 'series-' in sUrl or '-Saison' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif '-Sagas' in sUrl:
                oGui.addMoviePack(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        if not sSearch:
            for n, u in NextPage:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', u)
                sNumPage = re.search('/([0-9]+)/', u).group(1)
                oGui.addNext(SITE_IDENTIFIER, 'showSearchResult', 'Page ' + sNumPage + ' ' + n, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<table style="float:left;padding-left:8px"> *<td> *<div align="left"> *<a href="([^"]+)" onmouseover="Tip\(\'<b>([^"]+?)</b>.+?Description :</b> <i>([^<]+?)<.+?<img src="([^"]+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        oOutputParameterHandler = cOutputParameterHandler()
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
            sTitle = aEntry[1].replace(' - Saison', ' Saison').replace(' - saison', ' Saison')
            sDesc = aEntry[2]
            sDesc = sDesc.decode("unicode_escape").encode("latin-1")
            sThumb = aEntry[3]

            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if '/mangas' in sUrl:
                oGui.addAnime(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif 'series-' in sUrl or '-Saison' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif '-Sagas' in sUrl:
                oGui.addMoviePack(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            sNumPage = re.search('/([0-9]+)/', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sNumPage, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="courante">[^<]+</span> <a href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
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
    # parfois présent, plus sure que de réduire la regex
    sHtmlContent = re.sub('</font>', '', sHtmlContent)

    # recuperation nom de la release
    if 'elease :' in sHtmlContent:
        sPattern = 'elease :([^<]+)<'
    else:
        sPattern = '<br /> *([^<]+)</p></center>'

    aResult1 = oParser.parse(sHtmlContent, sPattern)
    # VSlog(aResult1)

    if aResult1[0] is True:
        if 'Forced' in aResult1[1][0]:
            aResult1[1][0] = ''

    # cut de la zone des liens
    if 'Lien Premium' in sHtmlContent:
        sPattern = 'Lien Premium(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if not aResult[0]:
            return
        sHtmlContent = aResult[1][0]

        if 'Interchangeables' in sHtmlContent:
            # cut de restes de liens non premiums
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
        sPattern = 'target="_blank" href="([^"]+)"'
    else:
        sPattern = '<b> *([^<]+)</b> </br> <a href="([^"]+)" target="_blank" *><b><font color="#00aeef">Cliquer ici'

    aResult = oParser.parse(sHtmlContent, sPattern)
    # VSlog(aResult)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            if '-multi' in aEntry:
                sHostName = 'Liens Multi'
            else:
                if 'nitroflare' in aEntry[1] or 'turbo' in aEntry[1] or 'q.gs' in aEntry[1]:  # hosters non géré
                    continue
                if 'hitfile' in aEntry[1] or 'hil.to' in aEntry[1]:  # hosters non géré
                    continue
                if 'uplooad' in aEntry[1] or 'rapidgator' in aEntry[1]:  # hoster non géré
                    continue

                sHostName = aEntry[0]
                # on récupère le nom du hoster dans l'url
                # Sinon les hosters sont souvent affiché en temps que Free-telechargements
                if 'uptobox' in aEntry[1]:
                    sHostName = 'UpToBox'
                if 'uploaded' in aEntry[1]:
                    sHostName = 'Uploaded'
                if '1fichier' in aEntry[1]:
                    sHostName = '1Fichier'

                sHostName = cUtil().removeHtmlTags(sHostName)

            sTitle = '[COLOR coral]' + sHostName + '[/COLOR]'

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
    # parfois présent, plus sure que de réduire la regex
    sHtmlContent = re.sub('</font>', '', sHtmlContent)

    oParser = cParser()

    # recuperation nom de la release
    sPattern = '</span> ([^<]+)</strong> :.'
    aResult1 = oParser.parse(sHtmlContent, sPattern)

    # cut de la zone des liens
    if 'Lien Premium' in sHtmlContent:
        sPattern = 'Lien Premium *--(.+?)</div>'
    else:
        sPattern = '<div id="link">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sHtmlContent = aResult[1][0]
    sHtmlContent = re.sub('<font color="[^"]+">', '', sHtmlContent)
    sHtmlContent = re.sub('</font>', '', sHtmlContent)
    # sHtmlContent = re.sub('link.php\?lien\=', '', sHtmlContent)

    if '-multi' in sHtmlContent:
        sPattern = 'target="_blank" href="([^"]+)"'
    else:
        sPattern = '<b> *([^<]+)</b> </br> <a href="([^"]+)" target="_blank" *><b><font color="#00aeef">Cliquer ici'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        total = len(aResult[1])
        oGui.addText(SITE_IDENTIFIER, sMovieTitle + aResult1[1][0])

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if total == 1:
                sTitle = '[COLOR coral]' + 'Liens Premium' + '[/COLOR]'
                oOutputParameterHandler.addParameter('siteUrl', aEntry)
            else:
                sTitle = '[COLOR coral]' + aEntry[0] + '[/COLOR]'
                oOutputParameterHandler.addParameter('siteUrl', aEntry[1])

            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addLink(SITE_IDENTIFIER, 'Display_protected_link', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def Display_protected_link():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    # Est ce un lien dl-protect ?
    if URL_PROTECT in sUrl:
        if "lien=" in sUrl:
            sUrl = sUrl.split('lien=')[1]
        sHtmlContent = DecryptddlProtect(sUrl)

        if sHtmlContent:
            # Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotect = (True, [sHtmlContent])
            else:
                sPattern_dlprotect = 'target=_blank>([^<]+)<'
                aResult_dlprotect = oParser.parse(sHtmlContent, sPattern_dlprotect)

        else:
            dialog().VSok('Désolé, problème de captcha.')
            aResult_dlprotect = (False, False)
    # Si lien normal
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotect = (True, [sUrl])

    if aResult_dlprotect[0]:
        for aEntry in aResult_dlprotect[1]:
            sHosterUrl = aEntry

            sTitle = sMovieTitle

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def DecryptddlProtect(url):
    # VSlog('entering DecryptddlProtect')
    if not url:
        return ''

    # Get host
    tmp = url.split('/')
    host = tmp[0] + '//' + tmp[2] + '/'

    dialogs = dialog()
    # try to get previous cookie
    cookies = GestionCookie().Readcookie('liens_free-telechargement_org')

    oRequestHandler = cRequestHandler(url)
    if cookies:
        oRequestHandler.addHeaderEntry('Cookie', cookies)
    sHtmlContent = oRequestHandler.request()

    # A partir de la on a les bon cookies pr la protection cloudflare

    # Si ca demande le captcha
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

        captcha, cookies2 = get_response(image, cookies)
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

        # si captcha reussi
        # save cookies
        GestionCookie().SaveCookie('liens_free-telechargement_org', cookies)

    return sHtmlContent


def get_response(img, cookie):
    # on telecharge l'image
    import xbmcvfs

    dialogs = dialog()

    filename = "special://home/userdata/addon_data/plugin.video.vstream/Captcha.raw"
    # PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile"))
    # filename  = os.path.join(PathCache, 'Captcha.raw')

    # hostComplet = re.sub(r'(https*:\/\/[^/]+)(\/*.*)', '\\1', img)
    # host = re.sub(r'https*:\/\/', '', hostComplet)
    url = img

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    # oRequestHandler.addHeaderEntry('Referer', url)
    oRequestHandler.addHeaderEntry('Cookie', cookie)

    htmlcontent = oRequestHandler.request()

    NewCookie = oRequestHandler.GetCookies()

    downloaded_image = xbmcvfs.File(filename, 'wb')
    # downloaded_image = file(filename, "wb")
    downloaded_image.write(htmlcontent)
    downloaded_image.close()

    # on affiche le dialogue
    solution = ''

    if True:
        # nouveau captcha
        try:
            # affichage du dialog perso
            class XMLDialog(xbmcgui.WindowXMLDialog):
                # """
                # Dialog class for captcha
                # """
                def __init__(self, *args, **kwargs):
                    xbmcgui.WindowXMLDialog.__init__(self)
                    pass

                def onInit(self):
                    # image background captcha
                    self.getControl(1).setImage(filename.encode("utf-8"), False)
                    # image petit captcha memory fail
                    self.getControl(2).setImage(filename.encode("utf-8"), False)
                    self.getControl(2).setVisible(False)
                    # Focus clavier
                    self.setFocus(self.getControl(21))

                def onClick(self, controlId):
                    if controlId == 20:
                        # button Valider
                        solution = self.getControl(5000).getLabel()
                        xbmcgui.Window(10101).setProperty('captcha', solution)
                        self.close()
                        return

                    elif controlId == 30:
                        # button fermer
                        self.close()
                        return

                    elif controlId == 21:
                        # button clavier
                        self.getControl(2).setVisible(True)
                        kb = xbmc.Keyboard(self.getControl(5000).getLabel(), '', False)
                        kb.doModal()

                        if kb.isConfirmed():
                            self.getControl(5000).setLabel(kb.getText())
                            self.getControl(2).setVisible(False)
                        else:
                            self.getControl(2).setVisible(False)

                def onFocus(self, controlId):
                    self.controlId = controlId

                def _close_dialog(self):
                    self.close()

                def onAction(self, action):
                    # touche return 61448
                    if action.getId() in (9, 10, 11, 30, 92, 216, 247, 257, 275, 61467, 61448):
                        self.close()

            path = "special://home/addons/plugin.video.vstream"
            wd = XMLDialog('DialogCaptcha.xml', path, 'default', '720p')
            wd.doModal()
            del wd
        finally:

            solution = xbmcgui.Window(10101).getProperty('captcha')
            if solution == '':
                dialogs.VSinfo("Vous devez taper le captcha")

    else:
        # ancien Captcha
        try:
            img = xbmcgui.ControlImage(450, 0, 400, 130, filename.encode("utf-8"))
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
            # xbmc.sleep(3000)
            kb = xbmc.Keyboard("", "Tapez les Lettres/chiffres de l'image", False)
            kb.doModal()
            if kb.isConfirmed():
                solution = kb.getText()
                if solution == '':
                    dialogs.VSinfo("Vous devez taper le captcha")
            else:
                dialogs.VSinfo("Vous devez taper le captcha")
        finally:
            wdlg.removeControl(img)
            wdlg.close()

    return solution, NewCookie
