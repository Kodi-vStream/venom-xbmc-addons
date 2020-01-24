#-*- coding: utf-8 -*-
#vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress
# from resources.lib.sucuri import SucurieBypass

SITE_IDENTIFIER = 'filmzenstream_com'
SITE_NAME = 'Filmzenstream'
SITE_DESC = 'Film streaming HD gratuit complet'

URL_MAIN = 'https://filmzenstream.online/'

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
# MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + 'index.php?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'index.php?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'genre/action-films/'] )
    liste.append( ['Animation', URL_MAIN + 'genre/animation-films/'] )
    liste.append( ['Aventure', URL_MAIN + 'genre/aventure-films/'] )
    liste.append( ['Biographie', URL_MAIN + 'genre/biographie-films/'] )
    liste.append( ['Comédie', URL_MAIN + 'genre/comedie-online-vf/'] )
    liste.append( ['Crime', URL_MAIN + 'genre/crime-films/'] )
    liste.append( ['Drame', URL_MAIN + 'genre/drame-films/'] )
    liste.append( ['Familial', URL_MAIN + 'genre/familial-films/'] )
    liste.append( ['Fantastique', URL_MAIN + 'genre/fantastique-films/'] )
    liste.append( ['Guerre', URL_MAIN + 'genre/guerre-films/'] )
    liste.append( ['Histoire', URL_MAIN + 'genre/histoire-films/'] )
    liste.append( ['Horreur', URL_MAIN + 'genre/horreur-online-hd/'] )
    liste.append( ['Musical', URL_MAIN + 'genre/musical-films/'] )
    liste.append( ['Mystère', URL_MAIN + 'genre/mystere-films/'] )
    liste.append( ['Romance', URL_MAIN + 'genre/romance-films/'] )
    liste.append( ['Science-fiction', URL_MAIN + 'genre/science-fiction/'] ) # Pas de suffixe -films
    liste.append( ['Sport', URL_MAIN + 'genre/sport-films/'] )
    liste.append( ['Thriller', URL_MAIN + 'genre/thriller-films/'] )
    liste.append( ['War', URL_MAIN + 'genre/war-films/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showYears():
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sStart = '<h3>Année de sortie'
    sEnd = '<h3>Qualité'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    #sHtmlContent = SucurieBypass().GetHtml(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sPattern = '<article id=".+?<a href="([^"]+)" title="([^"]+)".+? src="([^"]+)"'
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

            sUrl2 = aEntry[0]
            sTitle = aEntry[1]
            sThumb = aEntry[2]
            if sThumb.startswith('//'):
                sThumb = 'http:' + sThumb

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 3:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH_MOVIES[0], ''), sTitle) == 0:
                    continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        if not sSearch:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^"]+?)" >Page suivante'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return  aResult[1][0]

    return False

def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    # sHtmlContent = SucurieBypass().GetHtml(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe.+?src="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if 'belike' in aEntry:
                if aEntry.startswith('/'):
                    oRequestHandler = cRequestHandler('https:' + aEntry)
                else:
                    oRequestHandler = cRequestHandler(aEntry)

                oRequestHandler.request()
                sHosterUrl = oRequestHandler.getRealUrl()

            else:
                sHosterUrl = aEntry
                #Vire les bandes annonces
                if 'youtube.com' in aEntry:
                    continue

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
