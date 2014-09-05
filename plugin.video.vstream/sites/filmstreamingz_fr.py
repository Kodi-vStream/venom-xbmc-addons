#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser


SITE_IDENTIFIER = 'filmstreamingz_fr'
SITE_NAME = 'FilmStreamingz.fr'
SITE_DESC = 'Film Streaming & Serie Streaming: Regardez films et series de qualité entièrement gratuit. Tout les meilleurs streaming en illimité.'

URL_MAIN = 'http://filmstreamingz.fr/'
URL_MAIN2 = 'http://seriestreaming.org/'

MOVIE_NEWS = 'http://filmstreamingz.fr/'
MOVIE_VIEWS = 'http://filmstreamingz.fr/les-plus-vus/'
MOVIE_COMMENTS = 'http://filmstreamingz.fr/les-plus-commentes-2/'
MOVIE_NOTES = 'http://filmstreamingz.fr/les-mieux-notes-2/'
MOVIE_GENRES = True
SERIE_SERIES = 'http://seriestreaming.org/'

def load(): 
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', 'Films Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Nouveautés', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les Plus Vus', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les Plus Commentés', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les Mieux Notés', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeriesSearch', 'Series Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series Nouveautés', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://seriestreaming.org/les-plus-vues/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series Les Plus Vues', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://seriestreaming.org/les-plus-commentees/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series Les Plus Commentés', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://seriestreaming.org/les-mieux-notees/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series Les Mieux Notées', 'series.png', oOutputParameterHandler)


    oGui.setEndOfDirectory()

def showMoviesSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://filmstreamingz.fr/?s='+sSearchText
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return
    

def showSeriesSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://seriestreaming.org/?s='+sSearchText
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return
    


def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []

    liste.append( ['Action','http://filmstreamingz.fr/category/action/'] )
    liste.append( ['Afro','http://filmstreamingz.fr/category/afro/'] )
    liste.append( ['Animation','http://filmstreamingz.fr/category/animation/'] )
    liste.append( ['Arts Martiaux','http://filmstreamingz.fr/category/arts-martiaux/'] )
    liste.append( ['Aventure','http://filmstreamingz.fr/category/aventure/'] )
    liste.append( ['Comedie','http://filmstreamingz.fr/category/comedie/'] )
    liste.append( ['Documentaire','http://filmstreamingz.fr/category/documentaire/'] )
    liste.append( ['Drame','http://filmstreamingz.fr/category/drame/'] )
    liste.append( ['Espionnage','http://filmstreamingz.fr/category/espionnage/'] )
    liste.append( ['Famille','http://filmstreamingz.fr/category/famille/'] )
    liste.append( ['Fantastique','http://filmstreamingz.fr/category/fantastique/'] )
    liste.append( ['Guerre','http://filmstreamingz.fr/category/guerre/'] )
    liste.append( ['Historique','http://filmstreamingz.fr/category/historique/'] )
    liste.append( ['Epouvante-Horreur','http://filmstreamingz.fr/category/horreur/'] )
    liste.append( ['Musical','http://filmstreamingz.fr/category/musical/'] )
    liste.append( ['Policier','http://filmstreamingz.fr/category/policier/'] )
    liste.append( ['Romance','http://filmstreamingz.fr/category/romance/'] )
    liste.append( ['Science-Fiction','http://filmstreamingz.fr/category/science-fiction/'] )
    liste.append( ['Spectacle','http://filmstreamingz.fr/category/spectacle/'] )
    liste.append( ['Thriller','http://filmstreamingz.fr/category/thriller/'] )
    liste.append( ['Western','http://filmstreamingz.fr/category/western/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('//ad.advertstream.com/', '').replace('http://www.adcash.com/', '').replace('http://regie.espace-plus.net/', '')
    sPattern = '<div class="moviefilm"><a href=".+?"><img src="([^<]+)" alt=".+?" height=".+?" width=".+?" /></a><div class="movief"><a href="([^<]+)">([^<]+)</a></div><div class="movies"><small>(.+?)</small></div></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sSmall = aEntry[3].replace('<span class="likeThis">', '').replace('</span>', '')
            sTitle = aEntry[2]+' - [COLOR azure]'+sSmall+'[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            if 'series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, '', aEntry[0], '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], '', oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sUrl = sUrl+'100/'
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<a href="([^<]+)"><span>(.+?)</span></a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            sTitle = sMovieTitle+' - '+aEntry[1]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<span class=\'current\'>.+?</span><a class="page larger" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sUrl = aResult[1][0]
        return sUrl

    return False


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','')


    sPattern = '<iframe.+?src=[\'|"](.+?)[\'|"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = str(aEntry)
            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()


def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    sPattern = 'href="([^<]+)" target="_blank">.+?</a>'
    oParser = cParser()
    aResult = oParser.parse(sUrl, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = str(aEntry)
            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
