#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress#, VSlog
import urllib

SITE_IDENTIFIER = 'planet_streaming'
SITE_NAME = 'Planet Streaming'
SITE_DESC = 'Films en Streaming complet  VF HD'

URL_MAIN = 'https://www.streaming-planet.net/'

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'regarder-film/', 'showMovies')
MOVIE_TOP = (URL_MAIN + 'exclu/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'xfsearch/hd/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_TOP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_TOP[1], 'Films (Top exclu)', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (HD)', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

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
    liste.append( ['HD/HQ', URL_MAIN + 'xfsearch/hd/'] )
    liste.append( ['Action', URL_MAIN + 'action/'] )
    liste.append( ['Animation', URL_MAIN + 'animation/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'arts-martiaux/'] )
    liste.append( ['Aventure', URL_MAIN + 'aventure/'] )
    liste.append( ['Biopic', URL_MAIN + 'biopic/'] )
    liste.append( ['Comédie', URL_MAIN + 'comedie/'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'comedie-dramatique/'] )
    liste.append( ['Comédie Musicale', URL_MAIN + 'comedie-musicale/'] )
    liste.append( ['Documentaire', URL_MAIN + 'documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'drame/'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'epouvante-horreur/'] )
    liste.append( ['Famille', URL_MAIN + 'famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'historique/'] )
    liste.append( ['Musical', URL_MAIN + 'musical/'] )
    liste.append( ['Policier', URL_MAIN + 'policier/'] )
    liste.append( ['Romance', URL_MAIN + 'romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'science-fiction/'] )
    liste.append( ['Thriller', URL_MAIN + 'thriller/'] )
    liste.append( ['Western', URL_MAIN + 'western/'] )
    #la suite fonctionne mais pas de menu sur le site
    liste.append( ['Espionnage', URL_MAIN + 'espionnage/'] )
    liste.append( ['Péplum', URL_MAIN + 'peplum/'] )
    liste.append( ['Divers', URL_MAIN + 'divers/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    Nextpagesearch = oInputParameterHandler.getValue('Nextpagesearch')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    bGlobal_Search = False

    if Nextpagesearch:
        sSearch = sUrl

    if sSearch:

        if URL_SEARCH[0] in sSearch:
            bGlobal_Search = True
            sSearch = sSearch.replace(URL_SEARCH[0], '')

        #sType = oInputParameterHandler.getValue('type')

        if Nextpagesearch:
            query_args = (('do', 'search'), ('subaction', 'search'), ('search_start', Nextpagesearch), ('story', sSearch))
        else:
            query_args = (('do', 'search'), ('subaction', 'search'), ('story', sSearch), ('titleonly', '3'))

        data = urllib.urlencode(query_args)

        oRequestHandler = cRequestHandler(URL_SEARCH[0])
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParametersLine(data)
        oRequestHandler.addParameters('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()

        #if (sType):
        #    if sType == 'serie':
        #        oRequestHandler.addParameters('catlist[]', '30')
        #    elif sType == 'film':
        #        oRequestHandler.addParameters('catlist[]', '3')

        sHtmlContent = oRequestHandler.request()

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="fullstream fullstreaming">\s*<img src="([^"]+)"[^<>]+alt="([^"]+)".+?<h3 class="mov-title"><a href="([^"]+)".+?<strong>(?:Qualité|Version)(.+?)<\/*strong>.+?xfsearch.+?">([^<]+)'
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
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            siteUrl = aEntry[2]
            sTitle = aEntry[1]
            sQual = cUtil().removeHtmlTags(aEntry[3])
            sQual = sQual.replace(':', '').replace(' ', '').replace(',', '/')
            sYear = aEntry[4]

            sDisplayTitle = '%s [%s] (%s)' % (sTitle, sQual, sYear)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        if sSearch:
            sPattern = '<a name="nextlink" id="nextlink" onclick="javascript:list_submit\(([0-9]+)\); return\(false\)" href="#">Suivant'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sSearch)
                oOutputParameterHandler.addParameter('Nextpagesearch', aResult[1][0])
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

        else:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if Nextpagesearch:
        oGui.setEndOfDirectory()

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^"]+)">Suivant &#8594;<\/a>'
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

    sPattern = '<i class="fa fa-play-circle-o"></i>([^<]+)</div>|<a href="([^"]+)" title="([^"]+)" target="seriePlayer"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
                # continue

            sHosterUrl = aEntry[1]

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
