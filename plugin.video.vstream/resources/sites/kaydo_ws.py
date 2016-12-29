#-*- coding: utf-8 -*-
#Venom & johngf.
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
import re,urllib2,urllib,xbmc

#copie du site http://www.film-streaming.co/
#copie du site http://www.streaming-club.com/
#copie du site http://www.hd-stream.in/
#copie du site http://www.kaydo.ws/


SITE_IDENTIFIER = 'kaydo_ws'
SITE_NAME = 'Kaydo.ws'
SITE_DESC = 'Le seul site de streaming en HD 720p 100% Gratuit'

URL_MAIN = 'http://www.kaydo.ws/'
 
MOVIE_NEWS = (URL_MAIN + 'films.php', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films.php', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'populaires.php', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'best-rating.php', 'showMovies')
MOVIE_HD = (URL_MAIN + 'films.php', 'showMovies')
 
MOVIE_GENRES = (True, 'showGenre')
 
URL_SEARCH = (URL_MAIN + 'search.php?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
   
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Nouveautes', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films les plus vues', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'top-films.php')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Top Films', 'films.png', oOutputParameterHandler)
    
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
    
    # fh = open('I:\\test.txt', "w")
    # fh.write(sHtmlContent)
    # fh.close()

    sPattern = '<div class="box"> *<img src="([^"]+)" width=".+?" height=".+?">.+?<h2>([^<]+)</h2>.+?<p.*?>([^<]+)</p>.+?ref="([^"]+)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sThumbnail = URL_MAIN+str(aEntry[0])
            siteUrl = URL_MAIN+str(aEntry[3])
            sCom = str(aEntry[2])
            sTitle = str(aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumbnail, sCom, oOutputParameterHandler)
           
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
         
def __checkForNextPage(sHtmlContent):
    sPattern = 'class="pagination">.*?<li class="active">.+?<li><a href="(.+?)"'
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
     
    oParser = cParser()
    sPattern = '<video><source type="video/mp4" src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        BA = aResult[1][0]
    else:
        BA = False

    sPattern = '{file:"([^\"]+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):   
        sHosterUrl = str(aResult[1][0])
        oHoster = cHosterGui().checkHoster(sHosterUrl)       
        if (oHoster != False):            
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
            
        if (BA != False):
            sHosterUrl2 = str(BA)
            oHoster2 = cHosterGui().checkHoster(sHosterUrl2)
            if (oHoster2 != False):            
                oHoster2.setDisplayName(sMovieTitle + '[COLOR coral]' + (' [Bande Annonce] ') + '[/COLOR]')
                oHoster2.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster2, sHosterUrl2, '') 
                  
        oGui.setEndOfDirectory()
