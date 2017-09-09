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

import re
import xbmc
import xbmcaddon,os

PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile"))

SITE_IDENTIFIER = 'streamase_com'
SITE_NAME = '[COLOR violet]Streamase[/COLOR]'
SITE_DESC = 'Fichiers en Streaming et en DDL, HD'

#film
URL_MAIN = 'https://streamase.com/'
MOVIE_NEWS = (URL_MAIN , 'showMovies')
MOVIE_MOVIE = (True, 'showMenuFilms')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_ANNEES = (True, 'showMovieAnnees')

#serie
URL_MAIN_SERIE = 'http://serie.streamase.com/'
SERIE_NEWS = (URL_MAIN_SERIE + 'index.php?do=lastnews/' , 'showMovies')
SERIE_SERIES = (True, 'showMenuSeries')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_ANNEES = (True, 'showSerieAnnees')

URL_FAV = URL_MAIN + 'favorites/'

#recherche
URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMembres', 'Espace Membres', 'none.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMembres():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'login', 'Login', 'none.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showFavorites', 'Mes Favoris', 'none.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuFilms():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oOutputParameterHandler.addParameter('type', 'film')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche de Films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'films_annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oOutputParameterHandler.addParameter('type', 'serie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche de Séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par Années)', 'series_annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showFavorites():
    oGui = cGui()
    showMovies(URL_FAV)
    oGui.setEndOfDirectory()
    return

def showMovieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN + 'action/' ] )
    liste.append( ['Animation',URL_MAIN + 'animation/' ] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'arts-martiaux/' ] )
    liste.append( ['Aventure',URL_MAIN + 'aventure/' ] )
    liste.append( ['Biographies',URL_MAIN + 'biopic/' ] )
    liste.append( ['Comédie',URL_MAIN + 'comedie/' ] )
    liste.append( ['Comédie dramatique',URL_MAIN + 'comedie-dramatique/' ] )
    liste.append( ['Comédie musicale',URL_MAIN + 'comedie-musicale/' ] )
    liste.append( ['Crime',URL_MAIN + 'crime/' ] )
    liste.append( ['Documentaire',URL_MAIN + 'documentaire/' ] )
    liste.append( ['Drame',URL_MAIN + 'drame/' ] )
    liste.append( ['Divers',URL_MAIN + 'divers/' ] )
    liste.append( ['Espionnage',URL_MAIN + 'espionage/' ] )
    liste.append( ['Famille',URL_MAIN + 'famille/' ] )
    liste.append( ['Fantastique',URL_MAIN + 'fantastique/' ] )
    liste.append( ['Guerre',URL_MAIN + 'guerre/' ] )
    liste.append( ['Historique',URL_MAIN + 'historique/' ] )
    liste.append( ['Horreur',URL_MAIN + 'horror/' ] )
    liste.append( ['Musical',URL_MAIN + 'musical/' ] )
    liste.append( ['Péplum',URL_MAIN + 'pplum/' ] )
    liste.append( ['Policier',URL_MAIN + 'policier/' ] )
    liste.append( ['Romance',URL_MAIN + 'romance/' ] )
    liste.append( ['Science fiction',URL_MAIN + 'sci-fi/' ] )
    liste.append( ['Spectacle',URL_MAIN + 'spectacle/' ] )
    liste.append( ['Sport',URL_MAIN + 'sport/' ] )
    liste.append( ['Thriller',URL_MAIN + 'thriller/' ] )
    liste.append( ['Western',URL_MAIN + 'western/' ] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN_SERIE + 'action/' ] )
    liste.append( ['Animation',URL_MAIN_SERIE + 'animation/' ] )
    liste.append( ['Arts Martiaux',URL_MAIN_SERIE + 'arts-martiaux/' ] )
    liste.append( ['Aventure',URL_MAIN_SERIE + 'aventure/' ] )
    liste.append( ['Comédie',URL_MAIN_SERIE + 'comedie/' ] )
    liste.append( ['Comédie dramatique',URL_MAIN_SERIE + 'comedie-dramatique/' ] )
    liste.append( ['Comédie musicale',URL_MAIN_SERIE + 'comedie-musicale/' ] )
    liste.append( ['Documentaire',URL_MAIN_SERIE + 'documentaire/' ] )
    liste.append( ['Drame',URL_MAIN_SERIE + 'drame/' ] )
    liste.append( ['Espionnage',URL_MAIN_SERIE + 'espionnage/' ] )
    liste.append( ['Famille',URL_MAIN_SERIE + 'famille/' ] )
    liste.append( ['Fantastique',URL_MAIN_SERIE + 'fantastique/' ] )
    liste.append( ['Guerre',URL_MAIN_SERIE + 'guerre/' ] )
    liste.append( ['Historique',URL_MAIN_SERIE + 'historique/' ] )
    liste.append( ['Horreur',URL_MAIN_SERIE + 'horror/' ] )
    liste.append( ['Musical',URL_MAIN_SERIE + 'musical/' ] )
    liste.append( ['Policier',URL_MAIN_SERIE + 'policier/' ] )
    liste.append( ['Romance',URL_MAIN_SERIE + 'romance/' ] )
    liste.append( ['Science fiction',URL_MAIN_SERIE + 'sci-fi/' ] )
    liste.append( ['Thriller',URL_MAIN_SERIE + 'thriller/' ] )
    liste.append( ['Western',URL_MAIN_SERIE + 'western/' ] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'series_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovieAnnees():
    oGui = cGui()

    for i in reversed (xrange(1932, 2018)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'date-' + Year + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieAnnees():
    oGui = cGui()

    for i in reversed (xrange(2011, 2018)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN_SERIE + 'date-' + Year + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def login():
    oGui = cGui()
    name = oGui.showKeyBoard()
    password = oGui.showKeyBoard()
    cookies = ''

    oRequestHandler = cRequestHandler(URL_MAIN)
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    #oRequestHandler.addHeaderEntry('Origin',URL_MAIN)
    oRequestHandler.addHeaderEntry('Referer',URL_MAIN)
    oRequestHandler.addParameters('login_name', name)
    oRequestHandler.addParameters('login_password', password)
    oRequestHandler.addParameters('login', 'submit')

    sHtmlContent = oRequestHandler.request()
    cookies = oRequestHandler.GetCookies()
    print cookies
    if cookies:
        cConfig().showInfo('vStream', 'Login OK')
        #save cookies
        GestionCookie().SaveCookie('streamase.com',cookies)

    oGui.setEndOfDirectory()
    return

def showMovies(sSearch = ''):
    #xbmc.log('showMovies')

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    if sSearch:

        oInputParameterHandler = cInputParameterHandler()
        sType = oInputParameterHandler.getValue('type')

        Url_Search = URL_MAIN

        if sType:
            if sType == "serie":
                Url_Search = URL_MAIN_SERIE
            else:
                Url_Search = URL_MAIN

        if sSearch == URL_FAV:
            sUrl = URL_FAV
            cookies = ''
            #try to get previous cookie
            cookies = GestionCookie().Readcookie('streamase.com')
            oRequestHandler = cRequestHandler(sUrl)
            if cookies:
                oRequestHandler.addHeaderEntry('Cookie',cookies)

            sHtmlContent = oRequestHandler.request()

            sSearch = ''
            #xbmc.log(sHtmlContent)
        else:
            sUrl = Url_Search + 'index.php?do=search'

            if URL_SEARCH[0] in sSearch:
                sSearch=sSearch.replace(URL_SEARCH[0],'')

            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
            #oRequestHandler.addHeaderEntry('Origin',URL_MAIN)
            oRequestHandler.addHeaderEntry('Referer',Url_Search)
            #oRequestHandler.addParameters('do', 'search')
            oRequestHandler.addParameters('subaction', 'search')
            oRequestHandler.addParameters('search_start', '0')
            oRequestHandler.addParameters('full_search', '0')
            oRequestHandler.addParameters('result_from', '1')
            oRequestHandler.addParameters('story', sSearch)

            sHtmlContent = oRequestHandler.request()

    else:

        sUrl = oInputParameterHandler.getValue('siteUrl')

        #xbmc.log(sUrl)

        oRequestHandler = cRequestHandler(sUrl)
        if URL_FAV in sUrl:
            cookies = GestionCookie().Readcookie('streamase.com')
            oRequestHandler.addHeaderEntry('Cookie',cookies)

        sHtmlContent = oRequestHandler.request()
        #xbmc.log(sHtmlContent)

    sCom = ''
    sQual = ''
    sYear = ''

    sPattern = '<h3 class="btl"><a href="([^"]+)">([^<]+?)</a></h3>.+?<div class="maincont">.+?src="([^"]+)".+?<br */>([^<]+?)<br */><br */>(.+?)<div class="clr"><\/div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #cConfig().log(str(aResult))

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        for aEntry in aResult[1]:
            sQual = str(aEntry[3])
            sTitle = str(aEntry[1])
            sUrl2 = aEntry[0]
            sCom = aEntry[4]
            sCom = sCom.decode("unicode_escape").encode("latin-1")
            if aEntry[2].startswith('http'):
                sThumbnail=aEntry[2]
            else:
                sThumbnail=URL_MAIN + aEntry[2]


            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch,sTitle) == 0:
                    continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl2))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sCom', sCom)
            sDisplayTitle = cUtil().DecoTitle(sTitle + ' (' + sQual + ')')

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, sCom, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    #Passage en mode vignette sauf en cas de recherche globale
    #if not bGlobal_Search:
        #xbmc.executebuiltin('Container.SetViewMode(500)')

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a href="([^"]+)"><span class="thide pnext">Next</span></a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #xbmc.log(str(aResult))
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    #xbmc.log("showHosters")

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')

    #cConfig().log(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sPattern = '<!--/colorstart-->([^<]+)<!--colorend-->|<a href="([^"]+)" *target="_blank">([^<]+?)</a>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    #xbmc.log(str(aResult))

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR] ')
            else:
                sHosterUrl=aEntry[1]
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                sTitle = aEntry[2]
                if (oHoster != False):
                    sDisplayTitle = cUtil().DecoTitle(sTitle)
                    sDisplayTitle = sDisplayTitle.replace('-EXTREME','')
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
