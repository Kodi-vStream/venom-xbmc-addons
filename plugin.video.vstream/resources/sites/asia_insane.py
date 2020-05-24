#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, VSlog
from resources.lib.multihost import cMultiup
import re

SITE_IDENTIFIER = 'asia_insane'
SITE_NAME = 'Asia Insane'
SITE_DESC = 'Regarder Films et Séries Asiatique en Streaming gratuit'

URL_MAIN = 'https://www.asia-insane.biz/'

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + 'wp-admin/admin-ajax.php', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_MOVIE = (True, 'load')
MOVIE_NEWS = (URL_MAIN + 'films-asiatiques-affichage-grid/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (True, 'showYears')
MOVIE_LIST = (URL_MAIN + 'films-asiatiques-vostfr-affichage-alphanumerique/', 'showAlpha')
DRAMA_DRAMAS = (URL_MAIN + 'liste-des-dramas-vostfr-ddl/', 'showMovies')

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DRAMA_DRAMAS[0])
    oGui.addDir(SITE_IDENTIFIER, DRAMA_DRAMAS[1], 'Séries (Dramas)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIST[1], 'Films (Ordre alphabétique)', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + 'amy_genre/'

    liste = []
    liste.append(['Action', sUrl + 'action/'])
    liste.append(['Adulte', sUrl + 'adulte/'])
    liste.append(['Arts Martiaux', sUrl + 'arts-martiaux/'])
    liste.append(['Aventure', sUrl + 'aventure/'])
    liste.append(['Comédie', sUrl + 'comedie/'])
    liste.append(['Comédie érotique', sUrl + 'comedie-erotique/'])
    liste.append(['Contenu adulte', sUrl + 'contenu-adulte/'])
    liste.append(['Crime', sUrl + 'crime/'])
    liste.append(['Drame', sUrl + 'drame/'])
    liste.append(['Ecole', sUrl + 'ecole/'])
    liste.append(['Erotique', sUrl + 'erotique/'])
    liste.append(['Expérimental', sUrl + 'experimental/'])
    liste.append(['Famille', sUrl + 'famille'])
    liste.append(['Fantastique', sUrl + 'fantastique/'])
    liste.append(['Gastronomie', sUrl + 'gastronomie/'])
    liste.append(['Gay', sUrl + 'gay/'])
    liste.append(['Guerre', sUrl + 'guerre/'])
    liste.append(['Histoire vraie', sUrl + 'histoire-vraie/'])
    liste.append(['Historique', sUrl + 'historique/'])
    liste.append(['Horreur', sUrl + 'horreur/'])
    liste.append(['Maladie', sUrl + 'maladie/'])
    liste.append(['Médecine', sUrl + 'medecine/'])
    liste.append(['Mélodrame', sUrl + 'melodrame/'])
    liste.append(['Musical', sUrl + 'musical/'])
    liste.append(['Mystère', sUrl + 'mystere/'])
    liste.append(['Policier', sUrl + 'policier/'])
    liste.append(['Psycologique', sUrl + 'psycologique/'])
    liste.append(['Romance', sUrl + 'romance/'])
    liste.append(['Science Fiction', sUrl + 'science-fiction/'])
    liste.append(['Sport', sUrl + 'sport'])
    liste.append(['Suspense', sUrl + 'suspense'])
    liste.append(['Travail', sUrl + 'travail/'])
    liste.append(['Tranche de vie', sUrl + 'tranche-de-vie/'])
    liste.append(['Thriller', sUrl + 'thriller/'])

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showYears():
    oGui = cGui()

    from itertools import chain
    generator = chain([1966, 1972, 1987, 1988, 1990, 1991, 1992], range(1994, 2021))

    for i in reversed(list(generator)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'date/' + Year + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAlpha():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'front">.+?src="(http[^"]+).+?field-title"><a href="([^"]+)">([^.]+)d{2}.+?.+?field-desc"><p>([^<]+)'
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

            sThumb = aEntry[0]
            sUrl = aEntry[1]
            sTitle = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/dramas/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            sPattern = 'class="next page-numbers".+?page/(\d{1,3})'
            aResult = oParser.parse(sHtmlContent, sPattern)
            page = ''
            if (aResult[0] == True):
                page = aResult[1][0]

            oGui.addNext(SITE_IDENTIFIER, 'showAlpha', '[COLOR teal]Page ' + page + ' >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    bGlobal_Search = False

    if sSearch:
        if URL_SEARCH[0] in sSearch:
            bGlobal_Search = True
            sSearch=sSearch.replace(URL_SEARCH[0], '')

        sPattern = '<a class=\'asp_res_image_url\' href=\'([^>]+)\'.+?url\("([^"]+)"\).+?\'>([^.]+)d{2}.+?<span.+?<div class="asp_res_text">([^<]+)<'

        oRequestHandler = cRequestHandler(URL_SEARCH[0])
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequestHandler.addHeaderEntry('Accept-Encoding','gzip, deflate')
        oRequestHandler.addHeaderEntry('Referer', "https://www.asia-insane.biz/recherche-avancee-asia-insane/")
        oRequestHandler.addHeaderEntry('Content-Type','application/x-www-form-urlencoded')

        oRequestHandler.addParameters('action',"ajaxsearchpro_search")
        oRequestHandler.addParameters('asid',"1")
        oRequestHandler.addParameters('aspp',sSearch)
        oRequestHandler.addParameters('asp_inst_id', "1_1")
        oRequestHandler.addParameters('options',"current_page_id=413&qtranslate_lang=0&asp_gen%5B%5D=title&customset%5B%5D=amy_movie&customset%5B%5D=amy_tvshow&termset%5Bamy_director%5D%5B%5D=-1&termset%5Bamy_actor%5D%5B%5D=-1")
        sHtmlContent = oRequestHandler.request()

    elif '/amy_genre/' in sUrl or '/date/' in sUrl:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'entry-item clearfix">.+?src="(http[^"]+).+?entry-title"><a href="([^"]+)">([^.]+)d{2}.+?'

    else:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        sPattern = 'class="attachment.+?noscript.+?src="([^"]+).+?class="amy-movie-field-title".+?href="([^"]+)">([^.]+)d{2}.+?class="amy-movie-field-desc"><p>([^<]+).+?Date.+?\/date\/([^\/]+)'
        
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

            if sSearch:
                sUrl2 = aEntry[0]
                sThumb = aEntry[1]
                sTitle = aEntry[2]
                sDesc = aEntry[3]

                sDisplayTitle = ('%s') % (sTitle)

            elif '/amy_genre/' in sUrl or '/date/' in sUrl:
                sUrl2 = aEntry[1]
                sThumb = aEntry[0]
                sTitle = aEntry[2]
                sDesc = ""

                sDisplayTitle = ('%s') % (sTitle)

            else:
                sUrl2 = aEntry[1]
                sThumb = aEntry[0]
                sTitle = aEntry[2]
                sDesc = aEntry[3]
                sYear = aEntry[4]

                sDisplayTitle = ('%s ([COLOR coral]%s[/COLOR])') % (sTitle, sYear)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/dramas/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            number = re.search('/page/([0-9]+)/', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + number + ' >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="next page-numbers" href="([^"]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    page = ''
    if (aResult[0] == True):
        VSlog(aResult)
        return aResult[1][0]

    return False

def ShowSerieSaisonEpisodes():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sStart = '<div class="entry-content e-content" itemprop="description articleBody">'
    sEnd = '<div class="entry-comment">'
    sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)

    sPattern = '<a href="([^"]+)">([^"]+)</a>'
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

            sTitle = sMovieTitle + "E" + aEntry[1]
            sUrl2 = aEntry[0]

            if not sUrl2.startswith('http'):
                sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('HostUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sUrl2 = oInputParameterHandler.getValue('HostUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    if '/dramas/' in sUrl:
        if 'multiup' in sUrl2:
            aResult = cMultiup().GetUrls(sUrl2)

            if (aResult):
                for aEntry in aResult:
                    sHosterUrl = aEntry

                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                        oHoster.setDisplayName(sMovieTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
        
        else:
            sHosterUrl = sUrl2

            oHoster = cHosterGui().checkHoster(sUrl2)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        sStart = '<pre>'
        sEnd = '</pre>'
        sHtmlContent = oParser.abParse(sHtmlContent, sStart, sEnd)
        sPattern = '>.+?href="([^"]+)">'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:

                sTitle = sMovieTitle
                sHosterUrl = aEntry

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
