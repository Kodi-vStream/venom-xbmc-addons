#-*- coding: utf-8 -*-
# Par chataigne73 
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig



import re,urllib,urllib2,xbmc

#pour sucury
from resources.lib.sucuri import SucurieBypass

class NoRedirection(urllib2.HTTPErrorProcessor):    
    def http_response(self, request, response):
        return response


SITE_IDENTIFIER = 'sokrostream_biz'
SITE_NAME = 'Sokrostream'
SITE_DESC = 'Films & Séries en streaming en vf et Vostfr'

URL_MAIN = 'http://sokrostream.cc/'

MOVIE_NEWS = (URL_MAIN + 'categories/films', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'les-films-les-plus-vues-2', 'showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'les-films-les-plus-commentes-2', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'films-les-mieux-notes-2', 'showMovies')
MOVIE_GENRES = (URL_MAIN , 'showGenres')
MOVIE_VF = (URL_MAIN + 'langues/french', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'langues/vostfr', 'showMovies')

SERIE_NEWS = (URL_MAIN + 'categories/series-streaming', 'showMovies') # serie nouveautés
SERIE_SERIES = (URL_MAIN + 'categories/series-streaming', 'showMovies') # serie vrac
SERIE_VFS = (URL_MAIN + 'series-tv/langues/french', 'showMovies') # serie VF
SERIE_VOSTFRS = (URL_MAIN + 'series-tv/langues/vostfr', 'showMovies') # serie Vostfr
SERIE_HD = (URL_MAIN + 'series-tv/qualites/hd-720p', 'showMovies') # serie HD
SERIE_GENRES = (URL_MAIN + 'series-tv/', 'showGenres')

URL_SEARCH = (URL_MAIN + 'search.php?q=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

UA = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'films_views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_COMMENTS[1], 'Films (Les plus commentés)', 'films_comments.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'films_notes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showPys', 'Films (Par Pays)', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showAne', 'Films (Par Années)', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showQlt', 'Films (Qualités)', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showLag', 'Films (Langues)', 'lang.png', oOutputParameterHandler)
        
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showPlt', 'Films (Plateformes)', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)
    	
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
    liste.append( ['Action',sUrl + 'genre/action'] )
    liste.append( ['Animation',sUrl + 'genre/animation'] )
    liste.append( ['Aventure',sUrl + 'genre/aventure'] )
    liste.append( ['Biopic',sUrl + 'genre/biopic'] )
    liste.append( ['Comédie',sUrl + 'genre/comedie'] )
    liste.append( ['Comédie Dramatique',sUrl + 'genre/comedie-dramatique'] )
    liste.append( ['Comédie Musicale',sUrl + 'genre/comedie-musicale'] )
    liste.append( ['Drame',sUrl + 'genre/drame'] )
    liste.append( ['Epouvante Horreur',sUrl + 'genre/epouvante-horreur'] ) 
    liste.append( ['Espionnage',sUrl + 'genre/espionnage'] )
    liste.append( ['Famille',sUrl + 'genre/famille'] )
    liste.append( ['Fantastique',sUrl + 'genre/fantastique'] )  
    liste.append( ['Guerre',sUrl + 'genre/guerre'] )
    liste.append( ['Historique',sUrl + 'genre/historique'] )
    liste.append( ['Judiciaire',sUrl + 'genre/judiciaire'] )
    liste.append( ['Médical',sUrl + 'genre/musical'] )
    liste.append( ['Policier',sUrl + 'genre/policier'] )
    liste.append( ['Péplum',sUrl + 'genre/peplum'] )
    liste.append( ['Romance',sUrl + 'genre/romance'] )
    liste.append( ['Science-Fiction',sUrl + 'genre/science-fiction'] )
    liste.append( ['Thriller',sUrl + 'genre/thriller'] )
    liste.append( ['Western',sUrl + 'genre/western'] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
        
def showPys():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Americain',URL_MAIN + 'pays/americain'] )
    liste.append( ['Allemand',URL_MAIN + 'pays/allemand'] )
    liste.append( ['Britanique',URL_MAIN + 'pays/britannique'] )
    liste.append( ['Canadien',URL_MAIN + 'pays/canadien'] )
    liste.append( ['Espagnol',URL_MAIN + 'pays/espagnol'] )
    liste.append( ['Francais',URL_MAIN + 'pays/francais'] )
    liste.append( ['Italien',URL_MAIN + 'pays/italien/'] )
    liste.append( ['Japonnais',URL_MAIN + 'pays/japonnais'] )
    liste.append( ['Norvegien',URL_MAIN + 'pays/norvegien'] )
    
    
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()
    
def showAne():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['2017',URL_MAIN + 'annees/2017'] )
    liste.append( ['2016',URL_MAIN + 'annees/2016'] )
    liste.append( ['2015',URL_MAIN + 'annees/2015'] )
    liste.append( ['2014',URL_MAIN + 'annees/2014'] )
    liste.append( ['2013',URL_MAIN + 'annees/2013'] )
    liste.append( ['2012',URL_MAIN + 'annees/2012'] )
    liste.append( ['2011',URL_MAIN + 'annees/2011'] )
    liste.append( ['2010',URL_MAIN + 'annees/2010'] )
    liste.append( ['2009',URL_MAIN + 'annees/2009'] )
    liste.append( ['2008',URL_MAIN + 'annees/2008'] )
    liste.append( ['2007',URL_MAIN + 'annees/2007'] )
    liste.append( ['2006',URL_MAIN + 'annees/2006'] )
    liste.append( ['2005',URL_MAIN + 'annees/2005'] )
    liste.append( ['2004',URL_MAIN + 'annees/2004'] )
    liste.append( ['2003',URL_MAIN + 'annees/2003'] )
    liste.append( ['2002',URL_MAIN + 'annees/2002'] )
    liste.append( ['2001',URL_MAIN + 'annees/2001'] )
    liste.append( ['2000',URL_MAIN + 'annees/2000'] )
    liste.append( ['1999',URL_MAIN + 'annees/1999'] )
    liste.append( ['1998',URL_MAIN + 'annees/1998'] )
    liste.append( ['1997',URL_MAIN + 'annees/1997'] )
    liste.append( ['1996',URL_MAIN + 'annees/1996'] )
    liste.append( ['1995',URL_MAIN + 'annees/1995'] )
    liste.append( ['1994',URL_MAIN + 'annees/1994'] )
    liste.append( ['1993',URL_MAIN + 'annees/1993'] )
    liste.append( ['1992',URL_MAIN + 'annees/1992'] )
    liste.append( ['1991',URL_MAIN + 'annees/1991'] )
    liste.append( ['1990',URL_MAIN + 'annees/1990'] )
    liste.append( ['1989',URL_MAIN + 'annees/1989'] )
    liste.append( ['1988',URL_MAIN + 'annees/1988'] )
    liste.append( ['1987',URL_MAIN + 'annees/1987'] )
    liste.append( ['1986',URL_MAIN + 'annees/1986'] )
    liste.append( ['1985',URL_MAIN + 'annees/1985'] )
    liste.append( ['1984',URL_MAIN + 'annees/1984'] )
    liste.append( ['1983',URL_MAIN + 'annees/1983'] )
    liste.append( ['1982',URL_MAIN + 'annees/1982'] )
    liste.append( ['1981',URL_MAIN + 'annees/1981'] )
    liste.append( ['1980',URL_MAIN + 'annees/1980'] )
    liste.append( ['1979',URL_MAIN + 'annees/1979'] )
    liste.append( ['1978',URL_MAIN + 'annees/1978'] )
    liste.append( ['1977',URL_MAIN + 'annees/1977'] )
    liste.append( ['1976',URL_MAIN + 'annees/1976'] )
    liste.append( ['1975',URL_MAIN + 'annees/1975'] )
    liste.append( ['1974',URL_MAIN + 'annees/1974'] )
    liste.append( ['1973',URL_MAIN + 'annees/1973'] )
    liste.append( ['1972',URL_MAIN + 'annees/1972'] )
    liste.append( ['1971',URL_MAIN + 'annees/1971'] )
    liste.append( ['1970',URL_MAIN + 'annees/1970'] )
    liste.append( ['1969',URL_MAIN + 'annees/1969'] )
    liste.append( ['1968',URL_MAIN + 'annees/1968'] )
    liste.append( ['1967',URL_MAIN + 'annees/1967'] )
    liste.append( ['1966',URL_MAIN + 'annees/1966'] )
    liste.append( ['1964',URL_MAIN + 'annees/1964'] )
    liste.append( ['1963',URL_MAIN + 'annees/1963'] )
    liste.append( ['1962',URL_MAIN + 'annees/1962'] )
    liste.append( ['1961',URL_MAIN + 'annees/1961'] )
    liste.append( ['1960',URL_MAIN + 'annees/1960'] )
    liste.append( ['1959',URL_MAIN + 'annees/1959'] )
    liste.append( ['1957',URL_MAIN + 'annees/1957'] )
    liste.append( ['1956',URL_MAIN + 'annees/1956'] )
    liste.append( ['1955',URL_MAIN + 'annees/1955'] )
    liste.append( ['1954',URL_MAIN + 'annees/1954'] )
    liste.append( ['1953',URL_MAIN + 'annees/1953'] )
    liste.append( ['1952',URL_MAIN + 'annees/1952'] )
    liste.append( ['1951',URL_MAIN + 'annees/1951'] )
    liste.append( ['1950',URL_MAIN + 'annees/1950'] )
    liste.append( ['1945',URL_MAIN + 'annees/1945'] )
    liste.append( ['1940',URL_MAIN + 'annees/1940'] )
    liste.append( ['1937',URL_MAIN + 'annees/1937'] )
    liste.append( ['1936',URL_MAIN + 'annees/1936'] )
    liste.append( ['1933',URL_MAIN + 'annees/1933'] )
    liste.append( ['1931',URL_MAIN + 'annees/1931'] )
    liste.append( ['1925',URL_MAIN + 'annees/1925'] )

    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()
    
def showQlt():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['DVDRip',URL_MAIN + 'qualites/dvdrip'] )
    liste.append( ['BDRip',URL_MAIN + 'qualites/bdrip'] )
    liste.append( ['HD 720p',URL_MAIN + 'qualites/hd-720p/'] )
    liste.append( ['HD 1080p',URL_MAIN + 'qualites/hd-1080p/'] )   
    liste.append( ['R6',URL_MAIN + 'qualites/r6'] )
    #la suite fonctionne mais n'est pas dispo sur le site
    liste.append( ['DVDSCR',URL_MAIN + 'qualites/dvdscr'] )

    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()
        
def showLag():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['FRENCH',URL_MAIN + 'langues/french'] )
    liste.append( ['VO',URL_MAIN + 'langues/vo'] )
    liste.append( ['VOSTFR',URL_MAIN + 'langues/vostfr'] ) 
    
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()
    
