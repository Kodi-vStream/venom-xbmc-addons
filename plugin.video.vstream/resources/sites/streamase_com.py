#-*- coding: utf-8 -*-

from resources.lib.config import cConfig
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.rechercheHandler import cRechercheHandler
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.favourite import cFav
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

import urllib,re,urllib2
import xbmcgui
import xbmc
import xbmcaddon,os

PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile"))

SITE_IDENTIFIER = 'streamase_com' 
SITE_NAME = '[COLOR violet]Streamase.com[/COLOR]' 
SITE_DESC = 'Fichier en Streaming et en DDL, HD' 

URL_MAIN = 'http://streamase.com/'
URL_FAV = URL_MAIN + 'favorites/'


URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'lastnews/' , 'showMovies') # derniers films ajoutes
MOVIE_GENRES = (True, 'showGenreMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMembres', 'Espace Membres', 'none.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)  
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    #oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Series', 'series.png', oOutputParameterHandler)       
   
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    #oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Mangas', 'animes.png', oOutputParameterHandler)    
    
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
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Derniers Films ajoutes', 'news.png', oOutputParameterHandler)    
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films par Genre', 'genres.png', oOutputParameterHandler)

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
    showGenre("")

def showGenre(basePath): 
    oGui = cGui()
    
    liste = []
    liste.append( ['Action',URL_MAIN + 'action/' + basePath] )
    liste.append( ['Animation',URL_MAIN + 'animation/' + basePath] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'arts-martiaux/' + basePath] )
    liste.append( ['Aventure',URL_MAIN + 'aventure/' + basePath] )
    liste.append( ['Biographies',URL_MAIN + 'biopic/' + basePath] )
    liste.append( ['Comédie',URL_MAIN + 'comedie/' + basePath] )
    liste.append( ['Comédie dramatique',URL_MAIN + 'comedie-dramatique/' + basePath] )
    liste.append( ['Comédie musicale',URL_MAIN + 'comedie-musicale/' + basePath] )
    liste.append( ['Crime',URL_MAIN + 'crime/' + basePath] )
    liste.append( ['Documentaire',URL_MAIN + 'documentaire/' + basePath] )
    liste.append( ['Drame',URL_MAIN + 'drame/' + basePath] )
    liste.append( ['Espionnage',URL_MAIN + 'espionage/' + basePath] ) 
    liste.append( ['Famille',URL_MAIN + 'famille/' + basePath] ) 
    liste.append( ['Fantastique',URL_MAIN + 'fantastique/' + basePath] ) 
    liste.append( ['Guerre',URL_MAIN + 'guerre/' + basePath] ) 
    liste.append( ['Historique',URL_MAIN + 'historique/' + basePath] ) 
    liste.append( ['Horreur',URL_MAIN + 'horror/' + basePath] ) 
    liste.append( ['Péplum',URL_MAIN + 'peplum/' + basePath] ) 
    liste.append( ['Policier',URL_MAIN + 'policier/' + basePath] ) 
    liste.append( ['Romance',URL_MAIN + 'romance/' + basePath] ) 
    liste.append( ['Science fiction',URL_MAIN + 'sci-fi/' + basePath] ) 
    liste.append( ['Spectacle',URL_MAIN + 'spectacle/' + basePath] ) 
    liste.append( ['Sport',URL_MAIN + 'sport/' + basePath] ) 
    liste.append( ['Thriller',URL_MAIN + 'thriller/' + basePath] ) 
    liste.append( ['Western',URL_MAIN + 'western/' + basePath] ) 
                
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
        SaveCookie('streamase.com',cookies)
    
    
    oGui.setEndOfDirectory()
    return     

    
def showMovies(sSearch = ''):
    #xbmc.log('showMovies')
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    if sSearch:
        if sSearch == URL_FAV:
            sUrl = URL_FAV
            cookies = ''
            #try to get previous cookie
            cookies = Readcookie('streamase.com')
            oRequestHandler = cRequestHandler(sUrl)
            if cookies:
                oRequestHandler.addHeaderEntry('Cookie',cookies)
             
            sHtmlContent = oRequestHandler.request()
            #xbmc.log(sHtmlContent)
        else:
            sUrl = URL_SEARCH[0]  
            oRequestHandler = cRequestHandler(URL_SEARCH[0])
            oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
            #oRequestHandler.addHeaderEntry('Origin','http://streamase.com/')
            oRequestHandler.addHeaderEntry('Referer','http://streamase.com/')
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
            cookies = Readcookie('streamase.com')
            oRequestHandler.addHeaderEntry('Cookie',cookies)
 
        sHtmlContent = oRequestHandler.request()
        #xbmc.log(sHtmlContent)
      
    
    sCom = ''
    sQual = ''
    sYear = ''

    sPattern = '<h3 class="btl"><a href="([^"]+)">([^<]+?)</a></h3>.+?<div class="maincont">.+?src="([^"]+)".+?<br */>([^<]+?)<br */><br */>(.+?)<div class="clr"><\/div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #xbmc.log(str(aResult))
    
    if (aResult[0] == True):
        total = len(aResult[1])        
        for aEntry in aResult[1]:
            sQual = str(aEntry[3])
            sTitle = str(aEntry[1])
            sUrl2 = aEntry[0]
            sCom = aEntry[4]
            sCom = sCom.decode("unicode_escape").encode("latin-1")
            if 'http://' in aEntry[2]:
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
    
    #xbmc.log(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #xbmc.log(sHtmlContent)
    oParser = cParser()
    
    sPattern = '<!--/colorstart-->([^<]+)<!--colorend-->|<a href="([^"]+)" target="_blank">([^<]+?)</a>'
   
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
  

def DeleteCookie(Domain):
    file = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')
    os.remove(os.path.join(PathCache,file))
    
def SaveCookie(Domain,data):
    Name = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')

    #save it
    file = open(Name,'w')
    file.write(data)

    file.close()
    
def Readcookie(Domain):
    Name = os.path.join(PathCache,'Cookie_'+ str(Domain) +'.txt')
    
    try:
        file = open(Name,'r')
        data = file.read()
        file.close()
    except:
        return ''
    
    return data
