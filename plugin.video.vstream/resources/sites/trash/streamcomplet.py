#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#21/05 2host beaucoup de lien mort site pas interessant.
return False
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig
from resources.lib.packer import cPacker
import re

SITE_IDENTIFIER = 'streamcomplet'
SITE_NAME = 'StreamComplet'
SITE_DESC = 'Streaming Gratuit de 6420 Films Complets en VF.'

URL_MAIN = 'http://streamcomplet.me/'

MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
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
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'film/action/'] )
    liste.append( ['Animation', URL_MAIN + 'film/animation/'] )
    liste.append( ['Aventure', URL_MAIN + 'film/aventure/'] )
    liste.append( ['Comédie', URL_MAIN + 'film/comedie/'] )
    liste.append( ['Drame', URL_MAIN + 'film/drame/'] )
    liste.append( ['Fiction', URL_MAIN + 'film/fiction/'] )
    liste.append( ['Guerre', URL_MAIN + 'film/guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'film/historique/'] )
    liste.append( ['Horreur', URL_MAIN + 'film/horreur/'] )
    liste.append( ['Musique', URL_MAIN + 'film/musique/'] )
    liste.append( ['Policier', URL_MAIN + 'film/policier/'] )
    liste.append( ['Romance', URL_MAIN + 'film/romance/'] )
    liste.append( ['Thriller', URL_MAIN + 'film/thriller/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<div class="moviefilm"><a href=".+?"><img src="([^<]+)" alt=".+?" height=".+?" width=".+?" />.+?<a href="([^<]+)">([^<]+)</a>'
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

            sThumb = str(aEntry[0])
            sUrl = str(aEntry[1])
            sTitle = str(aEntry[2])

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), sTitle) == 0:
                    continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

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
    sPattern = '<span class=\'current\'>.+?</span><a class="page larger" href="(.+?)">'
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
    #vimple redirect to ok or openload
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    list_url = []

    sPattern = 'src="(http:\/\/media\.vimple\.me.+?f=([^"]+))"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sUrl3 = 'https://ok.ru/videoembed/' + aResult[1][0][1]
        list_url.append(sUrl3)

        sUrl2 = aResult[1][0][0]

        oRequestHandler = cRequestHandler(sUrl2)
        oRequestHandler.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0')
        oRequestHandler.addHeaderEntry('Referer', sUrl)
        sHtmlContent = oRequestHandler.request()

        sHtmlContent = oParser.abParse(sHtmlContent, "<script>", "</script><script>")

        sPattern = 'eval\s*\(\s*function(?:.|\s)+?{}\)\)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sHtmlContent = cPacker().unpack(aResult[1][0])
            sHtmlContent = sHtmlContent.replace('\\', '')
            code = re.search('(https://openload.+?embed\/.+?\/)', sHtmlContent)
            if code:
                sUrl4 = code.group(1)
                list_url.append(sUrl4)


    for aEntry in list_url:
        oHoster = cHosterGui().checkHoster(aEntry)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, aEntry, '')

    oGui.setEndOfDirectory()
