#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#17/12/18
#return False
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'cinemavf'
SITE_NAME = 'CinemaVF'
SITE_DESC = 'Films, Séries & Mangas en streaming.'

URL_MAIN = 'http://filmstreamin1.com/'

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN , 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'film-streaming', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')

SERIE_NEWS = (URL_MAIN + 'serie/', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'serie/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')

ANIM_NEWS = (URL_MAIN + 'mangas/', 'showMovies')
ANIM_ANIMS = (URL_MAIN + 'mangas/', 'showMovies')
ANIM_GENRES = (True, 'showMangaGenres')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animés (Genres)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showMovieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'category/action'] )
    liste.append( ['Animation', URL_MAIN + 'category/animation'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'category/arts-martiaux'] )
    liste.append( ['Aventure', URL_MAIN + 'category/aventure'] )
    liste.append( ['Biopic', URL_MAIN + 'category/biopic'] )
    liste.append( ['Classique', URL_MAIN + 'category/classique'] )
    liste.append( ['Comédie', URL_MAIN + 'category/comedie'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'category/comedie-dramatique'] )
    liste.append( ['Concert', URL_MAIN + 'category/concert'] )
    liste.append( ['Divers', URL_MAIN + 'category/divers'] )
    liste.append( ['Documentaire', URL_MAIN + 'category/documentaire-exclusive'] )
    liste.append( ['Dramatique', URL_MAIN + 'category/dramatique'] )
    liste.append( ['Drame', URL_MAIN + 'category/drame'] )
    liste.append( ['Emissions TV', URL_MAIN + 'category/emissions-tv'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'category/epouvante-horreur'] )
    liste.append( ['Erotique', URL_MAIN + 'category/erotique'] )
    liste.append( ['Espionnage', URL_MAIN + 'category/espionnage'] )
    liste.append( ['Expérimental', URL_MAIN + 'category/experimental'] )
    liste.append( ['Famille', URL_MAIN + 'category/famille'] )
    liste.append( ['Fantastique', URL_MAIN + 'category/fantastique'] )
    liste.append( ['Guerre', URL_MAIN + 'category/guerre'] )
    liste.append( ['Historique', URL_MAIN + 'category/historique'] )
    liste.append( ['Horreur', URL_MAIN + 'category/horreur'] )
    liste.append( ['Humour', URL_MAIN + 'category/humour'] )
    liste.append( ['Judiciaire', URL_MAIN + 'category/judiciaire'] )
    liste.append( ['Manga', URL_MAIN + 'category/manga'] )
    liste.append( ['Musical', URL_MAIN + 'category/musical'] )
    liste.append( ['Opéra', URL_MAIN + 'category/opera'] )
    liste.append( ['Péplum', URL_MAIN + 'category/peplum'] )
    liste.append( ['Policier', URL_MAIN + 'category/policier'] )
    liste.append( ['Romance', URL_MAIN + 'category/romance'] )
    liste.append( ['Science Fiction', URL_MAIN + 'category/science-fiction'] )
    liste.append( ['Show', URL_MAIN + 'category/show'] )
    liste.append( ['Spectacle', URL_MAIN + 'category/spectacle'] )
    liste.append( ['Sport', URL_MAIN + 'category/sport'] )
    liste.append( ['Téléréalité', URL_MAIN + 'category/telerealite'] )
    liste.append( ['Thriller', URL_MAIN + 'category/thriller'] )
    liste.append( ['Vieux films', URL_MAIN + 'category/vieux-films-2'] )
    liste.append( ['Walt Disney', URL_MAIN + 'category/walt-disney'] )
    liste.append( ['Western', URL_MAIN + 'category/western'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'serie/category/action'] )
    liste.append( ['Animation', URL_MAIN + 'serie/category/animation'] )
    liste.append( ['Aventure', URL_MAIN + 'serie/category/aventure'] )
    liste.append( ['Comédie', URL_MAIN + 'serie/category/comedie'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'serie/category/comedie-dramatique'] )
    liste.append( ['Documentaire', URL_MAIN + 'serie/category/documentaire'] )
    liste.append( ['Drame', URL_MAIN + 'serie/category/drame'] )
    liste.append( ['Emissions TV', URL_MAIN + 'serie/category/emissions-tv'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'serie/category/epouvante-horreur'] )
    liste.append( ['Erotique', URL_MAIN + 'serie/category/erotique'] )
    liste.append( ['Espionnage', URL_MAIN + 'serie/category/espionnage'] )
    liste.append( ['Famille', URL_MAIN + 'serie/category/famille'] )
    liste.append( ['Fantastique', URL_MAIN + 'serie/category/fantastique'] )
    liste.append( ['Guerre', URL_MAIN + 'serie/category/guerre'] )
    liste.append( ['Historique', URL_MAIN + 'serie/category/historique'] )
    liste.append( ['Judiciaire', URL_MAIN + 'serie/category/judiciaire'] )
    liste.append( ['Médical', URL_MAIN + 'serie/category/medical'] )
    liste.append( ['Musical', URL_MAIN + 'serie/category/musical'] )
    liste.append( ['Péplum', URL_MAIN + 'serie/category/peplum'] )
    liste.append( ['Policier', URL_MAIN + 'serie/category/policier'] )
    liste.append( ['Romance', URL_MAIN + 'serie/category/romance'] )
    liste.append( ['Science Fiction', URL_MAIN + 'serie/category/science-fiction'] )
    liste.append( ['Thriller', URL_MAIN + 'serie/category/thriller'] )
    liste.append( ['Western', URL_MAIN + 'serie/category/western'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMangaGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'mangas/category/action'] )
    liste.append( ['Amitié', URL_MAIN + 'mangas/category/amitie'] )
    liste.append( ['Amour', URL_MAIN + 'mangas/category/amour-love'] )
    liste.append( ['Animation', URL_MAIN + 'mangas/category/animation'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'mangas/category/arts-martiaux'] )
    liste.append( ['Aventure', URL_MAIN + 'mangas/category/aventure'] )
    liste.append( ['Comédie', URL_MAIN + 'mangas/category/comedie'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'mangas/category/comedie-drama'] )
    liste.append( ['Dramatique', URL_MAIN + 'mangas/category/dramatique'] )
    liste.append( ['Drame', URL_MAIN + 'mangas/category/drame'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'mangas/category/epouvante-horreur'] )
    liste.append( ['Erotique', URL_MAIN + 'mangas/category/erotique'] )
    liste.append( ['Famille', URL_MAIN + 'mangas/category/famille'] )
    liste.append( ['Fantastique', URL_MAIN + 'mangas/category/fantastique'] )
    liste.append( ['Guerre', URL_MAIN + 'mangas/category/guerre'] )
    liste.append( ['Historique', URL_MAIN + 'mangas/category/historique'] )
    liste.append( ['Horreur', URL_MAIN + 'mangas/category/horreur'] )
    liste.append( ['Humour', URL_MAIN + 'mangas/category/humour'] )
    liste.append( ['Musical', URL_MAIN + 'mangas/category/musical'] )
    liste.append( ['Non classé', URL_MAIN + 'mangas/category/non-classe'] )
    liste.append( ['Policier', URL_MAIN + 'mangas/category/policier'] )
    liste.append( ['Romance', URL_MAIN + 'mangas/category/romance'] )
    liste.append( ['Science Fiction', URL_MAIN + 'mangas/category/science-fiction'] )
    liste.append( ['Show', URL_MAIN + 'mangas/category/show'] )
    liste.append( ['Sport', URL_MAIN + 'mangas/category/sport'] )
    liste.append( ['Thriller', URL_MAIN + 'mangas/category/thriller'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<a title=".+?href="(.+?)">.+?<div class=".+?">.+?<img src="(.+?)" alt="(.+?)" />.+?</ul>.+?<div class="ExcerptContent">(.+?)</div>'

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
            sTitle = aEntry[2].decode("unicode_escape").encode("latin-1")
            sDesc = aEntry[3]

            #tris search
            if sSearch and total > 3:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), sTitle) == 0:
                    continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb )

            if '/serie' in sUrl or '/mangas' in sUrl or '/serie' in sUrl2 or '/mangas' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSaisons', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a class="nextpostslink" rel="next" href="(.+?)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def ShowSaisons():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #probleme de redirection non finalisée sur leur site
    sUrl = oRequestHandler.getRealUrl()

    sPattern = '<div class="season">.+?<h3>(.+?)</h3>|<a class="num_episode" href="(.+?)"><span>(.+?)<\/span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

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
                sUrl2 = aEntry[1]
                sTitle = aEntry[2].replace(' streaming', '')

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb )
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #probleme de redirection non finalisée sur leur site
    sUrl = oRequestHandler.getRealUrl()

    #récupération des Synopsis
    sDesc = ''
    try:
        sPattern = '<p>(.+?)<\/p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
            sDesc = sDesc.replace('\\', '').replace('&#8230;', '...').replace('<br />', ' ').replace('<span>', '').replace('</span>', '')
    except:
        pass

    #filtre pour ne pas afficher les langues en telechargement
    sStart = '<div class="player-container">'
    sEnd = '<div class="iframe-vid-container">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<span>(vf|vo)</span>|<a onclick=".+?">.+?</i>\s*([^<>]+)\s*<\/a>\s*<input name="levideo" value="([^"]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0].upper() + '[/COLOR]')
            else:
                sHost = aEntry[1].capitalize()
                sHost = re.sub('\.\w+', '', sHost)
                #on filtre les hosters hs
                if 'Auroravid' in sHost:
                    continue
                sPost = aEntry[2]
                sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sPost', sPost)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sPost = oInputParameterHandler.getValue('sPost')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addParameters('levideo', sPost)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = sHtmlContent.replace('src="https://www.youtube.com/embed/', '')

    oParser = cParser()
    sPattern = '<iframe.+?src=["\']([^"\']+)["\']'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            if 'vid.php' in sHosterUrl:
                oRequestHandler = cRequestHandler(sHosterUrl)
                tmp = oRequestHandler.request()
                sHosterUrl = oRequestHandler.getRealUrl()

            if sHosterUrl.startswith('/'):
                sHosterUrl = 'http:' + sHosterUrl
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