def showPlt():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['OK.RU',URL_MAIN + 'plateformes/ok-ru'] ) 
    liste.append( ['FlashX',URL_MAIN + 'plateformes/flashx'] ) 
    liste.append( ['Netu',URL_MAIN + 'plateformes/netu'] )
    liste.append( ['OpenLoad',URL_MAIN + 'plateformes/openload'] )
    liste.append( ['Youwatch',URL_MAIN + 'plateformes/youwatch'] ) 
    liste.append( ['Vidup',URL_MAIN + 'plateformes/vidup'] )
    liste.append( ['Uptobox',URL_MAIN + 'plateformes/uptobox'] )
    # les suivants n'apparaissent plus sur le site mais fonctionnent
    liste.append( ['DivxStage',URL_MAIN + 'plateformes/divxstage'] )
    liste.append( ['Exashare',URL_MAIN + 'plateformes/exashare'] )
    liste.append( ['Firedrive',URL_MAIN + 'plateformes/firedrive'] )
    liste.append( ['MovShare',URL_MAIN + 'plateformes/movshare'] )
    liste.append( ['NovaMov',URL_MAIN + 'plateformes/novamov'] )
    liste.append( ['NowVideo',URL_MAIN + 'plateformes/nowvideo'] )
    liste.append( ['Putlocker',URL_MAIN + 'plateformes/putlocker'] )
    liste.append( ['RapidVideo',URL_MAIN + 'plateformes/rapidvideo'] )
    liste.append( ['SockShare',URL_MAIN + 'plateformes/sockshare'] )
    liste.append( ['SpeedVideo',URL_MAIN + 'plateformes/speedvideo'] )
    liste.append( ['UploadHero',URL_MAIN + 'plateformes/uploadhero'] )
    liste.append( ['UptoStream',URL_MAIN + 'plateformes/uptostream'] )
    liste.append( ['VideoMega',URL_MAIN + 'plateformes/videomega'] )
    liste.append( ['VideoWeed',URL_MAIN + 'plateformes/videoweed'] )
    liste.append( ['Vidto',URL_MAIN + 'plateformes/vidto'] )
    liste.append( ['Vimple',URL_MAIN + 'plateformes/vimple'] )
    liste.append( ['Vodlocker',URL_MAIN + 'plateformes/vodlocker'] )
    
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    
    if sSearch:
        sUrl = sSearch
        
        #need a cookie for search
        oRequestHandler = cRequestHandler(URL_MAIN)
        sHtmlContent = oRequestHandler.request()

        head = oRequestHandler.GetHeaders()
        
        c = re.search('Set-Cookie: PHPSESSID=(.+?);',str(head))
        if c:
            cookiesearch = 'PHPSESSID=' + c.group(1)

            #on recupere les cookie cloudflare
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()
            
            from resources.lib.config import GestionCookie
            cookies = GestionCookie().Readcookie('sokrostream_biz')
            
            #on ajoute les deux
            cookies = cookies + '; ' + cookiesearch
            
            #xbmc.log('NEW ****' + cookies, xbmc.LOGNOTICE)
        
        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('Cookie',cookies)
        oRequestHandler.addHeaderEntry('Referer',sUrl)
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4')
        oRequestHandler.addHeaderEntry('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('Content-Type', 'text/html; charset=utf-8')
        sHtmlContent = oRequestHandler.request()

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
        
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        #sHtmlContent = SucurieBypass().GetHtml(sUrl)
        
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

    sHtmlContent = sHtmlContent.replace('<span class="tr-dublaj"></span>', '').replace('<span class="tr-altyazi"></span>','').replace('<small>','').replace('</small>','').replace('<span class="likeThis">','').replace('</span>','')
    
    if (sSearch or ('/series' in sUrl) or ('/search/' in sUrl)):
        sHtmlContent = sHtmlContent.replace("\n","")
        sHtmlContent = re.sub('<div class="yazitip">Series similaires</div>.+','',sHtmlContent)
        sPattern = '<div class="moviefilm">\s+<a href=".+?">\s+<img src="([^<]+)" alt=".+?".+?<\/a>\s+<div class="movief"><a href="([^<]+)">(.+?)<\/a>'
    else:
        sPattern = '<div class="moviefilm"> *<a href=".+?"> *<img src="([^<]+)" alt=".+?" height=".+?" width=".+?" \/><\/a> *<div class="ozet">.+?</div> *<div class="movief"><a href="([^<]+)">([^<]+)<\/a><\/div> *<div class="movie.+?">(.+?)<\/div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent,sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            
            #on n'affiche pas les contenus similaires
            if (URL_MAIN + 'series/' in sUrl) and ('-saison-' not in aEntry[1]):
                continue
            
            if (sSearch or ('categories/series' in sUrl) or ('/series/' in sUrl) or ('/series-tv/' in sUrl) or ('/search/' in sUrl)):
                sTitle = aEntry[2]
            else:
                sTitle = aEntry[2]+' ('+aEntry[3]+')'
            
            if sMovieTitle:
                sTitle = sMovieTitle + sTitle
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            sUrl2 = str(aEntry[1])
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2 )
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))

            if ('-saison-' in sUrl2):
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle,'', aEntry[0], '', oOutputParameterHandler)
            elif ('/series/' in sUrl2):
                oGui.addTV(SITE_IDENTIFIER, 'showMovies', sDisplayTitle,'', aEntry[0], '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', aEntry[0], '', oOutputParameterHandler)
            
        cConfig().finishDialog(dialog)
        
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
            
    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent): 
    oParser = cParser()
    sPattern = '<span class="current">.+?<a class="page larger" href=\'(.+?)\'>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
    
