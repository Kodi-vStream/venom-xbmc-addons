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
import re
 
SITE_IDENTIFIER = 'french_stream_com'
SITE_NAME = 'French-stream'
SITE_DESC = 'films en streaming'
 
URL_MAIN = 'http://french-stream.com/'
 
URL_SEARCH = (URL_MAIN + 'index.php?do=search&subaction=search&story=','showMovies')
FUNCTION_SEARCH = 'showMovies'
 
MOVIE_NEWS = (URL_MAIN + 'film-en-streaming/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_VF = (URL_MAIN +'film-en-streaming/vf/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN +'film-en-streaming/vostfr/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'film-en-streaming/hd-vf/','showMovies')
 
SERIE_NEWS = (URL_MAIN +'serie-tv-en-streaming/', 'showMovies')
SERIE_VFS = (URL_MAIN +'serie-tv-en-streaming/serie-en-vf-streaming/', 'showMovies') 
SERIE_VOSTFRS = (URL_MAIN +'serie-tv-en-streaming/serie-en-vostfr-streaming/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_HD = (URL_MAIN + 'serie-tv-en-streaming/serie-en-hd-streaming/','showSeries')

def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
 
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'films_news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF[1], 'Films VF (Derniers ajouts)', 'films_vf.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films Vostfr (Derniers ajouts)', 'films_vostfr.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'films_genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (HD-Light)', 'films_hd.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries VF (Derniers ajouts)', 'series_vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries Vostfr (Derniers ajouts)', 'series_vostfr.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD[1], 'Séries (HD-Light)', 'series.png', oOutputParameterHandler)
             
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'series_genres.png', oOutputParameterHandler)
             
    oGui.setEndOfDirectory()
   
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0]+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
   
