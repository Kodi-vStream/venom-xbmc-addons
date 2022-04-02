# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager

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

URL_SEARCH = (URL_MAIN, 'showSearch')
URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_SERIES = ('', 'showSeries')
FUNCTION_SEARCH = 'showSearch'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://film')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://serie')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Séries', 'search.png', oOutputParameterHandler)

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
    if sSearchText != False:

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

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)
    TriAlpha = []
    if aResult[0] is True:
        for aEntry in aResult[1]:
            sUrl = URL_MAIN + aEntry[0]
            sTitle = aEntry[1].capitalize()
            TriAlpha.append((sTitle, sUrl))

        # Trie des genres par ordre alphabétique
        TriAlpha = sorted(TriAlpha, key=lambda genre: genre[0])

        oOutputParameterHandler = cOutputParameterHandler()
        for sTitle, sUrl in TriAlpha:
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')

        pdata = 'do=search&subaction=search&story=' + sUrl + '&titleonly=3&all_word_seach=1&catlist[]=1'

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

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

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

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>([^<]+)</a> *</span>.*?<span class="pnext"><a href="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
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
        sUrl = sSearch.replace(' ', '+')

        pdata = 'do=search&subaction=search&story=' + sUrl + '&titleonly=3&all_word_seach=1&catlist[]=31'

        oRequest = cRequestHandler(URL_SEARCH[0])
        # oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
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

    sPattern = 'mov clearfix.+?src="([^"]+)" *alt="([^"]+).+?data-link="([^"]+).+?block-sai">([^<]+).+?ml-desc">(.+?)</div>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + aEntry[0]

            sTitle = aEntry[1].replace('- Saison', 'saison').replace(' wiflix', '')
            sLang = re.sub('Saison \d+', '', aEntry[3]).replace(' ', '')
            sDisplayTitle = ('%s (%s)') % (sTitle, sLang)
            sUrl = aEntry[2]
            sDesc = aEntry[4]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
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
    sPattern = '<div class="(ep.+?)"|<a href="([^"]+)"[^><]+target="x_player"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    # Afficher le numero de l episode et la saison dans le titre
    # permet de marquer vu avec trakt automatiquement.
    ep = 0
    sLang = ''

    if aResult[0] is True:
        for aEntry in aResult[1]:
            if aEntry[0]:

                if 'vs' in aEntry[0]:
                    sLang = ' (VOSTFR)'
                elif 'vf' in aEntry[0]:
                    sLang = ' (VF)'

                if 'epblocks' in aEntry[0]:
                    continue

                ep = aEntry[0].replace('ep', 'Episode ').replace('vs', '').replace('vf', '')

            if aEntry[1]:
                sTitle = sMovieTitle + ' ' + ep + sLang
                sHosterUrl = aEntry[1].replace('/vd.php?u=', '')
                if 'players.wiflix.' in sHosterUrl:
                    oRequestHandler = cRequestHandler(sHosterUrl)
                    oRequestHandler.request()
                    sHosterUrl = oRequestHandler.getRealUrl()

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster != False:
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sTitle)
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
    sPattern = '<a href="\/vd.php\?u=([^"]+)"[^<>]+target="x_player_wfx"><span>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]  # .replace('/wiflix.cc/', '')
            if 'wiflix.' in sHosterUrl:
                oRequestHandler = cRequestHandler(sHosterUrl)
                oRequestHandler.request()
                sHosterUrl = oRequestHandler.getRealUrl()
            else:
                sHosterUrl = aEntry[0].replace('/wiflix.cc/', '')
            sLang = aEntry[1].replace('2', '').replace('3', '')
            if 'Vost' in aEntry[1]:
                sDisplayTitle = ('%s (%s)') % (sMovieTitle, sLang)
            else:
                sDisplayTitle = sMovieTitle
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
