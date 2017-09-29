#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig

SITE_IDENTIFIER = 'reportagestv_com'
SITE_NAME = 'Reportages TV'
SITE_DESC = 'Reportages TV - Replay des reportages télé français en streaming.'

URL_MAIN = 'http://www.reportagestv.com/'

DOC_NEWS = (URL_MAIN, 'showMovies')
DOC_DOCS = ('http://', 'load')
DOC_GENRES = (True, 'showGenres')

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
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_GENRES[1], 'Genres', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = URL_SEARCH[0] + sSearchText
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Espionnage',URL_MAIN + 'category/espionnage/'] )
    liste.append( ['Grand-Banditisme',URL_MAIN + 'category/grand-ganditisme/'] )
    liste.append( ['Mafias',URL_MAIN + 'category/mafias/'] )
    liste.append( ['TF1',URL_MAIN + 'category/tf1/'] )
    liste.append( ['TF1 - Appels d\'Urgence',URL_MAIN + 'category/tf1/appels-durgence/'] )
    liste.append( ['TF1 - Sept à Huit',URL_MAIN + 'category/tf1/sept-a-huit/'] )
    liste.append( ['France 2',URL_MAIN + 'category/france-2/'] )
    liste.append( ['France 2 - Apocalypse la 1ère guerre mondiale',URL_MAIN + 'category/france-2/apocalypse-la-1-ere-guerre-mondiale/'] )
    liste.append( ['France 2 - Envoyé Spécial',URL_MAIN + 'category/france-2/envoye-special/'] )
    liste.append( ['Canal+',URL_MAIN + 'category/canal-plus/'] )
    liste.append( ['Canal+ - Nouvelle Vie',URL_MAIN + 'category/canal-plus/nouvelle-vie/'] )
    liste.append( ['Canal+ - Spécial Investigation',URL_MAIN + 'category/canal-plus/special-investigation/'] )
    liste.append( ['D8 - Au coeur de l\'Enquête',URL_MAIN + 'category/d8/au-coeur-de-lenquete/'] )
    liste.append( ['D8 - En quête d\'Actualité',URL_MAIN + 'category/d8/en-quete-dactualite/'] )
    liste.append( ['D8',URL_MAIN + 'category/d8/'] )
    liste.append( ['TMC',URL_MAIN + 'category/tmc/'] )
    liste.append( ['TMC - 90 Enquêtes',URL_MAIN + 'category/tmc/90-enquetes/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'doc.png', oOutputParameterHandler)

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

    sPattern = 'class="mh-loop-thumb">.+?<img.+?src="([^<]+)" class="attachment.+?<a href="([^"]+)" rel="bookmark">([^<]+)</a>.+?<div class="mh-excerpt"><p>(.+?)<a class'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sTitle = aEntry[2].replace('&laquo;','<<').replace('&raquo;','>>').replace('&nbsp;','')
            sSin = aEntry[3].replace('&laquo;','<<').replace('&raquo;','>>')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[1])
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', aEntry[0])
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', aEntry[0], sSin, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = "<span class='page-numbers current'>.+?<a class='page-numbers' href='(.+?)'>.+?</a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def __checkForRealUrl(sHtmlContent):
    sPattern = 'center.+?<a href="(.+?)".+?<input type="button".+?</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    cConfig().log(str(aResult))
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sRealUrl = __checkForRealUrl(sHtmlContent)

    if (sRealUrl != False):
        oRequestHandler = cRequestHandler(sRealUrl)
        sHtmlContent = oRequestHandler.request();

    sPattern = '<iframe.+?src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = str(aEntry)
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

    oGui.setEndOfDirectory()
