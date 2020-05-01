# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
import base64
import re

from resources.lib.comaddon import progress  # , VSlog
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil, Unquote

SITE_IDENTIFIER = 'filmstreaming'
SITE_NAME = 'Film Streaming'
SITE_DESC = 'Films en streaming'
URL_MAIN = 'https://www.filmstreamingvf.watch/'

MOVIE_MOVIE = ('http://', 'load')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_VIEWS = (URL_MAIN + '?v_sortby=views&v_orderby=desc', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_LIST = (URL_MAIN, 'AlphaSearch')

# la recherche global ne fonctionne pas
FUNCTION_SEARCH = 'showSearchMovies'
URL_SEARCH = ('', 'showSearchMovies')
URL_SEARCH_MOVIES = ('', 'showSearchMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

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
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Ordre alphabétique)', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showSearchMovies(sSearchText)
        oGui.setEndOfDirectory()
        return


def showSearchMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:

        sSearch = Unquote(sSearch)
        sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'
        pdata = 'nonce=3293a1b68c&action=tr_livearch&trsearch=' + sSearch #la valeur nonce change

        oRequest = cRequestHandler(sUrl2)
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0")
        oRequest.addParameters('Referer', URL_MAIN)
        oRequest.addParametersLine(pdata)

        sHtmlContent = oRequest.request()
        sPattern = '<div class="TPost B">.+?<a href="([^"]+)">.+?<img src="([^"]+)".+?<div class="Title">([^<]+)</div>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break

                sUrl = aEntry[0]
                sThumb = re.sub('/w\d+', '/w342', aEntry[1], 1)
                if sThumb.startswith('/'):
                    sThumb = 'https:' + sThumb
                sTitle = aEntry[2]

                #tris search
                if sSearch and total > 3:
                    if cUtil().CheckOccurence(sSearch, sTitle) == 0:
                        continue

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

            progress_.VSclose(progress_)


def AlphaSearch():
    oGui = cGui()

    for i in range(0, 27):

        if (i < 1):
            sLetter = '0-9'
            sUrl = URL_MAIN + 'letters/0-9/'
        else:
            sLetter = chr(64 + i)
            sUrl = URL_MAIN + 'letters/' + sLetter + '/'

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovieslist', 'Lettre [COLOR coral]' + sLetter + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(MOVIE_NEWS[0])
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(sHtmlContent, '<div class=Title>Film Streaming Par Genres</div>', '</div></aside>')

    sPattern = '<li class="cat-item cat-item-.+?"><a href=([^>]+)>([^<]+)</a>([^<]+)</li>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1] + aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieslist():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<span class=Num>.+?href=(.+?) class=MvTbImg> <img src=(.+?) alt=.+?<strong>([^<]+)</strong> </a></td><td>([^<]+)<.+?class=Qlty>([^<]+)<'
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
            sThumb = re.sub('/w\d+', '/w342', aEntry[1], 1)
            if sThumb.startswith('/'):
                sThumb = 'http:' + sThumb
            sTitle = aEntry[2]
            sYear = aEntry[3]
            sQual = aEntry[4]

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
            oGui.addNext(SITE_IDENTIFIER, 'showMovieslist', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(sHtmlContent, 'MovieList Rows', '</body></html>')
    sPattern = '<div class=Image>.+?src=([^ ]+) .+?<span class=Qlty>.+?<a href=([^>]+)><div class=Title>([^<]+)</div></a>.+?<div class=Description><p>(.+?)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = re.sub('/w\d+', '/w342', aEntry[0], 1)
            if sThumb.startswith('/'):
                sThumb = 'https:' + sThumb

            sUrl = aEntry[1]
            sTitle = aEntry[2]
            sDesc = aEntry[3]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'href="*([^">]+)"*>Next'
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

    sPattern = '<p class=AAIco-language>([^<]+)</p><p class=AAIco-dns>.+?<p class=AAIco-equalizer>([^<]+)</p>'  # qual, lang
    aResult1 = re.findall(sPattern, sHtmlContent, re.DOTALL)
    # VSlog(str(aResult1)) #Commenter ou supprimer cette ligne une fois fini

    sPattern2 = '<div id=VideoOption\d+ class="*Vid.+?>([^<]+)</div>'
    aResult2 = re.findall(sPattern2, sHtmlContent, re.DOTALL)
    # VSlog(str(aResult2)) #Commenter ou supprimer cette ligne une fois fini

    aResult = zip(aResult2, [x[1] + '] (' + x[0] for x in aResult1])
    # VSlog(str(aResult)) #Commenter ou supprimer cette ligne une fois fini

    if (aResult):
        for aEntry in aResult:
            sHtmlContent = base64.b64decode(aEntry[0])
            # VSlog(sHtmlContent)

            sHosterUrl = ''
            sUrl = re.search('src="([^"]+)"', sHtmlContent)
            sHosterUrl = sUrl.group(1)

            oRequestHandler = cRequestHandler(sHosterUrl)
            sHtmlContent = oRequestHandler.request()
            sUrl = re.search('<iframe id="iframe" src="([^"]+)"', sHtmlContent)
            if sUrl:
                sHosterUrl = sUrl.group(1)

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle + ' [' + aEntry[1] + ')')
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
