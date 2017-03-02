#-*- coding: utf-8 -*-
#From chataigne73

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

import urllib, re,urllib2
import xbmcgui
import xbmc

from resources.lib.dl_deprotect import DecryptDlProtect

SITE_IDENTIFIER = 'megatrackmovies_net' 
SITE_NAME = '[COLOR violet]MegaTrackMovies[/COLOR]' 
SITE_DESC = 'Films en DDL, HD' 

URL_MAIN = 'http://megatrackmovies.net/'

URL_SEARCH_MOVIES = (URL_MAIN + 'index.php?do=search&subaction=search&titleonly=3&catlist%5B%5D=49&story=', 'showMovies')

URL_SEARCH = (URL_MAIN + 'index.php?do=search&subaction=search&titleonly=3&catlist%5B%5D=49&story=', 'showMovies')

FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'film', 'showMovies') # films nouveautés
MOVIE_EXCLUS = (URL_MAIN + 'exclu', 'showMovies') # exclus (films populaires)
MOVIE_HD = (URL_MAIN + 'blu-ray-720p', 'showMovies') # films en HD
MOVIE_HDLIGHT = (URL_MAIN + '720p-hdlight-x264', 'showMovies') # films en x265 et x264

MOVIE_GENRES = (True, 'showGenre')
MOVIE_VOSTFR = (URL_MAIN + 'vostfr', 'showMovies') # films VOSTFR
MOVIE_ANIME = (URL_MAIN + 'animation', 'showMovies') # dessins animes


def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovies', 'Recherche de films', 'search.png', oOutputParameterHandler) 
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EXCLUS[1], 'Exclus (Films populaires)', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Derniers Films ajoutes', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films en HD', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films x265/x264', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANIME[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Dessins Animes', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films Genre', 'genres.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory() 

def showSearchMovies(): 
    print "Entering showSearchMovies"
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText
        showMovies(sUrl) 
        oGui.setEndOfDirectory()
        return
    
def showGenre(): 
    oGui = cGui()
    
    liste = []
    liste.append( ['Action',URL_MAIN + 'action'] )
    liste.append( ['Animation',URL_MAIN + 'animation'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'arts-martiaux'] )
    liste.append( ['Aventure',URL_MAIN + 'aventure'] )
    liste.append( ['Biopic',URL_MAIN + 'biopic'] )
    liste.append( ['Comedie',URL_MAIN + 'comdie'] )
    liste.append( ['Comedie Musicale',URL_MAIN + 'comdie-musicale'] )
    liste.append( ['Documentaires',URL_MAIN + 'documentaire'] )
    liste.append( ['Drame',URL_MAIN + 'drame'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'epouvante-horreur'] ) 
    liste.append( ['Espionnage',URL_MAIN + 'espionnage'] )
    liste.append( ['Famille',URL_MAIN + 'famille'] )
    liste.append( ['Fantastique',URL_MAIN + 'fantastique'] )  
    liste.append( ['Guerre',URL_MAIN + 'guerre'] )
    liste.append( ['Historique',URL_MAIN + 'historique'] )
    liste.append( ['Musical',URL_MAIN + 'musical'] )
    liste.append( ['Policier',URL_MAIN + 'policier'] )
    liste.append( ['Romance',URL_MAIN + 'romance'] )
    liste.append( ['Science Fiction',URL_MAIN + 'science-fiction'] )
    liste.append( ['Thriller',URL_MAIN + 'thriller'] )
    liste.append( ['Western',URL_MAIN + 'western'] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)    
       
    oGui.setEndOfDirectory() 


def showMovies(sSearch = ''):
    #print "Entering showMovies"
    oGui = cGui()
    bGlobal_Search = False
    if sSearch:
        
        #par defaut
        sUrl = sSearch
        
        if URL_SEARCH[0] in sSearch:
            bGlobal_Search = True
        

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') 
        
    oRequestHandler = cRequestHandler(sUrl) 
    sHtmlContent = oRequestHandler.request()
    
	#Fonction pour recuperer uniquement les liens de la frame principale
    sHtmlContent = CutMainFrame(sHtmlContent)
    
    sPattern = '<div class="short-images radius-3"> *<a href="([^"]+)" title="(.+?)Qualité[^<]+<img src="([^<"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult 
    
    if (aResult[0] == True):
        total = len(aResult[1])        
        for aEntry in aResult[1]:

            sTitle = str(aEntry[1])
            sUrl2 = aEntry[0]
            #sFanart =aEntry[1]
            sThumbnail=aEntry[2]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl2)) 
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle)) 
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            oGui.addMisc(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)
            

        sNextPage = __checkForNextPage(sHtmlContent)#cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    #tPassage en mode vignette sauf en cas de recherche globale   
     
    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<div class="pages-numbers"> *<span>1</span> <a href="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        #print aResult
        return aResult[1][0]
        
    return False

    
