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
from resources.lib.util import cUtil
from resources.lib.config import cConfig
import re, urllib

SITE_IDENTIFIER = 'zdstream_org'
SITE_NAME = 'Zdstream.org'
SITE_DESC = 'Film streaming, film gratuit, film en streaming, Streaming Film, site de streaming, serie streaming, series en sreaming,  streaming gratuit regarder film'

URL_MAIN = 'http://zdstream.org/'

MOVIE_NEWS = ('http://zdstream.org/', 'showMovies')
MOVIE_VIEWS = ('http://zdstream.org/les-plus-vues/', 'showMovies')
MOVIE_COMMENTS = ('http://zdstream.org/les-plus-commentes/', 'showMovies')
MOVIE_POPULAIRES = ('http://zdstream.org/les-plus-populaires/', 'showMovies')
MOVIE_GENRES = (True, 'showGenre') 
SERIE_SERIES = ('http://zdstream.org/genre/series-tv', 'showMovies')

URL_SEARCH = ('http://zdstream.org/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Nouveautés', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus Vues', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus Commentés', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_POPULAIRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus Populaires', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showQlt', 'Films Qualités', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showPys', 'Films Pays', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showPlt', 'Films Plateformes', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series Nouveautés', 'series.png', oOutputParameterHandler)
    
            
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://zdstream.org/?s='+sSearchText  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return
                      
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action','http://zdstream.org/genre/action/'] )
    liste.append( ['Animation','http://zdstream.org/genre/animation/'] )
    liste.append( ['Aventure','http://zdstream.org/genre/aventure/'] )
    liste.append( ['Biopic','http://zdstream.org/genre/biopic/'] )
    liste.append( ['Comedie','http://zdstream.org/genre/comedie/'] )
    liste.append( ['Comedie dramatique','http://zdstream.org/genre/comedie-dramatique/'] )
    liste.append( ['Comedie musicale','http://zdstream.org/genre/comedie-musicale/'] )
    liste.append( ['Drame','http://zdstream.org/genre/drame/'] )
    liste.append( ['Epouvante horreur','http://zdstream.org/genre/epouvante-horreur/'] )
    liste.append( ['Espionage','http://zdstream.org/genre/espionnage/'] )
    liste.append( ['Famille','http://zdstream.org/genre/famille/'] ) 
    liste.append( ['Fantastique','http://zdstream.org/genre/fantastique/'] )
    liste.append( ['Guerre','http://zdstream.org/genre/guerre/'] )
    liste.append( ['Historique','http://zdstream.org/genre/historique/'] )
    liste.append( ['judiciaire','http://zdstream.org/genre/judiciaire/'] )
    liste.append( ['Policier','http://zdstream.org/genre/policier/'] )
    liste.append( ['Romance','http://zdstream.org/genre/romance/'] )
    liste.append( ['Science Fiction','http://zdstream.org/genre/science-fiction/'] )
    liste.append( ['Thriller','http://zdstream.org/genre/thriller/'] )
    liste.append( ['Western','http://zdstream.org/genre/western/'] )
    
    for sTitle,sUrl in liste:
                
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
        
def showQlt():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['DVDRIP','http://zdstream.org/qualite/dvdrip/'] )
    liste.append( ['BDRIP','http://zdstream.org/qualite/bdrip/'] )
    liste.append( ['R5','http://zdstream.org/qualite/r5/'] )
    liste.append( ['CAM','http://zdstream.org/qualite/cam/'] )
    liste.append( ['DVDSCR','http://zdstream.org/qualite/dvdscr/'] ) 
    
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()
        
def showPys():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Americain','http://zdstream.org/pays/americain/'] )
    liste.append( ['Francais','http://zdstream.org/pays/francais/'] )
    liste.append( ['Britannique','http://zdstream.org/pays/britannique/'] )
    liste.append( ['Allemand','http://zdstream.org/pays/allemand/'] )
    liste.append( ['Belge','http://zdstream.org/pays/belge/'] ) 
    liste.append( ['Canadien','http://zdstream.org/pays/canadien/'] )
    liste.append( ['Italien','http://zdstream.org/pays/italien/'] )
    liste.append( ['Coreen','http://zdstream.org/pays/coreen/'] )
    liste.append( ['Japonais','http://zdstream.org/pays/japonais/'] )
    liste.append( ['Australien','http://zdstream.org/pays/australien/'] ) 
    
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()
        
