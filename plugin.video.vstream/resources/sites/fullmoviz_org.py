#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.favourite import cFav
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'fullmoviz_org'
SITE_NAME = 'FullMoviz.org'
SITE_DESC = 'Films complets en streaming et en Français sur Fullmoviz'

URL_MAIN = 'http://www.fullmoviz.org/'

MOVIE_MOVIE = ('http://www.fullmoviz.org/?p=movies&orderby=name', 'showMovies')
MOVIE_NEWS = ('http://www.fullmoviz.org/?p=movies&orderby=date', 'showMovies')
MOVIE_COMMENTS = ('http://www.fullmoviz.org/?p=movies&orderby=comment_count', 'showMovies')
MOVIE_GENRES = ('http://www.fullmoviz.org/', 'showGenre')

URL_SEARCH = ('http://www.fullmoviz.org/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Nouveautés', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus commentés', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

    
def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://www.fullmoviz.org/?s='+sSearchText
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
    
 
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action','http://www.fullmoviz.org/category/action/'] )
    liste.append( ['Animation','http://www.fullmoviz.org/category/animation/'] )
    liste.append( ['Art martiaux','http://www.fullmoviz.org/category/art-martiaux/'] )
    liste.append( ['Aventure','http://www.fullmoviz.org/category/aventure/'] )
    liste.append( ['Biographique','http://www.fullmoviz.org/category/biographique/'] )
    liste.append( ['Comédie','http://www.fullmoviz.org/category/comedie/'] )
    liste.append( ['Drame','http://www.fullmoviz.org/category/drame/'] )
    liste.append( ['Epique','http://www.fullmoviz.org/category/epique/'] )
    liste.append( ['Epouvante','http://www.fullmoviz.org/category/epouvante/'] )
    liste.append( ['Familial','http://www.fullmoviz.org/category/familial/'] )
    liste.append( ['Fantaisie','http://www.fullmoviz.org/category/fantaisie/'] )
    liste.append( ['Film noir','http://www.fullmoviz.org/category/film-noir'] )
    liste.append( ['Highlights','http://www.fullmoviz.org/category/highlights/'] )
    liste.append( ['Historique','http://www.fullmoviz.org/category/historique/'] )
    liste.append( ['Psychologique','http://www.fullmoviz.org/category/psychologique'] )
    liste.append( ['Romance','http://www.fullmoviz.org/category/romance/'] )
    liste.append( ['Science-fiction','http://www.fullmoviz.org/category/science-fiction/'] )
    liste.append( ['Thriller','http://www.fullmoviz.org/category/thriller/'] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
    
    
def showMovies(sSearch=''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('&#039;', '\'').replace('&#46;', '')
    
    sPattern = '<div class="post-thumbnail"><a href="([^<]+)" title="(.+?)"><img width=".+?" height=".+?" src="(.+?)".+?>.+?<div class="entry excerpt entry-summary"><p>(.+?)</p></div>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[1].replace('Film Complet en Streaming', '')
            #sThumbnail = 'http:'+str(aEntry[2])
            #sUrl = URL_MAIN+str(aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[2], aEntry[3], oOutputParameterHandler)
         
        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<li class="next right"><a href="(.+?)".+?</a></li>'
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
    sHtmlContent = oRequestHandler.request();

    sPattern = '<iframe.+?src=[\'|"](.+?)[\'|"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
        
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
    
