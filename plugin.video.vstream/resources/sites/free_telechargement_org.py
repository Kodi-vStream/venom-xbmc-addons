#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.config import cConfig
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.cloudflare import CloudflareBypass
from resources.lib.cloudflare import NoRedirection
from resources.lib.config import GestionCookie

import re,xbmc,xbmcgui,xbmcaddon,os

PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile"))
UA = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

SITE_IDENTIFIER = 'free_telechargement_org'
SITE_NAME = '[COLOR violet]Free-Téléchargement[/COLOR]'
SITE_DESC = 'Fichiers en DDL, HD, Films, Séries, Mangas Etc...'

URL_MAIN = 'http://www.free-telechargement.com/'
URL_PROTECT = 'http://liens.free-telechargement.com/'
URL_PROTECTBIS = 'http://liens.free-telechargement.org/'
#URL_SEARCH_MOVIES_SD = (URL_MAIN + '1/recherche/1.html?rech_cat=video&rech_fiche=', 'showMovies')
#URL_SEARCH_MOVIES_HD = (URL_MAIN + '1/recherche/1.html?rech_cat=Films+HD&rech_fiche=', 'showMovies')

#URL_SEARCH_SERIE_SD = (URL_MAIN + '1/recherche1/1.html?rech_cat=serie&rech_fiche=', 'showMovies')
#URL_SEARCH_SERIE_HD = (URL_MAIN + '1/recherche1/1.html?rech_cat=seriehd&rech_fiche=', 'showMovies')
URL_SEARCH_EMISSIONS_TV = (URL_MAIN, 'showMovies')
URL_SEARCH_SPECTACLES = (URL_MAIN, 'showMovies')

URL_SEARCH = (URL_MAIN + '1/recherche/1.html?rech_fiche=', 'showSearchResult')
FUNCTION_SEARCH = 'showSearchResult'

MOVIE_SD_DVDRIP = (URL_MAIN + '1/categorie-Films+DVDRiP+et+BDRiP/1.html', 'showMovies') # derniers films en SD
MOVIE_SD_CAM = (URL_MAIN + '1/categorie-Films+CAM+TS+R5+et+DVDSCR/1.html', 'showMovies') # derniers films en SD
MOVIE_SD_VOSTFR = (URL_MAIN + '1/categorie-Films+VOSTFR+et+VO/1.html', 'showMovies') # derniers films en SD
MOVIE_SD_CLASSIQUE = (URL_MAIN + '1/categorie-Films+Classiques/1.html', 'showMovies') # derniers films en SD
MOVIE_SD_VIEWS = (URL_MAIN + '1/films/affichage', 'showMovies') # derniers films en SD
MOVIE_GENRES_SD = (True, 'showGenreMoviesSD')

MOVIE_HD = (URL_MAIN + '1/categorie-Films+BluRay+720p+et+1080p/1.html', 'showMovies') # derniers films en HD
MOVIE_3D = (URL_MAIN + '1/categorie-Films+BluRay+3D/1.html', 'showMovies') # derniers films en 3D
MOVIE_HD_VIEWS = (URL_MAIN + '1/films-bluray/affichage', 'showMovies') # derniers films en HD
MOVIE_GENRES_HD = (True, 'showGenreMoviesHD')

ANIM_ANIMS = (URL_MAIN + '1/animations/1', 'showMovies') # derniers dessins animés
ANIM_VFS = (URL_MAIN + '1/categorie-Mangas+VF/1.html', 'showMovies') # derniers dessins animés
ANIM_VOSTFRS = (URL_MAIN + '1/categorie-Mangas+VOST/1.html', 'showMovies') # derniers dessins animés

EMISSIONS_TV = (URL_MAIN + '1/categorie-Emissions/1.html', 'showMovies') # dernieres émissions TV

SPECTACLES = (URL_MAIN + '1/categorie-Spectacles/1.html', 'showMovies') # dernieres émissions TV

