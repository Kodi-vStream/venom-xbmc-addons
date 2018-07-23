#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

#from resources.lib.util import cUtil #outils pouvant etre utiles

SITE_IDENTIFIER = 'k_streaming'
SITE_NAME = 'K-Streaming'
SITE_DESC = 'films en streaming, streaming hd, streaming 720p, Films/séries, récent'

URL_MAIN = 'https://fr.k-streaming.com/'

#definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle sera affichee.
#LA RECHERCHE GLOBAL N'UTILE PAS showSearch MAIS DIRECTEMENT LA FONCTION INSCRITE DANS LA VARIABLE URL_SEARCH_*
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
#recherche global films
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
#recherche global serie
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
#recherche global divers
URL_SEARCH_MISC = (URL_MAIN + '?s=', 'showMovies')
#
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_MOVIE = (URL_MAIN, 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'film-les-plus-vues/', 'showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'films-plus-commenter-streaming/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'film-streaming-populaires/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = (URL_MAIN + 'film/serie-gratuit/', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'film/serie-gratuit/', 'showMovies')
SERIE_VIEWS =  (URL_MAIN + 'film-les-plus-vues/', 'showMovies')
SERIE_COMMENTS = (URL_MAIN + 'films-plus-commenter-streaming/', 'showMovies')
SERIE_NOTES = (URL_MAIN + 'film-streaming-populaires/', 'showMovies')

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
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_COMMENTS[1], 'Films (Les plus commentés)', 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Les plus vues)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_COMMENTS[1], 'Séries (Les plus commentées) ', 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NOTES[1], 'Séries (Les mieux notées)', 'notes.png', oOutputParameterHandler)

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

    liste = []
    liste.append( ['Action', URL_MAIN + 'film/action-gratuit-vf/'] )
    liste.append( ['Animation', URL_MAIN + 'film/animation-gratuit/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'film/arts-martiaux-streaming-vf/'] )
    liste.append( ['Aventure', URL_MAIN + 'film/aventure-streaming-vf/'] )
    liste.append( ['Comédie', URL_MAIN + 'film/films-comedie-streaming/'] )
    liste.append( ['Documentaire', URL_MAIN + 'film/documentaire-streaming/'] )
    liste.append( ['Drame', URL_MAIN + 'film/film-drame-streaming-vf/'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'film/horreur-streaming-film/'] )
    liste.append( ['Espionnage', URL_MAIN + 'film-espionnage-streaming/'] )
    liste.append( ['Famille', URL_MAIN + 'film/famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'film-fantastique-streaming/'] )
    liste.append( ['Guerre', URL_MAIN + 'film/film-guerre-streaming/'] )
    liste.append( ['Historique', URL_MAIN + 'film/film-historique-streaming/'] )
    liste.append( ['Musical', URL_MAIN + 'film/film-musical-streaming/'] )
    liste.append( ['Policier', URL_MAIN + 'film/film-policier-streaming/'] )
    liste.append( ['Romance', URL_MAIN + 'film-romance-streaming/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'film/film-science-fiction-streaming/'] )
    liste.append( ['Spectacle', URL_MAIN + 'film/film-spectacles-streaming/'] )
    liste.append( ['Thriller', URL_MAIN + 'film/film-thriller-streaming/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

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

    sPattern = '<div class="moviefilm"><a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"'
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

            sTitle = str(aEntry[2]).replace('&#8217;', '\'')
            #delete du tiret pour les series
            sTitle = sTitle.replace(' - Saison', ' Saison')
            sUrl2 = 'https:' + str(aEntry[0])
            sThumb = 'https:' + str(aEntry[1])
            sDesc = ''

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '-saison-' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

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
    sPattern = '<a class="nextpostslink" rel="next" href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return 'https:' + aResult[1][0]

    return False


def showEpisodes():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #recuperation du synopsis
    sDesc = ''
    try:
        sPattern = 'Synopsis</span>:([^<]+)<'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
            #sDesc = sDesc.replace('<br />', '').replace('&#8230;', '...').replace('&#8217;', '\'')
    except:
        pass

    #recuperation du hoster de base
    ListeUrl = []
    sPattern = '<div class="keremiya_part"> *<span>([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        ListeUrl = [(sUrl, aResult[1][0])]

    #recuperation des suivants
    sPattern = '<a href="([^<]+)"><span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    ListeUrl = ListeUrl + aResult[1]

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in ListeUrl:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = sMovieTitle + str(aEntry[1])
            sUrl2 = str(aEntry[0])
            if sUrl2.startswith ('/'):
                sUrl2 = 'https:' + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    #si un seul episode
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle + 'episode 1')
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addTV(SITE_IDENTIFIER, 'showHosters', sMovieTitle + 'episode 1', '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<iframe.+?src="(.+?)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry)
            if '//www.facebook.com/' in sHosterUrl:
                continue

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
