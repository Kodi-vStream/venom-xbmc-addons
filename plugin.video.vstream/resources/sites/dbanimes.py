# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'dbanimes'
SITE_NAME = 'DBanimes'
SITE_DESC = 'animés en streaming'

URL_MAIN = "https://dbanimes.com/"

ANIM_ANIMS = (True, 'load')
ANIM_VOSTFRS = (URL_MAIN + 'anime/', 'showMovies')
ANIM_NEWS = (URL_MAIN + 'anime/', 'showMovies')
ANIM_MOVIES = (URL_MAIN + 'statu/films/', 'showMovies')
ANIM_LIST = (URL_MAIN + 'liste/a/', 'showAlpha')
ANIM_GENRES = (True, 'showGenres')
ANIM_LAST_EPISODES = (URL_MAIN, 'showMovies')
key_serie = '?key_serie&s='
key_film = '?key_film&s='

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')
URL_INTERNALSEARCH_SERIES = (URL_MAIN + key_serie, 'showMovies')
URL_INTERNALSEARCH_MOVIES = (URL_MAIN + key_film, 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'siteUrl')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Films & Séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'siteUrl')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSerie', 'Recherche Séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_LAST_EPISODES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_LAST_EPISODES[1], 'Animés (Derniers épisodes)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'siteUrl')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovie', 'Recherche Films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_MOVIES[1], 'Animés (Films)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_LIST[1], 'Animés (Ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()

    listegenre = ['action', 'aventure', 'comedie', 'crime', 'drame', 'family', 'fantastique', 'josei', 'musical',
                  'mystere', 'psychologique', 'romance', 'school-life', 'science-fiction', 'seinen', 'shoujo',
                  'shounen', 'slice-of-life', 'sports', 'surnaturel', 'thriller', 'ueda-shigeru']

    oOutputParameterHandler = cOutputParameterHandler()
    for igenre in listegenre:
        sTitle = igenre.capitalize().replace('-', ' ')
        sUrl = URL_MAIN + 'genre/' + igenre + '/'
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAlpha():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'class=liste><a href=(\S+).+?mb-2">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sLetter = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('AZ', sLetter)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sLetter + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearchMovie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_INTERNALSEARCH_MOVIES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchSerie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_INTERNALSEARCH_SERIES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sSearch:
        sUrl = sSearch.replace(' ', '+') + '&post_type=anime&submit='

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    if URL_MAIN == sUrl or URL_MAIN + 'page/' in sUrl:
        sPattern = 'movie-gride-agile1">.+?<a href=([^\s]+)\s*title="([^"]+).+?src=([^\s]+)'
    else:
        sPattern = 'class=item>.+?<a href=([^\s]+)\s*title="([^"]+).+?src=([^\s]+)'

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

            sDesc = ''
            sUrl2 = aEntry[0]
            sTitle = aEntry[1].replace('VOSTFR', '').replace('vostfr', '').replace('Vostfr', '')  # à confirmer : tous vostr meme ceux  notés non vostfr
            sTitle = sTitle.replace('Saision', 'Saison').replace('Sasion', 'Saison')
            sDisplayTitle = sTitle
            sThumb = aEntry[2]

            if key_serie in sUrl:
                if 'film' in sTitle.lower():
                    continue
            if key_film in sUrl:
                if 'film' not in sTitle.lower():
                    continue

            if 'film' in sTitle.lower():
                sTitle = sTitle.replace('Film', '').replace('film', '')  # à reverifier .replace('Movie', '')
                sDisplayTitle = sTitle + ' [Film]'

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if URL_MAIN == sUrl or URL_MAIN + 'page/' in sUrl:
                oGui.addAnime(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addAnime(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '(\d+)</a></li> <li><a class="next page-numbers" href=([^\s]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, False


def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    sPattern = 'Synopsis\s*:(.*?)(?:</p>|</div>)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] == True:
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', cleanDesc(aResult[1][0]))

    sYear = ''
    sPattern = 'Année de Production.+?(\d+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] == True:
        sYear = aResult[1][0]

    sPattern = '(?:<p>|a>)\s<a href=([^\s]+).+?title=.+?>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] == True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME, large=total > 50)

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            sUrl = aEntry[0]
            sEpisode = aEntry[1]
            sTitle = sMovieTitle + ' ' + sEpisode
            sDisplayTitle = sTitle
            if sYear:
                sDisplayTitle = sTitle + '(' + sYear + ')'

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li class=streamer>.+?<iframe.*?src="*([^"\s]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    # i = 0
    if aResult[0] == True:
        for aEntry in aResult[1]:
            sHosterUrl = aEntry.strip()
            if 'https:' not in sHosterUrl:
                sHosterUrl = 'https:' + sHosterUrl

            # sHost = getHostName(sHosterUrl)
            # i = i + 1
            # sDisplayTitle = '%s [COLOR coral]%s[/COLOR]' % (sMovieTitle, sHost)

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def getHostName(url):
    oHoster = cHosterGui().checkHoster(url)
    if (oHoster != False):
        return oHoster.getDisplayName()
    try:
        if 'www' not in url:
            sHost = re.search('http.*?\/\/([^.]*)', url).group(1)
        else:
            sHost = re.search('htt.+?\/\/(?:www).([^.]*)', url).group(1)
    except:
        sHost = url
    return sHost.capitalize()


def cleanDesc(sDesc):
    oParser = cParser()
    sPattern = '(<.+?>)'
    aResult = oParser.parse(sDesc, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sDesc = sDesc.replace(aEntry, '')
    return sDesc
