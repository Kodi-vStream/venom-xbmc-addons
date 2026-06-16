# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil, Unquote
from resources.lib.comaddon import siteManager, addon
import re


UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0'

# --- IDENTIFIANTS UNIQUES 
SITE_IDENTIFIER = 'cinestream'
SITE_NAME = 'CineStream'
SITE_DESC = 'Films en Streaming illimité'
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (URL_MAIN, 'load')
MOVIE_BOX = ('film-en-streaming/1', 'showMovies')
MOVIE_NEWS = ('films-ajoutes-recemment/1', 'showMovies')
MOVIE_VIEWS = ('films-populaires/1', 'showMovies')
MOVIE_ANNEES = ('', 'showMovieYears')
MOVIE_GENRES = ('films/', 'showGenres')

URL_SEARCH = ('search?q=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

DOC_DOCS = ('films/Documentaire/1', 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')  # Documentaires


def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30076), 'search-films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BOX[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BOX[1], addons.VSlang(30101), 'boxoffice.png', oOutputParameterHandler)
    
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], addons.VSlang(30134), 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], addons.VSlang(30102), 'popular.png', oOutputParameterHandler) 
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], addons.VSlang(30105), 'genres.png', oOutputParameterHandler)
        
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], addons.VSlang(30106), 'annees.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()    
    if sSearchText:
        oInputParameterHandler = cInputParameterHandler()
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        showMovies(siteUrl + sSearchText)
        oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()

    liste = ['Action', 'Animation', 'Aventure', 'Crime', 'Drame',
             'Documentaire', 'Familial', 'Fantastique', 'Guerre',
             'Horreur', 'Histoire', 'Romance', 'Science-Fiction',
             'Thriller', 'Western' ]
   
    for sTitle in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        sUrl = '%s%s/1' % (MOVIE_GENRES[0], sTitle)
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovieYears():
    import datetime
    oGui = cGui()
    current_year = int(datetime.datetime.now().year)

    for year in reversed(range(1920, current_year + 1)):
        oOutputParameterHandler = cOutputParameterHandler()
        sUrl = 'annee/%d/1' % year
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', str(year), 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    oUtil = cUtil()
    oParser = cParser()
    
    # 1. GESTION DES PARAMÈTRES
    if sSearch:
        sUrl = URL_MAIN + sSearch
        sSearchText = oUtil.CleanName(sSearch.split('=')[1])
    else:
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        sPage = oInputParameterHandler.getValue('sPage')        
        sUrl = URL_MAIN + siteUrl
        
        if sPage:
            sBaseUrl = siteUrl.rstrip('/').rsplit('/', 1)[0]
            sUrl = sBaseUrl + '/' + sPage                                                                

    # 2. REQUÊTE ET HEADERS
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Cookie', 'g=true')
    sHtmlContent = oRequestHandler.request()
    
    if not sHtmlContent:
        oGui.setEndOfDirectory()
        return

    # 3. PARSING
    sPattern = '<article.*?href="([^"]+)".*?_next/image\?url=([^&"]+).*?<span[^>]*>([^<]+)</span>.*?<span[^>]*>([^<]+)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    posterWidth = addon().getSetting('poster_tmdb')

    if aResult[0]:
        for aEntry in aResult[1]:
            sUrlMovie = aEntry[0]
            sRawThumb = aEntry[1]
            sRawTitle = aEntry[2]
            sYear = aEntry[3]
            
            sTitleReal = oUtil.unescape(sRawTitle.replace("Affiche du film ", "").split(" en streaming")[0]).strip()
            
            if sTitleReal.lower() in ['truefrench', 'vf', 'vostfr', 'hdlight', 'bluray']:
                continue
            
            if sSearch and not oUtil.CheckOccurence(sSearchText, sTitleReal):
                continue
            
            if sUrlMovie.startswith('/'):
                sUrlMovie = sUrlMovie

            # mettre la taille de l'affiche selon le parametre défini dans vStream/Affichage                
            sThumb = Unquote(sRawThumb)
            sThumb = re.sub('/w\d+/', '/%s/' % posterWidth, sThumb)
                
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrlMovie)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitleReal)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitleReal, sThumb, sThumb, '', oOutputParameterHandler)

    # 4. PAGINATION
    if not sSearch:
        if aResult[0]:
            sNextPattern = r'href="([^"]+)"><span[^>]*>Next</span><svg'
            match = re.search(sNextPattern, sHtmlContent, re.IGNORECASE)
                    
            if match is not None:
                sCurrentPage = sUrl.rstrip('/').split('/')[-1]
                if not sCurrentPage.isdigit():
                    sCurrentPage = '1'
                    
                sNextPage = str(int(sCurrentPage) + 1)
    
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sPage', sNextPage) 
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sNextPage, oOutputParameterHandler)
            
        oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear') or ''
    
    sGlobalLang = 'VF'
    sTmdbId = ''
    
    # Nettoyage du titre pour éviter les bugs Kodi
    sMovieTitle = sMovieTitle.replace('/', ' - ').replace(':', ' - ')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    if not sHtmlContent:
        return oGui.setEndOfDirectory()

    # Extraction du TMDB ID
    match_tmdb = re.search(r'tmdb(?:id)?\\*["\']?\s*:\s*["\']?(\d+)', sHtmlContent, re.IGNORECASE)
    if not match_tmdb:
        match_tmdb = re.search(r'data-tmdb(?:id)?=["\'](\d+)["\']', sHtmlContent, re.IGNORECASE)

    if match_tmdb:
        sTmdbId = match_tmdb.group(1)

    # Extraction de la langue
    match_lang = re.search(r'Version:\s*</span>\s*<span>([^<]+)</span>', sHtmlContent, re.IGNORECASE)
    if match_lang:
        sExtractedLang = match_lang.group(1).strip().upper()
        if 'VOSTFR' in sExtractedLang:
            sGlobalLang = 'VOSTFR'
        elif 'VF' in sExtractedLang:
            sGlobalLang = 'VF'

    # Extraction des boutons
    aButtons = re.findall(r'<button\s+id="([^"]+)"[^>]*playerbuttons', sHtmlContent)
    
    if sTmdbId and aButtons:
        for server_id, sButtonId in enumerate(aButtons):
            sPlayerUrl = URL_MAIN + 'player/%s/%s' % (sTmdbId, str(server_id))
            oRequest = cRequestHandler(sPlayerUrl)
            oRequest.addHeaderEntry('Referer', sUrl)
            sHtml = oRequest.request()

            if sHtml:
                aLinks = re.findall(r'src="([^"]+)"', sHtml)
                for link in aLinks:
                    if 'static' in link:
                        continue
                    link = link.replace('\/', '/')
                    if link.startswith('//'):
                        link = 'https:' + link
                        
                    oHoster = cHosterGui().checkHoster(link)
                    if oHoster:
                        sLang = 'VOSTFR' if 'vostfr' in sButtonId.lower() else sGlobalLang
                        sDisplayTitle = '%s (%s) (%s)' % (sMovieTitle, sYear, sLang)
                        oHoster.setDisplayName(sDisplayTitle)
                        oHoster.setFileName(sMovieTitle)
                        cHosterGui().showHoster(oGui, oHoster, link, sThumb)

    oGui.setEndOfDirectory()
