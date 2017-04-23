#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig
import re, urllib

SITE_IDENTIFIER = 'tv_streaming_ch'
SITE_NAME = 'Tv-streaming'
SITE_DESC = 'Films/Séries/Animés/Documentaires/ReplayTV en streaming'

URL_MAIN = 'http://www.tv-streaming-serie.xyz/'

MOVIE_MOVIE = (URL_MAIN + 'category/films', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'category/films', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = (URL_MAIN + 'category/series-tv', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'category/series-tv', 'showMovies')
SERIE_VFS = (URL_MAIN + 'category/series-tv/serie-vf', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'category/series-tv/serie-vostfr', 'showMovies')

ANIM_VFS = (URL_MAIN + 'category/manga-vf', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'category/manga-vf/manga-vostfr', 'showMovies')
ANIM_ENFANTS = (URL_MAIN + 'category/dessin-anime', 'showMovies')

DOC_NEWS = (URL_MAIN + 'category/television/documentaire', 'showMovies')
DOC_DOCS = ('http://', 'load')

SPORT_SPORTS = (URL_MAIN + 'category/sport', 'showMovies')

REPLAYTV_GENRES = (True, 'ReplayTV')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

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
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'series_vf.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'series_vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/category/sitcoms/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Sitcoms', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'animes_vf.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'animes_vostfr.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ENFANTS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ENFANTS[1] ,'Dessins animés', 'animes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_GENRES[1] ,'Replay TV (Genres)', 'replay.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1] ,'Sport', 'sport.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + urllib.quote(sSearchText)
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  

def ReplayTV():
    oGui = cGui()
 
    liste = []
    liste.append( ['Animaux',URL_MAIN + 'category/television/animaux'] )
    liste.append( ['Concert',URL_MAIN + 'category/television/concert'] )
    liste.append( ['Documentaires',URL_MAIN + 'category/television/documentaire'] )
    liste.append( ['Emissions TV',URL_MAIN + 'category/television/emission-tv'] )
    liste.append( ['Historique',URL_MAIN + 'category/television/historique'] )
    liste.append( ['Journal',URL_MAIN + 'category/television/journal'] )
    liste.append( ['Karaoké',URL_MAIN + 'category/television/karaoke'] )
    liste.append( ['Météo',URL_MAIN + 'category/television/meteo'] )
    liste.append( ['Spécial',URL_MAIN + 'category/television/special'] )
    liste.append( ['TV réalité',URL_MAIN + 'category/television/tv-realite'] )
    liste.append( ['One Man Show',URL_MAIN + 'category/television/one-man-sohw'] )
    liste.append( ['Rétro',URL_MAIN + 'category/television/retro'] )
    liste.append( ['Rétro Souvenir',URL_MAIN + 'category/television/retro-souvenir'] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'tv.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def showGenres():
    oGui = cGui()
 
    liste = []
    liste.append( ['Action',URL_MAIN + 'category/films/action'] )
    liste.append( ['Animation',URL_MAIN + 'category/films/animation-streaming'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'category/films/arts-martiaux'] )
    liste.append( ['Aventure',URL_MAIN + 'category/films/aventure'] )
    liste.append( ['Comédie',URL_MAIN + 'category/films/comedie'] )
    liste.append( ['Drame',URL_MAIN + 'category/films/drame'] )
    liste.append( ['Epouvante-Horreur',URL_MAIN + 'category/films/epouvante-horreur'] )
    liste.append( ['Espionnage',URL_MAIN + 'category/films/espionnage'] )   
    liste.append( ['Fantastique',URL_MAIN + 'category/films/fantastique'] )
    liste.append( ['Famille',URL_MAIN + 'category/films/famille'] )
    liste.append( ['Guerre',URL_MAIN + 'category/films/guerre'] )
    liste.append( ['Historique',URL_MAIN + 'category/films/historique-streaming'] )
    liste.append( ['Musical',URL_MAIN + 'category/films/musical'] )
    liste.append( ['Policier',URL_MAIN + 'category/films/policier'] )
    liste.append( ['Science-fiction',URL_MAIN + 'category/films/science-fiction'] )
    liste.append( ['Romance',URL_MAIN + 'category/films/romance'] )
    liste.append( ['Thriller',URL_MAIN + 'category/films/thriller'] )
    liste.append( ['Western',URL_MAIN + 'category/films/western'] )
                
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

    
    sPattern = '<div.*?class="moviefilm"> *<a.*?href="([^<]+)">.*?<img.*?src="([^<]+)" alt="(.+?)".+?>'
    
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
                
            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sUrl.replace(URL_SEARCH[0],''),aEntry[2]) == 0:
                    continue
            
            #sTitle = aEntry[2]+' - [COLOR azure]'+aEntry[3]+'[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1]))
            sDisplayTitle = cUtil().DecoTitle(aEntry[2])
            if '/films/' in aEntry[0]:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', aEntry[2], '', aEntry[1], '', oOutputParameterHandler) 
            elif '/series-tv/' in aEntry[0] or '/manga/' in aEntry[0] or '/dessin-anime/' in aEntry[0]:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries',sDisplayTitle ,'', aEntry[1], '', oOutputParameterHandler) 
            else:
                oGui.addMisc(SITE_IDENTIFIER, 'showSeries',sDisplayTitle ,'', aEntry[1], '', oOutputParameterHandler)                 
    
        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries(sLoop = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    if sUrl.endswith('/'):
        sUrl = sUrl+'100/'
    else:
        sUrl = sUrl+'/100/'
        
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a *href="([^<]+)"><span>.+?<font class="">(.+?)<\/font><\/font>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #astuce en cas d'episode unique
    if (aResult[0] == False) and (sLoop == False):
        showHosters(True)
        return
    
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            episode = ''
            if aEntry[1]:
                episode = ' - ' + aEntry[1]
                
            sTitle = sMovieTitle + episode

            sDisplayTitle = cUtil().DecoTitle(sTitle)
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)            
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="nextpostslink" rel="next" href="(.+?)">(?:»|&raquo;)<\/a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
    
def showHosters(sLoop = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.replace('facebook','<>')
    
    sPattern = '<iframe.+?src="(http[^<>]+?)" [^<>]+?><\/iframe>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            if 'dailymotion' in aEntry:
                continue
            
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
