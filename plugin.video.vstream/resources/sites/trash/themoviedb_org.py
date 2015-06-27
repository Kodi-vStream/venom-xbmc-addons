#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.favourite import cFav
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import urllib

try:    import json
except: import simplejson as json

SITE_IDENTIFIER = 'themoviedb_org'
SITE_NAME = 'TheMovieDB (beta)'
SITE_DESC = 'Base de données video.'

#doc de l'api http://docs.themoviedb.apiary.io/

URL_MAIN = 'https://api.themoviedb.org/'

API_KEY = '92ab39516970ab9d86396866456ec9b6'
API_VERS = '3'
API_URL = URL_MAIN+API_VERS

POSTER_URL = 'https://image.tmdb.org/t/p/w396/'
FANART_URL = 'https://image.tmdb.org/t/p/w1280/'


#https://api.themoviedb.org/3/movie/popular?api_key=92ab39516970ab9d86396866456ec9b6


def load():
    oGui = cGui()
    
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    # oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', API_URL+'/movie/popular')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Populaires', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', API_URL+'/movie/now_playing')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films en salle', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', API_URL+'/movie/top_rated')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films les mieux notés', 'films.png', oOutputParameterHandler)
   
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', API_URL+'/genre/movie/list')
    # oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', API_URL+'/tv/popular')
    # oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Séries Populaires', 'films.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', API_URL+'/tv/on_the_air')
    # oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Séries a la tv', 'films.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', API_URL+'/tv/top_rated')
    # oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Séries les mieux notés', 'films.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', API_URL+'/genre/tv/list')
    # oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Séries Genres', 'genres.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

    
def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://www.fullmoviz.org/?s='+sSearchText
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
    
 
def showGenre():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addParameters('api_key', API_KEY)
    oRequestHandler.addParameters('language', 'fr')
    
    sHtmlContent = oRequestHandler.request(); 
    result = json.loads(sHtmlContent)       

 
    total = len(sHtmlContent)
    if (total > 0):
        for i in result['genres']:
            sId, sTitle = i['id'], i['name']

            sTitle = sTitle.encode("utf-8")

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'none')
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', str(sTitle), 'genres.png', oOutputParameterHandler)
           
    oGui.setEndOfDirectory()
    

def showMovies():
    oGui = cGui()
 
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    iPage = 1
    if (oInputParameterHandler.exist('page')):
        iPage = oInputParameterHandler.getValue('page')
   
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addParameters('api_key', API_KEY)
    oRequestHandler.addParameters('language', 'fr')
    oRequestHandler.addParameters('page', iPage)

    sHtmlContent = oRequestHandler.request();
    result = json.loads(sHtmlContent)
    
    total = len(sHtmlContent)

    if (total > 0):
        for i in result['results']:
            sId, sTitle, sOtitle, sThumbnail, sFanart = i['id'], i['title'], i['original_title'], i['poster_path'], i['backdrop_path']
            #sTitle = aEntry[2].decode('latin-1').encode("utf-8")
            #sThumbnail = 'http:'+str(aEntry[2])
            #sUrl = URL_MAIN+str(aEntry[1])
            #print ['results']['title']
            if sThumbnail:
                sThumbnail = POSTER_URL+sThumbnail
            else: sThumbnail = ''

            sTitle = sTitle.encode("utf-8")

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str('none'))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)
            
        if (iPage > 0):
            iNextPage = int(iPage) + 1
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('page', iNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page '+str(iNextPage)+' >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeries(sSearch=''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    iPage = 1
    if (oInputParameterHandler.exist('page')):
        iPage = oInputParameterHandler.getValue('page')
   
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addParameters('api_key', API_KEY)
    oRequestHandler.addParameters('language', 'fr')
    sHtmlContent = oRequestHandler.request();
    result = json.loads(sHtmlContent)
    
    total = len(sHtmlContent)
    sPattern = '<div class="loop-thumb"><a href="([^<]+)"><img width=".+?" height=".+?" src="([^<]+)" class="attachment-loop wp-post-image" alt="(.+?)" /></a>'
    #oParser = cParser()
    #aResult = oParser.parse(sHtmlContent, sPattern)
    if (total > 0):
        for i in result['results']:
            sId, sTitle, sThumbnail, sFanart = i['id'], i['name'], i['poster_path'], i['backdrop_path']
            #sTitle = aEntry[2].decode('latin-1').encode("utf-8")
            #sThumbnail = 'http:'+str(aEntry[2])
            #sUrl = URL_MAIN+str(aEntry[1])
            #print ['results']['title']
            if sThumbnail:
                sThumbnail = POSTER_URL+sThumbnail
            else: sThumbnail = ''
            sTitle = sTitle.encode("utf-8")

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str('none'))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)
            
        if (iPage > 0):
            iNextPage = int(iPage) + 1
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('page', iNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Page '+str(iNextPage)+' >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = "<span class='page-numbers current'>.+?</span><a class='page-numbers' href='([^<]+)'>.+?</a>"
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

    liste = []
    liste.append( ["frenchstream_org", "http://frenchstream.org/?s=", urllib.quote(sMovieTitle)] )
    #liste.append( ["full_streaming_org", "showMovies", "http://full-streaming.org/xfsearch/"+sMovieTitle] )
    #liste.append( ["adkami_com", "showMovies", "http://www.adkami.com/video?recherche="] )
    liste.append( ["dpstreaming_org", "http://dpstreaming.org/?s=", urllib.quote(sMovieTitle)] )
    #liste.append( ["fifostream_me", "showMovies", "http://www.fifostream.me/?s="] )
    #liste.append( ["filmstreamingz_fr", "showMovies", "http://filmstreamingz.fr/?s="] )
    #liste.append( ["filmstreamingz_fr", "showMovies", "http://seriestreaming.org/?s="] )
    #liste.append( ["full_stream_net", "showMovies", "http://full-stream.net/xfsearch/"] )
    #liste.append( ["fullmoviz_org", "showMovies", "http://www.fullmoviz.org/?s="] )
    #liste.append( ["streamzer_net", "resultSearch", "http://www.streamzer.net/index.php?file=Search&op=mod_search&main="] )
    #liste.append( ["vos_animes_com", "showMovies", "http://www.vos-animes.com/xfsearch/"] )
    try:
        sources = __callsearch(liste)
        print sources
        try:
            links = __calllink(sources)
            try:
                hosts = __callhost(links)
            except: return
        except: return
    except: pass
    
    if hosts:
        for i in range(len(hosts)):

            sHosterUrl = str(hosts[i]['url'])
            sSourceUrl = str(hosts[i]['source'])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle+' - [COLOR azure]'+sSourceUrl+'[/COLOR]')
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 

        oGui.setEndOfDirectory()
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', '')  
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Aucune source[/COLOR]', 'next.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()

    
def __callsearch(liste):
    sources = []
    for sSiteName, sUrl, sTitle in liste:
        try:

            exec "import "+sSiteName+" as search"
            searchUrl = "search.getSource('%s', '%s')" % (sUrl, sTitle)
            exec("sources += %s") % (searchUrl)
            
        except:       
            pass
    return sources

def __calllink(sources):
    links = []
    for i in range(len(sources)):
        try:
            exec "import "+sources[i]['source']+" as link"
            linkUrl = "link.getLink('%s')" % (sources[i]['url'])
            exec("links += %s") % (linkUrl)
        except:       
            pass
    return links

def __callhost(links):
    hosts = []
    for i in links:
        try:       
            exec "import "+i['source']+" as host"
            hostUrl = "host.getHost('%s')" % (i['url'])
            exec("hosts += %s") % (hostUrl)
        except:       
            pass
    return hosts