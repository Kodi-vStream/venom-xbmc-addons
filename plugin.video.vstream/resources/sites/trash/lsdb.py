# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Ovni-crea

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager

SITE_IDENTIFIER = 'lsdb'
SITE_NAME = 'Liveset Database'
SITE_DESC = 'liveset podcast et autre de musique électronique'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json
# URL_MAIN = 'https://lsdb.eu'  # Pas de / car peut poser probleme

URL_SEARCH = (URL_MAIN + '/search?q=', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

NETS_NEWS = (URL_MAIN + '/livesets', 'showMovies')
NETS_GENRES = (True, 'showGenres')
NETS_EVENTS = (URL_MAIN + '/events/index/1', 'showEvents')
NETS_SHOWS = (URL_MAIN + '/events/index/2', 'showShows')
NETS_PODCAST = (URL_MAIN + '/events/index/3', 'showPodcast')
NETS_PROMO = (URL_MAIN + '/events/index/4', 'showPromo')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', NETS_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_NEWS[1], 'Les nouveaux liveset', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', NETS_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_GENRES[1], 'Les genres musicaux', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', NETS_EVENTS[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_EVENTS[1], 'Les évènements ', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', NETS_SHOWS[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_SHOWS[1], 'Les shows', 'replay.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', NETS_PODCAST[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_PODCAST[1], 'Les podcasts', 'replay.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', NETS_PROMO[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_PROMO[1], 'Les promotions', 'replay.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Ambient', 'genre/ambient'], ['Acid', 'genre/acid'], ['Autre', 'genre/other'],
             ['Breakbeat', 'genre/breakbeat'], ['Breakcore', 'genre/breakcore'], ['Chiptune ', 'genre/chiptune'],
             ['Classic hardstyle', 'tag/classic-hardstyle'], ['Crossbreed', 'genre/crossbreed'],
             ['Dance', 'genre/dance'], ['Darkcore', 'genre/darkcore'], ['Deep House', 'genre/deephouse'],
             ['Disco', 'genre/disco'], ['Dark Psy', 'genre/darkpsy'], ['Darkstep', 'genre/darkstep'],
             ['Drum and bass', 'genre/drumnbass'], ['Dubstep', 'genre/dubstep'],
             ['Early hardcore', 'genre/earlyhardcore'], ['Early hardstyle', 'genre/earlyhardstyle'],
             ['Early terror', 'genre/earlyterror'], ['EBM', 'genre/ebm'], ['Eclectic', 'genre/eclectic'],
             ['Electro', 'genre/electro'], ['Euphoric hardstyle', 'tag/euphoric-hardstyle'], ['Fidget', 'genre/fidget'],
             ['Frenchcore', 'genre/frenchcore'], ['Funk', 'genre/funk'], ['Garage', 'genre/garage'],
             ['Goa', 'genre/goa'], ['Grime', 'genre/grim'], ['Hands-up', 'genre/handsup'],
             ['Happy hardcore', 'genre/happyhardcore'], ['Hardcore', 'genre/hardcore'], ['Hardstyle', 'genre/hardstyle'],
             ['Hardtechno', 'genre/hardtechno'], ['Hardtek', 'genre/hardtek'], ['Hardtrance', 'genre/hardtrance'],
             ['House', 'genre/house'], ['Industrial', 'genre/industrial'],
             ['Industrial hardcore', 'genre/industrialhardcore'], ['IDM', 'genre/idm'], ['Jump', 'genre/jump'],
             ['Jungle', 'genre/jungle'], ['Liquid', 'genre/liquid'], ['Lounge', 'genre/lounge'],
             ['Minimal', 'genre/minimal'], ['Moombahton', 'genre/moombahton'], ['Noise', 'genre/noise'],
             ['Oldschool', 'genre/oldschool'], ['Progressive', 'genre/progressive'],
             ['Progressive House', 'genre/progressivehouse'], ['Progressive Trance', 'genre/progressivetrance'],
             ['Psytrance', 'genre/psytrance'], ['Raw Hardstyle', 'tag/raw-hardstyle'], ['Speedcore', 'genre/speedcore'],
             ['Schranz', 'genre/schranz'], ['Speedcore', 'genre/speedcore'], ['Splittercore', 'genre/splittercore'],
             ['Tech house', 'genre/techhouse'], ['Techno', 'genre/techno'], ['Techtrance', 'genre/techtrance'],
             ['Tek', 'genre/tek'], ['Tekno', 'genre/tekno'], ['Terror', 'genre/terror'], ['Trance', 'genre/trance'],
             ['Tribal House', 'genre/tribalhouse'], ['UK Happy hardcore', 'genre/ukhappyhardcore'],
             ['UK Hardcore', 'genre/ukhardcore'], ['UK Hardhouse', 'genre/ukhardhouse'],
             ['Vocal Trance', 'genre/vocaltrance'], ['Witch house', 'genre/witchhouse']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/' + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<a href="([^"]+)">\s*<time datetime=.+?</time>\s*<span class=".+?<i class=".+?></i>\s*([^"]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = URL_MAIN + aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addMisc(SITE_IDENTIFIER, 'showIsdb', sTitle, 'replay.png', '', '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def showIsdb():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<a href="([^"]+)" class="split button expand text-left.+?> *([^<> ]+)*[.].+?<'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = URL_MAIN + aEntry[0]
            sHoster = aEntry[1].capitalize()
            sThumb = 'special://home/addons/plugin.video.vstream/resources/art/replay.png'

            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHoster)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        oGui.setEndOfDirectory()


def showEvents():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<i class=".+?"></i>\s* <a href="([^"]+)">\s*([^"]+)\s*</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = URL_MAIN + aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'annees.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showEvents', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showShows():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<i class=".+?"></i>\s* <a href="([^"]+)">\s*([^"]+)\s*</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = URL_MAIN + aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'replay.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showShows', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showPodcast():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<i class=".+?"></i>\s* <a href="([^"]+)">\s*([^"]+)\s*</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = URL_MAIN + aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'replay.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showPodcast', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showPromo():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<i class=".+?"></i>\s* <a href="([^"]+)">\s*([^"]+)\s*</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = URL_MAIN + aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'replay.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showPromo', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'class="active"><a href="".+?href="([^"]+).+?>(\d+)</a></li>\s*</ul>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = URL_MAIN + aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<br />\s*<a href="([^"]+)">.+?</a>.+?<br />'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
