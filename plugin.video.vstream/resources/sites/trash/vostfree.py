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

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'

SITE_IDENTIFIER = 'vostfree'
SITE_NAME = 'Vostfree'
SITE_DESC = 'anime en streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

URL_SEARCH = (URL_MAIN + '?do=search&subaction=search&speedsearch=1&story=', 'showMovies')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'films-vf-vostfr/', 'showMovies')

ANIM_ANIMS = ('http://', 'load')
ANIM_NEWS = (URL_MAIN + 'lastnews/', 'showMovies')
ANIM_VFS = (URL_MAIN + 'animes-vf/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'animes-vostfr/', 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovies(sSearch=''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if sSearch:
        sUrl = sSearch.replace(' ', '+')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if sSearch:
        sPattern = '<span class="image"><img src="([^"]+)" alt="([^"]+).+?<a href="([^"]+).+?desc">([^<]+)'
    elif '/films-vf-vostfr/' in sUrl:
        sPattern = 'href="([^"]+)" alt="([^"]+).+?src="([^"]+).+?desc">([^<]+)'
    else:
        sPattern = 'href="([^"]+)" alt="([^"]+).+?src="([^"]+).+?desc">([^<]+).+?</i>Saison</span><b>([^<]+).+?Ep</span><b>([^<]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if sSearch:
                sThumb = aEntry[0]
                if 'http' not in sThumb:
                    sThumb = URL_MAIN + sThumb
                sUrl2 = aEntry[2]
            else:
                sUrl2 = aEntry[0]
                sThumb = aEntry[2]
                if 'http' not in sThumb:
                    sThumb = URL_MAIN + sThumb

            sMovieTitle = aEntry[1]
            sDesc = aEntry[3]

            sLang = ''
            if 'FRENCH' in sMovieTitle or 'French' in sMovieTitle:
                sLang = 'VF'
            if 'VOSTFR' in sMovieTitle:
                sLang = 'VOSTFR'

            sMovieTitle = sMovieTitle.replace(' VOSTFR', '').replace(' FRENCH', '').replace(' French', '')
            sDisplayTitle = sMovieTitle + ' (' + sLang + ')'
            if len(aEntry) > 4:
                sDisplayTitle = sDisplayTitle + ' S' + aEntry[4] + ' E' + aEntry[5]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addAnime(SITE_IDENTIFIER, 'seriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>([^<]+)</a>\s*</div>\s*<a href="([^"]+)">\s*<span class="next-page">Suivant</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        sNumberNext = re.search('/page/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def seriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    url = URL_MAIN + 'templates/Animix/js/anime.js'

    oRequestHandler = cRequestHandler(url)
    playerContent = oRequestHandler.request()

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # On récupère l'id associé à l'épisode
    sPattern = '<option value="buttons_([0-9]+)">([^<]+)</option>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    epNumber = ''
    sHosterUrl = ''
    if aResult[0]:
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            # Streaming
            sTitle = sMovieTitle + ' ' + aEntry[1]
            if epNumber != aEntry[1]:
                epNumber = aEntry[1]
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + epNumber + '[/COLOR]')

            # On récupère l'info du player
            sPattern = '<div id="buttons_' + aEntry[0] + '" class="button_box">(.+?)/div></div>'
            htmlCut = oParser.parse(sHtmlContent, sPattern)[1][0]

            sPattern = '<div id="player_([0-9]+)".+?class="new_player_([^"]+)'
            data = oParser.parse(htmlCut, sPattern)

            for aEntry1 in data[1]:

                sPattern = '<div id="content_player_' + aEntry1[0] + '" class="player_box">([^<]+)</div>'
                playerData = oParser.parse(sHtmlContent, sPattern)[1][0]

                if 'http' not in playerData:
                    sPattern = 'player_type[^;]*=="new_player_' + aEntry1[1].lower() + '"\|.+?(?:src=\\\\")([^"]*).*?player_content.*?"([^\\\\"]*)'
                    aResult2 = oParser.parse(playerContent, sPattern)
                    if aResult2[0] is True:
                        sHosterUrl = aResult2[1][0][0] + playerData + aResult2[1][0][1]
                        if 'http' not in sHosterUrl:
                            sHosterUrl = 'https:' + sHosterUrl

                else:
                    sHosterUrl = playerData

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            sPattern = '<div class="lien-episode">.+?<b>' + epNumber + '<.+?href="([^"]+).+?<b>([^<]+)<'
            ddlData = oParser.parse(sHtmlContent, sPattern)

            oOutputParameterHandler = cOutputParameterHandler()
            for aEntry2 in ddlData[1]:
                sTitle = sMovieTitle + ' ' + epNumber + ' ' + aEntry2[1]
                url = aEntry2[0]

                if 'ouo' in url:
                    oOutputParameterHandler.addParameter('siteUrl', url)
                    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                    oOutputParameterHandler.addParameter('sThumb', sThumb)
                    oGui.addLink(SITE_IDENTIFIER, 'DecryptOuo', sTitle, sThumb, '', oOutputParameterHandler)
                else:
                    sHosterUrl = url
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if oHoster:
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
    oGui.setEndOfDirectory()


def DecryptOuo():
    from resources.lib.recaptcha import ResolveCaptcha
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    urlOuo = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if '/fbc/' not in urlOuo:
        urlOuo = urlOuo.replace('io/', 'io/fbc/').replace('press/', 'press/fbc/')

    oRequestHandler = cRequestHandler(urlOuo)
    sHtmlContent = oRequestHandler.request()
    Cookie = oRequestHandler.GetCookies()

    key = re.search('sitekey: "([^"]+)', str(sHtmlContent)).group(1)
    OuoToken = re.search('<input name="_token" type="hidden" value="([^"]+).+?id="v-token" name="v-token" type="hidden" value="([^"]+)', str(sHtmlContent), re.MULTILINE | re.DOTALL)

    gToken = ResolveCaptcha(key, urlOuo)

    url = urlOuo.replace('/fbc/', '/go/')
    params = '_token=' + OuoToken.group(1) + '&g-recaptcha-response=' + gToken + '&v-token=' + OuoToken.group(2)

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    oRequestHandler.addHeaderEntry('Referer', urlOuo)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Content-Length', str(len(params)))
    oRequestHandler.addHeaderEntry('Cookie', Cookie)
    oRequestHandler.addParametersLine(params)
    sHtmlContent = oRequestHandler.request()

    final = re.search('<form method="POST" action="(.+?)" accept-charset=.+?<input name="_token" type="hidden" value="(.+?)">', str(sHtmlContent))

    url = final.group(1)
    params = '_token=' + final.group(2) + '&x-token=' + ''

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    oRequestHandler.addHeaderEntry('Referer', urlOuo)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Content-Length', str(len(params)))
    oRequestHandler.addHeaderEntry('Cookie', Cookie)
    oRequestHandler.addParametersLine(params)
    # sHtmlContent = oRequestHandler.request()

    sHosterUrl = oRequestHandler.getRealUrl()
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
