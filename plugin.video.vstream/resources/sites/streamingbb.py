#-*- coding: utf-8 -*-
#Razorex
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser

from resources.lib.util import cUtil #outils pouvant etre utiles

import xbmc

SITE_IDENTIFIER = 'streamingbb'
SITE_NAME = 'StreamingBB'
SITE_DESC = 'Films en streaming'

URL_MAIN = 'http://www.streamingbb.tv/'

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN, 'showMoviesNews')
MOVIE_MOVIE = (URL_MAIN, 'showMoviesNews')
MOVIE_GENRES = (True, 'showGenres')

def load():
    oGui = cGui()
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    
    liste = []
    liste.append( ['Action',URL_MAIN + 'film-category/action'] )
    liste.append( ['Animation',URL_MAIN + 'film-category/animation'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'film-category/arts-martiaux'] )
    liste.append( ['Aventure',URL_MAIN + 'film-category/aventure'] )
    liste.append( ['Biopic',URL_MAIN + 'film-category/biopic'] )
    liste.append( ['Bollywood',URL_MAIN + 'film-category/bollywood'] )
    liste.append( ['Classique',URL_MAIN + 'film-category/classique'] )
    liste.append( ['Comédie',URL_MAIN + 'film-category/comedie'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + 'film-category/comedie-dramatique'] )
    liste.append( ['Comédie Musicale',URL_MAIN + 'film-category/comedie-musicale'] )
    liste.append( ['Concert',URL_MAIN + 'film-category/concert'] )
    liste.append( ['Dessin animé',URL_MAIN + 'film-category/dessin-anime'] )
    liste.append( ['Divers',URL_MAIN + 'film-category/divers'] ) 
    liste.append( ['Documentaire',URL_MAIN + 'film-category/documentaire'] )
    liste.append( ['Drame',URL_MAIN + 'film-category/drame'] )
    liste.append( ['Emissions TV',URL_MAIN + 'film-category/emissions-tv'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'film-category/epouvante-horreur'] )
    liste.append( ['Erotique',URL_MAIN + 'film-category/erotique'] )
    liste.append( ['Espionnage',URL_MAIN + 'film-category/espionnage/'] )
    liste.append( ['Expérimental',URL_MAIN + 'film-category/experimental'] )
    liste.append( ['Famille',URL_MAIN + 'film-category/famille'] )
    liste.append( ['Fantastique',URL_MAIN + 'film-category/fantastique'] )
    liste.append( ['Guerre',URL_MAIN + 'film-category/guerre'] )
    liste.append( ['Historique',URL_MAIN + 'film-category/historique'] )
    liste.append( ['Judiciaire',URL_MAIN + 'film-category/judiciaire'] )
    liste.append( ['Musical',URL_MAIN + 'film-category/musical'] )
    liste.append( ['Non classé',URL_MAIN + 'film-category/non-classe'] )
    liste.append( ['Opéra',URL_MAIN + 'film-category/opera'] )
    liste.append( ['Péplum',URL_MAIN + 'film-category/peplum'] )
    liste.append( ['Policier',URL_MAIN + 'film-category/policier'] )
    liste.append( ['Romance',URL_MAIN + 'film-category/romance'] )
    liste.append( ['Science Fiction',URL_MAIN + 'film-category/science-fiction'] )
    liste.append( ['Show',URL_MAIN + 'film-category/show'] )
    liste.append( ['Spectacle',URL_MAIN + 'film-category/spectacle'] )
    liste.append( ['Sport enet',URL_MAIN + 'film-category/sport-event'] )
    liste.append( ['Thriller',URL_MAIN + 'film-category/thriller'] )
    liste.append( ['Vieux Films',URL_MAIN + 'film-category/vieux-films'] )
    liste.append( ['Walt Disney',URL_MAIN + 'film-category/walt-disney'] )
    liste.append( ['Western',URL_MAIN + 'film-category/western'] )
	
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory() 


def showMoviesNews():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    #Decoupage pour cibler la partie Dernier Films Ajouté
    sPattern = '<span class="name">Dernier Films Ajouté :</span>(.+?)<div id="sidebar" role="complementary" class="masonry">'
	
    aResult = oParser.parse(sHtmlContent, sPattern)
    sHtmlContent = aResult
	
    #regex pour listage films sur la partie decoupée
    sPattern = '<div class="thumb">.+?<img src="([^<]+)" alt="(.+?)".+?<a href="(.+?)"'
    
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sThumb = str(aEntry[0])
            sTitle = str(aEntry[1]).decode("unicode_escape").encode("latin-1")
            sUrl = str(aEntry[2])
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb )

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)
            
        cConfig().finishDialog(dialog)
		
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMoviesNews', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

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
    #Decoupage pour cibler la partie Film hors carroussel
    sPattern = '<div class="loop-header below-no-actions">(.+?)<div id="sidebar" role="complementary" class="masonry">'
	
    aResult = oParser.parse(sHtmlContent, sPattern)
    sHtmlContent = aResult
	
    #regex pour listage films sur la partie decoupée
    sPattern = '<div class="thumb">.+?<img src="([^<]+)" alt="(.+?)".+?<a href="(.+?)"'
    
    aResult = oParser.parse(sHtmlContent, sPattern)
    #cConfig().log(str(aResult)) #Commenter ou supprimer cette ligne une fois fini
    
    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sThumb = str(aEntry[0])
            sTitle = str(aEntry[1]).decode("unicode_escape").encode("latin-1")
            sUrl = str(aEntry[2])
            
            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), sTitle) == 0:
                    continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb )

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)
                
        cConfig().finishDialog(dialog)
           
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a class="nextpostslink" rel="next" href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        return aResult[1][0]

    return False


def showLinks():
    oGui = cGui()
	
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<form action="#playfilm" method="post">.+?<span>([^<>]+)</span>.+?<input name="levideo" value="([^"]+)"'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHost = str(aEntry[0])#.strip()
            sHost = sHost.replace('.to', '').replace('.com', '').replace('.co', '').replace('.me', '').replace('.ec', '').replace('.eu', '').replace('.sx', '')
            sPost = str(aEntry[1])
            sTitle = ('%s (%s)') % (sMovieTitle, sHost)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sPost', sPost)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()  

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sPost = oInputParameterHandler.getValue('sPost')
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addParameters('levideo', sPost)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<iframe.+?src=["\'](.+?)["\']'
    
    aResult = oParser.parse(sHtmlContent, sPattern)
    #pensez a faire un cConfig().log(str(aResult)) pour verifier
    #cConfig().log(str(sUrl))
    #cConfig().log(str(aResult))
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            sHosterUrl = str(aEntry)
            if sHosterUrl.startswith('/'):
                sHosterUrl = 'http:' + sHosterUrl
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                
    oGui.setEndOfDirectory()
