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

SITE_IDENTIFIER = 'streamzzz_com'
SITE_NAME = 'streamzzz.com'
SITE_DESC = 'Streaming series'

URL_MAIN = 'http://streamzzz.com/'

SERIE_SERIES = ('http://streamzzz.com/', 'showMovies')
#SERIE_VFS = ('http://www.telecharger-films.ws/telecharger-serie/series-fr/', 'showMovies')
#SERIE_VOSTFRS = ('http://www.telecharger-films.ws/telecharger-serie/sries-vostfr/', 'showMovies')

#MOVIE_GENRES = (True, 'showGenre')

def load():
    oGui = cGui()

    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    #oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    #oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'films.png', oOutputParameterHandler)
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    #oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries liste complete', 'series.png',oOutputParameterHandler)
    
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    #oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries VF', 'series.png', oOutputParameterHandler)
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    #oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries VOSTFR', 'series.png',oOutputParameterHandler)
    
            
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
    #sHtmlContent = sHtmlContent.replace('Programme', '').replace('F.A.Q', '').replace('Séries', '')
    sPattern = '<li><a href="(http:..streamzzz.com[^<]+)" title="([^<]+)">.+?</a></li>'
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
            
            sTitle=re.sub('(.*)(\[.*\])','\\1 [COLOR azure]\\2[/COLOR]', str(aEntry[1]))
            sMovieTitle=re.sub('(\[.*\])','', str(aEntry[1]))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))

            if '/series-tv/' in sUrl or 'saison' in aEntry[0]:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, 'tv.png', '', '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, 'tv.png', '', '', oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)

        oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch

    else:
      oInputParameterHandler = cInputParameterHandler()
      sUrl = oInputParameterHandler.getValue('siteUrl')
      sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
 
    sPattern = '<li><a href="(http:..streamzzz.com\/page[^<]+)" title=".+?">([^<]+)<.a><.li>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)


    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = str(aEntry[1])
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle )
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            oGui.addMisc(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, 'tv.png', '', '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="pagination-next" href="(.+?)">.+?</a>'
     
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0] == True):
        return aResult[1][0]

    return False
       
def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    
    #recuperation thumb
    sThumbnail = ''
    sPattern = 'style="cursor: default; float: left; margin: 0px 10px 10px 0px;" unselectable="on" src="([^<>"]+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sThumbnail = aResult[1][0]
        
    sPattern = '<a href="([^<>"]+?)" target="_blank"><img'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult
     
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
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
