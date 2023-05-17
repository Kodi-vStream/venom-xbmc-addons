# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
import base64
import xbmc

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager
from resources.lib.util import cUtil

# Detecte si c'est Kodi 19 ou plus
if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
    isPython3 = True
else:
    isPython3 = False

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

SITE_IDENTIFIER = 'french_stream_com'
SITE_NAME = 'French-stream'
SITE_DESC = 'Films, Séries & Mangas en streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

# URL_SEARCH_MOVIES = (URL_MAIN + 'index.php?do=search&subaction=search&catlist[]=9&story=', 'showMovies')
# URL_SEARCH_SERIES = (URL_MAIN + 'index.php?do=search&subaction=search&catlist[]=10&story=', 'showSeries')
URL_SEARCH_MOVIES = (URL_MAIN + 'search/', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'search/', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films-streaming/', 'showMovies')
# MOVIE_VF = (URL_MAIN + 'films/vf/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'film/VOSTFR/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'qualit/HDLight/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'serie-tv-streaming', 'showSeries')
SERIE_VFS = (URL_MAIN + 'serie/VF/', 'showSeries')
SERIE_VOSTFRS = (URL_MAIN + 'serie/VOSTFR/', 'showSeries')
SERIE_GENRES = (True, 'showSerieGenres')

ANIM_ANIMS = (True, 'showMenuAnims')
ANIM_NEWS = (URL_MAIN + 'mangas/', 'showSeries')


def decode_url_Serie(url, sId, tmp=''):
    v = url
    if 'singh' in sId:
        fields = url.split('nbsp')
        try:
            if isPython3:
                t = base64.b64encode(base64.b64encode(fields[1].encode()))
            else:
                t = base64.b64encode(base64.b64encode(fields[1]))
        except IndexError:
            if isPython3:
                t = base64.b64encode(base64.b64encode(fields[0].encode()))
            else:
                t = base64.b64encode(base64.b64encode(fields[0]))
        else:
            return
        v = "/s.php?p_id=1&&c_id=" + str(t)

    if sId == 'honey':
        fields = url.split('nbsp')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/s.php?p_id=1&&c_id=" + str(t)

    if sId == 'yoyo':
        fields = url.split('nbsp')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/s.php?p_id=1&&c_id=" + str(t)

    if sId == 'seriePlayer':
        fields = url.split('nbsp')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/s.php?p_id=1&&c_id=" + str(t)

    return v


def decode_url(url, sId, tmp=''):
    v = url
    if sId == 'seriePlayer':
        fields = tmp.split('sig=705&&')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = '/f.php?p_id=1&&c_id=' + str(t)

    if sId == 'gGotop1':
        fields = tmp.split('sig=705&&')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = '/f.php?p_id=1&&c_id=' + str(t)

    if sId == 'gGotop2':
        fields = url.split('nbsp')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/f.php?p_id=2&&c_id=" + str(t)

    if sId == 'gGotop3':
        fields = url.split('nbsq')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/f.php?p_id=3&&c_id=" + str(t)

    if sId == 'gGotop4':
        fields = url.split('nbsr')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/f.php?p_id=4&&c_id=" + str(t)

    if sId == 'gGotop5':
        fields = url.split('nbss')
        if isPython3:
            t = base64.b64encode(base64.b64encode(fields[1].encode()))
        else:
            t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/dl.php?p_id=5&&c_id=" + str(t)

    return v


def resolveUrl(url):
    try:
        url2 = ''
        pat = 'p_id=([0-9]+).+?c_id=([^&]+)'
        sId = re.search(pat, url, re.DOTALL).group(1)
        hAsh = re.search(pat, url, re.DOTALL).group(2)
        hAsh = base64.b64decode(base64.b64decode(hAsh))

        if sId == '2':
            url2 = 'https://oload.stream/embed/'
        elif sId == '3':
            url2 = 'https://vidlox.me/embed-'
        elif sId == '4':
            url2 = 'https://hqq.watch/player/embed_player.php?vid='

        url2 = url2 + hAsh
        return url2
    except:
        return ''
    return ''


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Film', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Recherche Série', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Film', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_VF[1], 'Films (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (HD-VF)', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Recherche Série', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuAnims():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH_MOVIES[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearchSeries():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH_SERIES[0] + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovieGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts Martiaux', 'arts-Martiaux'],
             ['Aventure', 'aventure'], ['Biopic', 'biopic'], ['Comédie', 'com%C3%A9die'],
             ['Comédie Dramatique', 'com%C3%A9die-dramatique'], ['Comédie Musicale', 'com%C3%A9die-musicale'],
             ['Documentaire', 'documentaire'], ['Drame', 'drame'], ['Epouvante Horreur', 'epouvante_horreur'],
             ['Erotique', 'erotique'], ['Espionnage', 'espionnage'], ['Famille', 'famille'],
             ['Fantastique', 'fantastique'], ['Guerre', 'guerre'], ['Historique', 'historique'], ['Musical', 'musical'],
             ['Policier', 'policier'], ['Péplum', 'peplum'], ['Romance', 'romance'],
             ['Science Fiction', 'science-fiction'], ['Spectacle', 'spectacle'], ['Super héros', 'Super_héros'],
             ['Thriller', 'thriller'], ['Walt Disney', 'Walt-Disney'], ['Western', 'western'], ['Divers', 'divers']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'film-genre/' + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieGenres():
    oGui = cGui()

    liste = [['Action', 'Action'], ['Animation', URL_MAIN + 'serie-genreAnimation'], ['Arts Martiaux', 'Arts-Martiaux'],
             ['Aventure', 'Aventure'], ['Biopic', 'Biopic'], ['Comédie', 'Comédie'],
             ['Comédie Dramatique', 'Comédie+dramatique'], ['Comédie Musicale', 'Comédie+musicale'],
             ['Documentaire', 'Documentaire'], ['Drame', 'Drame'], ['Epouvante Horreur', 'Epouvante-horreur'],
             ['Espionnage', 'Espionnage'], ['Famille', 'Famille'], ['Fantastique', 'Fantastique'], ['Guerre', 'Guerre'],
             ['Historique', 'Historique'], ['Judiciaire', 'Judiciaire'], ['Médical', 'Médical'], ['Musical', 'Musical'],
             ['Policier', 'Policier'], ['Romance', 'Romance'], ['Science Fiction', 'Science+fiction'], ['Soap', 'Soap'],
             ['Sport', 'Sport+event'], ['Thriller', 'Thriller'], ['Western', 'Western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'serie-genre/' + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_MOVIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'film-ripz".+?href="([^"]+)" title="[^"]+">.+?<img src="([^"]+).+?class="short-titl.+?>([^<]+)<(/div|br>(.+?)<)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = URL_MAIN[:-1] + aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            sTitle = aEntry[2]

            if sSearch and ' - Saison ' in sTitle:  # La recherche retourne aussi des séries
                continue

            # on recupere le titre dans le poster car le site ne l'affiche pas toujours
            if sTitle == ' ':
                sTitle = aEntry[1].replace('/static/poster/', '').replace('-', ' ').replace('.jpg', '').title()

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            # Année parfois
            sYear = ''
            if len(aEntry) > 4:
                sYear = aEntry[4]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def showSeries(sSearch=''):
    oGui = cGui()

    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH_SERIES[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'class="short-poster.+?href="([^"]+)".+?img src="([^"]*)".*?class="short-title.+?>([^<]+)<'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = URL_MAIN[:-1] + aEntry[0]
            sThumb = aEntry[1]
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            sTitle = aEntry[2]

            if sSearch and ' - Saison ' not in sTitle:  # La recherche retourne aussi des films
                continue

            # Filtre de recherche
            if sSearch:
                if not oUtil.CheckOccurence(sSearchText, sTitle):
                    continue

            # filtre pour réorienter les mangas
            # if '/manga' in sUrl:
                # sType = 'mangas'
            # else:
                # sType = 'autre'

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            # oOutputParameterHandler.addParameter('sType', sType)

            if '/manga' in sUrl:
                oGui.addAnime(SITE_IDENTIFIER, 'mangaHosters', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, '', sThumb, '', oOutputParameterHandler)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', 'Page ' + sPaging, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'href="([^"]+)">>></a>.+?>(\d+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNextPage = URL_MAIN[:-1] + aResult[1][0][0]
        sNumberMax = aResult[1][0][1]
        sNumberNext = re.search('/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    sPattern = '>([^<]+)</a>\s*<a href="([^"]+)">>>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = URL_MAIN[:-1] + aResult[1][0][1]
        sNumberNext = re.search('/([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<a style="display.+?cid="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:

                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showEpisode():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    # sType = oInputParameterHandler.getValue('sType')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    try:
        sPattern = 'id="s-desc">.+? : (.+?)<'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = re.sub('Résumé.+?$', '', aResult[1][0])
    except:
        pass

    sPattern = '</i> *(VF|VOSTFR) *</div>|<a id="([^"]+)".+?target="seriePlayer".+?"([^"]+)" data-rel="([^"]+)"'
    aResult = re.findall(sPattern, sHtmlContent)
    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    sLang = ''
    if aResult:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult:

            if aEntry[0]:
                sLang = aEntry[0]
            else:
                # sId = aEntry[1]
                sTitle = sMovieTitle + ' ' + aEntry[2]
                sDisplayTitle = '%s [%s]' % (sTitle, sLang)
                sData = aEntry[3]

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sData', sData)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sLang', sLang)

                oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sData = oInputParameterHandler.getValue('sData')

    # if sData == 'episode1': #episode final au lieu du 1er donc pour le moment
        # return
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div id="' + sData + '" class="fullsfeature"(.+?)<div style='
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        block = aResult[1][0]
    else:
        return

    sPattern = '<a (?:id="([^"]+)"|onclick=".+?") *surl="([^"]+)"'
    aResult = oParser.parse(block, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            if aEntry[0]:
                url = aEntry[1]
                tmp = ''
                try:
                    tmp = re.search('input id="tmp".+?value="([^"]+)"', sHtmlContent, re.DOTALL).group(1)
                except:
                    pass

                if '/embed' in url or 'opsktp' in url or 'videovard' in url or 'iframe' in url or 'jetload' in url:
                    sHosterUrl = url
                else:
                    url2 = decode_url_Serie(url, aEntry[0], tmp)
                    # second convertion
                    sHosterUrl = resolveUrl(url2)

            else:
                sHosterUrl = aEntry[1]

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:

                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def mangaHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '</i> *(VF|VOSTFR) *</div>|<a style="padding:5px 0;" id=".+?" *cid="([^"]+)".+?</i>([^<]+)</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            else:
                sTitle = aEntry[2] + sMovieTitle
                sHosterUrl = aEntry[1]

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    # redirection en cas d'absence de résultat
    if not aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addLink(SITE_IDENTIFIER, 'showHosters', sMovieTitle, sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()
