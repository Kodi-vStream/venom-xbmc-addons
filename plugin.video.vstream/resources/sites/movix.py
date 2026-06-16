# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib import util
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import siteManager, addon
import re

SITE_IDENTIFIER = 'movix'
SITE_NAME = 'Movix'
SITE_DESC = 'La plateforme gratuite de films et séries pour tous'
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

#URL_MAIN = 'https://movix.news/'

MOVIE_MOVIE = (URL_MAIN, 'showMenuMovies')
MOVIE_NEWS = ('trending?type=movie&sort=release_date', 'showMovies')
MOVIE_VIEWS = ('trending?type=movie', 'showMovies')
MOVIE_ANNEES = ('movies?type=movie&release=%d', 'showMovieYears')
MOVIE_PAYS = ('movies?type=movie&country=%d', 'showMovieCountry')
MOVIE_GENRES = ('movies?type=movie&genre=%s', 'showGenres')

SERIE_SERIES = (URL_MAIN, 'showMenuSeries')
SERIE_NEWS = ('tv-shows?type=tv&sort=created_at', 'showSeries')
SERIE_VIEWS = ('trending?type=tv', 'showSeries')
SERIE_GENRES = ('tv-shows?type=tv&genre=%s', 'showSeriesGenres')

REPLAYTV_REPLAYTV = ('tv-shows?type=tv&genre=27', 'showSeries')
REPLAYTV_NEWS = ('tv-shows?type=tv&genre=27', 'showSeries')

URL_SEARCH = ('search/', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showSeries')
URL_SEARCH_ANIMS = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_REPLAY = (URL_SEARCH[0], 'showSeries')
URL_SEARCH_MISC = (URL_SEARCH_MOVIES[0], 'showMovies')  # Documentaires


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)    
#    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
   
def showMenuMovies():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearchMovies', 'Rechercher', 'search-films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], addons.VSlang(30134), 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], addons.VSlang(30102), 'popular.png', oOutputParameterHandler)

    # ne fonctionne pas sur le site
    # oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    # oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], addons.VSlang(30106), 'annees.png', oOutputParameterHandler)    
   
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], addons.VSlang(30105), 'genres.png', oOutputParameterHandler)
        
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_PAYS[1], 'Pays', 'host.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearchSeries', 'Rechercher', 'search-series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], addons.VSlang(30134), 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], addons.VSlang(30102), 'popular.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], addons.VSlang(30105), 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearchMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSearchText = oGui.showKeyBoard()
    if sSearchText:   
        sUrl = URL_SEARCH[0] + sSearchText.replace('%20', ' ')
        showMovies(sUrl)
        oGui.setEndOfDirectory()
    return

def showSearchSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSearchText = oGui.showKeyBoard()
    if sSearchText:   
        sUrl = URL_SEARCH[0] + sSearchText.replace('%20', ' ')
        showSeries(sUrl)
        oGui.setEndOfDirectory()
    return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append(['Action', 1])
    liste.append(['Aventure', 35])
    liste.append(['Animation', 3])
    liste.append(['Comédie', 22])  
    liste.append(['Crime', 5])
    liste.append(['Documentaire', 25])
    liste.append(['Drame', 20])
    liste.append(['Guerre', 33])
    liste.append(['Histoire', 40])
    liste.append(['Horreur', 32])
    liste.append(['Famille', 24])
    liste.append(['Fantastique', 36])
    liste.append(['Musique', 38])
    liste.append(['Mystère', 21])
    liste.append(['Romance', 14])
    liste.append(['Science Fiction', 15])
    liste.append(['Téléfilm', 34])
    liste.append(['Thriller', 17])
    liste.append(['Western', 19])
   
    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sGenre in liste:
        oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0] % sGenre)
        oGui.addGenre(SITE_IDENTIFIER, 'showMovies', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeriesGenres():
    oGui = cGui()
 
    liste = []
    liste.append(['Action & Adventure', 26])
    liste.append(['Animation', 3])
    liste.append(['Comédie', 22])  
    liste.append(['Crime', 5])
    liste.append(['Documentaire', 25])
    liste.append(['Drame', 20])
    liste.append(['Enfants', 30])
    liste.append(['Famille', 24])
    liste.append(['Fantastique', 23])
    liste.append(['Guerre', 28])
    liste.append(['Mystère', 21])
    liste.append(['Reality', 27 ])
    liste.append(['Soap', 31])
    liste.append(['Western', 19])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sGenre in liste:
        oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0] % sGenre)
        oGui.addGenre(SITE_IDENTIFIER, 'showSeries', sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory() 

def showMovieCountry():
    oGui = cGui()
 
    liste = []
    liste.append(['Allemagne', 86])
    liste.append(['Argentine', 10])
    liste.append(['Autriche', 14])  
    liste.append(['Belgique', 22])
    liste.append(['Brésil', 31])
    liste.append(['Canada', 41])
    liste.append(['Chine', 48])
    liste.append(['Corée du Sud', 217])
    liste.append(['Danemark', 62])
    liste.append(['Espagne', 218])
    liste.append(['États-Unis', 250])
    liste.append(['France', 78])
    liste.append(['Italie', 112])
    liste.append(['Japan', 114])
    liste.append(['Mexique', 146])
    liste.append(['Norvège', 173])
    liste.append(['Pays-Bas', 160])
    liste.append(['Pologne', 187])
    liste.append(['Romanie', 191])
    liste.append(['Royaume-Uni', 249])
    liste.append(['Russie', 192])
    liste.append(['Suède', 224])   
    liste.append(['Thaïlande', 231])
    liste.append(['Turquie', 238])

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, iGenre in liste:
        oOutputParameterHandler.addParameter('siteUrl', MOVIE_PAYS[0] % iGenre)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'host.png', oOutputParameterHandler)

    oGui.setEndOfDirectory() 

