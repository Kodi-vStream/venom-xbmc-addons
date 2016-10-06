#-*- coding: utf-8 -*-
#Venom & johngf.
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
import urllib

SITE_IDENTIFIER = 'fullmoviz_org'
SITE_NAME = 'FullMoviz.org'
SITE_DESC = 'Films complets en streaming et en Français sur Fullmoviz'

URL_MAIN = 'http://www.fullmoviz.org/'

MOVIE_MOVIE = (URL_MAIN + '?p=movies&orderby=name', 'showMovies')
MOVIE_NEWS = (URL_MAIN + '?p=movies&orderby=date', 'showMovies')
MOVIE_COMMENTS = (URL_MAIN + '?p=movies&orderby=comment_count', 'showMovies')
MOVIE_GENRES = (URL_MAIN + '', 'showGenre')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
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
        sUrl = URL_MAIN + '?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  

 
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action',URL_MAIN + 'category/action/'] )
    liste.append( ['Animation',URL_MAIN + 'category/animation/'] )
    liste.append( ['Art martiaux',URL_MAIN + 'category/art-martiaux/'] )
    liste.append( ['Aventure',URL_MAIN + 'category/aventure/'] )
    liste.append( ['Biographique',URL_MAIN + 'category/biographique/'] )
    liste.append( ['Comédie',URL_MAIN + 'category/comedie/'] )
    liste.append( ['Drame',URL_MAIN + 'category/drame/'] )
    liste.append( ['Epique',URL_MAIN + 'category/epique/'] )
    liste.append( ['Epouvante',URL_MAIN + 'category/epouvante/'] )
    liste.append( ['Familial',URL_MAIN + 'category/familial/'] )
    liste.append( ['Fantaisie',URL_MAIN + 'category/fantaisie/'] )
    liste.append( ['Film noir',URL_MAIN + 'category/film-noir'] )
    liste.append( ['Highlights',URL_MAIN + 'category/highlights/'] )
    liste.append( ['Historique',URL_MAIN + 'category/historique/'] )
    liste.append( ['Psychologique',URL_MAIN + 'category/psychologique'] )
    liste.append( ['Romance',URL_MAIN + 'category/romance/'] )
    liste.append( ['Science-fiction',URL_MAIN + 'category/science-fiction/'] )
    liste.append( ['Thriller',URL_MAIN + 'category/thriller/'] )
                
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
    
    oParser = cParser()
    
    sPattern = '<div class="post-thumbnail"><a href="([^<]+)" title="([^"]+)"><img [^<>]+src="([^"]+)".+?<p>([^<>]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[1]
            bliste = ['Film Complet en Streaming','en streaming','streaming','sreaming']
            for item in bliste:
                if item in aEntry[1]:
                   sTitle = sTitle.replace(item,'')
            
            sThumb = aEntry[2]
            sThumb = urllib.quote(sThumb, safe=':/')
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)           
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, aEntry[3], oOutputParameterHandler)
         
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
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()

    sPattern = '<iframe.+?src=[\'|"](.+?)[\'|"]'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = str(aEntry)
            
            if 'filmzenstream.com' in sHosterUrl:
                if not sHosterUrl.startswith('http'):
                    sHosterUrl = 'http:' + sHosterUrl
                oRequestHandler = cRequestHandler(sHosterUrl)
                sHtmlContent = oRequestHandler.request()
                sPattern = 'file: *"([^"]+)"'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if (aResult[0] == True):
                    sHosterUrl = aResult[1][0]
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
        
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
