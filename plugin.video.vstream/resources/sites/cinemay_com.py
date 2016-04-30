#-*- coding: utf-8 -*-
#Venom.
#rajout fonction pour listage Film Nouveauté par Kodigoal

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

import re,unicodedata

SITE_IDENTIFIER = 'cinemay_com' 
SITE_NAME = 'Cinemay.com' 
SITE_DESC = 'films et series en streaming' 

URL_MAIN = 'http://cinemay.com' 

MOVIE_NEWS = ('http://www.cinemay.com/', 'showMoviesNews')

MOVIE_MOVIE = ('http://www.cinemay.com/films/', 'showMovies')
MOVIE_GENRES = (True, 'showGenre')

SERIE_SERIES = ('http://www.cinemay.com/serie/', 'showMovies')

URL_SEARCH = ('http://www.cinemay.com/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load(): 
    oGui = cGui() 

    oOutputParameterHandler = cOutputParameterHandler() 
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/') 
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler) 
    
    #rajout listage film nouveauté   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'news.png', oOutputParameterHandler)
  
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films Genres', 'genres.png', oOutputParameterHandler) 
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)
    
            
    oGui.setEndOfDirectory() 

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = 'http://cinemay.com/?s='+sSearchText  
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
       
def showGenre():
    oGui = cGui()
 
    liste = []
    liste.append( ['Action','http://www.cinemay.com/action/'] )
    liste.append( ['Animation','http://www.cinemay.com/animation/'] )
    liste.append( ['Arts Martiaux','http://www.cinemay.com/arts-martiaux/'] )
    liste.append( ['Aventure','http://www.cinemay.com/aventure/'] )
    liste.append( ['Biopic','http://www.cinemay.com/biopic/'] )
    liste.append( ['Comédie','http://www.cinemay.com/comedie/'] )
    liste.append( ['Comédie Dramatique','http://www.cinemay.com/comedie-dramatique/'] )
    liste.append( ['Documentaire','http://www.cinemay.com/documentaire/'] )
    liste.append( ['Drame','http://www.cinemay.com/drame/'] )
    liste.append( ['Epouvante Horreur','http://www.cinemay.com/epouvante-horreur/'] ) 
    liste.append( ['Espionnage','http://www.cinemay.com/espionnage/'] )
    liste.append( ['Famille','http://www.cinemay.com/famille/'] )
    liste.append( ['Fantastique','http://www.cinemay.com/fantastique/'] )  
    liste.append( ['Guerre','http://full-streaming.org/guerre/'] )
    liste.append( ['Historique','http://www.cinemay.com/histoirique/'] )
    liste.append( ['Manga','http://www.cinemay.com/manga/'] )    
    liste.append( ['Musical','http://www.cinemay.com/musical/'] )
    liste.append( ['Non_classé','http://www.cinemay.com/non-classe/'] )
    liste.append( ['peplum','http://www.cinemay.com/peplum-2/'] )        
    liste.append( ['Policier','http://www.cinemay.com/policier/'] )
    liste.append( ['Romance','http://www.cinemay.com/romance/'] )
    liste.append( ['Science_Fiction','http://www.cinemay.com/science-fiction/'] )
    liste.append( ['Spéctacle','http://www.cinemay.com/spectacle/'] )
    liste.append( ['Thriller','http://www.cinemay.com/thriller/'] )
    liste.append( ['Western','http://www.cinemay.com/western/'] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

       
    oGui.setEndOfDirectory() 

def showMoviesNews():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
     
    oParser = cParser()
    #Decoupage pour cibler la partie Film ajouté    
    sPattern = '<h1>Dernier Films Ajouté</h1>(.+?)</body>'
   
    aResult = oParser.parse(sHtmlContent, sPattern)
    #regex pour listage films sur la partie decoupée  
    sHtmlContent = aResult
    
    sPattern = '<img class="imgpic" src="(.+?)".+?/>.+?<h3.+?><a href="(.+?)"  title=".+?">.+?<strong>(.+?)</strong></a>.+?</h3>.+?<div class="infob">.+?<p>(.+?)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
      
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            #encode/decode pour affichage des accents
            sTitle = unicode(aEntry[2].replace('streaming','').replace('Streaming',''), 'utf-8')
            
            sTitle = unicodedata.normalize('NFD', sTitle).encode('ascii', 'ignore').decode("unicode_escape")
            sTitle = sTitle.encode("latin-1")
            
            sCom = aEntry[3]
            sCom = sCom.decode("unicode_escape").encode("latin-1")
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))

            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, aEntry[0], aEntry[0], sCom, oOutputParameterHandler)

        cConfig().finishDialog(dialog)
            
    oGui.setEndOfDirectory()

    
    
def showMovies(sSearch=''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sPattern = '<img class=".+?" src="([^<]+)" title="(.+?)".+?<a href="(.+?)"'
    sPattern = '<img class="imgpic" src="(.+?)".+?/>.+?<h3.+?><a href="(.+?)"  title=".+?">.+?<strong>(.+?)</strong></a>.+?</h3>.+?<div class="infob">.+?<p>(.+?)</p>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[2].replace('streaming','').replace('Streaming','')
            
            sCom = aEntry[3]
            #sCom = sCom.decode("utf-8", "ignore")
            sCom = sCom.decode("unicode_escape").encode("latin-1")
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            if '/serie/' in sUrl or '/serie/' in aEntry[0]:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, aEntry[0], aEntry[0], sCom , oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, aEntry[0], aEntry[0], sCom, oOutputParameterHandler)

        cConfig().finishDialog(dialog)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<span class=\'current\'>.+?</span><a class="page larger" href="(.+?)">.+?</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    if (aResult[0] == True):
        sNext = aResult[1][0]
        return sNext

    return False
    

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
 
    sPattern = '<ul class="css-tabs_series skin3">(.+?)</ul><div class="css-panes_series skin3">(.+?)</div></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    list = str(aResult[1][0][0]).split('<li>')
    list2 = str(aResult[1][0][1]).split('<div>')

    newList = ''
    for index, item in enumerate(list):
        item2 = list2[index]        
        newList+=( item + item2)

        
    sPattern = '<a href="#">([^<]+)</a>|<li class="bordred"><small><em>.+?</em></small>.+?<a href="([^<]+)" class="link_series_epi">([^<]+)</a></li>'

    oParser = cParser()
    aResult = oParser.parse(newList, sPattern)
    
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
                sSaison = aEntry[0]
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR red]'+str(aEntry[0])+'[/COLOR]', 'host.png', oOutputParameterHandler)
                
            else: 
                sTitle = sMovieTitle+' -'+sSaison+aEntry[2]
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)            
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()    
def showLinks():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('&#039;', '\'').replace('&#8217;', '\'')
    sPattern = '<td><a href="(.+?)">(.+?)</a>.+?<span class="user-icn">'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):

        for aEntry in aResult[1]:
            
            sHoster = cHosterGui().checkHoster(aEntry[1].lower())
            if (sHoster != False):
            
                sTitle = sMovieTitle + ' - [COLOR skyblue]' + sHoster.getDisplayName()+'[/COLOR]'
                sUrl = URL_MAIN+aEntry[0]
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)
        

    oGui.setEndOfDirectory() 
    

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<iframe src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult
    if (aResult[0] == True):

        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry)
            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
        
            if (oHoster != False):
                #sMovieTitle=re.sub(r'\[.*\]',r'',sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
