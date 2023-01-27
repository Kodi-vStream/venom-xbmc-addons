# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import progress, isMatrix, siteManager
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'adkami_com'
SITE_NAME = 'ADKami'
SITE_DESC = 'Animés & Dramas en streaming.'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = (True, 'showAnimMenu')
ANIM_NEWS = (URL_MAIN + 'anime', 'showSeries')
ANIM_LIST = (URL_MAIN + 'video?search=&n=&g=&s=&v=&t=0&p=&order=&d1=&d2=&e=&m=&q=&l=', 'showAZ')
ANIM_VIEWS = (URL_MAIN + 'video?search=&t=0&order=3', 'showSeries')

DRAMA_DRAMAS = (True, 'showDramaMenu')
DRAMA_LIST = (URL_MAIN + 'video?search=&n=&g=&s=&v=&t=5&p=&order=&d1=&d2=&e=&m=&q=&l=', 'showAZ')
DRAMA_VIEWS = (URL_MAIN + 'video?search=&t=5&order=3', 'showSeries')

URL_SEARCH = (URL_MAIN + 'video?search=', 'showSeries')
URL_SEARCH_ANIMS = (URL_MAIN + 'video?t=0&order=0&search=', 'showSeries')
URL_SEARCH_DRAMAS = (URL_MAIN + 'video?t=5&order=0&search=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_DRAMAS[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_DRAMAS[1], 'Dramas', 'dramas.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAnimMenu():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchAnim', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_LIST[1], 'Animés (Liste alphabétique)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VIEWS[1], 'Animés (Populaire)', 'views.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showDramaMenu():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchDrama', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_LIST[1], 'Dramas (Liste alphabétique)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_VIEWS[1], 'Dramas (Populaire)', 'views.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearchSerie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH_SERIES[0] + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchAnim():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH_ANIMS[0] + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchDrama():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH_DRAMAS[0] + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sType2 = oInputParameterHandler.getValue('type2')

    liste = []
    liste.append(['Action', URL_MAIN + 'video?recherche=&genre3=1&type2=' + sType2])
    liste.append(['Aventure', URL_MAIN + 'video?recherche=&genre3=2&type2=' + sType2])
    liste.append(['Amour & Amitié', URL_MAIN + 'video?recherche=&genre3=3&type2=' + sType2])
    liste.append(['Combat', URL_MAIN + 'video?recherche=&genre3=4&type2=' + sType2])
    liste.append(['Comédie', URL_MAIN + 'video?recherche=&genre3=5&type2=' + sType2])
    liste.append(['Contes & Récits', URL_MAIN + 'video?recherche=&genre3=6&type2=' + sType2])
    liste.append(['Cyber & Mecha', URL_MAIN + 'video?recherche=&genre3=7&type2=' + sType2])
    liste.append(['Dark Fantasy', URL_MAIN + 'video?recherche=&genre3=8&type2=' + sType2])
    liste.append(['Drame', URL_MAIN + 'video?recherche=&genre3=9&type2=' + sType2])
    liste.append(['Ecchi', URL_MAIN + 'video?recherche=&genre3=10&type2=' + sType2])
    liste.append(['Éducatif', URL_MAIN + 'video?recherche=&genre3=11&type2=' + sType2])
    liste.append(['Énigme & Policier', URL_MAIN + 'video?recherche=&genre3=12&type2=' + sType2])
    liste.append(['Épique & Héroique', URL_MAIN + 'video?recherche=&genre3=13&type2=' + sType2])
    liste.append(['Espace & Sci-Fiction', URL_MAIN + 'video?recherche=&genre3=14&type2=' + sType2])
    liste.append(['Familial & Jeunesse', URL_MAIN + 'video?recherche=&genre3=15&type2=' + sType2])
    liste.append(['Fantastique & Mythe', URL_MAIN + 'video?recherche=&genre3=16&type2=' + sType2])
    liste.append(['Hentai', URL_MAIN + 'video?recherche=&genre3=17&type2=' + sType2])
    liste.append(['Historique', URL_MAIN + 'video?recherche=&genre3=18&type2=' + sType2])
    liste.append(['Horreur', URL_MAIN + 'video?recherche=&genre3=19&type2=' + sType2])
    liste.append(['Magical Girl', URL_MAIN + 'video?recherche=&genre3=20&type2=' + sType2])
    liste.append(['Musical', URL_MAIN + 'video?recherche=&genre3=21&type2=' + sType2])
    liste.append(['Psychologique', URL_MAIN + 'video?recherche=&genre3=22&type2=' + sType2])
    liste.append(['Sport', URL_MAIN + 'video?recherche=&genre3=23&type2=' + sType2])
    liste.append(['Tranche de vie', URL_MAIN + 'video?recherche=&genre3=24&type2=' + sType2])
    liste.append(['Shôjo-Ai', URL_MAIN + 'video?recherche=&genre3=25&type2=' + sType2])
    liste.append(['Shônen-Ai', URL_MAIN + 'video?recherche=&genre3=26&type2=' + sType2])
    liste.append(['Yaoi/BL', URL_MAIN + 'video?recherche=&genre3=27&type2=' + sType2])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAZ():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    # pas d'url pour les non alpha, on utilise l'ancienne méthode épurée.
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addDir(SITE_IDENTIFIER, 'showNoAlpha', '[COLOR teal] Lettre [COLOR red]123[/COLOR]', 'az.png', oOutputParameterHandler)

    import string
    for i in string.ascii_lowercase:
        sUrl2 = sUrl + str(i)

        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal] Lettre [COLOR red]' + str(i).upper() + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showNoAlpha():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Decoupage pour cibler la partie non alpha
    sPattern = 'class="video-item-list-days"><h5>Lettre 123</h5>(.+?)<div id="A"'
    sHtmlContent = oParser.parse(sHtmlContent, sPattern)

    # regex pour listage sur la partie decoupée
    sPattern = 'data-original="([^"]+)".+?<span class="top"><a href="([^"]+)"><span class="title">([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()

        for aEntry in aResult[1]:

            sThumb = aEntry[0]
            sUrl2 = aEntry[1]
            sTitle = aEntry[2]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 't=1' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaison', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            elif 't=5' in sUrl:
                oGui.addDrama(SITE_IDENTIFIER, 'showSaison', sTitle, 'dramas.png', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addAnime(SITE_IDENTIFIER, 'showSaison', sTitle, 'animes.png', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeries(sSearch=''):
    oGui = cGui()
    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_ANIMS[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_DRAMAS[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'data-original="([^"]+)".+?class="top">.+?<a href="([^"]+)">.+?<span class="title">([^<]+)'
    aResult = re.findall(sPattern, sHtmlContent, re.DOTALL)

    if not aResult:
        oGui.addText(SITE_IDENTIFIER)
    else:
        total = len(aResult)
        progress_ = progress().VScreate(SITE_NAME, large=total > 50)
        oOutputParameterHandler = cOutputParameterHandler()

        for aEntry in aResult:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            sUrl2 = aEntry[1]
            sTitle = aEntry[2]

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if 't=1' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaison', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)
            elif 't=5' in sUrl:
                oGui.addDrama(SITE_IDENTIFIER, 'showSaison', sTitle, 'dramas.png', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addAnime(SITE_IDENTIFIER, 'showSaison', sTitle, 'animes.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage is not False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            sNumPage = re.search('page=([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', 'Page ' + sNumPage, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<button class=\'actuel\'>[0-9]+</button><a href="([^"]+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return aResult[1][0]

    return False


def showSaison():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    # info anime et serie
    sDesc = ''
    try:
        sPattern = '<p class="description.+?">([^<]+)<a title'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
            sDesc = sDesc.replace('<br />', '').replace('&apos;', '\'')
    except:
        pass

    sPattern = 'line-height:200px;font-size:26px;text-align:center;">L.anime est licencié<.p>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Animé licencié[/COLOR]')

    else:
        sPattern = '<li class="saison">.+?(\d+)<\/li>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:

                sNumSaison = aEntry[0]
                sSaison = 'Saison ' + aEntry[0]
                sUrlSaison = sUrl + "?sNumSaison=" + sNumSaison
                sDisplayTitle = sMovieTitle + ' ' + sSaison
                sTitle = sMovieTitle

                oOutputParameterHandler.addParameter('siteUrl', sUrlSaison)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)

                oGui.addSeason(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    sUrl, sNumSaison = sUrl.split('?sNumSaison=')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'line-height:200px;font-size:26px;text-align:center;">L.anime est licencié<.p>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Animé licencié[/COLOR]')

    else:
        sStart = 'class="saison">saison ' + sNumSaison
        sEnd = '<div class="saison-container">'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
        sPattern = '<a href="(https://www\.adkami\.com[^"]+)"[^<>]+>([^<]+)</a></li>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
                sUrl = aEntry[0]
                sEpisode = aEntry[1]
                Saison = 'Saison ' + sNumSaison
                sTitle = sMovieTitle + ' ' + Saison + ' ' + sEpisode
                sTitle = re.sub(' vf', ' (VF)', sTitle, re.IGNORECASE)
                sDisplayTitle = re.sub(' vostfr', ' (VOSTFR)', sTitle, re.IGNORECASE)

                sLang = ''
                if '(VOSTFR)' in sDisplayTitle:
                    sLang = 'VOSTFR'
                elif '(VF)' in sDisplayTitle:
                    sLang = 'VF'

                sTitle = sDisplayTitle.replace(' (VF)', '').replace(' (VOSTFR)', '')

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sLang', sLang)

                oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sPattern = '<div class="video-iframe.+?url="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not aResult[0]:
        sPattern = 'class="video-video">.+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

    if "crunchyroll" in str(sHtmlContent) or "wakanim" in str(sHtmlContent) or "animedigitalnetwork" in str(sHtmlContent):
        sPattern = 'encrypted-media.+?src="([^"]+)"'
        aResult2 = oParser.parse(sHtmlContent, sPattern)

        if not aResult[0]:
            aResult = aResult2
        else:
            if aResult2[0]:
                f = aResult[1] + aResult2[1]
                aResult[1] = f

    for aEntry in aResult[1]:

        sUrl = aEntry.replace('+', 'plus')
        if 'youtube' in sUrl and 'hl=fr' not in sUrl:
            sUrl = decodex(sUrl)

        if sUrl.startswith('//'):
            sUrl = 'https:' + sUrl

        sHosterUrl = sUrl.replace('plus', '+')
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def decodex(x):
    from itertools import chain
    import base64

    x = x.replace('https://www.youtube.com/embed/', '')

    missing_padding = len(x) % 4
    if missing_padding:
        x += '=' * (4 - missing_padding)

    try:
        e = base64.b64decode(x)
        t = ''
        r = "ETEfazefzeaZa13MnZEe"
        a = 0

        px = chain(e)
        for y in list(px):
            if isMatrix():
                t += chr(int(175 ^ y) - ord(r[a]))
            else:
                t += chr(int(175 ^ ord(y[0])) - ord(r[a]))
            a = 0 if a > len(r) - 2 else a + 1
        return t
    except:
        return ''

    return ''
