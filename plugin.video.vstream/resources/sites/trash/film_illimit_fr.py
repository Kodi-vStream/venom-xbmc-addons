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
from resources.lib.util import cUtil, QuotePlus, Noredirection
from resources.lib.comaddon import progress

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

SITE_IDENTIFIER = 'film_illimit_fr'
SITE_NAME = 'Film illimité'
SITE_DESC = 'Films, Séries HD en streaming'

URL_MAIN = 'https://www.official-film-illimite.to/'

MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'films/streaming-720p-streaming-1080p/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (HD)', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

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

    liste = []
    liste.append(['Ultra-HD', URL_MAIN + 'ultra-hd/'])
    liste.append(['720p/1080p', URL_MAIN + 'films/streaming-720p-streaming-1080p/'])
    liste.append(['Action/Aventure', URL_MAIN + 'films/action-aventure/'])
    liste.append(['Animation', URL_MAIN + 'films/animation/'])
    liste.append(['Arts Martiaux', URL_MAIN + 'films/arts-martiaux/'])
    liste.append(['Biographie', URL_MAIN + 'films/biographique/'])
    liste.append(['Comédie', URL_MAIN + 'films/comedie/'])
    liste.append(['Crime/Gangster', URL_MAIN + 'films/crimegangster/'])
    liste.append(['Documentaire', URL_MAIN + 'films/documentaire/'])
    liste.append(['Drame', URL_MAIN + 'films/drame/'])
    liste.append(['Epouvante Horreur', URL_MAIN + 'films/epouvante-horreur/'])
    liste.append(['Etranger', URL_MAIN + 'films/etranger/'])
    liste.append(['Famille', URL_MAIN + 'films/famille/'])
    liste.append(['Fantastique', URL_MAIN + 'films/fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'films/guerre/'])
    liste.append(['Histoire', URL_MAIN + 'films/histoire/'])
    liste.append(['Musique/Danse', URL_MAIN + 'films/musiquedanse/'])
    liste.append(['Mystère', URL_MAIN + 'films/mystere/'])
    liste.append(['Policier', URL_MAIN + 'films/policier/'])
    liste.append(['Romance', URL_MAIN + 'films/romance/'])
    liste.append(['Science-fiction', URL_MAIN + 'films/science-fiction/'])
    liste.append(['Spectacle (FR)', URL_MAIN + 'spectacle/francais-spectacle/'])
    liste.append(['Spectacle (VOSTFR)', URL_MAIN + 'spectacle/vostfr-spectacle/'])
    liste.append(['Sport', URL_MAIN + 'films/sport/'])
    liste.append(['Suspense/Thriller', URL_MAIN + 'films/thrillersuspense/'])
    liste.append(['Téléfilm', URL_MAIN + 'films/telefilm/'])
    liste.append(['VOSTFR', URL_MAIN + 'films/vostfr/'])
    liste.append(['Western', URL_MAIN + 'films/western/'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="filter-content-slider">'
    sEnd = '<div class="filter-slide filter-slide-down">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl = URL_MAIN[:-1] + aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.replace('en illimité', 'en illimite')

    oParser = cParser()
    sPattern = 'class="item">.+?href="([^"]+).+?src="([^"]+)" alt="([^"]+).+?ttx">([^<]+).+?(?:|class="year">([^<]+).+?)class="calidad2'
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

            sTitle = aEntry[2].replace(' Streaming Ultra-HD', '').replace(' Streaming Full-HD', '')\
                              .replace(' en Streaming HD', '').replace(' Streaming HD', '')\
                              .replace(' streaming', '').replace('HD', '')

            sUrl2 = aEntry[0]
            sThumb = re.sub('/w\d+', '/w342', aEntry[1])
            if sThumb.startswith('//'):
                sThumb = 'http:' + sThumb
            sDesc = aEntry[3].split('en illimite')[1].replace('&#160;', '')
            sYear = aEntry[4]

            # Si recherche et trop de resultat, on filtre
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), sTitle) == 0:
                    continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)

            sPattern1 = '.+?saison [0-9]+'
            aResult1 = oParser.parse(sTitle, sPattern1)

            if aResult1[0]:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            number = re.search('page/([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + str(number) + ' >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = "<a class=\'current.+?href=\'([^']+)\'"
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
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Vire les bandes annonces
    sHtmlContent = sHtmlContent.replace('src="//www.youtube.com/', '')

    sPattern = '<iframe.+?src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry)
            if '//goo.gl' in sHosterUrl:
                try:
                    url8 = sHosterUrl.replace('https', 'http')

                    opener = Noredirection()
                    opener.addheaders.append(('User-Agent', UA))
                    opener.addheaders.append(('Connection', 'keep-alive'))

                    HttpReponse = opener.open(url8)
                    sHosterUrl = HttpReponse.headers['Location']
                    sHosterUrl = sHosterUrl.replace('https', 'http')
                except:
                    pass

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.replace('<iframe width="420" height="315" src="https://www.youtube.com/', '')
    sPattern = '<iframe.+?src="(http.+?)".+?>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        i = 1
        for aEntry in aResult[1]:

            sUrl = aEntry
            sTitle = '%s episode %s' % (sMovieTitle.replace(' - Saison', ' Saison'), i)

            i = i + 1

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'ShowSpecialHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def ShowSpecialHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    data = re.sub('(.+?f=)', '', sUrl)
    data = data.replace('&c=', '')
    pdata = 'data=' + QuotePlus(data)

    if 'fr-land.me' in sUrl:
        oRequest = cRequestHandler('http://fr-land.me/Htplugins/Loader.php')
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        # oRequest.addHeaderEntry('Host', 'official-film-illimite.to')
        oRequest.addHeaderEntry('Referer', sUrl)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequest.addParametersLine(pdata)

        sHtmlContent = oRequest.request()
        sHtmlContent = sHtmlContent.replace('\\', '')

        # fh = open('c:\\test.txt', "w")
        # fh.write(sHtmlContent)
        # fh.close()

        sPattern = '\[(.+?)\]'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            listurl = aResult[1][0].replace('"', '').split(',http')
            listqual = aResult[1][1].replace('"', '').split(',')

            tab = zip(listurl, listqual)

            for url, qual in tab:
                sHosterUrl = url
                if not sHosterUrl.startswith('http'):
                    sHosterUrl = 'http' + sHosterUrl

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    sDisplayTitle = '[' + qual + '] ' + sMovieTitle
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:

        oHoster = cHosterGui().checkHoster(sUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sUrl, sThumb)

    oGui.setEndOfDirectory()
