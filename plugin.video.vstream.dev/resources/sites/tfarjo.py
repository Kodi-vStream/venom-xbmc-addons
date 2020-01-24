#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
return False
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, addon, VSlog
import re
sColor = addon().getSetting("deco_color")

SITE_IDENTIFIER = 'tfarjo'
SITE_NAME = 'Tfarjo'
SITE_DESC = 'Films & Séries en streaming VO | VF | VOSTFR'

#URL_MAIN = 'https://www5.tfarjo.ws/'
#URL_MAIN = 'https://www.filmz.cc/'
URL_MAIN = 'https://www.tfarjo.cc/'

MOVIE_NEWS = (URL_MAIN + 'films', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')

SERIE_NEWS = (URL_MAIN + 'series', 'showSeries')
SERIE_SERIES = (URL_MAIN + 'series', 'showSeries')
#SERIE_VFS = (URL_MAIN + 'series/vf', 'showSeries')
#SERIE_VOSTFRS = (URL_MAIN + 'series/vostfr', 'showSeries') #pas fiable et pareil que dernier ajouts

URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_SERIES = ('', 'showMovies')

FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0'

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

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)


    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sText= sSearchText
        showMovies(sText)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'films/genre/action'] )
    liste.append( ['Animation', URL_MAIN +'films/genre/animation'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'films/genre/arts-Martiaux'] )
    liste.append( ['Aventure', URL_MAIN + 'films/genre/aventure'] )
    liste.append( ['Biopic', URL_MAIN + 'films/genre/biopic'] )
    liste.append( ['Comédie', URL_MAIN + 'films/genre/comédie'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'films/genre/comédie-dramatique'] )
    liste.append( ['Comédie Musicale', URL_MAIN + 'films/genre/comédie-musicale'] )
    liste.append( ['Spectacle', URL_MAIN + 'films/genre/crime'] )
    liste.append( ['Spectacle', URL_MAIN + 'films/genre/dance'] )
    liste.append( ['Documentaire', URL_MAIN + 'films/genre/documentaire'] )
    liste.append( ['Drame', URL_MAIN + 'films/genre/drame'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'films/genre/epouvante-horreur'] )
    liste.append( ['Erotique', URL_MAIN + 'films/genre/erotique'] )
    liste.append( ['Espionnage', URL_MAIN + 'films/genre/espionnage'] )
    liste.append( ['Famille', URL_MAIN + 'films/genre/famille'] )
    liste.append( ['Fantastique', URL_MAIN + 'films/genre/fantastique'] )
    liste.append( ['Guerre', URL_MAIN + 'films/genre/guerre'] )
    liste.append( ['Historique', URL_MAIN + 'films/genre/historique'] )
    liste.append( ['Musical', URL_MAIN + 'films/genre/musical'] )
    liste.append( ['Spectacle', URL_MAIN + 'films/genre/mystere'] )
    liste.append( ['Policier', URL_MAIN + 'films/genre/policier'] )
    liste.append( ['Romance', URL_MAIN + 'films/genre/romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'films/genre/science-fiction'] )
    liste.append( ['Divers', URL_MAIN + 'films/genre/sport'] )
    liste.append( ['Thriller', URL_MAIN + 'films/genre/thriller'] )
    liste.append( ['Western', URL_MAIN + 'films/genre/western'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def getcode(sHtmlContent):
    sPattern1 = '<input type="hidden" name="csrf_test_name" id="csrf_test_name" value="([^"]+)">'
    sCode = re.search(sPattern1, sHtmlContent)
    if sCode:
        return sCode.group(1)
    else:
        return ''

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        oRequest = cRequestHandler(URL_MAIN)
        sHtmlContent = oRequest.request()
        cook = oRequest.GetCookies()

        sCode = getcode(sHtmlContent)

        sText = sSearch
        oRequest = cRequestHandler(URL_MAIN + 'search')
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
        oRequest.addHeaderEntry('Cookie', cook)
        oRequest.addParametersLine('search=' + sText + '&csrf_test_name=' + sCode)

        sHtmlContent = oRequest.request()
        sHtmlContent = re.sub('<h2></h2>', '<span class="Langue..."></span><span class="qalite">Qualité...</span>', sHtmlContent)#recherche pas de qualité,langue

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        #parfois pas de qualité,langue,liens >> BA
        sHtmlContent = re.sub('<span class="bientot"></span>', '<span class="nothing"></span><span class="qalite">nothing</span>', sHtmlContent)

    sPattern = '<div class="image">.+?<a href="([^"]+)".+?<img src="([^"]+)".+?title="([^"]+)">.+?<span class="([^"]+)"></span><span class="qalite">([^<]+)</span>'

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

            if aEntry[3] == 'nothing' and aEntry[4] == 'nothing':#pas de qualité,langue,liens >> BA
                continue

            sUrl = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]
            sLang = aEntry[3]
            sQual = aEntry[4]

            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            if 'serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="active">\d+</span>.+?<a href="([^"]+)" data-ci'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<div class="image">.+?<a href="([^"]+)".+?<img src="([^"]+)".+?title="([^"]+)">'

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
            sTitle = aEntry[2]


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)


    oGui.setEndOfDirectory()

def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #sHtmlContent = oParser.abParse(sHtmlContent, 'begin seasons', 'end seasons')
    #pas encore d'épisode >> timer avant sortie
    sHtmlContent = re.sub('<kbd><span', '<kbd>nothing</span>', sHtmlContent)

    sPattern = '<h3 class="panel-title"><a href=".+?">(saison *\d+)<\/a>|<div class="panel-body">.+?href="([^"]+)">.+?<\/span>([^"]+)</a>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')

            else:
                # if aEntry[3] == 'nothing':
                    # continue

                sUrl = aEntry[1]

                sDisplayTitle = "%s %s" % (sMovieTitle, aEntry[2].replace(',', ''))

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showLink', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()
    cook = oRequest.GetCookies()
    sCode = getcode(sHtmlContent)

    sPattern2 = "<button *class=\"players(?:(vf|vo|vostfr))\" *onclick=\"getIframe\('([^']+)'\).+?<\/span> *([^<]+)<"
    aResult = oParser.parse(sHtmlContent, sPattern2)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sLang = aEntry[0].upper()
            sHost = aEntry[2].capitalize()
            sCode2 = aEntry[1]

            sDisplayTitle = ('%s (%s) [COLOR %s]%s[/COLOR]') % (sMovieTitle, sLang, sColor, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sCode', sCode)
            oOutputParameterHandler.addParameter('sCode2', sCode2)
            oOutputParameterHandler.addParameter('sCook', cook)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sCode = oInputParameterHandler.getValue('sCode')
    sCode2 = oInputParameterHandler.getValue('sCode2')
    sCook = oInputParameterHandler.getValue('sCook')

    oParser = cParser()

    #VSlog(URL_MAIN + 'getlinke')
    #VSlog(sCook)

    if '/serie' in sUrl:
        oRequest = cRequestHandler(URL_MAIN + 'getlinke')
        oRequest.addParametersLine('csrf_test_name=' + sCode + '&episode=' + sCode2)
    else:
        oRequest = cRequestHandler(URL_MAIN + 'getlink')
        oRequest.addParametersLine('csrf_test_name=' + sCode + '&movie=' + sCode2)

    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Referer', sUrl)
    oRequest.addHeaderEntry('Cookie', sCook)

    sHtmlContent = oRequest.request()
    sHtmlContent = sHtmlContent.replace('\\', '')

    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    sPattern = '<iframe.+?src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):

        sHosterUrl = aResult[1][0]

        oHoster = cHosterGui().checkHoster(sHosterUrl)

        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
