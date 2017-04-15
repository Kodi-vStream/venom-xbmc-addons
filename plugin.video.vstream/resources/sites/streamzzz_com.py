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
import re,urllib,xbmc
import unicodedata
SITE_IDENTIFIER = 'streamzzz_com'
SITE_NAME = 'Streamzzz'
SITE_DESC = 'Streaming séries'

URL_MAIN = 'http://streamzzz.com/'

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

SERIE_SERIES = (URL_MAIN + 'tvshows/', 'showMovies')
SERIE_NEWS = (URL_MAIN, 'showSerieNews')
#SERIE_GENRES = (True, 'showGenres')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler) 


    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png',oOutputParameterHandler)

    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    #oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

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
    liste.append( ['Action',URL_MAIN + 'genre/action/'] )
    liste.append( ['Action & Aventure',URL_MAIN + 'genre/action-adventure/'] )
    liste.append( ['Animation',URL_MAIN + 'genre/animation/'] )
    liste.append( ['Aventure',URL_MAIN + 'genre/aventure/'] )
    liste.append( ['Biopic',URL_MAIN + 'genre/biopic/'] )
    liste.append( ['Comédie',URL_MAIN + 'genre/comedie/'] )
    liste.append( ['Crime',URL_MAIN + 'genre/crime/'] )
    liste.append( ['Documentaire',URL_MAIN + 'genre/documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'genre/drame/'] )
    liste.append( ['Familial',URL_MAIN + 'genre/familial/'] )
    liste.append( ['Fantastique',URL_MAIN + 'genre/fantastique/'] )
    liste.append( ['Histoire',URL_MAIN + 'genre/histoire/'] )
    liste.append( ['Horreur',URL_MAIN + 'genre/horreur/'] )
    liste.append( ['Musical',URL_MAIN + 'genre/musical/'] )
    liste.append( ['Mystère',URL_MAIN + 'genre/mystere/'] )
    liste.append( ['Mystery',URL_MAIN + 'genre/mystery/'] )
    liste.append( ['Romance',URL_MAIN + 'genre/romance/'] )
    liste.append( ['Sci-fi & Fantasy',URL_MAIN + 'genre/sci-fi-fantasy/'] )
    liste.append( ['Science-Fiction',URL_MAIN + 'genre/science-fiction/'] )
    liste.append( ['Science-Fiction & Fantastique',URL_MAIN + 'genre/science-fiction-fantastique/'] )
    liste.append( ['Suspense',URL_MAIN + 'genre/suspense/'] )
    liste.append( ['Thriller',URL_MAIN + 'genre/thriller/'] )
    liste.append( ['War & politics',URL_MAIN + 'genre/war-politics/'] )
    liste.append( ['Western',URL_MAIN + 'genre/western/'] )
    
    for sTitle,sUrl in liste:
    
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'series_genres.png', oOutputParameterHandler)
    
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
    oParser = cParser()
    #recuperation syn
    sSyn = ''
    sPattern = '<div class="category_desc">([^<]+)<\/div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sSyn = aResult[1][0]
    
    sPattern = '<li><a href="(http:..streamzzz.com\/page[^<]+)" title=".+?">([^<]+)<.a><.li>'
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
            
            oGui.addMisc(SITE_IDENTIFIER, 'listHosters', sDisplayTitle, 'tv.png', '', sSyn, oOutputParameterHandler)

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
    if (aResult[0] == True):
        return aResult[1][0]

    return False
       
def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumbnail')

    if 'regarder-film-gratuit' in sThumb:
        sUrl = sUrl.replace('http://streamzzz.com/page/','http://www.regarder-film-gratuit.com/')
        sUrl = unicode(sUrl,'utf-8')
        sUrl = unicodedata.normalize('NFD', unicode(sUrl)).encode('ascii', 'ignore')
        sUrl = re.search('([^"<>]+-[0-9]+)',sUrl)
        sUrl = sUrl.group(1)

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        oParser = cParser()
        sPattern = '<p><a href="([^"<>]+?)" target="_blank"><br\/>\s*<img src="http:\/\/www\.regarder-film-gratuit\.com'
        aResult = oParser.parse(sHtmlContent, sPattern)

    else:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        oParser = cParser()
        sPattern = '<a href="([^<>"]+?)" target="_blank"><img'
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
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)         
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
    
def showSerieNews():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
        
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<h1><a href="([^"]+)".+?title="([^"]+)".+?<body>.+?<img.+?rc="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = aEntry[0]
            filter = re.search('(\d+)-(\d+)',sUrl)
            if filter:
               continue
            sTitle = aEntry[1]
            sThumb = aEntry[2]
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)


        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSerieNews', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()
        
def listHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    #recuperation thumb
    sThumbnail = ''
    sPattern = '<body><p>.+?src="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sThumbnail = aResult[1][0]
        
    sPattern = '<a href="([^<>"]+?)" target="_blank"><img'
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
