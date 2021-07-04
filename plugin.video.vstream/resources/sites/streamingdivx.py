# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, addon

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
sColor = addon().getSetting("deco_color")

SITE_IDENTIFIER = 'streamingdivx'
SITE_NAME = 'Streamingdivx'
SITE_DESC = 'Films VF en streaming.'

URL_MAIN = 'https://wvw.streamingdivx.stream/'

MOVIE_NEWS = (URL_MAIN + 'films.html', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'films/', 'showGenres')

SERIE_NEWS = (URL_MAIN + 'series.html', 'showMovies')

URL_SEARCH = (URL_MAIN + 'recherche?q=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'recherche?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

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
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append(['Action', sUrl + 'action'])
    liste.append(['Animation', sUrl + 'animation'])
    liste.append(['Aventure', sUrl + 'aventure'])
    liste.append(['Biopic', sUrl + 'biopic'])
    liste.append(['Comédie', sUrl + 'comedie'])
    liste.append(['Comédie-dramatique', sUrl + 'comedie-dramatique'])
    liste.append(['Comédie-musicale', sUrl + 'comedie-musicale'])
    liste.append(['Documentaire', sUrl + 'documentaire'])
    liste.append(['Drame', sUrl + 'drame'])
    liste.append(['Epouvante Horreur', sUrl + 'epouvante-horreur'])
    liste.append(['Famille', sUrl + 'famille'])
    liste.append(['Fantastique', sUrl + 'fantastique'])
    liste.append(['Guerre', sUrl + 'guerre'])
    liste.append(['Opera', sUrl + 'opera'])
    liste.append(['Policier', sUrl + 'policier'])
    liste.append(['Romance', sUrl + 'romance'])
    liste.append(['Science-fiction', sUrl + 'science-fiction'])
    liste.append(['Thriller', sUrl + 'thriller'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="short-images.+?<a href="([^"]+)" title="([^"]+)" class=.+?<img src="([^"]+).+?(?:<div class="short-content">|<a href=.+?qualite.+?>(.*?)</a>.+?<a href=.+?langue.+?>(.*?)</a>)'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            if sUrl.startswith('/'):
                sUrl = URL_MAIN[:-1] + sUrl

            sTitle = aEntry[1].replace('Streaming', '').replace('streaming', '').replace('série', '')
            # sTitle = sTitle.decode('utf-8').encode("latin-1")

            sThumb = aEntry[2]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            sThumb = sThumb.replace('wwww.', 'www.')    # pb d'url sur les images lors des recherches

            sQual = ''
            if aEntry[3]:
                sQual = aEntry[3]

            sLang = ''
            if aEntry[4]:
                sLang = aEntry[4]

            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang.upper())

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 'series/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:  # une seule page par recherche
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            number = re.search('page-([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = ">([^<]+)</a></div></div><div class=\"col-lg-1 col-sm-2 col-xs-2 pages-next\"><a href=['\"]([^'\"]+)"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page-([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        if sNextPage.startswith('/'):
            sNextPage = URL_MAIN[:-1] + sNextPage

        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # syno
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
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in reversed(aResult[1]):

            sUrl = aEntry[0]
            if sUrl.startswith('/'):
                sUrl = URL_MAIN[:-1] + sUrl

            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            sTitle = aEntry[2].replace('Streaming', '').replace('streaming', '')\
                              .replace('Voir la série', '').replace('en  VF et VOSTFR', '')

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addSeason(SITE_IDENTIFIER, 'showEp', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEp():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = oParser.abParse(sHtmlContent, '<div class="episode-list">', 'Series similaires')

    sPattern = '<div class="sai.+?<a href="([^"]+)".+?<span>(.+?)</span>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in reversed(aResult[1]):

            sUrl = aEntry[0]
            if not sUrl.startswith('http'):
                sUrl = URL_MAIN + sUrl

            sTitle = aEntry[1]

            sDisplayTitle = ('%s %s') % (sMovieTitle, sTitle)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    # streamer.php?p=169&c=V1RJeGMxcHVSbmhhUnpGMFltNU9kMWxYVW5sWlVUMDk=
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    
    sUrl = oRequest.getRealUrl()

    # syno
    sDesc = ''
    try:
        sPattern = '<div class="f*synopsis"><p>(.+?)</p></div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    sPattern2 = 'class="stream.*?">.+?data-num="([^"]+)" data-code="([^"]+)".+?<i class="([^"]+)".+?src="([^"]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern2)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sHost = aEntry[2].replace('server player-', '').replace('télécharger sur ', '').capitalize()

            # Filtre des host
            oHoster = cHosterGui().checkHoster(sHost)
            if not oHoster:
                continue

            sLang = aEntry[3].split('/')[-1].replace('.png', '').replace('?ver=41', '').upper()

            sDisplayTitle = ('%s (%s) [COLOR %s]%s[/COLOR]') % (sMovieTitle, sLang, sColor, sHost)

            oOutputParameterHandler.addParameter('datanum', aEntry[0])
            oOutputParameterHandler.addParameter('datacode', aEntry[1])
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sReferer = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    datanum = oInputParameterHandler.getValue('datanum')
    datacode = oInputParameterHandler.getValue('datacode')

    sUrl = URL_MAIN + 'streamer.php?p=' + datanum + '&c=' + datacode

    oRequest = cRequestHandler(sUrl)
    # oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', sReferer)
    oRequest.request()

    sHosterUrl = oRequest.getRealUrl()
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
