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
 
SITE_IDENTIFIER = 'vkstreamingfilm_biz'
SITE_NAME = 'Vkstreamingfilm.biz'
SITE_DESC = 'Film en Streaming HD'
 
URL_MAIN = 'http://vkstreamingfilm.biz'

MOVIE_MOVIE = ('http://www.vkstreamingfilm.biz/films/', 'showMovies') 
MOVIE_NEWS = ('http://www.vkstreamingfilm.biz/films/', 'showMovies')
MOVIE_GENRES = (True, 'showGenre')
 
URL_SEARCH = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
def DecoTitle(string):
    #pr les tag
    string = re.sub('([\[\(].{1,7}[\)\]])','[COLOR coral]\\1[/COLOR]', str(string))
    #pr les saisons
    string = re.sub('(?i)(.*)(saison [0-9]+)','\\1[COLOR coral]\\2[/COLOR]', str(string))
    return string
 
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
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genre', 'genres.png', oOutputParameterHandler)
           
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
    liste.append( ['Action','http://www.vkstreamingfilm.biz/films/action/'] )
    liste.append( ['Animation','http://www.vkstreamingfilm.biz/films/animation/'] )
    liste.append( ['Arts Martiaux','http://www.vkstreamingfilm.biz/films/arts-martiaux/'] )
    liste.append( ['Aventure','http://www.vkstreamingfilm.biz/films/aventure/'] )
    liste.append( ['Biographique','http://www.vkstreamingfilm.biz/films/biographique/'] )
    liste.append( ['Comedie','http://www.vkstreamingfilm.biz/films/comedie/'] )
    liste.append( ['Danse','http://www.vkstreamingfilm.biz/films/comedie/'] )
    liste.append( ['Documentaire','http://www.vkstreamingfilm.biz/films/documentaire/'] )
    liste.append( ['Drame','http://www.vkstreamingfilm.biz/films/drame/'] )
    liste.append( ['Epouvante-Horreur','http://www.vkstreamingfilm.biz/films/epouvante-horreur/'] )
    liste.append( ['Espionnage','http://www.vkstreamingfilm.biz/films/espionnage/'] )
    liste.append( ['Fantastique','http://www.vkstreamingfilm.biz/films/fantastique/'] )
    liste.append( ['Famille','http://www.vkstreamingfilm.biz/films/famille/'] )
    liste.append( ['Divers','http://www.vkstreamingfilm.biz/films/divers/'] )
    liste.append( ['Guerre','http://www.vkstreamingfilm.biz/films/guerre/'] )
    liste.append( ['Historique','http://www.vkstreamingfilm.biz/films/historique/'] )
    liste.append( ['Musical','http://www.vkstreamingfilm.biz/films/musical/'] )
    liste.append( ['Peplum','http://www.vkstreamingfilm.biz/films/peplum/'] )
    liste.append( ['Polcicier','http://www.vkstreamingfilm.biz/films/policier/'] )
    liste.append( ['Romance','http://www.vkstreamingfilm.biz/films/Romance/'] )
    liste.append( ['Science-Fiction','http://www.vkstreamingfilm.biz/films/science-fiction/'] )
    liste.append( ['Spectacle','http://www.vkstreamingfilm.biz/films/spectacle/'] )
    liste.append( ['Sport','http://www.vkstreamingfilm.biz/films/sport/'] )
    liste.append( ['Thriller','http://www.vkstreamingfilm.biz/films/thriller/'] )
    liste.append( ['Western','http://www.vkstreamingfilm.biz/films/western/'] )
               
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
        url = 'http://www.vkstreamingfilm.biz/index.php?do=search=' + sSearch
        request = urllib2.Request(url,data,headers)
     
        try:
            reponse = urllib2.urlopen(request)
        except URLError, e:
            print e.read()
            print e.reason
     
        sHtmlContent = reponse.read()
        sPattern = '<div class="img-block border-2">.*?<img src="(.*?)" alt="(.*?)" class="img-poster border-2 shadow-dark7" width="151" height="215".*?<a href="(http://www.vkstreamingfilm.*?)" title'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = '<div class="img-block border-2">.*?<img src="(.*?)" alt="(.*?)\sstreaming".*?<a href="(http://www.vkstreamingfilm.*?)" title'
       
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
           
            #sTitle = aEntry[2].decode('latin-1').encode("utf-8")
            #sThumbnail = 'http:'+str(aEntry[2])
            #sUrl = URL_MAIN+str(aEntry[1])
           
            sThumbnail = str(aEntry[0])
            if not 'http://www.vkstreamingfilm' in sThumbnail:
                  sThumbnail = 'http://www.vkstreamingfilm.fr' + sThumbnail
            #print sThumbnail
 
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sMovieTitle',str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', aEntry[1], '', sThumbnail, '', oOutputParameterHandler)
           
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
         
 
def __checkForNextPage(sHtmlContent):
   
    sPattern = '<div class="navigation">(?:<a href="http:[^<>]+?">[0-9]+<\/a> )*<span>[0-9]+<\/span> <a href="(.+?)">'
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
   
    #Recuperation qualitee
    qualite = ''
    sPattern = '<b>QualitÃ© :<\/b><\/span> +?<p class="text">([^<>()|]+)(?:\(.+?\))*[ |]*.+?<\/p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        qualite = ' [' + aResult[1][0] + ']'
        qualite = qualite.replace('VF','')
        qualite = qualite.replace('VOSTFR','')
        qualite = qualite.replace(' ]',']')
   
    #Recup langue
    langue = ''
    sPattern = '<a href="#(video[0-9]+?)" title=".+?" class="border-3"><span>.+?(\[.+?\])<\/span><\/a><\/li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        langue = aResult[1]
 
    sPattern = '<div class="fstory-video-block" id="(.+?)">.+?<iframe.+?src=[\'|"](.+?)[\'|"]'
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    sMovieTitle = sMovieTitle + qualite
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            sMovieTitle2 = sMovieTitle
            #Rajout lanques
            for aEntry9 in langue:
                if aEntry9[0] == aEntry[0]:
                    sMovieTitle2 = sMovieTitle + aEntry9[1]
           
            sHosterUrl = str(aEntry[1])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
           
            sMovieTitle2 = cUtil().DecoTitle(sMovieTitle2)
       
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle2)
                oHoster.setFileName(sMovieTitle2)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
 
        cConfig().finishDialog(dialog)
 
        oGui.setEndOfDirectory()
