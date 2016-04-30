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
from resources.lib.config import cConfig

SITE_IDENTIFIER = 'reportagestv_com'
SITE_NAME = 'ReportagesTV.com'
SITE_DESC = 'Reportages TV - Replay des reportages télé français en streaming.'

URL_MAIN = 'http://www.reportagestv.com/'

DOC_NEWS = ('http://www.reportagestv.com/', 'showMovies')
DOC_DOCS = ('http://', 'load')
DOC_GENRES = (True, 'showGenre')

URL_SEARCH = ('http://www.reportagestv.com/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Nouveautés', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenre():
   
    oGui = cGui()
 
    liste = []
    liste.append( ["Reportage","http://www.reportagestv.com/"] )
    liste.append( ["Canal+","http://www.reportagestv.com/category/canal-plus/"] )
    liste.append( ["D8","http://www.reportagestv.com/category/d8/"] )
    liste.append( ["France 2","http://www.reportagestv.com/category/france-2/"] )
    liste.append( ["TF1","http://www.reportagestv.com/category/tf1/"] )
    liste.append( ["TMC","http://www.reportagestv.com/category/tmc/"] )    
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'doc.png', oOutputParameterHandler)
      
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Emmisions', 'doc.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory() 

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://www.reportagestv.com/?s='+sSearchText 
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
    

def showGenre():
    oGui = cGui()
 
    liste = []
    liste.append( ['Canal+ - Nouvelle Vie','http://www.reportagestv.com/category/canal-plus/nouvelle-vie/'] )
    liste.append( ['Canal+ - Spécial Investigation','http://www.reportagestv.com/category/canal-plus/special-investigation/'] )
    liste.append( ['D8 - Au coeur de l\'Enquête','http://www.reportagestv.com/category/d8/au-coeur-de-lenquete/'] )
    liste.append( ['D8 - En quête d\'Actualité','http://www.reportagestv.com/category/d8/en-quete-dactualite/'] )
    liste.append( ['France 2 - Apocalypse la 1ère guerre mondiale','http://www.reportagestv.com/category/france-2/apocalypse-la-1-ere-guerre-mondiale/'] )
    liste.append( ['France 2 - Envoyé Spécial','http://www.reportagestv.com/category/france-2/envoye-special/'] )
    liste.append( ['TF1 - Appels d\'Urgence','http://www.reportagestv.com/category/tf1/appels-durgence/'] )
    liste.append( ['TF1 - Sept à Huit','http://www.reportagestv.com/category/tf1/sept-a-huit/'] )
    liste.append( ['TMC - 90 Enquêtes','http://www.reportagestv.com/category/tmc/90-enquetes/'] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'doc.png', oOutputParameterHandler)
       
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
    sHtmlContent = sHtmlContent.replace('&#039;', '\'').replace('&#8217;', '\'')
    #sPattern = '<img src="([^<]+)" class="attachment.+?<h3 class="loop-title"><a href="([^<]+)" rel="bookmark">([^<]+)</a></h3>.+?<div class="mh-excerpt">(.+?)</a>'
    
    sPattern = '<img src="([^<]+)" class="attachment.+?<h3 class="entry-title mh-loop-title">.+?<a href="([^<]+)" rel="bookmark">([^<]+)</a></h3>.+?<div class="mh-excerpt">(.+?)</a>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', aEntry[2], '', aEntry[0], aEntry[3], oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = "<span class='page-numbers current'>.+?</span> <a class='page-numbers' href='(.+?)'>.+?</a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
    
def __checkForRealUrl(sHtmlContent):
    sPattern = '<p style="text-align: center;">.+?<a href="(.+?)".+?<input type="button".+?</a>'
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
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('&#039;', '\'').replace('&#8217;', '\'')
    sPattern = '<div class="entry clearfix">(.+?)<p style="text-align: center;">.+?<a href="(.+?)">.+?<input type="button".+?</div>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):

        for aEntry in aResult[1]:
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sMovieTitle, '', sThumbnail, aEntry[0], oOutputParameterHandler)
        

    oGui.setEndOfDirectory()
    

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request(); 

    sRealUrl = __checkForRealUrl(sHtmlContent)

    if (sRealUrl != False):
        oRequestHandler = cRequestHandler(sRealUrl)
        sHtmlContent = oRequestHandler.request(); 
        
    sPattern = '<iframe.+?src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
        
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            aEntry= aEntry.replace('//', 'http://')
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog) 
                
    oGui.setEndOfDirectory()
    