def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request()
    sHtmlContent = SucurieBypass().GetHtml(sUrl)
    
    oParser = cParser()
    
    #get post vars
    #sPattern = '<div class="num_link">Lien.+?\/([vostfr]+)\.png">([^<]+).+?<input name="([^<]+)" value="(.+?)"'
    sPattern = '<div class="num_link">Lien.+?\.png">([^<>]+)<.+?\/([vostfr]+)\.png">.+?<input name="([^<]+)" value="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #xbmc.log(str(aResult))    
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sLang = '[' + aEntry[1].upper() + ']'
            sHost = aEntry[0]
            sHost = sHost.replace('Telecharger sur ','').replace('&nbsp;','')
            
            sTitle = sLang + ' ' + sMovieTitle
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            sTitle = sDisplayTitle +  ' [COLOR coral]' + sHost +'[/COLOR]'
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sUrl', sUrl)
            oOutputParameterHandler.addParameter('sPOST', str(aEntry[2]+'='+aEntry[3]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()  
 
 
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sPOST = oInputParameterHandler.getValue('sPOST')
    sUrl = oInputParameterHandler.getValue('sUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    if '29702' in sPOST:
        sPOST = ''
    

    sHtmlContent = ''

    #utilisation de sucuri en POST
    SBP = SucurieBypass()
    
    cookies = SBP.Readcookie('sokrostream_biz')
    
    opener = urllib2.build_opener(NoRedirection)
    opener.addheaders = SBP.SetHeader()
    
    if cookies:
        opener.addheaders.append(('Cookie', cookies))
    
    response = opener.open(sUrl,sPOST)
    sHtmlContent = response.read()
    response.close()
    
    if SBP.CheckIfActive(sHtmlContent):
        
        cConfig().log('sucuri present')
        
        #on cherche le nouveau cookie
        cookies = SBP.DecryptCookie(sHtmlContent)

        #on sauve le nouveau cookie
        SBP.SaveCookie('sokrostream_biz',cookies)
        
        #et on recommence
        opener2 = urllib2.build_opener(NoRedirection)
        opener2.addheaders = SBP.SetHeader()
        opener2.addheaders.append(('Cookie', cookies))
        
        response2 = opener2.open(sUrl,sPOST)
        sHtmlContent = response2.read()
        response2.close()
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
    
    sHtmlContent = re.sub(r'<iframe.+?src=(.+?//www\.facebook\.com.+</iframe>)','',sHtmlContent)
    
    oParser = cParser()

    sPattern = '<iframe.+?src=([^ ]+).+?<\/iframe>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        cUrl = str(aResult[1][0])
        if 'sokrostr' in cUrl:
            UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
            headers = {'User-Agent': UA ,
                       'Host' : 'sokrostrem.xyz',
                       'Referer': sUrl,
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Content-Type': 'text/html; charset=utf-8'}

            request = urllib2.Request(cUrl,None,headers)
            reponse = urllib2.urlopen(request)
            repok = reponse.read()
            reponse.close()
            vUrl = re.search('url=([^"]+)"',repok)
            if vUrl:   
               sHosterUrl = vUrl.group(1)
               if 'uptobox' in sHosterUrl:
                   sHosterUrl = re.sub(r'(http://sokrostream.+?/uptobox\.php\?id=)','http://uptobox.com/',sHosterUrl)
                   
        else:
            sHosterUrl = str(aResult[1][0])
            
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
            oHoster.setDisplayName(sDisplayTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
                
    oGui.setEndOfDirectory()
   
def showEpisode(): #cherche les episode de series

    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request()
    sHtmlContent = SucurieBypass().GetHtml(sUrl)
    
    #cConfig().log(sMovieTitle)
    
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','').replace('<iframe src=\'http://creative.rev2pub.com','')
 
    sPattern = '<div class="movief2"><a href="([^<]+)" class="listefile">(.+?)<\/a><\/div>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle + ' ' + aEntry[1]
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addTV(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)            
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
