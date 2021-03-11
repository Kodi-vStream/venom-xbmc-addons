# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

"""
Pour rappel.
Problème avec les DNS en ipv6 il faut utiliser les suivantes
CloudFlare DNS:
Préféré : 2606:4700:4700::1111
Auxiliaire : 2606:4700:4700::1001
Ou:
Google DNS:
Préféré : 2001:4860:4860::8888
Auxiliaire : 2001:4860:4860::8844
"""

import re
import xbmc

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, dialog
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'series_en_streaming'
SITE_NAME = 'Series-en-Streaming'
SITE_DESC = 'Séries & Animés en Streaming'

URL_MAIN = 'https://ww1.series-en-streaming.xyz/'

SERIE_SERIES = ('http://', 'load')
SERIE_NEWS = (URL_MAIN + 'category/series/?orderby=date', 'showMovies')
SERIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(URL_SEARCH[0] + sSearchText)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    sUrl = URL_MAIN

    liste = []
    liste.append(['Action', sUrl + 'category/series/action/'])
    liste.append(['Animation', sUrl + 'category/series/animation/'])
    liste.append(['Arts Martiaux', sUrl + 'category/series/arts-martiaux/'])
    liste.append(['Aventure', sUrl + 'category/series/aventure/'])
    liste.append(['Biopic', sUrl + 'category/series/biopic/'])
    liste.append(['Classique', sUrl + 'category/series/classique/'])
    liste.append(['Comédie', sUrl + 'category/series/comedie/'])
    liste.append(['Comédie dramatique', sUrl + 'category/series/comedie-dramatique/'])
    liste.append(['Comédie musicale', sUrl + 'category/series/comedie-musicale/'])
    liste.append(['Dessin animés', sUrl + 'category/series/dessin-anime/'])
    liste.append(['Divers', sUrl + 'category/series/divers/'])
    liste.append(['Documentaire', sUrl + 'category/series/documentaire/'])
    liste.append(['Drama', sUrl + 'category/series/drama/'])
    liste.append(['Drame', sUrl + 'category/series/drame/'])
    liste.append(['Epouvante-Horreur', sUrl + 'category/series/epouvante-horreur/'])
    liste.append(['Espionnage', sUrl + 'category/series/espionnage/'])
    liste.append(['Famille', sUrl + 'category/series/famille/'])
    liste.append(['Fantastique', sUrl + 'category/series/fantastique/'])
    liste.append(['Guerre', sUrl + 'category/series/guerre/'])
    liste.append(['Historique', sUrl + 'category/series/historique/'])
    liste.append(['Judiciaire', sUrl + 'category/series/judiciaire/'])
    liste.append(['Médical', sUrl + 'category/series/medical/'])
    liste.append(['Musical', sUrl + 'category/series/musical/'])
    liste.append(['Péplum', sUrl + 'category/series/peplum/'])
    liste.append(['Policier', sUrl + 'category/series/policier/'])
    liste.append(['Romance', sUrl + 'category/series/romance/'])
    liste.append(['Science-fiction', sUrl + 'category/series/science-fiction/'])
    liste.append(['Soap', sUrl + 'category/series/soap/'])
    liste.append(['Thriller', sUrl + 'category/series/thriller/'])
    liste.append(['Webséries', sUrl + 'category/series/webserie/'])
    liste.append(['Western', sUrl + 'category/series/western/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="video\s.+?href="([^"]+).+?class="izimg".+?src="([^"]+).+?title="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sTitle = aEntry[2].replace(' Streaming', '')

            sThumb = aEntry[1]
            if not sThumb.startswith('http'):
                sThumb = URL_MAIN + sThumb

            # tris search
            if sSearch and total > 3:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), sTitle) == 0:
                    continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'ShowEpisode', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '>([^<]+)</a></div><span class="son bg"><a href="([^"]+)" *>Suivante'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def ShowEpisode():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # récupération des Synopsis
    sDesc = ''
    try:
        sPattern = '<b>Synopsis :</b>(.+?)</p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
            sDesc = sDesc.replace('\\', '')
    except:
        pass

    sPattern = '<a href="([^"]+)" class="post-page-numbers".+?<span>([^<>]+)</span></a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = sMovieTitle + ' episode ' + aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<span class="lg">(.+?)</span>|myLecteur">Lecteur (?:<b>)*([a-z]+)(?:</b>)* *:</span> <a href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                sLang = aEntry[0].replace('Langue(', 'Langue (')
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + sLang + '[/COLOR]')
            else:
                sHost = aEntry[1].capitalize()
                sUrl = aEntry[2]
                if sUrl.startswith('/'):
                    sUrl = URL_MAIN[:-1] + sUrl

                sDisplayTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sHosterUrl = protectStreamByPass(sUrl)
    oHoster = cHosterGui().checkHoster(sHosterUrl)

    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def protectStreamByPass(url):

    # lien commencant par VID_
    Codedurl = url
    oRequestHandler = cRequestHandler(Codedurl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'var k=\"([^<>\"]*?)\";'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        postdata = 'k=' + aResult[1][0]

        dialog().VSinfo('Décodage en cours', "Patientez", 5)
        xbmc.sleep(5000)

        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'

        oRequest = cRequestHandler(URL_MAIN + 'embed_secur.php')
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', UA)
        # oRequest.addHeaderEntry('Host', 'www.protect-stream.com')
        oRequest.addHeaderEntry('Referer', Codedurl)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequest.addParametersLine(postdata)
        sHtmlContent = oRequest.request()

        # Test de fonctionnement
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            dialog().VSinfo('Lien encore protégé', "Erreur", 5)
            return ''

        # recherche du lien embed
        sPattern = '<iframe src=["\']([^<>"\']+?)["\']'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        # recherche d'un lien redirigé
        sPattern = '<a class=.button. href=["\']([^<>"\']+?)["\'] target=._blank.>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

    return ''
