#-*- coding: utf-8 -*-
# Par chataigne73 

from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig
import re, urllib, urllib2
from urllib2 import URLError

import xbmc

SITE_IDENTIFIER = 'sokrostream_biz'
SITE_NAME = 'Sokrostream'
SITE_DESC = 'Film en streaming, regarder film en direct, streaming vf regarder film gratuitement sur SokroStream.com'

URL_MAIN = 'http://sokrostream.biz/'

MOVIE_NEWS = (URL_MAIN + 'categories/films', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'les-films-les-plus-vues-2', 'showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'les-films-les-plus-commentes-2', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'films-les-mieux-notes-2', 'showMovies')
MOVIE_GENRES = (URL_MAIN , 'showGenre')
MOVIE_VF = (URL_MAIN + 'langues/french', 'showMovies') # films VF
MOVIE_VOSTFR = (URL_MAIN + 'langues/vostfr', 'showMovies') # films VOSTFR

SERIE_NEWS = (URL_MAIN + 'categories/series', 'showMovies') # serie nouveautés
SERIE_SERIES = (URL_MAIN + 'categories/series', 'showMovies') # serie vrac
SERIE_VFS = (URL_MAIN + 'series-tv/langues/french', 'showMovies') # serie VF
SERIE_VOSTFRS = (URL_MAIN + 'series-tv/langues/vostfr', 'showMovies') # serie Vostfr
SERIE_GENRES = (URL_MAIN + 'series-tv/', 'showGenre')

URL_SEARCH = ('http://sokrostream.biz/search.php?slug=&slug=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautes', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films Les plus vus', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_COMMENTS[1], 'Films Les plus commentes', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films Les mieux notes', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films Genre', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showPys', 'Films Pays', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showAne', 'Films Années', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showQlt', 'Films Qualites', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showLag', 'Films Langues', 'films.png', oOutputParameterHandler)
        
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showPlt', 'Films Plateforme', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Series', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Series Genre', 'genres.png', oOutputParameterHandler)
    	
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
    
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action',sUrl + 'genre/action'] )
    liste.append( ['Animation',sUrl + 'genre/animation'] )
    liste.append( ['Aventure',sUrl + 'genre/aventure'] )
    liste.append( ['Biopic',sUrl + 'genre/biopic'] )
    liste.append( ['Comedie',sUrl + 'genre/comedie'] )
    liste.append( ['Comedie Dramatique',sUrl + 'genre/comedie-dramatique'] )
    liste.append( ['Comedie Musicale',sUrl + 'genre/comedie-musicale'] )
    liste.append( ['Drame',sUrl + 'genre/drame'] )
    liste.append( ['Epouvante Horreur',sUrl + 'genre/epouvante-horreur'] ) 
    liste.append( ['Espionnage',sUrl + 'genre/espionnage'] )
    liste.append( ['Famille',sUrl + 'genre/famille'] )
    liste.append( ['Fantastique',sUrl + 'genre/fantastique'] )  
    liste.append( ['Guerre',sUrl + 'genre/guerre'] )
    liste.append( ['Historique',sUrl + 'genre/historique'] )
    liste.append( ['Judiciaire',sUrl + 'genre/historique'] )
    liste.append( ['Medical',sUrl + 'genre/musical'] )
    liste.append( ['Policier',sUrl + 'genre/policier'] )
    liste.append( ['Peplum',sUrl + 'genre/peplum'] )
    liste.append( ['Romance',sUrl + 'genre/romance'] )
    liste.append( ['Science Fiction',sUrl + 'genre/science-fiction'] )
    liste.append( ['Thriller',sUrl + 'genre/thriller'] )
    liste.append( ['Western',sUrl + 'genre/western'] )
                
    for sTitle,sUrl in liste:#boucle
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
        
def showPys():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Americain',URL_MAIN + 'pays/americain/'] )
    liste.append( ['Allemand',URL_MAIN + 'pays/allemand/'] )
    liste.append( ['Britanique',URL_MAIN + 'pays/britannique/'] )
    liste.append( ['Canadien',URL_MAIN + 'pays/canadien/'] )
    liste.append( ['Espagnol',URL_MAIN + 'pays/espagnol/'] )
    liste.append( ['Francais',URL_MAIN + 'pays/francais/'] )
    liste.append( ['Italien',URL_MAIN + 'pays/italien/'] )
    liste.append( ['Japonnais',URL_MAIN + 'pays/japonnais/'] )
    liste.append( ['Norvegien',URL_MAIN + 'pays/norvegien/'] )
    
    
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
    liste.append( ['1925',URL_MAIN + 'annees/1925/'] )
    liste.append( ['1931',URL_MAIN + 'annees/1931/'] )
    liste.append( ['1933',URL_MAIN + 'annees/1933/'] )
    liste.append( ['1936',URL_MAIN + 'annees/1936/'] )
    liste.append( ['1937',URL_MAIN + 'annees/1937/'] )
    liste.append( ['1940',URL_MAIN + 'annees/1940/'] )
    liste.append( ['1945',URL_MAIN + 'annees/1945/'] )
    liste.append( ['1950',URL_MAIN + 'annees/1950/'] )
    liste.append( ['1951',URL_MAIN + 'annees/1951/'] )
    liste.append( ['1952',URL_MAIN + 'annees/1952/'] )
    liste.append( ['1953',URL_MAIN + 'annees/1953/'] )
    liste.append( ['1954',URL_MAIN + 'annees/1954/'] )
    liste.append( ['1955',URL_MAIN + 'annees/1955/'] )
    liste.append( ['1956',URL_MAIN + 'annees/1956/'] )
    liste.append( ['1957',URL_MAIN + 'annees/1957/'] )
    liste.append( ['1959',URL_MAIN + 'annees/1959/'] )
    liste.append( ['1960',URL_MAIN + 'annees/1960/'] )
    liste.append( ['1961',URL_MAIN + 'annees/1961/'] )
    liste.append( ['1962',URL_MAIN + 'annees/1962/'] )
    liste.append( ['1963',URL_MAIN + 'annees/1963/'] )
    liste.append( ['1964',URL_MAIN + 'annees/1964/'] )
    liste.append( ['1966',URL_MAIN + 'annees/1966/'] )
    liste.append( ['1967',URL_MAIN + 'annees/1967/'] )
    liste.append( ['1968',URL_MAIN + 'annees/1968/'] )
    liste.append( ['1969',URL_MAIN + 'annees/1969/'] )
    liste.append( ['1970',URL_MAIN + 'annees/1970/'] )
    liste.append( ['1971',URL_MAIN + 'annees/1971/'] )
    liste.append( ['1972',URL_MAIN + 'annees/1972/'] )
    liste.append( ['1973',URL_MAIN + 'annees/1973/'] )
    liste.append( ['1974',URL_MAIN + 'annees/1974/'] )
    liste.append( ['1975',URL_MAIN + 'annees/1975/'] )
    liste.append( ['1976',URL_MAIN + 'annees/1976/'] )
    liste.append( ['1977',URL_MAIN + 'annees/1977/'] )
    liste.append( ['1978',URL_MAIN + 'annees/1978/'] )
    liste.append( ['1979',URL_MAIN + 'annees/1979/'] )
    liste.append( ['1980',URL_MAIN + 'annees/1980/'] )
    liste.append( ['1981',URL_MAIN + 'annees/1981/'] )
    liste.append( ['1982',URL_MAIN + 'annees/1982/'] )
    liste.append( ['1983',URL_MAIN + 'annees/1983/'] )
    liste.append( ['1984',URL_MAIN + 'annees/1984/'] )
    liste.append( ['1985',URL_MAIN + 'annees/1985/'] )
    liste.append( ['1986',URL_MAIN + 'annees/1986/'] )
    liste.append( ['1987',URL_MAIN + 'annees/1987/'] )
    liste.append( ['1988',URL_MAIN + 'annees/1988/'] )
    liste.append( ['1989',URL_MAIN + 'annees/1989/'] )
    liste.append( ['1990',URL_MAIN + 'annees/1990/'] )
    liste.append( ['1991',URL_MAIN + 'annees/1991/'] )
    liste.append( ['1992',URL_MAIN + 'annees/1992/'] )
    liste.append( ['1993',URL_MAIN + 'annees/1993/'] )
    liste.append( ['1994',URL_MAIN + 'annees/1994/'] )
    liste.append( ['1995',URL_MAIN + 'annees/1995/'] )
    liste.append( ['1996',URL_MAIN + 'annees/1996/'] )
    liste.append( ['1997',URL_MAIN + 'annees/1997/'] )
    liste.append( ['1998',URL_MAIN + 'annees/1998/'] )
    liste.append( ['1999',URL_MAIN + 'annees/1999/'] )
    liste.append( ['2000',URL_MAIN + 'annees/2000/'] )
    liste.append( ['2001',URL_MAIN + 'annees/2001/'] )
    liste.append( ['2002',URL_MAIN + 'annees/2002/'] )
    liste.append( ['2003',URL_MAIN + 'annees/2003/'] )
    liste.append( ['2004',URL_MAIN + 'annees/2004/'] )
    liste.append( ['2005',URL_MAIN + 'annees/2005/'] )
    liste.append( ['2006',URL_MAIN + 'annees/2006/'] )
    liste.append( ['2007',URL_MAIN + 'annees/2007/'] )
    liste.append( ['2008',URL_MAIN + 'annees/2008/'] )
    liste.append( ['2009',URL_MAIN + 'annees/2009/'] )
    liste.append( ['2010',URL_MAIN + 'annees/2010/'] )
    liste.append( ['2011',URL_MAIN + 'annees/2011/'] )
    liste.append( ['2012',URL_MAIN + 'annees/2012/'] )
    liste.append( ['2013',URL_MAIN + 'annees/2013/'] )
    liste.append( ['2014',URL_MAIN + 'annees/2014/'] )
    liste.append( ['2015',URL_MAIN + 'annees/2015/'] )

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
    #liste.append( ['1080p',URL_MAIN + 'qualites/1080p/'] )   
    #liste.append( ['720p',URL_MAIN + 'qualites/720p/'] )
    liste.append( ['BDRip',URL_MAIN + 'qualites/bdrip'] )
    #liste.append( ['BRRip',URL_MAIN + 'qualites/BRRip/'] )
    liste.append( ['CAMRip',URL_MAIN + 'qualites/camrip'] )
    liste.append( ['DVDRip',URL_MAIN + 'qualites/dvdrip'] )
    liste.append( ['DVDSCR',URL_MAIN + 'qualites/dvdscr'] )
    #liste.append( ['HDRip',URL_MAIN + 'qualites/HDRip/'] )
    #liste.append( ['HDTV',URL_MAIN + 'qualites/HDTV/'] )
    #liste.append( ['PDTV',URL_MAIN + 'qualites/PDTV/'] )
    liste.append( ['R6',URL_MAIN + 'qualites/r6'] )
    #liste.append( ['TS MD',URL_MAIN + 'qualites/ts-md/'] )
    #liste.append( ['TVRip',URL_MAIN + 'qualites/TVRip/'] )
    #liste.append( ['VHSRip',URL_MAIN + 'qualites/VHSRip/'] )
    #liste.append( ['VOBRIP',URL_MAIN + 'qualites/VOBRIP/'] )
    #liste.append( ['WEB-DL',URL_MAIN + 'qualites/web-dl/'] )
    #liste.append( ['WEBRIP',URL_MAIN + 'qualites/WEBRIP/'] )

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
    liste.append( ['Cloudy.ec',URL_MAIN + 'plateformes/cloudy'] )
    liste.append( ['DivxStage',URL_MAIN + 'plateformes/divxstage'] )
    liste.append( ['Easywatch',URL_MAIN + 'langues/easywatch'] )
    liste.append( ['Exashare',URL_MAIN + 'plateformes/exashare'] )
    liste.append( ['FastVideo',URL_MAIN + 'plateformes/fastvideo'] )
    liste.append( ['Firedrive',URL_MAIN + 'plateformes/firedrive'] )
    liste.append( ['GigaUpload',URL_MAIN + 'plateformes/gigaupload'] )
    liste.append( ['MadVID',URL_MAIN + 'plateformes/madvid'] )
    liste.append( ['MailRu',URL_MAIN + 'plateformes/mailru'] )
    liste.append( ['MixtureVideo',URL_MAIN + 'plateformes/mixturevideo'] )
    liste.append( ['Moevideo',URL_MAIN + 'plateformes/moevideo'] )
    liste.append( ['MovShare',URL_MAIN + 'plateformes/movshare'] )
    liste.append( ['MyStream.la',URL_MAIN + 'plateformes/myStream-la'] )
    liste.append( ['Netu',URL_MAIN + 'plateformes/netu'] )
    liste.append( ['NovaMov',URL_MAIN + 'plateformes/novamov'] )
    liste.append( ['NowVideo',URL_MAIN + 'plateformes/nowvideo'] )
    liste.append( ['OneVideo',URL_MAIN + 'plateformes/onevideo'] )
    liste.append( ['Purevideo',URL_MAIN + 'plateformes/purevideo'] )
    liste.append( ['Putlocker',URL_MAIN + 'plateformes/putlocker'] )
    liste.append( ['RapidVideo',URL_MAIN + 'plateformes/rapidvideo'] )
    liste.append( ['SockShare',URL_MAIN + 'plateformes/sockshare'] )
    liste.append( ['SpeedVideo',URL_MAIN + 'plateformes/speedvideo'] )
    liste.append( ['TurboVid',URL_MAIN + 'plateformes/turbovid'] )
    liste.append( ['UploadBB',URL_MAIN + 'plateformes/uploadbb'] )
    liste.append( ['UploadHero',URL_MAIN + 'plateformes/uploadhero'] )
    liste.append( ['UptoStream',URL_MAIN + 'plateformes/uptostream'] )
    liste.append( ['VideoHut',URL_MAIN + 'plateformes/videohut'] )
    liste.append( ['VideoMega',URL_MAIN + 'plateformes/videomega'] )
    liste.append( ['VideoRaj',URL_MAIN + 'plateformes/videoraj'] )
    liste.append( ['VideoWeed',URL_MAIN + 'plateformes/videoweed'] )
    liste.append( ['Vidto',URL_MAIN + 'plateformes/vidto'] )
    liste.append( ['VidZi.tv',URL_MAIN + 'plateformes/vidzi-tv'] )
    liste.append( ['Vimple',URL_MAIN + 'plateformes/vimple'] )
    liste.append( ['VK Player',URL_MAIN + 'plateformes/vk-player'] )
    liste.append( ['Vodlocker',URL_MAIN + 'plateformes/vodlocker'] )
    liste.append( ['Watching.to',URL_MAIN + 'plateformes/watching-to'] )
    liste.append( ['Youwatch',URL_MAIN + 'plateformes/youwatch'] ) 
    
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    if sSearch:
      sUrl = sSearch

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
        
    #print sUrl
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()	
    sHtmlContent = sHtmlContent.replace('<span class="tr-dublaj"></span>', '').replace('<span class="tr-altyazi"></span>','').replace('<small>','').replace('</small>','').replace('<span class="likeThis">','').replace('</span>','')
    
    if (sSearch or ('/series' in sUrl)):
      #sPattern = '<div class="moviefilm"> *<a href=".+?"> *<img src="([^<]+)" alt=".+?" height=".+?" width=".+?" \/><\/a> *<div class="movief"><a href="([^<]+)">(.+?)<\/a><\/div> *<div class="movies"><\/div>'
      sPattern = '<div class="moviefilm"> *<a href=".+?"> *<img src="([^<]+)" alt=".+?" height="125px" width="119px" \/><\/a> *<div class="movief"><a href="([^<]+)">(.+?)<\/a>'
    else:
      sPattern = '<div class="moviefilm"> *<a href=".+?"> *<img src="([^<]+)" alt=".+?" height=".+?" width=".+?" \/><\/a> *<div class="ozet">.+?</div> *<div class="movief"><a href="([^<]+)">([^<]+)<\/a><\/div> *<div class="movies">(.+?)<\/div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            
            #on n'affiche pas les contenus similaires
            if (URL_MAIN + 'series/' in sUrl) and ('-saison-' not in aEntry[1]):
                continue
            
            if (sSearch or ('categories/series' in sUrl) or ('/series/' in sUrl) or ('/series-tv/' in sUrl)):
              sTitle = aEntry[2]
            else:
              sTitle = aEntry[2]+' ('+aEntry[3]+')'
              
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            sUrl2 = str(aEntry[1])
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2 )
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
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
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #import xbmc
    #xbmc.log(sUrl)       
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()

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
            sHost = sHost.replace('Telecharger sur ','')
                
            sDisplayTitle = cUtil().DecoTitle(sLang + sMovieTitle)
            sTitle = sDisplayTitle +  ' - [COLOR skyblue]' + sHost +'[/COLOR]'
            
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
    
    #data = urllib.urlencode(sPOST)
    request = urllib2.Request(sUrl,sPOST)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
    sHtmlContent = ''
    try: 
        reponse = urllib2.urlopen(request)
        sHtmlContent = reponse.read()
        reponse.close
    except URLError, e:
        print e.read()
        print e.reason
    
    oParser = cParser()
    
    #Recherche du bon fichier
    sPattern = '<iframe.+?src=([^ ]+) |<script[^<>]+src="([^<>" ]+hash[^"]+)"><\/script>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    #print aResult
    	
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            if aEntry[0]:
                sHosterUrl = str(aEntry[0])
            else:
                sHosterUrl = str(aEntry[1])               
                
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

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','').replace('<iframe src=\'http://creative.rev2pub.com','')
 
    sPattern = '<div class="moviefilm2"><div class="movief2"><a href="([^<]+)" class="listefile">(.+?)<\/a><\/div><\/div>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    
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
