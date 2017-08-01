#-*- coding: utf-8 -*-
#Razorex.TmpName
#
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
#from resources.lib.util import cUtil #outils pouvant etre utiles

import xbmc

SITE_IDENTIFIER = 'cinemavf'
SITE_NAME = 'CinemaVF'
SITE_DESC = 'Films, Séries & Mangas en streaming.'

URL_MAIN = 'http://cinemavf.info/'

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN , 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'film-en-streaming', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'film-en-streaming', 'showGenres')

SERIE_NEWS = (URL_MAIN + 'serie/', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'serie/', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'serie/', 'showGenres')

ANIM_NEWS = (URL_MAIN + 'mangas/', 'showMovies')
ANIM_ANIMS = (URL_MAIN + 'mangas/', 'showMovies')
ANIM_GENRES = (URL_MAIN + 'mangas/', 'showGenres')

def load():
    oGui = cGui()
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'animes_genres.png', oOutputParameterHandler)
    
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
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    if 'film' in sUrl:
        reqURL = MOVIE_GENRES[0]
        sStart = '<h3 class="widget-title">Genres du films</h3>'
        sEnd = '<footer id="footer">'
    elif 'serie' in sUrl:
        reqURL = SERIE_GENRES[0]
        sStart = '<h3 class="widget-title">Catégories</h3>'
        sEnd = '<footer id="footer">'
    else:
        reqURL = ANIM_GENRES[0]
        sStart = '<h3 class="widget-title">Catégories</h3>'
        sEnd = '<footer id="footer">'
        
    oParser = cParser()
    
    oRequestHandler = cRequestHandler(reqURL)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(sHtmlContent,sStart,sEnd)

    sPattern = '<li class="cat-item cat-item.+?"><a href="([^"]+)".+?>(.+?)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = str(aEntry[0])
            sTitle = str(aEntry[1])
            
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
    
    sPattern = '<div class="thumb">.+?<img src="([^<]+)" alt="(.+?)".+?>.+?<a href="(.+?)".+?'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = str(aEntry[1]).replace('&#8217;','\'')
            sUrl2 = str(aEntry[2])
            sThumb = str(aEntry[0])
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle',sTitle)
            oOutputParameterHandler.addParameter('sThumbnail',sThumb )

            if '/serie' in sUrl or '/mangas' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSaisons', sTitle,'', sThumb, '', oOutputParameterHandler)
            else:
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

def ShowSaisons():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumbnail')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<div class="season">.+?<h3>(.+?)</h3>|<a class="num_episode" href="(.+?)">(.+?)<span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            if (aEntry[0]):
                oGui.addText(SITE_IDENTIFIER,  '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')
            else:
                sUrl2 = str(aEntry[1])
                sTitle = str(aEntry[2]) + sMovieTitle
				
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle',sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail',sThumb )
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle,'', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()
	
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumbnail')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<div class="langue.*?">.*?<span>(.*?)<\/span>|<a onclick=".+?">\s*([^<>]+)\s*<\/a>\s*<input name="levideo" value="([^"]+)"'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
	
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if (aEntry[0]):
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]).upper() + '[/COLOR]')
            else:
                sHost = str(aEntry[1]).strip()
                sHost = sHost.replace('.to','').replace('.com','').replace('.me','').replace('.ec','').replace('.co','').replace('.eu','')
                sPost = str(aEntry[2])
                sTitle = ('%s (%s)') % (sMovieTitle, sHost)
            
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sPost', sPost)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumb)
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumbnail')
    sPost = oInputParameterHandler.getValue('sPost')
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addParameters('levideo', sPost)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<iframe.+?src=["\']([^"\']+)["\']'
    
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
