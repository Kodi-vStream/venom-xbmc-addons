# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager
from resources.lib.util import Quote

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

SITE_IDENTIFIER = 'voiranime'
SITE_NAME = 'VoirAnime'
SITE_DESC = 'Animés en Streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = (True, 'load')
ANIM_NEWS = (URL_MAIN, 'showAnimes')
ANIM_VOSTFRS = (URL_MAIN + '?filter=subbed', 'showAnimes')
ANIM_VFS = (URL_MAIN + '?filter=dubbed', 'showAnimes')
ANIM_GENRES = (URL_MAIN + 'anime-genre/', 'showGenres')
ANIM_ALPHA = (URL_MAIN + 'liste-danimes/?start=', 'showAlpha')

FUNCTION_SEARCH = 'showAnimes'
URL_SEARCH = (URL_MAIN + '?post_type=wp-manga&m_orderby=views', 'showAnimes')
URL_SEARCH_ANIMS = (URL_SEARCH[0] + '&s=', 'showAnimes')

URL_SEARCH_VOSTFR = (URL_SEARCH[0] + '&language=vostfr&s=', 'showAnimes')
URL_SEARCH_VF = (URL_SEARCH[0] + '&language=vf&s=', 'showAnimes')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche d\'animés (VOSTFR)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_VF[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche d\'animés (VF)', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Par genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ALPHA[1], 'Animés (Par ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sUrl = sUrl + Quote(sSearchText)
        showAnimes(sUrl)
        oGui.setEndOfDirectory()
        return


