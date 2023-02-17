# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, siteManager
from resources.lib.util import QuoteSafe, Quote
import re

SITE_IDENTIFIER = 'voirfilms_org'
SITE_NAME = 'VoirFilms'
SITE_DESC = 'Films, Séries & Animés en Streaming'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = 'https://wvv.voirfilms.club/'  # url de repli site sans pub

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_LIST = (URL_MAIN + 'alphabet', 'showAlpha')
MOVIE_NEWS = (URL_MAIN + 'film-en-streaming', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_LIST = (URL_MAIN + 'series/alphabet', 'showAlpha')
SERIE_NEWS = (URL_MAIN + 'series-tv-streaming/', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'series/', 'showGenres')
SERIE_ANNEES = (True, 'showSerieYears')

ANIM_ANIMS = (True, 'showMenuAnims')
ANIM_LIST = (URL_MAIN + 'animes/alphabet/', 'AlphaSearch')
ANIM_NEWS = (URL_MAIN + 'animes/', 'showMovies')

URL_SEARCH = ('', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'recherche?type=film&s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'recherche?type=serie&s=', 'showMovies')
URL_SEARCH_ANIMS = (URL_MAIN + 'recherche?type=anime&s=', 'showMovies')
# FUNCTION_SEARCH = 'showMovies'
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
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
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Par ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Par ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuAnims():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_LIST[1], 'Animés (Par ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sUrl = sUrl + Quote(sSearchText)
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def AlphaSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    progress_ = progress().VScreate(SITE_NAME)
    oOutputParameterHandler = cOutputParameterHandler()
    for i in range(0, 27):
        progress_.VSupdate(progress_, 36)

        if i > 0:
            sTitle = chr(64 + i)
        else:
            sTitle = '09'

        oOutputParameterHandler.addParameter('siteUrl', sUrl + sTitle.upper())
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'az.png', oOutputParameterHandler)

    progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append(['Action', sUrl + 'action_1'])
    liste.append(['Animation', sUrl + 'animation_1'])
    liste.append(['Arts Martiaux', sUrl + 'arts-martiaux_1'])
    liste.append(['Aventure', sUrl + 'aventure_1'])
    liste.append(['Biopic', sUrl + 'biopic_1'])
    liste.append(['Comédie', sUrl + 'film-comedie'])
    liste.append(['Comédie Dramatique', sUrl + 'comedie-dramatique_1'])
    liste.append(['Documentaire', sUrl + 'documentaire_1'])
    liste.append(['Drame', sUrl + 'drame_1'])
    liste.append(['Epouvante Horreur', sUrl + 'epouvante-horreur_1'])
    liste.append(['Erotique', sUrl + 'erotique_1'])
    liste.append(['Espionnage', sUrl + 'espionnage_1'])
    liste.append(['Fantastique', sUrl + 'fantastique_1'])
    liste.append(['Guerre', sUrl + 'guerre_1'])
    liste.append(['Historique', sUrl + 'historique_1'])
    liste.append(['Musical', sUrl + 'musical_1'])
    liste.append(['Policier', sUrl + 'policier_1'])
    liste.append(['Romance', sUrl + 'romance_1'])
    liste.append(['Science Fiction', sUrl + 'science-fiction_1'])
    liste.append(['Série', sUrl + 'series_1'])
    liste.append(['Thriller', sUrl + 'thriller_1'])
    liste.append(['Western', sUrl + 'western_1'])
    liste.append(['Non classé', sUrl + 'non-classe_1'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1913, 2023)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieYears():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1936, 2023)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAlpha():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'series' in sUrl:
        code = 'series/alphabet/'
    else:
        code = 'alphabet/'

    liste = []
    liste.append(['0', URL_MAIN + code + '0'])
    liste.append(['1', URL_MAIN + code + '1'])
    liste.append(['2', URL_MAIN + code + '2'])
    liste.append(['3', URL_MAIN + code + '3'])
    liste.append(['4', URL_MAIN + code + '4'])
    liste.append(['5', URL_MAIN + code + '5'])
    liste.append(['6', URL_MAIN + code + '6'])
    liste.append(['7', URL_MAIN + code + '7'])
    liste.append(['8', URL_MAIN + code + '8'])
    liste.append(['9', URL_MAIN + code + '9'])
    liste.append(['A', URL_MAIN + code + 'A'])
    liste.append(['B', URL_MAIN + code + 'B'])
    liste.append(['C', URL_MAIN + code + 'C'])
    liste.append(['D', URL_MAIN + code + 'D'])
    liste.append(['E', URL_MAIN + code + 'E'])
    liste.append(['F', URL_MAIN + code + 'F'])
    liste.append(['G', URL_MAIN + code + 'G'])
    liste.append(['H', URL_MAIN + code + 'H'])
    liste.append(['I', URL_MAIN + code + 'I'])
    liste.append(['J', URL_MAIN + code + 'J'])
    liste.append(['K', URL_MAIN + code + 'K'])
    liste.append(['L', URL_MAIN + code + 'L'])
    liste.append(['M', URL_MAIN + code + 'M'])
    liste.append(['N', URL_MAIN + code + 'N'])
    liste.append(['O', URL_MAIN + code + 'O'])
    liste.append(['P', URL_MAIN + code + 'P'])
    liste.append(['Q', URL_MAIN + code + 'Q'])
    liste.append(['R', URL_MAIN + code + 'R'])
    liste.append(['S', URL_MAIN + code + 'S'])
    liste.append(['T', URL_MAIN + code + 'T'])
    liste.append(['U', URL_MAIN + code + 'U'])
    liste.append(['V', URL_MAIN + code + 'V'])
    liste.append(['W', URL_MAIN + code + 'W'])
    liste.append(['X', URL_MAIN + code + 'X'])
    liste.append(['Y', URL_MAIN + code + 'Y'])
    liste.append(['Z', URL_MAIN + code + 'Z'])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
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
        oRequest.addHeaderEntry('User-Agent', UA)
        oRequest.addHeaderEntry('Referer', URL_MAIN)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')

        sHtmlContent = oRequest.request()

        sPattern = '<div class="unfilm".+?href="([^"]+)" title="([^"]+).+?class="type ([^"]+)".+?<img src="([^"]+).+?("suivre2">([^<]+)<|<span class="qualite ([^"]+)|<div class="cdiv")'

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sHtmlContent = re.sub('alt="title="', 'alt="', sHtmlContent)  # anime
        sPattern = '<div class="unfilm".+?href="([^"]+).+?<img src="([^"]+)" alt="([^"]+).+?("suivre2">([^<]+)<|<span class="qualite ([^"]+)|<div class="cdiv")'

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
                sTitle = aEntry[1]
                sType = aEntry[2]
                sThumb = aEntry[3]
                sYear = aEntry[5]
                sQual = aEntry[6]
                if sTypeSearch:
                    if sTypeSearch != sType:  # genre recherché:  film/serie/anime
                        continue
            else:
                sThumb = aEntry[1]
                sTitle = aEntry[2]
                sYear = aEntry[4]
                sQual = aEntry[5]

            sUrl = aEntry[0]
            if 'http' not in sUrl:
                sUrl = URL_MAIN[:-1] + sUrl

            sTitle = sTitle.replace('film ', '')  # genre
            sTitle = sTitle.replace(' streaming', '')  # genre

            sLang = ''
            if 'Vostfr' in sTitle:
                sTitle = sTitle.replace('Vostfr', '')
                sLang = 'VOSTFR'

            sDisplayTitle = '%s [%s] (%s) (%s)' % (sTitle, sQual, sLang, sYear)

            if 'http' not in sThumb:
                sThumb = URL_MAIN + sThumb

            # not found better way
            # sTitle = unicode(sTitle, errors='replace')
            # sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')

            # vStream don't work with unicode url for the moment
            # sThumb = unicode(sThumb, 'UTF-8')
            # sThumb = sThumb.encode('ascii', 'ignore').decode('ascii')
            # sThumb = sThumb.decode('utf8')

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showS_E', sDisplayTitle, sThumb, sThumb, '', oOutputParameterHandler)
            elif 'anime' in sUrl:
                oGui.addAnime(SITE_IDENTIFIER, 'showS_E', sDisplayTitle, sThumb, sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, sThumb, sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sHtmlContent = re.sub(" rel='nofollow'", "", sHtmlContent)  # next genre
    sPattern = ">([^<]+)</a><a href='([^']+)'>suiv »"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = aResult[1][0][1]
        if sNextPage.startswith('/'):
            sNextPage = URL_MAIN[:-1] + sNextPage
        sNumberNext = re.findall('([0-9]+)', sNextPage)[-1]
        sPaging = str(sNumberNext) + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    # patch for unicode url
    sUrl = QuoteSafe(sUrl)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'data-src="([^"]+)" target="filmPlayer".+?span class="([^"]+)"></span>.+?class="([^"]+)"></span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl2 = aEntry[0]
            sHost = aEntry[1].capitalize()
            if 'apidgator' in sHost or 'dl_to' in sHost:
                continue

            sLang = aEntry[2].upper().replace('L', '')
            sTitle = '%s (%s) [COLOR coral]%s[/COLOR]' % (sMovieTitle, sLang, sHost)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oOutputParameterHandler.addParameter('sLang', sLang)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler)

    sPattern = 'href="(https:\/\/cineactu.co\/.+?").*?span class="([^"]+).*?class="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl2 = aEntry[0]
            sHost = aEntry[1]
            if 'fichier' in sHost:
                sHost = '1 Fichier'
            if 'uptobox' in sHost:
                sHost = 'Uptobox'
            sHost = sHost.capitalize()  # ou autres ?

            sLang = aEntry[2].upper().replace('L', '')
            sTitle = '%s (%s) [COLOR coral]%s[/COLOR]' % (sMovieTitle, sLang, sHost)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('siteReferer', sUrl)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oGui.addLink(SITE_IDENTIFIER, 'showHostersDL', sTitle, sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showS_E():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # sHtmlContent = sHtmlContent.replace("\r\t", "")
    if '-saison-' in sUrl or 'anime' in sUrl:
        sPattern = '<a class="n_episode2" title=".+?, *([A-Z]+) *,.+?" *href="([^"]+)">(.+?)</a></li>'
    else:
        sPattern = '<div class="unepetitesaisons">[^<>]*?<a href="([^"]+)" title="([^"]+)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1][::-1]:

            # Si plusieurs langues sont disponibles, une seule est affichée ici.
            # Ne rien mettre, la langue sera ajoutée avec le host
            if 'anime' in sUrl:
                sUrl2 = aEntry[1]
                sNM = aEntry[2].replace('<span>', '').replace('</span>', '')
                sTitle = sMovieTitle + ' E' + sNM
                sDisplayTitle = sTitle
            elif '-saison-' in sUrl:
                sUrl2 = aEntry[1]
                sNM = aEntry[2].replace('<span>', ' ').replace('</span>', '')
                sTitle = sMovieTitle + sNM
                sDisplayTitle = sTitle
            else:
                sUrl2 = aEntry[0]
                sTitle = re.sub('\d x ', 'E', aEntry[1])
                sTitle = sTitle.replace('EP ', 'E')
                sDisplayTitle = sTitle

            if 'http' not in sUrl2:
                sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '-episode-' in sUrl2 or '/anime' in sUrl:
                oGui.addEpisode(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addSeason(SITE_IDENTIFIER, 'showS_E', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    host = sUrl.split('/')[0:3]
    host = host[0] + '//' + host[2] + '/'

    # VSlog('org > ' + sUrl)

    # Attention ne marche pas dans tout les cas, certain site retourne aussi un 302 et la lib n'en gere qu'un
    if False:
        # On recupere la redirection
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', host)
        sHtmlContent = oRequestHandler.request()
        redirection_target = oRequestHandler.getRealUrl()

    else:
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.disableRedirect()
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', host)
        sHtmlContent = oRequestHandler.request()

        redirection_target = sUrl

        if oRequestHandler.statusCode() == 302:
            redirection_target = reponse.getResponseHeader()['Location']

    # attention fake redirection
    sUrl = redirection_target
    try:
        m = re.search(r'url=([^"]+)', sHtmlContent)
    except:
        m = re.search(r'url=([^"]+)', str(sHtmlContent))

    if m:
        sUrl = m.group(1)

    # Modifications
    sUrl = sUrl.replace('1wskdbkp.xyz', 'youwatch.org')
    if '1fichier' in sUrl:
        sUrl = re.sub('(http.+?\?link=)', 'https://1fichier.com/?', sUrl)

    sHosterUrl = sUrl
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showHostersDL():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    siteReferer = oInputParameterHandler.getValue('siteReferer')

    if 'cineactu.co' in sUrl:  # tjrs vrai mais au cas ou autre pattern fait sur host DL
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', siteReferer)
        oRequestHandler.request()
        redirection_target = oRequestHandler.getRealUrl()
        if 'shortn.co' in redirection_target:
            bvalid, shost = Hoster_shortn(redirection_target, sUrl)
            if bvalid:
                sHosterUrl = shost
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def Hoster_shortn(url, refer):
    shost = ''
    # url="https://shortn.co/f/6183943"
    url = url.replace('%22', '')
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', refer)
    sHtmlContent = oRequestHandler.request()
    cookies = oRequestHandler.GetCookies()
    sPattern = "type.*?name=.*?value='([^']+)"
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        token = aResult[0]
        data = '_token=' + token
        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Referer', url)
        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Content-Type', "application/x-www-form-urlencoded")
        oRequestHandler.addHeaderEntry('Cookie', cookies)
        oRequestHandler.addParametersLine(data)
        sHtmlContent = oRequestHandler.request()

        # https://1fichier.com/?jttay6v60izpcu3rank7
        # https://uptobox.com/vy7g5a6itlgj?aff_id=10831504
        sPattern = 'href="([^"]+).+?target="_blank'
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            shost = aResult[0]
            if '?' in shost and 'uptobox' in shost:
                shost = shost.split('?')[0]
    if shost:
        return True, shost

    return False, False
