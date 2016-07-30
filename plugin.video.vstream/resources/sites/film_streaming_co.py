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
from resources.lib.player import cPlayer
import re,urllib2,urllib

#copie du site http://www.film-streaming.co/
#copie du site http://www.streaming-club.com/
#copie du site http://www.hd-stream.in/


SITE_IDENTIFIER = 'film_streaming_co'
SITE_NAME = 'Film-streaming.co'
SITE_DESC = 'Le seul site de streaming en HD 720p 100% Gratuit'

URL_MAIN = 'http://www.film-streaming.co/'

 
MOVIE_NEWS = (URL_MAIN + 'index.php', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films.php', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'top.php', 'showMovies')
 
MOVIE_GENRES = (True, 'showGenre')
 
URL_SEARCH = (URL_MAIN + 'search.php?s=', 'showMovies')
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
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films les plus vus', 'top.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Tout Les Films', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genre', 'genres.png', oOutputParameterHandler)
           
    oGui.setEndOfDirectory()
 
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sSearchText = cUtil().urlEncode(sSearchText)
        sUrl = URL_SEARCH[0] + sSearchText 
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return 

def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Animation',URL_MAIN + 'genre.php?g=Animation'] )    
    liste.append( ['Action',URL_MAIN + 'genre.php?g=Action'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'genre.php?g=Arts%20Martiaux'] )
    liste.append( ['Aventure',URL_MAIN + 'genre.php?g=Aventure'] )
    liste.append( ['Biopic',URL_MAIN + 'genre.php?g=Biopic'] )
    liste.append( ['Comedie',URL_MAIN + 'genre.php?g=Com%C3%A9die'] )
    liste.append( ['Comedie Dramatique',URL_MAIN + 'genre.php?g=Com%C3%A9die%20dramatique'] )
    liste.append( ['Documentaire',URL_MAIN + 'genre.php?g=Documentaire'] )
    liste.append( ['Drame',URL_MAIN + 'genre.php?g=Drame'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'genre.php?g=Epouvante-horreur'] )
    liste.append( ['Espionage',URL_MAIN + 'genre.php?g=Espionnage'] )  
    liste.append( ['Fantastique',URL_MAIN + 'genre.php?g=Fantastique'] )
    liste.append( ['Famille',URL_MAIN + 'genre.php?g=Famille'] )
    liste.append( ['Guerre',URL_MAIN + 'genre.php?g=Guerre'] )
    liste.append( ['Historique',URL_MAIN + 'genre.php?g=Historique'] )
    liste.append( ['Musical',URL_MAIN + 'genre.php?g=Musical'] )
    liste.append( ['Policier',URL_MAIN + 'genre.php?g=Policier'] )
    liste.append( ['Romance',URL_MAIN + 'genre.php?g=Romance'] )
    liste.append( ['Sciense Fiction',URL_MAIN + 'genre.php?g=Science%20fiction'] )
    liste.append( ['Thriller',URL_MAIN + 'genre.php?g=Thriller'] )
    liste.append( ['Western',URL_MAIN + 'genre.php?g=Western'] )
               
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
    sHtmlContent = oRequestHandler.request()
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    sPattern = '<figure class="thumbnail thumbnail__portfolio"> <a href="([^"]+)" class="image-wrap" title="([^"]+)"> <img src="([^"]+)" '

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
           
            sThumbnail = URL_MAIN+str(aEntry[2])
            siteUrl = URL_MAIN+str(aEntry[0])
            sTitle = str(aEntry[1]).replace('en Streaming','')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
           
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
         
def __checkForNextPage(sHtmlContent):
    
    sPattern = '<a href=.([^"\']+). class="inactive">Suivant<\/a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        sUrl = URL_MAIN+aResult[1][0]     
        return sUrl 
 
    return False
 
def showHosters():
   
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail  = oInputParameterHandler.getValue('sThumbnail')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     
    url = ''
   
    oParser = cParser()
    sPattern = '{file:"([^"]+mp4)"}'
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        url = aResult[1][0]
    
    #dialogue final
    if (url):
 
        sHosterUrl = str(url)
        oHoster = cHosterGui().checkHoster(sHosterUrl)
       
        if (oHoster != False):
            sHosterUrl = sHosterUrl + '|Referer='+ sUrl.replace(URL_MAIN,'http://www.hd-stream.in/')
            # oGuiElement = cGuiElement()
            # oGuiElement.setSiteName(SITE_IDENTIFIER)
            # oGuiElement.setTitle(sMovieTitle)
            # oGuiElement.setMediaUrl(sHosterUrl)
            # oGuiElement.setThumbnail(sThumbnail)

            # oPlayer = cPlayer()
            # oPlayer.clearPlayList()
            # oPlayer.addItemToPlaylist(oGuiElement)
            # oPlayer.startPlayer()
            
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
            
             
        oGui.setEndOfDirectory()
