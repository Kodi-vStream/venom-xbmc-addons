#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'filmstreamvk_com'
SITE_NAME = 'Filmstreamvk'
SITE_DESC = 'Films, Séries & Mangas en Streaming'

URL_MAIN = 'http://filmstreamvk.co/'

MOVIE_MOVIE = (URL_MAIN, 'showMovies')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'les-plus-vues-films', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = (URL_MAIN + 'serie', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'serie', 'showMovies')

ANIM_ANIMS = (URL_MAIN + 'manga', 'showMovies')
ANIM_NEWS = (URL_MAIN + 'manga', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les Plus Vus)', 'films_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)

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
    liste.append( ['Action',URL_MAIN + 'category/action'] )
    liste.append( ['Animation',URL_MAIN + 'category/animation'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'category/arts-martiaux'] )
    liste.append( ['Aventure',URL_MAIN + 'category/aventure'] )
    liste.append( ['Bande annonce',URL_MAIN + 'category/bande-annonce'] )
    liste.append( ['Biographie',URL_MAIN + 'category/biography'] )
    liste.append( ['Biopic',URL_MAIN + 'category/biopic'] )
    liste.append( ['Capes et épées',URL_MAIN + 'category/capes-et-epees'] )
    liste.append( ['Comédie',URL_MAIN + 'category/comedie'] )
    liste.append( ['Comédie dramatique',URL_MAIN + 'category/comedie-dramatique'] )
    liste.append( ['Comédie musicale',URL_MAIN + 'category/comedie-musicale'] )
    liste.append( ['Concert',URL_MAIN + 'category/concert'] )
    liste.append( ['Crime',URL_MAIN + 'category/crime'] )
    liste.append( ['Days (TV)',URL_MAIN + 'category/days-tv'] )
    liste.append( ['Divers',URL_MAIN + 'category/divers'] )
    liste.append( ['Documentaire',URL_MAIN + 'category/documentaire'] )
    liste.append( ['Drame',URL_MAIN + 'category/drame'] )
    liste.append( ['Enigme',URL_MAIN + 'category/enigme'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'category/epouvante-horreur'] )
    liste.append( ['Espionnage',URL_MAIN + 'category/espionnage'] )
    liste.append( ['Exclues',URL_MAIN + 'category/exclues'] )
    liste.append( ['Famille',URL_MAIN + 'category/famille'] )
    liste.append( ['Fantastique',URL_MAIN + 'category/fantastique'] )
    liste.append( ['Fantasy',URL_MAIN + 'category/fantasy'] )
    liste.append( ['Film récompensé',URL_MAIN + 'category/film-recompense'] )
    liste.append( ['Golden Time',URL_MAIN + 'category/golden-time'] )
    liste.append( ['Guerre',URL_MAIN + 'category/guerre'] )
    liste.append( ['Gugure! Kokkuri-san',URL_MAIN + 'category/gugure-kokkuri-san'] )
    liste.append( ['Histoire vraie',URL_MAIN + 'category/histoire-vraie'] )
    liste.append( ['Historique',URL_MAIN + 'category/historique'] )
    liste.append( ['Horreur',URL_MAIN + 'category/horreur'] )
    liste.append( ['Judiciaire',URL_MAIN + 'category/judiciaire'] )
    liste.append( ['Love Live!',URL_MAIN + 'category/love-live'] )
    liste.append( ['Musical',URL_MAIN + 'category/musical'] )
    liste.append( ['Mystery',URL_MAIN + 'category/mystery'] )
    liste.append( ['Naruto Shippuden Kai',URL_MAIN + 'category/naruto-shippuden-kai'] )
    liste.append( ['Non classé',URL_MAIN + 'category/non-classe'] )
    liste.append( ['Péplum',URL_MAIN + 'category/peplum'] )
    liste.append( ['Pixar',URL_MAIN + 'category/pixar'] )
    liste.append( ['Policier',URL_MAIN + 'category/policier'] )
    liste.append( ['Romance',URL_MAIN + 'category/romance'] )
    liste.append( ['Science-Fiction',URL_MAIN + 'category/science-fiction'] )
    liste.append( ['Série',URL_MAIN + 'category/serie'] )
    liste.append( ['Souryo to Majiwaru Shikiyoku no Yoru ni',URL_MAIN + 'category/souryo-to-majiwaru-shikiyoku-no-yoru-ni'] )
    liste.append( ['Spectacle',URL_MAIN + 'category/spectacle'] )
    liste.append( ['Sport',URL_MAIN + 'category/sport'] )
    liste.append( ['Sport event',URL_MAIN + 'category/sport-event'] )
    liste.append( ['Survival',URL_MAIN + 'category/survival'] )
    liste.append( ['Thriller',URL_MAIN + 'category/thriller'] )
    liste.append( ['Tokyo Ravens',URL_MAIN + 'category/tokyo-ravens'] )
    liste.append( ['Top films',URL_MAIN + 'category/exclues/top-films'] )
    liste.append( ['Walt Disney',URL_MAIN + 'category/walt-disney'] )
    liste.append( ['Western',URL_MAIN + 'category/western'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()

    if sSearch:
        sUrl = sSearch
        sUrl = sUrl.replace('%20', '+')

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="moviefilm">.+?<img src="([^<"]+)".+?<a href="([^<]+)">([^<]+)<\/a>'

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

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0],''),aEntry[2]) == 0:
                    continue

            sThumb = aEntry[0]
            sUrl = aEntry[1]
            sTitle = aEntry[2].replace('&#8217;', '\'').replace('&#8230;', '...')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/serie/' in sUrl or '/manga/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="nextpostslink" rel="next" href="([^"]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #cConfig().log(sUrl)

    oParser = cParser()
    ListeUrl = []
    #recuperation du hoster de base
    sPattern = '<div class="keremiya_part"> <span>(.+?)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        ListeUrl = [(sUrl,aResult[1][0])]

    #Recuperation des suivants
    sPattern = '<a href="([^<]+)"><span>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    ListeUrl = ListeUrl + aResult[1]

    #si quedale on tente le tout pour le tout
    if (aResult[0] == False):
        showHosters()

    if (aResult[0] == True):
        total = len(ListeUrl)
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in ListeUrl:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle + ' (' + aEntry[1] + ')'
            if 'pisode' in aEntry[1]:
                sTitle = sMovieTitle
            sUrl = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<td class="liste_episode" width="10%">(.+?)<\/td>|<a href="([^<>"]+?)" title="" class="num_episode">([0-9]+)<\/a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
                sLang = aEntry[0].decode("utf8")
                sLang = cUtil().unescape(sLang).encode("utf8")
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + sLang + '[/COLOR]')
            else:
                sTitle = sMovieTitle + ' episode ' + aEntry[2]
                sUrl = aEntry[1]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showHostersSerie', sTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHostersSerie():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/', '')

    #deux pattern pour supprimer les doublons hoster dans les series
    if '/manga/' in sUrl:
        sPattern = 'onclick="lecteur_.+?\([0-9]+,\'((?:http|\/)[^<>]+?)\'\);" class="bb">'
    else:
        sPattern = 'class="bb".+?onclick="lecteur_.+?\([0-9]+,\'((?:http|\/)[^<>]+?)\'\);">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #si quedale on tente le tout pour le tout
    if (aResult[0] == False):
        showHosters()

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = str(aEntry)
            if sHosterUrl.startswith('/'):
                sHosterUrl = 'http:' + sHosterUrl

            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHosters():

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/', '')

    sPattern = '<iframe.+?src=[\'|"](.+?)[\'|"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = str(aEntry)

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