SERIE_SD_EN_COURS_VF = (URL_MAIN + '1/categorie-Saisons+en+cours+VF+/', 'showMovies') # derniers films en SD
SERIE_SD_EN_COURS_VOSTFR = (URL_MAIN + '1/categorie-Saisons+en+cours+VOST/', 'showMovies') # derniers films en SD
SERIE_SD_TERMINE_VF = (URL_MAIN + '1/categorie-Saison+Terminée+VF/', 'showMovies') # derniers films en SD
SERIE_SD_TERMINE_VOSTFR = (URL_MAIN + '1/categorie-Saison+Terminée+VOST/', 'showMovies') # derniers films en SD
SERIE_HD_EN_COURS_VF = (URL_MAIN + '1/categorie-Saisons+en+cours+VF+HD/', 'showMovies') # derniers films en SD
SERIE_HD_EN_COURS_VOSTFR = (URL_MAIN + '1/categorie-Saisons+en+cours+VOST+HD/', 'showMovies') # derniers films en SD
SERIE_HD_TERMINE_VF = (URL_MAIN + '1/categorie-Saison+Terminée+VF+HD/', 'showMovies') # derniers films en SD
SERIE_HD_TERMINE_VOSTFR = (URL_MAIN + '1/categorie-Saison+Terminée+VOST+HD/', 'showMovies') # derniers films en SD

def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries', 'series.png', oOutputParameterHandler)       
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Mangas', 'animes.png', oOutputParameterHandler)    
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSpectacles', 'Spectacles', 'films.png', oOutputParameterHandler)    
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuEmissionsTV', 'Emissions TV', 'tv.png', oOutputParameterHandler)    
    
    oGui.setEndOfDirectory() 

