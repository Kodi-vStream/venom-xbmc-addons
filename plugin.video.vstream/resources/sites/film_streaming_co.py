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
 
SITE_IDENTIFIER = 'film_streaming_co'
SITE_NAME = 'Film-streaming.co'
SITE_DESC = 'Le seul site de streaming en HD 720p 100% Gratuit'

URL_MAIN = 'http://www.film-streaming.co/'
 
MOVIE_NEWS = ('http://www.film-streaming.co/index.php', 'showMovies')
MOVIE_FILMS = ('http://www.film-streaming.co/films.php', 'showMovies')
MOVIE_TOP = ('http://www.film-streaming.co/top.php', 'showMovies')
 
 
MOVIE_GENRES = (True, 'showGenre')
 
 
URL_SEARCH = ('http://www.film-streaming.co/search.php?movie=', 'resultSearch')
FUNCTION_SEARCH = 'resultSearch'
   
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Nouveautés', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Top Films', 'top.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FILMS[0])
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
        sUrl = 'http://www.film-streaming.co/search.php?movie='+sSearchText 
        resultSearch(sUrl)
        oGui.setEndOfDirectory()
        return 

def showPage():
    oGui = cGui()
 
    sSearchNum = oGui.showNumBoard()
    
    if (sSearchNum):

        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrlbase')
        sMaxPage = oInputParameterHandler.getValue('MaxPage')
        
        sSearchNum = str(sSearchNum)
        
        if int(sSearchNum) > int (sMaxPage):
            sSearchNum = sMaxPage
            
        sUrl = sUrl + str(sSearchNum)
        
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

    
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Animation','http://www.film-streaming.co/genre.php?g=Animation'] )    
    liste.append( ['Action','http://www.film-streaming.co/genre.php?g=Action'] )
    liste.append( ['Arts Martiaux','http://www.film-streaming.co/genre.php?g=Arts%20Martiaux'] )
    liste.append( ['Aventure','http://www.film-streaming.co/genre.php?g=Aventure'] )
    liste.append( ['Biopic','http://www.film-streaming.co/genre.php?g=Biopic'] )
    liste.append( ['Comedie','http://www.film-streaming.co/genre.php?g=Com%C3%A9die'] )
    liste.append( ['Comedie Dramatique','http://www.film-streaming.co/genre.php?g=Com%C3%A9die%20dramatique'] )
    liste.append( ['Documentaire','http://www.film-streaming.co/genre.php?g=Documentaire'] )
    liste.append( ['Drame','http://www.film-streaming.co/genre.php?g=Drame'] )
    liste.append( ['Epouvante Horreur','http://www.film-streaming.co/genre.php?g=Epouvante-horreur'] )
    liste.append( ['Espionage','http://www.film-streaming.co/genre.php?g=Espionnage'] )  
    liste.append( ['Fantastique','http://www.film-streaming.co/genre.php?g=Fantastique'] )
    liste.append( ['Famille','http://www.film-streaming.co/genre.php?g=Famille'] )
    liste.append( ['Guerre','http://www.film-streaming.co/genre.php?g=Guerre'] )
    liste.append( ['Historique','http://www.film-streaming.co/genre.php?g=Historique'] )
    liste.append( ['Musical','http://www.film-streaming.co/genre.php?g=Musical'] )
    liste.append( ['Policier','http://www.film-streaming.co/genre.php?g=Policier'] )
    liste.append( ['Romance','http://www.film-streaming.co/genre.php?g=Romance'] )
    liste.append( ['Sciense Fiction','http://www.film-streaming.co/genre.php?g=Science%20fiction'] )
    liste.append( ['Thriller','http://www.film-streaming.co/genre.php?g=Thriller'] )
    liste.append( ['Western','http://www.film-streaming.co/genre.php?g=Western'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def resultSearch(sSearch = ''):
    oGui = cGui()  
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sPattern = '<td class="wrapper_pic_td"><img src="(.+?)" border="0" alt="(.+?)\sStreaming".+?></td>.+?<span class="std">(.+?)</span>'
    
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
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', aEntry[1], 'films.png', sThumbnail, aEntry[2], oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
        
    if not sSearch:       
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
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')

    sPattern = '<td.+?class="over_modul">.+?<a href="(.+?)"><img src="(.+?)" border="0" alt="(.+?)\sstreaming".+?</a>'     

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
           
            sThumbnail = URL_MAIN+str(aEntry[1])
            siteUrl = URL_MAIN+str(aEntry[0])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', aEntry[2], 'films.png', sThumbnail, '', oOutputParameterHandler)
           
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage[1] + str(int(sNextPage[0]) + 1))
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next ' + sNextPage[0] + '/' + sNextPage[2] + '>>> [/COLOR]', 'next.png', oOutputParameterHandler)
        
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrlbase', sNextPage[1])
            oOutputParameterHandler.addParameter('MaxPage', sNextPage[2])
            oGui.addDir(SITE_IDENTIFIER, 'showPage', '[COLOR teal]Choisir Page >>> [/COLOR]', 'next.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
         
def __checkForNextPage(sHtmlContent):
    #sPattern = '<(?:strong class="current"|span class="btn btn-default active")>([0-9]+) *<.+?<span class="btn btn-default">\.\.\. *<a class="btn btn-default" href="([^<>"]+?=)[0-9]+">([0-9]+)<\/a>'
    sPattern = '<(?:strong class="current"|span class="btn btn-default active")>([0-9]+) *<.+?class="btn btn-default" href="([^<>"]+?=)[0-9]+".*?>([0-9]+)<(?!.+?>[0-9]+<.+?)(.+?)<\/td>'
    
    #fh = open('c://test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
 
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        #aResult[1][0][0] num current page
        #aResult[1][0][1] url vierge url.php?page=
        #aResult[1][0][2] num derniere page
        
        return aResult[1][0][0], URL_MAIN + aResult[1][0][1], aResult[1][0][2] 
 
    return False
 
def showHosters():
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail  = oInputParameterHandler.getValue('sThumbnail')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
     
    url = ''
   
    oParser = cParser()
    sPattern = 'document.write\(unescape\("(.+?)"\)\);'
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        chainedecrypte = urllib.unquote(aResult[1][0])
        sPattern = 'file: "(http.+?mp4)"'
        aResult = re.findall(sPattern,chainedecrypte)
        if (aResult):
            url = aResult[0]
   
    #dialogue final
    if (url):
 
        sHosterUrl = str(url)
        oHoster = cHosterGui().checkHoster(sHosterUrl)
       
        if (oHoster != False):
            sHosterUrl = sHosterUrl + '|Referer='+ sUrl
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setTitle(sMovieTitle)
            oGuiElement.setMediaUrl(sHosterUrl)
            oGuiElement.setThumbnail(sThumbnail)

            oPlayer = cPlayer()
            oPlayer.clearPlayList()
            oPlayer.addItemToPlaylist(oGuiElement)
            oPlayer.startPlayer()
            
            #oHoster.setDisplayName(sMovieTitle)
            #oHoster.setFileName(sMovieTitle)
            #cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
             
        #cConfig().finishDialog(dialog)
