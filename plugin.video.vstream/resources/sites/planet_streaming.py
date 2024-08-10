# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'planet_streaming'
SITE_NAME = 'Planet Streaming'
SITE_DESC = 'Films en Streaming complet VF HD'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_TOP = (URL_MAIN + 'exclu/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'xfsearch/hd/', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')

URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP[1], 'Films (Populaires)', 'views.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (HD)', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        showMovies(sSearchText)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animation', 'animation'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie Musicale', 'musical'],
             ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Epouvante Horreur', 'epouvante-horreur'],
             ['Espionnage', 'espionnage'], ['Famille', 'famille'], ['Fantastique', 'fantastique'],
             ['Guerre', 'guerre'], ['Historique', 'historique'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science Fiction', 'science-fiction'],
             ['Thriller', 'thriller'], ['Western', 'western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'xfsearch/' + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    nextPageSearch = oInputParameterHandler.getValue('nextPageSearch')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if nextPageSearch:
        sSearch = sUrl

    if sSearch:
        if URL_SEARCH[0] in sSearch:
            sSearch = sSearch.replace(URL_SEARCH[0], '')

        oUtil = cUtil()
        sSearchText = oUtil.CleanName(sSearch)

        if nextPageSearch:
#            query_args = (('do', 'search'), ('subaction', 'search'), ('search_start', nextPageSearch), ('story', sSearch))
            query_args = '?do=search&subaction=search&search_start=%s&speedsearch=1&story=' % nextPageSearch
        else:
            # query_args = (('do', 'search'), ('subaction', 'search'), ('story', sSearch))
            query_args = '?do=search&subaction=search&speedsearch=1&story='

        oRequestHandler = cRequestHandler(URL_MAIN + query_args + sSearch)#URL_SEARCH[0])
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParameters('User-Agent', UA)
        oRequestHandler.addParameters('Content-Type', 'application/x-www-form-urlencoded')
#        data = urlEncode(query_args)
#        oRequestHandler.addParametersLine(data)
#        oRequestHandler.addParameters('Referer', URL_MAIN)
#        oRequestHandler.addParameters('Cookie', 'PHPSESSID=95n37c5jvq0ov35i3ugeo542d7; _ga=GA1.1.800104158.1713656815; _ga_LVMLC0MKH6=GS1.1.1713716057.2.1.1713716875.0.0.0')
        sHtmlContent = oRequestHandler.request()
        sPattern = '"mov-title"><a href="([^"]+)" >([^<]+)<.+?color="#00FF00"> (<strong>Date de sortie :  | )([^<]+).+?img src="([^"]+)"'
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'class="fullstream fullstreaming.+?src="([^"]+).+?alt="([^"]+).+?<strong>([^<]+).+?color="#00FF00"> (<strong>Date de sortie :  | )([^<]+).+?itemprop="description.+?;">([^<]+).+?<a href="([^"]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sYear = ''
            if sSearch:

                sTitle = aEntry[1]
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue  # Filtre de recherche

                sThumb = aEntry[4]
                if sThumb.startswith('/'):
                    sThumb = URL_MAIN[:-1] + sThumb

                siteUrl = re.sub('www\.', '', aEntry[0])
                sDesc = ''

                # Certains films n'ont pas de date.
                try:
                    sYear = re.search('(\d{4})', aEntry[3]).group(1)
                except:
                    pass

                sDisplayTitle = sTitle

            else:
                sThumb = aEntry[0]
                if sThumb.startswith('/'):
                    sThumb = "https:" + sThumb

                sTitle = aEntry[1]
                # sQual = aEntry[2].replace(':', '').replace(' ', '').replace(',', '/')

                # Certains films n'ont pas de date.
                try:
                    sYear = re.search('(\d{4})', aEntry[4]).group(1)
                except:
                    pass

                sDesc = aEntry[5]
                siteUrl = re.sub('www\.', '', aEntry[6])
                sDisplayTitle = sTitle


            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumb, sDesc, oOutputParameterHandler)

        if sSearch:
            sPattern = 'nextlink" id="nextlink" onclick="javascript:list_submit\(([0-9]+)\); return\(false\)" href="#">Suivant'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sSearch)
                oOutputParameterHandler.addParameter('nextPageSearch', aResult[1][0])
                number = re.search('([0-9]+)', aResult[1][0]).group(1)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + number, oOutputParameterHandler)

        else:
            sNextPage, sPaging = __checkForNextPage(sHtmlContent)
            if sNextPage:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

    if nextPageSearch:
        oGui.setEndOfDirectory()

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>([^<]+)</a>\s+<a href="([^"]+)">Suivant &#8594;'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="fa fa-play-circle-o"><\/i>([^<]+)<\/div>|href="([^"]+)" title="([^"]+)" target="seriePlayer'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sethost = set()

    if aResult[0]:
        for aEntry in aResult[1]:

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
                continue

            sHosterUrl = aEntry[1]
            if sHosterUrl not in sethost:
                sethost.add(sHosterUrl)
            else:
                continue

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
