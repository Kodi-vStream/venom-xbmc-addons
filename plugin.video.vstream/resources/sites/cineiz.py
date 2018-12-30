#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog
import re
return false

SITE_IDENTIFIER = 'cineiz'
SITE_NAME = 'Cineiz'
SITE_DESC = 'Films, Séries et mangas en streaming'

URL_MAIN = 'https://ww3.cineiz.io/'

URL_SEARCH = ('', 'showMovieSearch')
URL_SEARCH_MOVIES = ('', 'showMovieSearch')
URL_SEARCH_SERIES = ('', 'showMovieSearch')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'films.htm', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'films.htm', 'showMovies')
MOVIE_GENRES = ('http://film', 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
MOVIE_LIST = ('http://film', 'showList')

SERIE_NEWS = (URL_MAIN + 'series-tv.htm', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'series-tv.htm', 'showMovies')
SERIE_GENRES = ('http://serie', 'showGenres')
SERIE_ANNEES = (True, 'showSerieYears')
SERIE_LIST = (True, 'showList')

ANIM_NEWS = (URL_MAIN + 'animes/dernier/', 'showMovies')
ANIM_ANIMS = (URL_MAIN + 'animes.htm', 'showMovies')
ANIM_VIEWS = (URL_MAIN + 'animes/populaire/', 'showMovies')
ANIM_GENRES = (True, 'showGenres')
ANIM_ANNEES = (True, 'showAnimesYears')
ANIM_ENFANTS = (URL_MAIN + 'animes', 'showMovies')
ANIM_LIST = (True, 'showAnimesList')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Liste)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VIEWS[1], 'Animés (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_LIST[1], 'Animés (Liste)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovieSearch(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'film' in sUrl:
        code = 'films-genre-'
    elif 'serie' in sUrl:
        code = 'series-tv/genre-'
    else:
        code = 'animes-du-genre-'

    liste = []
    liste.append( ['Action', URL_MAIN + code + 'action.htm'] )
    liste.append( ['Animation', URL_MAIN +  code + 'animation.htm'] )
    liste.append( ['Arts Martiaux', URL_MAIN +  code + 'arts-martiaux.htm'] )
    liste.append( ['Aventure', URL_MAIN +  code + 'aventure.htm'] )
    liste.append( ['Biopic', URL_MAIN +  code + 'biopic.htm'] )
    liste.append( ['Classique', URL_MAIN +  code + 'classique.htm'] )
    liste.append( ['Comédie', URL_MAIN +  code + 'comedie.htm'] )
    liste.append( ['Comédie Dramatique', URL_MAIN +  code + 'comedie-dramatique.htm'] )
    liste.append( ['Comédie Musicale', URL_MAIN +  code + 'comedie-musicale.htm'] )
    liste.append( ['Dessin animé', URL_MAIN +  code + 'dessin-anime.htm'] )
    liste.append( ['Divers', URL_MAIN +  code + 'divers.htm'] )
    liste.append( ['Documentaire', URL_MAIN +  code + 'documentaire.htm'] )
    liste.append( ['Drame', URL_MAIN +  code + 'drame.htm'] )
    liste.append( ['Epouvante Horreur', URL_MAIN +  code + 'epouvante-horreur.htm'] )
    liste.append( ['Erotique', URL_MAIN +  code + 'erotique.htm'] )
    liste.append( ['Espionnage', URL_MAIN +  code + 'espionnage.htm'] )
    liste.append( ['Expérimental', URL_MAIN +  code + 'experimental.htm'] )
    liste.append( ['Famille', URL_MAIN +  code + 'famille.htm'] )
    liste.append( ['Fantastique', URL_MAIN +  code + 'fantastique.htm'] )
    liste.append( ['Guerre', URL_MAIN +  code + 'guerre.htm'] )
    liste.append( ['Historique', URL_MAIN +  code + 'historique.htm'] )
    liste.append( ['Judicaire', URL_MAIN +  code + 'judiciaire.htm'] )
    liste.append( ['Musical', URL_MAIN +  code + 'musical.htm'] )
    liste.append( ['Policier', URL_MAIN +  code + 'policier.htm'] )
    liste.append( ['Péplum', URL_MAIN +  code + 'peplum.htm'] )
    liste.append( ['Romance', URL_MAIN +  code + 'romance.htm'] )
    liste.append( ['Science Fiction', URL_MAIN +  code + 'science-fiction.htm'] )
    liste.append( ['Sport event', URL_MAIN +  code + 'sport-event.htm'] )
    liste.append( ['Thriller', URL_MAIN +  code + 'thriller.htm'] )
    liste.append( ['Western', URL_MAIN +  code + 'western.htm'] )
    liste.append( ['Non classé', URL_MAIN +  code + 'non-classe.htm'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showList():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'film' in sUrl:
        code = 'films-commence-par-'
    else:
        code = 'series-tv/commence-par-'

    liste = []
    liste.append( ['0', URL_MAIN + code + '0.htm'] )
    liste.append( ['1', URL_MAIN + code + '1.htm'] )
    liste.append( ['2', URL_MAIN + code + '2.htm'] )
    liste.append( ['3', URL_MAIN + code + '3.htm'] )
    liste.append( ['4', URL_MAIN + code + '4.htm'] )
    liste.append( ['5', URL_MAIN + code + '5.htm'] )
    liste.append( ['6', URL_MAIN + code + '6.htm'] )
    liste.append( ['7', URL_MAIN + code + '7.htm'] )
    liste.append( ['8', URL_MAIN + code + '8.htm'] )
    liste.append( ['9', URL_MAIN + code + '9.htm'] )
    liste.append( ['A', URL_MAIN + code + 'A.htm'] )
    liste.append( ['B', URL_MAIN + code + 'b.htm'] )
    liste.append( ['C', URL_MAIN + code + 'C.htm'] )
    liste.append( ['D', URL_MAIN + code + 'D.htm'] )
    liste.append( ['E', URL_MAIN + code + 'E.htm'] )
    liste.append( ['F', URL_MAIN + code + 'F.htm'] )
    liste.append( ['G', URL_MAIN + code + 'G.htm'] )
    liste.append( ['H', URL_MAIN + code + 'H.htm'] )
    liste.append( ['I', URL_MAIN + code + 'I.htm'] )
    liste.append( ['J', URL_MAIN + code + 'J.htm'] )
    liste.append( ['K', URL_MAIN + code + 'K.htm'] )
    liste.append( ['L', URL_MAIN + code + 'L.htm'] )
    liste.append( ['M', URL_MAIN + code + 'M.htm'] )
    liste.append( ['N', URL_MAIN + code + 'N.htm'] )
    liste.append( ['O', URL_MAIN + code + 'O.htm'] )
    liste.append( ['P', URL_MAIN + code + 'P.htm'] )
    liste.append( ['Q', URL_MAIN + code + 'Q.htm'] )
    liste.append( ['R', URL_MAIN + code + 'R.htm'] )
    liste.append( ['S', URL_MAIN + code + 'S.htm'] )
    liste.append( ['T', URL_MAIN + code + 'T.htm'] )
    liste.append( ['U', URL_MAIN + code + 'U.htm'] )
    liste.append( ['V', URL_MAIN + code + 'V.htm'] )
    liste.append( ['W', URL_MAIN + code + 'W.htm'] )
    liste.append( ['X', URL_MAIN + code + 'X.htm'] )
    liste.append( ['Y', URL_MAIN + code + 'Y.htm'] )
    liste.append( ['Z', URL_MAIN + code + 'Z.htm'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAnimesList():
    oGui = cGui()

    liste = []
    liste.append( ['09', URL_MAIN + 'animes/alphabet/09'] )
    liste.append( ['A', URL_MAIN + 'animes/alphabet/A'] )
    liste.append( ['B', URL_MAIN + 'animes/alphabet/B'] )
    liste.append( ['C', URL_MAIN + 'animes/alphabet/C'] )
    liste.append( ['D', URL_MAIN + 'animes/alphabet/D'] )
    liste.append( ['E', URL_MAIN + 'animes/alphabet/E'] )
    liste.append( ['F', URL_MAIN + 'animes/alphabet/F'] )
    liste.append( ['G', URL_MAIN + 'animes/alphabet/G'] )
    liste.append( ['H', URL_MAIN + 'animes/alphabet/H'] )
    liste.append( ['I', URL_MAIN + 'animes/alphabet/I'] )
    liste.append( ['J', URL_MAIN + 'animes/alphabet/J'] )
    liste.append( ['K', URL_MAIN + 'animes/alphabet/K'] )
    liste.append( ['L', URL_MAIN + 'animes/alphabet/L'] )
    liste.append( ['M', URL_MAIN + 'animes/alphabet/M'] )
    liste.append( ['N', URL_MAIN + 'animes/alphabet/N'] )
    liste.append( ['O', URL_MAIN + 'animes/alphabet/O'] )
    liste.append( ['P', URL_MAIN + 'animes/alphabet/P'] )
    liste.append( ['Q', URL_MAIN + 'animes/alphabet/Q'] )
    liste.append( ['R', URL_MAIN + 'animes/alphabet/R'] )
    liste.append( ['S', URL_MAIN + 'animes/alphabet/S'] )
    liste.append( ['T', URL_MAIN + 'animes/alphabet/T'] )
    liste.append( ['U', URL_MAIN + 'animes/alphabet/U'] )
    liste.append( ['V', URL_MAIN + 'animes/alphabet/V'] )
    liste.append( ['W', URL_MAIN + 'animes/alphabet/W'] )
    liste.append( ['X', URL_MAIN + 'animes/alphabet/X'] )
    liste.append( ['Y', URL_MAIN + 'animes/alphabet/Y'] )
    liste.append( ['Z', URL_MAIN + 'animes/alphabet/Z'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovieYears():
    oGui = cGui()

    for i in reversed (xrange(1921, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films-annee-' + Year + '.htm')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieYears():
    oGui = cGui()

    for i in reversed (xrange(1961, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series-tv/annee-' + Year + '.htm')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieSearch(sSearch = ''):
    oGui = cGui()

    if not sSearch:
        return
    else:
        sUrl = URL_MAIN + 'recherche'

    oRequestHandler = cRequestHandler(sUrl)
    #oRequestHandler.addHeaderEntry('Referer', 'https://www.cineiz.io/recherche')
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('action', 'recherche')
    oRequestHandler.addParameters('story', sSearch)

    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="unfilm".+?href="(.+?)".+?<img src="(.+?)".+?<span class="linkfilm">(.+?)</span>'

    oParser = cParser()
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

            sUrl2 = str(aEntry[0])
            sThumb = URL_MAIN + str(aEntry[1])
            sTitle = str(aEntry[2])
            sDesc = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/series-tv/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif '/anime/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
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

    sPattern = '<div class="unfilm".+?href="(.+?)".+?<img src="(.+?)".+?<span class="xquality">(.+?)</span>.+?<span class="xlangue">(.+?)</span>.+?<span class="linkfilm">(.+?)</span>'

    oParser = cParser()
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

            sUrl2 = str(aEntry[0])
            sThumb = str(aEntry[1])
            if 'films' in sUrl:
                sQual = str(aEntry[2])
                sLang = str(aEntry[3])
            else:
                sQual = ''
                sLang = ''
            sTitle = str(aEntry[4])
            sDesc = ''

            sDisplayTitle = ('%s (%s) (%s)') % (sTitle, sQual, sLang.upper())

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif '/anime' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
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
    sPattern = '<a href=\'([^<]+)\' rel=\'nofollow\'>suiv »'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        if aResult[1][0].startswith ('/'):
            return URL_MAIN[:-1] + aResult[1][0]
        else:
            return aResult[1][0]

    return False

def showSaisons():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="unepetitesaisons"><a href="(.+?)" title=.+?<div class="etlelien">(.+?)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = str(aEntry[0])
            #sTitle = str(aEntry[1]) + sMovieTitle
            sTitle = ('%s %s') % (aEntry[1], sMovieTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="n_episode2".+?href="([^"]+)"><span class="head">(.+?)</span><span class="body">(.+?)</span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = str(aEntry[1]) + str(aEntry[2]) + ' ' + sMovieTitle
            sUrl2 = str(aEntry[0])
            if sUrl2.startswith ('/'):
                sUrl2 = URL_MAIN[:-1] + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()
    import threading
    threads = []

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    #faut post
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('levideo', '123456')
    sHtmlContent = oRequestHandler.request().replace('<span class="telecharger_sur_uptobox"></span>', '')

    sDesc = ''
    try:
        sPattern = '<p>Synopsis.+?</strong> :(.+?)<\/p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    sPattern = '<div class="num_link">Lien:.+?<span class="(.+?)".+?span style="width:55px;" class="(.+?)">.+?<input name="levideo" value="(.+?)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHost = str(aEntry[0]).capitalize()
            if 'Nowvideo' in sHost:
                continue
            sLang = str(aEntry[1])
            sPost = str(aEntry[2])
            sTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sPost', sPost)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            #oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            #dispo a la version 0.6.2
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl').replace('https://streamcomplet.cineiz.io',URL_MAIN)
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sPost = oInputParameterHandler.getValue('sPost')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addParameters('levideo', sPost)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '</script></div></div><iframe src="(.+?)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            url = URL_MAIN + aEntry
            oRequestHandler = cRequestHandler(url)
            sHtmlContent = oRequestHandler.request()
            sHosterUrl = oRequestHandler.getRealUrl()

            if 'facebook.com' in sHosterUrl:
                continue

            if 'vimple.org' in sHosterUrl:
                oRequestHandler = cRequestHandler(sHosterUrl)
                oRequestHandler.addHeaderEntry('Referer', sUrl)
                sHtmlContent2 = oRequestHandler.request()
                try:
                    sHosterUrl = re.search('url=([^"]+)"', sHtmlContent2, re.DOTALL).group(1)
                except:
                    sHosterUrl = str(oRequestHandler.getRealUrl())

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
