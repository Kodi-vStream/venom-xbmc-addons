#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'streamiz_co'
SITE_NAME = 'Streamiz'
SITE_DESC = 'Tous vos films en streaming gratuitement'

URL_MAIN = 'https://streamiz.org/'
URL_API = URL_MAIN + '/xhr/get-player/'

MOVIE_NEWS = (URL_MAIN + 'recemment-ajoute/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN, 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'les-plus-vus/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + 'xhr/search?q=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'xhr/search?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMoviesSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN + 'accueil/')

    sHtmlContent = oRequestHandler.request()
    sStart = '<h3 class="nav-title nop">Film Streaming par Genres</h3>'
    sEnd = '<h3 class="nav-title nop">Film Streaming par Années</h3>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<li class="cat-item.+?"><a href=([^>]+)><i class="icons icon-play"></i>([^<]+)<i class=count>([^<]+)</i>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1] + '(' + aEntry[2] + ')'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showYears():
    #for i in itertools.chain(xrange(5, 7), [8, 9]): afficher dans l'ordre (pense bete ne pas effacer)
    oGui = cGui()
    #compliquer pour rien.
    # from itertools import chain
    # generator = chain([1998, 1999], xrange(2000, 2019))#desordre
    # for i in reversed(list(generator)):
    for i in reversed(range(2000, 2020)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', ('%s%s%s%s') % (URL_MAIN, 'annee/', Year, '/'))
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):

    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()

    if sSearch:
        sUrl = sSearch.replace(" ", "+")
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #indispensable
    sHtmlContent = sHtmlContent.replace("\t", "")
    sHtmlContent = sHtmlContent.replace("\n", "")

    if sSearch:
        sPattern = 'post_title":[\'"]([^<>\'"]+)[\'"],"post_slug":[\'"]([^<>\'"]+)[\'"],.+?"post_poster":[\'"]([^<>\'"]+)[\'"]'
    else:
        sPattern = '<div class=movie_last> *<a href=([^ ]+).+?src=([^ ]+).+?<div class=title>([^<]+)<\/div>.+?<i class=quality>([^<]+)</i>.+?class="nop synopsis">([^<]+)</p>'

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

            if sSearch:
                sUrl = URL_MAIN + aEntry[1].replace('\/', '/')
                sThumb = aEntry[2].replace('\/', '/')
                sTitle = aEntry[0]
                sDesc = ''#aEntry[2].replace("&laquo;", '«').replace("&raquo;", '»').replace('  ', ' ')
                sDisplayTitle = sTitle
            else:
                sUrl = aEntry[0]
                sThumb = aEntry[1]
                sTitle = aEntry[2]
                sQual = aEntry[3]
                sDesc = aEntry[4].replace("&laquo;", '«').replace("&raquo;", '»').replace('  ', ' ')
                sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<li class=active>.+?<\/a><\/li><li><a.+?ref=([^>]+)>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    import json
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class=movie_player data-id=([0-9]+)'
    Fresult = oParser.parse(sHtmlContent, sPattern)

    if (Fresult[0] == True):
        sID = Fresult[1][0]
        oRequestHandler = cRequestHandler(URL_API + sID)
        sHtmlContent = oRequestHandler.request()
        if sHtmlContent:
            page = json.loads(sHtmlContent)
            page = page["data"]
            if page:
                for x in page:
                    #sTitle = x.keys()[0]
                    sHosterUrl = x.values()[0]

                    if 'playvid' in sHosterUrl:
                        sHosterUrl = GetPlayvid(sHosterUrl)

                    if 'duckload' in sHosterUrl: #pas trouvé de liens ok
                        sHosterUrl = 'https://' + sHosterUrl.split('/')[2] + '/hls/'+sHosterUrl.split('id=')[1] + '/' + sHosterUrl.split('id=')[1] + '.playlist.m3u8'

                    if 'make_mp4' in sHosterUrl:
                        sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, "GoogleVideo")
                        oOutputParameterHandler = cOutputParameterHandler()
                        oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                        oOutputParameterHandler.addParameter('sThumb', sThumb)
                        oGui.addMovie(SITE_IDENTIFIER, 'showGoogleLink', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def GetPlayvid(url):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0')
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'id="iframe" src="([^"]+)"'
    result = oParser.parse(sHtmlContent, sPattern)

    if (result[0] == True):
        return result[1][0]

    else:
        sPattern = "<source src='([^']+)' *type="
        result = oParser.parse(sHtmlContent, sPattern)
        if (result[0] == True):
            return result[1][0]
            
def showGoogleLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler('https://playvid.org' + sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0')
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<source src="([^"]+)".+?size="([^"]+)"'
    result = oParser.parse(sHtmlContent, sPattern)

    if (result[0] == True):
        for aEntry in result[1]:
            sHosterUrl = aEntry[0]
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle + ' ' + aEntry[1])
                oHoster.setFileName(sMovieTitle + ' ' + aEntry[1])
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                
    oGui.setEndOfDirectory()
