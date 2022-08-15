# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 44 https://funeralforamanga.fr/
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress


SITE_IDENTIFIER = 'funeralforamanga'
SITE_NAME = 'Funeral for a manga'
SITE_DESC = 'animés en streaming'

URL_MAIN = 'https://funeralforamanga.fr/'

ANIM_ANIMS = ('http://', 'load')

ANIM_NEWS = (URL_MAIN + 'videos?sk=c&unlicenced=1&p=1', 'showMovies')
ANIM_POPULAR = (URL_MAIN + 'videos?sk=b&unlicenced=1&p=1&', 'showMovies')
ANIM_ANNEES = (True, 'showAllYears')
ANIM_ALPHA = (True, 'showAllAlpha')
ANIM_GENRES = (True, 'showAllGenre')
ANIM_VFS = (URL_MAIN + 'videos?sk=c&unlicenced=1&lang=vf&p=1', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'videos?sk=c&unlicenced=1&lang=vostfr&p=1', 'showMovies')

ANIM_SERIE_NEWS = (URL_MAIN + 'videos?sk=c&filter=serie&unlicenced=1&p=1', 'showMovies')
ANIM_SERIE_POPULAR = (URL_MAIN + 'videos?sk=b&filter=serie&unlicenced=1&p=1', 'showMovies')
ANIM_SERIE_ANNEES = (True, 'showSerieYears')
ANIM_SERIE_ALPHA = (True, 'showSerieAlpha')
ANIM_SERIE_GENRES = (True, 'showSerieGenre')
ANIM_SERIE_VFS = (URL_MAIN + 'videos?sk=c&filter=serie&unlicenced=1&lang=vf&p=1', 'showMovies')
ANIM_SERIE_VOSTFRS = (URL_MAIN + 'videos?sk=c&filter=serie&unlicenced=1&lang=vostfr&p=1', 'showMovies')

ANIM_MOVIE_NEWS = (URL_MAIN + '/videos?sk=c&filter=movie&unlicenced=1&p=1', 'showMovies')
ANIM_MOVIE_POPULAR = (URL_MAIN + '/videos?sk=b&filter=movie&unlicenced=1&p=1', 'showMovies')
ANIM_MOVIE_ANNEES = (True, 'showMovieYears')
ANIM_MOVIE_ALPHA = (True, 'showMovieAlpha')
ANIM_MOVIE_GENRES = (True, 'showMovieGenre')
ANIM_MOVIE_VFS = (URL_MAIN + 'videos?sk=c&filter=movie&unlicenced=1&lang=vf&p=1', 'showMovies')
ANIM_MOVIE_VOSTFRS = (URL_MAIN + 'videos?sk=c&filter=movie&unlicenced=1&lang=vostfrp=1', 'showMovies')

URL_SEARCH_ANIMS = (URL_MAIN + 'videos?unlicenced=1&q=', 'showMovies')
URL_SEARCH = (URL_MAIN + 'videos?unlicenced=1&q=', 'showMovies')
URL_INTERNALSEARCH_SERIES = (URL_MAIN + 'videos?filter=serie&unlicenced=1&q=', 'showMovies')
URL_INTERNALSEARCH_MOVIES = (URL_MAIN + 'videos?filter=movie&unlicenced=1&q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'siteUrl')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Films & Séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Récents)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_POPULAR[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_POPULAR[1], 'Animés (Populaires)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANNEES[1], 'Animés (Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ALPHA[1], 'Animés (Alpha)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'siteUrl')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSerie', 'Recherche Séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_SERIE_NEWS[1], 'Animés Séries (Récents)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_SERIE_POPULAR[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_SERIE_POPULAR[1], 'Animés Séries (Populaires)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_SERIE_ANNEES[1], 'Animés Séries (Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_SERIE_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_SERIE_ALPHA[1], 'Animés Séries (Alpha)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_SERIE_GENRES[1], 'Animés Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_SERIE_VOSTFRS[1], 'Animés Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_SERIE_VFS[1], 'Animés Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'siteUrl')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovie', 'Recherche Films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_MOVIE_NEWS[1], 'Animés Films (Récents)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIE_POPULAR[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_MOVIE_POPULAR[1], 'Animés Films (Populaires)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_MOVIE_ANNEES[1], 'Animés Films (Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIE_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_MOVIE_ALPHA[1], 'Animés Films (Alpha)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_MOVIE_GENRES[1], 'Animés Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_MOVIE_VOSTFRS[1], 'Animés Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_MOVIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_MOVIE_VFS[1], 'Animés Films (VF)', 'vf.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieAlpha():
    showAllAlpha('movie')


def showSerieAlpha():
    showAllAlpha('serie')


def showAllAlpha(sfilter=''):
    oGui = cGui()
    import string
    sAlpha = string.ascii_lowercase
    listalpha = list(sAlpha)

    url1 = 'videos?sk=a&alpha='
    url2 = '&filter=' + sfilter + '&unlicenced=1&p=1'

    oOutputParameterHandler = cOutputParameterHandler()
    for alpha in listalpha:
        sTitle = str(alpha).upper()
        sUrl = URL_MAIN + url1 + alpha + url2 
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
    showAllYears('movie')


def showSerieYears():
    showAllYears('serie')


def showAllYears(sfilter=''):
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1983, 2022)):
        sYear = str(i)
        url1 = 'videos?sk=c&filter=' + sfilter + '&unlicenced=1&aired-min=' + sYear + '&aired-max=' + sYear + '&p=1'
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + url1)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showMovieGenre():
    showAllGenre('movie')


