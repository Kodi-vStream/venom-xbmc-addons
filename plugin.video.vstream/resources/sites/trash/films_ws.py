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
import re, urllib

SITE_IDENTIFIER = 'films_ws'
SITE_NAME = 'Telecharger-films.ws'
SITE_DESC = 'Streaming ou Telechargement films series mangas gratuitement et sans limite. Des films en exclusivite en qualite DVD a regarder ou telecharger'

URL_MAIN = 'http://www.telecharger-films.ws/'

MOVIE_NEWS = ('http://www.telecharger-films.ws/telecharger-films-gratuit/', 'showMovies')

SERIE_SERIES = ('http://www.telecharger-films.ws/telecharger-serie/', 'showMovies')
SERIE_VFS = ('http://www.telecharger-films.ws/telecharger-serie/series-fr/', 'showMovies')
SERIE_VOSTFRS = ('http://www.telecharger-films.ws/telecharger-serie/sries-vostfr/', 'showMovies')

MOVIE_GENRES = (True, 'showGenre')

URL_SEARCH = ('http://www.telecharger-films.ws/index.php?do=search&subaction=search&story=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series Nouveautés', 'series.png',oOutputParameterHandler)
    
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries VF', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries VOSTFR', 'series.png',oOutputParameterHandler)
    
            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://www.telecharger-films.ws/index.php?do=search&subaction=search&story='+sSearchText  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
    
    
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action','http://www.telecharger-films.ws/telecharger-films-action/'] )
    liste.append( ['Animation','http://www.telecharger-films.ws/telecharger-films-animation/'] )
    liste.append( ['Arts Martiaux','http://www.telecharger-films.ws/telecharger-films-arts-martiaux/'] )
    liste.append( ['Aventure','http://www.telecharger-films.ws/telecharger-films-aventure/'] )
    liste.append( ['Biopic','http://www.telecharger-films.ws/telecharger-films-biopic/'] )
    liste.append( ['Comedie','http://www.telecharger-films.ws/telecharger-films-comdie/'] )
    liste.append( ['Comedie Dramatique','http://www.telecharger-films.ws/telecharger-films-comdie-dramatique/'] )
    liste.append( ['Drame','http://www.telecharger-films.ws/telecharger-films-drame/'] )
    liste.append( ['Espionnage','http://www.telecharger-films.ws/telecharger-films-espionnage/'] )
    liste.append( ['Famille','http://www.telecharger-films.ws/telecharger-films-famille/'] )
    liste.append( ['Fantastique','http://www.telecharger-films.ws/telecharger-films-fantastique/'] )
    liste.append( ['Guerre','http://www.telecharger-films.ws/telecharger-films-guerre/'] )
    liste.append( ['Historique','http://www.telecharger-films.ws/telecharger-films-historique/'] )
    liste.append( ['Epouvante-Horreur','http://www.telecharger-films.ws/telecharger-films-epouvante-horreur/'] )
    liste.append( ['Musical','http://www.telecharger-films.ws/telecharger-films-musical/'] )
    liste.append( ['Policier','http://www.telecharger-films.ws/telecharger-films-policier/'] )
    liste.append( ['Romance','http://www.telecharger-films.ws/telecharger-films-romance/'] )
    liste.append( ['Science-Fiction','http://www.telecharger-films.ws/telecharger-films-science-fiction/'] )
    liste.append( ['Sport','http://www.telecharger-films.ws/telecharger-films-sport/'] )
    liste.append( ['Western','http://www.telecharger-films.ws/telecharger-film-western/'] )
    liste.append( ['Thriller','http://www.telecharger-films.ws/telecharger-films-thriller/'] )
                
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
    sHtmlContent = sHtmlContent.replace('[MULTI]', '').replace('Telecharger', '')
    sPattern = 'div class="storybtm">.+?<a title="([^<]+)" href="([^<]+)">.+?<!--dle_image_begin:.+?--><img src="(.+?)".+?<!--dle_image_end-->.+?<br /><i>(.+?)</i><br />'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult

    if (aResult[0] == False):
        oGui.addNone(SITE_IDENTIFIER)
        
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = aEntry[0].replace('gratuit','')
            sMovieTitle=re.sub('(\[.*\])','', str(sTitle))
            sTitle=re.sub('(.*)(\[.*\])','\\1 [COLOR azure]\\2[/COLOR]', str(sTitle))
            
            
            
            
            #oGuiElement = cGuiElement()
            #oGuiElement.setFileName(sMovieTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))
            if '/series-tv/' in sUrl or 'saison' in aEntry[0]:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, '', aEntry[2], aEntry[3], oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[2], aEntry[3], oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<strong>Téléchargement VOSTFR','').replace('<strong>Téléchargement VF','').replace('<strong>Téléchargement','')
 
    sPattern = '<span style="color: #33cccc;"><strong>([^<]+)|<p style="text-align: center;">([^<]+)<a (.+?)</p>'
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
                oGui.addMisc(SITE_IDENTIFIER, 'showSeries', '[COLOR red]'+str(aEntry[0])+'[/COLOR]', 'series.png', sThumbnail, '', oOutputParameterHandler)
            else:
                sTitle = sMovieTitle+' - '+aEntry[1]
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2]))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMisc(SITE_IDENTIFIER, 'serieHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = ' <span class="next"><a href="(.+?)">.+?</a></span>'
     
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
    sHtmlContent = sHtmlContent.replace('<iframe src="http://ads.affbuzzads.com','')


    sPattern = '<a href="([^<]+)" target="_blank">'
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
            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
        
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog) 

    oGui.setEndOfDirectory()
    
    
def mangaHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="http://ads.affbuzzads.com','')


    sPattern = '<p style="text-align: center;">([^<]+)<a href="([^<]+)" target="_blank">.+?</a></p>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = str(aEntry[1])
            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
        
            if (oHoster != False):
                sTitle = sMovieTitle+' - '+aEntry[0]
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
    
def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    sPattern = 'href="([^<]+)" target="_blank">.+?</a>'
    oParser = cParser()
    aResult = oParser.parse(sUrl, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = str(aEntry)
            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()