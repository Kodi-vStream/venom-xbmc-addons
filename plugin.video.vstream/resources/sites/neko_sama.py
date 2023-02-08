# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager


SITE_IDENTIFIER = 'neko_sama'
SITE_NAME = 'Neko Sama'
SITE_DESC = 'Animés en streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

ANIM_ANIMS = ('http://', 'load')
ANIM_NEWS = (URL_MAIN, 'showLastEp')
ANIM_VFS = (URL_MAIN + 'anime-vf', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'anime', 'showMovies')

URL_SEARCH = (ANIM_VOSTFRS[0], 'showSearchResult')
URL_SEARCH_ANIMS = (ANIM_VOSTFRS[0], 'showSearchResult')
URL_SEARCH_VF = (ANIM_VFS[0], 'showSearchResult')

FUNCTION_SEARCH = 'showSearchResult'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche d\'animés (VOSTFR)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_VF[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche d\'animés (VF)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Dernier ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        showSearchResult(sSearchText)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts Martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie Dramatique', 'comedie-dramatique'], ['Comédie Musicale', 'comedie-musicale'],
             ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Epouvante Horreur', 'epouvante-horreur'],
             ['Erotique', 'erotique'], ['Espionnage', 'espionnage'], ['Famille', 'famille'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Historique', 'historique'], ['Musical', 'musical'],
             ['Policier', 'policier'], ['Péplum', 'peplum'], ['Romance', 'romance'],
             ['Science Fiction', 'science-fiction'], ['Spectacle', 'spectacle'], ['Thriller', 'thriller'],
             ['Western', 'western'], ['Divers', 'divers']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearchResult(sSearch):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    searchURL = URL_MAIN[:-1] + re.search('var urlsearch = "([^"]+)";', sHtmlContent).group(1)

    bGlobal_Search = False
    if sSearch:
        if URL_SEARCH[0] in sSearch:
            bGlobal_Search = True
            sSearch = sSearch.replace(URL_SEARCH[0], '')
    sSearch = sSearch.lower()

    oRequestHandler = cRequestHandler(searchURL)
    data = oRequestHandler.request(jsonDecode=True)

    oOutputParameterHandler = cOutputParameterHandler()
    for dicts in data:
        if sSearch in dicts['title'].lower() or sSearch in dicts['title_english'].lower() or sSearch in dicts['others'].lower():
            sTitle = dicts['title']
            sUrl2 = URL_MAIN[:-1] + dicts['url']
            sThumb = dicts['url_image']
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addAnime(SITE_IDENTIFIER, 'showSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def showLastEp():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '"episode":"([^"]+)".+?","title":"([^"]+)".+?"lang":"([^"]+)".+?"anime_url":"([^"]+)".+?"url_bg":"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = URL_MAIN[:-1] + aEntry[3]
            sThumb = aEntry[4]
            sLang = aEntry[2].upper()
            sTitle = '%s %s [%s]' % (aEntry[1], aEntry[0], sLang)
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oGui.addEpisode(SITE_IDENTIFIER, 'showSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)">.+?src="([^"]+)" alt="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = URL_MAIN[:-1] + aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addAnime(SITE_IDENTIFIER, 'showSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>([^<]+)</a><a href="([^"]+)" class=""><svg'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = URL_MAIN[:-1] + aResult[1][0][1]
        sNumberNext = re.search('/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisonEpisodes():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    if sUrl.endswith("vostfr"):
        oRequestHandler = cRequestHandler(sUrl.replace('vostfr', 'vf'))
        sHtmlContent = oRequestHandler.request()
        if "404 Not Found" not in sHtmlContent:
            oOutputParameterHandler = cOutputParameterHandler()
            sTitle = "[COLOR red]Cliquez ici pour accéder à la version VF[/COLOR]"
            oOutputParameterHandler.addParameter('siteUrl', sUrl.replace('vostfr', 'vf'))
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showSaisonEpisodes', sTitle, '', oOutputParameterHandler)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    try:
        sPattern = '<p>(.+?)</p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    sPattern = '"episode":"([^"]+)".+?"url":"([^"]+)","url_image":"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sTitle = sMovieTitle + ' ' + aEntry[0].replace('Ep. ', 'E')
            sUrl2 = URL_MAIN[:-1] + aEntry[1].replace('\\/', '/')
            sThumb = aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = "video\[\d+\] = \'([^']+)\'"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            # Enlève les faux liens
            # if 'openload' in aEntry or '.mp4' not in aEntry:
            if 'openload' in aEntry or 'mystream.to' in aEntry or "streamtape" in aEntry:
                continue

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
