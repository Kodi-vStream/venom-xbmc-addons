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
import re,urllib2,urllib

 
SITE_IDENTIFIER = 'full_streamvk_com'
SITE_NAME = 'Full-streamvk.com'
SITE_DESC = 'Film Serie et Anime en Streaming HD - Vk.Com - Netu.tv - ExaShare - YouWatch'
 
URL_MAIN = 'http://full-streamvk.com'
 
MOVIE_NEWS = ('http://full-streamvk.com/films-streamingvk-vf/', 'showMovies')
MOVIE_GENRES = (True, 'showGenre')
 
URL_SEARCH = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
 
def load():
    oGui = cGui()
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Nouveautees', 'news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genre', 'icon.png', oOutputParameterHandler)
           
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(sSearchText)
        oGui.setEndOfDirectory()
        return  
 
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action','http://full-streamvk.com/films-streamingvk-vf/streaming-action/'] )
    liste.append( ['Animation','http://full-streamvk.com/films-streamingvk-vf/streaming-animation/'] )
    liste.append( ['Arts Martiaux','http://full-streamvk.com/films-streamingvk-vf/streaming-arts-martiaux/'] )
    liste.append( ['Aventure','http://full-streamvk.com/films-streamingvk-vf/streaming-aventure/'] )
    liste.append( ['Biographique','http://full-streamvk.com/films-streamingvk-vf/streaming-biopic/'] )
    liste.append( ['Comedie','http://full-streamvk.com/films-streamingvk-vf/streaming-comedie/'] )
    liste.append( ['Musical','http://full-streamvk.com/films-streamingvk-vf/streaming-musical/'] )
    liste.append( ['Documentaire','http://full-streamvk.com/films-streamingvk-vf/streaming-documentaire/'] )
    liste.append( ['Dramatique','http://full-streamvk.com/films-streamingvk-vf/streaming-drame/'] )
    liste.append( ['Horreur','http://full-streamvk.com/films-streamingvk-vf/streaming-horreur/'] )
    liste.append( ['Espionnage','http://full-streamvk.com/films-streamingvk-vf/streaming-espionnage/'] )
    liste.append( ['Famille','http://full-streamvk.com/films-streamingvk-vf/streaming-famille/'] )
    liste.append( ['Fantastique','http://full-streamvk.com/films-streamingvk-vf/streaming-fantastique/'] )
    liste.append( ['Guerre','http://full-streamvk.com/films-streamingvk-vf/streaming-guerre/'] )
    liste.append( ['Historique','http://full-streamvk.com/films-streamingvk-vf/streaming-historique/'] )
    liste.append( ['Polcicier','http://full-streamvk.com/films-streamingvk-vf/streaming-policier/'] )
    liste.append( ['Romance','http://full-streamvk.com/films-streamingvk-vf/streaming-romance/'] )
    liste.append( ['Thriller','http://full-streamvk.com/films-streamingvk-vf/streaming-thriller/'] )
    liste.append( ['Science-Fiction','http://full-streamvk.com/films-streamingvk-vf/streaming-science-fiction/'] )
    liste.append( ['Manga','http://full-streamvk.com/films-streamingvk-vf/streaming-manga/'] )
    liste.append( ['Walt Disney','http://full-streamvk.com/films-streamingvk-vf/streaming-walt-disney/'] )
    liste.append( ['Western','http://full-streamvk.com/films-streamingvk-vf/streaming-western/'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
   
def showMovies(sSearch=''):
    oGui = cGui()
    if sSearch:
        #on redecode la recherhce codé il y a meme pas une seconde par l'addon
        sSearch = urllib2.unquote(sSearch)
       
        query_args = { 'do' : 'search' , 'subaction' : 'search' , 'story' : str(sSearch) , 'x' : '0', 'y' : '0'}
       
        data = urllib.urlencode(query_args)
        headers = {'User-Agent' : 'Mozilla 5.10'}
        url = 'http://www.full-streamvk.com/index.php?do=search=' + sSearch
        request = urllib2.Request(url,data,headers)
     
        try:
            reponse = urllib2.urlopen(request)
        except URLError, e:
            print e.read()
            print e.reason
     
        sHtmlContent = reponse.read()
        sPattern = '<div class="img-block border-2">.*?<img src="(.*?)" alt="(.*?)" class="img-poster border-2 shadow-dark7" width="151" height="215" />.+?<a href="(http://www.full-streamvk.*?)" title'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        #sPattern = '<div class="img-block border-2">.*?<img src="(.*?)" alt="(.*?)".*?<a href="(.*?)" title'
        sPattern = '<div class="img-block border-2">.*?<img src="(.*?)" alt="(.*?)".*?<a href="(http://www.full-streamvk.*?)" title'
       
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '')
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
           
           
            #sTitle = aEntry[2].decode('latin-1').encode("utf-8")
            #sThumbnail = 'http:'+str(aEntry[2])
            #sUrl = URL_MAIN+str(aEntry[1])
           
            sThumbnail = str(aEntry[0])
            if not 'full-streamvk' in sThumbnail:
                  sThumbnail = 'http://www.full-streamvk.com' + sThumbnail
            #print sThumbnail
 
     
 
 
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', aEntry[1], '', sThumbnail, '', oOutputParameterHandler)
           
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        print sNextPage
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

             
    if not sSearch:
        oGui.setEndOfDirectory() 
                
def __checkForNextPage(sHtmlContent):
    sPattern = 'href="([^<>]+?)">([Suivant >>])<\/a>'
    sPattern = '<a class="btn btn-default" href="(.+?)">[Suivant >>]<\/a>'
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
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('src="http://full-streamvk.com/','')
 
 
    sPattern = '<div class="fstory-video-block" id=".+?">.+?<iframe.+?src=[\'|"](.+?)[\'|"]'
    oParser = cParser()
    #print aResult
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
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
   
        cConfig().finishDialog(dialog)
 
    oGui.setEndOfDirectory()
