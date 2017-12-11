#-*- coding: utf-8 -*-
#Aria800.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser


SITE_IDENTIFIER = 'papstream'
SITE_NAME = 'PapStream'
SITE_DESC = 'Films série manga'

URL_MAIN = 'http://www.papstream.net'

URL_SEARCH = (URL_MAIN + '/films-en-streaming?search=', 'showMovies')

URL_SEARCH_MOVIES = (URL_MAIN + '/films-en-streaming?search=', 'showMovies')
#URL_SEARCH_SERIES = (URL_MAIN + 'films-en-streaming?search=', 'showMovies')

FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + '/dernier-films.html', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + '/films.html', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = (URL_MAIN + '/series.html', 'showMovies')
SERIE_GENRES = (True, 'showGenresTv')

ANIM_ANIMS = (URL_MAIN + '/animes.html', 'showMovies')
ANIM_GENRES = (True, 'showGenresManga')

def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)


    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'animes_genres.png', oOutputParameterHandler)

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
    liste.append( ['Action', URL_MAIN + '/films/action/'] )
    liste.append( ['Animation',URL_MAIN + '/films/animation/'] )
    liste.append( ['Aventure',URL_MAIN + '/films/aventure/'] )
    liste.append( ['Biopic',URL_MAIN + '/films/biopic/'] )
    liste.append( ['Comédie',URL_MAIN +'/films/comedie/'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + '/films/comedie-dramatique/'] )
    liste.append( ['Comédie Musicale',URL_MAIN + '/films/comedie-musicale/'] )
    liste.append( ['Divers',URL_MAIN + '/films/divers/'] )
    liste.append( ['Documentaire',URL_MAIN + '/films/documentaire/'] )
    liste.append( ['Drame',URL_MAIN + '/films/drame/'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + '/films/epouvante-horreur/'] )
    liste.append( ['Famille',URL_MAIN + '/films/famille/'] )
    liste.append( ['Fantastique',URL_MAIN + '/films/fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + '/films/guerre/'] )
    liste.append( ['Policier',URL_MAIN + '/films/policier/'] )
    liste.append( ['Romance',URL_MAIN +'/films/romance/'] )
    liste.append( ['Science Fiction',URL_MAIN + '/films/science-fiction/'] )
    liste.append( ['Thriller',URL_MAIN + '/films/thriller/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenresTv():
    oGui = cGui()


    liste = []
    liste.append( ['Action', URL_MAIN + '/series/action/'] )
    liste.append( ['Animation',URL_MAIN + '/series/animation/'] )
    liste.append( ['Aventure',URL_MAIN + '/series/aventure/'] )
    liste.append( ['Biopic',URL_MAIN + '/series/biopic/'] )
    liste.append( ['Comédie',URL_MAIN +'/series/comedie/'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + '/series/comedie-dramatique/'] )
    liste.append( ['Comédie Musicale',URL_MAIN + '/series/comedie-musicale/'] )
    liste.append( ['Divers',URL_MAIN + '/series/divers/'] )
    liste.append( ['Documentaire',URL_MAIN + '/series/documentaire/'] )
    liste.append( ['Drame',URL_MAIN + '/series/drame/'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + '/series/epouvante-horreur/'] )
    liste.append( ['Famille',URL_MAIN + '/series/famille/'] )
    liste.append( ['Fantastique',URL_MAIN + '/series/fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + '/series/guerre/'] )
    liste.append( ['Policier',URL_MAIN + '/series/policier/'] )
    liste.append( ['Romance',URL_MAIN +'/series/romance/'] )
    liste.append( ['Science Fiction',URL_MAIN + '/series/science-fiction/'] )
    liste.append( ['Thriller',URL_MAIN + '/series/thriller/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenresManga():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + '/animes/action/'] )
    liste.append( ['Animation',URL_MAIN + '/animes/animation/'] )
    liste.append( ['Aventure',URL_MAIN + '/animes/aventure/'] )
    liste.append( ['Biopic',URL_MAIN + '/animes/biopic/'] )
    liste.append( ['Comédie',URL_MAIN +'/animes/comedie/'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + '/animes/comedie-dramatique/'] )
    liste.append( ['Comédie Musicale',URL_MAIN + '/animes/comedie-musicale/'] )
    liste.append( ['Divers',URL_MAIN + '/animes/divers/'] )
    liste.append( ['Documentaire',URL_MAIN + '/animes/documentaire/'] )
    liste.append( ['Drame',URL_MAIN + '/animes/drame/'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + '/animes/epouvante-horreur/'] )
    liste.append( ['Famille',URL_MAIN + '/animes/famille/'] )
    liste.append( ['Fantastique',URL_MAIN + '/animes/fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + '/animes/guerre/'] )
    liste.append( ['Policier',URL_MAIN + '/animes/policier/'] )
    liste.append( ['Romance',URL_MAIN +'/animes/romance/'] )
    liste.append( ['Science Fiction',URL_MAIN + '/animes/science-fiction/'] )
    liste.append( ['Thriller',URL_MAIN + '/animes/thriller/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

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

    sPattern = 'shortstory-in.+?<img src="([^"]+)".+?short-link"><a href="(.+?)".+?>(.+?)</a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)


    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = str(aEntry[2])
            sUrl = URL_MAIN + aEntry[1]
            sThumb = URL_MAIN + aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="col-xs-4">\s*<a href="(.+?)".+?src="(.+?)".+?<h3>(.+?)</h3>\s*<p>(.+?)</p>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl2 = str(aEntry[0])
            sThumb = str(aEntry[1])
            if sThumb.startswith('/'):
                sThumb = URL_MAIN[:-1] + sThumb
            sTitle = str(aEntry[2])
            sDesc = str(aEntry[3])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaison', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = "<span>.+?</span><a href='(.+?)'"
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]

    return False

def ShowSerieSaison():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    #Decoupage pour cibler la partie des saisons
    sPattern = '<div class="collapse navbar-collapse" id="navbar-saisons">(.+?)<nav class="navbar navbar-default navbar-custom">'

    aResult = oParser.parse(sHtmlContent, sPattern)
    sHtmlContent = aResult

    sPattern = '<a href="(.+?)" title="Voir en streaming.+?">(.+?)</a>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sUrl2 = str(aEntry[0])
            sSaison = str(aEntry[1])
            sUrl2 = sUrl + sUrl2
            sTitle = sSaison + sMovieTitle

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addTV(SITE_IDENTIFIER, 'ShowSerieEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        oGui.setEndOfDirectory()

def ShowSerieEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<article class="col-xs-12 col-md-6 preview">\s*<a href="(.+?)" title="Voir en streaming (.+?)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)

        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = str(aEntry[1])
            sUrl2 = sUrl + str(aEntry[0])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'seriesHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def seriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    #Decoupage pour supprimer les doublons host
    sPattern = '<strong>Liens en streaming disponibles:</strong>(.+?)<aside class="container" id="embed-container">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    sHtmlContent = aResult

    sPattern = '<button data-src="([^<]+)" class="btn btn-primary.+?">(.+?)</button>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    cConfig().log(str(sUrl))

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if 'VF' in aEntry[1]:
                sLang = ' [VF]'
            if 'VOSTFR' in aEntry[1]:
                sLang = ' [VOSTFR]'
            sTitle = sMovieTitle + sLang

            sHosterUrl = str(aEntry[0])

            if '//goo.gl' in sHosterUrl:
                import urllib2
                try:
                    cConfig().log('ok ' + sHosterUrl)
                    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
                    request = urllib2.Request(sHosterUrl, None, headers)
                    reponse = urllib2.urlopen(request)
                    sHosterUrl = reponse.geturl()
                except:
                    pass

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def showHosters():

    #ne fonctionne pas retourne la mauvaise URL une redirection ? des cookies ?
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = 'id="fplay".+?rel="(.+?)".+?player_v_DIV_5">.+?<\/i>(.+?)<\/span>.+?<img src="(.+?)".+?<span.+?>(.+?)<'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sLang = str(aEntry[2]).replace('/images/', '').replace('.png', '')

            sQual = str(aEntry[3])

            sTitle = '%s (%s) %s' % (sMovieTitle,sLang, sQual)

            sHosterUrl = str(aEntry[0])

            #cherche la vrais url
            import urllib2
            try:
                headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
                request = urllib2.Request(sHosterUrl, None, headers)
                reponse = urllib2.urlopen(request)
                print reponse
                print reponse.geturl()

            except:
                pass

            print sHosterUrl

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
