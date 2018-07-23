#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'streamiz_co'
SITE_NAME = 'Streamiz'
SITE_DESC = 'Tous vos films en streaming gratuitement'

URL_MAIN = 'http://film.streamiz.co/'
URL_API = 'https://api.streamiz.co/movies/'

MOVIE_NEWS = (URL_MAIN + 'recemment-ajoute/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN, 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'les-plus-vus/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = ('http/venom', 'showYears')

URL_SEARCH = (URL_API + 'search/?query=', 'showMovies')
URL_SEARCH_MOVIES = (URL_API + 'search/?query=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les Plus Vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMoviesSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)

    sHtmlContent = oRequestHandler.request()
    sStart = '<h3 class="nav-title nop">Film Streaming par Genres</h3>'
    sEnd = '<h3 class="nav-title nop">Film Streaming par Années</h3>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<li class="cat-item cat-item.+?"><a href="([^"]+)"><i class="icons icon-play"></i>(.+?)<i class="count">(.+?)</i>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1] + '(' + aEntry[2] + ')'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showYears():
    #for i in itertools.chain(xrange(5, 7), [8, 9]): afficher dans l'ordre (pense bete ne pas effacer)
    oGui = cGui()
    #compliquer pour rien.
    # from itertools import chain
    # generator = chain([1998,1999],xrange(2000,2019))#desordre
    # for i in reversed(list(generator)):
    for i in reversed(range(2000,2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', ('%s%s%s%s') % (URL_MAIN, 'annee/', Year, '/'))
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()
    
def showMovies(sSearch = ''):

    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()

    if sSearch:
        sUrl = sSearch
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #indispensable
    sHtmlContent = sHtmlContent.replace("\t", "")
    sHtmlContent = sHtmlContent.replace("\n", "")

    if sSearch:
        sPattern = 'post_title":[\'"]([^<>\'"]+)[\'"],"post_name":[\'"]([^<>\'"]+)[\'"],"poster_url":[\'"]([^<>\'"]+)[\'"]'
    else:
        sPattern = '<div class="movie_last"><a href="([^"]+)".+?<img src="([^"]+)".+?<div class="title">(.+?)<\/div>.+?<i class="quality">(.+?)</i>.+?<p class="nop synopsis">(.+?)</p>'

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

            if sSearch:
                sUrl = URL_MAIN + aEntry[1].replace('\/', '/')
                sThumb = aEntry[2].replace('\/', '/')
                sTitle = aEntry[0]
                sDesc = ''#aEntry[2].replace("&laquo;", '«').replace("&raquo;", '»').replace('  ', ' ')
                sDisplayTitle = sTitle
            else:
                sUrl = aEntry[0]
                sThumb = aEntry[1]
                sTitle = aEntry[2].replace('&#8217;', '\'')
                sQual = aEntry[3]
                sDesc = aEntry[4].replace("&laquo;", '«').replace("&raquo;", '»').replace('  ', ' ')
                sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<li class=.active.>.+?<\/a><\/li><li><a.+?ref=.(.+?).>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="movie_player" data-id="(.+?)"'
    Fresult = oParser.parse(sHtmlContent, sPattern)

    if (Fresult[0] == True):
        sID = Fresult[1][0]
        oRequestHandler = cRequestHandler(URL_API + sID + '/embeds')
        sHtmlContent = oRequestHandler.request()
        if sHtmlContent:
            sHtmlContent = sHtmlContent.replace('\\', '')
            sHtmlContent = sHtmlContent.strip('[""]')
            sHtmlContent = sHtmlContent.replace('"', '')
            sHtmlContent = sHtmlContent.split(',')

            for aEntry in sHtmlContent:
                sHosterUrl = aEntry
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
