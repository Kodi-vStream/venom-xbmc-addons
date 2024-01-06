# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons.
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'blueseries'
SITE_NAME = 'BLUEseries'
SITE_DESC = 'Streaming des séries'

URL_MAIN = URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SERIE_NEWS = (URL_MAIN + 'regarder-series/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_ANNEES = (URL_MAIN, 'showSerieYears')
SERIE_LIST = (URL_MAIN, 'showSerieAlpha')
SERIE_VOSTFRS = (URL_MAIN + 'regarder-series/series-vostfr/', 'showMovies')

URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showMovies')
URL_SEARCH_SERIES = ('', 'showMovies')

# recherche utilisée quand on n'utilise pas le globale
MY_SEARCH_SERIES = (True, 'showSearch')

# Menu GLOBALE HOME
SERIE_SERIES = (True, 'showMenuTvShows')


def load():
    showMenuTvShows()

def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_SERIES[1], 'Recherche Séries ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Série (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Série (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSerieAlpha():
    import string

    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    listalpha = ['1']
    listalpha.extend(list(string.ascii_lowercase))
    for alpha in listalpha:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'catalog/' + alpha + '&cat=2')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + str(alpha).upper() + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieGenres():
    oGui = cGui()
    listegenre = [['Action', 'action_s'], ['Animation', 'animation_s'], ['Aventure', 'aventure_s'], ['Biopic', 'biopic-s'], ['Comédie', 'comedie_s'],
             ['Documentaire', 'documentaire-s'], ['Drame', 'drame_s'], ['Famille', 'famille-s'],
             ['Fantastique', 'fantastique_s'], ['Guerre', 'guerre_s'], ['Historique', 'historique_s'], ['Horreur', 'horreur_s'],
             ['Judiciaire', 'judiciare-s'], ['Musique', 'musical_s'], ['Policier', 'policier_s'], ['Romance', 'romance_s'],
             ['Science-Fiction', 'science_fiction_s'], ['Thriller', 'thriller_s'],['western', 'western_s']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in listegenre:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'regarder-series/' + sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieYears():
    oGui = cGui()
#    import datetime

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1930, 2022)):  #int(datetime.datetime.now().year) + 1)):
        sYear = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'annee/' + sYear  + '&cat=2')
        oOutputParameterHandler.addParameter('sYear', sYear)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        oUtil = cUtil()
        sSearchText = oUtil.CleanName(sSearch)
        
        sSearch = sSearch.replace(' ', '+').replace('%20', '+')
        pdata = 'do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=' + sSearch
        oRequest = cRequestHandler(URL_SEARCH[0])
        oRequest.setRequestType(1)
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

    # thumb url title
    sPattern = '<article class="movie-box.+?img src="([^"]+)".+?a href="([^"]+)" title="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[1]
            sThumb = aEntry[0]
            if 'http' not in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb
            sTitle = aEntry[2]

            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue  # Filtre de recherche

            sDisplayTitle = sTitle

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            
            oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    else:
        oGui.addText(SITE_IDENTIFIER)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()

    sPattern = 'navigation.+?<span>\d+</span> <a href="([^"]+).+?>([^<]+)</a></div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'
    
def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="description">.+?<p>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sDesc = ''
    if aResult[0]:
        sDesc = aResult[1][0]

    sPattern = '<span class="part12">([^<]*)</span>.+?<div class="spoiler1-body">.+?<a\s+href="([^"]+)/'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in reversed(aResult[1]):

            sUrl2 = aEntry[1] + '.html'
            sSaison = aEntry[0]  # SAISON 2

            sTitle = ("%s %s") % (sMovieTitle, sSaison)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        oGui.addText(SITE_IDENTIFIER)

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

    sStart = 'class="saisontab'
    sEnd = 'class="clear'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+).+?<span class="name">(.*?)</span>.*?<span class="arrow-right"></span>(.*?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sEpisode = aEntry[1] + '  ' + aEntry[2].replace('é', 'e').strip() # épisode 2
            if 'http' not in sUrl2:
                sUrl2 = URL_MAIN[:-1] + sUrl2
            sTitle = sMovieTitle + ' ' + sEpisode

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addEpisode(SITE_IDENTIFIER, 'showSerieLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        oGui.addText(SITE_IDENTIFIER)

    oGui.setEndOfDirectory()


def showSerieLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    cook = oRequestHandler.GetCookies()

    sPattern = "class=\"lien.+?playEpisode.+?\'([^\']*).+?'([^\']*)"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            videoId = aEntry[0]
            xfield = aEntry[1]
            hosterName = xfield.replace('_', ' ').capitalize().replace('-vf', ' (VF)').replace('-vostfr', ' (VOSTFR)')

            postdata = 'id=' + videoId + '&xfield=' + xfield + '&action=playEpisode'
            sUrl2 = URL_MAIN + 'engine/ajax/Season.php'

            sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sTitle, hosterName)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('cook', cook)
            oOutputParameterHandler.addParameter('postdata', postdata)

            oGui.addLink(SITE_IDENTIFIER, 'showSerieHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    referer = oInputParameterHandler.getValue('referer')
    # cook = oInputParameterHandler.getValue('cook')
    postdata = oInputParameterHandler.getValue('postdata')

    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    # oRequest.addHeaderEntry('Cookie', cook) # pas besoin ici mais besoin pour les films
    oRequest.addParametersLine(postdata)
    sHtmlContent = oRequest.request()

    oParser = cParser()
    sPattern = '<iframe src=\'([^\']+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sHosterUrl = aResult[1][0]
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