def showMenuFilms():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oOutputParameterHandler.addParameter('type', 'film')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche de films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_VIEWS[1], 'Films SD (Les plus vus)', 'films_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_DVDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_DVDRIP[1], 'Films SD DVDRIP & BDRIP (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_CAM[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_CAM[1], 'Films SD CAM & DVDScr (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_VOSTFR[1], 'Films SD VOSTFR (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD_CLASSIQUE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD_CLASSIQUE[1], 'Films SD Classiques (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films HD 720p & 1080p (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Films 3D (Derniers ajouts)', 'films_news.png', oOutputParameterHandler) 
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD_VIEWS[1], 'Films HD (Les plus vus)', 'films_views.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES_SD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES_SD[1], 'Films SD (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES_HD[1], 'Films HD (Genres)', 'films_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()     

def showMenuSeries():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oOutputParameterHandler.addParameter('type', 'serie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche de séries', 'search.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SD_EN_COURS_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SD_EN_COURS_VF[1], 'Séries SD VF en cours', 'series_news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SD_EN_COURS_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SD_EN_COURS_VOSTFR[1], 'Séries SD VOSTFR en cours', 'series_news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SD_TERMINE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SD_TERMINE_VF[1], 'Séries SD VF terminées', 'series_news.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SD_TERMINE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SD_TERMINE_VOSTFR[1], 'Séries SD VOSTFR terminées', 'series_vostfr.png', oOutputParameterHandler)  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD_EN_COURS_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD_EN_COURS_VF[1], 'Séries HD VF en cours', 'series_vf.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD_EN_COURS_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD_EN_COURS_VOSTFR[1], 'Séries HD VOSTFR en cours', 'series_vostfr.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD_TERMINE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD_TERMINE_VF[1], 'Séries HD VF terminées', 'series_vf.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD_TERMINE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD_TERMINE_VOSTFR[1], 'Séries HD VOSTFR terminées', 'series_vostfr.png', oOutputParameterHandler)  

    oGui.setEndOfDirectory()     
    
def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oOutputParameterHandler.addParameter('type', 'anime')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMangas', 'Recherche d\'animés', 'search.png', oOutputParameterHandler) 
  
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Dessins Animés (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Mangas VF (Derniers ajouts)', 'animes_vf.png', oOutputParameterHandler)  

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Mangas VOSTFR (Derniers ajouts)', 'animes_vostfr.png', oOutputParameterHandler) 

    oGui.setEndOfDirectory()     

def showMenuSpectacles():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSpectacles', 'Recherche de Spectacles', 'search.png', oOutputParameterHandler) 
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPECTACLES[0])
    oGui.addDir(SITE_IDENTIFIER, SPECTACLES[1], 'Spectacles (Derniers ajouts)', 'news.png', oOutputParameterHandler)  
    
    oGui.setEndOfDirectory()         
    
def showMenuEmissionsTV():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearchEmissionsTV', 'Recherche émissions TV', 'search.png', oOutputParameterHandler) 
  
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', EMISSIONS_TV[0])
    oGui.addDir(SITE_IDENTIFIER, EMISSIONS_TV[1], 'Dernières émissions TV', 'tv.png', oOutputParameterHandler)  
    
    oGui.setEndOfDirectory()     
  
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showSearchResult(sUrl)
        oGui.setEndOfDirectory()
        return     

def showSearchSpectacles(): 
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH_SPECTACLES[0] + sSearchText
        showSearchResult(sUrl) 
        oGui.setEndOfDirectory()
        return    
               
def showSearchEmissionsTV(): 
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH_EMISSIONS_TV[0] + sSearchText
        showSearchResult(sUrl) 
        oGui.setEndOfDirectory()
        return    
      
def showGenreMoviesSD(): 
    showGenre("films+dvdrip+et+bdrip/")
 
def showGenreMoviesHD(): 
    showGenre("Films+BluRay+720p+et+1080p/")

def showGenre(basePath): 
    oGui = cGui()
    
    liste = []
    liste.append( ['Action',URL_MAIN + '1/genre-Action/' + basePath] )
    liste.append( ['Animation',URL_MAIN + '1/genre-Animation/' + basePath] )
    liste.append( ['Arts Martiaux',URL_MAIN + '1/genre-Arts%20Martiaux/' + basePath] )
    liste.append( ['Aventure',URL_MAIN + '1/genre-Aventure/' + basePath] )
    liste.append( ['Biographies',URL_MAIN + '1/genre-Biographies/' + basePath] )
    liste.append( ['Comédie',URL_MAIN + '1/genre-Comedie/' + basePath] )
    liste.append( ['Comédie dramatique',URL_MAIN + '1/genre-Comedie+Dramatique/' + basePath] )
    liste.append( ['Comédie musicale',URL_MAIN + '1/genre-Comedie+Musicale/' + basePath] )
    liste.append( ['Divers',URL_MAIN + '1/genre-Divers/' + basePath] )
    liste.append( ['Drame',URL_MAIN + '1/genre-Drame/' + basePath] )
    liste.append( ['Espionnage',URL_MAIN + '1/genre-Espionnage/' + basePath] ) 
    liste.append( ['Famille',URL_MAIN + '1/genre-Famille/' + basePath] ) 
    liste.append( ['Fantastique',URL_MAIN + '1/genre-Fantastique/' + basePath] ) 
    liste.append( ['Guerre',URL_MAIN + '1/genre-Guerre/' + basePath] ) 
    liste.append( ['Historique',URL_MAIN + '1/Historique/' + basePath] ) 
    liste.append( ['Horreur',URL_MAIN + '1/genre-Horreur-Epouvante/' + basePath] ) 
    liste.append( ['Péplum',URL_MAIN + '1/genre-Peplum/' + basePath] ) 
    liste.append( ['Policier',URL_MAIN + '1/genre-Policiers/' + basePath] ) 
    liste.append( ['Romance',URL_MAIN + '1/genre-Romance/' + basePath] ) 
    liste.append( ['Science fiction',URL_MAIN + '1/genre-Science-Fiction/' + basePath] ) 
    liste.append( ['Thriller',URL_MAIN + '1/genre-Thriller/' + basePath] ) 
    liste.append( ['Western',URL_MAIN + '1/genre-Westerns/' + basePath] ) 
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)    
       
    oGui.setEndOfDirectory()

def showSearchResult(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    sUrl = sSearch
    
    HD = 0
    SD = 0
    
    #uniquement si c'est la premiere page
    if sSearch:
        sType = oInputParameterHandler.getValue('type')
        
        loop = 1
      
        if sType:
            if sType == "film":
                sUrl = sUrl + '&rech_cat=video'
                loop = 2
            if sType == "serie":
                sUrl = sUrl + '&rech_cat=serie'
                loop = 2
            if sType == "anime":
                sUrl = sUrl + '&rech_cat=Animations'
         
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')  
        loop = 1
        SD = HD = -1
         
    oParser = cParser()
    aResult = []
    NextPage = []

    while (loop):
        oRequestHandler = cRequestHandler(sUrl) 
        sHtmlContent = oRequestHandler.request()
        sHtmlContent = sHtmlContent.replace('<span style="background-color: yellow;"><font color="red">','')
        sPattern = '<b><p style="font-size: 18px;"><A href="([^"]+)">(.+?)<\/A.+?<td align="center">\s*<img src="([^"]+)".+?<b>Description : <\/b><\/br><\/br>(.+?)<'
        aResult1 = oParser.parse(sHtmlContent, sPattern)
        if aResult1[0]:
            aResult = aResult + aResult1[1]

            sNextPage = __checkForNextPage(sHtmlContent)
            
            if (sNextPage != False):
                n = '[COLOR teal]Next >>>[/COLOR]'
                if sSearch:
                    n = '[COLOR teal]Next SD >>>[/COLOR]'
                if loop == 2:
                    n ='[COLOR teal]Next HD >>>[/COLOR]'
                NextPage.append((n,sNextPage))
                
        loop = loop - 1
        if (loop == 1):
            HD = len(aResult)
            if sUrl.endswith('video'):
                sUrl = sUrl.replace('=video','=Films+HD')
            if sUrl.endswith('serie'):
                sUrl = sUrl.replace('=serie','=seriehd')
        
    if (aResult):
        total = len(aResult)
        i = 0
        for aEntry in aResult:
            
            #titre ?
            if i == SD:
                oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Qualitee SD[/COLOR]')
            if i == HD:
                oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Qualitee HD[/COLOR]')
            i = i + 1
            
            sQual = 'SD'
            if '-hd/' in aEntry[0] or 'bluray' in aEntry[0]:
                sQual = 'HD'
            if '-3d/' in aEntry[0]:
                sQual = '3D'
            
            sTitle = str(aEntry[1])
            sTitle = cUtil().removeHtmlTags(sTitle)
            sUrl2 = aEntry[0]

            sCom = aEntry[3]
            sCom = sCom.decode("unicode_escape").encode("latin-1")
            sThumbnail=aEntry[2]
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(sUrl2)) 
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle)) 
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sCom', sCom)
            sDisplayTitle = cUtil().DecoTitle('('+sQual+') '+sTitle)
            
            if 'series-' in sUrl or '-Saison' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, sCom, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, sCom, oOutputParameterHandler)
        
        for n,u in NextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', u)
            oGui.addDir(SITE_IDENTIFIER, 'showSearchResult', n, 'next.png', oOutputParameterHandler)
    if not sSearch:
        oGui.setEndOfDirectory()        
        
