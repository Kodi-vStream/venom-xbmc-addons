#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'filmstreamvk_com'
SITE_NAME = 'Filmstreamvk'
SITE_DESC = 'Films, Séries & Mangas en Streaming'

URL_MAIN = 'https://www.filmstreamvf.com/'

MOVIE_MOVIE = (URL_MAIN + 'film-streaming-vf', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'film-streaming-vf?sort=date', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'film-streaming-vf?sort=views', 'showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'film-streaming-vf?sort=comments', 'showMovies')
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
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_COMMENTS[1], 'Films (Les plus commentés)', 'comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'news.png', oOutputParameterHandler)

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
    liste.append( ['Action', URL_MAIN + 'category/action'] )
    liste.append( ['Animation', URL_MAIN + 'category/animation'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'category/arts-martiaux'] )
    liste.append( ['Aventure', URL_MAIN + 'category/aventure'] )
    liste.append( ['Bande annonce', URL_MAIN + 'category/bande-annonce'] )
    liste.append( ['Biographie', URL_MAIN + 'category/biography'] )
    liste.append( ['Biopic', URL_MAIN + 'category/biopic'] )
    liste.append( ['Comédie', URL_MAIN + 'category/comedie'] )
    liste.append( ['Comédie dramatique', URL_MAIN + 'category/comedie-dramatique'] )
    liste.append( ['Comédie musicale', URL_MAIN + 'category/comedie-musicale'] )
    liste.append( ['Concert', URL_MAIN + 'category/concert'] )
    liste.append( ['Courts métrages', URL_MAIN + 'category/courts-metrages'] )
    liste.append( ['Crime', URL_MAIN + 'category/crime'] )
    liste.append( ['Divers', URL_MAIN + 'category/divers'] )
    liste.append( ['Documentaire', URL_MAIN + 'category/documentaire'] )
    liste.append( ['Drame', URL_MAIN + 'category/drame'] )
    liste.append( ['Enigme', URL_MAIN + 'category/enigme'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'category/epouvante-horreur'] )
    liste.append( ['Espionnage', URL_MAIN + 'category/espionnage'] )
    liste.append( ['Exclues', URL_MAIN + 'category/exclues'] )
    liste.append( ['Famille', URL_MAIN + 'category/famille'] )
    liste.append( ['Fantastique', URL_MAIN + 'category/fantastique'] )
    liste.append( ['Fantasy', URL_MAIN + 'category/fantasy'] )
    liste.append( ['Film récompensé', URL_MAIN + 'category/film-recompense'] )
    liste.append( ['Guerre', URL_MAIN + 'category/guerre'] )
    liste.append( ['Histoire vraie', URL_MAIN + 'category/histoire-vraie'] )
    liste.append( ['Historique', URL_MAIN + 'category/historique'] )
    liste.append( ['Horreur', URL_MAIN + 'category/horreur'] )
    liste.append( ['Judiciaire', URL_MAIN + 'category/judiciaire'] )
    liste.append( ['Musical', URL_MAIN + 'category/musical'] )
    liste.append( ['Mystery', URL_MAIN + 'category/mystery'] )
    liste.append( ['Non classé', URL_MAIN + 'category/non-classe'] )
    liste.append( ['Péplum', URL_MAIN + 'category/peplum'] )
    liste.append( ['Policier', URL_MAIN + 'category/policier'] )
    liste.append( ['Romance', URL_MAIN + 'category/romance'] )
    liste.append( ['Science-Fiction', URL_MAIN + 'category/science-fiction'] )
    liste.append( ['Série', URL_MAIN + 'category/serie'] )
    liste.append( ['Spectacle', URL_MAIN + 'category/spectacle'] )
    liste.append( ['Sport', URL_MAIN + 'category/sport'] )
    liste.append( ['Sport event', URL_MAIN + 'category/sport-event'] )
    liste.append( ['Survival', URL_MAIN + 'category/survival'] )
    liste.append( ['Thriller', URL_MAIN + 'category/thriller'] )
    liste.append( ['Top films', URL_MAIN + 'category/exclues/top-films'] )
    liste.append( ['Walt Disney', URL_MAIN + 'category/walt-disney'] )
    liste.append( ['War', URL_MAIN + 'category/war'] )
    liste.append( ['Western', URL_MAIN + 'category/western'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="movie-poster">.+?<img src="([^"]+)".+?<a href="([^"]+)" title="([^"]+)"'
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

            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0], ''), aEntry[2]) == 0:
                    continue

            sThumb = aEntry[0]
            sUrl = aEntry[1]
            sTitle = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/series/' in sUrl or '/serie/' in sUrl or '/manga/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^"]+)" *>Suivan.+?<\/a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #recuperation du synopsis
    sDesc = ''
    try:
        sPattern = '<div class="excerpt.+?">(.+?)<\/div>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
            sDesc = sDesc.replace('<br />', '').replace('&#8217;', '\'').replace('&#8230;', '...')
    except:
        pass

    #recuperation du hoster de base
    ListeUrl = []
    sPattern = '<div class="keremiya_part"> <span>(.+?)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        ListeUrl = [(sUrl, aResult[1][0])]

    #recuperation des suivants
    sPattern = '<a href="([^"]+)" class="post-page-numbers".+?<span>(.+?)<\/span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    ListeUrl = ListeUrl + aResult[1]

    #si quedale on tente le tout pour le tout
    if (aResult[0] == False):
        showHosters()

    if (aResult[0] == True):
        for aEntry in ListeUrl:

            sHost = aEntry[1].capitalize()
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHost)
            if 'pisode' in aEntry[1]:
                sTitle = sMovieTitle
            sUrl = aEntry[0]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showEpisode():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #recuperation du synopsis
    sDesc = ''
    try:
        sPattern = '<div class="konuozet">.+?</b>(.+?)<br>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
    except:
        pass

    sPattern = '<td class="liste_episode" width="10%">([^<]+)<\/td>|<a href="([^<>"]+?)" title="" class="num_episode">([0-9]+)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                sLang = aEntry[0].decode("utf8")
                sLang = cUtil().unescape(sLang).encode("utf8")
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + sLang + '[/COLOR]')
            else:
                #ce ne sont pas les mêmes tirets ne pas supprimer
                sMovieTitle = sMovieTitle.replace(' – Saison', ' Saison').replace(' - Saison', ' Saison')
                sTitle = sMovieTitle + ' episode ' + aEntry[2]
                sUrl = aEntry[1]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()


    sPattern = '<input type="hidden" name="ep" id="ep" value="([^"]+)".+?name="type" id="type" value="([^"]+)".+?name="np" id="np" value="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        ep = aResult[1][0][0]
        type = aResult[1][0][1]
        np = aResult[1][0][2]
        ref = sUrl.rsplit('/', 1)[0]

        pdata = 'action=electeur&lien_referer=' + ref + '&ep=' + ep + '&type=' + type + '&np=' + np
        

        oRequest = cRequestHandler(URL_MAIN + 'wp-admin/admin-ajax.php')
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0')
        oRequest.addHeaderEntry('Referer', sUrl)
        oRequest.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequest.addParametersLine(pdata)

        sHtmlContent = oRequest.request()

        if 'serie' in sUrl or 'manga' in sUrl:
            sPattern = "onclick=\"lecteur_.+?\(.+?'([^']+)',.+?\);"
        else:
            sPattern = '<iframe.+?src=[\'|"](.+?)[\'|"]'

        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:

                sHosterUrl = aEntry

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
