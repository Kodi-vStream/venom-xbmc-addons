#-*- coding: utf-8 -*-
#Venom.
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
import re, urllib
import urllib2


SITE_IDENTIFIER = 'frenchstream_org'
SITE_NAME = 'FrenchStream'
SITE_DESC = 'Films/Series/Animes en streaming'

URL_MAIN = 'http://frenchstream.tv/'
#URL_MAIN = 'http://154.46.33.11/'


MOVIE_MOVIE = (URL_MAIN + 'films/', 'showMovies')
MOVIE_NEWS = (URL_MAIN , 'showMovies')
MOVIE_HD = (URL_MAIN + 'films-hd/', 'showMovies')
#MOVIE_VIEWS = (URL_MAIN + 'les-plus-vues/', 'showMovies')
#MOVIE_COMMENTS = (URL_MAIN + 'les-plus-commentes/', 'showMovies')
#MOVIE_NOTES = (URL_MAIN + 'les-mieux-notes/', 'showMovies')
MOVIE_OSC = (URL_MAIN + 'mots-clefs/oscars-2016/', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'films-genre/', 'showGenre')

SERIE_SERIES = (URL_MAIN + 'series/', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'genre-series/', 'showGenre')
#SERIE_NEWS = (URL_MAIN + 'tv-series/', 'showMovies')

