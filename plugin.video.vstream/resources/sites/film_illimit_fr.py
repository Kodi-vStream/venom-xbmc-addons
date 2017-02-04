#-*- coding: utf-8 -*-
#Venom.
#
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
import re,urllib,urllib2,xbmc

from resources.lib.sucuri import SucurieBypass
 
SITE_IDENTIFIER = 'film_illimit_fr'
SITE_NAME = 'Film illimite'
SITE_DESC = 'Films HD en streaming'
 
#URL_MAIN = 'http://xn--official-film-illimit-v5b.fr/'
URL_MAIN = 'http://official-film-illimite.net/'

MOVIE_NEWS = (URL_MAIN , 'showMovies')
MOVIE_HD = (URL_MAIN + '720p1080p/', 'showMovies')
#MOVIE_MOVIE = (True, 'showAlpha')
MOVIE_GENRES = (True, 'showGenre')

SERIE_NEWS = (URL_MAIN + 'serie-tv/', 'showMovies')
SERIE_HD = (URL_MAIN + 'serie-tv/', 'showMovies')
  
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
 
def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    #oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films A-Z', 'news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films HD', 'news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films par Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries', 'series.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_MAIN + '?s='+sSearchText 
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
            
   
def showGenre():
    oGui = cGui()
 
    liste = []
    liste.append( ['Action/Aventure',URL_MAIN + 'action-aventure/'] )
    liste.append( ['Animation',URL_MAIN + 'animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'arts-martiaux/'] )
    liste.append( ['Biographie',URL_MAIN + 'biographique/'] )
    liste.append( ['Comedie',URL_MAIN + 'comedie/'] )
    liste.append( ['Drame',URL_MAIN + 'drame/'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'epouvante-horreur/'] )
    liste.append( ['Fantastique',URL_MAIN + 'fantastique/'] )  
    liste.append( ['Famille',URL_MAIN + 'famille/'] )
    liste.append( ['Guerre',URL_MAIN + 'guerre/'] )
    liste.append( ['Policier',URL_MAIN + 'policier/'] )
    liste.append( ['Romance',URL_MAIN + 'romance/'] )
    liste.append( ['Science Fiction',URL_MAIN + 'science-fiction/'] )
    liste.append( ['Thriller/Suspense',URL_MAIN + 'thrillersuspense/'] )
    liste.append( ['720p/1080p',URL_MAIN + '720p1080p/'] )
    liste.append( ['Mystère',URL_MAIN + 'mystere/'] )
    liste.append( ['Western',URL_MAIN + 'western/'] )
    liste.append( ['Animes',URL_MAIN + 'mangas/'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def showAlpha():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    dialog = cConfig().createDialog(SITE_NAME)

    for i in range(0,27) :
        cConfig().updateDialog(dialog, 27)
        if dialog.iscanceled():
            break
        
        sTitle = chr(64+i)
        sUrl = URL_MAIN + 'film-de-a-a-z/lettre-' + chr(96+i) + '/'
        
        if sTitle == '@':
            sTitle= '[0-9]'
            sUrl = URL_MAIN + 'film-de-a-a-z/0-9/'
          
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addTV(SITE_IDENTIFIER, 'showMovies','[COLOR teal] Lettre [COLOR red]'+ sTitle +'[/COLOR][/COLOR]','', '', '', oOutputParameterHandler)
        
    cConfig().finishDialog(dialog)
    
    oGui.setEndOfDirectory()
 
def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sSearch = sSearch.replace(' ','+')
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request()
    sHtmlContent = SucurieBypass().GetHtml(sUrl)
    
    xbmc.log(sUrl)
    
    oParser = cParser()
    sPattern = 'class="item"> *<a href="([^<]+)">.+?<img src="([^<>"]+?)" alt="([^"]+?)".+?<span class="calidad2">(.+?)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == False):
        oGui.addNone(SITE_IDENTIFIER)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total) #dialog
            if dialog.iscanceled():
                break
                
            sName = aEntry[2].replace(' en Streaming HD','')
            sName = sName.replace(' Streaming HD','')
            sName = sName.decode('utf8')
            sName = cUtil().unescape(sName)
            try:
                sName = sName.encode("utf-8")
            except:
                pass
            
            sTitle = sName + ' [' + aEntry[3] + ']'
            sUrl2 = aEntry[0]
            sThumbnail = aEntry[1]
            
            if sThumbnail.startswith('//'):
                sThumbnail = 'http:' + sThumbnail

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl2))
            oOutputParameterHandler.addParameter('sMovieTitle', sName)
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            if re.match('.+?saison [0-9]+',sTitle,re.IGNORECASE):
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, '', sThumbnail,'', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
            
 
        cConfig().finishDialog(dialog)
           
        if not sSearch:
            sNextPage = __checkForNextPage(sUrl)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
   
def __checkForNextPage(sUrl):
    #sPattern = 'class="current">.+?<a rel="nofollow" class="page larger" href="(.+?)">(.+?)</a>'
    if '/page/' in sUrl:
        sPattern = "\/page\/([0-9]+)\/"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            newpage = str(int(aResult[1][0]) + 1)
            return sUrl.replace('/page/' + aResult[1][0],'/page/' + newpage)
 
    return sUrl + 'page/2/'
 
def showHosters():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request() 
    sHtmlContent = SucurieBypass().GetHtml(sUrl)
    
    #Vire les bandes annonces
    sHtmlContent = sHtmlContent.replace('src="https://www.youtube.com/', '')
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    sPattern = '<iframe[^<>]+?src="(http.+?)"'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #xbmc.log(sUrl)
    #xbmc.log(str(aResult))
   
    if (aResult[0] == True):

        for aEntry in aResult[1]:
                
            sHosterUrl = str(aEntry)
            
            if '//goo.gl' in sHosterUrl:
                try:
                    class NoRedirection(urllib2.HTTPErrorProcessor):    
                        def http_response(self, request, response):
                            return response
                    
                    url8 = sHosterUrl.replace('https','http')
                    
                    opener = urllib2.build_opener(NoRedirection)
                    opener.addheaders.append (('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'))
                    opener.addheaders.append (('Connection', 'keep-alive'))
            
                    HttpReponse = opener.open(url8)
                    sHosterUrl = HttpReponse.headers['Location']

                except:
                    pass
            
            if 'official-film-illimite' in sHosterUrl:
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                sDisplayTitle = sDisplayTitle + ' [COLOR skyblue]Google[/COLOR]'
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oGui.addMisc(SITE_IDENTIFIER, 'ShowSpecialHosters', sDisplayTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
            else:
                oHoster = cHosterGui().checkHoster(sHosterUrl)
     
                if (oHoster != False):
                    sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
       
    oGui.setEndOfDirectory()
    
def serieHosters():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request()
    sHtmlContent = SucurieBypass().GetHtml(sUrl)

    sHtmlContent = sHtmlContent.replace('<iframe width="420" height="315" src="https://www.youtube.com/', '')
    sPattern = '<iframe.+?src="(http.+?)".+?>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        i = 1
        for aEntry in aResult[1]: 
        
            sUrl = str(aEntry)
            sTitle = sMovieTitle + 'episode ' + str(i)
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            i = i + 1

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addTV(SITE_IDENTIFIER, 'ShowSpecialHosters', sDisplayTitle, '', sThumbnail,'', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def ShowSpecialHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    data = sUrl.replace('http://official-film-illimite.net/Jwplayer_plugins_official-film-illimite.net/embed.php?f=','').replace('&c=','')
    pdata = 'data=' + urllib.quote_plus(data)
    
    if 'official-film-illimite' in sUrl:
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

        headers = {'User-Agent': UA ,
                   'Host' : 'official-film-illimite.net',
                   'Referer': sUrl,
                   #'Accept': '*/*',
                   'Accept-Language': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
                   
        request = urllib2.Request('http://official-film-illimite.net/Jwplayer_plugins_official-film-illimite.net/Htplugins/Loader.php',pdata,headers)
        reponse = urllib2.urlopen(request)
        sHtmlContent = reponse.read().replace('\\','')
        reponse.close()

        sPattern = '\[(.+?)\]'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            listurl = aResult[1][0].replace('"','').split(',http')
            listqual = aResult[1][1].replace('"','').split(',')
            
            tab = zip(listurl,listqual)
            
            for url,qual in tab:
                sHosterUrl = url
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    sDisplayTitle = '[' + qual + '] ' + sMovieTitle
                    sDisplayTitle = cUtil().DecoTitle(sDisplayTitle)
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()    