def showMovieYears():
    import datetime
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oOutputParameterHandler = cOutputParameterHandler()
    for year in reversed(range(1945, int(datetime.datetime.now().year) + 1)):
        oOutputParameterHandler.addParameter('siteUrl', sUrl % year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', str(year), 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        oUtil = cUtil()
        sSearchText = '/'.join(sSearch.split('/')[-1:])
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        siteUrl = sUrl = oInputParameterHandler.getValue('siteUrl')
        sPage = oInputParameterHandler.getValue('sPage')
        if sPage:
            if 'movie' in siteUrl:
                sUrl += '&page=' + sPage
            else:
                sUrl += '?page=' + sPage

    oRequestHandler = cRequestHandler(URL_MAIN + sUrl)
    sHtmlContent = oRequestHandler.request()
#    sPattern = '<div class="relative group overflow-hidden">.+?<a href="([^"]+)">.+?data-src="([^"]+)".+?<span>([^<]+)</span>.+?>([^<]+)</h3>'
    sPattern = 'overflow-hidden">.+?href="([^"]+)".+?data-src="([^"]+)" alt="([^"]+)".+?<span>([^<]+)<\/span> *<!--\[if ENDBLOCK\]><!\[endif\]--> *<\/div>.+?ml-auto">([^<>]+)'

    aResult = oParser.parse(sHtmlContent, sPattern)            
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()

        for aEntry in aResult[1]:
            sType = aEntry[4]
            if not 'Movie' in sType:
                continue
            sUrl2 = aEntry[0]
            sThumb =  aEntry[1]
            sTitle = aEntry[2]
            sYear = aEntry[3]

            # Filtre de recherche
            if sSearch and not oUtil.CheckOccurence(sSearchText, sTitle):
                continue

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, 'films.png', sThumb, '', oOutputParameterHandler)

    if not sSearch:      
        if sPage:
            sPage = str(int(sPage)+1)
        else:
            sPage = '2'

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sPage', sPage)
        oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + sPage, oOutputParameterHandler)
        oGui.setEndOfDirectory()

        
def showSeries(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        oUtil = cUtil()
        sSearchText = '/'.join(sSearch.split('/')[-1:])
        sSearchText = oUtil.CleanName(sSearchText)        
        sUrl = sSearch

    else:
        oInputParameterHandler = cInputParameterHandler()
        siteUrl = sUrl = oInputParameterHandler.getValue('siteUrl')
        sPage = oInputParameterHandler.getValue('sPage')
        if sPage:
            if '?' in siteUrl:
                sUrl += '&page=' + sPage
            else:
                sUrl += '?page=' + sPage
                
    oRequestHandler = cRequestHandler(URL_MAIN + sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'overflow-hidden">.+?href="([^"]+)".+?data-src="([^"]+)" alt="([^"]+)".+?<span>([^<]+)<\/span> *<!--\[if ENDBLOCK\]><!\[endif\]--> *<\/div>.+?ml-auto">([^<>]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()

        for aEntry in aResult[1]:
            sThumb = aEntry[1]
            sType = aEntry[4]
            if not 'TV' in sType:
                continue
            
            sTitle = aEntry[2]
            
            # Filtre de recherche
            if sSearch and not oUtil.CheckOccurence(sSearchText, sTitle):
                continue
            
            sUrl2 = aEntry[0]
            sYear = aEntry[3]
            sTitle = re.sub('\(' + sYear + '\)', '', sTitle)            
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear) 
            oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sTitle, '', sThumb, '', oOutputParameterHandler)            
            
    if not sSearch:
        if sPage:
            sPage = str(int(sPage)+1)
        else:
            sPage = '2'
  
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sPage', sPage)
        oGui.addNext(SITE_IDENTIFIER, 'showSeries', 'Page ' + sPage, oOutputParameterHandler)
        oGui.setEndOfDirectory()
                     
def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = URL_MAIN + oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
#    sPattern = '<p class=".+?">([^<]+)</p>'
    sPattern = 'wire:click="updateSeason\(\'(\d+)\'\).*?">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
#        for aEntry in aResult[1][::-1]:
        for aEntry in sorted(aResult[1], key=lambda saison: saison[0]):
            sSaison = aEntry[1].strip()
            sTitle = sDisplayTitle = sMovieTitle + ' ' + sSaison
            if 'saison' not in sSaison and 'season' not in sSaison:
                hasNum = re.search('(\d+)', sSaison)
                if hasNum:
                    numSaison = hasNum.group(1)
                else:
                    numSaison = 1
                sTitle = sDisplayTitle = '%s Saison %s' % (sMovieTitle, numSaison)
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addSeason(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sYear = oInputParameterHandler.getValue('sYear')    
        
    sUrl = ('%sepisode/%s/%s-1') % (URL_MAIN, sUrl.split('/')[-1], sMovieTitle.split(' ')[-1])
    # url title
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'href="([^"]+)" *class="flex transition.+?font-medium">([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl = aEntry[0]
            sTitle = sMovieTitle + ' ' + aEntry[1].replace('#', '')
            #sDesc = aEntry[0].strip() 
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle.split(' ')[0])
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oParser = cParser()
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = 'version":"([^"]+)".+?link":"([^"]+)"'

    sHtmlContent = oParser.abParse(sHtmlContent, 'currentVersionVideos() {', '];')
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        links = {}
        for sLang, sHosterUrl in aResult[1]:
            link = links.get(sLang, [])
            link.append(sHosterUrl)
            links[sLang] = link

        for sLang in sorted(links):
            hosters = links.get(sLang)
            for sHosterUrl in hosters:
                sDisplayTitle = '%s  (%s)' % (sMovieTitle,  sLang)
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if oHoster:
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
