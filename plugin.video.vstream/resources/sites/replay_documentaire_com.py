#-*- coding: utf-8 -*-
#zombi.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.lib.util import cUtil
import re, urllib2

SITE_IDENTIFIER = 'replay_documentaire_com'
SITE_NAME = 'replay-documentaire'
SITE_DESC = 'Revoir très facilement tous vos documentaires en replay streaming'

URL_MAIN = 'http://www.replay-documentaire.com/'


DOC_NEWS = ('http://www.replay-documentaire.com/cat%C3%A9gories/documentaire/', 'showMovies')
DOC_DOCS = ('http://', 'load')

REPLAYTV_NEWS = ('http://www.replay-documentaire.com/', 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')
REPLAYTV_GENRES = (True, 'showGenres')

URL_SEARCH = ('http://replay-streaming.com/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


#bypass soucis ssl/tls SNI <kodi17
def sslBypass(url):

    UA = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    headers = { 'User-Agent' : UA }
    link = 'https://ooops.rf.gd/url.php?url=' + url
    request = urllib2.Request(link,None, headers)
    reponse = urllib2.urlopen(request)
    sHtmlContent = reponse.read()
    reponse.close()
    return sHtmlContent


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://frenchstream.org/les-plus-vues')
    oGui.addDir(SITE_IDENTIFIER, 'showGenres', 'Documentaires Genres', 'genres.png', oOutputParameterHandler)    
            
    oGui.setEndOfDirectory()
  
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://replay-streaming.com/?s='+sSearchText  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
    
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["telefilm","http://replay-streaming.com/categorie/telefilm/"] )
    liste.append( ["spectacle","http://replay-streaming.com/categorie/spectacle/"] )
    liste.append( ["concert","http://replay-streaming.com/categorie/concert/"] )
    liste.append( ["series","http://replay-streaming.com/categorie/series/"] )
    liste.append( ["telefoot","http://replay-streaming.com/categorie/telefoot/"] )
                
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
   
    try:
       oRequestHandler = cRequestHandler(sUrl)
       sHtmlContent = oRequestHandler.request()
    except:
       sHtmlContent = sslBypass(sUrl)
    
    sPattern = '<a class="img-holder" href="([^"]+)" title="([^"]+)" style="background-image: url\(([^\)]+)\);"><\/a>'
    
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
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', aEntry[1], 'doc.png', aEntry[2], "", oOutputParameterHandler)

        cConfig().finishDialog(dialog)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    #sPattern = 'id="tie-next-page"> <a href="([^<]+)">'
    sPattern = '<link rel="next" href="([^"]+)"/>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        
        url = aResult[1][0]
        if url.startswith('//'):
           url = 'http:' + url
        return url
    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    try:
       oRequestHandler = cRequestHandler(sUrl)
       sHtmlContent = oRequestHandler.request();
    except:
           sHtmlContent = sslBypass(sUrl)

    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','')
           
    sPattern = 'data-lazy-src="([^<]+)/.*?.mp4" scrolling="no"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            url = str(aEntry)
            if url.startswith('//'):
                url = 'http:' + url
            
            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog) 
                
    oGui.setEndOfDirectory()
