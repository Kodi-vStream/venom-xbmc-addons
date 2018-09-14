#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, addon
#revoir genre pour serie
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
sColor = addon().getSetting("deco_color")

SITE_IDENTIFIER = 'streamingdivx'
SITE_NAME = 'Streamingdivx'
SITE_DESC = 'Films VF en streaming.'

URL_MAIN = 'https://www.streamingdivx.co/'

MOVIE_NEWS = (URL_MAIN + 'films.html', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'series.html', 'showMovies')

MOVIE_GENRES = ('http://venom', 'showGenres')

URL_SEARCH = (URL_MAIN + '/recherche?q=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/recherche?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)


    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []

    liste.append( ['Action', URL_MAIN + 'films/action/'] )
    liste.append( ['Animation', URL_MAIN + 'films/animation/'] )
    liste.append( ['Aventure', URL_MAIN + 'films/aventure/'] )
    liste.append( ['Biopic', URL_MAIN + 'films/biopic/'] )
    liste.append( ['Comédie', URL_MAIN + 'films/comedie/'] )
    liste.append( ['Comédie-dramatique', URL_MAIN + 'films/comedie-dramatique/'] )
    liste.append( ['Comédie-musicale', URL_MAIN + 'films/comedie-musicale/'] )
    liste.append( ['Documentaire', URL_MAIN + 'films/documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'films/drame/'] )
    liste.append( ['Divers', URL_MAIN + 'films/divers/'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'films/epouvante-horreur/'] )
    liste.append( ['Famille', URL_MAIN + 'films/famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'films/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'films/guerre/'] )
    liste.append( ['Opera', URL_MAIN + 'films/opera/'] )
    liste.append( ['Policier', URL_MAIN + 'films/policier/'] )
    liste.append( ['Romance', URL_MAIN + 'films/romance/'] )
    liste.append( ['Science-fiction', URL_MAIN + 'films/science-fiction/'] )
    liste.append( ['Thriller', URL_MAIN + 'films/thriller/'] )

    for sTitle, sUrl in liste:

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
        
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="short-images.+?<a href="([^"]+)" title="([^"]+)" class=.+?<img src="([^"]+)".+?(?:<div class="short-content">|<a href=.+?qualite.+?>(.+?)</a>.+?<a href=.+?langue.+?>(.+?)<\/a>)'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
                
            sUrl = aEntry[0]
            if sUrl.startswith('/'):
                sUrl = URL_MAIN[:-1] + sUrl
                
            sTitle = aEntry[1].replace('Streaming','').replace('streaming','').replace('série','')
            
            sThumb = aEntry[2]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            sQual = ''
            if aEntry[3]:
                sQual = aEntry[3]

            sLang = ''
            if aEntry[4]:
                sLang = aEntry[4]
                
            sDisplayTitle = ('%s (%s) [COLOR %s]%s[/COLOR]') % (sTitle, sLang, sColor, sQual)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            if 'series/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            
        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'pages-next"><a href="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        if aResult[1][0].startswith('/'):
            return URL_MAIN[:-1] + aResult[1][0]
        else:
            return aResult[1][0]

    return False
    
def showSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #syno
    sDesc = ''
    try:
        sPattern = '<div class="f*synopsis"><p>(.+?)</p></div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass
        
    sPattern = '<div class="short-images.+?<a href="([^"]+)" class="short-images.+?<img src="([^"]+)" alt="([^"]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            if sUrl.startswith('/'):
                sUrl = URL_MAIN[:-1] + sUrl
            
            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
                
            sTitle = aEntry[2].replace('Streaming','').replace('streaming','').replace('série','')
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showEp', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def showEp():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(sHtmlContent, '<h2 class="serie-middle"', 'Series similaires')

    sPattern = '<div class="sai.+?<a href="([^"]+)".+?<span>(.+?)<\/span>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            if sUrl.startswith('/'):
                sUrl = URL_MAIN[:-1] + sUrl

            sTitle = aEntry[1]
            
            sDisplayTitle = ('%s %s') % (sMovieTitle, sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def showLinks():
    #streamer.php?p=169&c=V1RJeGMxcHVSbmhhUnpGMFltNU9kMWxYVW5sWlVUMDk=
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    #syno
    sDesc = ''
    try:
        sPattern = '<div class="f*synopsis"><p>(.+?)</p></div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    sPattern2 = '<li class="stream.+?"><div data-num="([^"]+)" data-code="([^"]+)".+?<i class="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern2)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHost = aEntry[2].replace('server player-','').capitalize()

            sDisplayTitle = ('%s [COLOR %s]%s[/COLOR]') % (sMovieTitle, sColor, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('datanum', aEntry[0])
            oOutputParameterHandler.addParameter('datacode', aEntry[1])
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    datanum = oInputParameterHandler.getValue('datanum')
    datacode = oInputParameterHandler.getValue('datacode')
    
    import urllib2
    
    sUrl = ('%s%s%s%s%s' % (URL_MAIN,'streamer.php?p=', datanum, '&c=', datacode))
    
    class NoRedirection(urllib2.HTTPErrorProcessor):
            def http_response(self, request, response):
                return response
                
            https_response = http_response
            
    opener = urllib2.build_opener(NoRedirection)
    opener.addheaders = [('User-agent', UA)]
    opener.addheaders = [('Referer', URL_MAIN)]
    response = opener.open(sUrl)

    if response.code == 302:
        redirection_target = response.headers['Location']
        if redirection_target:

            sHosterUrl = redirection_target
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

                oGui.setEndOfDirectory()
                
    response.close()