def showMovies():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')     
 
    oRequestHandler = cRequestHandler(sUrl) 
    sHtmlContent = oRequestHandler.request()
    
    sCom = ''
    sQual = ''

    sPattern = '<table style="float:left;padding-left:8px"> *<td> *<div align="left"> *<a href="([^"]+)" onmouseover="Tip\(\'<b>([^"]+?)<\/b>.+?Description :</b> <i>([^<]+?)<.+?<img src="([^"]+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])        
        for aEntry in aResult[1]:
            sQual = 'SD'
            if '-hd/' in aEntry[0] or 'bluray' in aEntry[0]:
                sQual = 'HD'
            if '-3d/' in aEntry[0]:
                sQual = '3D'
            
            sTitle = str(aEntry[1])
            sUrl2 = aEntry[0]

            sCom = aEntry[2]
            sCom = sCom.decode("unicode_escape").encode("latin-1")
            sThumbnail=aEntry[3]
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(sUrl2)) 
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle)) 
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sCom', sCom)
            sDisplayTitle = cUtil().DecoTitle('('+sQual+') '+sTitle)
            
            if 'series-' in sUrl or '-Saison' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, sCom, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, sCom, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)#cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    #Merci de ne pas faire ça
    #xbmc.executebuiltin('Container.SetViewMode(500)')

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="courante">[^<]+</span> <a href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        return URL_MAIN+aResult[1][0]
        
    return False

