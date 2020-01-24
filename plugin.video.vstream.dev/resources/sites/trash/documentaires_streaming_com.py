#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
return false
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'documentaires_streaming_com'
SITE_NAME = 'Documentaires Streaming'
SITE_DESC = 'replay tv, documentaire, reportage'

URL_MAIN = 'http://voir.documentaires-streaming.com/'

DOC_NEWS = (URL_MAIN + 'category/documentaire/', 'showMovies')
DOC_DOCS = ('http://', 'load')
DOC_GENRES = (True, 'showDocuGenres')

REPLAYTV_NEWS = (URL_MAIN + 'category/replay_tv/', 'showMovies')
REPLAYTV_REPLAYTV = ('http://', 'load')
REPLAYTV_GENRES = (True, 'showReplayGenres')

REPORTAGE_NEWS = (URL_MAIN + 'category/reportages/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showDocuGenres', 'Documentaires (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Replay TV (chaines)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPORTAGE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPORTAGE_NEWS[1], 'Reportages', 'doc.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showDocuGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Histoires', URL_MAIN + 'category/histoires/'] )
    liste.append( ['Nature, Animaux', URL_MAIN + 'category/nature_animaux/'] )
    liste.append( ['Paranormal', URL_MAIN + 'category/paranormal/'] )
    liste.append( ['Politique, Société', URL_MAIN + 'category/politique-societe/'] )
    liste.append( ['Science', URL_MAIN + 'category/science/'] )
    liste.append( ['Société', URL_MAIN + 'documentaire/societe/'] )
    liste.append( ['Sport', URL_MAIN + 'category/sport/'] )
    liste.append( ['Voiture', URL_MAIN + 'category/voiture/'] )
    liste.append( ['Voyage', URL_MAIN + 'category/voyage-2/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showReplayGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Arte', URL_MAIN + 'category/replay_tv/arte-replay_tv/'] )
    liste.append( ['France 2', URL_MAIN + 'category/replay_tv/france_2/'] )
    liste.append( ['France 3', URL_MAIN + 'category/replay_tv/france_3/'] )
    liste.append( ['France 5', URL_MAIN + 'category/replay_tv/france_5/'] )
    liste.append( ['M6', URL_MAIN + 'category/replay_tv/m6/'] )
    liste.append( ['6Ter', URL_MAIN + 'category/replay_tv/6ter/'] )
    liste.append( ['D8', URL_MAIN + 'category/replay_tv/d8/'] )
    liste.append( ['France O', URL_MAIN + 'category/replay_tv/franceo/'] )
    liste.append( ['ICI', URL_MAIN + 'category/replay_tv/ici/'] )
    liste.append( ['N23', URL_MAIN + 'category/replay_tv/n23/'] )
    liste.append( ['Nrj12', URL_MAIN + 'category/replay_tv/nrj12/'] )
    liste.append( ['Nt1', URL_MAIN + 'category/replay_tv/nt1/'] )
    liste.append( ['Rmc', URL_MAIN + 'category/replay_tv/rmc/'] )
    liste.append( ['Tf1', URL_MAIN + 'category/replay_tv/tf1/'] )
    liste.append( ['Tmc', URL_MAIN + 'category/replay_tv/tmc/'] )
    liste.append( ['W9', URL_MAIN + 'category/replay_tv/w9/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('&#039;', '\'').replace('&#8212;', '-').replace('&#8217;', '\'').replace('&#8230;', '...')
    sHtmlContent = sHtmlContent.replace('[&hellip;]', '...')

    sPattern = '<div id="post-.*?<a href="([^"]+)".*?<img src="([^"]+)" alt="([^"]+)"(?:.+?<div class="item-content hidden"><p>([^<]+)</p>|)'

    oParser = cParser()
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

            sUrl = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]#.replace('&laquo;', '<<').replace('&raquo;', '>>').replace('&nbsp;', '')
            sDesc = aEntry[3]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<link rel="next" href="([^"]+)" />'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/', '')

    sPattern = '<iframe.+?src="([^"]+)".+?</iframe>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
