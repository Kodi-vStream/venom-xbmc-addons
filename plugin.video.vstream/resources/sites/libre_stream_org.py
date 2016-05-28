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

SITE_IDENTIFIER = 'libre_stream_org'
SITE_NAME = 'Libre-stream.com'
SITE_DESC = 'films en streaming, vk streaming, youwatch, vimple , streaming hd , streaming 720p , streaming sans limite'

URL_MAIN = 'http://libre-stream.com/'

MOVIE_MOVIE = (URL_MAIN + 'films/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = (True, 'showGenre')

SERIE_SERIE = (URL_MAIN + 'liste-des-series/', 'AlphaSearch')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_VFS = (URL_MAIN + 'series/version-francaise/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'series/vostfr', 'showMovies')

URL_SEARCH = (URL_MAIN + '?q=', 'showMovies')
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
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genre', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showQlt', 'Films Qualités', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries Nouveautés', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries VF', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries VOSTFR', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIE[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIE[1], 'Series Liste Complete', 'series.png', oOutputParameterHandler)    
             
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText  
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action',URL_MAIN + 'films/action/'] )
    liste.append( ['Animation',URL_MAIN + 'films/animation'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'films/arts-martiaux'] )
    liste.append( ['Aventure',URL_MAIN + 'films/aventure'] )
    liste.append( ['Biopic',URL_MAIN + 'films/biopic'] )
    liste.append( ['Comedie',URL_MAIN + 'films/comedie'] )
    liste.append( ['Comedie Dramatique',URL_MAIN + 'films/comedie-dramatique'] )
    liste.append( ['Comedie Musicale',URL_MAIN + 'films/comedie-musicale'] )
    liste.append( ['Disney',URL_MAIN + 'films/disney'] )
    liste.append( ['Divers',URL_MAIN + 'films/divers'] )    
    liste.append( ['Documentaire',URL_MAIN + 'films/documentaire'] )
    liste.append( ['Drame',URL_MAIN + 'films/drame'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'films/horreur'] ) 
    liste.append( ['Espionnage',URL_MAIN + 'films/espionnage'] )
    liste.append( ['Famille',URL_MAIN + 'film/famille'] )
    liste.append( ['Fantastique',URL_MAIN + 'film/fantastique'] )  
    liste.append( ['Guerre',URL_MAIN + 'film/guerre'] )
    liste.append( ['Historique',URL_MAIN + 'film/historique'] )
    liste.append( ['Musical',URL_MAIN + 'film/musical'] )
    liste.append( ['Policier',URL_MAIN + 'film/policier'] )
    liste.append( ['Romance',URL_MAIN + 'film/romance'] )
    liste.append( ['Science Fiction',URL_MAIN + 'film/science-fiction'] )
    liste.append( ['Spectacle',URL_MAIN + 'film/spectacles'] )
    liste.append( ['Thriller',URL_MAIN + 'film/triller'] )
                
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
    liste.append( ['HD',URL_MAIN + 'films-hd/'] )
    liste.append( ['DvdRip',URL_MAIN + 'quality/dvdrip/'] )
    liste.append( ['BdRip',URL_MAIN + 'quality/bdrip/'] )
    liste.append( ['R5',URL_MAIN + 'quality/R5/'] )
    liste.append( ['Cam Rip',URL_MAIN + 'quality/camrip/'] )
    liste.append( ['TS',URL_MAIN + 'quality/ts/'] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def AlphaSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    dialog = cConfig().createDialog(SITE_NAME)
    
    for i in range(0,36) :
        cConfig().updateDialog(dialog, 36)
        if dialog.iscanceled():
            break
        
        if (i < 10):
            sTitle = chr(48+i)
        else:
            sTitle = chr(65+i-10)
            
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + sTitle.lower() + '.html' )
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'AlphaDisplay', '[COLOR teal] Lettre [COLOR red]'+ sTitle +'[/COLOR][/COLOR]', 'genres.png', oOutputParameterHandler)
        
    cConfig().finishDialog(dialog)
    
    oGui.setEndOfDirectory()
        
def AlphaDisplay():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a href="([^<>"]+?)">([^<>"]+?)<\/a><br\/>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sTitle = aEntry[1]
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sDisplayTitle, '', '','', oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
        
        oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<div class="libre-movie libre-movie-block">.+?data-src="(.+?)".+?title="(.+?)".+?<h2 onclick="window.location.href=\'(.+?)\'">'
    if '/films/' in sUrl:
        sPattern = sPattern + '.+?<div class="maskquality (.+?)">'
        
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0],''),aEntry[1]) == 0:
                    continue
            
            sMovieTitle = str(aEntry[1])
                
            #Si recherche et trop de resultat, on nettoye
            #if sSearch and total > 4:
            #    if cUtil().CheckOccurence(sUrl.replace(URL_SEARCH[0],''),sMovieTitle) == 0:
            #        continue

            if '/films/' in sUrl:
                sMovieTitle = sMovieTitle + ' [' + str(aEntry[3]) + ']'
                
            sTitle = cUtil().DecoTitle(sMovieTitle)
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))

            if '/series/' in sUrl or '-saison-' in aEntry[2]:
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sDisplayTitle,'', aEntry[0], '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', aEntry[0], '', oOutputParameterHandler)
           
    
        cConfig().finishDialog(dialog)
        

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^<>""]+?)"><i class="fa fa-angle-right"></i></a>'
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
    sHtmlContent = sHtmlContent.replace('http://creative.rev2pub.com','')
               
        
    sPattern = '<iframe.+?src=[\'"]([^<>\'"]+?)[\'"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    sDisplayTitle = cUtil().DecoTitle(sMovieTitle)

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
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
        cConfig().finishDialog(dialog)
                
    oGui.setEndOfDirectory()
    
def seriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
               
    oParser = cParser()          
    sPattern = '<div class="e-number">.+?<iframe src="(.+?)".+?class="episode-id">(.+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = sMovieTitle + ' ' + str(aEntry[1])
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            sHosterUrl = str(aEntry[0])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
        cConfig().finishDialog(dialog)
                
    oGui.setEndOfDirectory()
