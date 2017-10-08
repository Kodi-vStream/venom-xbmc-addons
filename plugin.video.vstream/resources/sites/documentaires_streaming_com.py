#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig

SITE_IDENTIFIER = 'documentaires_streaming_com'
SITE_NAME = 'Documentaires Streaming'
SITE_DESC = 'replay tv, documentaire, reportage'

URL_MAIN = 'http://www.documentaires-streaming.com/'

DOC_NEWS = (URL_MAIN+'category/documentaire/', 'showMovies')
DOC_DOCS = ('http://', 'load')
DOC_GENRES = (True, 'showGenres')

REPLAYTV_REPLAYTV = ('http://', 'showReplayGenres')

REPORTAGE_NEWS = (URL_MAIN+'category/reportages/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + '?s=', 'showMovies')

FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://')
    oGui.addDir(SITE_IDENTIFIER, 'showDocuGenres', 'Documentaires (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_REPLAYTV[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_REPLAYTV[1], 'Replay TV (chaines)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPORTAGE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPORTAGE_NEWS[1], 'Reportages', 'news.png', oOutputParameterHandler)

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
    liste.append( ['Histoires',URL_MAIN + 'category/histoires/'] )
    liste.append( ['Nature, Animaux',URL_MAIN + 'category/nature_animaux/'] )
    liste.append( ['Paranormal',URL_MAIN + 'category/paranormal/'] )
    liste.append( ['Politique, Société',URL_MAIN + 'category/politique-societe/'] )
    liste.append( ['Science',URL_MAIN + 'category/science/'] )
    liste.append( ['Société',URL_MAIN + 'documentaire/societe/'] )
    liste.append( ['Sport',URL_MAIN + 'category/sport/'] )
    liste.append( ['Voiture',URL_MAIN + 'category/voiture/'] )
    liste.append( ['Voyage',URL_MAIN + 'category/voyage-2/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showReplayGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Arte',URL_MAIN + 'category/replay_tv/arte-replay_tv/'] )
    liste.append( ['France 2',URL_MAIN + 'category/replay_tv/france_2/'] )
    liste.append( ['France 3',URL_MAIN + 'category/replay_tv/france_3/'] )
    liste.append( ['France 5',URL_MAIN + 'category/replay_tv/france_5/'] )
    liste.append( ['M6',URL_MAIN + 'category/replay_tv/m6/'] )
    liste.append( ['6Ter',URL_MAIN + 'category/replay_tv/6ter/'] )
    liste.append( ['D8',URL_MAIN + 'category/replay_tv/d8/'] )
    liste.append( ['France O',URL_MAIN + 'category/replay_tv/franceo/'] )
    liste.append( ['ICI',URL_MAIN + 'category/replay_tv/ici/'] )
    liste.append( ['N23',URL_MAIN + 'category/replay_tv/n23/'] )
    liste.append( ['Nrj12',URL_MAIN + 'category/replay_tv/nrj12/'] )
    liste.append( ['Nt1',URL_MAIN + 'category/replay_tv/nt1/'] )
    liste.append( ['Rmc',URL_MAIN + 'category/replay_tv/rmc/'] )
    liste.append( ['Tf1',URL_MAIN + 'category/replay_tv/tf1/'] )
    liste.append( ['Tmc',URL_MAIN + 'category/replay_tv/tmc/'] )
    liste.append( ['W9',URL_MAIN + 'category/replay_tv/w9/'] )


    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)

    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('&#039;', '\'').replace('&#8217;', '\'')

    sPattern = '<div class="item-thumbnail">.*?<a href="([^"]+)".*?<img src="([^"]+)" alt="([^"]+)"(?:.+?<div class="item-content hidden"><p>([^<]+)</p>|)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            #sTitle = aEntry[2].replace('&laquo;','<<').replace('&raquo;','>>').replace('&nbsp;','')
            sCom = aEntry[3].replace('[&hellip;]','...')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            #oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', aEntry[1])
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', aEntry[2], 'doc.png', aEntry[1], sCom, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<link rel="next" href="(.+?)" />'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('title')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/', '')

    sPattern = '<IFRAME SRC="(.+?)".+?</IFRAME>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