def showMovieGenres():
    oGui = cGui()
 
    liste = []
    liste.append( ['Action',URL_MAIN + 'xfsearch/genre-1/action/'] )
    liste.append( ['Animation',URL_MAIN +'xfsearch/genre-1/animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'xfsearch/genre-1/arts+Martiaux/'] )
    liste.append( ['Aventure',URL_MAIN + 'xfsearch/genre-1/aventure/'] )
    liste.append( ['Biopic',URL_MAIN + 'xfsearch/genre-1/biopic/'] )
    liste.append( ['Walt Disney',URL_MAIN + '/index.php?do=xfsearch&xfname=genre-1&xf=Walt+Disney+Animation'] )
    liste.append( ['Comédie',URL_MAIN + 'xfsearch/genre-1/comedie/'] )
    liste.append( ['Comédie Dramatique',URL_MAIN + 'xfsearch/genre-1/dramatique/'] )
    liste.append( ['Comédie Musicale',URL_MAIN + 'xfsearch/genre-1/comedie-musicale/'] )
    liste.append( ['Documentaire',URL_MAIN + 'xfsearch/genre-1/documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'xfsearch/genre-1/drame/'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'xfsearch/genre-1/epouvante-horreur/'] )
    liste.append( ['Erotique',URL_MAIN + 'xfsearch/genre-1/erotique'] )
    liste.append( ['Espionnage',URL_MAIN + 'xfsearch/genre-1/espionnage/'] )
    liste.append( ['Famille',URL_MAIN + 'xfsearch/genre-1/famille/'] )
    liste.append( ['Fantastique',URL_MAIN + 'xfsearch/genre-1/fantastique/'] )  
    liste.append( ['Guerre',URL_MAIN + 'xfsearch/genre-1/guerre/'] )
    liste.append( ['Historique',URL_MAIN + 'xfsearch/genre-1/historique/'] )
    liste.append( ['Musical',URL_MAIN + 'xfsearch/genre-1/musical/'] )
    liste.append( ['Policier',URL_MAIN + 'xfsearch/genre-1/policier/'] )
    liste.append( ['Péplum',URL_MAIN + 'xfsearch/genre-1/peplum/'] )
    liste.append( ['Romance',URL_MAIN + 'xfsearch/genre-1/romance/'] )
    liste.append( ['Science Fiction',URL_MAIN + 'xfsearch/genre-1/science-fiction/'] )
    liste.append( ['Spectacle',URL_MAIN + 'xfsearch/genre-1/spectacle/'] )
    liste.append( ['Thriller',URL_MAIN + 'xfsearch/genre-1/thriller/'] )
    liste.append( ['Western',URL_MAIN + 'xfsearch/genre-1/western/'] )
    liste.append( ['Divers',URL_MAIN + 'xfsearch/genre-1/divers/'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'films_genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def showSerieGenres():
    oGui = cGui()
 
    liste = []
    liste.append( ['Action',URL_MAIN +'xfsearch/genre-serie/Action/'] )
    liste.append( ['Animation',URL_MAIN+'xfsearch/genre-serie/Animation/'])
    liste.append( ['Arts Martiaux',URL_MAIN + 'xfsearch/genre-serie/Arts+Martiaux/'] )
    liste.append( ['Aventure',URL_MAIN + 'xfsearch/genre-serie/Aventure/'])
    liste.append( ['Comédie',URL_MAIN + 'xfsearch/genre-serie/Comedie/'])
    liste.append( ['Comédie Dramatique',URL_MAIN + 'xfsearch/genre-serie/Comédie+dramatique/'] )
    liste.append( ['Comédie Musicale',URL_MAIN + 'xfsearch/genre-serie/Comédie+musicale/'] )
    liste.append( ['Documentaire',URL_MAIN + 'xfsearch/genre-serie/Documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'xfsearch/genre-serie/Drame/'])
    liste.append( ['Epouvante Horreur',URL_MAIN + 'xfsearch/genre-serie/Epouvante-horreur/'] )
    liste.append( ['Espionnage',URL_MAIN + 'xfsearch/genre-serie/Espionnage/'])
    liste.append( ['Famille',URL_MAIN + 'xfsearch/genre-serie/Famille/'])
    liste.append( ['Fantastique',URL_MAIN + 'xfsearch/genre-serie/Fantastique/'] )  
    liste.append( ['Guerre',URL_MAIN + 'xfsearch/genre-serie/Guerre/'])
    liste.append( ['Historique',URL_MAIN + 'xfsearch/genre-serie/Historique/'])
    liste.append( ['Judiciaire',URL_MAIN + 'xfsearch/genre-serie/Judidiaire/'])
    liste.append( ['Médical',URL_MAIN + 'xfsearch/genre-serie/Médical/'])
    liste.append( ['Musical',URL_MAIN + 'xfsearch/genre-serie/Musical/'] )
    liste.append( ['Policier',URL_MAIN + 'xfsearch/genre-serie/Policier/'] )
    liste.append( ['Romance',URL_MAIN + 'xfsearch/genre-serie/Romance/'] )
    liste.append( ['Science Fiction',URL_MAIN + 'xfsearch/genre-serie/Science+fiction/'] )
    liste.append( ['Soap',URL_MAIN + 'xfsearch/genre-serie/Soap/'] )
    liste.append( ['Thriller',URL_MAIN + 'xfsearch/genre-serie/Thriller/'] )
    liste.append( ['Western',URL_MAIN + 'xfsearch/genre-serie/Western/'] )
       
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'series_genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()    
    
def showMovies(sSearch = ''):
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    
    if sSearch:
        sUrl = sSearch
        sPattern = 'fullstreaming">.*?<img src="(.+?)".+?<h3.+?><a href="(.+?)">(.+?)<\/a>.+?(?:<a href=".quality.+?">(.+?)<\/a>.+?)*<span style="font-family:.+?>(.+?)<\/span>'
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sPattern = 'fullstreaming">.*?<img src="(.+?)".+?<h3.+?><a href="(.+?)">(.+?)<\/a>.+?(?:<a href=".quality.+?">(.+?)<\/a>.+?)*<span style="font-family:.+?>(.+?)<\/span>'
   
    oRequestHandler = cRequestHandler(sUrl)       
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sThumb = str(aEntry[0])
            sTitle = aEntry[2]
            if aEntry[3] :
                sTitle = sTitle + ' (' + aEntry[3] + ')'
            sTitle = sTitle.replace('Haute-qualité','HQ')
                
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            if not 'http' in sThumb:
                sThumb = URL_MAIN[:-1] + sThumb
                
            #Bon petit modif pr corriger nom, apparement le regex a tendance a chnager
            if sThumb.startswith('/IMG/') or sThumb.startswith('/img/'):
                sThumb = sThumb.replace('/IMG/french-stream.php?src=','').replace('/img/french-stream.com.php?src=','')
                sThumb = sThumb.split('&')[0]

            #if sSearch:
            #    sCom = ''
            #else:
            sCom = aEntry[4]
            
            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sUrl.replace(URL_SEARCH[0],''),aEntry[2]) == 0:
                    continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)

            if '/seriestv/' in sUrl or 'saison' in aEntry[1] or re.match('.+?saison [0-9]+',sTitle,re.IGNORECASE):
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, '', sThumb,sCom, oOutputParameterHandler)
            elif '/mangas/' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, '', sThumb, sCom, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sCom, oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^"]+)"><b class="pprev ico">Suivant <i'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
    
def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^<]+)" target="filmPlayer" class="ilink sinactive"><img alt="(.+?)"'
    sPattern = '<i class="fa fa-play-circle-o"></i>([^<]+)</div>|<a href="([^<>"]+)" title="([^<]+)" target="seriePlayer".+?>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addDir(SITE_IDENTIFIER, 'showHosters', '[COLOR red]' + str(aEntry[0]) + '[/COLOR]', 'host.png', oOutputParameterHandler)

            sHosterUrl = str(aEntry[1])
            oHoster = cHosterGui().checkHoster(sHosterUrl)
        
            if (oHoster != False):         
                try:
                    oHoster.setHD(sHosterUrl)
                except: pass
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)

                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
    
def Showlink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    if '9animeonline' in sUrl:
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        
        sPattern = 'file: "([^"]+)"'
        aResult = re.findall(sPattern,sHtmlContent)
        if (aResult):
            sUrl = aResult[0]
            
    oHoster = cHosterGui().checkHoster(sUrl)

    if (oHoster != False):
        sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
        
        oHoster.setDisplayName(sDisplayTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sUrl, sThumbnail)
                
    oGui.setEndOfDirectory()
    
def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    oParser = cParser()   
        
    sPattern = '<\/i> (VOSTFR|VF) *<\/div>|<a class="fstab" href="([^"]+)" *id="gGotop" *target="seriePlayer".+?<\/i>\s+([^<>]+?)\s+<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addDir(SITE_IDENTIFIER, 'showHosters', '[COLOR red]' + str(aEntry[0]) + '[/COLOR]', 'host.png', oOutputParameterHandler)

            elif aEntry[1]:

                sTitle = str(sMovieTitle) + ' ' +  str(aEntry[2])
                
                sHosterUrl = aEntry[1]
                sHosterName = ''
                
                if '9animeonline' in sHosterUrl:
                    sHosterName = 'Google'

                else:              
                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    sHosterName = str(oHoster.getDisplayName())
                    
                sDisplayTitle = sTitle + '[' + sHosterName + ']' 
            
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oGui.addTV(SITE_IDENTIFIER, 'Showlink', sDisplayTitle, '', sThumbnail,'', oOutputParameterHandler)       

    cConfig().finishDialog(dialog)
                
    oGui.setEndOfDirectory()
