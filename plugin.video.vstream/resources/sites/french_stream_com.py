#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress

import re, base64

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

SITE_IDENTIFIER = 'french_stream_com'
SITE_NAME = 'French-stream'
SITE_DESC = 'films en streaming'

URL_MAIN = 'http://french-stream.co/'

URL_SEARCH_MOVIE = (URL_MAIN + 'index.php?do=search&subaction=search&catlist[]=9&story=', 'showMovies')
URL_SEARCH_SERIE = (URL_MAIN + 'index.php?do=search&subaction=search&catlist[]=10&story=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_MOVIE = (True, 'showMoviesMenu')
MOVIE_VF = (URL_MAIN + 'films/vf/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'films/vostfr/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'films/hd-vf/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')

SERIE_NEWS = (URL_MAIN + 'series/', 'showSeries')
SERIE_SERIES = (True, 'showSeriesMenu')
SERIE_VFS = (URL_MAIN + 'series/serie-en-vf-streaming/', 'showSeries')
SERIE_VOSTFRS = (URL_MAIN + 'series/serie-en-vostfr-streaming/', 'showSeries')
SERIE_GENRES = (True, 'showSerieGenres')

ANIM_ANIMS = (URL_MAIN + 'mangas/', 'showMangasMenu')
ANIM_NEWS = (URL_MAIN + 'mangas/', 'showSeries')

def decode_url_Serie(url, id, tmp = ''):

    v = url

    if 'singh' in id:
        id2 = id[6:]
        fields = url.split('nbsp')
        t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/s.php?p_id=1&&c_id=" + t

    if id == 'honey':
        id2 = id[6:]
        fields = url.split('nbsp')
        t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/s.php?p_id=1&&c_id=" + t

    if id == 'yoyo':
        id2 = id[5:]
        fields = url.split('nbsp')
        t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/s.php?p_id=1&&c_id=" + t

    if id == 'seriePlayer':
        fields = url.split('nbsp')
        t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/s.php?p_id=1&&c_id=" + t

    return v

def decode_url(url, id, tmp = ''):

    v = url

    if id == 'seriePlayer':
        fields = tmp.split('sig=705&&')
        t = base64.b64encode(base64.b64encode(fields[1]))
        v = '/f.php?p_id=1&&c_id=' + t

    if id == 'gGotop1':
        fields = tmp.split('sig=705&&')
        t = base64.b64encode(base64.b64encode(fields[1]))
        v = '/f.php?p_id=1&&c_id=' + t

    if id == 'gGotop2':
        fields = url.split('nbsp')
        t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/f.php?p_id=2&&c_id=" + t

    if id == 'gGotop3':
        fields = url.split('nbsq')
        t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/f.php?p_id=3&&c_id=" + t

    if id == 'gGotop4':
        fields = url.split('nbsr')
        t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/f.php?p_id=4&&c_id=" + t

    if id == 'gGotop5':
        fields = url.split('nbss')
        t = base64.b64encode(base64.b64encode(fields[1]))
        v = "/dl.php?p_id=5&&c_id=" + t

    return v

def ResolveUrl(url):

    try:
        url2 = ''
        pat = 'p_id=([0-9]+).+?c_id=([^&]+)'
        id = re.search(pat, url, re.DOTALL).group(1)
        hash = re.search(pat, url, re.DOTALL).group(2)
        hash = base64.b64decode(base64.b64decode(hash))

        if id == '1':
            url2 = 'http://cloudvid.co/embed-'
        if id == '2':
            url2 = 'https://oload.stream/embed/'
        elif id == '3':
            url2 = 'https://vidlox.tv/embed-'
        elif id == '4':
            url2 = 'https://hqq.watch/player/embed_player.php?vid='

        url2 = url2 + hash
        return url2
    except:
        return ''
    return ''

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Film', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Recherche Série', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films (Menu)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries (Menu)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés (Menu)', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMoviesMenu():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Film', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF[1], 'Films (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (HD-VF)', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeriesMenu():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Recherche Série', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()   

def showMangasMenu():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()   

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH_MOVIE[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showSearchSeries():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH_SERIE[0] + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'xfsearch/genre-1/action/'] )
    liste.append( ['Animation', URL_MAIN +'xfsearch/genre-1/animation/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'xfsearch/genre-1/arts+Martiaux/'] )
    liste.append( ['Aventure', URL_MAIN + 'xfsearch/genre-1/aventure/'] )
    liste.append( ['Biopic', URL_MAIN + 'xfsearch/genre-1/biopic/'] )
    liste.append( ['Comédie', URL_MAIN + 'xfsearch/genre-1/comédie/'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'xfsearch/genre-1/comédie+dramatique/'] )
    liste.append( ['Comédie Musicale', URL_MAIN + 'xfsearch/genre-1/comédie+musicale/'] )
    liste.append( ['Documentaire', URL_MAIN + 'xfsearch/genre-1/documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'xfsearch/genre-1/drame/'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'xfsearch/genre-1/epouvante-horreur/'] )
    liste.append( ['Erotique', URL_MAIN + 'xfsearch/genre-1/erotique/'] )
    liste.append( ['Espionnage', URL_MAIN + 'xfsearch/genre-1/espionnage/'] )
    liste.append( ['Famille', URL_MAIN + 'xfsearch/genre-1/famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'xfsearch/genre-1/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'xfsearch/genre-1/guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'xfsearch/genre-1/historique/'] )
    liste.append( ['Musical', URL_MAIN + 'xfsearch/genre-1/musical/'] )
    liste.append( ['Policier', URL_MAIN + 'xfsearch/genre-1/policier/'] )
    liste.append( ['Péplum', URL_MAIN + 'xfsearch/genre-1/peplum/'] )
    liste.append( ['Romance', URL_MAIN + 'xfsearch/genre-1/romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'xfsearch/genre-1/science+fiction/'] )
    liste.append( ['Spectacle', URL_MAIN + 'xfsearch/genre-1/spectacle/'] )
    liste.append( ['Thriller', URL_MAIN + 'xfsearch/genre-1/thriller/'] )
    liste.append( ['Walt Disney', URL_MAIN + 'xfsearch/Walt+Disney+Animation/'] )
    liste.append( ['Western', URL_MAIN + 'xfsearch/genre-1/western/'] )
    liste.append( ['Divers', URL_MAIN + 'xfsearch/genre-1/divers/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN +'xfsearch/genre-serie/Action/'] )
    liste.append( ['Animation', URL_MAIN+'xfsearch/genre-serie/Animation/'])
    liste.append( ['Arts Martiaux', URL_MAIN + 'xfsearch/genre-serie/Arts+Martiaux/'] )
    liste.append( ['Aventure', URL_MAIN + 'xfsearch/genre-serie/Aventure/'])
    liste.append( ['Biopic', URL_MAIN + 'xfsearch/genre-serie/Biopic/'])
    liste.append( ['Comédie', URL_MAIN + 'xfsearch/genre-serie/Comédie/'])
    liste.append( ['Comédie Dramatique', URL_MAIN + 'xfsearch/genre-serie/Comédie+dramatique/'] )
    liste.append( ['Comédie Musicale', URL_MAIN + 'xfsearch/genre-serie/Comédie+musicale/'] )
    liste.append( ['Documentaire', URL_MAIN + 'xfsearch/genre-serie/Documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'xfsearch/genre-serie/Drame/'])
    liste.append( ['Epouvante Horreur', URL_MAIN + 'xfsearch/genre-serie/Epouvante-horreur/'] )
    liste.append( ['Espionnage', URL_MAIN + 'xfsearch/genre-serie/Espionnage/'])
    liste.append( ['Famille', URL_MAIN + 'xfsearch/genre-serie/Famille/'])
    liste.append( ['Fantastique', URL_MAIN + 'xfsearch/genre-serie/Fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'xfsearch/genre-serie/Guerre/'])
    liste.append( ['Historique', URL_MAIN + 'xfsearch/genre-serie/Historique/'])
    liste.append( ['Judiciaire', URL_MAIN + 'xfsearch/genre-serie/Judiciaire/'])
    liste.append( ['Médical', URL_MAIN + 'xfsearch/genre-serie/Médical/'])
    liste.append( ['Musical', URL_MAIN + 'xfsearch/genre-serie/Musical/'] )
    liste.append( ['Policier', URL_MAIN + 'xfsearch/genre-serie/Policier/'] )
    liste.append( ['Romance', URL_MAIN + 'xfsearch/genre-serie/Romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'xfsearch/genre-serie/Science+fiction/'] )
    liste.append( ['Soap', URL_MAIN + 'xfsearch/genre-serie/Soap/'] )
    liste.append( ['Sport', URL_MAIN + 'xfsearch/genre-serie/Sport+event/'] )
    liste.append( ['Thriller', URL_MAIN + 'xfsearch/genre-serie/Thriller/'] )
    liste.append( ['Western', URL_MAIN + 'xfsearch/genre-serie/Western/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'film-ripz"><a href=".+?">([^<]+)</a>.+?film-verz"><a href=".+?">([^<]+)</a>.+?href="([^"]+)"><img src="([^"]+)".+?(?:alt|title)="(.+?)"'

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

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sUrl.replace(URL_SEARCH_MOVIE[0], ''), aEntry[4]) == 0:
                    continue

            sQual = str(aEntry[0])
            sLang = str(aEntry[1])
            sUrl2 = str(aEntry[2])
            sThumb = str(aEntry[3]).replace('/img/french-stream.com.php?src=', '')
            sThumb = sThumb.split('&')[0]
            if sThumb.startswith ('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            sTitle = str(aEntry[4])
            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="short-poster.+?href="([^<]+)"><img src="([^"]+)".*?(?:alt|title)="(.+?)"'

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

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sUrl.replace(URL_SEARCH_SERIE[0], ''), aEntry[2]) == 0:
                    continue

            sUrl2 = str(aEntry[0])
            sThumb = str(aEntry[1]).replace('/img/french-stream.com.php?src=', '')
            sThumb = sThumb.split('&')[0]
            if sThumb.startswith ('/'):
                sThumb = URL_MAIN[:-1] + sThumb

            #filtre pour réorienter les mangas
            if '/mangas/' in sUrl:
                sType = 'mangas'
            else:
                sType = 'autre'

            sTitle = aEntry[2].replace('- Saison', ' Saison')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sType', sType)

            oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="pnext"><a href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'href="([^"]+)" *id="([^"]+)" *target="seriePlayer".+?i class=[^>]+><\/i> ([^<]+) <'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sTitle = aEntry[2] + ' ' + sMovieTitle

            url = aEntry[0]
            #first convertion
            tmp = ''
            try:
                tmp = re.search('input id="tmp".+?value="([^"]+)"', sHtmlContent, re.DOTALL).group(1)
            except:
                pass

            if 'hqq' in url:
                sHosterUrl = url
            else:
                url = decode_url(url, aEntry[1], tmp)

                #second convertion
                sHosterUrl = ResolveUrl(url)

            #if not url.startswith('http'):
            #    url = URL_MAIN[:-1] + url

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
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
    sType = oInputParameterHandler.getValue('sType')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sDesc = ''
    try:
        sPattern = 'id="s-desc">(.+?)<'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    sPattern = '<\/i> (VF|VOSTFR) *<\/div>|<a id="([^"]+)".+?target="seriePlayer".+?"([^"]+)" data-rel="([^"]+)"'
    #aResult = oParser.parse(sHtmlContent, sPattern)
    aResult = re.findall(sPattern, sHtmlContent)

    if (aResult):

        for aEntry in aResult:

            if str(aEntry[0]):
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')

            else:
                sId = aEntry[1]
                sTitle = str(aEntry[2]) + ' ' + sMovieTitle
                sData = str(aEntry[3])

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sData', sData)
                oOutputParameterHandler.addParameter('sId', sId)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                if 'mangas' in sType:
                    oGui.addTV(SITE_IDENTIFIER, 'mangaHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                else:
                    oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    else:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]indisponible[/COLOR]')

    oGui.setEndOfDirectory()

def serieHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sData = oInputParameterHandler.getValue('sData')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div id="' + sData + '".+?<\/div>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        block = aResult[1][0]
    else:
        return

    sPattern = '<a (?:|id="([^"]+)" (?:|onclick=".+?")) *href="([^"]+)"'
    aResult = oParser.parse(block, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if aEntry[0]:

                sUrl = aEntry[1]
                tmp = ''
                try:
                    tmp = re.search('input id="tmp".+?value="([^"]+)"', sHtmlContent, re.DOTALL).group(1)
                except:
                    pass
                url2 = decode_url_Serie(sUrl, aEntry[0], tmp)

                #second convertion
                sHosterUrl = ResolveUrl(url2)

            else:
                sHosterUrl = aEntry[1]

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):

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
    sId = oInputParameterHandler.getValue('sId')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a id="' + sId + '" *href="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry)

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
