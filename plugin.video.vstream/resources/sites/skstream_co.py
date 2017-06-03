#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig
import re,xbmcgui,urllib2

SITE_IDENTIFIER = 'skstream_co'
SITE_NAME = 'Skstream'
SITE_DESC = 'Films Series Mangas'

URL_MAIN = 'http://www.skstream.co/'

MOVIE_NEWS = (URL_MAIN + 'films', 'showMovies')
MOVIE_MOVIE = ('http://films', 'showMenuMovies')
MOVIE_GENRES = (MOVIE_NEWS[0] , 'showGenres')
MOVIE_ANNEES = (MOVIE_NEWS[0] + '-produit-en-' , 'showMovies')
MOVIE_QLT = (MOVIE_NEWS[0] , 'showQlt')
MOVIE_PAYS = ('http://films', 'showPays')

SERIE_NEWS = (URL_MAIN + 'series', 'showMovies')
SERIE_SERIES = ('http://series', 'showMenuSeries')
SERIE_GENRES = (SERIE_NEWS[0], 'showGenres')
SERIE_ANNEES = (SERIE_NEWS[0] + '-sortie-en-', 'showMovies')
SERIE_QLT = (SERIE_NEWS[0], 'showQlt')
SERIE_PAYS = ('http://series', 'showPays')

ANIM_NEWS = (URL_MAIN + 'mangas' , 'showMovies')
ANIM_ANIMS = ('http://mangas', 'showMenuMangas')
ANIM_GENRES = (ANIM_NEWS[0], 'showGenres')
ANIM_ANNEES = (ANIM_NEWS[0]+ '-sortie-en-', 'showMovies')
ANIM_QLT = (ANIM_NEWS[0], 'showQlt')
ANIM_PAYS = ('http://mangas', 'showPays')

URL_SEARCH = (URL_MAIN + 'recherche?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films (Menu)', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries (Menu)', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Mangas (Menu)', 'animes.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def showMenuMovies():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_QLT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_QLT[1], 'Films (Qualités)', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'annees.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_PAYS[1], 'Films (Par Pays)', 'lang.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_QLT[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_QLT[1], 'Séries (Qualités)', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par Années)', 'annees.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_PAYS[1], 'Séries (Par Pays)', 'lang.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def showMenuMangas():
    oGui = cGui()
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animes (Derniers ajouts)', 'animes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_QLT[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_QLT[1], 'Animes (Qualités)', 'animes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animes (Genres)', 'animes_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANNEES[1], 'Animes (Par Années)', 'annees.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_PAYS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_PAYS[1], 'Animes (Par Pays)', 'lang.png', oOutputParameterHandler)

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
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
	
    liste = []
    liste.append( ['Action',sUrl + '-du-genre-action'] )
    liste.append( ['Animation',sUrl + '-du-genre-animation'] )
    liste.append( ['Arts-Martiaux',sUrl + '-du-genre-arts-martiaux'] )
    liste.append( ['Aventure',sUrl + '-du-genre-aventure'] )
    liste.append( ['Biopic',sUrl + '-du-genre-biopic'] )
    liste.append( ['Comédie',sUrl + '-du-genre-comedie'] )
    liste.append( ['Comédie Dramatique',sUrl + '-du-genre-comedie-dramatique'] )
    liste.append( ['Comédie Musicale',sUrl + '-du-genre-comedie-musicale'] )
    liste.append( ['Drame',sUrl + '-du-genre-drame'] )
    liste.append( ['Epouvante Horreur',sUrl + '-du-genre-epouvante-horreur'] ) 
    liste.append( ['Espionnage',sUrl + '-du-genre-espionnage'] )
    liste.append( ['Famille',sUrl + '-du-genre-famille'] )
    liste.append( ['Fantastique',sUrl + '-du-genre-fantastique'] )  
    liste.append( ['Guerre',sUrl + '-du-genre-guerre'] )
    liste.append( ['Historique',sUrl + '-du-genre-historique'] )
    liste.append( ['Judiciaire',sUrl + '-du-genre-judiciaire'] )
    liste.append( ['Médical',sUrl + '-du-genre-medical'] )
    liste.append( ['Policier',sUrl + '-du-genre-policier'] )
    liste.append( ['Péplum',sUrl + '-du-genre-peplum'] )
    liste.append( ['Romance',sUrl + '-du-genre-romance'] )
    liste.append( ['Science-Fiction',sUrl + '-du-genre-science-fiction'] )
    liste.append( ['Thriller',sUrl + '-du-genre-thriller'] )
    liste.append( ['Western',sUrl + '-du-genre-western'] )
	
    for sTitle,sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
        
def showPays():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    liste = []
    liste.append( ['Americain',sUrl + '-de-nationalite-americain'] )
    liste.append( ['Allemand',sUrl + '-de-nationalite-allemand'] )
    liste.append( ['Britanique',sUrl + '-de-nationalite-britannique'] )
    liste.append( ['Canadien',sUrl + '-de-nationalite-canadien'] )
    liste.append( ['Espagnol',sUrl + '-de-nationalite-espagnol'] )
    liste.append( ['Francais',sUrl + '-de-nationalite-francais'] )
    liste.append( ['Italien',sUrl + '-de-nationalite-italien'] )
    liste.append( ['Japonnais',sUrl + '-de-nationalite-japonais'] )
    liste.append( ['Norvegien',sUrl + '-de-nationalite-norvegien'] )

    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'lang.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()


def showQlt():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
	
    liste = []
    
    liste.append( ['1080p',sUrl + '-qualites-1080p'] )
    liste.append( ['720p',sUrl + '-qualites-720p'] )
    liste.append( ['HDrip',sUrl + '-qualites-hdrip'] )
    liste.append( ['HDTV',sUrl + '-qualites-hd-tv'] )
    liste.append( ['BDrip',sUrl + '-qualites-bd-rip'] )
    liste.append( ['BRrip',sUrl + '-qualites-brrip'] )
    liste.append( ['DVDrip',sUrl + '-qualites-dvd-rip'] )
    liste.append( ['WEBrip',sUrl + '-qualites-web-rip'] )
    liste.append( ['DVDscr',sUrl + '-qualites-dvdscr'] )

    for sTitle,sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()

def showNumBoard(sDefaultNum=''):
    dialog = xbmcgui.Dialog()
    numboard = dialog.numeric(0, 'Entrer une année ex: 2005', sDefaultNum)
    if numboard != None:
       return numboard
    return False
    
def selectAnnees(sUrl):
    oGui = cGui()
    newNum = showNumBoard()
    fsUrl = sUrl + newNum
    return fsUrl
    
def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oParser = cParser()

    if 'films-produit-en' in sUrl:
        sUrl = selectAnnees(sUrl)
    elif 'series-sortie-en' in sUrl:
        sUrl = selectAnnees(sUrl)
    elif 'mangas-sortie-en' in sUrl:
        sUrl = selectAnnees(sUrl)
    else:
        sUrl = sUrl
    
    if sSearch:
        sUrl = sSearch
        
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="unfilm" *HREF="([^"]+)">.+?title="(.+?)".+?src="([^"]+)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent,sPattern)
    if (aResult[0] == True):     
        for aEntry in aResult[1]:
            sUrl = URL_MAIN[:-1] + aEntry[0]
            sTitle = aEntry[1]
            sThumb = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)

            if ('/series/' in sUrl or '/mangas/' in sUrl):
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sTitle,'', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)
        
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)
    else:
        oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + 'Aucun résultat' + '[/COLOR]')
        
    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent): 
    oParser = cParser()
    sPattern = '<li> *<a href="([^"]+)">Suivant *<i'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN[:-1] + aResult[1][0]

    return False

