#-*- coding: utf-8 -*-
#Venom.
#
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil

import re,urllib2,urllib
import base64

SITE_IDENTIFIER = 'megastream'
SITE_NAME = 'Mega-stream'
SITE_DESC = 'Films, Séries, Animés HD'

URL_MAIN = 'http://mega-stream.fr/'

MOVIE_NEWS = (URL_MAIN +'accueil-films', 'showMovies')
MOVIE_MOVIE = (URL_MAIN +'accueil-films', 'showMovies')
MOVIE_HD = (URL_MAIN +'accueil-films', 'showMovies')
MOVIE_GENRES = (URL_MAIN +'accueil-films', 'showGenres')

SERIE_NEWS = (URL_MAIN +'accueil-series', 'showMovies')
SERIE_SERIES = (URL_MAIN +'accueil-series', 'showMovies')
SERIE_HD = (URL_MAIN +'accueil-series', 'showMovies')
#SERIE_GENRES = (URL_MAIN +'accueil-series', 'showGenres') #pas de genre serie actif

ANIM_NEWS = (URL_MAIN +'accueil-mangas', 'showMovies')
ANIM_ANIMS = (URL_MAIN +'accueil-mangas', 'showMovies')
ANIM_HD = (URL_MAIN +'accueil-mangas', 'showMovies')
ANIM_GENRES = (URL_MAIN + 'accueil-mangas', 'showGenres')

