#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig
import re, urllib
import urllib2


SITE_IDENTIFIER = 'filmenstreaminghd_com'
SITE_NAME = 'FilmEnStreamingHD'
SITE_DESC = 'Films/Séries/Animés en streaming'

URL_MAIN = 'http://www.filmenstreaminghd.com/'

MOVIE_MOVIE = (URL_MAIN + 'films', 'showMovies')
MOVIE_HD = (URL_MAIN + '1080p-films', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'films-populaires', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')

SERIE_SERIES = (URL_MAIN + 'series-tv', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')

ANIM_ANIMS = (URL_MAIN +'animes', 'showMovies')

URL_SEARCH = ('', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (HD)', 'films_hd.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus Vus)', 'films_views.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showQlt', 'Films (Qualités)', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animés', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(str(sSearchText))
        oGui.setEndOfDirectory()
        return
    
def showMovieGenres():
    oGui = cGui()
 
    liste = []
    liste.append( ['Action',URL_MAIN+ 'action'] )
    liste.append( ['Animation',URL_MAIN + 'animation'] )
    liste.append( ['Aventure',URL_MAIN + 'aventure'] )
    liste.append( ['Biographie',URL_MAIN + 'biographie'] )
    liste.append( ['Comédie',URL_MAIN + 'comedie'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + 'comedie-dramatique'] )
    liste.append( ['Documentaire',URL_MAIN + 'documentaire'] )
    liste.append( ['Drame',URL_MAIN + 'drame'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'epouvante-horreur'] )
    liste.append( ['Familial',URL_MAIN + 'familial'] )
    liste.append( ['Fantastique',URL_MAIN + 'fantastique'] )
    liste.append( ['Histoire',URL_MAIN + 'histoire'] )
    liste.append( ['Musical',URL_MAIN + 'musical'] )
    liste.append( ['Mystère',URL_MAIN + 'mystere'] )
    liste.append( ['Policier',URL_MAIN + 'policier-crime'] )
    liste.append( ['Romance',URL_MAIN + 'romance'] )
    liste.append( ['Science Fiction',URL_MAIN + 'science-fiction'] )
    liste.append( ['Thriller',URL_MAIN + 'thriller'] )
    liste.append( ['Western',URL_MAIN + 'western'] )
 
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films_genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def showSerieGenres():
    oGui = cGui()
 
    liste = []
    liste.append( ['Action',URL_MAIN+ 'action-series'] )    
    liste.append( ['Action-Aventure',URL_MAIN + 'action-adventure-series'] )
    liste.append( ['Animation',URL_MAIN + 'animation-series'] )
    liste.append( ['Aventure',URL_MAIN + 'aventure-series'] )
    liste.append( ['Biographie',URL_MAIN + 'biographie-series'] )    
    liste.append( ['Comédie',URL_MAIN + 'comedie-series'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + 'comedie-dramatique-series'] )
    liste.append( ['Documentaire',URL_MAIN + 'documentaire-series'] )
    liste.append( ['Drame',URL_MAIN + 'drame-series'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'epouvante-horreur-series'] )
    liste.append( ['Familial',URL_MAIN + 'familial-series'] )
    liste.append( ['Fantastique',URL_MAIN + 'fantastique-series'] )
    liste.append( ['Histoire',URL_MAIN + 'histoire-series'] )
    liste.append( ['Musical',URL_MAIN + 'musical-series'] )
    liste.append( ['Mystère',URL_MAIN + 'mystere-series'] )
    liste.append( ['Policier',URL_MAIN + 'policier-crime-series'] )
    liste.append( ['Romance',URL_MAIN + 'romance-series'] )
    liste.append( ['Science Fiction',URL_MAIN + 'science-fiction-series'] )
    liste.append( ['Science Fiction - fantastique',URL_MAIN + 'science-Fiction-fantastique-series'] )
    liste.append( ['Thriller',URL_MAIN + 'thriller-series'] )
    liste.append( ['Western',URL_MAIN + 'western-series'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'series_genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    
def showQlt():
    oGui = cGui()
 
    liste = []
    liste.append( ['1080p',URL_MAIN + '1080p-films'] )   
    liste.append( ['720p',URL_MAIN + '720p-films'] )
    
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    if sSearch:
    
        oRequestHandler = cRequestHandler('http://www.filmenstreaminghd.com/recherche/')
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParameters('query', sSearch)
        oRequestHandler.addParameters('submit=Valider', 'Valider')
        sHtmlContent = oRequestHandler.request()

    else:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<div class="film-k.+?<a href="([^<"]+)".+?<div class="kalite">([^<"]+).+?<img src="([^<"]+).+?<div class="baslik">([^<"]+).+?<div class="aciklama">([^<"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sTitle = aEntry[3]
            if aEntry[1]:
                sTitle = sTitle + '[' + aEntry[1]  + '] ' 
                
            sCom = aEntry[4].decode("utf-8")
            sCom = cUtil().unescape(sCom).encode("utf-8")
            sCom = cUtil().removeHtmlTags(sCom)
            sUrl2 = URL_MAIN  + aEntry[0]
            sThumb = URL_MAIN + aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            if 'series-tv' in sUrl or 'saison' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sDisplayTitle,'series.png', sThumb, sCom, oOutputParameterHandler)
            elif 'animes' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sDisplayTitle,'animes.png', sThumb, sCom, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, 'films.png', sThumb, sCom, oOutputParameterHandler)           
    
        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            sUrl = re.sub('\/page-[0-9]','',sUrl)
            oOutputParameterHandler.addParameter('siteUrl', sUrl+'/'+sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sPattern = '<span class="pikon" style="background-image: url\(/sistem/inc/part_ikon/(.+?).png\);"></span>(.+?)<span|class="partsec.+?" id="([^"]+?)".+?</i>([^<]+?)</a>'
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
            sDisplayTitle = sDisplayTitle + '[COLOR teal] >> ' + aEntry[3] +' [/COLOR]'
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sPid', aEntry[2])
            
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER,  '[COLOR red]'+aEntry[0]+' - '+aEntry[1]+'[/COLOR]', oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    
    sPattern = '<a class="sonraki-sayfa" href="(?:/.+?/|)(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return  aResult[1][0]

    return False

def showLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    oParser = cParser()
    sPattern = '<a class="partsec" id="([^"]+)".+?</span>([^<]+)<span'
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
            oOutputParameterHandler.addParameter('siteUrl',  sUrl)
            oOutputParameterHandler.addParameter('sPid',  aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)             
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()  

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sPid = oInputParameterHandler.getValue('sPid')

    postdata = 'pid=' + sPid
    
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('pid', sPid)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<ifram[^<>]+? src=[\'"]([^\'"]+?)[\'"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
            
            sHosterUrl =  str(aEntry)
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)         
    
        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