def showPlt():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Youwatch','http://zdstream.org/plateformes/youwatch/'] )
    liste.append( ['Exashare','http://zdstream.org/plateformes/exashare/'] )
    liste.append( ['Nowvideo','http://zdstream.org/plateformes/nowvideo/'] )
    liste.append( ['NETU','http://zdstream.org/plateformes/netu/'] )
    liste.append( ['Speedvideo','http://zdstream.org/plateformes/speedvideo/'] )
    liste.append( ['VK','http://zdstream.org/plateformes/vk/'] ) 
    
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()
        
        
# def showMovies(sSearch = ''):
    # oGui = cGui()
    # if sSearch:
      # sUrl = sSearch
    # else:
        # oInputParameterHandler = cInputParameterHandler()
        # sUrl = oInputParameterHandler.getValue('siteUrl')
   
    # oRequestHandler = cRequestHandler(sUrl) 
    # sHtmlContent = oRequestHandler.request(); 
    # if '/serie-tv' in sUrl:
        # sPattern = '<a class="entry-thumbnails-link" href="([^<]+)"><img src="(.+?)" .+?/>.+?<h3 class="entry-title"><a href=".+?" rel="bookmark">(.+?)</a></h3><div class="entry-summary" style=".+?">(.+?)</div>'
    # else:
        # sPattern = '<a class="tooltips"  href="([^<]+)"> <img src="(.+?)" .*?alt="(.+?)" />.+?<br />(.+?)</span>'
       
    # oGui.setEndOfDirectory()   
    
   
    # oRequestHandler = cRequestHandler(sUrl)
    # sHtmlContent = oRequestHandler.request();
 
    # sPattern = '<li><atitle=".+?" href="([^<]+)">(.+?)</a> <spanclass="mctagmap_count">(.+?)</span>'
    
    # oParser = cParser()
    # aResult = oParser.parse(sHtmlContent, sPattern)
    # if (aResult[0] == True):
        # for aEntry in aResult[1]:

            # sTitle = aEntry[1]+' - '+aEntry[2]
            
            # oOutputParameterHandler = cOutputParameterHandler()
            # oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            # oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
           
    # oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')
    sPattern = '<div.*?class="moviefilm">.*?<a.*?href="([^<]+)">.+?<img.*?src="([^<]+)" alt="(.+?)".+?>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult
    if (aResult[0] == False):
        oGui.addNone(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            #sTitle = aEntry[2]+' - [COLOR azure]'+aEntry[3]+'[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1]))
            if '/series-tv' in sUrl or '/series-tv' in aEntry[0]:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', aEntry[2],'', aEntry[1], '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', aEntry[2], '', aEntry[1], '', oOutputParameterHandler)           
    
        cConfig().finishDialog(dialog)

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
    sUrl = sUrl+'/100/'
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<strong>Téléchargement VOSTFR','').replace('<strong>Téléchargement VF','').replace('<strong>Téléchargement','')
 
    sPattern = '<ahref="([^<]+)"><span>(.+?)</span></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle+' - '+aEntry[1]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler) 
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<aclass="page larger" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
    
  
def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sUrl = sUrl+'/100/'
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','')
               
    sPattern = '<ahref="([^<]+)"><span>(.+?)</span></a>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sHoster = cHosterGui().checkHoster(aEntry[1].lower())
            if (sHoster != False):
                sTitle = sMovieTitle+' - [COLOR azure]'+aEntry[1]+'[/COLOR]'
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()  

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','').replace('<iframesrc="http://www.facebook.com/','').replace('<iframesrc="//www.facebook.com/','').replace('<iframe src="http://www.facebook.com/', '')
               
        
    sPattern = 'iframe.*?src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult
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
    
def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','').replace('<iframesrc="http://www.facebook.com/','').replace('<iframesrc="//www.facebook.com/','').replace('<iframe src="http://www.facebook.com/', '')
               
        
    sPattern = 'iframe.*?src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult
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
    