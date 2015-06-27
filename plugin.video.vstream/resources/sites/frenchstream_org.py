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

SITE_IDENTIFIER = 'frenchstream_org'
SITE_NAME = 'FrenchStream.org'
SITE_DESC = 'Film en streaming, regarder film en direct, streaming vf regarder film gratuitement sur Frenchstream.org'

URL_MAIN = 'http://frenchstream.org/'

MOVIE_NEWS = ('http://frenchstream.org/films/', 'showMovies')
MOVIE_VIEWS = ('http://frenchstream.org/les-plus-vues/', 'showMovies')
MOVIE_COMMENTS = ('http://frenchstream.org/les-plus-commentes/', 'showMovies')
MOVIE_NOTES = ('http://frenchstream.org/les-mieux-notes/', 'showMovies')
MOVIE_GENRES = ('http://frenchstream.org/films-par-genre/', 'showGenre')
SERIE_SERIES = ('http://frenchstream.org/tv-series/', 'showMovies')

URL_SEARCH = ('http://frenchstream.org/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Nouveautés', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus Vues', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus Commentés', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les mieux Notés', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)
    
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
        
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showPlt', 'Films Plateforme', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series Nouveautés', 'series.png', oOutputParameterHandler)
    
            
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://frenchstream.org/?s='+sSearchText  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return  
    
    
def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
 
    sPattern = '<li><atitle=".+?" href="([^<]+)">(.+?)</a> <spanclass="mctagmap_count">(.+?)</span>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sTitle = aEntry[1]+' - '+aEntry[2]
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
           
    oGui.setEndOfDirectory()
        
