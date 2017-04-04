#-*- coding: utf-8 -*-

from resources.lib.config import cConfig
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

from resources.lib.config import GestionCookie

import re
import xbmc
import xbmcaddon,os

PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile"))

SITE_IDENTIFIER = 'streamase_com' 
SITE_NAME = 'Streamase' 
SITE_DESC = 'Fichiers en Streaming et en DDL, HD' 

#film
URL_MAIN = 'http://streamase.com/'
MOVIE_NEWS = (URL_MAIN + 'lastnews/' , 'showMovies')
MOVIE_GENRES = (True, 'showGenreMovies')

#animes
URL_MAIN_MANGA = 'http://manga.streamase.com/'
MANGA_NEWS = (URL_MAIN_MANGA + 'index.php?do=lastnews/' , 'showMovies')
MANGA_GENRES = (True, 'showGenreMangas')

#serie
URL_MAIN_SERIE = 'http://serie.streamase.com/'
SERIE_NEWS = (URL_MAIN_SERIE + 'index.php?do=lastnews/' , 'showMovies')
SERIE_GENRES = (True, 'showGenreSeries')

URL_FAV = URL_MAIN + 'favorites/'

#recherche
URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMembres', 'Espace Membres', 'none.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries', 'series.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Mangas', 'animes.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory() 

def showMenuMembres():
    oGui = cGui()
       
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'login', 'Login', 'none.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showFavorites', 'Mes Favoris', 'none.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()     

