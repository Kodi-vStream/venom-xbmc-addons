#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
return False 
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

MOVIE_MOVIE = (URL_MAIN + 'film-en-streaming', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'film-en-streaming', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
MOVIE_LIST = (URL_MAIN + 'alphabet', 'showAlpha')

SERIE_NEWS = (URL_MAIN + 'series-tv-streaming/', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'series-tv-streaming/', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'serie', 'showGenres')
SERIE_ANNEES = (True, 'showSerieYears')
SERIE_LIST = (URL_MAIN + 'series/alphabet', 'showAlpha')

ANIM_ANIMS = (URL_MAIN + 'animes/', 'showMovies')
ANIM_NEWS = (URL_MAIN + 'animes/dernier/', 'showMovies')
ANIM_LIST = (URL_MAIN + 'animes/alphabet/', 'AlphaSearch')
ANIM_VIEWS = (URL_MAIN + 'animes/populaire/', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Par ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Par ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_LIST[1], 'Animés (Par ordre alphabétique)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VIEWS[1], 'Animés (Les plus vus)', 'views.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def AlphaSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    progress_ = progress().VScreate(SITE_NAME)

    for i in range(0, 27) :
        progress_.VSupdate(progress_, 36)

        if (i > 0):
            sTitle = chr(64 + i)
        else:
            sTitle = '09'

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + sTitle.upper())
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'az.png', oOutputParameterHandler)

    progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

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
    #liste.append( ['Classique', URL + 'classique.htm'] )
    liste.append( ['Comédie', URL + 'comedie_1'] )
    liste.append( ['Comédie Dramatique', URL + 'comedie-dramatique_1'] )
    #liste.append( ['Comédie Musicale', URL + 'comedie-musicale.htm'] )
    #liste.append( ['Dessin animé', URL + 'dessin-anime.htm'] )
    #liste.append( ['Divers', URL + 'divers.htm'] )
    liste.append( ['Documentaire', URL + 'documentaire_1'] )
    liste.append( ['Drame', URL + 'drame_1'] )
    liste.append( ['Epouvante Horreur', URL +  'epouvante-horreur_1'] )
    liste.append( ['Erotique', URL + 'erotique_1'] )
    liste.append( ['Espionnage', URL + 'espionnage_1'] )
    #liste.append( ['Expérimental', URL + 'experimental.htm'] )
    #liste.append( ['Famille', URL + 'famille.htm'] )
    liste.append( ['Fantastique', URL + 'fantastique_1'] )
    liste.append( ['Guerre', URL +  'guerre_1'] )
    liste.append( ['Historique', URL + 'historique_1'] )
    #liste.append( ['Judicaire', URL + 'judiciaire.htm'] )
    liste.append( ['Musical', URL + 'musical_1'] )
    liste.append( ['Policier', URL + 'policier_1'] )
    #liste.append( ['Péplum', URL + 'peplum.htm'] )
    liste.append( ['Romance', URL +  'romance_1'] )
    liste.append( ['Science Fiction', URL + 'science-fiction_1'] )
    #liste.append( ['Sport event', URL + 'sport-event.htm'] )
    liste.append( ['Thriller', URL + 'thriller_1'] )
    liste.append( ['Western', URL +  'western_1'] )
    liste.append( ['Non classé', URL + 'non-classe_1'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
    oGui = cGui()

    for i in reversed (xrange(1913, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieYears():
    oGui = cGui()

    for i in reversed (xrange(1936, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
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
    liste.append( ['0', URL_MAIN + code + '0'] )
    liste.append( ['1', URL_MAIN + code + '1'] )
    liste.append( ['2', URL_MAIN + code + '2'] )
    liste.append( ['3', URL_MAIN + code + '3'] )
    liste.append( ['4', URL_MAIN + code + '4'] )
    liste.append( ['5', URL_MAIN + code + '5'] )
    liste.append( ['6', URL_MAIN + code + '6'] )
    liste.append( ['7', URL_MAIN + code + '7'] )
    liste.append( ['8', URL_MAIN + code + '8'] )
    liste.append( ['9', URL_MAIN + code + '9'] )
    liste.append( ['A', URL_MAIN + code + 'A'] )
    liste.append( ['B', URL_MAIN + code + 'B'] )
    liste.append( ['C', URL_MAIN + code + 'C'] )
    liste.append( ['D', URL_MAIN + code + 'D'] )
    liste.append( ['E', URL_MAIN + code + 'E'] )
    liste.append( ['F', URL_MAIN + code + 'F'] )
    liste.append( ['G', URL_MAIN + code + 'G'] )
    liste.append( ['H', URL_MAIN + code + 'H'] )
    liste.append( ['I', URL_MAIN + code + 'I'] )
    liste.append( ['J', URL_MAIN + code + 'J'] )
    liste.append( ['K', URL_MAIN + code + 'K'] )
    liste.append( ['L', URL_MAIN + code + 'L'] )
    liste.append( ['M', URL_MAIN + code + 'M'] )
    liste.append( ['N', URL_MAIN + code + 'N'] )
    liste.append( ['O', URL_MAIN + code + 'O'] )
    liste.append( ['P', URL_MAIN + code + 'P'] )
    liste.append( ['Q', URL_MAIN + code + 'Q'] )
    liste.append( ['R', URL_MAIN + code + 'R'] )
    liste.append( ['S', URL_MAIN + code + 'S'] )
    liste.append( ['T', URL_MAIN + code + 'T'] )
    liste.append( ['U', URL_MAIN + code + 'U'] )
    liste.append( ['V', URL_MAIN + code + 'V'] )
    liste.append( ['W', URL_MAIN + code + 'W'] )
    liste.append( ['X', URL_MAIN + code + 'X'] )
    liste.append( ['Y', URL_MAIN + code + 'Y'] )
    liste.append( ['Z', URL_MAIN + code + 'Z'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'az.png', oOutputParameterHandler)

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
            sUrl = aEntry[0].replace(URL_MAIN, '')
            sUrl = URL_MAIN + sUrl
            sThumb = aEntry[1].replace(URL_MAIN, '')
            sThumb = URL_MAIN + sThumb
            sTitle = aEntry[2]

            if aEntry[3]:
                sDisplayTitle = ('%s (%s)') % (sTitle, aEntry[3])
            else:
                sDisplayTitle = sTitle

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)


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
        sUrl = aResult[1][0].replace(URL_MAIN, '')
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

            sUrl2 = aEntry[0].replace(URL_MAIN, '')
            sUrl2 = URL_MAIN + sUrl2
            #sTitle = aEntry[1] + sMovieTitle
            sTitle = aEntry[1]
            sThumb = aEntry[2].replace(URL_MAIN, '')
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

            sTitle = aEntry[0]
            sUrl2 = aEntry[1].replace(URL_MAIN, '')
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
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="seme.+?data-src="(.+?)".+?style="width:55px;" class="(.+?)".+?<img border="0".+?>(.+?)</span>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            sLang = aEntry[1].replace('L', '')
            sHost = aEntry[2].capitalize()

            sTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang.upper(), sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
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
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)

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
