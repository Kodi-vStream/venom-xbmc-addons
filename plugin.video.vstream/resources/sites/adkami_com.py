# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'adkami_com'
SITE_NAME = 'ADKami'
SITE_DESC = 'Bienvenue sur ADKami un site Animés, Mangas & Séries en streaming.'

URL_MAIN = 'https://www.adkami.com/'

ANIM_ANIMS = (True, 'showAnimMenu')
ANIM_NEWS = (URL_MAIN + 'anime', 'showSeries')
ANIM_LIST = (URL_MAIN + 'video?search=&n=&g=&s=&v=&t=0&p=&order=&d1=&d2=&e=&m=&q=&l=', 'showAZ')
ANIM_VIEWS = (URL_MAIN + 'video?search=&t=0&order=3', 'showSeries')

SERIE_SERIES = (True, 'showSerieMenu')
SERIE_NEWS = (URL_MAIN + 'serie', 'showSeries')
SERIE_LIST = (URL_MAIN + 'video?search=&n=&g=&s=&v=&t=1&p=&order=&d1=&d2=&e=&m=&q=&l=', 'showAZ')
SERIE_VIEWS = (URL_MAIN + 'video?search=&t=1&order=3', 'showSeries')

DRAMA_DRAMAS = (True, 'showDramaMenu')
DRAMA_NEWS = (URL_MAIN + 'drama', 'showSeries')
DRAMA_LIST = (URL_MAIN + 'video?search=&n=&g=&s=&v=&t=5&p=&order=&d1=&d2=&e=&m=&q=&l=', 'showAZ')
DRAMA_VIEWS = (URL_MAIN + 'video?search=&t=5&order=3', 'showSeries')

URL_SEARCH = (URL_MAIN + 'video?search=', 'showSeries')
URL_SEARCH_SERIES = (URL_MAIN + 'video?t=1&order=0&search=', 'showSeries')
URL_SEARCH_DRAMAS = (URL_MAIN + 'video?t=5&order=0&search=', 'showSeries')
URL_SEARCH_ANIMS = (URL_MAIN + 'video?t=0&order=0&search=', 'showSeries')
FUNCTION_SEARCH = 'showSeries'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_DRAMAS[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_DRAMAS[1], 'Dramas', 'dramas.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieMenu():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSerie', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Les plus vues)', 'views.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAnimMenu():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchAnim', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_LIST[1], 'Animés (Liste)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VIEWS[1], 'Animés (Les plus vus)', 'views.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showDramaMenu():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchDrama', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_NEWS[1], 'Dramas (Liste)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_LIST[1], 'Dramas (Liste)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DRAMA_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_VIEWS[1], 'Dramas (Les plus vues)', 'dramas.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearchSerie():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH_SERIES[0] + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchAnim():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH_ANIMS[0] + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchDrama():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH_DRAMAS[0] + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenre():
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
    sPattern = '<span class="top"><a href="([^"]+)"><span class="title">([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()

        for aEntry in aResult[1]:

            sUrl2 = aEntry[0]
            sTitle = aEntry[1]  # .decode("unicode_escape").encode("latin-1")

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            if 't=1' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, 'series.png', '', '', oOutputParameterHandler)
            elif 't=5' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, 'dramas.png', '', '', oOutputParameterHandler)
            else:
                oGui.addAnime(SITE_IDENTIFIER, 'showEpisode', sTitle, 'animes.png', '', '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeries(sSearch=''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'class="top">\s*<a href="([^"]+)">\s*<span class="title">([^<]+)'
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

            sUrl2 = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            if 't=1' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, 'series.png', '', '', oOutputParameterHandler)
            elif 't=5' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, 'dramas.png', '', '', oOutputParameterHandler)
            else:
                oGui.addAnime(SITE_IDENTIFIER, 'showEpisode', sTitle, 'animes.png', '', '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
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
    if (aResult[0] == True):
        return aResult[1][0]

    return False


def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    # info anime et serie
    sThumb = ''
    sDesc = ''
    try:
        sPattern = '<img itemprop="image".+?src="([^"]+).+?<strong>(.+?)</strong>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            sThumb = aResult[1][0][0]
            sDesc = aResult[1][0][1]
            sDesc = sDesc.replace('<br />', '')
    except:
        pass

    sPattern = 'line-height:200px;font-size:26px;text-align:center;">L.anime est licencié<.p>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Animé licencié[/COLOR]')

    else:
        sPattern = '<li class="saison">([^<]+)</li>|<a href="(https://www\.adkami\.com[^"]+)"[^<>]+>([^<]+)</a></li>'

        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry in aResult[1]:
                if aEntry[0]:
                    sSaison = aEntry[0].capitalize()
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + sSaison + '[/COLOR]')
                else:
                    sUrl = aEntry[1]
                    sEpisode = aEntry[2]
                    sTitle = sMovieTitle + ' ' + sSaison + ' ' + sEpisode
                    sTitle = re.sub(' vf', ' (VF)', sTitle, re.IGNORECASE)
                    sDisplayTitle = re.sub(' vostfr', ' (VOSTFR)', sTitle, re.IGNORECASE)
                    sTitle = sDisplayTitle.replace(' (VF)', '').replace(' (VOSTFR)', '')

                    oOutputParameterHandler.addParameter('siteUrl', sUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oOutputParameterHandler.addParameter('sDesc', sDesc)

                    oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'video-iframe.+?data-url="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not aResult[0]:
        sPattern = '<iframe.+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

    oOutputParameterHandler = cOutputParameterHandler()
    for aEntry in aResult[1]:
        sUrl = aEntry.replace('+', 'plus')
        try:
            sUrl = decodex(sUrl)
        except Exception:
            pass

        if sUrl.startswith('//'):
            sUrl = 'https:' + sUrl

        if 'www.' in sUrl:
            sHost = sUrl.split("/")[2].split('.')[1]
        else:
            sHost = sUrl.split("/")[2].split('.')[0]

        if sHost:
            if "crunchyroll" in str(sHost) or "wakanim" in str(sHost) or "animedigitalnetwork" in str(sHost):
                sTitle = "[COLOR red]Licencié par : %s [/COLOR]" % str(sHost)
            else:
                sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost.capitalize())
        else:
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, 'Inconnu')

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    # bidouille facile
    sUrl = sUrl.replace('plus', '+')
    sHosterUrl = sUrl

    if sHosterUrl:
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')

    oGui.setEndOfDirectory()


def decodex(x):
    from itertools import chain
    import base64

    e = base64.b64decode(x.replace('https://www.youtube.com/embed/', ''))
    t = ''
    r = "ETEfazefzeaZa13MnZEe"
    a = 0

    px = chain(e)
    for y in list(px):
        t += chr(int(175 ^ ord(y[0])) - ord(r[a]))
        a = 0 if a > len(r) - 2 else a + 1
    return t
