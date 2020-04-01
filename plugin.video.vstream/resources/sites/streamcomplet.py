#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress#, VSlog
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'streamcomplet'
SITE_NAME = 'StreamComplet'
SITE_DESC = 'Les meilleurs films en version française'

URL_MAIN = 'https://www2.stream-complet.me/'

MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_MOVIE = ('http://', 'load')

URL_SEARCH = (URL_MAIN + 'search/', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

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
    liste.append( ['Aventure', URL_MAIN + 'films/aventure/'] )
    liste.append( ['Comédie', URL_MAIN + 'films/comedie/'] )
    liste.append( ['Drame', URL_MAIN + 'films/drame/'] )
    liste.append( ['Fiction', URL_MAIN + 'films/fiction/'] )
    liste.append( ['Guerre', URL_MAIN + 'films/guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'films/historique/'] )
    liste.append( ['Horreur', URL_MAIN + 'films/horreur/'] )
    liste.append( ['Musique', URL_MAIN + 'films/musical/'] )
    liste.append( ['Policier', URL_MAIN + 'films/policier/'] )
    liste.append( ['Romance', URL_MAIN + 'films/romance/'] )
    liste.append( ['Thriller', URL_MAIN + 'films/thriller/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

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

    sPattern = '<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)".+?<div class="(movies">(.+?)<|moviefilm">)'
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

            if (aEntry[0] == '/'):
                continue

            sUrl = URL_MAIN[:-1] + aEntry[0]
            sThumb = URL_MAIN[:-1] + aEntry[1]
            sTitle = aEntry[2]
            sYear = aEntry[4]

            #tris search
            if sSearch and total > 3:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), sTitle) == 0:
                    continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="current">.+?<a class="page larger" href="([^"]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]

    return False

def showLinks():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li class="player link" data-player="([^"]+)">.+?<span class="p-name">([^"]+)</span>'
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

            sUrl = URL_MAIN[:-1] + aEntry[0]
            sDisplayName = ('%s [COLOR coral]%s[/COLOR]') % (sTitle, aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayName, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    #vimple redirect to ok or openload
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sPattern = 'url=([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

#
#
# Ancient code du site .xyz
# si retour en arriere
#
#

#    sPattern = '<iframe.+?src="(http(?:|s):\/\/media\.vimple\.me.+?f=([^"]+))"'
#    aResult = oParser.parse(sHtmlContent, sPattern)
#    if (aResult[0] == True):

#        sUrl2 = aResult[1][0][0]
#
#        oRequestHandler = cRequestHandler(sUrl2)
#        oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0')
#        oRequestHandler.addHeaderEntry('Referer', sUrl)
#        sHtmlContent = oRequestHandler.request()
#
#        sPattern = '<iframe src="([^"]+)"'
#        aResult = oParser.parse(sHtmlContent, sPattern)
#
#        if (aResult[0] == True):
#            sHosterUrl = 'https:' + aResult[1][0]
#            #VSlog(sHosterUrl)
#            oHoster = cHosterGui().checkHoster(sHosterUrl)
#            if (oHoster != False):
#                oHoster.setDisplayName(sMovieTitle)
#                oHoster.setFileName(sMovieTitle)
#                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
#        else:
#            sHtmlContent = oParser.abParse(sHtmlContent, "<script>", "</script><script>")
#
#            sPattern = 'eval\s*\(\s*function(?:.|\s)+?{}\)\)'
#            aResult = oParser.parse(sHtmlContent, sPattern)
#            if (aResult[0] == True):
#                sHtmlContent = cPacker().unpack(aResult[1][0])
#                sHtmlContent = sHtmlContent.replace('\\', '')
#                #VSlog(sHtmlContent)
#                code = re.search('(https://openload.+?embed\/.+?\/)', sHtmlContent)
#                if code:
#                    sHosterUrl = code.group(1)
#                   #VSlog(sHosterUrl)
#                   oHoster = cHosterGui().checkHoster(sHosterUrl)
#                   if (oHoster != False):
#                       oHoster.setDisplayName(sMovieTitle)
#                       oHoster.setFileName(sMovieTitle)
#                       cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()
