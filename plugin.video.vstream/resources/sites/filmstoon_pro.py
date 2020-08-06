# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# TODO : resources/art/sites  https://www.filmstoon.pro/templates/filmstoon/images/logo.webp
# source 03

# update 30/07/2020
# add MOVIE_ANNEES;add MOVIE_VIEWS;update search; updateshowHosters()sPattern;

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import xbmc
from resources.lib.comaddon import VSlog

# liens not found pour 3 raisons connues assez peu nombreux mais presents
# courant:
# notification des liens register dans le hoster.displaytitle
# rares:
# xbmc notification: acces aux liens en changeant juste l'ip ;
# autre cas connu: cloudfare ( non traité )

bVSlog = False

SITE_IDENTIFIER = 'filmstoon_pro'
SITE_NAME = 'Filmstoon pro'
SITE_DESC = ' films en streaming'

# URL_MAIN = 'https://www.filmstoon.pro/'
URL_MAIN = 'https://www.filmstoon.pw/'

# globales
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')
MOVIE_VIEWS = (URL_MAIN + 'film/populaire/', 'showMovies')
MOVIE_MOVIE = (True, 'load')

# https://www.filmstoon.pw/film/populaire/
# https://www.filmstoon.pro/?s=blood

URL_SEARCH = (URL_MAIN, 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (les plus populaires)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER,MOVIE_ANNEES[1], 'Films (Par années)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        # sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        sUrl = sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', URL_MAIN + 'film/action/'])
    liste.append(['Animation', URL_MAIN + 'film/anime/'])
    liste.append(['Arts Martiaux', URL_MAIN + 'film/arts-martiaux/'])
    liste.append(['Aventure', URL_MAIN + 'film/aventure/'])
    liste.append(['Biopic', URL_MAIN + 'film/biopic/'])
    liste.append(['Comédie', URL_MAIN + 'film/comedie/'])
    liste.append(['Comédie dramatique', URL_MAIN + 'comedie-dramatique/'])
    liste.append(['Documentaire', URL_MAIN + 'film/documentaire/'])
    liste.append(['Drame', URL_MAIN + 'film/drame/'])
    liste.append(['Epouvante-horreur', URL_MAIN + 'film/epouvante-horreur/'])
    liste.append(['Espionnage', URL_MAIN + 'film/espionnage'])
    liste.append(['Famille', URL_MAIN + 'film/famille/'])
    liste.append(['Fantastique', URL_MAIN + 'film/fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'film/guerre/'])
    liste.append(['Historique', URL_MAIN + 'film/historique/'])
    liste.append(['Musical', URL_MAIN + 'film/musical/'])
    liste.append(['Policier', URL_MAIN + 'film/policier/'])
    liste.append(['Romance', URL_MAIN + 'film/romance/'])
    liste.append(['Science fiction', URL_MAIN + 'film/science-fiction/'])
    liste.append(['Thriller', URL_MAIN + 'film/thriller/'])
    liste.append(['Western', URL_MAIN + 'film/western/'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()
    # https://www.filmstoon.pw/2020/
    for i in reversed(range(1971, 2020)):
        sYear = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sYear + '/')  # / inutile
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    if sSearch:
        # '?s='
        pdata = 'do=search&subaction=search&story=' + sSearch
        sUrl = URL_MAIN + '?s=' + sSearch
        oRequest = cRequestHandler(sUrl)
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
        oRequest.addHeaderEntry('Referer', sUrl)
        oRequest.addParametersLine(pdata)
        sHtmlContent = oRequest.request()
        # url thumb tile desc
        sPattern = '<a class="sres-wrap.+?ref="([^"]*).+?data-src="([^"]*).+?alt="([^"]*).+?desc">([^<]*)'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        # url  title thumb desc
        sPattern = '<h2> <span>Film Streaming.+?href="(.+?)">(.+?)<.+?data-src="(.+?)".+?st-desc">(.+?)<.div'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)
        # ifVSlog(sHtmlContent)
        ifVSlog('')
        ifVSlog('Failed Pattern with url = ' + sUrl)
        ifVSlog('Selected Pattern = ' + sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])

        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sDesc = aEntry[3]
            if sSearch:
                sTitle = aEntry[2]
                sThumb = aEntry[1]
            else:
                sTitle = aEntry[1]
                sThumb = aEntry[2]
            # ifVSlog('sUrl2 =' + sUrl)
            # ifVSlog('sThumb =' + sThumb)
            # ifVSlog('sTitle =' + sTitle)
            # ifVSlog('sDesc =' + sDesc )
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        NextPage = __checkForNextPage(sHtmlContent)
        if (NextPage != False):
            sNumLastPage = NextPage[0]
            sUrlNextPage = NextPage[1]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrlNextPage)
            number = re.search('/page/([0-9]+)', sUrlNextPage ).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + number + '/' + sNumLastPage + ' >>>[/COLOR]', oOutputParameterHandler)
        else:
            ifVSlog('NextPage false')

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>([^<]*)<.a><.span>\s*<span class="pnext.+?href="([^<]*)"'
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
    sDesc = oInputParameterHandler.getValue('sDesc')  # faire un addlink  juste pour desc ?

    ifVSlog('#')
    ifVSlog('showHosters')
    ifVSlog('surl = ' + sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # sPattern='<div class="st-line"> Année:([^<]*)<.div>.+?line"> Durée:([^<]*)'
    # oParser = cParser()
    # aResult = oParser.parse(sHtmlContent, sPattern)
    # if (aResult[0] == True):
        # if len(aResult[1]) == 1:
            # aEntry = aResult[1][0]
            # sDesc= aEntry[0] +' ' +aEntry[1] + sDesc

    # html qui a changé spaterne hs
    # sPattern = 'iframe src="data:image.+?show.filmstoon.pro.+?php.([^"]*)&'

    # valides pattern
    # sPattern = 'data:image.+?data-src=".+?filmstoon.pw.playfst.php.([^"]*).p=http'  # temps trop long 200 ms
    # sPattern = 'data-src.+?filmstoon.pw.playfst.php.([^"]*).p=https' # 50 ms
    sPattern = 'data-src.+?playfst.php.([^"]*).p=https'  # 50

    # exemple
    # tl=Jumbo&yr=2020&im=tt6818118&butm=f8amdzps8q1k&sv=ms&sr=fst&ni=259782&fc=37290a4f2d42347bce34d609e8e0e01f

    # g1: parametres de la requete que l'on va copier et echanger
    # avec celle genérée normalement par https://easyplayer.cc/player.php?
    # c'est quasiment la meme

    requestlist = []
    sHosterUrllist = []
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)
        # ifVSlog(sHtmlContent)
        # ifVSlog('')
        ifVSlog('Failed Pattern with url = ' + sUrl)
        ifVSlog('Selected Pattern = ' + sPattern)
        # Your IP-address or subnet have been blocked
        if 'Your IP-address or subnet have been blocked' in sHtmlContent:
            xbmc.executebuiltin('Notification(%s, %s, %d)' % ('Filmstoon Plugin ', 'You have been blocked : Try change your IP-address ', 5000))

    if (aResult[0] == True):

        for aEntry in aResult[1]:
            req = 'https://easyplayer.cc/player.php?' + str(aEntry)
            requestlist.append(req)
    # i=0
    for irequest in requestlist:
        # url du host dans l'entete de la réponse
        urlreq = irequest
        ifVSlog(urlreq)
        oRequestHandler = cRequestHandler(urlreq)
        oRequestHandler.request()
        sHeader = oRequestHandler.getResponseHeader()
        bDoublon = False  # on verifie si url embed en double (mystrem)
        sremarque = ''
        for iheader in sHeader:
            if iheader == 'refresh':
                sHosterUrl = sHeader.getheader('refresh')
                ifVSlog('header ' + sHosterUrl)
                sHosterUrl = sHosterUrl.split(';')
                sHosterUrl = sHosterUrl[1]
                sHosterUrl = sHosterUrl.replace('url=', '')

                # ne marche pas
                # url=https://filmstreaming1.red/registred.php?
                if 'registred' in sHosterUrl:
                    sremarque = '[ Find register link !  ] '

                ifVSlog('header url=' + sHosterUrl)
                if not sHosterUrl in sHosterUrllist:
                    bDoublon = False
                    sHosterUrllist.append(sHosterUrl)
                    # i = i+1
                else:
                    bDoublon = True
                break

        if not bDoublon:  # a activer pour filtrer
        # if True:
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            sDisplayTitle = sremarque + sMovieTitle
            if (oHoster != False):
                # oHoster.setDisplayName(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def ifVSlog(log):
    if bVSlog:
        try:  # si no import VSlog from resources.lib.comaddon
            VSlog(str(log))
        except:
            pass
