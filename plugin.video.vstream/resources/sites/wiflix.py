# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.comaddon import siteManager
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil

import re

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'

SITE_IDENTIFIER = 'wiflix'
SITE_NAME = 'Wiflix'
SITE_DESC = 'Films & Séries en streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

MOVIE_MOVIE = (URL_MAIN + 'film-en-streaming/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'film-en-streaming/', 'showMovies')
MOVIE_EXCLU = (URL_MAIN + 'film-en-streaming/exclue', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = (URL_MAIN + 'serie-en-streaming/', 'showSeries')
SERIE_NEWS = (URL_MAIN + 'serie-en-streaming/', 'showSeries')
# SERIE_LIST = (URL_MAIN + 'serie-streaming/', 'showSeriesList')

URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showSearch')
URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_SERIES = ('', 'showSeries')
FUNCTION_SEARCH = 'showSearch'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://film')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Films', 'search-films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://serie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Séries', 'search-series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EXCLU[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EXCLU[1], 'Films et Séries (Exclus)', 'news.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if sSearchText:

        if 'film' in sUrl:
            showMovies(sSearchText)
        else:
            showSeries(sSearchText)

        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    oParser = cParser()

    sUrl = URL_MAIN
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = '</span><b>Films par genre</b></div>'
    sEnd = '<div class="side-b">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    TriAlpha = []
    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = URL_MAIN + aEntry[0]
            sTitle = aEntry[1].capitalize()
            TriAlpha.append((sTitle, sUrl))

        # Trie des genres par ordre alphabétique
        TriAlpha = sorted(TriAlpha, key=lambda genre: genre[0])

        oOutputParameterHandler = cOutputParameterHandler()
        for sTitle, sUrl in TriAlpha:
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)
        oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        oUtil = cUtil()
        sSearchText = oUtil.CleanName(sSearch.replace('%20', ' '))

        pdata = 'do=search&subaction=search&story=' + sSearchText.replace(' ', '+') + '&titleonly=3&catlist[]=1&catlist[]=37'

        oRequest = cRequestHandler(URL_SEARCH[0])
        # oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
        oRequest.addHeaderEntry('Origin', URL_MAIN)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequest.addParametersLine(pdata)
        sHtmlContent = oRequest.request()

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = 'mov clearfix.+?src="([^"]*)" *alt="([^"]*).+?link="([^"]+).+?(?:|bloc1">([^<]+).+?)(?:|bloc2">([^<]*).+?)'
    sPattern += 'ml-desc"> (?:([0-9]+)| )</div.+?Synopsis:.+?ml-desc">(.*?)</div'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()

        for aEntry in aResult[1]:
            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + aEntry[0]
            sTitle = aEntry[1].replace(' wiflix', '')
            sUrl = aEntry[2]
            sLang = aEntry[3]
            sQual = aEntry[4]
            sYear = aEntry[5]
            if sYear in sTitle:  # double affichage de l'année
                sTitle = re.sub('\(' + sYear + '\)', '', sTitle)

            # Filtre de recherche
            if sSearch and not oUtil.CheckOccurence(sSearchText, sTitle):
                continue

            # Nettoyage du synopsis
            sDesc = str(aEntry[6])
            sDesc = sDesc.replace('en streaming ', '')
            sDesc = sDesc.replace('Regarder film ' + sTitle + ';', '')
            sDesc = sDesc.replace('Regarder film ' + sTitle + ':', '')
            sDesc = sDesc.replace('Voir film ' + sTitle + ';', '')
            sDesc = sDesc.replace('Voir film ' + sTitle + ':', '')
            sDesc = sDesc.replace('Voir Film ' + sTitle + ':', '')
            sDesc = sDesc.replace('Voir film ' + sTitle + ' :', '')
            sDesc = sDesc.replace('Regarder ' + sTitle + ';', '')
            sDesc = sDesc.replace('Regarder ' + sTitle + ' :', '')
            sDesc = sDesc.replace('Regarder ' + sTitle + ':', '')
            sDesc = sDesc.replace('voir ' + sTitle + ';', '')
            sDesc = sDesc.replace('voir ' + sTitle + ':', '')
            sDesc = sDesc.replace('Voir ' + sTitle + ':', '')
            sDesc = sDesc.replace('Regarder film ', '')
            sDesc = sDesc.strip()

            sDisplayTitle = '%s [%s] (%s)' % (sTitle, sQual, sLang)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if 'serie-en-streaming' in sUrl:
                oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)
    else:
        oGui.addText(SITE_IDENTIFIER)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>([^<]+)</a> *</span>.*?<span class="pnext"><a href="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSeries(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        oUtil = cUtil()
        sSearchText = oUtil.CleanName(sSearch.replace('%20', ' '))
        sUrl = sSearch.replace(' ', '+')

        pdata = 'do=search&subaction=search&story=' + sUrl + '&titleonly=3&all_word_search=1&catlist[]=31&catlist[]=35'

        oRequest = cRequestHandler(URL_SEARCH[0])
        # oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry('Content-Type', 'application/json')
        oRequest.addParametersLine(pdata)
        sHtmlContent = oRequest.request()
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = 'mov clearfix.+?src="([^"]+)" *alt="([^"]+).+?data-link="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()

        for aEntry in aResult[1][::-1]:
            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + aEntry[0]

            sTitle = aEntry[1].replace('- Saison ', 'S').replace(' wiflix', '')
            
            # Filtre de recherche
            if sSearch and not oUtil.CheckOccurence(sSearchText, sTitle):
                continue
            
            sDisplayTitle = sTitle
            sUrl = aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', 'Page ' + sPaging, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '"clicbtn" rel="(ep\d+(vf|vs))" *>Episode (\d+)<'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    # Afficher le numero de l episode et la saison dans le titre
    # permet de marquer vu avec trakt automatiquement.
    sLang = ''

    sMovieTitle = sMovieTitle.replace('saison ', 'S')

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:

                if 'vs' in aEntry[1]:
                    sLang = ' (VOSTFR)'
                elif 'vf' in aEntry[1]:
                    sLang = ' (VF)'

                if 'epblocks' in aEntry[1]:
                    continue

                sTitle = '%s E%s' % (sMovieTitle, aEntry[2])
                sDisplayTitle = '%s %s' % (sTitle, sLang)
                oOutputParameterHandler.addParameter('siteUrl', '%s|%s' % (sUrl, aEntry[0]))
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
    
                oGui.addEpisode(SITE_IDENTIFIER, 'showHostersEpisode', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHostersEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl, sID = oInputParameterHandler.getValue('siteUrl').split('|')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sStart = '<div class="%s"' % sID
    sEnd = '</div>'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)


    sPattern = "onclick=\"loadVideo\('([^']+)"
    aResult = oParser.parse(sHtmlContent, sPattern)


    if aResult[0]:
        for aEntry in aResult[1]:
            sDisplayTitle = sMovieTitle
            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = "onclick=\"loadVideo\('([^']+)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:
            sDisplayTitle = sMovieTitle
            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
