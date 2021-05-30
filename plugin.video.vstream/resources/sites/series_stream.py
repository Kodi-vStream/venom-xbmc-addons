# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import progress
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'series_stream'
SITE_NAME = 'Séries Stream'
SITE_DESC = 'Voir une panoplie de séries en streaming VF et VOSTFR avec qualité full HD et en illimité.'

URL_MAIN = 'https://www.series-stream.cc/'

SERIE_SERIES = (True, 'load')
SERIE_NEWS = (URL_MAIN + 'series.html', 'showSeries')
SERIE_GENRES = (True, 'showGenres')
SERIE_ANNEES = (True, 'showYears')
SERIE_LIST = (True, 'showAlpha')

URL_SEARCH = (URL_MAIN + 'recherche?q=', 'showSeries')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showSeries')
FUNCTION_SEARCH = 'showSeries'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Par ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showSeries(URL_SEARCH[0] + sSearchText)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + 'series/action/'])
    liste.append(['Animation', URL_MAIN + 'series/animation/'])
    liste.append(['Aventure', URL_MAIN + 'series/aventure/'])
    liste.append(['Biopic', URL_MAIN + 'series/biopic/'])
    liste.append(['Comédie', URL_MAIN + 'series/comedie/'])
    liste.append(['Drame', URL_MAIN + 'series/drame/'])
    liste.append(['Epouvante Horreur', URL_MAIN + 'series/epouvante-horreur/'])
    liste.append(['Espionnage', URL_MAIN + 'series/espionnage/'])
    liste.append(['Famille', URL_MAIN + 'series/famille/'])
    liste.append(['Fantastique', URL_MAIN + 'series/fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'series/guerre/'])
    liste.append(['Historique', URL_MAIN + 'series/historique/'])
    liste.append(['Judiciaire', URL_MAIN + 'series/judiciaire/'])
    liste.append(['Musical', URL_MAIN + 'series/musical/'])
    liste.append(['Policier', URL_MAIN + 'series/policier/'])
    liste.append(['Romance', URL_MAIN + 'series/romance/'])
    liste.append(['Science Fiction', URL_MAIN + 'series/science-fiction/'])
    liste.append(['Sci-Fi & Fantasy', URL_MAIN + 'series/sci-fi-et-fantasy/'])
    liste.append(['Thriller', URL_MAIN + 'series/thriller/'])
    liste.append(['Western', URL_MAIN + 'series/western/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1989, 2022)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series/annee/' + Year + '.html')
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAlpha():
    oGui = cGui()
    sUrl = URL_MAIN + 'series/alphabet/'

    liste = [['0', sUrl + str('0')], ['1', sUrl + str('1')], ['2', sUrl + str('2')], ['3', sUrl + str('3')],
             ['4', sUrl + str('4')], ['5', sUrl + str('5')], ['6', sUrl + str('6')], ['7', sUrl + str('7')],
             ['8', sUrl + str('8')], ['9', sUrl + str('9')],
             ['A', sUrl + 'A'], ['B', sUrl + 'B'], ['C', sUrl + 'C'], ['D', sUrl + 'D'], ['E', sUrl + 'E'],
             ['F', sUrl + 'F'], ['G', sUrl + 'G'], ['H', sUrl + 'H'], ['I', sUrl + 'I'], ['J', sUrl + 'J'],
             ['K', sUrl + 'K'], ['L', sUrl + 'L'], ['M', sUrl + 'M'], ['N', sUrl + 'N'], ['O', sUrl + 'O'],
             ['P', sUrl + 'P'], ['Q', sUrl + 'Q'], ['R', sUrl + 'R'], ['S', sUrl + 'S'], ['T', sUrl + 'T'],
             ['U', sUrl + 'U'], ['V', sUrl + 'V'], ['W', sUrl + 'W'], ['X', sUrl + 'X'], ['Y', sUrl + 'Y'],
             ['Z', sUrl + 'Z']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeries(sSearch=''):
    oGui = cGui()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'radius-3">\s*<a href="([^"]+)".+?src="([^"]+)" alt="([^"]+)'
    oParser = cParser()
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

            sUrl = URL_MAIN[:-1] + aEntry[0]
            sThumb = URL_MAIN[:-1] + aEntry[1]
            sTitle = aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, '', oOutputParameterHandler)
        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>([0-9]+)</a></div>.+?next"><a href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sNumberMax = aResult[1][0][0]
        sNextPage = URL_MAIN[:-1] + aResult[1][0][1]
        sNumberNext = re.search('-([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération du Synopsis
    sDesc = ''
    try:
        sPattern = 'class="fsynopsis"><p>(.+?)</p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    sPattern = 'short-images radius-3".+?href="([^"]+)".+?<img src="([^"]+)".+?<figcaption>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            sThumb = URL_MAIN[:-1] + aEntry[1]
            sTitle = sMovieTitle + ' ' + aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="saision_LI2">\s*<a href="([^"]+)">\s*<span>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = URL_MAIN[:-1] + aEntry[0]
            sTitle = sMovieTitle + ' ' + aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLink', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'data-num="([^"]+).+?data-code="([^"]+).+?DIV_5.+?>([^<]+).+?src="/images/([^"]+).png'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            dataNum = aEntry[0]
            dataCode = aEntry[1]
            sHost = aEntry[2].capitalize()
            sLang = aEntry[3].upper()

            # filtrage des hosters
            oHoster = cHosterGui().checkHoster(sHost)
            if not oHoster:
                continue

            sTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)
            lien = URL_MAIN + 'streamer.php?p=' + dataNum + '&c=' + dataCode

            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('siteUrl', lien)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    referer = oInputParameterHandler.getValue('referer')
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Referer', referer)

    oRequestHandler.request()
    sHosterUrl = oRequestHandler.getRealUrl()
    oHoster = cHosterGui().checkHoster(sHosterUrl)

    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
