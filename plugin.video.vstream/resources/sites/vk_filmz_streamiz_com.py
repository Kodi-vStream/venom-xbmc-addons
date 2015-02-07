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

SITE_IDENTIFIER = 'vk_filmz_streamiz_com'
SITE_NAME = 'Vk-Filmz-Streamiz.com'
SITE_DESC = 'films en streaming, vk streaming, youwatch, vimple , streaming hd , streaming 720p , streaming sans limite'

URL_MAIN = 'http://vk-filmz-streamiz.com'

MOVIE_NEWS = ('http://vk-filmz-streamiz.com/lastmovies/', 'showMovies')
MOVIE_GENRES = (True, 'showGenre')
SERIE_SERIES = ('http://vk-filmz-streamiz.com/series/', 'showMovies')
SERIE_VFS = ('http://vk-filmz-streamiz.com/series/version-francaise', 'showMovies')
SERIE_VOSTFRS = ('http://vk-filmz-streamiz.com/series/vostfr', 'showMovies')
ANIM_VOSTFRS = ('http://vk-filmz-streamiz.com/mangas/mangas-vostfr/', 'showMovies')

URL_SEARCH = ('http://vk-filmz-streamiz.com/?do=search&subaction=search&story=', 'showMovies')
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
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series Nouveautés', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series VF', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series VOSTFR', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Animes VOSTFR', 'animes.png', oOutputParameterHandler)
    
            
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://vk-filmz-streamiz.com/?do=search&subaction=search&story='+sSearchText  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
    
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action','http://vk-filmz-streamiz.com/films/action'] )
    liste.append( ['Animation','http://vk-filmz-streamiz.com/films/animation'] )
    liste.append( ['Arts Martiaux','http://vk-filmz-streamiz.com/films/arts-martiaux'] )
    liste.append( ['Aventure','http://vk-filmz-streamiz.com/films/aventure'] )
    liste.append( ['Biopic','http://vk-filmz-streamiz.com/films/biopic'] )
    liste.append( ['Comedie','http://vk-filmz-streamiz.com/films/comedie'] )
    liste.append( ['Comedie Dramatique','http://vk-filmz-streamiz.com/films/comedie-dramatique'] )
    liste.append( ['Comedie Musicale','http://vk-filmz-streamiz.com/films/comedie-musicale'] )
    liste.append( ['Disney','http://vk-filmz-streamiz.com/films/disney'] )
    liste.append( ['Divers','http://vk-filmz-streamiz.com/films/divers'] )    
    liste.append( ['Documentaire','http://vk-filmz-streamiz.com/films/documentaire'] )
    liste.append( ['Drame','http://vk-filmz-streamiz.com/films/drame'] )
    liste.append( ['Epouvante Horreur','http://vk-filmz-streamiz.com/films/horreur'] ) 
    #liste.append( ['Erotique','http://full-streaming.org/erotique'] )
    liste.append( ['Espionnage','http://vk-filmz-streamiz.com/films/espionnage'] )
    liste.append( ['Famille','http://vk-filmz-streamiz.com/films/famille'] )
    liste.append( ['Fantastique','http://vk-filmz-streamiz.com/films/fantastique'] )  
    liste.append( ['Guerre','http://vk-filmz-streamiz.com/films/guerre'] )
    liste.append( ['Historique','http://vk-filmz-streamiz.com/films/historique'] )
    liste.append( ['Musical','http://vk-filmz-streamiz.com/films/musical'] )
    liste.append( ['Policier','http://vk-filmz-streamiz.com/films/policier'] )
    liste.append( ['Romance','http://vk-filmz-streamiz.com/films/romance'] )
    liste.append( ['Science Fiction','http://vk-filmz-streamiz.com/films/science-fiction'] )
    liste.append( ['Spectacle','http://vk-filmz-streamiz.com/films/spectacles'] )
    liste.append( ['Thriller','http://vk-filmz-streamiz.com/films/triller'] )
                
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
    liste.append( ['HD','http://vk-filmz-streamiz.com/films-hd'] )
    liste.append( ['DvdRip','http://vk-filmz-streamiz.com/quality/dvdrip'] )
    liste.append( ['BdRip','http://vk-filmz-streamiz.com/quality/bdrip'] )
    liste.append( ['R5','http://vk-filmz-streamiz.com/quality/R5'] )
    liste.append( ['Cam Rip','http://vk-filmz-streamiz.com/quality/camrip'] )
    liste.append( ['TS','http://vk-filmz-streamiz.com/quality/ts'] )

    
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films.png', oOutputParameterHandler)
       
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
    #sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')
    sPattern = '<img class="tubeposter" src="([^<]+)" alt=".+?" title=".+?" />.+?<h2 class="mtitle"><a href="([^<]+)">([^<]+)</a></h2>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle=re.sub('(.*)(\[.*\])','\\1 [COLOR azure]\\2[/COLOR]', str(aEntry[2]))
            sMovieTitle=re.sub('(\[.*\])','', str(aEntry[2]))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))

            if '/series/' in sUrl or '/series/' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle,'', aEntry[0], '', oOutputParameterHandler)
            elif '/mangas/' in sUrl or '/mangas/' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'mangasHosters', sTitle,'', aEntry[0], '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], '', oOutputParameterHandler)
           
    
        cConfig().finishDialog(dialog)
        

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<div class="navigation ignore-select">.+?<span>.+?</span> <a href="(.+?)">.+?</a>'
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
               
        
    sPattern = '<iframe.+?src="(.+?)"'
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
    
def seriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('http://creative.rev2pub.com','')
               
    sPattern = '<h2><img src=".+?" style="margin-right:5px" alt="" />([^<]+)</h2>|<a href="([^<]+)" target="vk-filmz" id="(.+?)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addDir(SITE_IDENTIFIER, 'seriesHosters', '[COLOR red]'+str(aEntry[0])+'[/COLOR]', 'host.png', oOutputParameterHandler)
                   
            
            sHosterUrl = str(aEntry[1])
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sTitle = sMovieTitle+'[COLOR azure]'+aEntry[2]+'[/COLOR]'
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
        cConfig().finishDialog(dialog)
                
    oGui.setEndOfDirectory()

def mangasHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('http://creative.rev2pub.com','')
               
    sPattern = '<a target="vk-filmz" href="(.+?)">(.+?)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sHosterUrl = str(aEntry[0])
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sTitle = sMovieTitle+' [COLOR azure]'+aEntry[1]+'[/COLOR]'
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
        cConfig().finishDialog(dialog)
                
    oGui.setEndOfDirectory()
    