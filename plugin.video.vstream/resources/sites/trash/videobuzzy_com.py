# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
return False
import re
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'videobuzzy_com'
SITE_NAME = 'Videobuzzy'
SITE_DESC = 'Sélection des vidéos les plus populaires de Videobuzzy'

URL_MAIN = 'https://www.videobuzzy.com/'

NETS_NETS = ('http://', 'load')
NETS_NEWS = (URL_MAIN, 'showMovies')
NETS_GENRES = (True, 'showGenres')

# URL_SEARCH = ('http://www.notre-ecole.net/?s=', 'showMovies')
# FUNCTION_SEARCH = 'showMovies'


def load():

    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', NETS_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_NEWS[1], 'Vidéos du net', 'buzz.png',oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', NETS_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_GENRES[1], 'Vidéos du net (Genres)', 'genres.png',oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText):
        sUrl = URL_MAIN + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []
    liste.append(['Galerie', URL_MAIN + 'galerie.htm'])
    liste.append(['Football', URL_MAIN + 'football.htm'])
    liste.append(['Humour', URL_MAIN + 'humour.htm'])
    liste.append(['Animaux', URL_MAIN + 'animaux.htm'])
    liste.append(['Insolite', URL_MAIN + 'insolite.htm'])
    liste.append(['Télévision', URL_MAIN + 'television.htm'])
    liste.append(['Musique', URL_MAIN + 'musique.htm'])
    liste.append(['Sport', URL_MAIN + 'sport.htm'])
    liste.append(['Cinéma', URL_MAIN + 'cinema.htm'])
    # liste.append(['Bref.', URL_MAIN + 'BREF-tous-les-episodes-de-la-serie-de-canal-+-4902.news'])
    liste.append(['Top Vidéo', URL_MAIN + 'top-video.php'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = "class='titre_news_index' href='(.+?)' title='(.+?)'.+?class=\"thumbnail\" src='(.+?)'.+?class='corps_news_p2'>(.+?)</span>"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1]
            sThumb = aEntry[2]
            sDesc = aEntry[3]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            number = re.search('/page-([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + number, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="current">.+?</span><a href="(.+?)" title=\'.+?\'>.+?</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return URL_MAIN + aResult[1][0]

    return False


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'file: "(.+?)", label: "(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]
            sTitle = sMovieTitle + ' | ' + aEntry[1]
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
