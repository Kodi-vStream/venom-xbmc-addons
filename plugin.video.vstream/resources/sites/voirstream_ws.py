#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
#clone de voirfilm_org
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'voirstream_ws'
SITE_NAME = 'VoirStream'
SITE_DESC = 'Films, Séries et mangas en streaming'

URL_MAIN = 'http://www.voirstream.ws/'

URL_SEARCH = (URL_MAIN + 'recherche?story=', 'showMovie')
URL_SEARCH_MOVIES = (URL_MAIN + 'recherche?story=', 'showMovie')
URL_SEARCH_SERIES = (URL_MAIN + 'recherche?story=', 'showMovie')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'film-en-streaming/', 'showMovies')
MOVIE_MOVIE = ('', 'load')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

SERIE_NEWS = (URL_MAIN + 'series-tv-streaming/', 'showMovies')
SERIE_SERIES = ('', 'load')
SERIE_GENRES = ('serie', 'showGenres')
SERIE_ANNEES = ('serie', 'showYears')


ANIM_NEWS = (URL_MAIN + 'animes/', 'showMovies')
ANIM_ANIMS = ('', 'load')
ANIM_VIEWS = (URL_MAIN + 'animes/populaire/', 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'films_annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par Années)', 'series_annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VIEWS[1], 'Animés (Les plus vus)', 'animes_views.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'serie' in sUrl:
        URL = '%s/series/' % URL_MAIN
    else:
        URL = URL_MAIN

    liste = []
    liste.append( ['Aventure', URL + 'aventure_1'] )
    liste.append( ['Action', URL + 'action_1'] )
    liste.append( ['Animation', URL + 'animation_1'] )
    liste.append( ['Arts Martiaux', URL + 'arts-martiaux_1'] )
    liste.append( ['Biopic', URL + 'biopic_1'] )
    # liste.append( ['Classique', URL +  code + 'classique.htm'] )
    liste.append( ['Comédie', URL + 'comedie_1'] )
    liste.append( ['Comédie Dramatique', URL + 'comedie-dramatique_1'] )
    # liste.append( ['Comédie Musicale', URL +  code + 'comedie-musicale.htm'] )
    # liste.append( ['Dessin animé', URL +  code + 'dessin-anime.htm'] )
    # liste.append( ['Divers', URL +  code + 'divers.htm'] )
    liste.append( ['Documentaire', URL + 'documentaire_1'] )
    liste.append( ['Drame', URL + 'drame_1'] )
    liste.append( ['Epouvante Horreur', URL +  'epouvante-horreur_1'] )
    liste.append( ['Erotique', URL + 'erotique_1'] )
    liste.append( ['Espionnage', URL + 'espionnage_1'] )
    #liste.append( ['Expérimental', URL +  code + 'experimental.htm'] )
    #liste.append( ['Famille', URL +  code + 'famille.htm'] )
    liste.append( ['Fantastique', URL + 'fantastique_1'] )
    liste.append( ['Guerre', URL +  'guerre_1'] )
    liste.append( ['Historique', URL + 'historique_1'] )
    #liste.append( ['Judicaire', URL +  code + 'judiciaire.htm'] )
    liste.append( ['Musical', URL + 'musical_1'] )
    liste.append( ['Policier', URL + 'policier_1'] )
    #liste.append( ['Péplum', URL +  code + 'peplum.htm'] )
    liste.append( ['Romance', URL +  'romance_1'] )
    liste.append( ['Science Fiction', URL + 'science-fiction_1'] )
    #liste.append( ['Sport event', URL +  code + 'sport-event.htm'] )
    liste.append( ['Thriller', URL + 'thriller_1'] )
    liste.append( ['Western', URL +  'western_1'] )
    liste.append( ['Non classé', URL + 'non-classe_1'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'serie' in sUrl:
        URL = "%s/series/annee-" % URL_MAIN
    else:
        URL = "%s/films/annee-" % URL_MAIN

    for i in reversed (xrange(1996, 2019)):
        Year = str(i)
        #http://www.voirstream.ws/series/annee-2013/
        #http://www.voirstream.ws/films/annee-2013
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="unfilm".+?<a href="(.+?)".+?<img src="(.+?)".+?class="titreunfilm".+?>(.+?)<(?:.+?<span class="qualite (.+?)"|)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            ##pas les memes url
            sUrl = str(aEntry[0]).replace('http://www.voirstream.ws/', '')
            sUrl = URL_MAIN + sUrl
            sThumb = str(aEntry[1]).replace('http://www.voirstream.ws/', '')
            sThumb = URL_MAIN + sThumb

            if aEntry[3]:
                sDisplayTitle = ('%s (%s)') % (aEntry[2], aEntry[3])
            else:
                sDisplayTitle = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)


            if '/serie/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            elif '/anime' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

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
    sPattern = "<a href=\'([^<]+)\' rel=\'nofollow\'>suiv"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sUrl = aResult[1][0].replace('http://www.voirstream.ws/', '')
        sUrl = URL_MAIN + sUrl
        return sUrl
    else:
        return False

def showSaisons():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="unepetitesaisons"><a href="(.+?)" title="(.+?)">.+?<img src="(.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        for aEntry in aResult[1]:

            sUrl2 = str(aEntry[0]).replace('http://www.voirstream.ws/', '')
            sUrl2 = URL_MAIN + sUrl2
            #sTitle = str(aEntry[1]) + sMovieTitle
            sTitle = str(aEntry[1])
            sThumb = str(aEntry[2]).replace('http://www.voirstream.ws/', '')
            sThumb = URL_MAIN + sThumb

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="n_episode2" title="(.+?),.+?href="(.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        for aEntry in aResult[1]:

            sTitle = str(aEntry[0])
            sUrl2 = str(aEntry[1]).replace('http://www.voirstream.ws/', '')
            sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)


    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('title')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="seme.+?data-src="(.+?)".+?style="width:55px;" class="(.+?)".+?<img border="0".+?>(.+?)</span>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHost = str(aEntry[2]).capitalize()
            sLang = str(aEntry[1]).replace('L', '')
            sTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    #oRequestHandler.addHeaderEntry('Host', 'www.voirstream.ws')
    oRequestHandler.addHeaderEntry('Referer', 'http://www.voirstream.ws/')

    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = 'url=(.+?)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        sHosterUrl = str(aResult[1][0])

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
