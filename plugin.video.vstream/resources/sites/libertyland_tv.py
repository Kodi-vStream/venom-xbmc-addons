#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress#, VSlog
import re

SITE_IDENTIFIER = 'libertyland_tv'
SITE_NAME = 'Libertyland'
SITE_DESC = 'Les films et séries récentes en streaming et en téléchargement'

#URL_MAIN = 'https://ww2.libertyvf.ch/'
#Modif du 26/08
URL_MAIN = 'https://libertyland.am/'

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

SERIE_SERIES = (True, 'showMenuSeries')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_ANNEES = (True, 'showSerieAnnees')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films (Menu)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries (Menu)', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche film', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche série', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sUrl + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovieGenres():
    oGui = cGui()
    sUrl = URL_MAIN + 'films/genre/'

    liste = []
    liste.append( ['Action', sUrl + 'action.html'] )
    liste.append( ['Animation', sUrl + 'animation.html'] )
    liste.append( ['Arts martiaux', sUrl + 'arts-martiaux.html'] )
    liste.append( ['Aventure', sUrl + 'aventure.html'] )
    liste.append( ['Biographie', sUrl + 'biographie.html'] )
    liste.append( ['Biopic', sUrl + 'biopic.html'] )
    liste.append( ['Comédie', sUrl + 'comedie.html'] )
    liste.append( ['Comédie Dramatique', sUrl + 'comedie-dramatique.html'] )
    liste.append( ['Comédie Musicale', sUrl + 'comedie-musicale.html'] )
    liste.append( ['Crime', sUrl + 'crime.html'] )
    liste.append( ['Drame', sUrl + 'drame.html'] )
    liste.append( ['Espionnage', sUrl + 'espionnage.html'] )
    liste.append( ['Famille', sUrl + 'famille.html'] )
    liste.append( ['Fantastique', sUrl + 'fantastique.html'] )
    liste.append( ['Guerre', sUrl + 'guerre.html'] )
    liste.append( ['Histoire', sUrl + 'histoire.html'] )
    liste.append( ['Historique', sUrl + 'historique.html'] )
    liste.append( ['Horreur', sUrl + 'horreur.html'] )
    liste.append( ['Judiciaire', sUrl + 'judiciaire.html'] )
    liste.append( ['Médical', sUrl + 'medical.html'] )
    liste.append( ['Musical', sUrl + 'musical.html'] )
    liste.append( ['Péplum', sUrl + 'peplum.html'] )
    liste.append( ['Policier', sUrl + 'policier.html'] )
    liste.append( ['Romance', sUrl + 'romance.html'] )
    liste.append( ['Science-Fiction', sUrl + 'science-fiction.html'] )
    liste.append( ['Sport', sUrl + 'sport.html'] )
    liste.append( ['Thriller', sUrl + 'thriller.html'] )
    liste.append( ['Western', sUrl + 'western.html'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieGenres():
    oGui = cGui()
    sUrl = URL_MAIN + 'v2/series/genre/'

    liste = []
    liste.append( ['Action', sUrl + 'action/'] )
    liste.append( ['Animé', sUrl + 'anime/'] )
    liste.append( ['Aventure', sUrl + 'aventure/'] )
    liste.append( ['Comédie', sUrl + 'comedie/'] )
    liste.append( ['DC Comics', sUrl + 'dc-comics/'] )
    liste.append( ['Documentaire', sUrl + 'documentaire/'] )
    liste.append( ['Drama', sUrl + 'drama/'] )
    liste.append( ['Drame', sUrl + 'drame/'] )
    liste.append( ['Emission TV', sUrl + 'emission-tv/'] )
    liste.append( ['Epouvante-Horreur', sUrl + 'epouvante-horreur/'] )
    liste.append( ['Fantastique', sUrl + 'fantastique/'] )
    liste.append( ['Gore', sUrl + 'gore/'] )
    liste.append( ['Guerre', sUrl + 'guerre/'] )
    liste.append( ['Historique', sUrl + 'historique/'] )
    liste.append( ['Mystère', sUrl + 'mystere/'] )
    liste.append( ['Policier', sUrl + 'policier/'] )
    liste.append( ['Romance', sUrl + 'romance/'] )
    liste.append( ['Science-Fiction', sUrl + 'science-fiction/'] )
    liste.append( ['Série TV', sUrl + 'serie-tv/'] )
    liste.append( ['Thriller', sUrl + 'thriller/'] )
    liste.append( ['Télé-réalité', sUrl + 'tele-realite/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovieAnnees():
    oGui = cGui()

    for i in reversed (xrange(1914, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee/' + Year + '.html')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieAnnees():
    oGui = cGui()

    for i in reversed (xrange(1989, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'v2/series/annee/' + Year + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch
        sPattern = '<img class="img-responsive" *src="([^"]+)".+?<div class="divtelecha.+?href="([^"]+)">([^<>]+)<'
#        sPattern = '<div class="bloc-generale">.+?href="([^"]+)"> *<img class="img-responsive" *src="([^"]+)" *alt="([^"]+)"'
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        if '/series' in sUrl:
            sPattern = '<div class="divtelecha.+?href="([^"]+)"><strong>([^<]+)<\/strong>.+?<img class="img-responsive".+?src="([^"]+)"'
        else:  # films
            sPattern = '<h2 class="heading"> *<a href="[^"]+">([^<]+)<.+?<img class="img-responsive" *src="([^"]+)" *alt.+?(?:<font color="#.+?">([^<]+)<\/font>.+?).+?>film de (\d{4})<.+?Synopsis : ([^<]+)<.+?<div class="divtelecha.+?href="([^"]+)"'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
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
            
            sDesc = ''
            sYear = ''
            if sSearch:
                sQual = ''
                sThumb = URL_MAIN[:-1] + aEntry[0]
                sTitle = aEntry[2].replace('télécharger ', '').replace('en Streaming', '')
                sTitle = sTitle.replace(' TELECHARGEMENT GRATUIT', '').replace('gratuitement', '')
                sUrl2 = URL_MAIN[:-1] + aEntry[1]
            elif '/series' in sUrl:
                sQual = ''
                sUrl2 = URL_MAIN[:-1] + aEntry[0]
                sTitle = aEntry[1].replace('Regarder ', '').replace('en Streaming', '')
                sThumb = URL_MAIN[:-1] + aEntry[2]
            else:
                sTitle = aEntry[0]
                sThumb = URL_MAIN[:-1] + aEntry[1]
                sYear = aEntry[3]
                sDesc = aEntry[4].decode('utf-8')
                sDesc = cUtil().unescape(sDesc).encode('utf-8')
                sUrl2 = URL_MAIN[:-1] + aEntry[5]

                sQual = aEntry[2]
                if sQual:
                    sQual = sQual.decode("utf-8").replace(u' qualit\u00E9', '').replace('et ', '/').replace(' ', '')
                    sQual = sQual.replace('Haute', 'HD').replace('Bonne', 'DVD').replace('Mauvaise', 'SD').encode("utf-8")

            sUrl2 = sUrl2.replace('telecharger', 'streaming')
            sTitle = sTitle.decode("utf-8").replace(u'T\u00E9l\u00E9charger ', '')
            sTitle = sTitle.encode("utf-8")

            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sYear)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)

            if '/series/' in sUrl or '/series/' in sUrl2 or '/series_co/' in sThumb:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisonsEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    sNextPage = __checkForNextPage(sHtmlContent)
    if (sNextPage != False):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sNextPage)
        oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li><a href="([^"]+)" class="next">Suivant'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
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

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '(?:<h2 class="heading-small">(Saison .+?)<)|(?:<li><a title=".+? \| (.+?)" class="num_episode" href="([^"]+)")'
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

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            else:
                ePisode = aEntry[1].replace(',', '')
                sTitle = sMovieTitle + ' ' + ePisode
                sUrl = URL_MAIN[:-1] + aEntry[2]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    #refomatage url
    sUrl = ReformatUrl(sUrl)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if '/films' in sUrl:
        sType = 'films'
    elif 'saison' in sUrl or 'episode' in sUrl:
        sType = 'series'

    sUrl2 = sUrl.rsplit('/', 1)[1]
    idMov = re.sub('-.+', '', sUrl2)

    sPattern = '<div title="([^"]+)".+?streaming="([^"]+)" heberger="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
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

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sType', sType)
            oOutputParameterHandler.addParameter('idMov', idMov)
            oOutputParameterHandler.addParameter('idHeb', idHeb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler)

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

    #film
    if (oInputParameterHandler.exist('idMov')):
        idMov = oInputParameterHandler.getValue('idMov')
        pdata = 'id=' + idHeb + '&id_movie=' + idMov + '&type=' + sType
        pUrl = URL_MAIN + 'v2/video.php'
    else:
        #serie pas d'idmov
        pdata = 'id=' + idHeb + '&type=' + sType
        pUrl = URL_MAIN + 'v2/video.php'

    pUrl = pUrl + '?' + pdata

    oRequest = cRequestHandler(pUrl)
#     oRequest.setRequestType(oRequest.REQUEST_TYPE_POST)
#     oRequest.addParametersLine(pdata)
    oRequest.addHeaderEntry('Referer', sUrl)
    sHtmlContent = oRequest.request()
    sHtmlContent = sHtmlContent.replace('\\', '')

    sPattern = '<iframe.+?src="([^"]+)".+?"qualite":"([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl

            sQual = aEntry[1]

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = ('%s [%s]') % (sMovieTitle, sQual)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:
        # au cas où pas de qualité
        sPattern = '<iframe.+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sHosterUrl = aEntry
                if sHosterUrl.startswith('//'):
                    sHosterUrl = 'http:' + sHosterUrl

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
