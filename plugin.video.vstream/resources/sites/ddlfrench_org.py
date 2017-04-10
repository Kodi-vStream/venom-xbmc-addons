#-*- coding: utf-8 -*-
#Zombi.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib import util
import re

SITE_IDENTIFIER = 'ddlfrench_org'
SITE_NAME = 'Ddlfrench'
SITE_DESC = 'TOP REPLAY TV'

URL_MAIN = 'http://ddlfrench.org/'

REPLAYTV_NEWS = ('http://ddlfrench.org/', 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')
REPLAYTV_GENRES = (True, 'showGenres')

URL_SEARCH = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'REPLAY TV (Derniers ajouts)', 'replay.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_GENRES[1], 'REPLAY TV (Par chaines)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
  
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'http://ddlfrench.org/index.php?story={'+sSearchText+'}&do=search&subaction=search'  
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['TF1',URL_MAIN + 'tf1'] )
    liste.append( ['France 2',URL_MAIN + 'france2'] )
    liste.append( ['France 3',URL_MAIN + 'france3'] )
    liste.append( ['France 4',URL_MAIN + 'france4'] )
    liste.append( ['France 5',URL_MAIN + 'france5'] )
    liste.append( ['France O',URL_MAIN + 'franceo'] )
    liste.append( ['ARTE',URL_MAIN + 'arte'] )
    liste.append( ['M6',URL_MAIN + 'm6'] )
    liste.append( ['W9',URL_MAIN + 'w9'] )
    liste.append( ['TMC',URL_MAIN + 'tmc'] )
    liste.append( ['NT1',URL_MAIN + 'nt1'] )
    liste.append( ['NRJ12',URL_MAIN + 'nrj12'] )
    liste.append( ['RMC DECOUVERTE',URL_MAIN + 'rmc-decouverte'] )
    liste.append( ['C8',URL_MAIN + 'c8'] )
    liste.append( ['CANAL+',URL_MAIN + 'canal-plus'] )
    liste.append( ['TNT CANALSAT',URL_MAIN + 'tnt-canalsat'] )

    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'tv.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      #sUrl = sSearch
      sUrl = 'http://ddlfrench.org/index.php?story={'+sSearch+'}&do=search&subaction=search'  
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #sPattern = "<div class='mediathumb'>.*?<a href='([^<]+)' title='([^<]+)'>.*?<img src='([^<]+)' alt='(.+?)'>.*?</a>"
    sPattern = '<div class="mov-i img-box"><img src="([^<]+)" alt="([^<]+)" /><div class="mov-mask flex-col ps-link" data-link="([^<]+)"><span'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[1]
            sUrl = str(aEntry[2])
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', aEntry[1], 'doc.png', aEntry[0], '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = 'class="pnext"><a href="([^<]+)"><span'
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
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sPattern = '<b>(.+?)2016<br' 
    sPattern = sPattern + '|' + '>E(.+?)<br'
    sPattern = sPattern + '|' + 'target="_blank">(.+?)</a>'
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
               oGui.addMisc(SITE_IDENTIFIER, 'showMovies','[COLOR red]'+ aEntry[0] + '[/COLOR]', 'series.png', '', '', oOutputParameterHandler)
    
            elif aEntry[1]:
                oOutputParameterHandler = cOutputParameterHandler()
                oGui.addMisc(SITE_IDENTIFIER, 'showMovies','[COLOR red]E'+ aEntry[1] + '[/COLOR]', 'series.png', '', '', oOutputParameterHandler)

            elif aEntry[2]:
                sHosterUrl = str(aEntry[2])
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog) 
  
    oGui.setEndOfDirectory()