def showEpisode():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    
    sSyn = '' 
    sPattern = '<div class="more-info">.+?<p>(.+?)<\/p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sSyn = cUtil().removeHtmlTags(aResult[1][0])
 
    sPattern = '<div class="panel-heading"><h4><i class="fa fa-television" id="(.+?)">|<a class="episode-block" href="([^"]+)" title="(.+?)">'

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            if aEntry[0]:
                sSaison = aEntry[0]
                oGui.addText(SITE_IDENTIFIER, '[COLOR crimson]' + sSaison + '[/COLOR]')
            else: 
                sUrl = URL_MAIN[:-1] + aEntry[1]
                sTitle = aEntry[2].replace('En Streaming','').replace(',','').replace('Regarder','').replace('en streaming','')
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumbnail, sSyn, oOutputParameterHandler)
                
        cConfig().finishDialog(dialog)
        
    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()

    sSyn = '' 
    sPattern = '<div class="more-info">.+?<p>(.+?)<\/p>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sSyn = aResult[1][0]
        
    sPattern = '<tr class="changeplayer.+?".+?data-embedlien="([^"]+)".+?<i class="server player-.+?"><\/i>(.+?)<.+?<span class="badge">(.+?)<\/span>.+?<td>(.+?)<\/td>'
    aResult = oParser.parse(sHtmlContent, sPattern)   

    if (aResult[0] == True):
        for aEntry in aResult[1]: 
            sHost = aEntry[1]
            if 'Skstream' in sHost:
                continue
            sLang = aEntry[2]
            sQual = aEntry[3]
            sUrl2 = aEntry[0]
            
            sTitle = '[%s] %s [%s] [COLOR coral]%s[/COLOR]' %(sLang,sMovieTitle,sQual,sHost)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('refUrl', sUrl)
            oOutputParameterHandler.addParameter('sUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, sSyn, oOutputParameterHandler)             

    oGui.setEndOfDirectory()  

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    refUrl = oInputParameterHandler.getValue('refUrl')
    sUrl = oInputParameterHandler.getValue('sUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'

    headers = {'User-Agent': UA ,
                'Referer': refUrl ,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

    request = urllib2.Request(sUrl,None,headers)
    reponse = urllib2.urlopen(request)
    vUrl = reponse.geturl()
    reponse.close()

    if vUrl:
        sHosterUrl = vUrl 
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
            oHoster.setDisplayName(sDisplayTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
 
    oGui.setEndOfDirectory()
