# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

# On garde le nom kepliz pour pas perturber
SITE_IDENTIFIER = 'kepliz_com'
SITE_NAME = 'Kepliz'
SITE_DESC = 'Films en streaming'

# Source compatible avec les clones : toblek, bofiaz, nimvon
# mais pas compatible avec les clones, qui ont une redirection direct : sajbo, trozam, radego
URL_HOST = 'http://www.wavob.com/'
URL_MAIN = 'URL_MAIN'

# pour l'addon
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'c/wavob/29/0', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_HD = (URL_MAIN, 'showMovies')

DOC_NEWS = (URL_MAIN + 'c/wavob/26/0', 'showMovies')
SHOW_SHOWS = (URL_MAIN + 'c/wavob/3/0', 'showMovies')

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
    if (sSearchText != False):
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
        sUrl = URL_MAIN + 'c/wavob/%d/0' %iGenre
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
        sSearch = sSearch[:20]      # limite de caractere sinon bug de la recherche
        oRequestHandler = cRequestHandler(sMainUrl + 'home/wavob/')
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParameters('searchword', sSearch.replace(' ', '+'))
        sABPattern = '<div class="column24"'
        # sUrl = URL_MAIN + 'index.php?ordering=&searchphrase=all&option=com_search&searchword=' + sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        if sUrl == URL_MAIN:        # page d'acceuil
            sABPattern = '<div class="column1"'
        else:
            sABPattern = '<div class="column20"'
        sUrl = sUrl.replace(URL_MAIN, sMainUrl)
        oRequestHandler = cRequestHandler(sUrl)

    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(sHtmlContent, sABPattern, '<div class="column2"')
    sPattern = '<span style="list-style-type:none;" >.+? href="\/[0-9a-zA-Z]+\/([^"]+)">(.+?)\((.+?)\).+?>(<i>(.+?)<\/i>|)'
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

            sUrl2 = aEntry[0]
            sYear = aEntry[2]

            sTitle = ("%s (%s) [%s]") % (aEntry[1], sYear, aEntry[4])

            oOutputParameterHandler.addParameter('siteUrl', sMainUrl + sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', aEntry[1].strip())
            oOutputParameterHandler.addParameter('sMainUrl', sMainUrl)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', '', '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_HOST + sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Suivant', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'href="([^"]+)"><img style="position:relative;" +src="data:image'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMainUrl = oInputParameterHandler.getValue('sMainUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sYear = oInputParameterHandler.getValue('sYear')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.replace('<br/>', '')  # traitement de sDesc

    # Recuperation info film, com et image
    sThumb = ''
    sDesc = ''
    sPattern = '<p style="text-align: center;"><img src="([^"]+)".+?<p style="text-align: left;">(.+?)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sThumb = aResult[1][0][0]
        sDesc = cUtil().unescape(aResult[1][0][1])

    sPattern = '<iframe src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):

        sMovieTitle = sMovieTitle.replace(' [HD]', '')
        sLink = aResult[1][0]
        if sLink.startswith('/'):
            sLink = URL_HOST[:-1] + sLink

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sLink', sLink)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)

        oGui.addLink(SITE_IDENTIFIER, 'showHostersLink3', sMovieTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHostersLink3():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sLink = oInputParameterHandler.getValue('sLink')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sLink)
    data = oRequestHandler.request()

    # Recherche du premier lien
    sPattern = "href='(.+?)'"
    aResult = oParser.parse(data, sPattern)

    # Si il existe, suivi du lien
    if ( aResult[0] == True ):
        oRequestHandler = cRequestHandler(aResult[1][0])
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', sLink)
        data = oRequestHandler.request()

    sPattern = "src: '(.+?)'.+?res: (.+?),"
    aResult = oParser.parse(data, sPattern)

    if (aResult[0] == True):

        for aEntry in aResult[1]:

            sLink2 = aEntry[0]
            sQual = aEntry[1]

            sTitle = ('%s [%s]') % (sMovieTitle, sQual)

            oHoster = cHosterGui().checkHoster("mp4")

            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sLink2, '')

    oGui.setEndOfDirectory()
