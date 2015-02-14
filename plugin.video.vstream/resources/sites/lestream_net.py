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

SITE_IDENTIFIER = 'lestream_net'
SITE_NAME = 'Lestream.net'
SITE_DESC = 'films en streaming, vk streaming, youwatch, vimple , streaming hd , streaming 720p , streaming sans limite'

URL_MAIN = 'http://www.lestream.net/'

MOVIE_NEWS = ('http://www.lestream.net/films', 'showMovies') 
MOVIE_VIEWS = ('http://www.lestream.net/films-populaires/', 'showMovies')
MOVIE_GENRES = True 
SERIE_SERIES = ('http://www.lestream.net/serie-tv', 'showMovies')

URL_SEARCH = ('http://www.lestream.net/index.php?menu=searchmov&query=','showMovies')
FUNCTION_SEARCH = 'showMovies'


def load(): 
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler) 
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films Les plus vues', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genre', 'genres.png', oOutputParameterHandler)

    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)
    
            
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://www.lestream.net/index.php?menu=searchmov&query='+sSearchText
            showMovies(sUrl) 
            oGui.setEndOfDirectory()
            return  
    
    
def showGenre():
    oGui = cGui()
 
    liste = []
    liste.append( ['Action','http://www.lestream.net/filmtag/action'] )
    liste.append( ['Animation','http://www.lestream.net/filmtag/animation'] )
    liste.append( ['Arts Martiaux','http://www.lestream.net/filmtag/arts_martiaux'] )
    liste.append( ['Aventure','http://www.lestream.net/filmtag/aventure'] )
    liste.append( ['Biopic','http://www.lestream.net/filmtag/biographies'] )
    liste.append( ['Comedie','http://www.lestream.net/filmtag/comdie'] )
    liste.append( ['Comedie Dramatique','http://www.lestream.net/filmtag/comdie_dramatique'] )
    liste.append( ['Documentaire','http://www.lestream.net/filmtag/documentaire'] )
    liste.append( ['Drame','http://www.lestream.net/filmtag/drame'] )
    liste.append( ['Epouvante Horreur','http://www.lestream.net/filmtag/epouvantehorreur'] ) 
    liste.append( ['Espionnage','http://www.lestream.net/filmtag/espionnage'] )
    liste.append( ['Famille','http://www.lestream.net/filmtag/famille'] )
    liste.append( ['Fantastique','http://www.lestream.net/filmtag/fantastique'] )  
    liste.append( ['Guerre','http://www.lestream.net/filmtag/guerre'] )
    liste.append( ['Historique','http://www.lestream.net/filmtag/historique'] )
    liste.append( ['Musical','http://www.lestream.net/filmtag/musical_'] )
    liste.append( ['Policier','http://www.lestream.net/filmtag/policier'] )
    liste.append( ['Peplum','http://www.lestream.net/filmtag/pplum'] )
    liste.append( ['Romance','http://www.lestream.net/filmtag/romance'] )
    liste.append( ['Science Fiction','http://www.lestream.net/filmtag/science_fiction'] )
    liste.append( ['Spectacle','http://www.lestream.net/filmtag/spectacles'] )
    liste.append( ['Thriller','http://www.lestream.net/filmtag/thriller'] )
    liste.append( ['Western','http://www.lestream.net/filmtag/western'] )
    liste.append( ['Divers','http://www.lestream.net/filmtag/divers'] ) 
	
                
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
    if '/serie-tv' in sUrl:
        sPattern = '<a class="entry-thumbnails-link" href="([^<]+)"><img src="(.+?)" .+?/>.+?<h3 class="entry-title"><a href=".+?" rel="bookmark">(.+?)</a></h3><div class="entry-summary" style=".+?">(.+?)</div>'
    else:
        sPattern = '<a class="tooltips"  href="([^<]+)"> <img src="(.+?)" .*?alt="(.+?)" />.+?<br />(.+?)</span>'
        
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = aEntry[2].decode('latin-1').encode("utf-8")
            sDesc = aEntry[3].decode('latin-1').encode("utf-8")
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0])) 
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle)) 
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1]))
            
            

            if '/serie-tv' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle,'', aEntry[1], sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[1], sDesc, oOutputParameterHandler)
                
        cConfig().finishDialog(dialog)#dialog
           
        sNextPage = __checkForNextPage(sHtmlContent)#cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'class="current">.+?</a>.+?<a href="(.+?)">.+?</a>'
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
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','').replace('<iframe src=\'http://creative.rev2pub.com','')   

    sPattern = '<iframe.+?src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    print aResult
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
                
    oGui.setEndOfDirectory()

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
 
    sPattern = '<h3 class="entry-title"><a href="([^<]+)" rel="bookmark">(.+?)</a></h3>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[1].decode('latin-1').encode("utf-8")
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)            
    
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
               
    sPattern = '<h3 class="entry-title"><a href="([^<]+)" rel="bookmark">(.+?)</a></h3>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            sHosterUrl = str(aEntry[0])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(aEntry[1])
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
                
    oGui.setEndOfDirectory()    