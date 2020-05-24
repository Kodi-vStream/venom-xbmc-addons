# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
import re

SITE_IDENTIFIER = 'asia_insane'
SITE_NAME = 'Asia Insane'
SITE_DESC = 'Regarder Films et Séries Asiatique en Streaming gratuit'

URL_MAIN = 'https://www.asia-insane.biz/'

# definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle sera affichee.
# LA RECHERCHE GLOBAL N'UTILE PAS showSearch MAIS DIRECTEMENT LA FONCTION INSCRITE DANS LA VARIABLE URL_SEARCH_*
# FUNCTION_SEARCH = 'showMovies'
# URL_SEARCH = (URL_MAIN + '/recherche/', 'showMovies')
# recherche global films
# URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
# recherche global serie
# URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films-asiatiques-affichage-grid/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')
MOVIE_LIST = (URL_MAIN + 'films-asiatiques-vostfr-affichage-alphanumerique/', 'showAlpha')
DRAMA_DRAMAS = (URL_MAIN + 'liste-des-dramas-vostfr-ddl/', 'showMovies')


def load():
    oGui = cGui()

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    # oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DRAMA_DRAMAS[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_DRAMAS[1], 'Films & Séries (Dramas)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Ordre alphabétique)', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + 'amy_genre/'

    liste = []
    liste.append(['Action', sUrl + 'action/'])
    liste.append(['Adulte', sUrl + 'adulte/'])
    liste.append(['Arts Martiaux', sUrl + 'arts-martiaux/'])
    liste.append(['Aventure', sUrl + 'aventure/'])
    liste.append(['Comédie', sUrl + 'comedie/'])
    liste.append(['Comédie érotique', sUrl + 'comedie-erotique/'])
    liste.append(['Contenu adulte', sUrl + 'contenu-adulte/'])
    liste.append(['Crime', sUrl + 'crime/'])
    liste.append(['Drame', sUrl + 'drame/'])
    liste.append(['Ecole', sUrl + 'ecole/'])
    liste.append(['Erotique', sUrl + 'erotique/'])
    liste.append(['Expérimental', sUrl + 'experimental/'])
    liste.append(['Famille', sUrl + 'famille'])
    liste.append(['Fantastique', sUrl + 'fantastique/'])
    liste.append(['Gastronomie', sUrl + 'gastronomie/'])
    liste.append(['Gay', sUrl + 'gay/'])
    liste.append(['Guerre', sUrl + 'guerre/'])
    liste.append(['Histoire vraie', sUrl + 'histoire-vraie/'])
    liste.append(['Historique', sUrl + 'historique/'])
    liste.append(['Horreur', sUrl + 'horreur/'])
    liste.append(['Maladie', sUrl + 'maladie/'])
    liste.append(['Médecine', sUrl + 'medecine/'])
    liste.append(['Mélodrame', sUrl + 'melodrame/'])
    liste.append(['Musical', sUrl + 'musical/'])
    liste.append(['Mystère', sUrl + 'mystere/'])
    liste.append(['Policier', sUrl + 'policier/'])
    liste.append(['Psycologique', sUrl + 'psycologique/'])
    liste.append(['Romance', sUrl + 'romance/'])
    liste.append(['Science Fiction', sUrl + 'science-fiction/'])
    liste.append(['Sport', sUrl + 'sport'])
    liste.append(['Suspense', sUrl + 'suspense'])
    liste.append(['Travail', sUrl + 'travail/'])
    liste.append(['Tranche de vie', sUrl + 'tranche-de-vie/'])
    liste.append(['Thriller', sUrl + 'thriller/'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showLight', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()

    from itertools import chain
    generator = chain([1966, 1972, 1987, 1988, 1990, 1991, 1992], range(1994, 2021))

    for i in reversed(list(generator)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'date/' + Year + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showLight', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAlpha():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'front">.+?src="(http[^"]+).+?field-title"><a href="([^"]+)">([^<]+).+?field-desc"><p>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            sUrl = aEntry[1]
            sTitle = aEntry[2].split('dd')[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '[' in aEntry[2]:  # pour les séries il y a des crochets dans le titre
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            sPattern = 'class="next page-numbers".+?page/(\d{1,3})'
            aResult = oParser.parse(sHtmlContent, sPattern)
            page = ''
            if (aResult[0] == True):
                page = aResult[1][0]

            oGui.addNext(SITE_IDENTIFIER, 'showAlpha', '[COLOR teal]Page ' + page + ' >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showLight():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'entry-item clearfix">.+?src="(http[^"]+).+?entry-title"><a href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            sUrl = aEntry[1]
            sTitle = aEntry[2].split('dd')[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '[' in aEntry[2]:  # pour les séries il y a des crochets dans le titre
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            sPattern = 'class="next page-numbers".+?page/(\d{1,3})'
            aResult = oParser.parse(sHtmlContent, sPattern)
            page = ''
            if (aResult[0] == True):
                page = aResult[1][0]

            oGui.addNext(SITE_IDENTIFIER, 'showLight', '[COLOR teal]Page ' + page + ' >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if sSearch:
        sUrl = sSearch.replace(' ', '+')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    # sPattern = 'front">.+?src="(http[^"]+).+?field-title".+?href="([^"]+)">([^<]+)d{2}.+?field-desc"><p>([^<]+).+?(?:|/version/([^/]+).+?)(?:|/date/([^/]+).+?)Genre:'
    sPattern = 'front">.+?src="(http[^"]+).+?field-title"><a href="([^"]+)">([^<]+).+?field-desc"><p>([^<]+).+?(?:|/version/([^/]+).+?)(?:|/date/([^/]+).+?)Genre:'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            sUrl2 = aEntry[1]
            sTitle = aEntry[2].split('dd')[0]
            sDesc = aEntry[3]
            sQual = aEntry[4].upper()
            sYear = aEntry[5]

            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sYear)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if '[' in aEntry[2]:  # pour les séries il y a des crochets dans le titre
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            sPattern = 'class="next page-numbers".+?page\/(\d{1,3})'
            aResult = oParser.parse(sHtmlContent, sPattern)
            page = ''
            if (aResult[0] == True):
                page = aResult[1][0]

            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + page + ' >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'class="next page-numbers".+?href="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return  aResult[1][0]

    return False


def showEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sStart = 'itemprop="description articleBody">'
    sEnd = '<!-- #respond -->'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    # fh = open('c:\\test.txt', 'w')
    # fh.write(sHtmlContent)
    # fh.close()
 
    sPattern = '(.pisode :|Bonus :|Multiup:|DDL :)|href="(https:\/\/(?:multiup|uptobox)[^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if aEntry[0]:  # Affichage de épisode ou bonus ou host
                oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + aEntry[0] + '[/COLOR]')
            else:
                sUrl = aEntry[1]
                sEpisode = 'Episode' + aEntry[2]
                sTitle = sMovieTitle + ' ' + sEpisode

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sYear', sYear)

                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = 'itemprop="description articleBody">'
    sEnd = '<!-- #respond -->'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
    sPattern = 'href="(https:\/\/(?:multiup|uptobox)[^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            sHost = aEntry[1]

            # filtrage des hosters
            # oHoster = cHosterGui().checkHoster(sHost)
            # if not oHoster:
                # continue

            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sHosterUrl = sUrl

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