ANIM_ANIMS = (URL_MAIN +'/animes', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'




#-------------------------------------------------
#Partie speciale pour contourner le DNS ban

import httplib
import socket

def MyResolver(host):
    if host == 'frenchstream.tv':
        #return '154.46.33.11'
        return 'frenchstream.tv'
    else:
        return host

class MyHTTPConnection(httplib.HTTPConnection):
    def connect(self):
        self.sock = socket.create_connection((MyResolver(self.host),self.port),self.timeout)

class MyHTTPHandler(urllib2.HTTPHandler):
    def http_open(self,req):
        return self.do_open(MyHTTPConnection,req)
        
def GetHtmlViaDns(url,postdata = None):
    opener = urllib2.build_opener(MyHTTPHandler)
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de-DE; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')]
    urllib2.install_opener(opener)

    f = urllib2.urlopen(url,postdata)
    sHtmlContent = f.read()
    f.close()
    
    return sHtmlContent
        
#---------------------------------------------------




def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films HD', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_OSC[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_OSC[1], 'Films OSCARS 2016', 'news.png',   oOutputParameterHandler)
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    #oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus Vues', 'films.png', oOutputParameterHandler)
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    #oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus Commentés', 'films.png', oOutputParameterHandler)
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    #oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les mieux Notés', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showPys', 'Films Pays', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showAne', 'Films Années', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showQlt', 'Films Qualités', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showLag', 'Films Langues', 'films.png', oOutputParameterHandler)
        
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    #oGui.addDir(SITE_IDENTIFIER, 'showPlt', 'Films Plateforme', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Series', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Series Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animes', 'series.png', oOutputParameterHandler)
    
            
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_MAIN + '?s='+sSearchText  
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
    
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action',sUrl + 'action'] )
    liste.append( ['Animation',sUrl + 'animation'] )
    liste.append( ['Aventure',sUrl + 'aventure'] )
    #liste.append( ['Biographie',sUrl + 'biographie'] )
    liste.append( ['Biopic',sUrl + 'biopic'] )
    liste.append( ['Comédie',sUrl + 'comedie'] )
    liste.append( ['Comédie Dramatique',sUrl + 'comedie-dramatique'] )
    liste.append( ['Comédie Musicale',sUrl + 'comedie-musicale'] )
    #liste.append( ['Crime',sUrl + 'crime'] )
    liste.append( ['Documentaire',sUrl + 'documentaire'] )
    liste.append( ['Drame',sUrl + 'drame'] )
    liste.append( ['Epouvante Horreur',sUrl + 'epouvante-horreur'] )
    liste.append( ['Espionage',sUrl + 'espionnage'] )  
    liste.append( ['Famille',sUrl + 'famille'] )
    liste.append( ['Fantastique',sUrl + 'fantastique'] )
    liste.append( ['Guerre',sUrl + 'guerre'] )
    liste.append( ['Histoire',sUrl + 'histoire'] )
    #liste.append( ['Horreur',sUrl + 'horreur'] )
    #liste.append( ['Judiciaire',sUrl + 'judiciaire'] )
    #liste.append( ['Médical',sUrl + 'medical'] )
    liste.append( ['Musical',sUrl + 'musical'] )
    #liste.append( ['Mystère',sUrl + 'mystere'] )
    liste.append( ['Policier',sUrl + 'policier'] )
    liste.append( ['Romance',sUrl + 'romance'] )
    liste.append( ['Sciense Fiction',sUrl + 'science-fiction'] )
    liste.append( ['Sport Event',sUrl + 'sport-event'] )
    liste.append( ['Thriller',sUrl + 'thriller'] )
    #liste.append( ['Thriller Psychologique',sUrl + 'thriller-psychologique'] ) 
    liste.append( ['Western',sUrl + 'western'] )
               
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
    liste.append( ['Afghanistan',URL_MAIN + 'films-pays/afghanistan/'] )
    liste.append( ['Afrique du Sud',URL_MAIN + 'films-pays/afrique-du-sud/'] )
    liste.append( ['Algérie',URL_MAIN + 'films-pays/algerie/'] )
    liste.append( ['Allemangne',URL_MAIN + 'films-pays/allemangne/'] )
    liste.append( ['Angleterre',URL_MAIN + 'films-pays/angleterre/'] ) 
    liste.append( ['Argentine',URL_MAIN + 'films-pays/argentine/'] )
    liste.append( ['Australie',URL_MAIN + 'films-pays/australie/'] )
    liste.append( ['Autriche',URL_MAIN + 'films-pays/autriche/'] )
    liste.append( ['Belgique',URL_MAIN + 'films-pays/belgique/'] )
    liste.append( ['Brésil',URL_MAIN + 'films-pays/bresil/'] )
    liste.append( ['Britanique',URL_MAIN + 'films-pays/britannique/'] )
    liste.append( ['Bulgarie',URL_MAIN + 'films-pays/bulgarie/'] )
    liste.append( ['Cambodgien',URL_MAIN + 'films-pays/cambodgien/'] )
    liste.append( ['Cameroun',URL_MAIN + 'films-pays/cameroun/'] )
    liste.append( ['Canada',URL_MAIN + 'films-pays/canada/'] )
    liste.append( ['Chelie',URL_MAIN + 'films-pays/chelie/'] )
    liste.append( ['Chine',URL_MAIN + 'films-pays/chine/'] )
    liste.append( ['colombie',URL_MAIN + 'films-pays/colombie/'] )
    liste.append( ['Corée',URL_MAIN + 'films-pays/coree/'] )
    liste.append( ['Corée du sud',URL_MAIN + 'films-pays/coree-du-sud/'] )
    liste.append( ['Croitie',URL_MAIN + 'films-pays/croitie/'] )
    liste.append( ['Cuba',URL_MAIN + 'films-pays/cuba/'] )
    liste.append( ['Danemark',URL_MAIN + 'films-pays/danemark/'] )
    liste.append( ['Emarats arabes unis',URL_MAIN + 'films-pays/emarats-arabes-unis/'] )
    liste.append( ['Espagne',URL_MAIN + 'films-pays/espagne/'] )
    liste.append( ['Etats-Unis',URL_MAIN + 'films-pays/etats-unis/'] )
    liste.append( ['Finlande',URL_MAIN + 'films-pays/finlande/'] )
    liste.append( ['France',URL_MAIN + 'films-pays/france/'] )
    liste.append( ['Grec',URL_MAIN + 'films-pays/grec/'] )
    liste.append( ['Haiti',URL_MAIN + 'films-pays/haiti/'] )
    liste.append( ['Hollande',URL_MAIN + 'films-pays/hollande/'] )
    liste.append( ['Hong kong',URL_MAIN + 'films-pays/hong-kong/'] )
    liste.append( ['Hongrie',URL_MAIN + 'films-pays/hongrie/'] )
    liste.append( ['Inde',URL_MAIN + 'films-pays/inde/'] )
    liste.append( ['Indonésie',URL_MAIN + 'films-pays/indonesie/'] )
    liste.append( ['Iran',URL_MAIN + 'films-pays/iran/'] )
    liste.append( ['Irlande',URL_MAIN + 'films-pays/irlande/'] )
    liste.append( ['Islande',URL_MAIN + 'films-pays/islande/'] )
    liste.append( ['Israel',URL_MAIN + 'films-pays/israel/'] )
    liste.append( ['Italie',URL_MAIN + 'films-pays/italie/'] )
    liste.append( ['Japon',URL_MAIN + 'films-pays/japon/'] )
    liste.append( ['Kasakh',URL_MAIN + 'films-pays/kasakh/'] )
    liste.append( ['Kenya',URL_MAIN + 'films-pays/kenya/'] )
    liste.append( ['Koweit',URL_MAIN + 'films-pays/koweit/'] )
    liste.append( ['Liechtenstein',URL_MAIN + 'films-pays/liechtenstein/'] )
    liste.append( ['Lituanie',URL_MAIN + 'films-pays/lituanie/'] )
    liste.append( ['Lexembourg',URL_MAIN + 'films-pays/lexembourg/'] )
    liste.append( ['Malaisie',URL_MAIN + 'films-pays/malaisie/'] )
    liste.append( ['Mali',URL_MAIN + 'films-pays/mali/'] )
    liste.append( ['Maroc',URL_MAIN + 'films-pays/maroc/'] )
    liste.append( ['Mexique',URL_MAIN + 'films-pays/mexique/'] )
    liste.append( ['Monaco',URL_MAIN + 'films-pays/monaco/'] )
    liste.append( ['Népalais',URL_MAIN + 'films-pays/nepalais/'] )
    liste.append( ['Nigeria',URL_MAIN + 'films-pays/nigeria/'] )
    liste.append( ['NorvÃ¨ge',URL_MAIN + 'films-pays/norvege/'] )
    liste.append( ['Nouvelle-Zélande',URL_MAIN + 'films-pays/nouvelle-zelande/'] )
    liste.append( ['Palestine',URL_MAIN + 'films-pays/palestine/'] )
    liste.append( ['Panama',URL_MAIN + 'films-pays/panama/'] )
    liste.append( ['Paraguay',URL_MAIN + 'films-pays/paraguay/'] )
    liste.append( ['Pays-Bas',URL_MAIN + 'films-pays/pays-bas/'] )
    liste.append( ['Perou',URL_MAIN + 'films-pays/perou/'] )
    liste.append( ['Philippin',URL_MAIN + 'films-pays/philippin/'] )
    liste.append( ['Philippines',URL_MAIN + 'films-pays/philippines/'] )
    liste.append( ['Polongne',URL_MAIN + 'films-pays/polongne/'] )
    liste.append( ['Porto Rico',URL_MAIN + 'films-pays/porto-rico/'] )
    liste.append( ['Portugal',URL_MAIN + 'films-pays/portugal/'] )
    liste.append( ['Quatar',URL_MAIN + 'films-pays/quatar/'] )
    liste.append( ['Québec',URL_MAIN + 'films-pays/quebec/'] )
    liste.append( ['République tchÃ¨que',URL_MAIN + 'films-pays/republique-tcheque/'] )
    liste.append( ['Reunion',URL_MAIN + 'films-pays/reunion/'] )
    liste.append( ['Roumanie',URL_MAIN + 'films-pays/roumanie/'] )
    liste.append( ['Russie',URL_MAIN + 'films-pays/russie/'] )
    liste.append( ['Saoudien',URL_MAIN + 'films-pays/saoudien/'] )
    liste.append( ['Sénégal',URL_MAIN + 'films-pays/senegale/'] )
    liste.append( ['Serbie',URL_MAIN + 'films-pays/serbie/'] )
    liste.append( ['Singapour',URL_MAIN + 'films-pays/serbie/'] )
    liste.append( ['Slovene',URL_MAIN + 'films-pays/serbie/'] )
    liste.append( ['Sud-Créen',URL_MAIN + 'films-pays/sud-coreen/'] )
    liste.append( ['SuÃ¨de',URL_MAIN + 'films-pays/suede/'] )
    liste.append( ['Suisse',URL_MAIN + 'films-pays/suisse/'] )
    liste.append( ['Taiwan',URL_MAIN + 'films-pays/taiwan/'] )
    liste.append( ['Tchad',URL_MAIN + 'films-pays/tchad/'] )
    liste.append( ['Tchécoslovaquie',URL_MAIN + 'films-pays/tchecoslovaquie/'] )
    liste.append( ['TchÃ¨que',URL_MAIN + 'films-pays/tcheque/'] )
    liste.append( ['Thailand',URL_MAIN + 'films-pays/thailand/'] )
    liste.append( ['Tunisie',URL_MAIN + 'films-pays/tunisie/'] )
    liste.append( ['Turquie',URL_MAIN + 'films-pays/turquie/'] )
    liste.append( ['Ukraine',URL_MAIN + 'films-pays/ukraine/'] )
    liste.append( ['Uruguay',URL_MAIN + 'films-pays/uruguay/'] )
    liste.append( ['Vietnam',URL_MAIN + 'films-pays/vietnam/'] )
    liste.append( ['Yougoslavie',URL_MAIN + 'films-pays/yougoslavie/'] )  
     
    
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
    liste.append( ['1080p',URL_MAIN + 'qualites/1080p/'] )   
    liste.append( ['720p',URL_MAIN + 'qualites/720p/'] )
    liste.append( ['BDRip',URL_MAIN + 'qualites/BDRip/'] )
    liste.append( ['BRRip',URL_MAIN + 'qualites/BRRip/'] )
    liste.append( ['CAMRip',URL_MAIN + 'qualites/CAMRip/'] )
    liste.append( ['DVDRip',URL_MAIN + 'qualites/DVDRip/'] )
    liste.append( ['DVDSCR',URL_MAIN + 'qualites/DVDSCR/'] )
    liste.append( ['HDRip',URL_MAIN + 'qualites/HDRip/'] )
    liste.append( ['HDTV',URL_MAIN + 'qualites/HDTV/'] )
    liste.append( ['PDTV',URL_MAIN + 'qualites/PDTV/'] )
    liste.append( ['R6',URL_MAIN + 'qualites/R6/'] )
    liste.append( ['TS MD',URL_MAIN + 'qualites/ts-md/'] )
    liste.append( ['TVRip',URL_MAIN + 'qualites/TVRip/'] )
    liste.append( ['VHSRip',URL_MAIN + 'qualites/VHSRip/'] )
    liste.append( ['VOBRIP',URL_MAIN + 'qualites/VOBRIP/'] )
    liste.append( ['WEB-DL',URL_MAIN + 'qualites/web-dl/'] )
    liste.append( ['WEBRIP',URL_MAIN + 'qualites/WEBRIP/'] )
    
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
    liste.append( ['FRENCH',URL_MAIN + 'langues/french/'] )
    liste.append( ['VO',URL_MAIN + 'langues/vo/'] )
    liste.append( ['VOSTFR',URL_MAIN + 'langues/vostfr/'] ) 
    
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
    liste.append( ['2016',URL_MAIN + 'films-annees/2016/'] )
    liste.append( ['2015',URL_MAIN + 'films-annees/2015/'] )
    liste.append( ['2014',URL_MAIN + 'films-annees/2014/'] ) 
    liste.append( ['2013',URL_MAIN + 'films-annees/2013/'] )
    liste.append( ['2012',URL_MAIN + 'films-annees/2012/'] )
    liste.append( ['2011',URL_MAIN + 'films-annees/2011/'] )
    liste.append( ['2010',URL_MAIN + 'films-annees/2010/'] )
    liste.append( ['2009',URL_MAIN + 'films-annees/2009/'] )
    liste.append( ['2008',URL_MAIN + 'films-annees/2008/'] )
    liste.append( ['2007',URL_MAIN + 'films-annees/2007/'] )
    liste.append( ['2006',URL_MAIN + 'films-annees/2006/'] )
    liste.append( ['2005',URL_MAIN + 'films-annees/2005/'] )
    liste.append( ['2004',URL_MAIN + 'films-annees/2004/'] )
    liste.append( ['2003',URL_MAIN + 'films-annees/2003/'] )
    liste.append( ['2002',URL_MAIN + 'films-annees/2002/'] )
    liste.append( ['2001',URL_MAIN + 'films-annees/2001/'] )
    liste.append( ['2000',URL_MAIN + 'films-annees/2000/'] )
    liste.append( ['1999',URL_MAIN + 'films-annees/1999/'] )
    liste.append( ['1998',URL_MAIN + 'films-annees/1998/'] )
    liste.append( ['1997',URL_MAIN + 'films-annees/1997/'] )
    liste.append( ['1996',URL_MAIN + 'films-annees/1996/'] )
    liste.append( ['1995',URL_MAIN + 'films-annees/1995/'] )
    liste.append( ['1994',URL_MAIN + 'films-annees/1994/'] )
    liste.append( ['1993',URL_MAIN + 'films-annees/1993/'] )
    liste.append( ['1992',URL_MAIN + 'films-annees/1992/'] )
    liste.append( ['1991',URL_MAIN + 'films-annees/1991/'] )
    liste.append( ['1990',URL_MAIN + 'films-annees/1990/'] )
    liste.append( ['1989',URL_MAIN + 'films-annees/1989/'] )
    liste.append( ['1988',URL_MAIN + 'films-annees/1988/'] )
    liste.append( ['1987',URL_MAIN + 'films-annees/1987/'] )
    liste.append( ['1986',URL_MAIN + 'films-annees/1986/'] )
    liste.append( ['1985',URL_MAIN + 'films-annees/1985/'] )
    liste.append( ['1984',URL_MAIN + 'films-annees/1984/'] )
    liste.append( ['1983',URL_MAIN + 'films-annees/1983/'] )
    liste.append( ['1982',URL_MAIN + 'films-annees/1982/'] )
    liste.append( ['1981',URL_MAIN + 'films-annees/1981/'] )
    liste.append( ['1980',URL_MAIN + 'films-annees/1980/'] )
    liste.append( ['1979',URL_MAIN + 'films-annees/1979/'] )
    liste.append( ['1978',URL_MAIN + 'films-annees/1978/'] )
    liste.append( ['1977',URL_MAIN + 'films-annees/1977/'] )
    liste.append( ['1976',URL_MAIN + 'films-annees/1976/'] )
    liste.append( ['1975',URL_MAIN + 'films-annees/1975/'] )
    liste.append( ['1974',URL_MAIN + 'films-annees/1974/'] )
    liste.append( ['1973',URL_MAIN + 'films-annees/1973/'] )
    liste.append( ['1972',URL_MAIN + 'films-annees/1972/'] )
    liste.append( ['1971',URL_MAIN + 'films-annees/1971/'] )
    liste.append( ['1970',URL_MAIN + 'films-annees/1970/'] )
    liste.append( ['1969',URL_MAIN + 'films-annees/1969/'] )
    liste.append( ['1968',URL_MAIN + 'films-annees/1968/'] )
    liste.append( ['1967',URL_MAIN + 'films-annees/1967/'] )
    liste.append( ['1966',URL_MAIN + 'films-annees/1966/'] )
    liste.append( ['1965',URL_MAIN + 'films-annees/1965/'] )
    liste.append( ['1964',URL_MAIN + 'films-annees/1964/'] )
    liste.append( ['1963',URL_MAIN + 'films-annees/1963/'] )
    liste.append( ['1962',URL_MAIN + 'films-annees/1962/'] )
    liste.append( ['1961',URL_MAIN + 'films-annees/1961/'] )
    liste.append( ['1960',URL_MAIN + 'films-annees/1960/'] )
    liste.append( ['1959',URL_MAIN + 'films-annees/1959/'] )
    liste.append( ['1958',URL_MAIN + 'films-annees/1958/'] )
    liste.append( ['1957',URL_MAIN + 'films-annees/1957/'] )
    liste.append( ['1956',URL_MAIN + 'films-annees/1956/'] )
    liste.append( ['1955',URL_MAIN + 'films-annees/1955/'] )
    liste.append( ['1954',URL_MAIN + 'films-annees/1954/'] )
    liste.append( ['1953',URL_MAIN + 'films-annees/1953/'] )
    liste.append( ['1952',URL_MAIN + 'films-annees/1952/'] )
    liste.append( ['1951',URL_MAIN + 'films-annees/1951/'] )
    liste.append( ['1950',URL_MAIN + 'films-annees/1950/'] )
    liste.append( ['1940',URL_MAIN + 'films-annees/1940/'] )
    liste.append( ['1937',URL_MAIN + 'films-annees/1937/'] )
    liste.append( ['1936',URL_MAIN + 'films-annees/1936/'] )
    liste.append( ['1933',URL_MAIN + 'films-annees/1933/'] )
    liste.append( ['1931',URL_MAIN + 'films-annees/1931/'] )
    liste.append( ['1925',URL_MAIN + 'films-annees/1925/'] )
    
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
    liste.append( ['Cloudy.ec',URL_MAIN + 'plateformes/cloudy/'] )
    liste.append( ['DivxStage',URL_MAIN + 'plateformes/divxstage/'] )
    liste.append( ['Easywatch',URL_MAIN + 'langues/easywatch/'] )
    liste.append( ['Exashare',URL_MAIN + 'plateformes/exashare/'] )
    liste.append( ['FastVideo',URL_MAIN + 'plateformes/fastvideo/'] )
    liste.append( ['Firedrive',URL_MAIN + 'plateformes/firedrive/'] )
    liste.append( ['GigaUpload',URL_MAIN + 'plateformes/gigaupload/'] )
    liste.append( ['MadVID',URL_MAIN + 'plateformes/madvid/'] )
    liste.append( ['MailRu',URL_MAIN + 'plateformes/mailru/'] )
    liste.append( ['MixtureVideo',URL_MAIN + 'plateformes/mixturevideo/'] )
    liste.append( ['Moevideo',URL_MAIN + 'plateformes/moevideo/'] )
    liste.append( ['MovShare',URL_MAIN + 'plateformes/movshare/'] )
    liste.append( ['MyStream.la',URL_MAIN + 'plateformes/myStream-la/'] )
    liste.append( ['Netu',URL_MAIN + 'plateformes/netu/'] )
    liste.append( ['NovaMov',URL_MAIN + 'plateformes/novamov/'] )
    liste.append( ['NowVideo',URL_MAIN + 'plateformes/nowvideo/'] )
    liste.append( ['OneVideo',URL_MAIN + 'plateformes/onevideo/'] )
    liste.append( ['Purevideo',URL_MAIN + 'plateformes/purevideo/'] )
    liste.append( ['Putlocker',URL_MAIN + 'plateformes/putlocker/'] )
    liste.append( ['RapidVideo',URL_MAIN + 'plateformes/rapidvideo/'] )
    liste.append( ['SockShare',URL_MAIN + 'plateformes/sockshare/'] )
    liste.append( ['SpeedVideo',URL_MAIN + 'plateformes/speedvideo/'] )
    liste.append( ['TurboVid',URL_MAIN + 'plateformes/turbovid/'] )
    liste.append( ['UploadBB',URL_MAIN + 'plateformes/uploadbb/'] )
    liste.append( ['UploadHero',URL_MAIN + 'plateformes/uploadhero/'] )
    liste.append( ['UptoStream',URL_MAIN + 'plateformes/uptostream/'] )
    liste.append( ['VideoHut',URL_MAIN + 'plateformes/videohut/'] )
    liste.append( ['VideoMega',URL_MAIN + 'plateformes/videomega/'] )
    liste.append( ['VideoRaj',URL_MAIN + 'plateformes/videoraj/'] )
    liste.append( ['VideoWeed',URL_MAIN + 'plateformes/videoweed/'] )
    liste.append( ['Vidto',URL_MAIN + 'plateformes/vidto/'] )
    liste.append( ['VidZi.tv',URL_MAIN + 'plateformes/vidzi-tv/'] )
    liste.append( ['Vimple',URL_MAIN + 'plateformes/vimple/'] )
    liste.append( ['VK Player',URL_MAIN + 'plateformes/vk-player/'] )
    liste.append( ['Vodlocker',URL_MAIN + 'plateformes/vodlocker/'] )
    liste.append( ['Watching.to',URL_MAIN + 'plateformes/watching-to/'] )
    liste.append( ['Youwatch',URL_MAIN + 'plateformes/youwatch/'] ) 
    
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()
    
def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
            
    if sSearch:
        sUrl = sSearch.replace(' ','+')
        
        sDisp = oInputParameterHandler.getValue('disp')
       
        if (sDisp == 'search3'):#anime
            sUrl = sUrl + '&cat_id=45477'
        elif (sDisp == 'search2'):#serie
            sUrl = sUrl + '&cat_id=16989'
        elif (sDisp == 'search1'):#film
            sUrl = sUrl + '&cat_id=1'   
        else:#tout le reste
            sUrl = sUrl
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
    
    sHtmlContent = GetHtmlViaDns(sUrl)
    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request()

    #Regex trop lourd donc on fractionne
    aResult=[(False)]
    oParser = cParser()
    sPattern = '(<li (?:class="budur" )*data-hover="details" data-title=".+?<\/li>)'
    aResult2 = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult2[0] == False):
        oGui.addNone(SITE_IDENTIFIER)
    if (aResult2[0] == True):
        list = []
        sPattern = '<li (?:class="budur" )*data-hover="details" data-title="(.+?)" data-ozet="(.*?)" data-tur.+?<a href="(.+?)">.+?<img src="(.+?)" class="film-list-thumb".+?<div class="film-list-quality"><span>([0-9]{3,4}p)*<\/span>'
        for aEntry in aResult2[1]:
            aResult3 = oParser.parse(aEntry, sPattern)
            if (aResult3[0] == True):
                list = list + aResult3[1]
            
        aResult = [(True),list]
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = aEntry[0]
            if aEntry[4]:
                sTitle = '[' + aEntry[4]  + '] ' + sTitle
            sCom = aEntry[1]
            sUrl2 = aEntry[2]
            sThumb = aEntry[3]
            
            sCom = cUtil().removeHtmlTags(sCom)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            if '/series/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showMovies', sDisplayTitle,'', sThumb, sCom, oOutputParameterHandler)
            elif '/animes/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle,'', sThumb, sCom, oOutputParameterHandler)
            elif '/series-saison/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle,'', sThumb, sCom, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, sCom, oOutputParameterHandler)           
    
        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    sHtmlContent = GetHtmlViaDns(sUrl)
    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sPattern = '<li><a href="([^<>"]+?)" (?:class="active")*><i class="fa fa-film"><\/i>(.+?)<span><\/span><\/a><\/li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult    
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = sMovieTitle
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            sDisplayTitle = sDisplayTitle + '[COLOR teal] >> ' + aEntry[1] +' [/COLOR]'
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()  
def __checkForNextPage(sHtmlContent):
    
    sPattern = '<a class="next page-numbers" href="(.+?)">Suivant &raquo;</a>'
    oParser = cParser()
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
    
    sHtmlContent = GetHtmlViaDns(sUrl)
    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request()
    
    sHtmlContent = sHtmlContent.replace('</i> Untitled<span>', '')
    
    oParser = cParser()
    sPattern = '<li><a href="([^<>"]+?)" (?:class="active")*><i class="fa fa-film"><\/i>(.+?)<span><\/span><\/a><\/li>'
    #sPattern='<div id="burayaclass".+?onclick="getirframe\(\'(.+?)\',\'(.+?)\'\)".+?<div class="col-md-4.+?<p>(.+?)</p>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = sMovieTitle
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            sDisplayTitle = sDisplayTitle + '[COLOR teal] >> ' + aEntry[1] +' [/COLOR]'
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl',  aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters2', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)
        
    else:
        
        sPattern='<div id="burayaclass".+?onclick="getirframe\(\'(.+?)\',\'(.+?)\'\)".+?<div class="col-md-4.+?<p>(.+?)</p>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            total = len(aResult[1])
            dialog = cConfig().createDialog(SITE_NAME)
            for aEntry in aResult[1]:
                cConfig().updateDialog(dialog, total)
                if dialog.iscanceled():
                    break
                
                sTitle = sMovieTitle
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                sDisplayTitle = sDisplayTitle + '[COLOR teal] >> ' +  aEntry[2] +' [/COLOR]'
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', 'http://')
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oOutputParameterHandler.addParameter('sParam', aEntry[0])
                oOutputParameterHandler.addParameter('sBunuid', aEntry[1])
                
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)             
        
            cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()  

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    #sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sParam = oInputParameterHandler.getValue('sParam')
    sBunuid = oInputParameterHandler.getValue('sBunuid')

    sUrl = 'http://frenchstream.tv/wp-content/plugins/host-x-files/islem.php'
    postdata = 'islem=framegetir&param=' + sParam + '&bunuid=' + sBunuid
    sHtmlContent = GetHtmlViaDns(sUrl,postdata)
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    sPattern = '(?:(?:<script type="text\/javascript")|(?:<ifram[^<>]+?)) src=[\'"](https*:[^\'"]+?)[\'"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    
     
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
    
def showHosters2():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    sHtmlContent = GetHtmlViaDns(sUrl)
    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request()
    
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','').replace('<iframe src="http://www.facebook.com/','')
    #sHtmlContent = sHtmlContent.replace('http://videomega.tv/validateemb.php','')
    #sHtmlContent = sHtmlContent.replace('src="http://frenchstream.org/','')
    
    sPattern = '(?:(?:<script type="text\/javascript")|(?:<ifram[^<>]+?)) src=[\'"](https*:[^\'"]+?)[\'"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    
     
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
    
def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    sHtmlContent = GetHtmlViaDns(sUrl)
    #oRequestHandler = cRequestHandler(sUrl)
    #sHtmlContent = oRequestHandler.request()
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close() 
 
    sPattern = '<li style="[^<>]+?"><a href="([^<>"]+?)">(.+?)<\/a><\/li>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle+' - ' + aEntry[1]
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oGui.addTV(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)            
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
