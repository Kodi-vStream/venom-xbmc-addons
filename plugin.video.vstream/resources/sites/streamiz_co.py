#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'streamiz_co'
SITE_NAME = 'Streamiz'
SITE_DESC = 'Tous vos films en streaming gratuitement'

URL_MAIN = 'https://www.streamiz.co/'

MOVIE_NEWS = (URL_MAIN + 'recemment-ajoute/','showMovies')
MOVIE_VIEWS = (URL_MAIN + 'les-plus-vus/', 'showMovies')
MOVIE_ANNEES = (True, 'showMovieAnnees')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = ('https://api.streamiz.co/movies/search/?query=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load(): 
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les Plus Vus)', 'films_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'films_annees.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showMoviesSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
        
def showMovieAnnees():
    oGui = cGui()
	
    liste = []
    liste.append( ['2017',URL_MAIN + 'annee/2017/'] )
    liste.append( ['2016',URL_MAIN + 'annee/2016/'] )
    liste.append( ['2015',URL_MAIN + 'annee/2015/'] )
    liste.append( ['2014',URL_MAIN + 'annee/2014/'] )
    liste.append( ['2013',URL_MAIN + 'annee/2013/'] )
    liste.append( ['2012',URL_MAIN + 'annee/2012/'] )
    liste.append( ['2011',URL_MAIN + 'annee/2011/'] )
    liste.append( ['2010',URL_MAIN + 'annee/2010/'] )
    liste.append( ['2009',URL_MAIN + 'annee/2009/'] )
    liste.append( ['2008',URL_MAIN + 'annee/2008/'] )
    liste.append( ['2007',URL_MAIN + 'annee/2007/'] )
    liste.append( ['2006',URL_MAIN + 'annee/2006/'] )
    liste.append( ['2005',URL_MAIN + 'annee/2005/'] )
    liste.append( ['2004',URL_MAIN + 'annee/2004/'] )
    liste.append( ['2003',URL_MAIN + 'annee/2003/'] )
    liste.append( ['2002',URL_MAIN + 'annee/2002/'] )
    liste.append( ['2001',URL_MAIN + 'annee/2001/'] )
    liste.append( ['2000',URL_MAIN + 'annee/2000/'] )
    liste.append( ['1999',URL_MAIN + 'annee/1999/'] )
    liste.append( ['1998',URL_MAIN + 'annee/1998/'] )
    liste.append( ['1997',URL_MAIN + 'annee/1997/'] )
    liste.append( ['1996',URL_MAIN + 'annee/1996/'] )
    liste.append( ['1995',URL_MAIN + 'annee/1995/'] )
    
    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def showGenres():
    oGui = cGui()

    liste = []

    liste.append( ['Action',URL_MAIN + 'action/'] )
    liste.append( ['Animation',URL_MAIN + 'animation/'] )
    liste.append( ['Aventure',URL_MAIN + 'aventure/'] )
    liste.append( ['Comédie',URL_MAIN + 'comedie/'] )
    liste.append( ['Crime',URL_MAIN + 'crime/'] )
    liste.append( ['Documentaire',URL_MAIN + 'documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'drame/'] )
    liste.append( ['Etranger',URL_MAIN + 'etranger/'] )
    liste.append( ['Familiale',URL_MAIN + 'familiale/'] )
    liste.append( ['Fantastique',URL_MAIN + 'fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + 'guerre/'] )
    liste.append( ['Histoire',URL_MAIN + 'histoire/'] )
    liste.append( ['Horreur',URL_MAIN + 'horreur/'] )
    liste.append( ['Musique',URL_MAIN + 'musique/'] )
    liste.append( ['Mystere',URL_MAIN + 'mystere/'] )
    liste.append( ['Romance',URL_MAIN + 'romance/'] )
    liste.append( ['Science-Fiction',URL_MAIN + 'science-fiction/'] )
    liste.append( ['Téléfilm',URL_MAIN + 'telefilm/'] )
    liste.append( ['Thriller',URL_MAIN + 'thriller/'] )
    liste.append( ['Western',URL_MAIN + 'western/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    if sSearch:
        sUrl = sSearch
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
        
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #indispensable
    sHtmlContent = sHtmlContent.replace("\t","")
    sHtmlContent = sHtmlContent.replace("\n","")

    sPattern = '<div class="movie_last"><a href="([^"]+)".+?<img src="([^"]+)".+?<div class="title">(.+?)<\/div>.+?<p class="nop synopsis">(.+?)</p>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]
            sSyn = aEntry[3].replace("&laquo;",'«').replace("&raquo;",'»').replace('  ',' ')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle,'', sThumb, sSyn, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = "<li class='active'>.+?<\/a><\/li><li><a.+?ref='(.+?)'>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    
    sPattern = '<div class="movie_player" data-id="(.+?)"'
    Fresult = oParser.parse(sHtmlContent, sPattern)
    if (Fresult[0] == True):
        sID = Fresult[1][0]
        oRequestHandler = cRequestHandler('https://api.streamiz.co/movies/'+sID+'/embeds')
        sHtmlContent = oRequestHandler.request()
        if sHtmlContent:
            sHtmlContent = sHtmlContent.replace('\\','')
            sHtmlContent = sHtmlContent.strip('[""]')

            sHosterUrl = sHtmlContent
            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
