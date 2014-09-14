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
SITE_DESC = 'Films complets en streaming et en Français sur Fullmoviz. Liste de sorties cinéma streaming. Top streaming FR.'

URL_MAIN = 'http://www.fullmoviz.org/'
MOVIE_NEWS = 'http://www.fullmoviz.org/?p=movies&orderby=date'
MOVIE_COMMENTS = 'http://www.fullmoviz.org/?p=movies&orderby=comment_count'
MOVIE_GENRES = 'http://www.fullmoviz.org/'

def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Nouveautés', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS)
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus commentés', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES)
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
    sHtmlContent = sHtmlContent.replace('&#039;', '\'')
    
    sPattern = '<div class="loop-thumb"><a href="([^<]+)"><img width=".+?" height=".+?" src="([^<]+)" class="attachment-loop wp-post-image" alt="(.+?)" /></a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)

            #sTitle = aEntry[2].decode('latin-1').encode("utf-8")
            #sThumbnail = 'http:'+str(aEntry[2])
            #sUrl = URL_MAIN+str(aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1]))            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', aEntry[2], '', aEntry[1], '', oOutputParameterHandler)
         
        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = "<span class='page-numbers current'>.+?</span><a class='page-numbers' href='([^<]+)'>.+?</a>"
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

            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
        
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
    