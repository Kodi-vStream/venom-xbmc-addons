# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import siteManager

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

# On garde le nom kepliz pour pas perturber
SITE_IDENTIFIER = 'kepliz_com'
SITE_NAME = 'Kepliz'
SITE_DESC = 'Films en streaming'

# Source compatible avec les clones : toblek, bofiaz, nimvon
# mais pas compatible avec les clones, qui ont une redirection directe : sajbo, trozam, radego
URL_HOST = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_HOST = dans sites.json
URL_MAIN = 'URL_MAIN'

# pour l'addon
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'c/poblom/29/0', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_HD = (URL_MAIN, 'showMovies')

DOC_NEWS = (URL_MAIN + 'c/poblom/26/0', 'showMovies')
SHOW_SHOWS = (URL_MAIN + 'c/poblom/3/0', 'showMovies')

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_MISC = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films (A l\'affiche)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SHOW_SHOWS[0])
    oGui.addDir(SITE_IDENTIFIER, SHOW_SHOWS[1], 'Spectacles', 'doc.png', oOutputParameterHandler)

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

    liste = []
    liste.append(['A l\'affiche', 29])
    liste.append(['Action', 1])
    liste.append(['Animation', 2])
    liste.append(['Aventure', 4])
    # liste.append(['Biographie', 5])  # aucun
    liste.append(['Comédie', 6])
    liste.append(['Documentaires', 26])
    liste.append(['Drame', 7])
    liste.append(['Epouvante Horreur', 9])
    liste.append(['Fantastique', 8])
    liste.append(['Policier', 10])
    liste.append(['Science Fiction', 11])
    liste.append(['Spectacle', 3])
    liste.append(['Thriller', 12])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, iGenre in liste:
        sUrl = URL_MAIN + 'c/poblom/%d/0' % iGenre
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    # L'url change tres souvent donc faut la retrouver
    oRequestHandler = cRequestHandler(URL_HOST)
    data = oRequestHandler.request()
    aResult = oParser.parse(data, '<a.+?href="(/*[0-9a-zA-Z]+)"')  # Compatible avec plusieurs clones
    if not aResult[0]:
        return   # Si ca ne marche pas, pas la peine de continuer

    # memorisation pour la suite
    sMainUrl = URL_HOST + aResult[1][0] + '/'
    # correction de l'url

    # En cas de recherche direct OU lors de la navigation dans les differentes pages de résultats d'une recherche
    if sSearch:
        oUtil = cUtil()
        sSearch = sSearchText = oUtil.CleanName(sSearch)
        sSearch = sSearch[:20]  # limite de caractere sinon bug de la recherche

        siteName = sMainUrl.split('/')[2].split('.')[0]
        sUrl = sMainUrl + 'home/{0!s}'.format(siteName)
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParameters('searchword', sSearch)
        sABPattern = '<div class="column24"'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        if sUrl == URL_MAIN:  # page d'accueil
            sABPattern = '<div class="column1"'
        else:
            sABPattern = '<div class="column20"'
        sUrl = sUrl.replace(URL_MAIN, sMainUrl)
        oRequestHandler = cRequestHandler(sUrl)

    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(sHtmlContent, sABPattern, '<div class="column2"')
    sPattern = '<span style="list-style-type:none;".+? href="\/[0-9a-zA-Z]+\/([^"]+)">(.+?)\((.+?)\).+?>(<i>(.+?)</i>|)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    else:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sTitle = aEntry[1].strip()
            sYear = aEntry[2]
            sQual = aEntry[4]
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue    # Filtre de recherche

            sDisplayTitle = ("%s (%s) [%s]") % (sTitle, sYear, sQual)
            oOutputParameterHandler.addParameter('siteUrl', sMainUrl + sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sMainUrl', sMainUrl)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', '', '', oOutputParameterHandler)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_HOST[:-1] + sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Suivant', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'a><a style="position: relative;top: 3px;margin-right: 6px;" href="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    # sMainUrl = oInputParameterHandler.getValue('sMainUrl')
    # sYear = oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.replace('<br/>', '')  # traitement de sDesc

    # Recuperation info film, com et image
    sThumb = ''
    sDesc = ''
    sPattern = '<img src="([^"]+).+?<p.+?>([^<]+)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sThumb = aResult[1][0][0]
        sDesc = aResult[1][0][1]

    sPattern = '<iframe.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sLink = aResult[1][0]
        if sLink.startswith('/'):
            sLink = URL_HOST[:-1] + sLink

        oRequestHandler = cRequestHandler(sLink)
        data = oRequestHandler.request()

        sPattern = 'file: *"(.+?)"'
        aResult = oParser.parse(data, sPattern)

        if aResult[0]:
            for aEntry in aResult[1]:

                sLink2 = aEntry
                oHoster = cHosterGui().checkHoster(sLink2)

                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sLink2, sThumb)

    oGui.setEndOfDirectory()
