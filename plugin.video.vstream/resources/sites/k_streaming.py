#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
import re

SITE_IDENTIFIER = 'k_streaming'
SITE_NAME = 'K-Streaming'
SITE_DESC = 'Regarder Films et Séries en Streaming gratuit'

URL_MAIN = 'https://www1.k-streaming.co'

#definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle sera affichee.
#LA RECHERCHE GLOBAL N'UTILE PAS showSearch MAIS DIRECTEMENT LA FONCTION INSCRITE DANS LA VARIABLE URL_SEARCH_*
FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '/recherche/', 'showMovies')
#recherche global films
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
#recherche global serie
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_NEWS = (URL_MAIN + '/films/', 'showMovies')
MOVIE_MOVIE = ('http://', 'showMenuMovies')
# MOVIE_VIEWS = (URL_MAIN + '/film-les-plus-vues/', 'showMovies')
# MOVIE_COMMENTS = (URL_MAIN + '/films-plus-commenter-streaming/', 'showMovies')
# MOVIE_NOTES = (URL_MAIN + '/film-streaming-populaires/', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')
MOVIE_LIST = (URL_MAIN, 'showAlpha')

SERIE_SERIES = ('http://', 'showMenuSeries')
SERIE_NEWS = (URL_MAIN + '/series/', 'showMovies')
# SERIE_VIEWS =  (URL_MAIN + '/film-les-plus-vues/', 'showMovies')
# SERIE_COMMENTS = (URL_MAIN + '/films-plus-commenter-streaming/', 'showMovies')
# SERIE_NOTES = (URL_MAIN + '/film-streaming-populaires/', 'showMovies')
SERIE_GENRES = (SERIE_NEWS[0], 'showGenres')
SERIE_ANNEES = (True, 'showSeriesYears')
SERIE_LIST = (URL_MAIN + '/series/', 'showAlpha')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

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
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Ordre alphabétique)', 'listes.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_COMMENTS[1], 'Films (Les plus commentés)', 'comments.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'notes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Ordre alphabétique)', 'listes.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Les plus vues)', 'views.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', SERIE_COMMENTS[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_COMMENTS[1], 'Séries (Les plus commentées) ', 'comments.png', oOutputParameterHandler)

    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', SERIE_NOTES[0])
    # oGui.addDir(SITE_IDENTIFIER, SERIE_NOTES[1], 'Séries (Les mieux notées)', 'notes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText.replace(' ', '+')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append( ['Action', sUrl + '/action_1/'] )
    liste.append( ['Animation', sUrl + '/animation_1/'] )
    liste.append( ['Arts Martiaux', sUrl + '/arts-martiaux_1/'] )
    liste.append( ['Aventure', sUrl + '/aventure_1/'] )
    liste.append( ['Comédie', sUrl + '/comedie_1/'] )
    liste.append( ['Documentaire', sUrl + '/documentaire_1/'] )
    liste.append( ['Biopic', sUrl + '/biopic_1/'] )
    liste.append( ['Drame', sUrl + '/drame_1/'] )
    liste.append( ['Epouvante Horreur', sUrl + '/epouvante-horreur_1/'] )
    liste.append( ['Erotique', sUrl + '/erotique_1/'] )
    liste.append( ['Espionnage', sUrl + '/espionnage_1/'] )
    liste.append( ['Famille', sUrl + '/famille_1'] )
    liste.append( ['Fantastique', sUrl + '/fantastique_1/'] )
    liste.append( ['Guerre', sUrl + '/guerre_1/'] )
    liste.append( ['Historique', sUrl + '/historique_1/'] )
    liste.append( ['Musical', sUrl + '/musical_1/'] )
    liste.append( ['Policier', sUrl + '/policier_1/'] )
    liste.append( ['Romance', sUrl + '/romance_1/'] )
    liste.append( ['Science Fiction', sUrl + '/science-fiction_1/'] )
    liste.append( ['Spectacle', sUrl + '/spectacles_1/'] )
    liste.append( ['Thriller', sUrl + '/thriller_1/'] )
    liste.append( ['Comédie Dramatique', sUrl + '/comedie-dramatique_1/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAlpha():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = []
    liste.append( ['0', sUrl + '/alphabet/0'] )
    liste.append( ['1', sUrl + '/alphabet/1'] )
    liste.append( ['2', sUrl + '/alphabet/2'] )
    liste.append( ['3', sUrl + '/alphabet/3'] )
    liste.append( ['4', sUrl + '/alphabet/4'] )
    liste.append( ['5', sUrl + '/alphabet/5'] )
    liste.append( ['6', sUrl + '/alphabet/6'] )
    liste.append( ['7', sUrl + '/alphabet/7'] )
    liste.append( ['8', sUrl + '/alphabet/8'] )
    liste.append( ['9', sUrl + '/alphabet/9'] )
    liste.append( ['A', sUrl + '/alphabet/A'] )
    liste.append( ['B', sUrl + '/alphabet/B'] )
    liste.append( ['C', sUrl + '/alphabet/C'] )
    liste.append( ['D', sUrl + '/alphabet/D'] )
    liste.append( ['E', sUrl + '/alphabet/E'] )
    liste.append( ['F', sUrl + '/alphabet/F'] )
    liste.append( ['G', sUrl + '/alphabet/G'] )
    liste.append( ['H', sUrl + '/alphabet/H'] )
    liste.append( ['I', sUrl + '/alphabet/I'] )
    liste.append( ['J', sUrl + '/alphabet/J'] )
    liste.append( ['K', sUrl + '/alphabet/K'] )
    liste.append( ['L', sUrl + '/alphabet/L'] )
    liste.append( ['M', sUrl + '/alphabet/M'] )
    liste.append( ['N', sUrl + '/alphabet/N'] )
    liste.append( ['O', sUrl + '/alphabet/O'] )
    liste.append( ['P', sUrl + '/alphabet/P'] )
    liste.append( ['Q', sUrl + '/alphabet/Q'] )
    liste.append( ['R', sUrl + '/alphabet/R'] )
    liste.append( ['S', sUrl + '/alphabet/S'] )
    liste.append( ['T', sUrl + '/alphabet/T'] )
    liste.append( ['U', sUrl + '/alphabet/U'] )
    liste.append( ['V', sUrl + '/alphabet/V'] )
    liste.append( ['W', sUrl + '/alphabet/W'] )
    liste.append( ['X', sUrl + '/alphabet/X'] )
    liste.append( ['Y', sUrl + '/alphabet/Y'] )
    liste.append( ['Z', sUrl + '/alphabet/Z'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showYears():#creer une liste inversée d'annees
    oGui = cGui()

    for i in reversed (xrange(1918, 2021)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/films/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeriesYears():#creer une liste inversée d'annees
    oGui = cGui()

    for i in reversed (xrange(1980, 2021)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + '/series/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if sSearch:
        sUrl = sSearch.replace(' ', '+')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #la qualité est une option pour la recherche
    sPattern = '<div class="imagefilm">\s*<a href="([^"]+)".+?<img src="([^"]+)" alt="([^"]+)".+?(?:|<span class="([^"]+)".+?)<\/div>'
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
            sTitle = aEntry[2].replace('Streaming', '')
            sQual = aEntry[3].replace('qualite ', '')
            sDisplayTitle = sTitle + ' [' + sQual + ']'

            sDesc = ''
            if not sThumb.startswith('http'):
                sThumb = URL_MAIN + sThumb

            if not sUrl2.startswith('http'):
                sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)


            if '-saison-' in sUrl2 or '/series-' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'href="([^"]+)">>>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]

    return False

def showSaisons():
    #Uniquement saison a chaque fois
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<div class="unepetitesaisons">\s*<a href="([^"]+)" title="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        for aEntry in aResult[1]:

            sUrl = aEntry[0]
            sTitle = aEntry[1]
            sTitle = re.sub(' - Saison \d+', '', sTitle)#double affichage de la saison

            if not sUrl.startswith('http'):
                sUrl = URL_MAIN + sUrl

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="n_episode2" title="([^"]+)"\s*href="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        for aEntry in aResult[1]:

            sTitle = aEntry[0].replace(' , VOSTFR , ', '')#Systematiquement affiché en vostfr
            sTitle = re.sub(' - Saison \d+', '', sTitle)#double affichage de la saison
            sUrl = aEntry[1]
            if not sUrl.startswith('http'):
                sUrl = URL_MAIN + sUrl

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'data-src="([^"]+)" target="filmPlayer"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            if '//www.facebook.com/' in sHosterUrl:
                continue

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