def showMenuFilms():
    oGui = cGui()
       
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oOutputParameterHandler.addParameter('type', 'film')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche de films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def showMenuSeries():
    oGui = cGui()
       
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oOutputParameterHandler.addParameter('type', 'serie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche de série', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def showMenuMangas():
    
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oOutputParameterHandler.addParameter('type', 'anime')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche de mangas', 'search.png', oOutputParameterHandler) 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MANGA_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MANGA_NEWS[1], 'Mangas (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MANGA_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MANGA_GENRES[1], 'Mangas (Genres)', 'animes_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return     

def showFavorites():
    oGui = cGui()
    showMovies(URL_FAV)
    oGui.setEndOfDirectory()
    return             
        
def showGenreMovies():
    showGenre(URL_MAIN)
    
def showGenreMangas():
    showGenre(URL_MAIN_MANGA)
    
def showGenreSeries():
    showGenre(URL_MAIN_SERIE)

def showGenre(basePath): 
    oGui = cGui()
    
    liste = []
    liste.append( ['Action',basePath + 'action/' ] )
    liste.append( ['Animation',basePath + 'animation/' ] )
    liste.append( ['Arts Martiaux',basePath + 'arts-martiaux/' ] )
    liste.append( ['Aventure',basePath + 'aventure/' ] )
    liste.append( ['Biographies',basePath + 'biopic/' ] )
    liste.append( ['Comédie',basePath + 'comedie/' ] )
    liste.append( ['Comédie dramatique',basePath + 'comedie-dramatique/' ] )
    liste.append( ['Comédie musicale',basePath + 'comedie-musicale/' ] )
    liste.append( ['Crime',basePath + 'crime/' ] )
    liste.append( ['Documentaire',basePath + 'documentaire/' ] )
    liste.append( ['Drame',basePath + 'drame/' ] )
    liste.append( ['Espionnage',basePath + 'espionage/' ] ) 
    liste.append( ['Famille',basePath + 'famille/' ] ) 
    liste.append( ['Fantastique',basePath + 'fantastique/' ] ) 
    liste.append( ['Guerre',basePath + 'guerre/' ] ) 
    liste.append( ['Historique',basePath + 'historique/' ] ) 
    liste.append( ['Horreur',basePath + 'horror/' ] ) 
    liste.append( ['Péplum',basePath + 'peplum/' ] ) 
    liste.append( ['Policier',basePath + 'policier/' ] ) 
    liste.append( ['Romance',basePath + 'romance/' ] ) 
    liste.append( ['Science fiction',basePath + 'sci-fi/' ] ) 
    liste.append( ['Spectacle',basePath + 'spectacle/' ] ) 
    liste.append( ['Sport',basePath + 'sport/' ] ) 
    liste.append( ['Thriller',basePath + 'thriller/' ] ) 
    liste.append( ['Western',basePath + 'western/' ] ) 
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)    
       
    oGui.setEndOfDirectory()

def login():
    oGui = cGui()
    name = oGui.showKeyBoard()
    password = oGui.showKeyBoard()
    cookies = ''
    
    oRequestHandler = cRequestHandler(URL_MAIN)
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    #oRequestHandler.addHeaderEntry('Origin','http://streamase.com/')
    oRequestHandler.addHeaderEntry('Referer','http://streamase.com/')
    oRequestHandler.addParameters('login_name', name)
    oRequestHandler.addParameters('login_password', password)
    oRequestHandler.addParameters('login', 'submit')
        
    sHtmlContent = oRequestHandler.request()
    cookies = oRequestHandler.GetCookies()
    print cookies
    if cookies:
        cConfig().showInfo('vStream', 'Login OK')
        #save cookies
        GestionCookie().SaveCookie('streamase.com',cookies)
    
    oGui.setEndOfDirectory()
    return     

def showMovies(sSearch = ''):
    #xbmc.log('showMovies')
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    if sSearch:
        
        oInputParameterHandler = cInputParameterHandler()
        sType = oInputParameterHandler.getValue('type') 
      
        Url_Search = URL_MAIN
       
        if sType:
            if sType == "serie":
                Url_Search = URL_MAIN_SERIE
            elif sType == "anime":
                Url_Search = URL_MAIN_MANGA
            else:
                Url_Search = URL_MAIN
        
        if sSearch == URL_FAV:
            sUrl = URL_FAV
            cookies = ''
            #try to get previous cookie
            cookies = GestionCookie().Readcookie('streamase.com')
            oRequestHandler = cRequestHandler(sUrl)
            if cookies:
                oRequestHandler.addHeaderEntry('Cookie',cookies)
             
            sHtmlContent = oRequestHandler.request()
            #xbmc.log(sHtmlContent)
        else:
            sUrl = Url_Search + 'index.php?do=search'
            
            if URL_SEARCH[0] in sSearch:
                sSearch=sSearch.replace(URL_SEARCH[0],'')
                
            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
            #oRequestHandler.addHeaderEntry('Origin','http://streamase.com/')
            oRequestHandler.addHeaderEntry('Referer',Url_Search)
            #oRequestHandler.addParameters('do', 'search')
            oRequestHandler.addParameters('subaction', 'search')
            oRequestHandler.addParameters('search_start', '0')
            oRequestHandler.addParameters('full_search', '0')
            oRequestHandler.addParameters('result_from', '1')
            oRequestHandler.addParameters('story', sSearch)
        
            sHtmlContent = oRequestHandler.request()
                
    else:
        
        sUrl = oInputParameterHandler.getValue('siteUrl')     
        
        #xbmc.log(sUrl)
   
        oRequestHandler = cRequestHandler(sUrl) 
        if URL_FAV in sUrl:
            cookies = GestionCookie().Readcookie('streamase.com')
            oRequestHandler.addHeaderEntry('Cookie',cookies)
 
        sHtmlContent = oRequestHandler.request()
        #xbmc.log(sHtmlContent)
      
    sCom = ''
    sQual = ''
    sYear = ''

    sPattern = '<h3 class="btl"><a href="([^"]+)">([^<]+?)</a></h3>.+?<div class="maincont">.+?src="([^"]+)".+?<br */>([^<]+?)<br */><br */>(.+?)<div class="clr"><\/div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #cConfig().log(str(aResult))
    
    if (aResult[0] == True):
        total = len(aResult[1])        
        for aEntry in aResult[1]:
            sQual = str(aEntry[3])
            sTitle = str(aEntry[1])
            sUrl2 = aEntry[0]
            sCom = aEntry[4]
            sCom = sCom.decode("unicode_escape").encode("latin-1")
            if aEntry[2].startswith('http'):
                sThumbnail=aEntry[2]
            else:
                sThumbnail=URL_MAIN+aEntry[2]
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl2)) 
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle)) 
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sCom', sCom)
            sDisplayTitle = cUtil().DecoTitle(sTitle + ' ('+sQual+')')
            
            if 'series-' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumbnail, sCom, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, sCom, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)#cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    #Passage en mode vignette sauf en cas de recherche globale
    #if not bGlobal_Search:
        #xbmc.executebuiltin('Container.SetViewMode(500)')
     
    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a href="([^"]+)"><span class="thide pnext">Next</span></a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #xbmc.log(str(aResult))
    if (aResult[0] == True):
        return aResult[1][0]
        
    return False

def showHosters():# recherche et affiche les hotes
    #xbmc.log("showHosters")
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler() 
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')
    
    #cConfig().log(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    
    sPattern = '<!--/colorstart-->([^<]+)<!--colorend-->|<a href="([^"]+)" *target="_blank">([^<]+?)</a>'
   
    aResult = oParser.parse(sHtmlContent, sPattern)
    #xbmc.log(str(aResult))
       
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR] ')
            else:
                sHosterUrl=aEntry[1]
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                sTitle = aEntry[2]
                if (oHoster != False):
                    sDisplayTitle = cUtil().DecoTitle(sTitle)
                    sDisplayTitle = sDisplayTitle.replace('-EXTREME','')
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
   
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