URL_SEARCH = ('', 'resultSearch')
URL_SEARCH_MOVIES = ('', 'resultSearch')
URL_SEARCH_SERIES = ('', 'resultSearch')
FUNCTION_SEARCH = 'resultSearch'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'fonctions/recherche.php')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    #oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'animes_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'top-films')
    oGui.addDir(SITE_IDENTIFIER, 'showTop', 'Top-100-Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'top-series')
    oGui.addDir(SITE_IDENTIFIER, 'showTop', 'Top-100-Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sSearchText = sSearchText
        resultSearch(sSearchText)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'film' in sUrl:
        code = 'accueil-films/'
    elif 'serie'in sUrl:
        code = 'accueil-series/'
    else:
        code = 'accueil-mangas/'

    liste = []
    liste.append( ['Action', URL_MAIN + code + 'action'] )
    liste.append( ['Animation', URL_MAIN + code + 'animation'] )
    liste.append( ['Arts Martiaux', URL_MAIN + code + 'arts-martiaux'] )
    liste.append( ['Aventure', URL_MAIN + code + 'aventure'] )
    liste.append( ['Biopic', URL_MAIN + code + 'biopic'] )
    liste.append( ['Comédie', URL_MAIN + code + 'comedie'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + code + 'comedie-dramatique'] )
    liste.append( ['Comédie Musicale', URL_MAIN + code + 'comedie-musicale'] )
    liste.append( ['Concert', URL_MAIN + code + 'concert'] )
    liste.append( ['Culture', URL_MAIN + code + 'culture'] )
    liste.append( ['Dessin', URL_MAIN + code + 'dessin'] )
    liste.append( ['Divers', URL_MAIN + code + 'divers'] )
    liste.append( ['Divertissement', URL_MAIN + code + 'divertissement'] )
    liste.append( ['Documentaire', URL_MAIN + code + 'documentaire'] )
    liste.append( ['Drame', URL_MAIN + code + 'drame'] )
    liste.append( ['Epouvante-horreur', URL_MAIN + code + 'epouvante-horreur'] )
    liste.append( ['Erotique', URL_MAIN + code + 'erotique'] )
    liste.append( ['Espionnage', URL_MAIN + code + 'espionnage'] )
    liste.append( ['Famille', URL_MAIN + code + 'famille'] )
    liste.append( ['Fantastique', URL_MAIN + code + 'fantastique'] )
    liste.append( ['Films de Noël', URL_MAIN + code + 'films-de-noel'] )
    liste.append( ['Guerre', URL_MAIN + code + 'guerre'] )
    liste.append( ['Historique', URL_MAIN + code + 'historique'] )
    liste.append( ['Horreur', URL_MAIN + code + 'horreur'] )
    liste.append( ['Humour', URL_MAIN + code + 'humour'] )
    liste.append( ['Judiciaire', URL_MAIN + code + 'judiciaire'] )
    liste.append( ['Médical', URL_MAIN + code + 'medical'] )
    liste.append( ['Musical', URL_MAIN + code + 'musical'] )
    liste.append( ['Mystère', URL_MAIN + code + 'mystere'] )
    liste.append( ['Mythe', URL_MAIN + code + 'mythe'] )
    liste.append( ['Péplum', URL_MAIN + code + 'peplum'] )
    liste.append( ['Policier', URL_MAIN + code + 'policier'] )
    liste.append( ['Romance', URL_MAIN + code + 'romance'] )
    liste.append( ['Science Fiction', URL_MAIN + code + 'science-fiction'] )
    liste.append( ['Sentai', URL_MAIN + code + 'sentai'] )
    liste.append( ['Soap', URL_MAIN + code + 'soap'] )
    liste.append( ['Spectacles', URL_MAIN + code + 'spectacles'] )
    liste.append( ['Sport', URL_MAIN + code + 'sport'] )
    liste.append( ['Sport Event', URL_MAIN + code + 'sport-event'] )
    liste.append( ['TV', URL_MAIN + code + 'tv'] )
    liste.append( ['Thriller', URL_MAIN + code + 'thriller'] )
    liste.append( ['Tragédie', URL_MAIN + code + 'trageie'] )
    liste.append( ['Télé-réalité', URL_MAIN + code + 'tele-realite'] )
    liste.append( ['Western', URL_MAIN + code + 'western'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def resultSearch(sSearch):

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    sUrl = "http://mega-stream.fr/recherche"

    post_data = {'search' : sSearch }

    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    headers = {'User-Agent': UA ,
               'Host' : 'mega-stream.fr'}

    req = urllib2.Request(sUrl , urllib.urlencode(post_data), headers)

    response = urllib2.urlopen(req)
    sHtmlContent = response.read()
    response.close()

    sPattern = '<div class="movie-img img-box">\s*<img.+?src="([^"]+)".+?<a href="([^"]+)"[^<>]+>.+?-([^<>]+)<\/a>.+?<span[^<>]+>([^<>]+)<\/span>'

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

            sQual = ""
            if aEntry[3]:
                sQual = ' [' + aEntry[3] + ']'
            siteUrl = aEntry[1]
            sThumbnail = aEntry[0]
            sTitle = aEntry[2]

            sDisplayTitle = cUtil().DecoTitle(sTitle + sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            if '-serie' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'series.png', sThumbnail, '', oOutputParameterHandler)
            elif '-mangas-' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'animes.png', sThumbnail, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

def showMovies(sSearch = ''):
    oGui = cGui()

    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    sPattern = '<img[^<>]+src="([^"]+)" class="tubeposter".+?<span[^<>]+>([^<>]+)*<\/span>.+?<a class="movie-title" href="([^"]+)"[^<>]+>([^<>]+)<.+?<b>Description :<\/b>([^><]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sQual = ''
            #sAnnee = aEntry[3]
            sThumbnail = aEntry[0]
            if aEntry[1]:
                sQual = ' [' + aEntry[1] + ']'
            siteUrl = aEntry[2]
            sTitle = aEntry[3]
            if '-films' in sUrl:
                sTitle = sTitle.split('-')[1]
            sCom = aEntry[4]

            sDisplayTitle = cUtil().DecoTitle(sTitle + sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            if '-mangas' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'animes.png', sThumbnail, sCom, oOutputParameterHandler)
            elif '-serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'series.png', sThumbnail, sCom, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumbnail, sCom, oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):

    sPattern = '<span class="pnext"><a href="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="(#saison[0-9]+)">(.+?)<\/a>|href="([^"]+/[0-9]+)">(.+?)<\/a><\/li>'
    aResult = re.findall(sPattern,sHtmlContent)

    if (aResult):
        total = len(aResult)
        dialog = cConfig().createDialog(SITE_NAME)
        sSaison = ''
        for aEntry in aResult:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
                sSaison = aEntry[1]
                oGui.addText(SITE_IDENTIFIER, '[COLOR olive]' + sSaison + '[/COLOR]')

            else:
                sTitle = sMovieTitle + ' ' + sSaison + ' ' + aEntry[3]
                sUrl = aEntry[2]
                sDisplayTitle = cUtil().DecoTitle(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #on recupere d'abord les liens
    sPattern = '<div id="(lecteur_[0-9]+)">.+?data-tnetnoc-crs="([^"]+)"'
    tablink = re.findall(sPattern,sHtmlContent, re.DOTALL)

    #le classique
    sPattern = '<a href="#(lecteur_[0-9]+)".+?title="([^"]+)"\/> *([^<>]+)<\/a'
    aResult = re.findall(sPattern,sHtmlContent, re.DOTALL)

    if (aResult):
        total = len(aResult)
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sQual = aEntry[2]
            sLang = aEntry[1]
            sDisplayTitle =  sMovieTitle + ' [' + sQual + '/' + sLang + ']'
            sDisplayTitle = cUtil().DecoTitle(sDisplayTitle)

            url = ''
            for i,j in tablink:
                if i == aEntry[0]:
                    url = base64.b64decode(j)[::-1]

            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showTop():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<li class="tops-item"><a href="([^"]+)".+?<img src="([^"]+)" alt="([^"]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sThumbnail = aEntry[1]
            sUrl = aEntry[0]
            sTitle = aEntry[2]

            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            if '-films-' in sUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'series.png', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
