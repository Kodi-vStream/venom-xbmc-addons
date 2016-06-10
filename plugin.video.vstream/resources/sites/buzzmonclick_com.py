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
import urllib2,urllib,re
import unicodedata
 
SITE_IDENTIFIER = 'buzzmonclick_com'
SITE_NAME = 'buzzmonclick.com'
SITE_DESC = 'Film Streaming & Serie Streaming: Regardez films et series de qualité entièrement gratuit. Tout les meilleurs streaming en illimité.'
 
URL_MAIN = 'http://buzzmonclick.com/category/replay-tv/'

REPLAYTV_NEWS = ('http://buzzmonclick.com/category/replay-tv/', 'showMovies')

REPLAYTV_REPLAYTV = ('http://', 'load')
#REPLAYTV_REPLAYTV = ('http://buzzmonclick.com/category/replay-tv/', 'showMovies')
DOC_NEWS = ('http://buzzmonclick.com/category/replay-tv/documentaires/', 'showMovies')
DOC_DOCS = ('http://', 'load')

 
 
URL_SEARCH = ('http://buzzmonclick.com/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', 'Recherche', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Replay TV', 'films.png', oOutputParameterHandler)
    
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', DOC_DOCS[0])
    # oGui.addDir(SITE_IDENTIFIER, DOC_DOCS[1], 'Documentaires', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://buzzmonclick.com/category/replay-tv/divertissement/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Divertissement', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://buzzmonclick.com/category/replay-tv/infos-magazine/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Info/Magazines', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://buzzmonclick.com/category/replay-tv/series-tv/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://buzzmonclick.com/category/replay-tv/tele-realite/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Télé-Réalité', 'films.png', oOutputParameterHandler)
    
 
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    # oGui.addDir(SITE_IDENTIFI#ER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
    
 
def showMoviesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'http://buzzmonclick.com/?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
   
 
 
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
	
    liste.append( ['divertissement','http://buzzmonclick.com/category/replay-tv/divertissement/'] )
    liste.append( ['infos','http://buzzmonclick.com/category/replay-tv/infos-magazine/page/2/'] )
    liste.append( ['series','http://buzzmonclick.com/category/replay-tv/series-tv/'] )
    liste.append( ['tele realite','http://buzzmonclick.com/category/replay-tv/tele-realite/'] )
   
 
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
   
    #sPattern = 'data-id="[0-9]+" title="([^<]+)" href="([^<]+)"><span class="clip"><img src="([^<]+)" alt="'
    sPattern = 'class="post-thumbnail">.*?<a href="([^"]+)" title="([^"]+)".*?<img.*?src="([^"]+)".*?<div class="entry">.*?<p>([^>]+)</p>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sTitle = unicode(aEntry[1], 'utf-8')#converti en unicode
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')#vire accent
            #sTitle = unescape(str(sTitle))
            sTitle = sTitle.encode( "utf-8")
            #print sTitle
            
            #mise en page
            sTitle = sTitle.replace('Permalien pour', '')
            sTitle = re.sub('(?:,)* (?:Replay |Video )*du ([0-9]+ [a-zA-z]+ [0-9]+)',' (\\1)', str(sTitle))
            sTitle = re.sub(', (?:Replay|Video)$','', str(sTitle))
            
            
            #couleur
            #sTitle = cUtil().DecoTitle(sTitle)
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))
           
            #print str(sTitle)
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            if "/series-tv/" in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'series.png', aEntry[2], aEntry[3], oOutputParameterHandler)
            else:
                oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'doc.png', aEntry[2], aEntry[3], oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
 
 
def __checkForNextPage(sHtmlContent):
    #sPattern = '<span class=\'current\'>.+?</span><a class="page larger" href="(.+?)">'
    sPattern = '<span class="current">.+?</span><a href="(.+?)"'
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
    sHtmlContent = oRequestHandler.request()
 
    sPattern = 'iframe src="(.+?)"'
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
