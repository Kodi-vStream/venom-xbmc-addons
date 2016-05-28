#-*- coding: utf-8 -*-
#Venom.
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
import re, urllib

SITE_IDENTIFIER = 'streaming_series_org'
SITE_NAME = 'Streaming-Series'
SITE_DESC = 'Film en streaming, regarder film en direct, streaming vf regarder film gratuitement sur Frenchstream.org'

URL_MAIN = 'http://streaming-series.tv/'

#SERIE_SERIES = 'http://url' # serie nouveautés #30106
#SERIE_VFS = 'http://url' # serie VF #30107
#SERIE_VOSTFRS = 'http://url' # serie Vostfr #30108


SERIE_SERIES = (URL_MAIN, 'showMovies')
SERIE_VIEWS = (URL_MAIN + 'lesplusvues/', 'showMovies')
SERIE_COMMENTS = (URL_MAIN + 'lespluscommentees/', 'showMovies')
SERIE_NOTES = (URL_MAIN + 'lesmieuxnotees/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerieSearch', 'Recherche Séries', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries Nouveautés', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries Les plus Vues', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries Les plus Commentés', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries Les mieux Notés', 'films.png', oOutputParameterHandler)
    
            
    oGui.setEndOfDirectory()
 

def showSerieSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = URL_MAIN + '?s='+sSearchText  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return
            
                 
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action','http://streamingfilms.fr/category/action/'] )
    liste.append( ['Afro','http://streamingfilms.fr/category/afro/'] )
    liste.append( ['Animation','http://streamingfilms.fr/category/animation/'] )
    liste.append( ['Arts Martiaux','http://streamingfilms.fr/category/arts-martiaux/'] )
    liste.append( ['Aventure','http://streamingfilms.fr/category/aventure/'] )
    liste.append( ['Comedie','http://streamingfilms.fr/category/comedie/'] )
    liste.append( ['Disny','http://streamingfilms.fr/category/disneyy/'] )
    liste.append( ['Documentaire','http://streamingfilms.fr/category/documentaire/'] )
    liste.append( ['Drame','http://streamingfilms.fr/category/drame/'] )  
    liste.append( ['Espionage','http://streamingfilms.fr/category/espionnage/'] )
    liste.append( ['Famille','http://streamingfilms.fr/category/famille/'] ) 
    liste.append( ['Fantastique','http://streamingfilms.fr/category/fantastique/'] ) 
    liste.append( ['Guerre','http://streamingfilms.fr/category/guerre/'] )
    liste.append( ['Historique','http://streamingfilms.fr/category/historique/'] )         
    liste.append( ['Horreur','http://streamingfilms.fr/category/horreur/'] )
    liste.append( ['Musical','http://streamingfilms.fr/category/musical/'] ) 
    liste.append( ['Non classé','http://streamingfilms.fr/category/non-classe/'] )  
    liste.append( ['Policier','http://streamingfilms.fr/category/policier/'] )
    liste.append( ['Romance','http://streamingfilms.fr/category/romance/'] )
    liste.append( ['Science fiction','http://streamingfilms.fr/category/science-fiction/'] )
    liste.append( ['Spectacle','http://streamingfilms.fr/category/spectacle/'] )
    liste.append( ['Thriller','http://streamingfilms.fr/category/thriller/'] )
    liste.append( ['Western','http://streamingfilms.fr/category/western/'] )
               
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
    sHtmlContent = sHtmlContent.replace('//ad.advertstream.com/', '').replace('http://www.adcash.com/', '').replace('http://regie.espace-plus.net/', '')
    sPattern = '<div class="moviefilm"><a href=".+?"><img src="([^<]+)" alt=".+?" height=".+?" width=".+?" /></a><div class="movief"><a href="([^<]+)">([^<]+)</a></div><div class="movies"><small>(.+?)</small></div></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0],''),aEntry[2]) == 0:
                    continue

            sSmall = aEntry[3].replace('<span class="likeThis">', '').replace('</span>', '')
            sTitle = aEntry[2]+' - [COLOR azure]'+sSmall+'[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            if 'series' in sUrl:
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sDisplayTitle, '', aEntry[0], '', oOutputParameterHandler)
            else:
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', aEntry[0], '', oOutputParameterHandler)

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
    sUrl = sUrl+'100/'
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<a href="([^<]+)"><span>(.+?)</span></a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = sMovieTitle+' - '+aEntry[1]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<span class=\'current\'>.+?</span><a class="page larger" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sUrl = aResult[1][0]
        return sUrl

    return False


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','')
    sHtmlContent = sHtmlContent.replace('\r','')

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

            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
