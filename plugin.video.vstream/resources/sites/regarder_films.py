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
 
SITE_IDENTIFIER = 'regarder_films'
SITE_NAME = 'Regarder-films-gratuit'
SITE_DESC = 'Streaming ou Telechargement films series mangas gratuitement et sans limite. Des films en exclusivite en qualite DVD a regarder ou telecharger'
 
URL_MAIN = 'http://www.regarder-film-gratuit.com/'
 
SERIE_SERIES = ('http://www.regarder-film-gratuit.com/', 'showMovies')
 
URL_SEARCH = ('http://www.regarder-film-gratuit.com/?s=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'
 
def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Series Nouveautees', 'series.png',oOutputParameterHandler)
   
   
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    #oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries VF', 'series.png', oOutputParameterHandler)
   
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    #oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries VOSTFR', 'series.png',oOutputParameterHandler)
   
           
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText  
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return 
 
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
        showSeries()
        return
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('Programme', '').replace('F.A.Q', '').replace('Séries', '')
    sPattern = '<li class="cat-item cat-item-.+?"><a href="(.+?)">([^<]+)</a>'
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
           
            sTitle = str(aEntry[1])
            sDisplayTitle = cUtil().DecoTitle(sTitle)
 
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            if '/series-tv/' in sUrl or 'saison' in aEntry[0]:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sDisplayTitle, 'tv.png', '', '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sDisplayTitle, 'tv.png', '', '', oOutputParameterHandler)
       
        cConfig().finishDialog(dialog)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
 
    else:
      oInputParameterHandler = cInputParameterHandler()
      sUrl = oInputParameterHandler.getValue('siteUrl')
      sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
      #sThumbnail = oInputParameterHandler.getValue('sThumbnail')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('<strong>Téléchargement VOSTFR','').replace('<strong>Téléchargement VF','').replace('<strong>Téléchargement','')
 
    sPattern = '<div class="post".+?<h2><a class="title" href="(.+?)" rel="bookmark">(.+?)</a></h2>'
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
                
            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0],''),aEntry[1]) == 0:
                    continue                
                
            sTitle = aEntry[1]
            sUrl = str(aEntry[0])
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            if ('Information' not in sTitle) and ('/liste-de-series/' not in sUrl) and ('/versions-francaises/' not in sUrl):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

                oGui.addMisc(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, '', '', '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
 
def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="nextpostslink" rel="next" href="(.+?)">..<'
    aResult = re.findall(sPattern,sHtmlContent,re.UNICODE)
    if (aResult):
        return aResult[0]
 
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
    sPattern = '<p><img src="([^<>"]+?)" alt=".+?" class="aligncenter size-full wp-image-[0-9]+"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sThumbnail = aResult[1][0]
        
    #print aResult
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
       
    sPattern = '<p><a href="([^"<>]+?)" target="_blank"><br\/>\s*<img src="http:\/\/www\.regarder-film-gratuit\.com'
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
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)        
   
        cConfig().finishDialog(dialog)
 
    oGui.setEndOfDirectory()
