#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re

from resources.lib.sucuri import SucurieBypass
 
SITE_IDENTIFIER = 'film_illimit_fr'
SITE_NAME = 'Film illimite'
SITE_DESC = 'Films HD en streaming'
 
#URL_MAIN = 'http://xn--official-film-illimit-v5b.fr/'
URL_MAIN = 'http://official-film-illimite.net/'

MOVIE_NEWS = (URL_MAIN + 'film-de-a-a-z/', 'showMovies')
MOVIE_HD = (URL_MAIN + '720p1080p/', 'showMovies')
MOVIE_MOVIE = (True, 'showAlpha')
MOVIE_GENRES = (True, 'showGenre')

SERIE_NEWS = (URL_MAIN + 'serie-tv/', 'showMovies')
  
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
 
def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films A-Z', 'news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films HD', 'news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films par Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries', 'series.png', oOutputParameterHandler)
            
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
 
    liste = []
    liste.append( ['Action',URL_MAIN + 'action-aventure/'] )
    liste.append( ['Animation',URL_MAIN + 'animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'arts-martiaux/'] )
    liste.append( ['Biographie',URL_MAIN + 'biographique/'] )
    liste.append( ['Comedie',URL_MAIN + 'comedie/'] )
    liste.append( ['Drame',URL_MAIN + 'drame/'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'epouvante-horreur/'] )
    liste.append( ['Fantastique',URL_MAIN + 'fantastique/'] )  
    liste.append( ['Famille',URL_MAIN + 'famille/'] )
    liste.append( ['Guerre',URL_MAIN + 'guerre/'] )
    liste.append( ['Policier',URL_MAIN + 'policier/'] )
    liste.append( ['Romance',URL_MAIN + 'romance/'] )
    liste.append( ['Science Fiction',URL_MAIN + 'science-fiction/'] )
    liste.append( ['Thriller/Suspense',URL_MAIN + 'thrillersuspense/'] )
    liste.append( ['720p/1080p',URL_MAIN + '720p1080p/'] )
    liste.append( ['Mystère',URL_MAIN + 'mystere/'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def showAlpha():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    dialog = cConfig().createDialog(SITE_NAME)

    for i in range(0,27) :
        cConfig().updateDialog(dialog, 27)
        if dialog.iscanceled():
            break
        
        sTitle = chr(64+i)
        sUrl = URL_MAIN + 'film-de-a-a-z/lettre-' + chr(96+i) + '/'
        
        if sTitle == '@':
            sTitle= '[0-9]'
            sUrl = URL_MAIN + 'film-de-a-a-z/0-9/'
          
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addTV(SITE_IDENTIFIER, 'showMovies','[COLOR teal] Lettre [COLOR red]'+ sTitle +'[/COLOR][/COLOR]','', '', '', oOutputParameterHandler)
        
    cConfig().finishDialog(dialog)
    
    oGui.setEndOfDirectory()
 
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sSearch = sSearch.replace(' ','+')
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request()
    sHtmlContent = SucurieBypass().GetHtml(sUrl)
    
    sPattern = 'class="item"> *<a href="([^<]+)">.+?<img src="([^<>"]+?)" alt="([^"]+?)".+?<span class="calidad2">(.+?)<\/span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == False):
        oGui.addNone(SITE_IDENTIFIER)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total) #dialog
            if dialog.iscanceled():
                break
                
            sName = aEntry[2].replace(' en Streaming HD','')
            sName = sName.replace(' Streaming HD','')
            sName = sName.decode('utf8')
            sName = cUtil().unescape(sName)
            try:
                sName = sName.encode("utf-8")
            except:
                pass
            
            sTitle = sName + ' [' + aEntry[3] + ']'
            sUrl = aEntry[0]
            sThumbnail = aEntry[1]
            
            if sThumbnail.startswith('//'):
                sThumbnail = 'http:' + sThumbnail

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
            oOutputParameterHandler.addParameter('sMovieTitle', sName)
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            if re.match('.+?saison [0-9]+',sTitle,re.IGNORECASE):
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, '', sThumbnail,'', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
            
 
        cConfig().finishDialog(dialog)
           
        if not sSearch:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
   
def __checkForNextPage(sHtmlContent):
    sPattern = "class='current'>.+?<a rel='nofollow' class='page larger' href='(.+?)'>"
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
    
    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request() 
    sHtmlContent = SucurieBypass().GetHtml(sUrl)
    
    #Vire les bandes annonces
    sHtmlContent = sHtmlContent.replace('src="https://www.youtube.com/', '')
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    sPattern = '<iframe[^<>]+?src="(http.+?)"'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult
   
    if (aResult[0] == True):

        for aEntry in aResult[1]:
                
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
 
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
       
    oGui.setEndOfDirectory()
    
def serieHosters():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request()
    sHtmlContent = SucurieBypass().GetHtml(sUrl)

    sHtmlContent = sHtmlContent.replace('<iframe width="420" height="315" src="https://www.youtube.com/', '')
    sPattern = '<div class="su-tabs-pane su-clearfix"><iframe.+?src="(http.+?)"[^<>]+?><\/iframe><\/div>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        i = 1
        for aEntry in aResult[1]:
                
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            
            sTitle = sMovieTitle + 'episode ' + str(i)
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            i = i + 1
 
            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
       
    oGui.setEndOfDirectory()
    
    
