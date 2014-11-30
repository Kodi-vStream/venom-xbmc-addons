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
import re

SITE_IDENTIFIER = 'full_stream_net'
SITE_NAME = 'Full-Stream.net'
SITE_DESC = 'Film et Série en Streaming HD - Vk.Com - Netu.tv - ExaShare - YouWatch'

URL_MAIN = 'http://full-stream.net'

MOVIE_NEWS = ('http://full-stream.net/', 'showMovies')
MOVIE_VIEWS = ('http://full-stream.net/films-en-vk-streaming/', 'showMovies')
MOVIE_GENRES = (True, 'showGenre')
SERIE_SERIES = ('http://full-stream.net/seriestv/', 'showMovies')
SERIE_VFS = ('http://full-stream.net/seriestv/vf/', 'showMovies')
SERIE_VOSTFRS = ('http://full-stream.net/seriestv/vostfr/', 'showMovies')
ANIM_VFS = ('http://full-stream.net/mangas/mangas-vf/', 'showMovies')
ANIM_VOSTFRS = ('http://full-stream.net/mangas/mangas-vostfr/', 'showMovies')

URL_SEARCH = ('http://full-stream.net/xfsearch/', 'showMovies')
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
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus vues', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genre', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries VF', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries VOSTFR', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Animés VF', 'animes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Animés VOSTFR', 'animes.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()

 
def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            #sSearchText = cUtil().urlEncode(sSearchText)
            sUrl = 'http://full-stream.net/xfsearch/'+sSearchText+'/'  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
    
    
def getPremiumUser():
    sUrl = 'http://full-stream.net/'
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('login_name', 'vstream')
    oRequestHandler.addParameters('login_password', 'vstream')
    oRequestHandler.addParameters('Submit', '')
    oRequestHandler.addParameters('login', 'submit')
    oRequestHandler.request()

    aHeader = oRequestHandler.getResponseHeader()
    sReponseCookie = aHeader.getheader("Set-Cookie")

    return sReponseCookie


def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['HD/HQ','http://full-stream.net/films-en-vk-streaming/haute-qualite/'] )
    liste.append( ['Action','http://full-stream.net/films-en-vk-streaming/action/'] )
    liste.append( ['Aventure','http://full-stream.net/films-en-vk-streaming/aventure/'] )
    liste.append( ['Animation','http://full-stream.net/films-en-vk-streaming/animation/'] )
    liste.append( ['Arts Martiaux','http://full-stream.net/films-en-vk-streaming/arts-martiaux/'] )
    liste.append( ['Biopic','http://full-stream.net/films-en-vk-streaming/biopic/'] )
    liste.append( ['Comedie','http://full-stream.net/films-en-vk-streaming/comedie/'] )
    liste.append( ['Comedie Dramatique','http://full-stream.net/films-en-vk-streaming/comedie-dramatique/'] )
    liste.append( ['Comedie Musicale','http://full-stream.net/films-en-vk-streaming/comedie-musicale/'] )
    liste.append( ['Drame','http://full-stream.net/films-en-vk-streaming/drame/'] )
    liste.append( ['Documentaire','http://full-stream.net/films-en-vk-streaming/documentaire/'] ) 
    liste.append( ['Horreur','http://full-stream.net/films-en-vk-streaming/horreur/'] )
    liste.append( ['Fantastique','http://full-stream.net/films-en-vk-streaming/fantastique/'] )
    liste.append( ['Guerre','http://full-stream.net/films-en-vk-streaming/guerre/'] )
    liste.append( ['Policier','http://full-stream.net/films-en-vk-streaming/policier/'] )
                
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
    sHtmlContent = sHtmlContent.replace('&amp;w=210&amp;h=280','')
    sPattern = 'full-stream-view-hover"><img src="(.+?)".+?<h2><a href="(.+?)">(.+?)</a></h2>.+?<b>Résumé</b>(.+?)</div>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            if '/seriestv/' in sUrl  or 'saison' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', aEntry[2], '', aEntry[0], aEntry[3], oOutputParameterHandler)
            elif '/mangas/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', aEntry[2], '', aEntry[0], aEntry[3], oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', aEntry[2], '', aEntry[0], aEntry[3], oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<div class="navigation".+? <span.+? <a href="(.+?)">'
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
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('login_name', 'vstream')
    oRequestHandler.addParameters('login_password', 'vstream')
    oRequestHandler.addParameters('Submit', '')
    oRequestHandler.addParameters('login', 'submit')
    sHtmlContent = oRequestHandler.request();


    sPattern = '<iframe.+?src=[\'|"](.+?)[\'|"]'
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
            oHoster = cHosterGui().checkHoster(sHosterUrl)                   
        
            if (oHoster != False):         
                try:
                    oHoster.setHD(sHosterUrl)
                except: pass
                oHoster.setDisplayName(sMovieTitle)
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

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<a href="([^<]+)" title="([^<]+)" target="seriePlayer" class="ilink sinactive">'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = str(aEntry[0])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
        
            if (oHoster != False):
                sTitle = aEntry[1]
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog)    

    oGui.setEndOfDirectory()