#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler

from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'fullstream'
SITE_NAME = 'Full Stream'
SITE_DESC = 'Films, Séries et Mangas Gratuit en streaming sur Full stream'

URL_MAIN = 'http://serie.full-stream.cc/'

#definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle sera affichee.
#LA RECHERCHE GLOBAL N'UTILE PAS showSearch MAIS DIRECTEMENT LA FONCTION INSCRITE DANS LA VARIABLE URL_SEARCH_*
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
#recherche global films
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
#recherche global serie, manga
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
#recherche global divers
URL_SEARCH_MISC = (URL_MAIN + '?s=', 'showMovies')
#
FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'film-streaming', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'film-streaming', 'showMovies')
MOVIE_HD = (URL_MAIN + 'url', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')
MOVIE_VF = (URL_MAIN + 'langues/vf', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'langues/vostfr', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'derniers-series-a-jours.html', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'serie-streaming', 'showMovies')
SERIE_LIST = (URL_MAIN + 'liste-des-series.html', 'AlphaSearch')
SERIE_VFS = (URL_MAIN + 'serie-streaming/series-vf', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'serie-streaming/series-vostfr', 'showMovies')

ANIM_ANIMS = (URL_MAIN + 'mangas', 'showMovies')
ANIM_NEWS = (URL_MAIN + 'mangas', 'showMovies')
ANIM_VFS = (URL_MAIN + 'mangas/mangas-fr', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'mangas/mangas-vostfr', 'showMovies')

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
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF[1], 'Films (VF)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_LIST[1], 'Séries (Liste) ', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF) ', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animés (VF) ', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

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

    for i in range(0, 27) :

        if (i < 1):
            sLetter = '[0-9]'
        else:
            sLetter = chr(64 + i)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sLetter', sLetter)
        oGui.addDir(SITE_IDENTIFIER, 'AlphaDisplay', '[COLOR teal] Lettre [COLOR red]' + sLetter + '[/COLOR][/COLOR]', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def AlphaDisplay():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sLetter = oInputParameterHandler.getValue('sLetter')

    oRequestHandler = cRequestHandler(SERIE_LIST[0])
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+?)" >(' + sLetter + '[^<]+?)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sTitle = aEntry[1]


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)

            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'series.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'film-streaming/action/'] )
    liste.append( ['Animation', URL_MAIN + 'film-streaming/animation/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'film-streaming/arts-martiaux/'] )
    liste.append( ['Aventure', URL_MAIN + 'film-streaming/aventure/'] )
    liste.append( ['Biopic', URL_MAIN + 'film-streaming/biopic/'] )
    liste.append( ['Comédie', URL_MAIN + 'film-streaming/comedie/'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'film-streaming/comedie-dramatique/'] )
    liste.append( ['Comédie Musicale', URL_MAIN + 'film-streaming/comedie-musicale/'] )
    liste.append( ['Documentaire', URL_MAIN + 'film-streaming/documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'film-streaming/drame/'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'film-streaming/epouvante-horreur/'] )
    liste.append( ['Erotique', URL_MAIN + 'film-streaming/erotique'] )
    liste.append( ['Espionnage', URL_MAIN + 'film-streaming/espionnage/'] )
    liste.append( ['Famille', URL_MAIN + 'film-streaming/famille/'] )
    liste.append( ['Famille', URL_MAIN + 'famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'film-streaming/fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'film-streaming/guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'film-streaming/historique/'] )
    liste.append( ['Musical', URL_MAIN + 'film-streaming/musical/'] )
    liste.append( ['Policier', URL_MAIN + 'film-streaming/policier/'] )
    liste.append( ['Péplum', URL_MAIN + 'film-streaming/peplum/'] )
    liste.append( ['Romance', URL_MAIN + 'film-streaming/romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'film-streaming/science-fiction/'] )
    liste.append( ['Spectacle', URL_MAIN + 'film-streaming/spectacle/'] )
    liste.append( ['Thriller', URL_MAIN + 'film-streaming/thriller/'] )
    liste.append( ['Western', URL_MAIN + 'film-streaming/western/'] )
    liste.append( ['Divers', URL_MAIN + 'film-streaming/divers/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
    oGui = cGui()

    for i in reversed (xrange(1942, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'annee/' + Year)
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

    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>', '')

    sPattern = 'class="shortstory cf">.+?<a href="([^"]+)".+?class="positive-rate">([^<]+)<.+?class="xquality">([^<]+)<.+?<img src="([^"]+)".+?alt="(.+?)"'

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

            sUrl2 = aEntry[0]
            sLang = aEntry[1]
            sQual = aEntry[2]
            sThumb = aEntry[3]
            sTitle = aEntry[4]
            sDesc = ''

            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '-saison-' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'a class="nextpostslink" rel="next" href="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

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
        sPattern = 'Synopsis</strong> :([^<]+)<'
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

            sTitle = sMovieTitle + aEntry[1].replace('Ep', 'episode').replace('EP', 'episode ')
            sUrl2 = aEntry[0]

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
    sPattern = '<a href="([^"]+)".+?class="link_a".+?<td>.+?</td><td>([^<]+)</td>'

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]
            #on affiche à nouveau la langue pour ceux qui proposent vf et vostfr
            sLang = aEntry[1]

            sDisplayTitle = ('%s (%s)') % (sMovieTitle, sLang)

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
