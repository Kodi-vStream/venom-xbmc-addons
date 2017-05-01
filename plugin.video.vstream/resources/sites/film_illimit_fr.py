#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.sucuri import SucurieBypass
import re,urllib

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
SITE_IDENTIFIER = 'film_illimit_fr'
SITE_NAME = 'Film illimité'
SITE_DESC = 'Films, Séries HD en streaming'

URL_MAIN = 'http://official-film-illimite.net/'

MOVIE_NEWS = (URL_MAIN , 'showMovies')
MOVIE_HD = (URL_MAIN + 'films/streaming-720p-streaming-1080p/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_NEWS = (URL_MAIN + 'serie-tv/', 'showMovies')
SERIE_HD = (URL_MAIN + 'serie-tv/', 'showMovies')
  
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
 
def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (HD)', 'films_hd.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries', 'series.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_MAIN + '?s=' + sSearchText 
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()
    
    liste = []
    liste.append( ['Ultra-HD',URL_MAIN + 'ultra-hd/'] )
    liste.append( ['720p/1080p',URL_MAIN + 'films/streaming-720p-streaming-1080p/'] )
    liste.append( ['Action/Aventure',URL_MAIN + 'films/action-aventure/'] )
    liste.append( ['Animation',URL_MAIN + 'films/animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'films/arts-martiaux/'] )
    liste.append( ['Biographie',URL_MAIN + 'films/biographique/'] )
    liste.append( ['Comédie',URL_MAIN + 'films/comedie/'] )
    liste.append( ['Crime/Gangster',URL_MAIN + 'films/crimegangster/'] )
    liste.append( ['Documentaire',URL_MAIN + 'films/documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'films/drame/'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'films/epouvante-horreur/'] )
    liste.append( ['Etranger',URL_MAIN + 'films/etranger/'] )
    liste.append( ['Famille',URL_MAIN + 'films/famille/'] )
    liste.append( ['Fantastique',URL_MAIN + 'films/fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + 'films/guerre/'] )
    liste.append( ['Histoire',URL_MAIN + 'films/histoire/'] )
    liste.append( ['Musique/Danse',URL_MAIN + 'films/musiquedanse/'] )
    liste.append( ['Mystère',URL_MAIN + 'films/mystere/'] )
    liste.append( ['Policier',URL_MAIN + 'films/policier/'] )
    liste.append( ['Romance',URL_MAIN + 'films/romance/'] )
    liste.append( ['Science-fiction',URL_MAIN + 'films/science-fiction/'] )
    liste.append( ['Spectacle (FR)',URL_MAIN + 'spectacle/francais-spectacle/'] )
    liste.append( ['Spectacle (VOSTFR)',URL_MAIN + 'spectacle/vostfr-spectacle/'] )
    liste.append( ['Sport',URL_MAIN + 'films/sport/'] )
    liste.append( ['Suspense/Thriller',URL_MAIN + 'films/thrillersuspense/'] )
    liste.append( ['Téléfilm',URL_MAIN + 'films/telefilm/'] )
    liste.append( ['VOSTFR',URL_MAIN + 'films/vostfr/'] )
    liste.append( ['Western',URL_MAIN + 'films/western/'] )
    
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sSearch = sSearch.replace(' ','+')
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    sHtmlContent = SucurieBypass().GetHtml(sUrl)

    oParser = cParser()
    sPattern = 'class="item"> *<a href="([^<]+)">.+?<img src="([^<>"]+?)" alt="([^"]+?)".+?<span class="calidad2">(.+?)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

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
    if 'page' or 'films' in sUrl:
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

    sHtmlContent = SucurieBypass().GetHtml(sUrl)
    
    #Vire les bandes annonces
    sHtmlContent = sHtmlContent.replace('src="https://www.youtube.com/', '')

    sPattern = '<iframe[^<>]+?src="(http.+?)"'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
                
            sHosterUrl = str(aEntry)
            if '//goo.gl' in sHosterUrl:
                import urllib2
                try:
                    class NoRedirection(urllib2.HTTPErrorProcessor):    
                        def http_response(self, request, response):
                            return response
                    
                    url8 = sHosterUrl.replace('https','http')
                    
                    opener = urllib2.build_opener(NoRedirection)
                    opener.addheaders.append (('User-Agent', UA))
                    opener.addheaders.append (('Connection', 'keep-alive'))
            
                    HttpReponse = opener.open(url8)
                    sHosterUrl = HttpReponse.headers['Location']
                    sHosterUrl = sHosterUrl.replace('https','http')
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

    sHtmlContent = SucurieBypass().GetHtml(sUrl)

    sHtmlContent = sHtmlContent.replace('<iframe width="420" height="315" src="https://www.youtube.com/', '')
    sPattern = '<iframe.+?src="(http.+?)".+?>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    print aResult
    
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
    
    #data = sUrl.replace('http://official-film-illimite.net/Jwplayer_plugins_official-film-illimite.net/embed.php?f=','').replace('&c=','')
    data = re.sub('(.+?f=)','', sUrl)
    data = data.replace('&c=','')
    pdata = 'data=' + urllib.quote_plus(data)
    
    #exemple url
    #http://official-film-illimite.net/Jwplayer_plugins_official-film-illimite.net/QbtbycmTz7dQ8vJSvvDPzMWP9C3YLLzDrZZzccRVFTRCcmYBE3K9T4hQ6eDMpSUARd4ZJM8eYWYzh7jAjancPcrxYdWUhuFJ5cSqCqsLJADsddpAWWGkn8jGfuLRzcvy.php?f=JCrtLCbsN7OiLhPR4FZzDROzDKeGwROTNROo4fx/JfAOb08obQpKrdMRAnHKBeZGYzrYbRrve9QJDnrsAA==&c=', 

    if 'official-film-illimite' in sUrl:
        oRequest = cRequestHandler('http://official-film-illimite.net/Jwplayer_plugins_official-film-illimite.net/Htplugins/Loader.php')
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent',UA)
        oRequest.addHeaderEntry('Host','official-film-illimite.net')
        oRequest.addHeaderEntry('Referer',sUrl)
        oRequest.addHeaderEntry('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry('Content-Type','application/x-www-form-urlencoded')
        oRequest.addParametersLine(pdata)
        
        sHtmlContent = oRequest.request()
        sHtmlContent = sHtmlContent.replace('\\','')

        sPattern = '\[(.+?)\]'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            listurl = aResult[1][0].replace('"','').split(',http')
            listqual = aResult[1][1].replace('"','').split(',')
            
            tab = zip(listurl,listqual)
            
            for url,qual in tab:
                sHosterUrl = url
                if not sHosterUrl.startswith('http'):
                    sHosterUrl = 'http' + sHosterUrl

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    sDisplayTitle = '[' + qual + '] ' + sMovieTitle
                    #sDisplayTitle = sMovieTitle
                    #sDisplayTitle = cUtil().DecoTitle(sDisplayTitle)
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()    
