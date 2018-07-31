#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'sokrostream_biz'
SITE_NAME = 'Sokrostream'
SITE_DESC = 'Films & Séries en streaming en vf et Vostfr'

URL_MAIN = 'http://filmstreamin.co/'

MOVIE_NEWS = (URL_MAIN + 'film-streaming/', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')

SERIE_NEWS = (URL_MAIN + 'serie/', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'serie/', 'showGenres')

ANIMES_NEWS = (URL_MAIN + 'mangas/', 'showMovies')
ANIMES_GENRES = (URL_MAIN + 'mangas/', 'showGenres')

URL_SEARCH = (URL_MAIN + '/?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '/?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'serie/?s=', 'showMovies')
URL_SEARCH_ANIMS = (URL_MAIN + 'mangas/?s=', 'showMovies')

FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Films)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Séries)', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche (Animes)', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIMES_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Animes (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIMES_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Animes (Genres)', 'genres.png', oOutputParameterHandler)
    
    
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sUrl + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append( ['Action', sUrl + 'category/action'] )
    liste.append( ['Animation', sUrl + 'category/animation'] )
    liste.append( ['Aventure', sUrl + 'category/aventure'] )
    liste.append( ['Comédie', sUrl + 'category/comedie'] )
    liste.append( ['Comédie Dramatique', sUrl + 'category/comedie-dramatique'] )
    liste.append( ['Documentaire', sUrl + 'category/documentaire'] )
    liste.append( ['Drame', sUrl + 'category/drame'] )
    liste.append( ['Emissions tv', sUrl + 'category/emissions-tv'] )
    liste.append( ['Epouvante Horreur', sUrl + 'category/epouvante-horreur'] )
    liste.append( ['Erotique', sUrl + 'category/erotique'] )
    liste.append( ['Espionnage', sUrl + 'category/espionnage'] )
    liste.append( ['Famille', sUrl + 'category/famille'] )
    liste.append( ['Fantastique', sUrl + 'category/fantastique'] )
    liste.append( ['Guerre', sUrl + 'category/guerre'] )
    liste.append( ['Histoire', sUrl + 'category/histoire'] )
    liste.append( ['Judiciaire', sUrl + 'category/judiciaire'] )
    liste.append( ['Médical', sUrl + 'category/medical'] )
    liste.append( ['Musical', sUrl + 'category/musical'] )
    liste.append( ['Peplum', sUrl + 'category/peplum'] )
    liste.append( ['Policier', sUrl + 'category/policier'] )
    liste.append( ['Romance', sUrl + 'category/romance'] )
    liste.append( ['Science-Fiction', sUrl + 'category/science-fiction'] )
    liste.append( ['Thriller', sUrl + 'category/thriller'] )
    liste.append( ['Western', sUrl + 'category/western'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()

    if sSearch:
        sUrl = sSearch
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a title="([^"]+)" href="([^"]+)">.+?<img src="([^"]+)".+?<div class="ExcerptContent">(.+?)<\/div>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)

            sTitle = aEntry[0].replace('streaming','')   
            sUrl = aEntry[1]
            sThumb = aEntry[2]
            sSyn = aEntry[3]
            

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sSyn', sSyn)
            
            if ('/serie' in sUrl):
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, sSyn, oOutputParameterHandler)
            elif ('/mangas' in sUrl):
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, sSyn, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sSyn, oOutputParameterHandler)
    
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
    sPattern = '<a class="nextpostslink" rel="next" href="([^"]+)">.+?<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sSyn = oInputParameterHandler.getValue('sSyn')
    
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="season">.+?<h3>([^<]+)<\/h3>|href="([^"]+)"><span>([^<]+)<\/span><\/a>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')

            else:
                sUrl = aEntry[1]
                sTitle = aEntry[2].replace('streaming','')
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sSyn', sSyn)
                oGui.addTV(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sSyn, oOutputParameterHandler)
                

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sSyn = oInputParameterHandler.getValue('sSyn')
    
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    try:

        sQual = ''
        sLang = ''
        sPattern = '<a href="h.+?quality/.+?">(.+?)<\/a>.+?<a href="h.+?langue/.+?">(.+?)<\/a>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sQual = aResult[1][0][0]
            sLang = aResult[1][0][1]
        else:
            #serie et anime lang
            sPattern = '<span>(?:(vf|vostfr|vo))<\/span>'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                sLang = aResult[1][0]

    except:
       pass
       
    sPattern = '<form action.+?<i class="fa fa-play"><\/i>(.+?)<\/a>.+?<input name="levideo" value="([^"]+)" type="hidden">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
                
            sHost = aEntry[0].replace(' ','')
            
            acut = sHost.rfind('.')
            if acut >= 0:
                sHost = sHost[:acut]
                
            sHost = sHost.capitalize()
            sCode = aEntry[1]
            
            if sQual and sLang:
                sTitle = "%s [%s %s %s]" % (sMovieTitle, sHost, sQual, sLang)
            elif sLang:
                sTitle = "%s [%s %s]" % (sMovieTitle, sHost, sLang)
            else:
                sTitle = "%s [%s]" % (sMovieTitle, sHost)
                
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sCode', sCode)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sCode = oInputParameterHandler.getValue('sCode')

    oParser = cParser()

    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', sUrl)
    oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequest.addParametersLine('levideo=' + sCode)

    sHtmlContent = oRequest.request()

    sPattern = '<iframe.+?src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        sHosterUrl = aResult[1][0]
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