def showSerieGenre():
    showAllGenre('serie')


def showAllGenre(sfilter=''):
    oGui = cGui()

    listegenre = ['action', 'aventure', 'comedie', 'drame', 'fantastique', 'horreur', 'policier', 'romance',
                  'science-fiction', 'sexy', 'sport']

    url1 = URL_MAIN + 'videos?sk=c&filter=' + sfilter + '&unlicenced=1&genres='
    url2 = '&p=1'
    oOutputParameterHandler = cOutputParameterHandler()
    for igenre in listegenre:
        sTitle = igenre.capitalize()
        sUrl = url1 + igenre + url2
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchMovie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_INTERNALSEARCH_MOVIES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchSerie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_INTERNALSEARCH_SERIES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovies(sSearch=''):

    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sSearch:
        sUrl = sSearch.replace(' ', '+')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = "col-sm-4 col-md-3\">.+?href=\"([^\"]+).+?url\(\'([^']+).+?<span class=.anime-label.+?uppercase.>([^<]+).+?anime-header.>([^<]+)"

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

            sUrl2 = URL_MAIN[:-1] + aEntry[0]
            sThumb = URL_MAIN[:-1] + aEntry[1]
            sType = aEntry[2] 
            sTitle = aEntry[3] 
            sDisplayTitle = sTitle + ' [' + sType + ']'

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addAnime(SITE_IDENTIFIER, 'showEpisodesxMovies', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent, sUrl)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent, sUrl):
    sNumberMax = ''
    sPattern = '"text-muted">page.+?sur\s*(\d+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sNumberMax = aResult[1][0]

    sPattern = '&p=(\d+)'
    aResult = oParser.parse(sUrl, sPattern)
    if (aResult[0] == True):
        sNumberCurrent = aResult[1][0]
        iNumberCurrent = int(sNumberCurrent)
        iNumberNext = iNumberCurrent + 1
        sNumberNext = str(iNumberNext)
        sNextPage = sUrl.replace('&p=' + sNumberCurrent, '&p=' + sNumberNext)
        if sNumberMax:
            if int(sNumberMax) >= iNumberNext:
                return sNextPage, sNumberNext + '/' + sNumberMax
        else:
            return sNextPage, sNumberNext
    return False, False


def showEpisodesxMovies():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    sPattern = '<h4>Intrigue<.h4>(.+?)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis : ', cleanDesc(aResult[1][0]))

    if 'aucune vidéo disponible' in sHtmlContent:
        oGui.addText(SITE_IDENTIFIER, 'Aucune video disponible')
        oGui.setEndOfDirectory()
        return

    sHtmlContent1 = oParser.abParse(sHtmlContent, '<h4 class="list-group-item-heading">', '<div id="footer')

    sPattern = '<h4 class="list-group-item-heading">([^<]+)<.h4>|<a href="([^"]+).+?(?:group-item-text">|>)([^<]+)(?:<.p>|<.a>)'
    sPattern = sPattern
    aResult = oParser.parse(sHtmlContent1, sPattern)

    sLang = ''
    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                sLang = aEntry[0]
                continue

            if sLang:
                sUrl = URL_MAIN[:-1] + aEntry[1]
                sTitle = sMovieTitle + ' ' + aEntry[2].replace('Épisode', 'Episode')

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sLang', sLang)
                oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="subsection">.+?label-default">\D*(\d+)([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sId = aEntry[0]
            sHost = aEntry[1].replace(' ', '').replace('-', '')
            sHost = re.sub('\.\w+', '', sHost)
            pdata = 'id=' + sId
            sMovieTitle = re.sub('\[.+?\]', '', sMovieTitle)
            sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
            sUrl2 = URL_MAIN + 'remote/ajax-load_video'

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oOutputParameterHandler.addParameter('siteRefer', sUrl)
            oOutputParameterHandler.addParameter('pdata', pdata)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    pdata = oInputParameterHandler.getValue('pdata')
    siteRefer = oInputParameterHandler.getValue('siteRefer')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', siteRefer)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addParametersLine(pdata)
    sHtmlContent = oRequestHandler.request()
 
    sPattern = 'frame.+?src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sHosterUrl = aResult[1][0]
        if 'https:' not in sHosterUrl:
            sHosterUrl = 'https:' + sHosterUrl
        # VSlog(sHosterUrl)
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def cleanDesc(sDesc):
    oParser = cParser()
    sPattern = '(<.+?>)'
    aResult = oParser.parse(sDesc, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sDesc = sDesc.replace(aEntry, '')
    return sDesc
