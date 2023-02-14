return False # Désactivé le 08/04/2020

# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

from resources.lib.comaddon import progress#, VSlog

SITE_IDENTIFIER = 'replaytvstreaming_com'
SITE_NAME = 'Replay Tv Streaming'
SITE_DESC = 'Replay TV'

URL_MAIN = 'https://replaytvstreaming.com/'

MOVIE_MOVIE = (URL_MAIN + 'film', 'showMovies')

REPLAYTV_NEWS = (URL_MAIN, 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')
REPLAYTV_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + 'index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + 'index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Replay (Derniers ajouts)', 'replay.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_GENRES[1], 'Replay (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        sSearchText = sSearchText.replace(' ', '+')

        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []
    liste.append(['Emissions et Magazines', URL_MAIN + 'emission-magazine'])
    liste.append(['Documentaires', URL_MAIN + 'documentaire'])
    liste.append(['Spectacles', URL_MAIN + 'spectacle'])
    liste.append(['Sports', URL_MAIN + 'sport'])
    liste.append(['Téléfilms Fiction', URL_MAIN + 'telefilm-fiction'])
    liste.append(['Films', URL_MAIN + 'film'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
        sUrl = URL_SEARCH[0] + sSearch

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)

        sHtmlContent = oRequestHandler.request()
        sPattern = '<div class="item-box"><a class="item-link" href="([^"]+)"><div class="item-img"><img src="([^"]+)".+?<div class="item-title">([^<]+)<'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = '<div class="item-box"><a class="item-link" href="([^"]+)">.+?<img src="([^"]+)".+?<div class="item-title">([^<]+)<\/div><div class="item-info clearfix">([^<]+)<\/div>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sTitle = aEntry[2]
            sThumb = aEntry[1]
            if not sThumb.startswith('http'):
                sThumb = URL_MAIN + sThumb

            sDesc = ''
            if len(aEntry) > 3:
                sDesc = aEntry[3]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="pnext"><a href="([^"]+)">SUIVANT<\/a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showLinks(page, video):
    sUrl = 'http://replaytvstreaming.com/engine/ajax/re_video_part.php?block=video&page=' + page + '&id=' + video

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    url = sHtmlContent
    return url


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<div id="video_[0-9]+" class="epizode re_poleta.+?" data-re_idnews="([^"]+)" data-re_xfn="video" data-re_page="([^"]+)">([^<]+)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sTest = ''

    if aResult[0]:
        for aEntry in aResult[1]:

            sPage = aEntry[1]
            sVideoID = aEntry[0]
            sHosterUrl = showLinks(sPage, sVideoID)
            sHosterUrl = cUtil().unescape(sHosterUrl)

            sTitle = aEntry[2]

            if not 'Lecteur' in sTitle and sTest != sTitle:
                oGui.addText(SITE_IDENTIFIER, '[COLOR olive]' + sTitle + '[/COLOR]')
                sTest = sTitle

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    else:
        sPattern = '<div class="playe.+?" data-show_player="video"><iframe.+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0]:
            sHosterUrl = aResult[1][0]
            sHosterUrl = cUtil().unescape(sHosterUrl)

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
