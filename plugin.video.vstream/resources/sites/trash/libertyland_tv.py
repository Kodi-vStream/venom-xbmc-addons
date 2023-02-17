# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

return False #de nouveau en panne au 08/07/22

import re

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress, siteManager

SITE_IDENTIFIER = 'libertyland_tv'
SITE_NAME = 'Libertyland'
SITE_DESC = 'Les films et séries récentes en streaming et en téléchargement'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

URL_SEARCH = (URL_MAIN + 'v2/recherche/', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'v2/recherche/categorie=films&mot_search=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'v2/recherche/categorie=series&mot_search=', 'showMovies')

FUNCTION_SEARCH = 'showMovies'

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/nouveautes/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'films/plus-vus-mois/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'films/les-mieux-notes/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_ANNEES = (True, 'showMovieAnnees')
MOVIE_VOSTFR = (URL_MAIN + 'films/films-vostfr/', 'showMovies')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_ANNEES = (True, 'showSerieAnnees')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche film', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche série', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = sUrl + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showMovieGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animation', 'animation'], ['Arts martiaux', 'arts-martiaux'],
             ['Aventure', 'aventure'], ['Biographie', 'biographie'], ['Biopic', 'biopic'], ['Comédie', 'comedie'],
             ['Comédie Dramatique', 'comedie-dramatique'], ['Comédie Musicale', 'comedie-musicale'], ['Crime', 'crime'],
             ['Drame', 'drame'], ['Espionnage', 'espionnage'], ['Famille', 'famille'], ['Fantastique', 'fantastique'],
             ['Guerre', 'guerre'], ['Histoire', 'histoire'], ['Historique', 'historique'], ['Horreur', 'horreur'],
             ['Judiciaire', 'judiciaire'], ['Médical', 'medical'], ['Musical', 'musical'], ['Péplum', 'peplum'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science-Fiction', 'science-fiction'],
             ['Sport', 'sport'], ['Thriller', 'thriller'], ['Western', 'western']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/genre/' + sUrl + '.html')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieGenres():
    oGui = cGui()

    liste = [['Action', 'action'], ['Animé', 'anime'], ['Aventure', 'aventure'], ['Comédie', 'comedie'],
             ['DC Comics', 'dc-comics'], ['Documentaire', 'documentaire'], ['Drama', 'drama'], ['Drame', 'drame'],
             ['Emission TV', 'emission-tv'], ['Epouvante-Horreur', 'epouvante-horreur'], ['Fantastique', 'fantastique'],
             ['Gore', 'gore'], ['Guerre', 'guerre'], ['Historique', 'historique'], ['Mystère', 'mystere'],
             ['Policier', 'policier'], ['Romance', 'romance'], ['Science-Fiction', 'science-fiction'],
             ['Série TV', 'serie-tv'], ['Thriller', 'thriller'], ['Télé-réalité', 'tele-realite']]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'v2/series/genre/' + sUrl + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieAnnees():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1914, 2023)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee/' + Year + '.html')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieAnnees():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    for i in reversed(range(1989, 2023)):
        Year = str(i)
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'v2/series/annee/' + Year + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch
        sPattern = '<img class="img-responsive" *src="([^"]+)".+?<div class="divtelecha.+?href="([^"]+)">([^<>]+)<'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        if '/series' in sUrl:
            sPattern = '<div class="divtelecha.+?href="([^"]+)"><strong>([^<]+)</strong>.+?<img class="img-responsive".+?src="([^"]+).+?serie de (\d{4})<.+?Synopsis :([^<]+)'
        else:  # films
            sPattern = '<h2 class="heading"> *<a href="[^"]+">([^<]+).+?<img class="img-responsive" *src="([^"]+)" *alt.+?(?:<font color="#.+?">([^<]+)</font>.+?).+?>film de (\d{4})<.+?Synopsis : ([^<]+).+?<div class="divtelecha.+?href="([^"]+)'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
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

            sDesc = ''
            sYear = ''
            if sSearch:
                sQual = ''
                sThumb = URL_MAIN[:-1] + aEntry[0]
                sTitle = aEntry[2].replace('télécharger ', '').replace('en Streaming', '')
                sTitle = sTitle.replace(' TELECHARGEMENT GRATUIT', '').replace('gratuitement', '')
                sUrl2 = aEntry[1]
            elif '/series' in sUrl:
                sQual = ''
                sUrl2 = aEntry[0]
                sTitle = aEntry[1].replace('Regarder ', '').replace('en Streaming', '')
                sThumb = URL_MAIN[:-1] + aEntry[2]
                sYear = aEntry[3]

                try:
                    sDesc = aEntry[4].decode('utf-8')
                except AttributeError:
                    pass

                sDesc = cUtil().unescape(sDesc).encode('utf-8')
            else:
                sTitle = aEntry[0]
                sThumb = URL_MAIN[:-1] + aEntry[1]
                sYear = aEntry[3]

                try:
                    sDesc = aEntry[4].decode('utf-8')
                except AttributeError:
                    pass

                sDesc = cUtil().unescape(sDesc).encode('utf-8')
                sUrl2 = aEntry[5]

                sQual = aEntry[2]
                if sQual:

                    try:
                        sQual = sQual.decode("utf-8")
                    except AttributeError:
                        pass

                    sQual = sQual.replace(u' qualit\u00E9', '').replace('et ', '/').replace('Haute', 'HD')\
                                 .replace(' ', '').replace('Bonne', 'DVD').replace('Mauvaise', 'SD').encode("utf-8")

            if 'https' not in sUrl2:
                sUrl2 = URL_MAIN[:-1] + sUrl2

            sUrl2 = sUrl2.replace('telecharger', 'streaming')

            try:
                sTitle = sTitle.decode("utf-8")
            except AttributeError:
                pass

            sTitle = sTitle.replace(u'T\u00E9l\u00E9charger ', '').encode("utf-8")

            # Remplace tout les decodage en python 3
            try:
                sTitle = str(sTitle, 'utf-8')
                sQual = str(sQual, 'utf-8')
                sDesc = str(sDesc, 'utf-8')
            except:
                pass

            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sYear)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if '/series/' in sUrl or '/series/' in sUrl2 or '/series_co/' in sThumb:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisonsEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if sNextPage:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            number = re.findall('([0-9]+)', sNextPage)[-1]
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + number, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li><a href="([^"]+)" class="next">Suivant'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        return URL_MAIN[:-1] + aResult[1][0]

    return False


