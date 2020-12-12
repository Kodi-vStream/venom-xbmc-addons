# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 34 https://french-stream.lol/  french-stream.lol 29112020
# update 06122020
import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress #, VSlog


SITE_IDENTIFIER = 'french_stream_lol'
SITE_NAME = 'French-stream-lol'
SITE_DESC = ' films et series'

URL_MAIN = 'https://french-stream.lol/'

MOVIE_NEWS = (URL_MAIN + 'film/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_VOSTFR = (URL_MAIN + 'film/vostfr/', 'showMovies')

MOVIE_VF_FRENCH = (URL_MAIN + 'xfsearch/version-film/French/', 'showMovies')
MOVIE_VF_TRUEFRENCH = (URL_MAIN + 'xfsearch/version-film/TrueFrench/', 'showMovies')

MOVIE_HDLIGHT = (URL_MAIN + 'xfsearch/qualit/HDLight/', 'showMovies')
MOVIE_DVD = (URL_MAIN + 'xfsearch/qualit/DVDSCR/', 'showMovies')
MOVIE_CAM = (URL_MAIN + 'xfsearch/qualit/CAM/', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'serie/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_VF = (URL_MAIN + 'serie/serie-en-vf-streaming/', 'showMovies')
SERIE_VOSTFR = (URL_MAIN + 'serie/serie-en-vostfr-streaming/', 'showMovies')

key_search_movies = '#searchsomemovies'
key_search_series = '#searchsomeseries'
URL_SEARCH = (URL_MAIN + 'index.php?do=search', 'showMovies')
URL_SEARCH_MOVIES = (key_search_movies, 'showMovies')
URL_SEARCH_SERIES= ( key_search_series, 'showMovies')

# recherche utilisée quand on utilise directement la source
MY_SEARCH_MOVIES = ( True, 'MyshowSearchMovie')
MY_SEARCH_SERIES = ( True, 'MyshowSearchSerie')

# Menu GLOBALE HOME
MOVIE_MOVIE = (True, 'showMoviesSource')
SERIE_SERIES = (True, 'showTvshowSource')


def load():

    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche Films & Séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_MOVIES[1], 'Recherche Films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF_FRENCH[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF_FRENCH[1], 'Films (French)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF_TRUEFRENCH[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF_TRUEFRENCH[1], 'Films (True French)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOST)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films (HD Light)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_DVD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_DVD[1], 'Films (DVD)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_CAM[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_CAM[1], 'Films (CAM)', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_SERIES[1], 'Recherche Series ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VF[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFR[1], 'Séries (VOST)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMoviesSource():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_MOVIES[1], 'Recherche Films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', [0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF_FRENCH[1], 'Films (French)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF_TRUEFRENCH[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF_TRUEFRENCH[1], 'Films (True French)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOST)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showTvshowSource():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MY_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, MY_SEARCH_SERIES[1], 'Recherche Series ', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Series (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VF[1], 'Séries (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFR[1], 'Séries (VOST)', 'vostfr.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def MyshowSearchSerie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = key_search_series + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def MyshowSearchMovie():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = key_search_movies + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovieGenres():

    oGui = cGui()
    liste = [] #'romance'
    listegenre = ['action', 'animation', 'arts-martiaux', 'aventure', 'biopic', 'comedie', 'drame'
                  , 'documentaire', 'epouvante-horreur', 'espionnage' ,'famille', 'fantastique'
                  , 'guerre', 'historique', 'policier', 'science-fiction', 'thriller', 'western']

    for igenre in listegenre:
        liste.append([igenre.capitalize(), URL_MAIN + igenre + '/'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieGenres():

    oGui = cGui()
    liste = []
    listegenre = ['action', 'animation', 'aventure', 'biopic', 'comedie', 'drame', 'famille'
                  , 'fantastique', 'historique', 'horreur', 'judiciaire', 'medical'
                  , 'policier', 'romance', 'science-fiction', 'thriller', 'western']

    # https://french-stream.lol/serie-judiciare/
    # https://french-stream.lol/serie/serie-judiciare/
    for igenre in listegenre:
        urlgenre = igenre
        if igenre == 'judiciaire':
            urlgenre  = 'judiciare'
        liste.append([igenre.capitalize(), URL_MAIN + 'serie/serie-' + urlgenre + '/'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):

    oGui = cGui()
    oParser = cParser()

    bSearchMovie = False
    bSearchSerie = False
    if sSearch:
        # sUrl = URL_SEARCH[0]  # sert a rien
        sSearch = sSearch.replace(' ', '+').replace('%20', '+')

        if key_search_movies in sSearch:
            sSearch = sSearch.replace(key_search_movies, '')
            bSearchMovie = True
        if key_search_series in sSearch:
            sSearch = sSearch.replace(key_search_series, '')
            bSearchSerie = True

        pdata = 'do=search&subaction=search&search_start=1&full_search=0&result_from=1&story=' + sSearch
        oRequest = cRequestHandler(URL_SEARCH[0])
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequest.addParametersLine(pdata)
        sHtmlContent = oRequest.request()

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    # ref thum title
    sPattern = '<div class="short-in.+?with-mask.+?ref="([^"]*).+?src="([^"]*).+?short-title">([^<]*)'
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

            sUrl2 = aEntry[0]
            sThumb = aEntry[1]
            sTitle = aEntry[2]  # .replace('-','')

            if bSearchMovie:
                if '/serie' in sUrl2:
                    continue
            if bSearchSerie:
                if '/serie' not in sUrl2:
                    continue

            sDisplayTitle = sTitle.replace('-', '')
            if sSearch and not bSearchMovie and not bSearchSerie:
                if '/serie' in sUrl2:
                    sDisplayTitle = sDisplayTitle + ' [serie]'
                else:
                    sDisplayTitle = sDisplayTitle + ' [film]'

            if 'http' not in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            if '/serie' not in sUrl2:
                oGui.addMovie(SITE_IDENTIFIER, 'showMovieLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'ShowEpisodes', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        bNextPage, urlNextpage, pagination = __checkForNextPage(sHtmlContent)
        if (bNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', urlNextpage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal] ' + pagination + ' >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    urlNextpage = ''
    snumberNext = ''
    sNumberMax = ''
    pagination = ''

    if '<span class="pnext">' not in sHtmlContent:
        return False, 'none', 'none'

    sPattern = '(\d+)<.a>\s*<.span>\s*<span class="pnext">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sNumberMax= aResult[1][0]

    sPattern = '<span class="pnext">.+?ref="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        urlNextpage = aResult[1][0]  # minimum requis
        try:
            snumberNext = re.search('page.([0-9]+)', urlNextpage).group(1)
        except:
            pass

    if snumberNext:
        pagination = 'Page ' + str(snumberNext)
        if sNumberMax:
            pagination = pagination + '/' + sNumberMax

    if urlNextpage:
        return True, urlNextpage, pagination

    return False, 'none', 'none'


def ShowEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if not 'saison' in sMovieTitle.lower():
        sPattern = 'saison-(\d+)'
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            sMovieTitle = sMovieTitle + ' - Saison ' + aResult[1][0]

    sPattern = 'id="s-desc">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sDesc = 'french stream lol'
    if (aResult[0] == True):
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', cleanDesc(aResult[1][0]))


    sPattern = 'fa-play-circle-o">.+?(VOSTFR|VF)|id="(?:honey|yoyo)(?:\d+)"\s*href="([^"]+).+?title="([^"]+).+?data-rel="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    bfind = ""
    ValidEntry = ""

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if aEntry[0]:
                Slang = aEntry[0].replace('-tab', '').replace('"', '')
                bfind = True

            if bfind and aEntry[1]:
                ValidEntry = True 
                sFirst_Url = aEntry[1]
                sEpisode = aEntry[2]
                sRel_Episode = aEntry[3]

                sDisplayTitle = sMovieTitle.replace('-', '') + ' ' + sEpisode + ' (' + Slang + ' )' 

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sRel_Episode', sRel_Episode)
                oOutputParameterHandler.addParameter('sFirst_Url', sFirst_Url)
                oOutputParameterHandler.addParameter('sDisplayTitle', sDisplayTitle )

                oGui.addEpisode(SITE_IDENTIFIER, 'showSerieLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not ValidEntry:
        oGui.addText(SITE_IDENTIFIER, '# Aucune  video trouvée #')

    oGui.setEndOfDirectory()


def showSerieLinks():

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sRel_Episode = oInputParameterHandler.getValue('sRel_Episode')
    sFirst_Url = oInputParameterHandler.getValue('sFirst_Url')
    sDisplayTitle1 = oInputParameterHandler.getValue('sDisplayTitle')

    # VSlog(sUrl );VSlog('sRel_Episode=' + sRel_Episode );VSlog('sFirst_Url=' +sFirst_Url )
    
    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # sPattern = '<div id="([^"]+) class="fullsfeature".*?<li><a (id="singh.*?<div style="height)'
    sPattern = '<div id="' + sRel_Episode + '" class="fullsfeature".*?<li><a (id="singh.*?<div style="height)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        # dans cas ou il n'y a qu'un seul lien il n'y a pas de reference  dans <div id="episodexx" class="fullsfeature">
        # le pattern devient alors normalement hs
        if sFirst_Url:
            sUrl2 = sFirst_Url 
            sHost = '[COLOR coral]' + GetHostname(sUrl2) + '[/COLOR]'

            sDisplayTitle = sDisplayTitle1 + ' ' + sHost 
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('referer', sUrl)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    if (aResult[0] == True):
        html = aResult[1][0]
        # VSlog(html)
        sPattern = 'href="([^"]+).*?aria-hidden'
        aResulturl = oParser.parse(html, sPattern)
        if (aResulturl[0] == True):
            for aEntry in aResulturl[1]:
                sUrl2 = aEntry

                if isblackhost(sUrl2):
                    continue

                if 'http' not in sUrl2: # liens naze du site url
                    # sUrl2 = URL_MAIN + "/film/f/" +sUrl2
                    continue

                if 'hqq.tv' in sUrl2:
                    continue
                    # pass

                sHost= '[COLOR coral]' + GetHostname(sUrl2) + '[/COLOR]'
                sDisplayTitle = sDisplayTitle1 + ' ' + sHost

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('referer', sUrl)

                oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieLinks():

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    # sDesc = oInputParameterHandler.getValue('sDesc')
    # VSlog(sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'id="s-desc">([^<]+)|Date de sortie:<.span>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sDesc = 'french stream lol'
    if (aResult[0] == True):
        try:  # a verifier
            if len(aResult[1]) == 2:
                syear = aResult[1][1][1]
                sDesc = ('%s [I][COLOR grey]%s[/COLOR][/I] %s') % ('Année : ' + syear + '\r\n', 'Synopsis :', cleanDesc(aResult[1][0][0]))
            else:
                sDesc = (' [I][COLOR grey]%s[/COLOR][/I] %s') % ( 'Synopsis :', cleanDesc(aResult[1][0][0]))
        except:
            pass

    sPattern = '<span>\s*<a.*?href="([^"]+).+?hidden="true'
    aResult = oParser.parse(sHtmlContent, sPattern)

    valide_host = []

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            sUrl2 = aEntry
            if isblackhost(sUrl2):
                continue

            if 'http' not in sUrl2:  # liens nazes du site url
                continue
            if 'hqq.tv' in sUrl2:
                continue

            if sUrl2 not in valide_host:  # à cause de l'url par défaut
                valide_host.append(sUrl2)
            else:
                continue

            sHost = '[COLOR coral]' + GetHostname(sUrl2) + '[/COLOR]'
            sDisplayTitle = sTitle + ' ' + sHost

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('referer', sUrl)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sHosterUrl = sUrl
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def GetHostname(url):
    try:
        # en genral pour liens opsktp url_redirect mais on affiche l'host
        bvalid, sHost = isValidhost(url)
        if bvalid:
            pass

        elif 'opsktp' in url:
            sHost = re.search('http.+?opsktp.+?\/([^\/]+)', url).group(1)
        elif 'www' not in url:
            sHost = re.search('http.*?\/\/([^.]*)', url).group(1)
        else:
            sHost = re.search('htt.+?\/\/(?:www).([^.]*)', url).group(1)
    except:
        sHost = url

    return sHost.capitalize()


def isValidhost(url):
    Validhost = ['mystream', 'uptobox', 'fembed', 'vidlox']
    urllower = url.lower()
    for host in Validhost:
        if host.lower() in urllower:
            return True, host
    return False, False


def isblackhost(url):
    black_host = ['playzer.xyz']  # à rajouter
    urllower = url.lower()
    for host in black_host:
        if host.lower() in urllower:
            return True
    return False


def cleanDesc(sdesc):

    oParser = cParser()
    sPattern = '(Résumé.+?streaming Complet)'
    aResult = oParser.parse(sdesc, sPattern)

    if (aResult[0] == True):
        sdesc = sdesc.replace(aResult[1][0], '')

    list_comment = [':', 'en streaming', 'Voir Serie ']

    for s in list_comment:
        sdesc = sdesc.replace(s, '')

    return sdesc
