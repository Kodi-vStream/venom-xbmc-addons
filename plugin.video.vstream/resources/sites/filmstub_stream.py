#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, dialog
import re

SITE_IDENTIFIER = 'filmstub_stream'
SITE_NAME = 'Filmstub'
SITE_DESC = 'Films, Séries & Mangas en streaming'
URL_MAIN = 'https://www.filmstub.stream/'

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN + 'films-streaming/', 'showMovies')
MOVIE_GENRES = ('http://film', 'showGenres')

SERIE_NEWS = (URL_MAIN + 'series-streaming/', 'showMovies')
SERIE_GENRES = ('http://serie', 'showSerieGenres')

ANIM_NEWS = (URL_MAIN + 'anime-streaming/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
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
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animes (Derniers ajouts)', 'news.png', oOutputParameterHandler)
    
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
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    if 'serie' in sUrl:
        sType = '?tr_post_type=2'
    else:
        sType = '?tr_post_type=1'
        
    liste = []
    liste.append( ['Action', URL_MAIN + 'category/action/' + sType] )
    liste.append( ['Action & Adventure', URL_MAIN + 'category/action-adventure/' + sType] )
    liste.append( ['Animation', URL_MAIN + 'category/animation/' + sType] )
    liste.append( ['Aventure', URL_MAIN + 'category/aventure/' + sType] )
    liste.append( ['BoxOffice', URL_MAIN + 'category/boxoffice/' + sType] )
    liste.append( ['Comédie', URL_MAIN + 'category/comedie/' + sType] )
    liste.append( ['Comedy', URL_MAIN + 'category/comedy/' + sType] )
    liste.append( ['Crime', URL_MAIN + 'category/crime/' + sType] )
    liste.append( ['Documentaire', URL_MAIN + 'category/documentaire/' + sType] )
    liste.append( ['Drama', URL_MAIN + 'category/drama/' + sType] )
    liste.append( ['Drame', URL_MAIN + 'category/drame/' + sType] )
    liste.append( ['Erotique', URL_MAIN + 'category/erotic/' + sType] )
    liste.append( ['Etranger', URL_MAIN + 'category/etranger/' + sType] )
    liste.append( ['Familial', URL_MAIN + 'category/familial/' + sType] )
    liste.append( ['Fantastique', URL_MAIN + 'category/fantastique/' + sType] )
    liste.append( ['Fantasy', URL_MAIN + 'category/fantasy/' + sType] )
    liste.append( ['Guerre', URL_MAIN + 'category/guerre/' + sType] )
    liste.append( ['Histoire', URL_MAIN + 'category/histoire/' + sType] )
    liste.append( ['Horreur', URL_MAIN + 'category/horreur/' + sType] )
    liste.append( ['Kids', URL_MAIN + 'category/kids/' + sType] )
    liste.append( ['Musique', URL_MAIN + 'category/musique/' + sType] )
    liste.append( ['Music', URL_MAIN + 'category/music/' + sType] )
    liste.append( ['Mystère', URL_MAIN + 'category/mystere/' + sType] )
    liste.append( ['Mystery', URL_MAIN + 'category/mystery/' + sType] )
    liste.append( ['News', URL_MAIN + 'category/news/' + sType] )
    liste.append( ['Reality', URL_MAIN + 'category/reality/' + sType] )
    liste.append( ['Romance', URL_MAIN + 'category/romance/' + sType] )
    liste.append( ['Sci-Fi & Fantasy', URL_MAIN + 'category/sci-fi-fantasy/' + sType] )
    liste.append( ['Science Fiction', URL_MAIN + 'category/science-fiction/' + sType] )
    liste.append( ['Science Fiction & Fantastique', URL_MAIN + 'category/science-fiction-fantastique/' + sType] )
    liste.append( ['Soap', URL_MAIN + 'category/soap/' + sType] )
    liste.append( ['Téléfilm', URL_MAIN + 'category/telefilm/' + sType] )
    liste.append( ['Thriller', URL_MAIN + 'category/thriller/' + sType] )
    liste.append( ['War & Politics', URL_MAIN + 'category/war-politics/' + sType] )
    liste.append( ['Western', URL_MAIN + 'category/western/' + sType] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()


    sPattern = 'class="TPost C"> *<a href="([^"]+)">.+?<img src="([^"]+)".+?class="Title">(.+?)<.+?<span class="Year">(.+?)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sTitle = aEntry[2]
            sThumb = aEntry[1]
            sYear = aEntry[3]

            sDisplayTitle = ('%s (%s)') % (sTitle, sYear)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
 
        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory() #arriver la

def __checkForNextPage(sHtmlContent):
    sPattern = 'href="*([^">]+)"*>Next'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
    
def showEpisode():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    
    sDesc = ''
    try:
        sPattern = '<div class="Description"><p>([^<]+)<\/p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass
    
    sPattern = '<div class="Title AA-Season.+?tab=".+?">([^<]+)<span>(\d+)</span>|<li class="[0-9a-zA-Z]+"> *<a href="([^"]+)">([^<]+)<\/a><\/li>'


    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if (aEntry[0] and aEntry[1]):
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + ' ' + aEntry[1] + '[/COLOR]')

            else:
                sUrl = aEntry[2]
                sTitle = sMovieTitle + ' ' + aEntry[3]
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()
    
def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #resume
    sDesc = ''
    try:
        sPattern = '<div class="Description"><p>([^<]+)<\/p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:

            sDesc = aResult[1][0]
    except:
        pass

    sHtmlContent = oParser.abParse(sHtmlContent, 'TPost Sing', '<span class="btnsplyr">') #film serie

    sHtmlContent = sHtmlContent.replace('&quot;','"').replace('#038;','').replace('&amp;','&')
    
    sHtmlContent = re.sub('<img class="imgfav" *src="https://www.google.com/s2/favicons\?domain=.+?">','',sHtmlContent)#film

    #1
    sPattern = 'data-tplayernv=".+?"><span>([^<]+)<\/span><span>([^<]+)<\/span>'
    aResult1 = re.findall(sPattern, sHtmlContent)

    #2
    sPattern1 = 'src="(https:\/\/www.filmstub.+?)"'
    aResult2 = re.findall(sPattern1, sHtmlContent)

    aResult = []
    aResult = zip(aResult2, [x[1] + ' ' + x[0] for x in aResult1])
    if (aResult):
        for aEntry in aResult:
            sUrl = aEntry[0]
            
            sHost = aEntry[1]
  
            sTitle = '%s (%s)' % (sMovieTitle, sHost)
 
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()

    sPattern = '<iframe.+?src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        oRequestHandler = cRequestHandler(aResult[1][0])
        sHtmlContent = oRequestHandler.request()

        sPattern = 'defer.+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            oRequestHandler = cRequestHandler(aResult[1][0])
            sHtmlContent = oRequestHandler.request()
            
            sPattern = "id=trde\('([^']+)'\)"
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sUrl = 'https://www.filmstub.stream/?trhide=1&trhex=' + decoded(aResult[1][0])


                oRequest = cRequestHandler(sUrl)
                sHtmlContent = oRequest.request()

                sHosterUrl = oRequest.getRealUrl()

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
    
def decoded(trde):
    #a = '13839373636353939373735313f2465626d656f656469667f25727e2b6f6f2f2a33707474786'
    b = int(len(trde) - 1)
    start = ''
    while (b >= 0):
        start += trde[b]
        b -= 1
        
    return start
