#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import urllib2,urllib,re

SITE_IDENTIFIER = 'voirfilms_org'
SITE_NAME = 'VoirFilms'
SITE_DESC = 'Films, Séries & Animés en Streaming'
 
URL_MAIN = 'http://www.voirfilms.biz/'

MOVIE_MOVIE = (URL_MAIN + 'alphabet', 'showAlpha')
MOVIE_NEWS = (URL_MAIN + 'film-en-streaming', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')
MOVIE_ANNEES = (URL_MAIN + 'films/' , 'showAnnees')

SERIE_SERIES = (URL_MAIN + 'series/alphabet/', 'showAlpha')
SERIE_NEWS = (URL_MAIN + 'series/page-1', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'series', 'showGenres')
SERIE_ANNEES = (URL_MAIN + 'series/', 'showAnnees')

ANIM_ANIMS = (URL_MAIN + 'animes/alphabet/', 'AlphaSearch')
ANIM_NEWS = (URL_MAIN + 'animes/', 'showMovies')
  
URL_SEARCH = ('', 'showMovies')
#FUNCTION_SEARCH = 'showMovies'
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'

def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films (Par ordre Alphabétique)', 'films_az.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par Années)', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries (Par ordre Alphabétique)', 'series_az.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par Années)', 'series.png', oOutputParameterHandler)
	
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers ajouts)', 'animes_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés (Par ordre Alphabétique)', 'animes_az.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(sSearchText)
        oGui.setEndOfDirectory()
        return
        
def AlphaSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    dialog = cConfig().createDialog(SITE_NAME)
    
    for i in range(0,27) :
        cConfig().updateDialog(dialog, 36)
        
        if (i > 0):
            sTitle = chr(64+i)
        else:
            sTitle = '09'
            
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + sTitle.upper())
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]'+ sTitle +'[/COLOR]', 'az.png', oOutputParameterHandler)
        
    cConfig().finishDialog(dialog)
    
    oGui.setEndOfDirectory()           
   
