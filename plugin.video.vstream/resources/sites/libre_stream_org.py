#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

#disabled 15/02
return False

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress#,VSlog

SITE_IDENTIFIER = 'libre_stream_org'
SITE_NAME = 'Libre-Streaming'
SITE_DESC = 'Films & Séries en streaming'

URL_MAIN = 'http://ls-streaming.org/'

MOVIE_MOVIE = (URL_MAIN + 'films/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_QLT = (True, 'showQlt')

SERIE_SERIES = (URL_MAIN + 'series/', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
#SERIE_LIST = (URL_MAIN + 'liste-des-series/', 'AlphaSearch')
SERIE_VFS = (URL_MAIN + 'series/version-francaise/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'series/vostfr/', 'showMovies')

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?q=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_QLT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_QLT[1], 'Films (Qualités)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    #En panne au 14/06
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    #oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

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

    liste = []
    liste.append( ['Action', URL_MAIN + 'films/action/'] )
    liste.append( ['Animation', URL_MAIN + 'films/animation/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'films/arts-martiaux/'] )
    liste.append( ['Aventure', URL_MAIN + 'films/aventure/'] )
    liste.append( ['Biopic', URL_MAIN + 'films/biopic/'] )
    liste.append( ['Comédie', URL_MAIN + 'films/comedie/'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'films/comedie-dramatique/'] )
    liste.append( ['Comédie Musicale', URL_MAIN + 'films/comedie-musicale/'] )
    liste.append( ['Disney', URL_MAIN + 'films/disney/'] )
    liste.append( ['Divers', URL_MAIN + 'films/divers/'] )
    liste.append( ['Documentaire', URL_MAIN + 'films/documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'films/drame/'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'films/horreur/'] )
    liste.append( ['Espionnage', URL_MAIN + 'films/espionnage/'] )
    liste.append( ['Famille', URL_MAIN + 'films/famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'films/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'films/guerre/'] )
    liste.append( ['Historiques', URL_MAIN + 'films/historique/'] )
    liste.append( ['Horreur', URL_MAIN + 'films/horreur/'] )
    liste.append( ['Manga', URL_MAIN + 'films/manga/'] )
    liste.append( ['Musicale', URL_MAIN + 'films/musical/'] )
    liste.append( ['Policier', URL_MAIN + 'films/policier/'] )
    liste.append( ['Romance', URL_MAIN + 'films/romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'films/science-fiction/'] )
    liste.append( ['Spectacles', URL_MAIN + 'films/spectacles/'] )
    liste.append( ['Thriller', URL_MAIN + 'films/triller/'] )
    liste.append( ['Western', URL_MAIN + 'films/western/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showQlt():
    oGui = cGui()

    liste = []
    liste.append( ['HD', URL_MAIN + 'films-hd/'] )
    liste.append( ['DvdRip', URL_MAIN + 'quality/dvdrip/'] )
    liste.append( ['BdRip', URL_MAIN + 'quality/bdrip/'] )
    liste.append( ['R5', URL_MAIN + 'quality/R5/'] )
    liste.append( ['Cam Rip', URL_MAIN + 'quality/camrip/'] )
    liste.append( ['TS', URL_MAIN + 'quality/ts/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def AlphaSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    progress_ = progress().VScreate(SITE_NAME)

    for i in range(0, 36) :
        progress_.VSupdate(progress_, 36)
        if progress_.iscanceled():
            break

        if (i < 10):
            sTitle = chr(48 + i)
        else:
            sTitle = chr(65 + i -10)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + sTitle.lower() + '.html')
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'AlphaDisplay', '[COLOR teal] Lettre [COLOR red]' + sTitle + '[/COLOR][/COLOR]', 'listes.png', oOutputParameterHandler)

    progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def AlphaDisplay():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a href="([^<>"]+?)">([^<>"]+?)<\/a><br \/>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addDir(SITE_IDENTIFIER, 'seriesHosters', sTitle, 'az.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

        oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
      sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="libre-movie.+?data-src="([^"]+)".+?title="([^"]+)".+?onclick="window.location.href=\'(.+?)\'">.+?class="maskhr">Synopsis.+?</span>(.+?)</div>'
    if '/films' in sUrl:
        sPattern = sPattern + '.+?<div class="maskquality (.+?)">'
    if '/series' in sUrl:
        sPattern = sPattern + '.+?>Séries</a>.+?<a href=".+?">([^<]+)</a>'

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

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), aEntry[1]) == 0:
                    continue

            sTitle = aEntry[1].replace(' - Saison', ' Saison')
            sUrl2 = aEntry[2]
            sDesc = aEntry[3]
            sThumb = aEntry[0]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            if not '/series/' in sUrl and not '/films/' in sUrl:
                sDisplayTitle = sTitle

            if '/films/' in sUrl:
                sQual = aEntry[4]
                #on supprime [VOSTFR], [HD 720p] et DVDRIP du titre car affiche en tant que qualite sinon doublons
                sMovieTitle = sTitle.replace('[VOSTFR]', '').replace('[HD 720p]', '').replace('DVDRIP ', '')
                sDisplayTitle = sMovieTitle + ' [' + sQual + ']'

            if '/series/' in sUrl:
                if not '/vostfr/' in sUrl and not '/version-francaise/' in sUrl:
                    sLang = aEntry[4]
                    sLang = sLang.replace('Version Française', 'VF')
                    sDisplayTitle = sTitle + ' (' + sLang + ')'
                else:
                    sDisplayTitle = sTitle

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/series/' in sUrl or '-saison-' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^"]+)"><i class="fa fa-angle-right"></i></a>'
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
    sHtmlContent = sHtmlContent.replace('http://creative.rev2pub.com', '')

    sPattern = '<iframe.+?src=[\'"]([^<>\'"]+?)[\'"]'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if '/player' in aEntry or 'lecteur' in aEntry:
                sTitle = sMovieTitle + ' (Redirection)'
                sUrl1 = aEntry.replace('player.full-stream.co/player?id=', 'full-stream.co/player.php?id=')
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl1)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb )
                oGui.addLink(SITE_IDENTIFIER, 'redirectHosters', sTitle, sThumb, '', oOutputParameterHandler)

            else:
                sHosterUrl = aEntry
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def seriesHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="e-number">.+?<iframe src="([^"]+)".+?class="episode-id">([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if '/player' in aEntry[0] or 'full-stream.' in aEntry[0] or 'lecteur' in aEntry[0]:
                sTitle = sMovieTitle + aEntry[1] + '(Redirection)'
                sUrl1 = aEntry[0].replace('player.full-stream.co/player?id=', 'full-stream.co/player.php?id=')
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl1)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb )
                oGui.addLink(SITE_IDENTIFIER, 'redirectHosters', sTitle, sThumb, '', oOutputParameterHandler)

            else:
                sTitle = sMovieTitle + ' ' + aEntry[1]
                sHosterUrl = aEntry[0]
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def redirectHosters():
    oGui = cGui()
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:69.0) Gecko/20100101 Firefox/69.0'
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequest = cRequestHandler(sUrl)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.request()

    sHosterUrl = oRequest.getRealUrl()

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
