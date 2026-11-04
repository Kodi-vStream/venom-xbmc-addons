# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.comaddon import siteManager
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'vidzy'
SITE_NAME = 'Vidzy'
SITE_DESC = 'Hébergeur direct'

URL_SEARCH = ('movie/%s', 'showMovies')
URL_SEARCH_MOVIES = ('', 'showMovies')

#URL_SEARCH_SERIES = ('serie/%d/%d/%d/vf', 'showSeries')  #  /serie/{tmdb}/{saison}/{episode}

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    searchIdTMDB = oInputParameterHandler.getValue('sTmdbId')

    for lang in ('fr', 'vostfr'):
        sUrl = '%s%s/%s' % (URL_MAIN, URL_SEARCH[0] % searchIdTMDB, lang)
        oRequestHandler = cRequestHandler(sUrl)
        data = oRequestHandler.request()
        aResult = oParser.parse(data, '<title>([^<]+)</title>')
        if not aResult[0]:
            return
        sMovieTitle = aResult[1][0]
        sDisplayTitle = '%s - [%s]' % (sMovieTitle, lang.upper()) 
        
        aResult = oParser.parse(data, '<iframe.+?src="([^"]+)')
        if not aResult[0]:
            return
        siteUrl = aResult[1][0]
    
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sTmdbId', searchIdTMDB)
        oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', '', '', oOutputParameterHandler)


def showHosters():
    oGui = cGui()
    oHosterGui = cHosterGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sHtmlContent = cRequestHandler(sUrl).request()
    aResult = oParser.parse(sHtmlContent, "fetch\('([^']+)")
    if aResult[0]:
        fetchUrl = aResult[1][0] + 'v=p1&cw=159.56&cw2=170.34&wg=1&ca=e55a64e071fadf14&cl=23946&dpr=1&sw=1680&hw=4&ft=%s&rf=%s' % (URL_MAIN, URL_MAIN)
        data = cRequestHandler(fetchUrl).request(True)
        gk = data.get('gk', None)
        if gk:
            aResult = oParser.parse(sHtmlContent, 'sources: *\[(.+?)\]')
            if aResult[0]:
                aResult = oParser.parse(aResult[1][0], 'src: *"([^"]+)')
                if aResult[0]:
                    sHosterUrl = aResult[1][0]
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        sHosterUrl += '&gk=%s' % gk
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        oHosterGui.showHoster(oGui, oHoster, sHosterUrl)

    oGui.setEndOfDirectory()
