#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.gui.hoster import cHosterGui
# from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress

import re

SITE_IDENTIFIER = 'streamavie'
SITE_NAME = 'Streamavie'
SITE_DESC = 'Films VF & VOSTFR en streaming.'

URL_MAIN = 'http://streamavie.com/'

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN, 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'tendance/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'evaluations/', 'showMovies')
#MOVIE_LIST = (True, 'showList')
MOVIE_ANNEES = (True, 'showYears')
MOVIE_GENRES = (True, 'showGenres')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'notes.png', oOutputParameterHandler)

    #ne fonctionne plus sur le site
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    #oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Liste)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

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
    oParser = cParser()

    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<li class="cat-item cat-item-.+?"><a href="([^<]+)">([^<]+)</a> <i>([^<]+)</i>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sTitle = aEntry[1] + ' (' + aEntry[2] + ')'
            sUrl = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showList():
    oGui = cGui()

    liste = []
    liste.append( ['09', URL_MAIN + '?letter=true&s=title-09'] )
    liste.append( ['A', URL_MAIN + '?letter=true&s=title-a'] )
    liste.append( ['B', URL_MAIN + '?letter=true&s=title-b'] )
    liste.append( ['C', URL_MAIN + '?letter=true&s=title-c'] )
    liste.append( ['D', URL_MAIN + '?letter=true&s=title-d'] )
    liste.append( ['E', URL_MAIN + '?letter=true&s=title-e'] )
    liste.append( ['F', URL_MAIN + '?letter=true&s=title-f'] )
    liste.append( ['G', URL_MAIN + '?letter=true&s=title-g'] )
    liste.append( ['H', URL_MAIN + '?letter=true&s=title-h'] )
    liste.append( ['I', URL_MAIN + '?letter=true&s=title-i'] )
    liste.append( ['J', URL_MAIN + '?letter=true&s=title-j'] )
    liste.append( ['K', URL_MAIN + '?letter=true&s=title-k'] )
    liste.append( ['L', URL_MAIN + '?letter=true&s=title-l'] )
    liste.append( ['M', URL_MAIN + '?letter=true&s=title-m'] )
    liste.append( ['N', URL_MAIN + '?letter=true&s=title-n'] )
    liste.append( ['O', URL_MAIN + '?letter=true&s=title-o'] )
    liste.append( ['P', URL_MAIN + '?letter=true&s=title-p'] )
    liste.append( ['Q', URL_MAIN + '?letter=true&s=title-q'] )
    liste.append( ['R', URL_MAIN + '?letter=true&s=title-r'] )
    liste.append( ['S', URL_MAIN + '?letter=true&s=title-s'] )
    liste.append( ['T', URL_MAIN + '?letter=true&s=title-t'] )
    liste.append( ['U', URL_MAIN + '?letter=true&s=title-u'] )
    liste.append( ['V', URL_MAIN + '?letter=true&s=title-v'] )
    liste.append( ['W', URL_MAIN + '?letter=true&s=title-w'] )
    liste.append( ['X', URL_MAIN + '?letter=true&s=title-x'] )
    liste.append( ['Y', URL_MAIN + '?letter=true&s=title-y'] )
    liste.append( ['Z', URL_MAIN + '?letter=true&s=title-z'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showYears():
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)

    sStart = '<ul class="releases scrolling">'
    sEnd = '</div>  <div class="content">'
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<li><a href="([^"]+)">([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
        sPattern = '<div class="result-item">.+?<img src="([^"]+)" alt="([^"]+)".+?<a href="([^"]+)".+?<p>(.+?)<\/p>'

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        if '/films/' in sUrl or '/annee/' in sUrl or '/genre/' in sUrl:
            sPattern = '<div class="poster".+?src="([^"]+)" alt="([^"]+)".+?quality">([^<]+)<.+?<a href="([^"]+)".+?<div class="texto">([^<]+)<'
        else:#qualite pas tjrs presente et pas de description
            sPattern = '<div class="poster".+?src="([^"]+)" alt="([^"]+)".+?(?:|quality">([^<]+)<.+?)<a href="([^"]+)"'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
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

            if sSearch:
                sThumb = aEntry[0]
                sTitle = aEntry[1]
                sUrl2 = aEntry[2]
                sDesc = aEntry[3]
                sDisplayTitle = sTitle
            elif '/films/' in sUrl or '/annee/' in sUrl or '/genre/' in sUrl:
                sThumb = aEntry[0]
                sTitle = aEntry[1]
                sQual = aEntry[2]
                sUrl2 = aEntry[3]
                sDesc = aEntry[4]
                sDisplayTitle = sTitle + ' [' + sQual + ']'
            else:
                sThumb = aEntry[0]
                sTitle = aEntry[1]
                sQual = aEntry[2]
                sUrl2 = aEntry[3]
                sDesc = ''
                sDisplayTitle = sTitle + ' [' + sQual + ']'

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), sTitle) == 0:
                    continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="current">.+?</span><a href=\'(.+?)\''
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showLink():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    sPattern = "data-type='([^']+)' data-post='(\d+)' data-nume='(\d+)'>.+?class='server'>([^<]+)<"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sUrl2 = URL_MAIN + 'wp-admin/admin-ajax.php'
            dType = aEntry[0]
            dPost = aEntry[1]
            dNum = aEntry[2]
            sHost = re.sub('\.\w+', '', aEntry[3]).capitalize()

            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('dType', dType)
            oOutputParameterHandler.addParameter('dPost', dPost)
            oOutputParameterHandler.addParameter('dNum', dNum)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    referer = oInputParameterHandler.getValue('referer')
    dPost = oInputParameterHandler.getValue('dPost')
    dNum = oInputParameterHandler.getValue('dNum')
    dType = oInputParameterHandler.getValue('dType')

    pdata = 'action=doo_player_ajax&post=' + dPost + '&nume=' + dNum + '&type=' + dType
    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
    oRequest.addHeaderEntry('Referer', referer)
    oRequest.addHeaderEntry('Accept', '*/*')
    oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequest.addParametersLine(pdata)

    sHtmlContent = oRequest.request()

    #sPattern = '<IFRAME SRC="([^"]+)"'
    #aResult = oParser.parse(sHtmlContent, sPattern)

    #if (aResult[0] == False):
    sPattern = "src='([^']+)'"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
