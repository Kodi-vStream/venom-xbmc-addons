#-*- coding: utf-8 -*-
#Venom.
#
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib.parser import cParser
from resources.lib.util import cUtil

import re,urllib2,urllib
import base64

SITE_IDENTIFIER = 'megastream'
SITE_NAME = 'Mega-stream'
SITE_DESC = 'Films, Series, Animes HD'

URL_MAIN = 'http://mega-stream.fr/'

MOVIE_NEWS = (URL_MAIN +'accueil-films', 'showMovies')
MOVIE_MOVIE = (URL_MAIN +'accueil-films', 'showMovies')
MOVIE_HD = (URL_MAIN +'accueil-films', 'showMovies')
MOVIE_GENRES = (True, 'showGenreMovie')

SERIE_SERIES = (URL_MAIN +'accueil-series', 'showMovies')
SERIE_HD = (URL_MAIN +'accueil-series', 'showMovies')
SERIE_GENRES = (True, 'showGenreSerie')

ANIM_ANIMS = (URL_MAIN +'accueil-mangas', 'showMovies')
ANIM_HD = (URL_MAIN +'accueil-mangas', 'showMovies')
ANIM_GENRES = (True, 'showGenreAnime')
 
URL_SEARCH = ('', 'resultSearch')
FUNCTION_SEARCH = 'resultSearch'
   
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'fonctions/recherche.php')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films', 'news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Tous Les Films', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films HD', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Series', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD[1], 'Series HD', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Series Genres', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animes', 'animes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_HD[0] )
    oGui.addDir(SITE_IDENTIFIER, ANIM_HD[1], 'Animes HD', 'animes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animes Genres', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'top-films')
    oGui.addDir(SITE_IDENTIFIER, 'showTop', 'Top-100-Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'top-series')
    oGui.addDir(SITE_IDENTIFIER, 'showTop', 'Top-100-Series', 'series.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()
 
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sSearchText = sSearchText
        resultSearch(sSearchText)
        oGui.setEndOfDirectory()
        return
       
def showGenreMovie():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action', URL_MAIN + 'accueil-films/action'] ) 
    liste.append( ['Animation', URL_MAIN + 'accueil-films/animation'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'accueil-films/arts-martiaux'] )
    liste.append( ['Aventure', URL_MAIN + 'accueil-films/aventure'] )
    liste.append( ['Biopic', URL_MAIN + 'accueil-films/biopic'] )
    liste.append( ['Concert', URL_MAIN + 'accueil-films/concert'] )
    liste.append( ['Comedie', URL_MAIN + 'accueil-films/comedie'] )
    liste.append( ['Comedie Dramatique', URL_MAIN + 'accueil-films/comedie-dramatique'] )
    liste.append( ['Comedie Musicale', URL_MAIN + 'accueil-films/comedie-musicale'] )
    liste.append( ['Documentaire', URL_MAIN + 'accueil-films/documentaire'] )
    liste.append( ['Drame', URL_MAIN + 'accueil-films/drame'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'accueil-films/epouvante-horreur'] )
    liste.append( ['Erotique', URL_MAIN + 'accueil-films/erotique'] )
    liste.append( ['Fantastique', URL_MAIN + 'accueil-films/fantastique'] )
    liste.append( ['Famille', URL_MAIN + 'accueil-films/famille'] )
    liste.append( ['Films de Noel', URL_MAIN + 'accueil-films/films-de-noel'] )
    liste.append( ['Guerre', URL_MAIN + 'accueil-films/guerre'] )
    liste.append( ['Historique', URL_MAIN + 'accueil-films/historique'] )
    liste.append( ['Horreur', URL_MAIN + 'accueil-films/horreur'] )
    liste.append( ['Humour', URL_MAIN + 'accueil-films/humour'] )
    liste.append( ['Musical', URL_MAIN + 'accueil-films/musical'] )
    liste.append( ['Peplum', URL_MAIN + 'accueil-films/peplum'] ) 
    liste.append( ['Policier', URL_MAIN + 'accueil-films/policier'] )
    liste.append( ['Romance', URL_MAIN + 'accueil-films/romance'] )
    liste.append( ['Science Fiction', URL_MAIN + 'accueil-films/science-fiction'] )
    liste.append( ['Spectacles', URL_MAIN + 'accueil-films/spectacles'] )
    liste.append( ['Sport', URL_MAIN + 'accueil-films/sport'] )
    liste.append( ['Sport Event', URL_MAIN + 'accueil-films/sport-event'] )
    liste.append( ['TV', URL_MAIN + 'accueil-films/tv'] )
    liste.append( ['Thriller', URL_MAIN + 'accueil-films/thriller'] )
    liste.append( ['Western', URL_MAIN + 'accueil-films/western'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def showGenreSerie():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action', URL_MAIN + 'accueil-series/action'] ) 
    liste.append( ['Animation', URL_MAIN + 'accueil-series/animation'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'accueil-series/arts-martiaux'] )
    liste.append( ['Aventure', URL_MAIN + 'accueil-series/aventure'] )
    liste.append( ['Biopic', URL_MAIN + 'accueil-series/biopic'] )
    liste.append( ['Concert', URL_MAIN + 'accueil-series/concert'] )
    liste.append( ['Comedie', URL_MAIN + 'accueil-series/comedie'] )
    liste.append( ['Comedie Dramatique', URL_MAIN + 'accueil-series/comedie-dramatique'] )
    liste.append( ['Comedie Musicale', URL_MAIN + 'accueil-series/comedie-musicale'] )
    liste.append( ['Documentaire', URL_MAIN + 'accueil-series/documentaire'] )
    liste.append( ['Drame', URL_MAIN + 'accueil-series/drame'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'accueil-series/epouvante-horreur'] )
    liste.append( ['Erotique', URL_MAIN + 'accueil-series/erotique'] )
    liste.append( ['Fantastique', URL_MAIN + 'accueil-series/fantastique'] )
    liste.append( ['Famille', URL_MAIN + 'accueil-series/famille'] )
    liste.append( ['Films de Noel', URL_MAIN + 'accueil-series/films-de-noel'] )
    liste.append( ['Guerre', URL_MAIN + 'accueil-series/guerre'] )
    liste.append( ['Historique', URL_MAIN + 'accueil-series/historique'] )
    liste.append( ['Horreur', URL_MAIN + 'accueil-series/horreur'] )
    liste.append( ['Humour', URL_MAIN + 'accueil-series/humour'] )
    liste.append( ['Musical', URL_MAIN + 'accueil-series/musical'] )
    liste.append( ['Peplum', URL_MAIN + 'accueil-series/peplum'] ) 
    liste.append( ['Policier', URL_MAIN + 'accueil-series/policier'] )
    liste.append( ['Romance', URL_MAIN + 'accueil-series/romance'] )
    liste.append( ['Soap', URL_MAIN + 'accueil-series/soap'] )
    liste.append( ['Science Fiction', URL_MAIN + 'accueil-series/science-fiction'] )
    liste.append( ['Spectacles', URL_MAIN + 'accueil-series/spectacles'] )
    liste.append( ['Sport', URL_MAIN + 'accueil-series/sport'] )
    liste.append( ['Sport Event', URL_MAIN + 'accueil-series/sport-event'] )
    liste.append( ['TV', URL_MAIN + 'accueil-series/tv'] )
    liste.append( ['Thriller', URL_MAIN + 'accueil-series/thriller'] )
    liste.append( ['Western', URL_MAIN + 'accueil-series/western'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def showGenreAnime():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Action',  URL_MAIN + 'accueil-mangas/action'] )    
    liste.append( ['Animation', URL_MAIN + 'accueil-mangas/animation'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'accueil-mangas/arts-martiaux'] )
    liste.append( ['Aventure', URL_MAIN + 'accueil-mangas/aventure'] )
    liste.append( ['Comedie', URL_MAIN + 'accueil-mangas/comedie'] )
    liste.append( ['Drame', URL_MAIN + 'accueil-mangas/drame'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'accueil-mangas/epouvante-horreur'] )
    liste.append( ['Fantastique', URL_MAIN + 'accueil-mangas/fantastique'] )
    liste.append( ['Historique', URL_MAIN + 'accueil-mangas/historique'] )
    liste.append( ['Horreur', URL_MAIN + 'accueil-mangas/horreur'] )
    liste.append( ['Mythe', URL_MAIN + 'accueil-mangas/mythe'] )
    liste.append( ['Policier', URL_MAIN + 'accueil-mangas/policier'] )
    liste.append( ['Romance', URL_MAIN + 'accueil-mangas/romance'] )
    liste.append( ['Science Fiction', URL_MAIN + 'accueil-mangas/science-fiction'] )
    liste.append( ['Sport', URL_MAIN + 'accueil-mangas/sport'] )
    liste.append( ['Thriller', URL_MAIN + 'accueil-mangas/thriller'] )
    liste.append( ['Tragedie', URL_MAIN + 'accueil-mangas/tragedie'] )
    
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
    
def resultSearch(sSearch):
    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
        
    sUrl = "http://mega-stream.fr/recherche"
    
    #oInputParameterHandler.getAllParameter()
    #sSearch = urllib.unquote(sSearch)

    post_data = {'search' : sSearch }
        
    UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    headers = {'User-Agent': UA ,
               'Host' : 'mega-stream.fr'}
    
    req = urllib2.Request(sUrl , urllib.urlencode(post_data), headers)
    
    response = urllib2.urlopen(req)
    sHtmlContent = response.read()
    response.close()
    
    sPattern = '<div class="movie-img img-box">\s*<img.+?src="([^"]+)".+?<a href="([^"]+)"[^<>]+>([^<>]+)<\/a>.+?<span[^<>]+>([^<>]+)<\/span>'
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sQual = ""
            if aEntry[3]:
                sQual = '[' + aEntry[3] + '] '
            siteUrl = aEntry[1]
            sThumbnail = aEntry[0]
            sTitle = aEntry[2]
            
            sDisplayTitle = cUtil().DecoTitle(sTitle + sQual)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            if '-serie' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
            elif '-mangas-' in siteUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
      

def showMovies(sSearch = ''):
    oGui = cGui()
    
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

        
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    
    sPattern = '<img[^<>]+src="([^"]+)" class="tubeposter".+?<span[^<>]+>([^<>]+)*<\/span>.+?<a class="movie-title" href="([^"]+)"[^<>]+>([^<>]+)<.+?<b>Description :<\/b>([^><]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sQual = ''
            #sAnnee = aEntry[3]
            sThumbnail = aEntry[0]
            if aEntry[1]:
                sQual = '[' + aEntry[1] + ']'
            siteUrl = aEntry[2]
            sTitle = aEntry[3]
            if '-films' in sUrl:
                sTitle = sTitle.split('-')[1]
            sCom = aEntry[4]
            
            sDisplayTitle = cUtil().DecoTitle(sTitle + sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            if '-mangas' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'films.png', sThumbnail, sCom, oOutputParameterHandler)
            elif '-serie' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'films.png', sThumbnail, sCom, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumbnail, sCom, oOutputParameterHandler)
           
        cConfig().finishDialog(dialog)
 
        #Affichage page suivante
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
    
def __checkForNextPage(sHtmlContent):
    
    sPattern = '<span class="pnext"><a href="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        sUrl = aResult[1][0]     
        return sUrl 
 
    return False

def showEpisode():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="(#saison[0-9]+)">(.+?)<\/a>|href="([^"]+/[0-9]+)">(.+?)<\/a><\/li>'
    aResult = re.findall(sPattern,sHtmlContent)

    if (aResult):
        total = len(aResult)
        dialog = cConfig().createDialog(SITE_NAME)
        sSaison = ''
        for aEntry in aResult:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if aEntry[0]:
                sSaison = aEntry[1]
                oGui.addText(SITE_IDENTIFIER, '[COLOR olive]'+ sSaison+ '[/COLOR]')
                
            else:
                sTitle = sMovieTitle + ' ' + sSaison + ' ' + aEntry[3]
                sUrl = aEntry[2]
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog) 

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #on recupere d'abord les liens
    sPattern = '<div id="(lecteur_[0-9]+)">.+?data-tnetnoc-crs="([^"]+)"'
    tablink = re.findall(sPattern,sHtmlContent, re.DOTALL)


    #le classique
    sPattern = '<a href="#(lecteur_[0-9]+)".+?title="([^"]+)"\/> *([^<>]+)<\/a'
    aResult = re.findall(sPattern,sHtmlContent, re.DOTALL)

    if (aResult):
        total = len(aResult)
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sQual = aEntry[2]
            sLang = aEntry[1]
            sDisplayTitle = '[' + sQual + '/' + sLang + ']' + sMovieTitle
            sDisplayTitle = cUtil().DecoTitle(sDisplayTitle)
            
            url = ''
            for i,j in tablink:
                if i == aEntry[0]:
                    url = base64.b64decode(j)[::-1]

            sHosterUrl = url
            oHoster = cHosterGui().checkHoster(sHosterUrl)
 
            if (oHoster != False):
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog) 

    oGui.setEndOfDirectory()

def showTop():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    
    sPattern = '<li class="tops-item">.+?<a href="([^"]+)".+?<img src="([^"]+)" alt="([^"]+)"'

    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
           
            sThumbnail = aEntry[1]
            sUrl = aEntry[0]
            sTitle = aEntry[2]
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            if '-films-' in sUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showEpisode', sDisplayTitle, 'series.png', sThumbnail, '', oOutputParameterHandler)
           
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
