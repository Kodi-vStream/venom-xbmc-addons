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

 
SITE_IDENTIFIER = 'full_streamvk_net'
SITE_NAME = 'Full-streamvk.net'
SITE_DESC = 'Film Serie et Anime en Streaming HD - Vk.Com - Netu.tv - ExaShare - YouWatch'
 
URL_MAIN = 'http://full-streamvk.com'
 
MOVIE_NEWS = (URL_MAIN + '/films-streamingvk-vf/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + '/films-streamingvk-vf/', 'showMovies')
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
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Nouveautés', 'news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films par Genres', 'icon.png', oOutputParameterHandler)
           
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
    liste.append( ['Action',URL_MAIN + '/films-streamingvk-vf/streaming-action/'] )
    liste.append( ['Animation',URL_MAIN + '/films-streamingvk-vf/streaming-animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + '/films-streamingvk-vf/streaming-arts-martiaux/'] )
    liste.append( ['Aventure',URL_MAIN + '/films-streamingvk-vf/streaming-aventure/'] )
    liste.append( ['Biographique',URL_MAIN + '/films-streamingvk-vf/streaming-biopic/'] )
    liste.append( ['Comedie',URL_MAIN + '/films-streamingvk-vf/streaming-comedie/'] )
    liste.append( ['Musical',URL_MAIN + '/films-streamingvk-vf/streaming-musical/'] )
    liste.append( ['Documentaire',URL_MAIN + '/films-streamingvk-vf/streaming-documentaire/'] )
    liste.append( ['Dramatique',URL_MAIN + '/films-streamingvk-vf/streaming-drame/'] )
    liste.append( ['Horreur',URL_MAIN + '/films-streamingvk-vf/streaming-horreur/'] )
    liste.append( ['Espionnage',URL_MAIN + '/films-streamingvk-vf/streaming-espionnage/'] )
    liste.append( ['Famille',URL_MAIN + '/films-streamingvk-vf/streaming-famille/'] )
    liste.append( ['Fantastique',URL_MAIN + '/films-streamingvk-vf/streaming-fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + '/films-streamingvk-vf/streaming-guerre/'] )
    liste.append( ['Historique',URL_MAIN + '/films-streamingvk-vf/streaming-historique/'] )
    liste.append( ['Polcicier',URL_MAIN + '/films-streamingvk-vf/streaming-policier/'] )
    liste.append( ['Romance',URL_MAIN + '/films-streamingvk-vf/streaming-romance/'] )
    liste.append( ['Thriller',URL_MAIN + '/films-streamingvk-vf/streaming-thriller/'] )
    liste.append( ['Science-Fiction',URL_MAIN + '/films-streamingvk-vf/streaming-science-fiction/'] )
    liste.append( ['Manga',URL_MAIN + '/films-streamingvk-vf/streaming-manga/'] )
    liste.append( ['Walt Disney',URL_MAIN + '/films-streamingvk-vf/streaming-walt-disney/'] )
    liste.append( ['Western',URL_MAIN + '/films-streamingvk-vf/streaming-western/'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
   
def showMovies(sSearch=''):
    oGui = cGui()
    if sSearch:
        #on redecode la recherhce code il y a meme pas une seconde par l'addon
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
        sPattern = '<div class="img-block border-2">.*?<img src="(.*?)" alt="(.*?)" class="img-poster border-2 shadow-dark7" width="151" height="215" />.+?<a href="(http:\/\/full-streamvk[^><"]+?)"'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = '<div class="img-block border-2">.*?<img src="(.*?)" alt="(.*?)".*?<a href="(http:\/\/full-streamvk[^><"]+?)"'
       
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '')
    
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
           
            sTitle = str(aEntry[1])
            sTitle = sTitle.replace(' Streaming VF','')
            sDisplayTitle = cUtil().DecoTitle(sTitle)
           
            sThumbnail = str(aEntry[0])
            if not sThumbnail.startswith('http'):
                  sThumbnail = URL_MAIN + sThumbnail
            #print sThumbnail
 
            oOutputParameterHandler = cOutputParameterHandler()

            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)
           
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

             
    if not sSearch:
        oGui.setEndOfDirectory() 
                
def __checkForNextPage(sHtmlContent):
    sPattern = '<div class="nextprev">.+?<a href="([^<>]+?)"><span class="pnext">Suivant<\/span>'
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
    #sHtmlContent = sHtmlContent.replace('src="http://full-streamvk.com/','')
 
 
    sPattern = '<iframe.+?src=[\'|"](.+?)[\'|"]'
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
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
   
        cConfig().finishDialog(dialog)
 
    oGui.setEndOfDirectory()
