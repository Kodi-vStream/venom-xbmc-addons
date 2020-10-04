# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 03 update 04/10/2020

import re
import xbmc

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog

# Liens 'not found' pour 3 raisons connues
# Courants:
# 1 Liens register ;notification dans le hoster.displaytitle
# 2 Erreur 521, CF n'as pas réussi à se connecter au site (addtext)
# Rares:
# 3 Blocked :il faut essayer de changer son ip : xbmc notification:  ;

bVSlog = False

SITE_IDENTIFIER = 'filmstoon_pro'
SITE_NAME = 'Films toon'
SITE_DESC = 'Films en streaming'

URL_MAIN = 'https://ww.filmstoon.cam/'

# globales
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')
MOVIE_VIEWS = (URL_MAIN + 'film/populaire/', 'showMovies')
MOVIE_MOVIE = (True, 'load')

URL_SEARCH = (URL_MAIN + '?do=search&subaction=search&story=', 'showMovies')
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
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'genres.png', oOutputParameterHandler)

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
    #liste.append(['Action', URL_MAIN + '/action/'])  # marche aussi
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
    for i in reversed(range(1971, 2021)):
        sYear = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + sYear + '/')  # / inutile
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sYear, 'annees.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    if sSearch:
        sUrl = sSearch
        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
        sHtmlContent = oRequest.request()
        # url thumb tile desc
        sPattern = '<a class="sres-wrap.+?ref="([^"]*).+?data-src="([^"]*).+?alt="([^"]*).+?desc">([^<]*)'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        # url  title thumb desc
        sPattern = '<div class="s-top fx-row">.+?ref="([^"]+)">(.+?)<.+?data-src="([^"]+).+?st-desc">(.+?)<.div'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)
        ifVSlog('showMovies : Failed Pattern with url = ' + sUrl)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sDesc = aEntry[3]
            if sSearch:
                sTitle = aEntry[2]
                sThumb = aEntry[1]
            else:
                sTitle = aEntry[1]
                sThumb = aEntry[2]
            if 'https:' not in sThumb:
                sThumb = 'https:' + sThumb

            # ifVSlog('sUrl2 =' + sUrl)
            # ifVSlog('sTitle =' + sTitle)
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        NextPage = __checkForNextPage(sHtmlContent)
        if (NextPage != False):
            sNumLastPage = NextPage[0]
            sUrlNextPage = NextPage[1]
            if 'http' not in sUrlNextPage:
                sUrlNextPage = URL_MAIN[:-1] + sUrlNextPage
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrlNextPage)
            number = re.search('/page/([0-9]+)', sUrlNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + number + '/' + sNumLastPage + ' >>>[/COLOR]', oOutputParameterHandler)

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

    ifVSlog('showHosters : sUrl = ' + sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'playfst.php.([^"]*).p='

    # exemple
    # tl=Jumbo&yr=2020&im=tt6818118&butm=f8amdzps8q1k&sv=ms&sr=fst&ni=259782&fc=37290a4f2d42347bce34d609e8e0e01f
    # g1: parametres de la requete que l'on va copier et echanger
    # avec celle genérée normalement par https://easyplayer.cc/player.php? c'est quasiment la meme

    sHosterUrllist = []
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        # ifVSlog(sHtmlContent)
        ifVSlog('Failed Pattern with url = ' + sUrl)
        # ifVSlog('Selected Pattern = ' + sPattern)
        if 'Your IP-address or subnet have been blocked' in sHtmlContent:
            xbmc.executebuiltin('Notification(%s, %s, %d)' % ('Filmstoon Plugin ', 'You have been blocked : Try change your IP-address ', 5000))
        if '521 Origin Down' in sHtmlContent:
            oGui.addText(SITE_IDENTIFIER,' Connexion au serveur impossible')
        else:
            oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            req = 'https://easyplayer.cc/player.php?' + str(aEntry)
            ifVSlog(req)
            oRequestHandler = cRequestHandler(req)
            oRequestHandler.request()
            sHeader = oRequestHandler.getResponseHeader()
            bDoublon = False  # on verifie si url embed en double (mystrem)
            sremarque = ''

            if 'refresh' in sHeader:
                sHosterUrl = sHeader.getheader('refresh')
                ifVSlog('header ' + sHosterUrl)
                sHosterUrl = sHosterUrl.split(';')
                sHosterUrl = sHosterUrl[1]
                sHosterUrl = sHosterUrl.replace('url=', '')

                # ne marche pas : url = https://filmstreaming1.red/registred.php?
                if 'registred' in sHosterUrl:
                    sremarque = '[ Find register link !  ] '

                ifVSlog('header url=' + sHosterUrl)
                if sHosterUrl not in sHosterUrllist:
                    sHosterUrllist.append(sHosterUrl)
                else:
                    bDoublon = True

            if not bDoublon:
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                sDisplayTitle = sremarque + sMovieTitle
                if (oHoster != False):
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