def showPys():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Afghanistan','http://frenchstream.org/pays/afghanistan/'] )
    liste.append( ['Afrique du Sud','http://frenchstream.org/pays/afrique-du-sud/'] )
    liste.append( ['Algérie','http://frenchstream.org/pays/algerie/'] )
    liste.append( ['Allemangne','http://frenchstream.org/pays/allemangne/'] )
    liste.append( ['Angleterre','http://frenchstream.org/pays/angleterre/'] ) 
    liste.append( ['Argentine','http://frenchstream.org/pays/argentine/'] )
    liste.append( ['Australie','http://frenchstream.org/pays/australie/'] )
    liste.append( ['Autriche','http://frenchstream.org/pays/autriche/'] )
    liste.append( ['Belgique','http://frenchstream.org/pays/belgique/'] )
    liste.append( ['Brésil','http://frenchstream.org/pays/bresil/'] )
    liste.append( ['Britanique','http://frenchstream.org/pays/britannique/'] )
    liste.append( ['Bulgarie','http://frenchstream.org/pays/bulgarie/'] )
    liste.append( ['Cambodgien','http://frenchstream.org/pays/cambodgien/'] )
    liste.append( ['Cameroun','http://frenchstream.org/pays/cameroun/'] )
    liste.append( ['Canada','http://frenchstream.org/pays/canada/'] )
    liste.append( ['Chelie','http://frenchstream.org/pays/chelie/'] )
    liste.append( ['Chine','http://frenchstream.org/pays/chine/'] )
    liste.append( ['colombie','http://frenchstream.org/pays/colombie/'] )
    liste.append( ['Corée','http://frenchstream.org/pays/coree/'] )
    liste.append( ['Corée du sud','http://frenchstream.org/pays/coree-du-sud/'] )
    liste.append( ['Croitie','http://frenchstream.org/pays/croitie/'] )
    liste.append( ['Cuba','http://frenchstream.org/pays/cuba/'] )
    liste.append( ['Danemark','http://frenchstream.org/pays/danemark/'] )
    liste.append( ['Emarats arabes unis','http://frenchstream.org/pays/emarats-arabes-unis/'] )
    liste.append( ['Espagne','http://frenchstream.org/pays/espagne/'] )
    liste.append( ['Etats-Unis','http://frenchstream.org/pays/etats-unis/'] )
    liste.append( ['Finlande','http://frenchstream.org/pays/finlande/'] )
    liste.append( ['France','http://frenchstream.org/pays/france/'] )
    liste.append( ['Grec','http://frenchstream.org/pays/grec/'] )
    liste.append( ['Haiti','http://frenchstream.org/pays/haiti/'] )
    liste.append( ['Hollande','http://frenchstream.org/pays/hollande/'] )
    liste.append( ['Hong kong','http://frenchstream.org/pays/hong-kong/'] )
    liste.append( ['Hongrie','http://frenchstream.org/pays/hongrie/'] )
    liste.append( ['Inde','http://frenchstream.org/pays/inde/'] )
    liste.append( ['Indonésie','http://frenchstream.org/pays/indonesie/'] )
    liste.append( ['Iran','http://frenchstream.org/pays/iran/'] )
    liste.append( ['Irlande','http://frenchstream.org/pays/irlande/'] )
    liste.append( ['Islande','http://frenchstream.org/pays/islande/'] )
    liste.append( ['Israel','http://frenchstream.org/pays/israel/'] )
    liste.append( ['Italie','http://frenchstream.org/pays/italie/'] )
    liste.append( ['Japon','http://frenchstream.org/pays/japon/'] )
    liste.append( ['Kasakh','http://frenchstream.org/pays/kasakh/'] )
    liste.append( ['Kenya','http://frenchstream.org/pays/kenya/'] )
    liste.append( ['Koweit','http://frenchstream.org/pays/koweit/'] )
    liste.append( ['Liechtenstein','http://frenchstream.org/pays/liechtenstein/'] )
    liste.append( ['Lituanie','http://frenchstream.org/pays/lituanie/'] )
    liste.append( ['Lexembourg','http://frenchstream.org/pays/lexembourg/'] )
    liste.append( ['Malaisie','http://frenchstream.org/pays/malaisie/'] )
    liste.append( ['Mali','http://frenchstream.org/pays/mali/'] )
    liste.append( ['Maroc','http://frenchstream.org/pays/maroc/'] )
    liste.append( ['Mexique','http://frenchstream.org/pays/mexique/'] )
    liste.append( ['Monaco','http://frenchstream.org/pays/monaco/'] )
    liste.append( ['Népalais','http://frenchstream.org/pays/nepalais/'] )
    liste.append( ['Nigeria','http://frenchstream.org/pays/nigeria/'] )
    liste.append( ['NorvÃ¨ge','http://frenchstream.org/pays/norvege/'] )
    liste.append( ['Nouvelle-Zélande','http://frenchstream.org/pays/nouvelle-zelande/'] )
    liste.append( ['Palestine','http://frenchstream.org/pays/palestine/'] )
    liste.append( ['Panama','http://frenchstream.org/pays/panama/'] )
    liste.append( ['Paraguay','http://frenchstream.org/pays/paraguay/'] )
    liste.append( ['Pays-Bas','http://frenchstream.org/pays/pays-bas/'] )
    liste.append( ['Perou','http://frenchstream.org/pays/perou/'] )
    liste.append( ['Philippin','http://frenchstream.org/pays/philippin/'] )
    liste.append( ['Philippines','http://frenchstream.org/pays/philippines/'] )
    liste.append( ['Polongne','http://frenchstream.org/pays/polongne/'] )
    liste.append( ['Porto Rico','http://frenchstream.org/pays/porto-rico/'] )
    liste.append( ['Portugal','http://frenchstream.org/pays/portugal/'] )
    liste.append( ['Quatar','http://frenchstream.org/pays/quatar/'] )
    liste.append( ['Québec','http://frenchstream.org/pays/quebec/'] )
    liste.append( ['République tchÃ¨que','http://frenchstream.org/pays/republique-tcheque/'] )
    liste.append( ['Reunion','http://frenchstream.org/pays/reunion/'] )
    liste.append( ['Roumanie','http://frenchstream.org/pays/roumanie/'] )
    liste.append( ['Russie','http://frenchstream.org/pays/russie/'] )
    liste.append( ['Saoudien','http://frenchstream.org/pays/saoudien/'] )
    liste.append( ['Sénégal','http://frenchstream.org/pays/senegale/'] )
    liste.append( ['Serbie','http://frenchstream.org/pays/serbie/'] )
    liste.append( ['Singapour','http://frenchstream.org/pays/serbie/'] )
    liste.append( ['Slovene','http://frenchstream.org/pays/serbie/'] )
    liste.append( ['Sud-Créen','http://frenchstream.org/pays/sud-coreen/'] )
    liste.append( ['SuÃ¨de','http://frenchstream.org/pays/suede/'] )
    liste.append( ['Suisse','http://frenchstream.org/pays/suisse/'] )
    liste.append( ['Taiwan','http://frenchstream.org/pays/taiwan/'] )
    liste.append( ['Tchad','http://frenchstream.org/pays/tchad/'] )
    liste.append( ['Tchécoslovaquie','http://frenchstream.org/pays/tchecoslovaquie/'] )
    liste.append( ['TchÃ¨que','http://frenchstream.org/pays/tcheque/'] )
    liste.append( ['Thailand','http://frenchstream.org/pays/thailand/'] )
    liste.append( ['Tunisie','http://frenchstream.org/pays/tunisie/'] )
    liste.append( ['Turquie','http://frenchstream.org/pays/turquie/'] )
    liste.append( ['Ukraine','http://frenchstream.org/pays/ukraine/'] )
    liste.append( ['Uruguay','http://frenchstream.org/pays/uruguay/'] )
    liste.append( ['Vietnam','http://frenchstream.org/pays/vietnam/'] )
    liste.append( ['Yougoslavie','http://frenchstream.org/pays/yougoslavie/'] )  
     
    
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
    liste.append( ['1925','http://frenchstream.org/annees/1925/'] )
    liste.append( ['1931','http://frenchstream.org/annees/1931/'] )
    liste.append( ['1933','http://frenchstream.org/annees/1933/'] )
    liste.append( ['1936','http://frenchstream.org/annees/1936/'] )
    liste.append( ['1937','http://frenchstream.org/annees/1937/'] )
    liste.append( ['1940','http://frenchstream.org/annees/1940/'] )
    liste.append( ['1945','http://frenchstream.org/annees/1945/'] )
    liste.append( ['1950','http://frenchstream.org/annees/1950/'] )
    liste.append( ['1951','http://frenchstream.org/annees/1951/'] )
    liste.append( ['1952','http://frenchstream.org/annees/1952/'] )
    liste.append( ['1953','http://frenchstream.org/annees/1953/'] )
    liste.append( ['1954','http://frenchstream.org/annees/1954/'] )
    liste.append( ['1955','http://frenchstream.org/annees/1955/'] )
    liste.append( ['1956','http://frenchstream.org/annees/1956/'] )
    liste.append( ['1957','http://frenchstream.org/annees/1957/'] )
    liste.append( ['1959','http://frenchstream.org/annees/1959/'] )
    liste.append( ['1960','http://frenchstream.org/annees/1960/'] )
    liste.append( ['1961','http://frenchstream.org/annees/1961/'] )
    liste.append( ['1962','http://frenchstream.org/annees/1962/'] )
    liste.append( ['1963','http://frenchstream.org/annees/1963/'] )
    liste.append( ['1964','http://frenchstream.org/annees/1964/'] )
    liste.append( ['1966','http://frenchstream.org/annees/1966/'] )
    liste.append( ['1967','http://frenchstream.org/annees/1967/'] )
    liste.append( ['1968','http://frenchstream.org/annees/1968/'] )
    liste.append( ['1969','http://frenchstream.org/annees/1969/'] )
    liste.append( ['1970','http://frenchstream.org/annees/1970/'] )
    liste.append( ['1971','http://frenchstream.org/annees/1971/'] )
    liste.append( ['1972','http://frenchstream.org/annees/1972/'] )
    liste.append( ['1973','http://frenchstream.org/annees/1973/'] )
    liste.append( ['1974','http://frenchstream.org/annees/1974/'] )
    liste.append( ['1975','http://frenchstream.org/annees/1975/'] )
    liste.append( ['1976','http://frenchstream.org/annees/1976/'] )
    liste.append( ['1977','http://frenchstream.org/annees/1977/'] )
    liste.append( ['1978','http://frenchstream.org/annees/1978/'] )
    liste.append( ['1979','http://frenchstream.org/annees/1979/'] )
    liste.append( ['1980','http://frenchstream.org/annees/1980/'] )
    liste.append( ['1981','http://frenchstream.org/annees/1981/'] )
    liste.append( ['1982','http://frenchstream.org/annees/1982/'] )
    liste.append( ['1983','http://frenchstream.org/annees/1983/'] )
    liste.append( ['1984','http://frenchstream.org/annees/1984/'] )
    liste.append( ['1985','http://frenchstream.org/annees/1985/'] )
    liste.append( ['1986','http://frenchstream.org/annees/1986/'] )
    liste.append( ['1987','http://frenchstream.org/annees/1987/'] )
    liste.append( ['1988','http://frenchstream.org/annees/1988/'] )
    liste.append( ['1989','http://frenchstream.org/annees/1989/'] )
    liste.append( ['1990','http://frenchstream.org/annees/1990/'] )
    liste.append( ['1991','http://frenchstream.org/annees/1991/'] )
    liste.append( ['1992','http://frenchstream.org/annees/1992/'] )
    liste.append( ['1993','http://frenchstream.org/annees/1993/'] )
    liste.append( ['1994','http://frenchstream.org/annees/1994/'] )
    liste.append( ['1995','http://frenchstream.org/annees/1995/'] )
    liste.append( ['1996','http://frenchstream.org/annees/1996/'] )
    liste.append( ['1997','http://frenchstream.org/annees/1997/'] )
    liste.append( ['1998','http://frenchstream.org/annees/1998/'] )
    liste.append( ['1999','http://frenchstream.org/annees/1999/'] )
    liste.append( ['2000','http://frenchstream.org/annees/2000/'] )
    liste.append( ['2001','http://frenchstream.org/annees/2001/'] )
    liste.append( ['2002','http://frenchstream.org/annees/2002/'] )
    liste.append( ['2003','http://frenchstream.org/annees/2003/'] )
    liste.append( ['2004','http://frenchstream.org/annees/2004/'] )
    liste.append( ['2005','http://frenchstream.org/annees/2005/'] )
    liste.append( ['2006','http://frenchstream.org/annees/2006/'] )
    liste.append( ['2007','http://frenchstream.org/annees/2007/'] )
    liste.append( ['2008','http://frenchstream.org/annees/2008/'] )
    liste.append( ['2009','http://frenchstream.org/annees/2009/'] )
    liste.append( ['2010','http://frenchstream.org/annees/2010/'] )
    liste.append( ['2011','http://frenchstream.org/annees/2011/'] )
    liste.append( ['2012','http://frenchstream.org/annees/2012/'] )
    liste.append( ['2013','http://frenchstream.org/annees/2013/'] )
    liste.append( ['2014','http://frenchstream.org/annees/2014/'] )
    liste.append( ['2015','http://frenchstream.org/annees/2015/'] )
 
    
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
    liste.append( ['1080p','http://frenchstream.org/qualites/1080p/'] )   
    liste.append( ['720p','http://frenchstream.org/qualites/720p/'] )
    liste.append( ['BDRip','http://frenchstream.org/qualites/BDRip/'] )
    liste.append( ['BRRip','http://frenchstream.org/qualites/BRRip/'] )
    liste.append( ['CAMRip','http://frenchstream.org/qualites/CAMRip/'] )
    liste.append( ['DVDRip','http://frenchstream.org/qualites/DVDRip/'] )
    liste.append( ['DVDSCR','http://frenchstream.org/qualites/DVDSCR/'] )
    liste.append( ['HDRip','http://frenchstream.org/qualites/HDRip/'] )
    liste.append( ['HDTV','http://frenchstream.org/qualites/HDTV/'] )
    liste.append( ['PDTV','http://frenchstream.org/qualites/PDTV/'] )
    liste.append( ['R6','http://frenchstream.org/qualites/R6/'] )
    liste.append( ['TS MD','http://frenchstream.org/qualites/ts-md/'] )
    liste.append( ['TVRip','http://frenchstream.org/qualites/TVRip/'] )
    liste.append( ['VHSRip','http://frenchstream.org/qualites/VHSRip/'] )
    liste.append( ['VOBRIP','http://frenchstream.org/qualites/VOBRIP/'] )
    liste.append( ['WEB-DL','http://frenchstream.org/qualites/web-dl/'] )
    liste.append( ['WEBRIP','http://frenchstream.org/qualites/WEBRIP/'] )
    
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
    liste.append( ['FRENCH','http://frenchstream.org/langues/french/'] )
    liste.append( ['VO','http://frenchstream.org/langues/vo/'] )
    liste.append( ['VOSTFR','http://frenchstream.org/langues/vostfr/'] ) 
    
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
    liste.append( ['Cloudy.ec','http://frenchstream.org/plateformes/cloudy/'] )
    liste.append( ['DivxStage','http://frenchstream.org/plateformes/divxstage/'] )
    liste.append( ['Easywatch','http://frenchstream.org/langues/easywatch/'] )
    liste.append( ['Exashare','http://frenchstream.org/plateformes/exashare/'] )
    liste.append( ['FastVideo','http://frenchstream.org/plateformes/fastvideo/'] )
    liste.append( ['Firedrive','http://frenchstream.org/plateformes/firedrive/'] )
    liste.append( ['GigaUpload','http://frenchstream.org/plateformes/gigaupload/'] )
    liste.append( ['MadVID','http://frenchstream.org/plateformes/madvid/'] )
    liste.append( ['MailRu','http://frenchstream.org/plateformes/mailru/'] )
    liste.append( ['MixtureVideo','http://frenchstream.org/plateformes/mixturevideo/'] )
    liste.append( ['Moevideo','http://frenchstream.org/plateformes/moevideo/'] )
    liste.append( ['MovShare','http://frenchstream.org/plateformes/movshare/'] )
    liste.append( ['MyStream.la','http://frenchstream.org/plateformes/myStream-la/'] )
    liste.append( ['Netu','http://frenchstream.org/plateformes/netu/'] )
    liste.append( ['NovaMov','http://frenchstream.org/plateformes/novamov/'] )
    liste.append( ['NowVideo','http://frenchstream.org/plateformes/nowvideo/'] )
    liste.append( ['OneVideo','http://frenchstream.org/plateformes/onevideo/'] )
    liste.append( ['Purevideo','http://frenchstream.org/plateformes/purevideo/'] )
    liste.append( ['Putlocker','http://frenchstream.org/plateformes/putlocker/'] )
    liste.append( ['RapidVideo','http://frenchstream.org/plateformes/rapidvideo/'] )
    liste.append( ['SockShare','http://frenchstream.org/plateformes/sockshare/'] )
    liste.append( ['SpeedVideo','http://frenchstream.org/plateformes/speedvideo/'] )
    liste.append( ['TurboVid','http://frenchstream.org/plateformes/turbovid/'] )
    liste.append( ['UploadBB','http://frenchstream.org/plateformes/uploadbb/'] )
    liste.append( ['UploadHero','http://frenchstream.org/plateformes/uploadhero/'] )
    liste.append( ['UptoStream','http://frenchstream.org/plateformes/uptostream/'] )
    liste.append( ['VideoHut','http://frenchstream.org/plateformes/videohut/'] )
    liste.append( ['VideoMega','http://frenchstream.org/plateformes/videomega/'] )
    liste.append( ['VideoRaj','http://frenchstream.org/plateformes/videoraj/'] )
    liste.append( ['VideoWeed','http://frenchstream.org/plateformes/videoweed/'] )
    liste.append( ['Vidto','http://frenchstream.org/plateformes/vidto/'] )
    liste.append( ['VidZi.tv','http://frenchstream.org/plateformes/vidzi-tv/'] )
    liste.append( ['Vimple','http://frenchstream.org/plateformes/vimple/'] )
    liste.append( ['VK Player','http://frenchstream.org/plateformes/vk-player/'] )
    liste.append( ['Vodlocker','http://frenchstream.org/plateformes/vodlocker/'] )
    liste.append( ['Watching.to','http://frenchstream.org/plateformes/watching-to/'] )
    liste.append( ['Youwatch','http://frenchstream.org/plateformes/youwatch/'] ) 
    
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<span class="likeThis">', '').replace('</span>','')
    sPattern = '<div.*?class="moviefilm"><a.*?href="([^<]+)">.+?<img.*?src="([^<]+)" alt="(.+?)".+?>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == False):
        oGui.addNone(SITE_IDENTIFIER)
        return False

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            #sTitle = aEntry[2]+' - [COLOR azure]'+aEntry[3]+'[/COLOR]'
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[1]))
            if '/tv-series' in sUrl or '/tv-series' in aEntry[0]:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', aEntry[2],'', aEntry[1], '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', aEntry[2], '', aEntry[1], '', oOutputParameterHandler)           
    
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
    sUrl = sUrl+'/100/'
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<strong>Téléchargement VOSTFR','').replace('<strong>Téléchargement VF','').replace('<strong>Téléchargement','')
 
    sPattern = '<ahref="([^<]+)"><span>(.+?)</span></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = sMovieTitle+' - '+aEntry[1]
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, '', oOutputParameterHandler)            
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<a class="page larger" href="(.+?)">'
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

    oRequestHandler = cRequestHandler(sUrl + '/100/')#Modification de l'adresse pr afficher tout les liens
    sHtmlContent = oRequestHandler.request()
    
    #sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/plugins/like.php','').replace('<iframe src="http://www.facebook.com/plugins/likebox.php','')
    
    a = sUrl.replace('/','\/')
    oParser = cParser()
    
    #quelques infos en plus
    annee = ""
    qualite = ""
    comm = ""
    sPattern = '<div class="konuozet">(.+?)<\/div>.+?<span>Ann..es<\/span>: <a href="[^<>]+?">([0-9]{4})<\/a>.+?<span>Qualit..s<\/span>: <a href="[^<>]+?">(.+?)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        annee = aResult[1][0][1]
        qualite = aResult[1][0][2]
        comm = aResult[1][0][0].replace('<p>','')
    
    #Recuperation des liens
    sPattern = '<a href="(' + a + '.*?)"><span>(.+?)<\/span><\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #print aResult    
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sHoster = cHosterGui().checkHoster(aEntry[1].lower())
            if (sHoster != False):
                sTitle = sMovieTitle + ' (' + annee + ') [COLOR coral]['+ qualite + '][/COLOR] - [COLOR azure]'+aEntry[1]+'[/COLOR]'
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumbnail, comm, oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()  

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','').replace('<iframe src="http://www.facebook.com/','')
    sHtmlContent = sHtmlContent.replace('http://videomega.tv/validateemb.php','')
    sHtmlContent = sHtmlContent.replace('src="http://frenchstream.org/','')
        
    sPattern = '(?:(?:<script type="text\/javascript")|(?:<ifram[^<>]+?)) src=[\'"](http:[^\'"]+?)[\'"]'
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
            
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