def ReformatUrl(link):
    if '/v2/mangas' in link:
        return link
    if '/telecharger/' in link:
        return link.replace('telecharger', 'streaming')
    if '-telecharger-' in link:
        f = link.split('/')[-1]
        return '/'.join(link.split('/')[:-1]) + '/streaming/' + f.replace('-telecharger', '')
    # if ('/v2/' in link) and ('/streaming/' in link):
        # return link.replace('/v2/', '/')
    # if ('/v2/' in link) and ('/genre/' in link):
        # return link
    # if '/v2/' in link:
        # return link.replace('/v2/', '/streaming/')
    return link


def showSaisonsEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '(?:<h2 class="heading-small">(Saison .+?)<)|(?:<li><a title=".+? \| (.+?)" class="num_episode" href="([^"]+)")'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            else:
                ePisode = aEntry[1].replace(',', '')
                sTitle = sMovieTitle + ' ' + ePisode
                sUrl = aEntry[2]
                if 'https' not in sUrl:
                    sUrl = URL_MAIN[:-1] + sUrl

                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sYear', sYear)  # utilisé par le skin
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

    # reformatage url
    sUrl = ReformatUrl(sUrl)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sType = ''
    if '/films' in sUrl:
        sType = 'films'
    elif 'saison' in sUrl or 'episode' in sUrl:
        sType = 'series'

    sUrl2 = sUrl.rsplit('/', 1)[1]
    idMov = re.sub('-.+', '', sUrl2)

    sPattern = '<div title="([^"]+)".+?streaming="([^"]+)" heberger="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            if 'VF' in aEntry[0]:
                sLang = 'VF'
            elif 'VOSTFR' in aEntry[0]:
                sLang = 'VOSTFR'
            else:
                sLang = 'VO'

            idHeb = aEntry[1]
            sHost = aEntry[2].capitalize()
            sTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oOutputParameterHandler.addParameter('sHost', sHost)
            oOutputParameterHandler.addParameter('sType', sType)
            oOutputParameterHandler.addParameter('idMov', idMov)
            oOutputParameterHandler.addParameter('idHeb', idHeb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sType = oInputParameterHandler.getValue('sType')
    idHeb = oInputParameterHandler.getValue('idHeb')

    if oInputParameterHandler.exist('idMov'):  # film
        idMov = oInputParameterHandler.getValue('idMov')
        pdata = 'id=' + idHeb + '&id_movie=' + idMov + '&type=' + sType
        pUrl = URL_MAIN + 'v2/video.php'
    else:  # serie pas d'idmov
        pdata = 'id=' + idHeb + '&type=' + sType
        pUrl = URL_MAIN + 'v2/video.php'

    pUrl = pUrl + '?' + pdata

    oRequest = cRequestHandler(pUrl)
    oRequest.addHeaderEntry('Referer', sUrl)
    sHtmlContent = oRequest.request()
    sHtmlContent = sHtmlContent.replace('\\', '')

    sPattern = '<iframe.+?src="([^"]+)".+?"qualite":"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl

            sQual = aEntry[1]

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster:
                sDisplayTitle = ('%s [%s]') % (sMovieTitle, sQual)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:
        # au cas où pas de qualité
        sPattern = '<iframe.+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            for aEntry in aResult[1]:
                sHosterUrl = aEntry
                if sHosterUrl.startswith('//'):
                    sHosterUrl = 'http:' + sHosterUrl

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
