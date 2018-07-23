#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#Venom.
#site HS le 03/06/18
return False
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
#from resources.lib.util import cUtil
from resources.lib.config import cConfig
import re, urllib

SITE_IDENTIFIER = 'tv_streaming_ch'
SITE_NAME = 'Tv-streaming'
SITE_DESC = 'Films/Séries/Animés/Documentaires/ReplayTV en streaming'

URL_MAIN = 'http://www.streamania.xyz/'

MOVIE_NEWS = (URL_MAIN + 'category/films-vf/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'category/films-vf/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_NEWS = (URL_MAIN + 'category/series-tv', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'category/series-tv', 'showMovies')
SERIE_VFS = (URL_MAIN + 'category/series-tv/serie-vf/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'category/series-tv/serie-vostfr/', 'showMovies')

ANIM_ANIMS = (URL_MAIN + 'category/manga/', 'showMovies')
ANIM_VFS = (URL_MAIN + 'category/manga/manga-vf/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'category/manga/manga-vostfr/', 'showMovies')
ANIM_ENFANTS = (URL_MAIN + 'category/dessin-anime/', 'showMovies')

DOC_NEWS = (URL_MAIN + 'category/television/documentaire/', 'showMovies')
DOC_DOCS = ('http://', 'load')

SPORT_SPORTS = (URL_MAIN + 'category/sport/', 'showMovies')

REPLAYTV_GENRES = (True, 'ReplayTV')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'category/sitcoms/')
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Sitcoms', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ENFANTS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ENFANTS[1], 'Dessins animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_GENRES[1], 'Replay TV (Genres)', 'replay.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1], 'Sport', 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + urllib.quote(sSearchText)
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def ReplayTV():
    oGui = cGui()

    liste = []
    liste.append( ['Concert', URL_MAIN + 'category/television/concert/'] )
    liste.append( ['Documentaires', URL_MAIN + 'category/television/documentaire/'] )
    liste.append( ['Emissions TV', URL_MAIN + 'category/television/emission-tv/'] )
    liste.append( ['Karaoké', URL_MAIN + 'karaoke/'] )
    liste.append( ['One Man Show', URL_MAIN + 'television/one-man-sohw/'] )
    liste.append( ['Rétro', URL_MAIN + 'category/television/retro/'] )
    liste.append( ['Rétro Souvenir', URL_MAIN + 'category/television/retro-souvenir/'] )
    liste.append( ['TV réalité', URL_MAIN + 'television/tv-realite/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'category/films-vf/action-films/'] )
    liste.append( ['Animation', URL_MAIN + 'category/films-vf/animation-films/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'category/films-vf/arts-martiaux-films/'] )
    liste.append( ['Aventure', URL_MAIN + 'category/films-vf/aventure-films/'] )
    liste.append( ['Comédie', URL_MAIN + 'category/films-vf/comedie-films/'] )
    liste.append( ['Disney', URL_MAIN + 'category/dessin-anime/disney/'] )
    liste.append( ['Drame', URL_MAIN + 'category/films-vf/drame-films/'] )
    liste.append( ['Epouvante-Horreur', URL_MAIN + 'category/films-vf/epouvante-horreur/'] )
    liste.append( ['Espionnage', URL_MAIN + 'category/films-vf/espionnage/'] )
    liste.append( ['Famille', URL_MAIN + 'category/films-vf/famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'category/films-vf/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'category/films-vf/guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'category/films-vf/historique-streaming/'] )
    liste.append( ['Musical', URL_MAIN + 'category/films-vf/musical/'] )
    liste.append( ['Policier', URL_MAIN + 'category/films-vf/policier/'] )
    liste.append( ['Romance', URL_MAIN + 'category/films-vf/romance/'] )
    liste.append( ['Science-fiction', URL_MAIN + 'category/films-vf/science-fiction/'] )
    liste.append( ['Sentaï', URL_MAIN + 'sentai/'] )
    liste.append( ['Téléfilms', URL_MAIN + 'category/films-vf/telefilms/'] )
    liste.append( ['Thriller', URL_MAIN + 'category/films-vf/thriller/'] )
    liste.append( ['Western', URL_MAIN + 'western/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oParser = cParser()
    oGui = cGui()
    if sSearch:
      sUrl = sSearch

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div.*?class="moviefilm">.+?href="([^<]+)".*?img src="([^<]+)" alt="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl = str(aEntry[0])
            sThumb = str(aEntry[1])
            sTitle = str(aEntry[2])


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '- Saison' in sTitle:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, '', sThumb, '', oOutputParameterHandler)
            elif '-saison-' in sUrl or '/manga' in sUrl or '/sentai/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sTitle, '', sThumb, '', oOutputParameterHandler)
            elif '/films' in sUrl in sUrl or '/sport/' in sUrl or '/western/' in sUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMisc(SITE_IDENTIFIER, 'showSeries', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="nextpostslink" rel="next" href="(.+?)">(?:»|&raquo;)<\/a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSeries(sLoop = False):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    if sUrl.endswith('/'):
        sUrl = sUrl + '100/'
    else:
        sUrl = sUrl + '/100/'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a *href="([^<]+)"><span>.+?<font class="">(.+?)<\/font><\/font>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    #astuce en cas d'episode unique
    if (aResult[0] == False) and (sLoop == False):
        showHosters(True)
        return

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            episode = ''
            if aEntry[1]:
                episode = aEntry[1] + ' '

            sUrl = str(aEntry[0])
            sTitle =  episode + sMovieTitle

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHosters(sLoop = False):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.replace('facebook', '<>')

    sPattern = '<iframe.+?src="(http[^<>]+?)" [^<>]+?><\/iframe>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if 'dailymotion' in aEntry:
                continue

            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
