# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Par jojotango

import base64
import re
import random

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager, VSlog
from resources.lib.config import GestionCookie
from resources.lib.util import Unquote, cUtil

SITE_IDENTIFIER = 'doc4u'
SITE_NAME = 'Doc4U'
SITE_DESC = 'Documentaires, Sports, Émissions TV et Téléréalités en Français'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

DOC_NEWS = (URL_MAIN + 'doc/', 'showMovies')
DOC_GENRES = (True, 'showGenres')
DOC_DOCS = ('http://', 'showMenuDoc')

REPLAYTV_REPLAYTV = (True, 'showMenuReplay')
REPLAYTV_NEWS = (URL_MAIN + 'genre/reality', 'showMovies')
REPLAYTV_POPULAIRE = (URL_MAIN + 'tvshows/', 'showMovies')
URL_SEARCH_REPLAY = (URL_SEARCH[0], 'showMovies')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires (Nouveautés)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_GENRES[1], 'Documentaires (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Emissions TV (Nouveautés)', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_POPULAIRE[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_POPULAIRE[1], 'Emissions TV (Populaires)', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuDoc():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires (Nouveautés)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_GENRES[1], 'Documentaires (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuReplay():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Emissions TV (Nouveautés)', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_POPULAIRE[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_POPULAIRE[1], 'Emissions TV (Populaires)', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', 'action'])
    liste.append(['Animaux', 'animaux'])
    liste.append(['Auto/Moto', 'auto-moto-2'])
    liste.append(['Aventure', 'aventure'])
    liste.append(['Biographie', 'biographie'])
    liste.append(['Catastrophe', 'catastrophe'])
    liste.append(['Comédie', 'comedie'])
    liste.append(['Crime', 'crime'])
    liste.append(['Cuisine', 'cuisine'])
    liste.append(['Documentaire', 'documentaire'])
    liste.append(['Drame', 'drame'])
    liste.append(['Familial', 'familial'])
    liste.append(['Fantastique', 'fantastique'])
    liste.append(['Guerre', 'guerre'])
    liste.append(['Guerre/Politique', 'war-politics'])
    liste.append(['Histoire', 'histoire'])
    liste.append(['Horreur', 'horreur'])
    liste.append(['Musique', 'musique'])
    liste.append(['Mystère', 'mystere'])
    liste.append(['Nature', 'nature'])
    liste.append(['Politique', 'politique'])
#    liste.append(['Replay TV', 'telefilm'])
    liste.append(['Santé/Bien-etre', 'sante'])
    liste.append(['Société', 'societe'])
    liste.append(['Sport', 'sport'])
    liste.append(['Talk', 'talk'])
    liste.append(['Technologie', 'technologie'])
#    liste.append(['Téléréalite', 'reality'])
    liste.append(['Thriller', 'thriller'])
    liste.append(['Transport', 'auto-moto'])
    liste.append(['Voyage/Decouverte', 'voyage'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'genre/' + sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH[0], '').replace('%20', ' ')
        sUrl = sSearch.replace('%20', '+')
        sPattern = '<img src="([^"]+)" alt="([^"]+)".+?href="([^"]+)".+?<p>([^<]+)'
    else:
        sPattern = 'poster"><img src="([^"]+)" alt="([^"]+).+?(subtitle_mn">|mepo">)([^<]+).+?href="([^"]+).+?class="texto">([^<]+)'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sThumb = aEntry[0]
            sTitle = aEntry[1]
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue  # Filtre de recherche

                sUrl = aEntry[2]
                sDesc = aEntry[3]
            else:
                sPack = aEntry[3]
                sUrl = aEntry[4]
                sDesc = aEntry[5]
                if 'PACK' in sPack:  # toute une saison dans un seul fichier
                    continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'doc.png', sThumb, sDesc, oOutputParameterHandler)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = "<div class=\"pagination\"><span>Page \d+ de (\d+).+?current.+?<a href='([^<]+)' class=\"inactive\">(\d+)<"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = aResult[1][0][2]
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sDisplayTitle = sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # premier type de liens
    sPattern = 'a href="(https:[^"]+)" class="su-button su-button-style-flat".+?</i>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = aEntry[1]

            if "1url" in sUrl:
                oRequestHandler = cRequestHandler(sUrl)
                sHtmlContent = oRequestHandler.request()
                sPattern = '\("href","(http[^"]+)"\)'
                aResultUrl = oParser.parse(sHtmlContent, sPattern)
                if aResultUrl[0]:
                    sHosterUrl = aResultUrl[1][0]
                    if "send.cm" in sHosterUrl:
                        continue

                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        sDisplayTitle = sMovieTitle + ' ' + sTitle.replace("TELECHARGER", "")
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
            # elif "cuty" in sUrl:
            #     oRequestHandler = cRequestHandler(sUrl)
            #     sHtmlContent = oRequestHandler.request()
            #     referer = sUrl
            #     sUrl = oRequestHandler.getRealUrl()
            #     sPattern = '<form id="submit-form" action=".+?value="([^"]+)'
            #
            #     aResultUrl = oParser.parse(sHtmlContent, sPattern)
            #     if aResultUrl[0]:
            #         token = aResultUrl[1][0]
            #
            #         oRequest = cRequestHandler(sUrl)
            #         oRequest.setRequestType(1)
            #         oRequest.addHeaderEntry('Referer', referer)
            #         oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
            #         oRequest.addParametersLine('_token=%s' % token)
            #         sHtmlContent = oRequest.request()

        oGui.setEndOfDirectory()
        return

    # deuxieme type de liens
    sPattern = "<li id='player-option-[0-9]+' class='dooplay_player_option' data-type='([^']+)' data-post='([^']+)' data-nume='([^']+)"
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = geturl(aEntry)

            if 'frembed' in sHosterUrl:
                oRequestHandler = cRequestHandler(sHosterUrl)
                sHtmlContent = oRequestHandler.request()
                sPattern = 'data-link="([^"]+)".+?;">([^<]+)'
                aResult = oParser.parse(sHtmlContent, sPattern)
                if aResult[0]:
                    for aEntry in aResult[1]:
                        sLink = aEntry[0]
                        sHostName = aEntry[1]
                        sLink = base64.b64decode(sLink)
                        sLink = str(sLink).replace("b'", "").replace("'", "")
                        sLink = Unquote(sLink)
                        oHoster = cHosterGui().checkHoster(sHostName)
                        if oHoster:
                            oHoster.setDisplayName(sMovieTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sLink, sThumb)

        oGui.setEndOfDirectory()
        return

    # troisieme type de liens
    sPattern = '<a href="([^"]+)" title=".+?".+?</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:

            # if "send.cm" in sHosterUrl:
            #     oRequestHandler = cRequestHandler(aEntry)
            #     oRequestHandler.addHeaderEntry('User-Agent', UA)
            #     oRequestHandler.addHeaderEntry('Accept', 'application/json, text/javascript, */*; q=0.01')
            #     oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            #     oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
            #     oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
            #     oRequestHandler.request()
            #     oRequestHandler.getRealUrl()

            if "clictune" in aEntry:
                oRequestHandler = cRequestHandler(aEntry)
                sHtmlContent = oRequestHandler.request()

                sPattern = 'txt = \'<b><a href="([^"]+)"'
                aResultTune = oParser.parse(sHtmlContent, sPattern)[1][0]
                aEntry = Unquote(re.search('url=(.+?)&',aResultTune).group(1))

            if "ReviveLink" in aEntry:
                url2 = 'http://' + (aEntry.split('/')[2]).lower() + '/qcap/Qaptcha.jquery.php'
                idUrl = aEntry.split('/')[3]

                # Make random key
                s = "azertyupqsdfghjkmwxcvbn23456789AZERTYUPQSDFGHJKMWXCVBN_-#@"
                RandomKey = ''.join(random.choice(s) for i in range(32))

                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.setRequestType(1)
                oRequestHandler.addHeaderEntry('Host', 'revivelink.com')
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Accept', 'application/json, text/javascript, */*; q=0.01')
                oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
                oRequestHandler.addHeaderEntry('Referer', aEntry)
                oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
                oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
                oRequestHandler.addParameters('action', 'qaptcha')
                oRequestHandler.addParameters('qaptcha_key', RandomKey)

                sHtmlContent = oRequestHandler.request()

                cookies = oRequestHandler.GetCookies()
                GestionCookie().SaveCookie('revivelink.com', cookies)
                # VSlog('result' + sHtmlContent)

                if '"error":false' not in sHtmlContent:
                    VSlog('Captcha rate')
                    VSlog(sHtmlContent)
                    return

                cookies = GestionCookie().Readcookie('revivelink.com')
                oRequestHandler = cRequestHandler('http://revivelink.com/slinks.php?R=' + idUrl + '&' + RandomKey)
                oRequestHandler.addHeaderEntry('Host', 'revivelink.com')
                oRequestHandler.addHeaderEntry('Referer', aEntry)
                oRequestHandler.addHeaderEntry('Accept', 'application/json, text/javascript, */*; q=0.01')
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Accept-Language', 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4')
                oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
                oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
                oRequestHandler.addHeaderEntry('Cookie', cookies)

                sHtmlContent = oRequestHandler.request()

                result = re.findall('<td><a href="([^"]+)" title=\'([^<]+)\'>', sHtmlContent)
                for url, title in result:
                    sHosterUrl = url
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(title)
                        oHoster.setFileName(title)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
            else:

                sHosterUrl = aEntry
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def geturl(aEntry):
    oParser = cParser()

    sPost = aEntry[1]
    sNum = aEntry[2]
    sType = aEntry[0]

    pdata = 'action=doo_player_ajax&post=' + sPost + '&nume=' + sNum + '&type=' + sType

    sUrl = URL_MAIN + 'wp-admin/admin-ajax.php'

    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('User-Agent', UA)
    oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    oRequest.addParametersLine(pdata)

    sHtmlContent = oRequest.request()

    sPattern = 'url":"([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]
    else:
        return ''