def showHosters():# recherche et affiche les hotes
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler() 
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    
    #recuperation nom de la release
    if 'elease :' in sHtmlContent:
        sPattern = 'elease :([^<]+)<'
    else:
        sPattern = '<br /> *([^<]+)</p></center>'
    
    aResult1 = oParser.parse(sHtmlContent, sPattern)
    if (aResult1[0] == True):
        if 'Forced' in aResult1[1][0]:
            aResult1[1][0]=''
    
    #cut de la zone des liens
    if 'Lien Premium' in sHtmlContent:
        sPattern = 'Lien Premium(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if not aResult[0]:
            return
        sHtmlContent = aResult[1][0]

        if 'Interchangeables' in sHtmlContent:
            #cut de restes de liens non premiums
            sPattern = '--(.+?)Interchangeables'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if not aResult[0]:
                return
            sHtmlContent = aResult[1][0]
            
    else:
        sPattern = '<div id="link">(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if not aResult[0]:
            return
        sHtmlContent = aResult[1][0]
        sHtmlContent = sHtmlContent.replace('&nbsp;','')
        
    if '-multi' in sHtmlContent:
        sPattern = '<a href="link.php\?lien\=([^"]+)"'
    else:
        sPattern = '<b>(.+?)<\/b>.+?<a href="link.php\?lien\=([^"]+)" target="_blank" *><b>Cliquer ici pour Télécharger'
   
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        oGui.addText(SITE_IDENTIFIER, aResult1[1][0])
        for aEntry in aResult[1]:
            
            sHostName = aEntry[0]
            sHostName = cUtil().removeHtmlTags(sHostName)
            
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            oOutputParameterHandler = cOutputParameterHandler()
            if total == 1:
                sTitle = '[COLOR skyblue]' + 'Liens Premium' + '[/COLOR] '
                oOutputParameterHandler.addParameter('siteUrl', aEntry)
            else:
                sTitle = '[COLOR skyblue]' + sHostName+ '[/COLOR] '
                oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
            
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumbnail, '', oOutputParameterHandler)
   
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
  
def showSeriesHosters():# recherche et affiche les hotes
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler() 
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    
    #recuperation nom de la release
    sPattern = '</span> ([^<]+)</strong> :.'
    aResult1 = oParser.parse(sHtmlContent, sPattern)
    
    #cut de la zone des liens
    if 'Lien Premium' in sHtmlContent:
        sPattern = 'Lien Premium *--(.+?)</div>'
    else:
        sPattern = '<div id="link">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sHtmlContent = aResult[1][0]
    sHtmlContent = re.sub('<font color="[^"]+">','',sHtmlContent)
    sHtmlContent = re.sub('</font>','',sHtmlContent)
    #sHtmlContent = re.sub('link.php\?lien\=','',sHtmlContent)
    
    if '-multi' in sHtmlContent:
        sPattern = '<a href="link.php\?lien\=([^"]+)"'
    else:
        sPattern = '<b>(.+?)</b> </br> <a href="link.php\?lien\=([^"]+)" target="_blank" ><b>Cliquer ici pour Télécharger</b></a><br /><br />'
   
    aResult = oParser.parse(sHtmlContent, sPattern) 
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        oGui.addText(SITE_IDENTIFIER, sMovieTitle + aResult1[1][0])
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            oOutputParameterHandler = cOutputParameterHandler()
            if total == 1:
                sTitle = '[COLOR skyblue]' + 'Liens Premium' + '[/COLOR] '
                oOutputParameterHandler.addParameter('siteUrl', aEntry)
            else:
                sTitle = '[COLOR skyblue]' + aEntry[0]+ '[/COLOR] '
                oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
            
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'Display_protected_link', sTitle, '', sThumbnail, '', oOutputParameterHandler)
   
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()  
  
