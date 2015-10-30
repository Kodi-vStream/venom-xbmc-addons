#-*- coding: utf-8 -*-
#Venom.

#Cloudflare protection
#https://raw.githubusercontent.com/daniel-lundin/dreamfilm-xbmc/master/cloudflare.py
#https://gist.github.com/Rainbowed/8917670

from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig
import re, urllib, urllib2

SITE_IDENTIFIER = 'tv_streaming_ch'
SITE_NAME = 'Tv-streaming.ch'
SITE_DESC = 'Film/Serie/Documentaire/Anime en streaming'

URL_MAIN = 'http://tv-streaming.ch'

MOVIE_MOVIE = ('http://tv-streaming.ch/category/films/', 'showMovies')
MOVIE_NEWS = ('http://tv-streaming.ch/category/films/', 'showMovies')
MOVIE_GENRES = (True, 'showGenre')

SERIE_SERIES = ('http://tv-streaming.ch/category/series-tv/', 'showMovies')
SERIE_NEWS = ('http://tv-streaming.ch/category/series-tv/', 'showMovies')
SERIE_VFS = ('http://tv-streaming.ch/category/series-tv/serie-vf/', 'showMovies')
SERIE_VOSTFRS = ('http://tv-streaming.ch/category/series-tv/serie-vostfr/', 'showMovies')


ANIM_VFS = ('http://tv-streaming.ch/category/manga-vf/', 'showMovies')
ANIM_VOSTFRS = ('http://tv-streaming.ch/category/manga-vf/manga-vostfr/', 'showMovies')

DOC_DOCS = ('http://tv-streaming.ch/category/television/documentaire/', 'showMovies')

SPORT_SPORTS = ('http://tv-streaming.ch/category/sport/', 'showReplay')

REPLAYTV_REPLAYTV = ('http://', 'ReplayTV')

URL_SEARCH = ('http://tv-streaming.ch/?s=', 'showMovies')
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
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series Nouveautés', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series VF', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series VOSTFR', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés VF', 'animesvf.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés VOSTFR', 'animesvostfr.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://tv-streaming.ch/category/dessin-anime/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies' ,'Dessins animes', 'animesvf.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_DOCS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_DOCS[1], 'Documentaires', 'animesvostfr.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'ReplayTV' ,'Replay TV', 'animesvf.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  

def ReplayTV():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://tv-streaming.ch/category/television/tv-realite/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'TV realite', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://tv-streaming.ch/category/television/spectacles/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Spectacle', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://tv-streaming.ch/category/television/emission-tv/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Emission TV', 'tv.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://tv-streaming.ch/category/television/documentaire/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Documentaire', 'tv.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()        
    
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action','http://tv-streaming.ch/category/films/action-streaming/'] )
    liste.append( ['Animation','http://tv-streaming.ch/category/films/animation-streaming/'] )
    liste.append( ['Arts Martiaux','http://tv-streaming.ch/category/films/arts-martiaux/'] )
    liste.append( ['Aventure','http://tv-streaming.ch/category/films/aventure-streaming/'] )
    liste.append( ['Comedie','http://tv-streaming.ch/category/films/comedie-streaming/'] )
    liste.append( ['Drame','http://tv-streaming.ch/category/films/drame-streaming/'] )
    liste.append( ['Espionnage','http://tv-streaming.ch/category/films/espionnage-streaming/'] )   
    liste.append( ['Fantastique','http://tv-streaming.ch/category/films/fantastique/'] )
    liste.append( ['Guerre','http://tv-streaming.ch/category/films/guerre-streaming/'] )
    liste.append( ['Historique','http://tv-streaming.ch/category/films/historique-streaming/'] )
    liste.append( ['Horreur','http://tv-streaming.ch/category/films/epouvante-horreur/'] )
    liste.append( ['Musical','http://tv-streaming.ch/category/films/musical/'] )
    liste.append( ['Policier','http://tv-streaming.ch/category/films/policier/'] )
    liste.append( ['Thriller','http://tv-streaming.ch/category/films/thriller/'] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
      #correction
      sUrl = sUrl.replace(URL_SEARCH[0],'')
      sUrl = URL_SEARCH[0] + urllib.quote(sUrl)

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    #print sUrl
     
    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request()

    headers = {'User-Agent' : 'Mozilla 5.10'}
    request = urllib2.Request(sUrl,None,headers)
      
    try: 
        reponse = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print e.read()
        print e.reason
      
    sHtmlContent = reponse.read()
    reponse.close()
    
    #fh = open('c:\\test.txt', "w")
    ##fh.write(sHtmlContent)
    #fh.close()
    
    sPattern = '<div.*?class="moviefilm"><a.*?href="([^<]+)">.*?<img.*?src="([^<]+)" alt="(.+?)".+?>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == False):
        oGui.addNone(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            #sTitle = aEntry[2]+' - [COLOR azure]'+aEntry[3]+'[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1]))
            if '/films/' in sUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', aEntry[2], '', aEntry[1], '', oOutputParameterHandler) 
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', cUtil().DecoTitle(aEntry[2]),'', aEntry[1], '', oOutputParameterHandler)         
    
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
    if sUrl.endswith('/'):
        sUrl = sUrl+'100/'
    else:
        sUrl = sUrl+'/100/'
        
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #sHtmlContent = sHtmlContent.replace('<strong>Téléchargement VOSTFR','').replace('<strong>Téléchargement VF','').replace('<strong>Téléchargement','')
 
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
 
    sPattern = '<a *href="([^<]+)"><span>.+?<font class="">(.+?)<\/font><\/font>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle+' - '+aEntry[1]
            sTitle = cUtil().DecoTitle(sTitle)
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)            
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="nextpostslink" rel="next" href="(http:\/\/tv-streaming\.ch.+?)">(?:»|&raquo;)<\/a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
    
  
def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sHtmlContent = sHtmlContent.replace('facebook','<>')
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    #Recuperation des liens
    sPattern = '<iframe src="(http[^]+?)" [^<>]+?><\/iframe>'
    oParser = cParser()
    #aResult = oParser.parse(sHtmlContent, sPattern)
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult    
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sHoster = cHosterGui().checkHoster(aEntry[1].lower())
            if (sHoster != False):
                sTitle = sMovieTitle + aEntry[1]
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, comm, oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()  

def showHosters():
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
    
    print aResult
     
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
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
