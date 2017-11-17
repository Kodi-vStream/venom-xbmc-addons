#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import util
from resources.lib.config import cConfig
import re,xbmcgui,unicodedata

#clone de dpstreaming.tv

SITE_IDENTIFIER = 'streamingk_com'
SITE_NAME = 'StreamingK'
SITE_DESC = 'Films, Séries & Mangas en streaming. Tout les meilleurs streaming en illimité.'

URL_MAIN = 'http://streamingk.com/'

MOVIE_NEWS = (URL_MAIN + 'category/films/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'category/films/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'category/films/vostfr-films/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = (URL_MAIN + 'category/series-tv/', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'category/series-tv/', 'showMovies')
SERIE_VIEWS = (URL_MAIN + 'most-viewed/', 'showMovies')
SERIE_COMMENTS = (URL_MAIN + 'most-popular/', 'showMovies')
SERIE_NOTES = (URL_MAIN + 'most-like/', 'showMovies')
SERIE_VFS = (URL_MAIN + 'category/series-tv/series-streaming-vf/', 'showMovies')
SERIE_VOSTFR = (URL_MAIN + 'series-tv/series-streaming-vostfr/', 'showMovies')

ANIM_ANIMS = (URL_MAIN + 'category/mangas/', 'showMovies')
ANIM_NEWS = (URL_MAIN + 'category/mangas/', 'showMovies')

REPLAYTV_REPLAYTV = (URL_MAIN + 'category/emissions-tv/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Les plus Vues)', 'series_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_COMMENTS[1], 'Séries (Les plus Commentées)', 'series_comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NOTES[1], 'Séries (Les mieux Notés)', 'series_notes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries (Liste)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'series_vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFR[1], 'Séries (VOSTFR)', 'series_vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_REPLAYTV[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_REPLAYTV[1], 'Emissions TV', 'replay.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMoviesSearch():
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
    liste.append( ['Action', URL_MAIN + 'category/films/action/'] )
    liste.append( ['Animation', URL_MAIN + 'category/films/animation/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'category/films/arts-martiaux/'] )
    liste.append( ['Aventure', URL_MAIN + 'category/films/biopic/'] )
    liste.append( ['Biopic', URL_MAIN + 'category/films/animation/'] )
    liste.append( ['Comédie', URL_MAIN + 'category/films/comedie/'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'category/films/comedie-dramatique/'] )
    liste.append( ['Documentaire', URL_MAIN + 'category/documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'category/films/drame/'] )
    liste.append( ['Espionnage', URL_MAIN + 'category/films/espionnage/'] )
    liste.append( ['Famille', URL_MAIN + 'category/films/famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'category/films/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'category/films/guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'category/films/historique/'] )
    liste.append( ['Horreur', URL_MAIN + 'category/films/horreur/'] )
    liste.append( ['Musical', URL_MAIN + 'category/films/musical/'] )
    liste.append( ['Policier', URL_MAIN + 'category/films/policier/'] )
    liste.append( ['Romance', URL_MAIN + 'category/films/romance/'] )
    liste.append( ['Science-Fiction', URL_MAIN + 'category/films/science-fiction/'] )
    liste.append( ['Spectacle', URL_MAIN + 'category/films/spectacle/'] )
    liste.append( ['Thriller', URL_MAIN + 'category/films/thriller/'] )
    liste.append( ['Western', URL_MAIN + 'category/films/western/'] )
    liste.append( ['VOSTFR', URL_MAIN + 'category/films/vostfr-films/'] )
    liste.append( ['BLURAY 1080p/720p', URL_MAIN + 'category/films/bluray-1080p-720p/'] )
    liste.append( ['BLURAY 3D', URL_MAIN + 'category/films/bluray-3d/'] )
    liste.append( ['Emissions TV', URL_MAIN + 'category/emissions-tv/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films_genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showList():
    oGui = cGui()

    liste = []
    liste.append( ['0-9', URL_MAIN + 'category/series-tv/0-9/'] )
    liste.append( ['A-B-C', URL_MAIN + 'category/series-tv/a-b-c/'] )
    liste.append( ['D-E-F', URL_MAIN + 'category/series-tv/d-e-f/'] )
    liste.append( ['G-H-I', URL_MAIN + 'category/series-tv/g-h-i/'] )
    liste.append( ['J-K-L', URL_MAIN + 'category/series-tv/j-k-l/'] )
    liste.append( ['M-N-O', URL_MAIN + 'category/series-tv/m-n-o/'] )
    liste.append( ['P-Q-R', URL_MAIN + 'category/series-tv/p-q-r/'] )
    liste.append( ['S-T-U', URL_MAIN + 'category/series-tv/s-t-u/'] )
    liste.append( ['V-W-X-Y-Z', URL_MAIN + 'category/series-tv/v-w-x-y-z/'] )

    for sTitle,sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettres [COLOR coral]' + sTitle + '[/COLOR]', 'listes.png', oOutputParameterHandler)

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
    #Meilleure resolution sThumb
    sHtmlContent = sHtmlContent.replace('119x125', '125x160')

    #Magouille pour virer les 3 ligne en trop en cas de recherche
    if sSearch:
        sHtmlContent = sHtmlContent.replace('quelle-est-votre-serie-preferee', '<>')
        sHtmlContent = sHtmlContent.replace('top-series-du-moment', '<>')
        sHtmlContent = sHtmlContent.replace('listes-des-series-annulees-et-renouvelees', '<>')

    oParser = cParser()
    sPattern = '<div class="moviefilm"> *<a href=".+?"> *<img src="([^<>"]+)".+?\/><\/a><div class="movief"><a href="([^<]+)">([^<]+)<\/a><\/div>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
		oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        #plante la recherche global dialog = util.createDialog(SITE_NAME)
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if util.cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), aEntry[2]) == 0:
                    continue

            sThumb = str(aEntry[0])
            sUrl = str(aEntry[1])
            sTitle = str(aEntry[2])
            sTitle = sTitle.replace(' [Streaming]', '')
            sTitle = sTitle.replace(' [Telecharger]', '').replace(' [Telechargement]', '')
            sTitle = sTitle.replace(' [Complète]', '').replace(' [Complete]', '')
            sTitle = sTitle.replace('&#8217;', '\'')

            sDisplayTitle = util.cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '-filmographie-streaming' in aEntry[1]:
                pass
            elif 'quelle-est-votre-serie-preferee' in aEntry[1]:
                pass
            elif 'series' in sUrl or re.match('.+?saison [0-9]+', sTitle, re.IGNORECASE):
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<span class=\'current\'>.+?</span><a class="page larger".+?href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showSeries(sLoop = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.decode('utf-8', "replace")
    sHtmlContent = unicodedata.normalize('NFD', sHtmlContent).encode('ascii', 'ignore').decode("unicode_escape")#vire accent et '\'
    sHtmlContent = sHtmlContent.encode('utf-8')#On remet en utf-8

    oParser = cParser()

    sPattern = '<span style="color: #33cccc;[^<>"]*">(?:<(?:strong|b)>)*((?:Stream|Telec)[^<>]+)|>(Episode[^<]{2,12})<(?!\/a>)(.{0,10}a href="http.+?)(?:<.p|<br|<.div)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    #astuce en cas d'episode unique
    if (aResult[0] == False) and (sLoop == False):
        #oGui.setEndOfDirectory()
        showHosters(True)
        return;

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = util.createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            util.updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            #langue
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')
            #episode
            else:
                sUrl = str(aEntry[2])
                sTitle = sMovieTitle + ' ' + str(aEntry[1])
                sDisplayTitle = util.cUtil().DecoTitle(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addMisc(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        util.finishDialog(dialog)

    oGui.setEndOfDirectory()

def showHosters(sLoop = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/', '')
    sHtmlContent = sHtmlContent.replace("src='https://ad.a-ads.com", '')

    oParser = cParser()

    #1 er version
    sPattern = '<iframe[^<>]+?src=[\'|"](http.+?)[\'|"]'
    aResult1 = re.findall( sPattern, sHtmlContent)

    #seconde version
    sPattern = '<a class="large.+?href="(.+?)" target="vid">'
    aResult2 = re.findall( sPattern, sHtmlContent)

    #3eme version
    sPattern = '<a class="large.+?href="([^<>"]+?)" target="(?:_blank|vid)"'
    aResult3 = re.findall( sPattern, sHtmlContent)

    #fusion des resultats
    aResult = []
    aResult = list(set( aResult1 + aResult2 + aResult3 ))


    #Si il y a rien a afficher c'est peut etre une serie
    if (len(aResult) == 0) and (sLoop == False):
        #oGui.setEndOfDirectory()
        showSeries(True)
        return

    if (len(aResult) > 0):
        for aEntry in aResult:

            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                sDisplayTitle = util.cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()

    sPattern = 'href="([^<]+)" target="_blank"[^<>]*>.+?<\/a>'
    aResult = oParser.parse(sUrl, sPattern)

    #affichage
    if (aResult[0] == True):
        index = 1
        for aEntry in aResult[1]:

            sTitle = sMovieTitle
            sTitle = sTitle + ' (' + str(index) + ') '
            index = index + 1

            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                sDisplayTitle = util.cUtil().DecoTitle(sTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
