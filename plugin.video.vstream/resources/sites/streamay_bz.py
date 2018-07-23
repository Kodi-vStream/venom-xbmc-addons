#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, dialog
import base64,re



SITE_IDENTIFIER = 'streamay_bz'
SITE_NAME = 'Streamay'
SITE_DESC = 'Films, Séries & Mangas en streaming'
URL_MAIN = 'http://streaming.streamay.com/'

MOVIE_NEWS = (URL_MAIN , 'showMovies')
MOVIE_MOVIE = (URL_MAIN, 'AlphaSearch')
MOVIE_GENRES = (URL_MAIN + 'films', 'showGenres')


URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showResultSearch'

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
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films (Liste) ', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return
        
def AlphaSearch():
    oGui = cGui()

    for i in range(0, 27) :

        if (i < 1):
            sLetter = '0-9'
            sUrl = URL_MAIN + 'letters/0-9/'
        else:
            sLetter = chr(64 + i)
            sUrl = URL_MAIN + 'letters/' + sLetter
            
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovieslist', 'Lettre [COLOR coral]' + sLetter + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    oParser = cParser()

    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(sHtmlContent, '<a target="_blank">Genres</a>', 'id="menu-item-20645"')

    sPattern = '<a href="([^"]+)">(.+?)<\/a><\/li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies2', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def showMovieslist():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<span class="Num">.+?<a href="([^"]+)".+?<img src="(.+?)".+?<strong>(.+?)<\/strong>.+?<td>(.+?)<\/td>.+?<span class="Qlty">(.+?)<\/span>'


    oParser = cParser()
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

            sQual = aEntry[4]
            sThumb = aEntry[1].replace('w92','w300')
            if not sThumb.startswith('http'):
               sThumb = 'http:' + sThumb
               
            sTitle = aEntry[2]
            sYear = aEntry[3]
            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sYear)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovieslist', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

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

    sHtmlContent = oParser.abParse(sHtmlContent, 'MovieList Rows', '</html>')


    sPattern = '<div class="Image">.+?<img src="([^"]+)".+?<a href="([^"]+)"><div class="Title">(.+?)</div></a>.+?<p>(.+?)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[2]
            sUrl = aEntry[1]
            sThumb = aEntry[0]
            if not sThumb.startswith('http'):
               sThumb = 'http:' + sThumb
               
            sDesc = aEntry[3]


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)
            
    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'href="([^"]+)">Next.+?<\/a><\/div>'
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
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    

    sPattern = 'data-VidOpt="VideoOption\d+".+?<p class="AAIco-language">(.+?)<\/p>.+?<p class="AAIco-equalizer">(.+?)</p>' #lang,qual,host
    aResult1 = re.findall(sPattern, sHtmlContent,re.DOTALL)
    
    sHtmlContent = oParser.abParse(sHtmlContent, '<div class="VideoPlayer">', '<div class="Image">')

    sPattern2 = '<div id="VideoOption\d+" class="Vid.+?">(.+?)</div>'
    aResult2 = re.findall(sPattern2, sHtmlContent,re.DOTALL)
    
    aResult = zip(aResult2,[x[0] + ' ' + x[1] for x in aResult1])

    if (aResult):
        for aEntry in aResult:
            sHtmlContent = base64.b64decode(aEntry[0])
            
            sUrl = re.search('src="([^"]+)"',sHtmlContent)
            if sUrl:
                sHosterUrl = sUrl.group(1)
                
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle + ' ['+ aEntry[1]+ ']')
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


