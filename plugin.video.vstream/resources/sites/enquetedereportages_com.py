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
 
SITE_IDENTIFIER = 'enquetedereportages_com'
SITE_NAME = 'Enquetedereportages.com'
SITE_DESC = 'replay tv'
 
URL_MAIN = 'http://enquetedereportages.com/'

DOC_NEWS = ('http://enquetedereportages.com', 'showMovies')
DOC_GENRES = ('http://', 'DocGenre')



DOC_DOCS =('http://', 'load')

#REPLAYTV_REPLAYTV = ('http://enquetedereportages.com/', 'showMovies')

REPLAYTV_NEWS = ('http://enquetedereportages.com', 'showMovies')

REPLAYTV_REPLAYTV = ('http://', 'load')
 
REPLAYTV_GENRES = (True, 'ReplayTV')

URL_SEARCH = ('http://enquetedereportages.com/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Nouveautés', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'DocGenre', 'Documentaire Genres', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'ReplayTV', 'Replay Genres', 'films.png', oOutputParameterHandler)
 
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    # oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Emissions', 'genres.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
    
def DocGenre():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://enquetedereportages.com/category/documentaire/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Documentaires', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://enquetedereportages.com/category/reportage/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Reportages', 'tv.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()  
    
def ReplayTV():

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
	
    liste.append( ['Discovery','http://enquetedereportages.com/category/discovery-channel/'] )
    liste.append( ['Emission','http://enquetedereportages.com/category/emission/'] )    
    liste.append( ['France2','http://enquetedereportages.com/category/france-2/'] )
    liste.append( ['France3','http://enquetedereportages.com/category/france-3/'] )
    
    liste.append( ['France4','http://enquetedereportages.com/category/france-4/'] )
    liste.append( ['FranceO','http://enquetedereportages.com/category/france-o/'] )    
    liste.append( ['M6','http://enquetedereportages.com/category/m6/'] )
    liste.append( ['NRJ12','http://enquetedereportages.com/category/nrj12/'] )
    liste.append( ['NT1','http://enquetedereportages.com/category/nt1/'] )
    
    liste.append( ['RMC','http://enquetedereportages.com/category/rmc-decouvertes/'] )
    liste.append( ['SportMeca','http://enquetedereportages.com/category/sports-meca/'] )    
    liste.append( ['TF1','http://enquetedereportages.com/category/tf1/'] )
    liste.append( ['TMC','http://enquetedereportages.com/category/tmc/'] )
    liste.append( ['W9','http://enquetedereportages.com/category/w9/'] )
    liste.append( ['Autre','http://enquetedereportages.com/category/uncategorized/'] )
    
    
 
    for sTitle,sUrl in liste:
 
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def showMoviesSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'http://enquetedereportages.com/?s='+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
   
 
 
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
	
    liste.append( ['Infrarouge','http://enquetedereportages.com/category/documentaire/infrarouge/'] )
    liste.append( ['Arte','http://enquetedereportages.com/category/documentaire/arte/'] )    
    liste.append( ['France4','http://enquetedereportages.com/category/documentaire/france-4-documentaire/'] )
    liste.append( ['France5','http://enquetedereportages.com/category/france-5/'] )
    
    liste.append( ['13eme-rue','http://enquetedereportages.com/category/reportage/13eme-rue/'] )
    liste.append( ['23eme','http://enquetedereportages.com/category/reportage/23eme/'] )    
    liste.append( ['6ter','http://enquetedereportages.com/category/reportage/6ter/'] )
    liste.append( ['Canal+','http://enquetedereportages.com/category/reportage/canal/'] )
    liste.append( ['D8','http://enquetedereportages.com/category/reportage/d8/'] )
    
    
    
   
 
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
   
    #sPattern = '<h1 class="genpost-entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a></h1><div class="genpost-entry-meta"> '
    #sPattern = '<figure class="genpost-featured-image"><a href="(.+?)" title="(.+?)"><img.+?src="(.+?)".+?</a></figure>'
    sPattern = '<article class="pexcerpt.+?"><a href="(.+?)" title="(.+?)".+?<img.+?src="(.+?)".+?/></div>.+?<div class="post-content image-caption-format-1">(.+?)</div>'
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
 
            sTitle = unicode(aEntry[1], 'utf-8')#converti en unicode
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore')#vire accent
            #sTitle = unescape(str(sTitle))
            sTitle = sTitle.encode( "utf-8")
            
            sTitle = re.sub('([0-9]+/[0-9]+/[0-9]+)','[COLOR teal]\\1[/COLOR]', str(sTitle))
            #sTitle = cUtil().DecoTitle(sTitle)
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            sTitle = sTitle.replace('http://enquetedereportages.com/','')
			 
           
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[2], aEntry[3], oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
 
 
 
def __checkForNextPage(sHtmlContent):
    #sPattern = '<a class="next page-numbers" href="(.+?)">Next <span class="meta-nav-next">'
    #sPattern = "<li class='current'>.+?<a.+?href='(.+?)' class='inactive'>"
    sPattern = "class='page-numbers current'>.+?<a class='page-numbers' href='(.+?)'>"
	
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
 
    sPattern = '<p><iframe src="(.+?)" width="540" height="290" frameborder="0" scrolling="no" allowfullscreen="allowfullscreen"></iframe></p'
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
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
 
        cConfig().finishDialog(dialog)
 
    oGui.setEndOfDirectory()