def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'series' in sUrl:
        code = URL_MAIN + 'series/'
    else:
        code = URL_MAIN 
 
    liste = []
    liste.append( ['Action',code + 'action_1'] )
    liste.append( ['Animation',code + 'animation_1'] )
    liste.append( ['Arts Martiaux',code + 'arts-martiaux_1'] )
    liste.append( ['Aventure',code + 'aventure_1'] )
    liste.append( ['Biopic',code + 'biopic_1'] )
    liste.append( ['Comédie',code + 'film-comedie'] )
    liste.append( ['Comédie Dramatique',code + 'comedie-dramatique_1'] )
    liste.append( ['Documentaire',code + 'documentaire_1'] )
    liste.append( ['Drame',code + 'drame_1'] )
    liste.append( ['Epouvante Horreur',code + 'epouvante-horreur_1'] )
    liste.append( ['Erotique',code + 'erotique_1'] )
    liste.append( ['Espionnage',code + 'espionnage_1'] )
    liste.append( ['Fantastique',code + 'fantastique_1'] )
    liste.append( ['Guerre',code + 'guerre_1'] )
    liste.append( ['Historique',code + 'historique_1'] )
    liste.append( ['Musical',code + 'musical_1'] )
    liste.append( ['Policier',code + 'policier_1'] )
    liste.append( ['Romance',code + 'romance_1'] )
    liste.append( ['Science Fiction',code + 'science-fiction_1'] )
    liste.append( ['Série',code + 'series_1'] )
    liste.append( ['Thriller',code + 'thriller_1'] )
    liste.append( ['Western',code + 'western_1'] )
    liste.append( ['Non classé',code + 'non-classe_1'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def showAnnees():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
	
    liste = []
    liste.append( ['2017',sUrl + 'annee-2017'] )
    liste.append( ['2016',sUrl + 'annee-2016'] )
    liste.append( ['2015',sUrl + 'annee-2015'] )
    liste.append( ['2014',sUrl + 'annee-2014'] )
    liste.append( ['2013',sUrl + 'annee-2013'] )
    liste.append( ['2012',sUrl + 'annee-2012'] )
    liste.append( ['2011',sUrl + 'annee-2011'] )
    liste.append( ['2010',sUrl + 'annee-2010'] )
    liste.append( ['2009',sUrl + 'annee-2009'] )
    liste.append( ['2008',sUrl + 'annee-2008'] )
    liste.append( ['2007',sUrl + 'annee-2007'] )
    liste.append( ['2006',sUrl + 'annee-2006'] )
    liste.append( ['2005',sUrl + 'annee-2005'] )
    liste.append( ['2004',sUrl + 'annee-2004'] )
    liste.append( ['2003',sUrl + 'annee-2003'] )
    liste.append( ['2002',sUrl + 'annee-2002'] )
    liste.append( ['2001',sUrl + 'annee-2001'] )
    liste.append( ['2000',sUrl + 'annee-2000'] )
    liste.append( ['1999',sUrl + 'annee-1999'] )
    liste.append( ['1998',sUrl + 'annee-1998'] )
    liste.append( ['1997',sUrl + 'annee-1997'] )
    liste.append( ['1996',sUrl + 'annee-1996'] )
    liste.append( ['1995',sUrl + 'annee-1995'] )
    liste.append( ['1994',sUrl + 'annee-1994'] )
    liste.append( ['1993',sUrl + 'annee-1993'] )
    liste.append( ['1992',sUrl + 'annee-1992'] )
    liste.append( ['1991',sUrl + 'annee-1991'] )
    liste.append( ['1990',sUrl + 'annee-1990'] )
    liste.append( ['1989',sUrl + 'annee-1989'] )
    liste.append( ['1988',sUrl + 'annee-1988'] )
    liste.append( ['1987',sUrl + 'annee-1987'] )
    liste.append( ['1986',sUrl + 'annee-1986'] )
    liste.append( ['1985',sUrl + 'annee-1985'] )
    liste.append( ['1984',sUrl + 'annee-1984'] )
    liste.append( ['1983',sUrl + 'annee-1983'] )
    liste.append( ['1982',sUrl + 'annee-1982'] )
    liste.append( ['1981',sUrl + 'annee-1981'] )
    liste.append( ['1980',sUrl + 'annee-1980'] )
    liste.append( ['1979',sUrl + 'annee-1979'] )
    liste.append( ['1978',sUrl + 'annee-1978'] )
    liste.append( ['1977',sUrl + 'annee-1977'] )
    liste.append( ['1976',sUrl + 'annee-1976'] )
    liste.append( ['1975',sUrl + 'annee-1975'] )
    liste.append( ['1974',sUrl + 'annee-1974'] )
    liste.append( ['1973',sUrl + 'annee-1973'] )
    liste.append( ['1972',sUrl + 'annee-1972'] )
    liste.append( ['1971',sUrl + 'annee-1971'] )
    liste.append( ['1970',sUrl + 'annee-1970'] )
    liste.append( ['1969',sUrl + 'annee-1969'] )
    liste.append( ['1968',sUrl + 'annee-1968'] )
    liste.append( ['1967',sUrl + 'annee-1967'] )
    liste.append( ['1966',sUrl + 'annee-1966'] )
    liste.append( ['1965',sUrl + 'annee-1965'] )
    liste.append( ['1964',sUrl + 'annee-1964'] )
    liste.append( ['1963',sUrl + 'annee-1963'] )
    liste.append( ['1962',sUrl + 'annee-1962'] )
    liste.append( ['1961',sUrl + 'annee-1961'] )
    liste.append( ['1960',sUrl + 'annee-1960'] )
    liste.append( ['1959',sUrl + 'annee-1959'] )
    liste.append( ['1958',sUrl + 'annee-1958'] )
    liste.append( ['1957',sUrl + 'annee-1957'] )
    liste.append( ['1956',sUrl + 'annee-1956'] )
    liste.append( ['1955',sUrl + 'annee-1955'] )
    liste.append( ['1954',sUrl + 'annee-1954'] )
    liste.append( ['1953',sUrl + 'annee-1953'] )
    liste.append( ['1952',sUrl + 'annee-1952'] )
    liste.append( ['1951',sUrl + 'annee-1951'] )
    liste.append( ['1950',sUrl + 'annee-1950'] )
    liste.append( ['1949',sUrl + 'annee-1949'] )
    liste.append( ['1948',sUrl + 'annee-1948'] )
    liste.append( ['1947',sUrl + 'annee-1947'] )
    liste.append( ['1946',sUrl + 'annee-1946'] )
    liste.append( ['1945',sUrl + 'annee-1945'] )
    liste.append( ['1944',sUrl + 'annee-1944'] )
    liste.append( ['1943',sUrl + 'annee-1943'] )
    liste.append( ['1942',sUrl + 'annee-1942'] )
    liste.append( ['1941',sUrl + 'annee-1941'] )
    liste.append( ['1940',sUrl + 'annee-1940'] )
    liste.append( ['1939',sUrl + 'annee-1939'] )
    liste.append( ['1938',sUrl + 'annee-1938'] )
    liste.append( ['1937',sUrl + 'annee-1937'] )
    liste.append( ['1936',sUrl + 'annee-1936'] )
    liste.append( ['1935',sUrl + 'annee-1935'] )
    liste.append( ['1934',sUrl + 'annee-1934'] )
    liste.append( ['1933',sUrl + 'annee-1933'] )
    liste.append( ['1932',sUrl + 'annee-1932'] )
    liste.append( ['1931',sUrl + 'annee-1931'] )
    liste.append( ['1930',sUrl + 'annee-1930'] )
    liste.append( ['1929',sUrl + 'annee-1929'] )
    #liste.append( ['1928',sUrl + 'annee-1928'] )
    liste.append( ['1927',sUrl + 'annee-1927'] )
    liste.append( ['1926',sUrl + 'annee-1926'] )
    liste.append( ['1925',sUrl + 'annee-1925'] )
    liste.append( ['1924',sUrl + 'annee-1924'] )
    liste.append( ['1923',sUrl + 'annee-1923'] )
    liste.append( ['1922',sUrl + 'annee-1922'] )
    liste.append( ['1921',sUrl + 'annee-1921'] )
    liste.append( ['1920',sUrl + 'annee-1920'] )
    liste.append( ['1919',sUrl + 'annee-1919'] )
    liste.append( ['1918',sUrl + 'annee-1918'] )
    liste.append( ['1917',sUrl + 'annee-1917'] )
    #liste.append( ['1916',sUrl + 'annee-1916'] )
    liste.append( ['1915',sUrl + 'annee-1915'] )
    liste.append( ['1914',sUrl + 'annee-1914'] )
    liste.append( ['1913',sUrl + 'annee-1913'] )
	
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()

def showAlpha():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if 'series' in sUrl:
        code = 'series/alphabet/'
    else:
        code = 'alphabet/' 
 
    liste = []
    liste.append( ['0',URL_MAIN + code + '0'] )
    liste.append( ['1',URL_MAIN + code + '1'] )
    liste.append( ['2',URL_MAIN + code + '2'] )
    liste.append( ['3',URL_MAIN + code + '3'] )
    liste.append( ['4',URL_MAIN + code + '4'] )
    liste.append( ['5',URL_MAIN + code + '5'] )
    liste.append( ['6',URL_MAIN + code + '6'] )
    liste.append( ['7',URL_MAIN + code + '7'] )
    liste.append( ['8',URL_MAIN + code + '8'] )
    liste.append( ['9',URL_MAIN + code + '9'] )
    liste.append( ['A',URL_MAIN + code + 'A'] )
    liste.append( ['B',URL_MAIN + code + 'B'] )
    liste.append( ['C',URL_MAIN + code + 'C'] )
    liste.append( ['D',URL_MAIN + code + 'D'] )
    liste.append( ['E',URL_MAIN + code + 'E'] )
    liste.append( ['F',URL_MAIN + code + 'F'] )
    liste.append( ['G',URL_MAIN + code + 'G'] )
    liste.append( ['H',URL_MAIN + code + 'H'] )
    liste.append( ['I',URL_MAIN + code + 'I'] )
    liste.append( ['J',URL_MAIN + code + 'J'] )
    liste.append( ['K',URL_MAIN + code + 'K'] )
    liste.append( ['L',URL_MAIN + code + 'L'] )
    liste.append( ['M',URL_MAIN + code + 'M'] )
    liste.append( ['N',URL_MAIN + code + 'N'] )
    liste.append( ['O',URL_MAIN + code + 'O'] )
    liste.append( ['P',URL_MAIN + code + 'P'] )
    liste.append( ['Q',URL_MAIN + code + 'Q'] )
    liste.append( ['R',URL_MAIN + code + 'R'] )
    liste.append( ['S',URL_MAIN + code + 'S'] )
    liste.append( ['T',URL_MAIN + code + 'T'] )
    liste.append( ['U',URL_MAIN + code + 'U'] )
    liste.append( ['V',URL_MAIN + code + 'V'] )
    liste.append( ['W',URL_MAIN + code + 'W'] )
    liste.append( ['X',URL_MAIN + code + 'X'] )
    liste.append( ['Y',URL_MAIN + code + 'Y'] )
    liste.append( ['Z',URL_MAIN + code + 'Z'] )
    
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Lettre [COLOR coral]'+ sTitle +'[/COLOR]', 'az.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()

    if sSearch:
        #on redecode la recherche codé il y a meme pas une seconde par l'addon
        sSearch = urllib2.unquote(sSearch)

        pdata = 'action=recherche&story=' + sSearch
        
        oRequest = cRequestHandler(URL_MAIN + 'recherche')
        oRequest.setRequestType(1)
        oRequest.addHeaderEntry('User-Agent',UA)
        oRequest.addHeaderEntry('Host','www.voirfilms.biz')
        oRequest.addHeaderEntry('Referer',URL_MAIN)
        oRequest.addHeaderEntry('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequest.addHeaderEntry('Accept-Language','fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequest.addHeaderEntry('Content-Type','application/x-www-form-urlencoded')
        oRequest.addParametersLine(pdata)
        
        sHtmlContent = oRequest.request()
        
        sPattern = '<div class="imagefilm">.+?<img src="(.+?)".+?<a href="([^<>]+?)".+?titreunfilm" style="width:145px;"> *(.+?) *<\/div>'
 
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
        if 'animes/' in sUrl:
            sPattern = '<div class="imagefilm">.+?<a href="([^<>]+?)".+?<img src="(.+?)".+?titreunfilm" style="width:145px;">(.+?)<\/div>'
            type = '2'
        else:
            sPattern = '<div class="imagefilm">.+?<img src="(.+?)".+?<a href="([^<>]+?)".+?titreunfilm" style="width:145px;">(.+?)<\/div>'
            type = '1'
            
    sHtmlContent = sHtmlContent.replace('\n','')

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if not (aResult[0] == False):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
 
            if type == '2':
               sPicture = str(aEntry[1])
               sUrl = str(aEntry[0])
            else:
                sPicture = str(aEntry[0])
                sUrl = str(aEntry[1])
                
            sTitle = cUtil().unescape(aEntry[2])
            
            if not 'http' in sPicture:
                sPicture = URL_MAIN + sPicture
          
            if not 'http' in sUrl:
                sUrl = URL_MAIN + sUrl
           
            #not found better way
            #sTitle = unicode(sTitle, errors='replace')
            #sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')
            
            #Vstream don't work with unicode url for the moment
            sPicture = unicode(sPicture,"UTF-8")
            sPicture = sPicture.encode('ascii', 'ignore').decode('ascii')
            #sPicture=sPicture.decode('utf8')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', sPicture)
 
            if 'serie' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sTitle, sPicture, sPicture, '', oOutputParameterHandler)
            elif 'anime' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sTitle, sPicture, sPicture, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, sPicture, sPicture, '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
           
        if not sSearch:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = "<a href='([^'<>]+?)' rel='nofollow'>suiv »</a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        next = aResult[1][0].replace(URL_MAIN, '')
        return URL_MAIN + next
 
    return False

def showHosters():
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    # patch for unicode url
    sUrl = urllib.quote(sUrl,':/')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    sPattern = '<a href="([^<>"]+?)" target="filmPlayer".+?class="([a-zA-Z]+)L"><\/span> *<\/div><span class="gras">.+?>(.+?)<\/span>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sHost = str(aEntry[2]).replace('&nbsp;','')
            #sTitle = '(' + str(aEntry[1]) + ') [' + sHost + '] ' + sMovieTitle
            sTitle = '%s [%s] [COLOR coral]%s[/COLOR]' %(sMovieTitle, str(aEntry[1]).upper(), sHost)
            sUrl = aEntry[0].replace('https://', 'http://')
            #print sUrl
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
 
            oGui.addMovie(SITE_IDENTIFIER, 'showHostersLink', sDisplayTitle , sThumbnail, sThumbnail, '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
       
    oGui.setEndOfDirectory()   

def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if '-saison-' in sUrl or '/anime/' in sUrl:
        sPattern = '<li class="description132"><a class="n_episode2" title=".+?" href="(.+?)">(.+?)<\/a><\/li>'
    else:
        sMovieTitle = ''
        sPattern = '<div class="unepetitesaisons"> +<a href="(.+?)" title="(.+?)"> +<div class="saisonimage">'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sEp = str(aEntry[1])
            sEp = re.sub('<span>(.+?)<\/span>','Episode \\1', str(sEp))
                
            sTitle = sMovieTitle + sEp
            sUrl = str(aEntry[0])
            if 'http' not in sUrl:
                sUrl = URL_MAIN + sUrl
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
 
            if '-episode-' in aEntry[0] or '/anime/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, sThumbnail, sThumbnail, '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, sThumbnail, sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)    

    oGui.setEndOfDirectory()

def showHostersLink():
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    #On recupere la redirection
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-agent',UA)
    oRequestHandler.addHeaderEntry('Referer',URL_MAIN)
    sHtmlContent = oRequestHandler.request()
    redirection_target = oRequestHandler.getRealUrl() 
    
    #opener = urllib2.build_opener(NoRedirection)
    #opener.addheaders = [('User-agent', UA)]
    #response = opener.open(sUrl)
    #sHtmlContent = response.read()
    #if response.code == 302:
    #    redirection_target = response.headers['Location']
    #response.close()
    
    #cConfig().log('red > ' + redirection_target)
    #cConfig().log('cod > ' + sHtmlContent)
    
    #attention fake redirection
    #sUrl = redirection_target
    m = re.search(r'url=([^"]+)',sHtmlContent)
    if m:
        sUrl = m.group(1)
        
    #Modifications
    sUrl = sUrl.replace('1wskdbkp.xyz','youwatch.org')
    if '1fichier' in sUrl:
        sUrl = re.sub('(http.+?\?link=)','https://1fichier.com/?',sUrl)

    sHosterUrl = sUrl
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 
   
    oGui.setEndOfDirectory()