def showMoviesLinks():
    #print "Entering showMoviesLinks"
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl) 
    sHtmlContent = oRequestHandler.request()
    #print sUrl
   
    oParser = cParser()
    
    #Recuperation infos
    sGenre = ''
    sDate = ''
    sCom = ''
    sBA = ''

    sPattern = 'height="325" src="([^"]+)".+?Date sortie:</div> *<div class="finfo-text">(.+?)</div>.+?<img src="/templates/flat-cinema/images/image.1.png".+?<b>(.+?)</b>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        sDate = aResult[1][0][1]
        sCom = aResult[1][0][2]
        sCom = cUtil().removeHtmlTags(sCom)
        sBA = aResult[1][0][0]
    if (sDate):
        oGui.addText(SITE_IDENTIFIER,'Date de Sortie : ' + str(sDate))
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sUrl',sBA)
    oOutputParameterHandler.addParameter('sMovieTitle', 'Voir la Bande annonce')
    oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
    oGui.addMovie(SITE_IDENTIFIER, 'ShowBA', 'Voir la Bande annonce', '', sThumbnail, '', oOutputParameterHandler)
    
    #Affichage du menu  
    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Qualités disponibles pour ce film :[/COLOR]')

    #on recherche d'abord la qualité courante
    sPattern = '<div class="finfo-title"> Titre :<\/div> *<div class="finfo-text"><b>.+?Qualité ([^<]+)<\/b><\/div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    sQual = ''
    if (aResult[0]):
        sQual = aResult[1][0]

    sTitle = sMovieTitle +  ' - [COLOR skyblue]' + sQual +'[/COLOR]'
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
    oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
    oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sCom, oOutputParameterHandler)

    #on regarde si dispo dans d'autres qualités
    sPattern = 'title="Téléchargez .+? QUALITÉ (.+?)" href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle +  ' - [COLOR skyblue]' + aEntry[0]+'[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sCom, oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)
    #xbmc.executebuiltin('Container.SetViewMode(503)')
    oGui.setEndOfDirectory()
   
 
def showHosters():# recherche et affiche les hotes
    #print "Entering showHosters"
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler() #apelle l'entree de paramettre
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumbnail=oInputParameterHandler.getValue('sThumbnail')
    
    #xbmc.log(sUrl)

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0')
    oRequestHandler.addHeaderEntry('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    sHtmlContent = oRequestHandler.request()

    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent.replace('\n',''))
    #fh.close()
    
    oParser = cParser()
    
    sPattern = '<b>\.\.([^<]+)</b></span></center></div> *<div class="dllinks"><a href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #xbmc.log(str(aResult))
        
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = '[COLOR skyblue]' + aEntry[0]+ '[/COLOR] ' + sMovieTitle
            oOutputParameterHandler = cOutputParameterHandler()
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

    #xbmc.log(sUrl)
    
    #Est ce un lien dl-protect ?
    if 'dl-protect' in sUrl:
        sHtmlContent = DecryptDlProtect(sUrl) 
        
        if sHtmlContent:
            #Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotect = (True, [sHtmlContent])
            else:
                sPattern_dlprotect = '><a href="(.+?)" target="_blank">'
                aResult_dlprotect = oParser.parse(sHtmlContent, sPattern_dlprotect)
            
        else:
            oDialog = cConfig().createDialogOK('Desole, probleme de captcha.\n Veuillez en rentrer un directement sur le site, le temps de reparer')
            aResult_dlprotect = (False, False)

    #Est ce un lien engine/tmpd ?
    elif 'engine/tmpd' in sUrl:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
    
        if sHtmlContent:
            sPattern_dlprotect = '><a href="(.+?)" target="_blank">'
            aResult_dlprotect = oParser.parse(sHtmlContent, sPattern_dlprotect)
    
    #Si lien normal       
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotect = (True, [sUrl]) 
        
    #print aResult_dlprotect
        
    if (aResult_dlprotect[0]):
            
        episode = 1
        
        for aEntry in aResult_dlprotect[1]:
            sHosterUrl = aEntry
            #print sHosterUrl
            
            sTitle = sMovieTitle
            if len(aResult_dlprotect[1]) > 1:
                sTitle = sMovieTitle + ' episode ' + str(episode)
            
            episode+=1
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
                        
    oGui.setEndOfDirectory()

def CutMainFrame(sHtmlContent):
    #print "Entering CutMainFrame"
    oParser = cParser()
    sPattern = '<div id=\'dle-content\'>(.+?)<div id="sidebar" class="radius-3">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        return aResult[1][0]
    #ok c'est une page battarde, dernier essais
    else:
        return sHtmlContent
    
    return ''
  
def ShowBA():
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('sUrl')
    #print sUrl
    video_id = re.findall('embed/(.+?)\?rel',sUrl)
    #print video_id
    xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/?action=play_video&videoid='+video_id[0]+')')
    
    return