def Display_protected_link():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')

    oParser = cParser()

    #Est ce un lien dl-protect ?
    if URL_PROTECT in sUrl or URL_PROTECTBIS in sUrl:
        sHtmlContent = DecryptddlProtect(sUrl) 
        if sHtmlContent:
            #Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotect = (True, [sHtmlContent])
            else:
                sPattern_dlprotect = 'target=_blank>([^<]+)<'
                aResult_dlprotect = oParser.parse(sHtmlContent, sPattern_dlprotect)
                
        else:
            oDialog = cConfig().createDialogOK('Desole, probleme de captcha.\n Veuillez en rentrer un directement sur le site, le temps de reparer')
            aResult_dlprotect = (False, False)

    #Si lien normal       
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotect = (True, [sUrl]) 
        
    if (aResult_dlprotect[0]):  
        for aEntry in aResult_dlprotect[1]:
            sHosterUrl = aEntry
            
            sTitle = sMovieTitle
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
                        
    oGui.setEndOfDirectory()

def DecryptddlProtect(url):

    if not (url): return ''
    
    cookies = ''
    #try to get previous cookie
    cookies = GestionCookie().Readcookie('liens_free-telechargement_org')

    oRequestHandler = cRequestHandler(url)
    if cookies:
        oRequestHandler.addHeaderEntry('Cookie',cookies)
    sHtmlContent = oRequestHandler.request()
    
    #A partir de la on a les bon cookies pr la protection cloudflare

    #Si ca demande le captcha
    if 'Veuillez recopier le captcha ci-dessus' in sHtmlContent:
        if cookies:
            GestionCookie().DeleteCookie('liens_free-telechargement_org')
            oRequestHandler = cRequestHandler(url)
            sHtmlContent = oRequestHandler.request()
            
        s = re.findall('src=".\/([^<>"]+?)" alt="CAPTCHA Image"',sHtmlContent)
        if URL_PROTECT in s[0]:
            image = s[0]
        else:
            image = URL_PROTECT + s[0]

        captcha,cookies2 = get_response(image,cookies)
        cookies = cookies + '; ' +cookies2

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent' , UA)
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4')
        oRequestHandler.addHeaderEntry('Accept' , 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('Cookie',cookies)
        oRequestHandler.addHeaderEntry('Referer',url)
        
        oRequestHandler.addParameters( 'do' , 'contact')
        oRequestHandler.addParameters( 'ct_captcha' , captcha)
        
        sHtmlContent = oRequestHandler.request()
        
        if 'Code de securite incorrect' in sHtmlContent:
            cConfig().showInfo("Erreur", 'Mauvais Captcha' , 5)
            return 'rate'
        
        if 'Veuillez recopier le captcha ci-dessus' in sHtmlContent:
            cConfig().showInfo("Erreur", 'Rattage' , 5)
            return 'rate'
            
        #si captcha reussi
        #save cookies
        GestionCookie().SaveCookie('liens_free-telechargement_org',cookies)        
    
    return sHtmlContent
	
def get_response(img,cookie):
    #on telecharge l'image

    hostComplet = re.sub(r'(https*:\/\/[^/]+)(\/*.*)','\\1',img)
    host = re.sub(r'https*:\/\/','',hostComplet)
    url = img                 

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent' , UA)
    #oRequestHandler.addHeaderEntry('Referer', url)
    oRequestHandler.addHeaderEntry('Cookie',cookie)

    htmlcontent = oRequestHandler.request()
    
    NewCookie = oRequestHandler.GetCookies()
	
    filename  = os.path.join(PathCache,'Captcha.raw')
    
    downloaded_image = file(filename, "wb")
    downloaded_image.write(htmlcontent)
    downloaded_image.close()

    #on affiche le dialogue
    solution = ''
    try:
        img = xbmcgui.ControlImage(450, 0, 400, 130, filename)
        wdlg = xbmcgui.WindowDialog()
        wdlg.addControl(img)
        wdlg.show()
        #xbmc.sleep(3000)
        kb = xbmc.Keyboard('', 'Tapez les Lettres/chiffres de l\'image', False)
        kb.doModal()
        if (kb.isConfirmed()):
            solution = kb.getText()
            if solution == '':
                cConfig().showInfo("Erreur", 'Vous devez taper le captcha' , 4)
        else:
            cConfig().showInfo("Erreur", 'Vous devez taper le captcha' , 4)
    finally:
        wdlg.removeControl(img)
        wdlg.close()
        
    return solution,NewCookie
