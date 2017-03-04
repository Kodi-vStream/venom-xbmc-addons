#-*- coding: utf-8 -*-
#Venom.
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

import re
 
SITE_IDENTIFIER = 'french_stream_com'
SITE_NAME = 'French-stream.com'
SITE_DESC = 'films en streaming'
 
URL_MAIN = 'http://french-stream.com/'
 
URL_SEARCH = (URL_MAIN + 'index.php?do=search&subaction=search&story=','showMovies')
FUNCTION_SEARCH = 'showMovies'
 
MOVIE_NEWS = (URL_MAIN + 'index.php?do=cat&category=film-en-streaming', 'showMovies')
MOVIE_GENRES = (True, 'showGenre')
MOVIE_VF = (URL_MAIN +'index.php?do=cat&category=vf', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN +'index.php?do=cat&category=vostfr', 'showMovies')
MOVIE_HD = (URL_MAIN + 'index.php?do=xfsearch&xfname=qualit&xf=HDLight','showMovies')
 
SERIE_NEWS = (URL_MAIN +'serie-tv-en-streaming/', 'showMovies')
SERIE_VFS = (URL_MAIN +'index.php?do=cat&category=serie-en-vf-streaming', 'showMovies') 
SERIE_VOSTFRS = (URL_MAIN +'index.php?do=cat&category=serie-en-vostfr-streaming', 'showMovies')
SERIE_GENRE = (True, 'showSerieGenre')
SERIE_HD = (URL_MAIN + 'index.php?do=cat&category=serie-en-hd-streaming','showSeries')

def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
 
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VF[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VF[1], 'Films VF nouveauté', 'news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films VOSTFR nouveauté', 'news.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films Genre', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films HD-Light', 'genres.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries VF nouveauté', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries Vostfr nouveauté', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD[1], 'Séries HD-Light', 'series.png', oOutputParameterHandler)
             
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRE[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRE[1], 'Séries Genre', 'series.png', oOutputParameterHandler)
             
    oGui.setEndOfDirectory()
   
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0]+sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
   
   
def showGenre():
    oGui = cGui()
 
    liste = []
    liste.append( ['Action',URL_MAIN + 'xfsearch/genre-1/action'] )
    liste.append( ['Animation',URL_MAIN +'xfsearch/genre-1/animation'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'xfsearch/genre-1/arts+Martiaux'] )
    liste.append( ['Aventure',URL_MAIN + 'xfsearch/genre-1/aventure'] )
    liste.append( ['Biopic',URL_MAIN + 'xfsearch/genre-1/biopic'] )
    liste.append( ['Walt Disney',URL_MAIN + '/index.php?do=xfsearch&xfname=genre-1&xf=Walt+Disney+Animation'] )
    liste.append( ['Comedie',URL_MAIN + 'xfsearch/genre-1/comedie'] )
    liste.append( ['Comedie Dramatique',URL_MAIN + 'xfsearch/genre-1/dramatique/'] )
    liste.append( ['Comedie Musicale',URL_MAIN + 'xfsearch/genre-1/comedie-musicale/'] )
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
    liste.append( ['Peplum',URL_MAIN + 'xfsearch/genre-1/peplum/'] )
    liste.append( ['Romance',URL_MAIN + 'xfsearch/genre-1/romance/'] )
    liste.append( ['Science Fiction',URL_MAIN + 'xfsearch/genre-1/science-fiction/'] )
    liste.append( ['Spectacle',URL_MAIN + 'xfsearch/genre-1/spectacle/'] )
    liste.append( ['Thriller',URL_MAIN + 'xfsearch/genre-1/thriller/'] )
    liste.append( ['Western',URL_MAIN + 'xfsearch/genre-1/western/'] )
    liste.append( ['Divers',URL_MAIN + 'xfsearch/genre-1/divers/'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()

def showSerieGenre():
    oGui = cGui()
 
    liste = []
    liste.append( ['Action',URL_MAIN +'index.php?do=xfsearch&xfname=genre-serie&xf=Action'] )
    liste.append( ['Animation',URL_MAIN+'index.php?do=xfsearch&xfname=genre-serie&xf=Animation'])
    liste.append( ['Arts Martiaux',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Arts+Martiaux'] )
    liste.append( ['Aventure',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Aventure'])
    liste.append( ['Comedie',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Comedie'])
    liste.append( ['Comedie Dramatique',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Comédie+dramatique'] )
    liste.append( ['Comedie Musicale',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Comédie+musicale'] )
    liste.append( ['Documentaire',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Documentaire'] )
    liste.append( ['Drame',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Drame'])
    liste.append( ['Epouvante Horreur',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Epouvante-horreur'] )
    liste.append( ['Espionnage',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Espionnage'])
    liste.append( ['Famille',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Famille'])
    liste.append( ['Fantastique',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Fantastique'] )  
    liste.append( ['Guerre',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Guerre'])
    liste.append( ['Historique',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Historique'])
    liste.append( ['Judiciaire',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Judidiaire'])
    liste.append( ['Médical',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Médical'])
    liste.append( ['Musical',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Musical'] )
    liste.append( ['Policier',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Policier'] )
    liste.append( ['Romance',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Romance'] )
    liste.append( ['Science Fiction',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Science+fiction/'] )
    liste.append( ['Soap',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Soap'] )
    liste.append( ['Thriller',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Thriller/'] )
    liste.append( ['Websérie',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Websérie/'] )
    liste.append( ['Western',URL_MAIN + 'index.php?do=xfsearch&xfname=genre-serie&xf=Western/'] )
       
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
            if sThumb.startswith('/IMG/french-stream.php?'):
                sThumb = sThumb.replace('/IMG/french-stream.php?src=','')
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
                oGui.addDir(SITE_IDENTIFIER, 'showHosters', '[COLOR red]'+str(aEntry[0])+'[/COLOR]', 'host.png', oOutputParameterHandler)

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
    
def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    #cConfig().log(sUrl)
    
    oParser = cParser()   
        
    sPattern = '<\/i> (VOSTFR|VF) *<\/div>|<a href="([^<>"]+)" target="seriePlayer" *title="([^"]+)" * data-rel="episode([0-9]+)"'
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
                oGui.addDir(SITE_IDENTIFIER, 'showHosters', '[COLOR red]'+str(aEntry[0])+'[/COLOR]', 'host.png', oOutputParameterHandler)

            elif aEntry[2]:
                    sPattern = '<div id="episode' + str(aEntry[3]) + '" class="fullsfeature">(.+?)<\/ul>'
                    aResult3 = oParser.parse(sHtmlContent, sPattern)
                    
                    #cConfig().log(sPattern)

                    if (aResult3[0] == True):
                        sPattern = '<a href="([^<>"]+?)" target="seriePlayer"'
                        aResult2 = oParser.parse(aResult3[1][0], sPattern)

                        if (aResult2[0] == True):
                            for aEntry2 in aResult2[1]:
                                sMovieTitle2 = str(sMovieTitle) + ' '+  str(aEntry[2])
                                sDisplayTitle = cUtil().DecoTitle(sMovieTitle2)
                                
                                sHosterUrl = aEntry2
                                oHoster = cHosterGui().checkHoster(sHosterUrl)
                        
                                if (oHoster != False):
                                    oHoster.setDisplayName(sDisplayTitle)
                                    oHoster.setFileName(sMovieTitle2)
                                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)              

    cConfig().finishDialog(dialog)
                
    oGui.setEndOfDirectory()
