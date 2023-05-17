# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'kstreamingserie'
SITE_NAME = 'K Streaming Série'
SITE_DESC = 'Médiathèque de chaînes officielles'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

SERIE_SERIE = (True, 'load')
SERIE_NEWS = (URL_MAIN, 'showSeries')
# SERIE_GENRES = (True, 'showGenres')
SERIE_LIST = (True, 'showList')

URL_SEARCH = (URL_MAIN + '?s=', 'showSeries')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showSeries')
FUNCTION_SEARCH = 'showSeries'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Afro', 'afro'], ['Animation', 'animation'], ['Arts Martiaux', 'art-martiaux'],
             ['Aventure', 'aventure'], ['Biographique', 'biographique'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie dramatique', 'comedie-dramatique'], ['Comédie musicale', 'comedie-musicale'], ['Crime', 'crime'],
             ['Divers', 'divers'], ['Documentaire', 'documentaire'], ['Drame', 'drame'],
             ['Epouvante-horreur', 'epouvante-horreur'], ['Erotique', 'erotique'], ['Espionnage', 'espionnage'],
             ['Famille', 'famille'], ['Fantastique', 'fantastique'], ['Film-musical', 'film-musical'],
             ['Guerre', 'guerre'], ['Historique', 'historique'], ['Horreur', 'horreur'], ['Judiciaire', 'judiciaire'],
             ['Musical', 'musique'], ['Mystère', 'mystere'], ['Non classé', 'non-classe'], ['Policier', 'policier'],
             ['Romance', 'romance'], ['Science fiction', 'science-fiction'], ['Slasher', 'slasher'],
             ['Sport', 'sport-event'], ['Terreur', 'thriller/terreur'], ['Thriller', 'thriller'], ['Western', 'western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showList():
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    # sHtmlContent = oParser.abParse(sHtmlContent, '<h1>Listes des séries:</h1>', 'Copyright')

    sPattern = 'class="cat-item cat-item-.+?"><a href="([^"]+)">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:

        # series = []

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1]
            # series.append((sTitle, sUrl))

        # Trie des séries par ordre alphabétique
        # series = sorted(series, key=lambda serie: serie[0])

        # for sTitle, sUrl:
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showSaisons', sTitle, 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeries(sSearch=''):
    oGui = cGui()
    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    if 'Récemment ajoutées' in sHtmlContent:
        sStart = 'Récemment ajoutées'
        sEnd = 'Séries streaming les plus populaires'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = 'center-icons".+?src="([^"]+)" alt="([^"]+).+?href="([^"]+).+?(?:|story\'>([^<]+).+?)movie-cast'
    if sSearch:
        sPattern = 'center-icons".+?src="([^"]+)" alt="([^"]+).+?href="([^"]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            sTitle = re.sub('\(\d{4}\)', '', aEntry[1])
            sUrl = aEntry[2]

            if sSearch:     # Filtre de recherche
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            sDesc = ''  # absente pour la recherche
            if len(aEntry) > 3:
                sDesc = aEntry[3]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>([^<]+)</a></div><div class="naviright"><a href="([^"]+?)" >Suivant'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('page.([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'movie-poster.+?href="([^"]+)".+?src="([^"]+)" alt="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in reversed(aResult[1]):
            sUrl = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2].replace(' Streaming', '')

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    try:
        sPattern = 'line-clamp line-hide">(.+?)</div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0].replace('<br />', '').replace('</div>', '')
    except:
        pass

    # recuperation du hoster de base
    sPattern = '<div class="keremiya_part"> <span>([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    ListeUrl = []
    if aResult[0]:
        ListeUrl = [(sUrl, aResult[1][0])]

    # Recuperation des suivants
    sPattern = '<a href="([^"]+)" class="post-page-numbers"><span>([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    ListeUrl = ListeUrl + aResult[1]

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in ListeUrl:
            sUrl = aEntry[0]
            sTitle = sMovieTitle + ' Episode' + aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    # si un seul episode
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle + ' episode 1')
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sMovieTitle + ' episode 1', '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<h3>.+?(VF|VOSTFR)\s*<\/h3>\s*<p><\/p>|<iframe.+?src="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            # langue
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            # hote
            else:
                sHosterUrl = aEntry[1]

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