def showAlpha():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    progress_ = progress().VScreate(SITE_NAME)

    oOutputParameterHandler = cOutputParameterHandler()
    for i in range(-1, 27):
        progress_.VSupdate(progress_, 36)

        if i == -1:
            sTitle = 'ALL'
            oOutputParameterHandler.addParameter('siteUrl', sUrl.replace('?start=', ''))
        elif i == 0:
            sTitle = '#'
            oOutputParameterHandler.addParameter('siteUrl', sUrl + 'non-char')
        else:
            sTitle = chr(64 + i)
            oOutputParameterHandler.addParameter('siteUrl', sUrl + sTitle)

        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showAnimes', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'az.png', oOutputParameterHandler)

    progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append(['Action', sUrl + 'action/'])
    liste.append(['Aventure', sUrl + 'adventure/'])
    liste.append(['Chinois', sUrl + 'chinese/'])
    liste.append(['Comédie', sUrl + 'comdey/'])
    liste.append(['Drama', sUrl + 'drama/'])
    liste.append(['Ecchi', sUrl + 'ecchi/'])
    liste.append(['Fantastique', sUrl + 'fantasy/'])
    liste.append(['Horreur', sUrl + 'horror/'])
    liste.append(['Mahou Shoujo', sUrl + 'mahou-shoujo/'])
    liste.append(['Mécha', sUrl + 'mecha/'])
    liste.append(['Musique', sUrl + 'music/'])
    liste.append(['Mystère', sUrl + 'mystery'])
    liste.append(['Psychologie', sUrl + 'psychological/'])
    liste.append(['Romance', sUrl + 'romance/'])
    liste.append(['Sci-Fi', sUrl + 'sci-fi/'])
    liste.append(['Trance de vie', sUrl + 'slice-of-life/'])
    liste.append(['Sports', sUrl + 'sports/'])
    liste.append(['Surnaturel', sUrl + 'supernatural/'])
    liste.append(['Thriller', sUrl + 'thriller/'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showAnimes', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAnimes(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch

        sTypeSearch = oParser.parseSingleResult(sUrl, '\?type=(.+?)&')
        if sTypeSearch[0]:
            sTypeSearch = sTypeSearch[1]
        else:
            sTypeSearch = False

        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        sHtmlContent = oRequest.request()
        sPattern = '<a href="([^"]+)" title="([^"]+)".+?src="([^"]+)".+?Type.+?content.+?>([^<]+)'

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = '<div class="page-item-detail video">.+?a href="([^"]+)" title="([^"]+)".+?src="([^"]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            if 'http' not in sUrl:
                sUrl = URL_MAIN[:-1] + sUrl

            sTitle = aEntry[1].replace('film ', '').replace(' streaming', '')
            sThumb = aEntry[2]
            if 'http' not in sThumb:
                sThumb = URL_MAIN + sThumb

            if 'VOSTFR' in sTitle:
                sTitle = sTitle.replace('VOSTFR', '')
                sLang = 'VOSTFR'
            elif 'VF' in sTitle:
                sTitle = sTitle.replace('VF', '')
                sLang = 'VF'
            else:
                sLang = 'VOSTFR'

            sDisplayTitle = '%s (%s)' % (sTitle, sLang)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addAnime(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, sThumb, sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage != False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            number = re.findall('([0-9]+)', sNextPage)[-1]
            oGui.addNext(SITE_IDENTIFIER, 'showAnimes', 'Page ' + number, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="nextpostslink".+?href="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0] is True:
        return aResult[1][0]

    return False


def showEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<div class="summary__content ">.+?<p>([^<]+)'  # recup description
    aResult = oParser.parse(sHtmlContent, sPattern)

    sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[0])

    sPattern = '<li class="wp-manga-chapter.+?="([^"]+)".+?([^<]+)'  # Recup lien + titre
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is False:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()

        # Dernier épisode
        sUrlEpisode = aResult[1][0][0]
        sTitle = aResult[1][0][1]

        oOutputParameterHandler.addParameter('siteUrl', sUrlEpisode)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', '===] Dernier épisode [===', '', sThumb, sDesc, oOutputParameterHandler)

        # Premier épisode
        sUrlEpisode = aResult[1][-1][0]
        sTitle = aResult[1][-1][1]

        oOutputParameterHandler.addParameter('siteUrl', sUrlEpisode)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', '===] Premier épisode [===', '', sThumb, sDesc, oOutputParameterHandler)

        # Liste des épisodes
        for aEntry in aResult[1]:
            sUrlEpisode = aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrlEpisode)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # Les elements post.
    data = re.search('data-action="bookmark" data-post="([^"]+)" data-chapter="([^"]+)"', sHtmlContent)
    post = data.group(1)
    chapter = data.group(2)

    # On extrait une partie de la page pour eviter les doublons.
    sData = re.search('<select class="selectpicker host-select">(.+?)</select> </label>', sHtmlContent, re.MULTILINE | re.DOTALL).group(1)

    oParser = cParser()
    sPattern = '<option data-redirect=.+?value="([^"]+)">LECTEUR.+?</option>'

    aResult = oParser.parse(sData, sPattern)

    if aResult[0] is True:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sTitle = sMovieTitle + aEntry

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', 'salut')
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sPost', post)
            oOutputParameterHandler.addParameter('sChapter', chapter)
            oOutputParameterHandler.addParameter('sType', aEntry)

            oGui.addEpisode(SITE_IDENTIFIER, 'RecapchaBypass', sTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def RecapchaBypass():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    post = oInputParameterHandler.getValue('sPost')
    chapter = oInputParameterHandler.getValue('sChapter')
    types = oInputParameterHandler.getValue('sType')

    # La lib qui gere recaptcha
    from resources.lib import librecaptcha
    test = librecaptcha.get_token(api_key="6Ld2q9gUAAAAAP9vNl23kYuST72fYsu494_B2qaZ", site_url=sUrl,
                                  user_agent=UA, gui=False, debug=False)

    if test is None:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]Resolution du Recaptcha annulé[/COLOR]')

    else:
        # N'affiche pas directement le liens car sinon Kodi crash.
        sDisplayTitle = "Recaptcha passé avec succès, cliquez pour afficher les liens"
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('Token', test)
        oOutputParameterHandler.addParameter('sPost', post)
        oOutputParameterHandler.addParameter('sChapter', chapter)
        oOutputParameterHandler.addParameter('sType', types)
        oGui.addEpisode(SITE_IDENTIFIER, 'getHost', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def getHost():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    test = oInputParameterHandler.getValue('Token')
    post = oInputParameterHandler.getValue('sPost')
    chapter = oInputParameterHandler.getValue('sChapter')
    types = oInputParameterHandler.getValue('sType')

    # On valide le token du coté du site
    data = 'action=get_video_chapter_content&grecaptcha=' + test + '&manga=' + post + '&chapter=' + chapter + '&host=' + types.replace(' ', '+')
    oRequestHandler = cRequestHandler("https://voiranime.com/wp-admin/admin-ajax.php")
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip')
    oRequestHandler.addHeaderEntry('Referer', sUrl)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Content-Length', len(str(data)))
    oRequestHandler.addParametersLine(data)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<iframe src="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] is True:

        for aEntry in aResult[1]:
            sHosterUrl = aEntry.replace('\\', '').replace('\\/', '/')
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()
