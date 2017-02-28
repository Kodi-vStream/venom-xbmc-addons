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
 
URL_SEARCH = ('http://french-stream.com/index.php?story='),('showMovies')
FUNCTION_SEARCH = 'showMovies'
 
MOVIE_NEWS = (URL_MAIN + 'index.php?do=cat&category=film-en-streaming', 'showMovies') # films nouveautés
MOVIE_MOVIE = ('http://url', 'showMovies') # films vrac
MOVIE_VIEWS = ('http://url', 'showMovies') # films + plus
MOVIE_COMMENTS = ('http://url', 'showMovies') # films + commentés
MOVIE_NOTES = ('http://url', 'showMovies') # films mieux notés
MOVIE_GENRES = (True, 'showGenre')
MOVIE_VF = (URL_MAIN +'index.php?do=cat&category=vf', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN +'index.php?do=cat&category=vostfr', 'showMovies')
MOVIE_HDLIGHT = (URL_MAIN + 'index.php?do=xfsearch&xfname=qualit&xf=HDLight','showMovies')
 
SERIE_NEWS = (URL_MAIN +'serie-tv-en-streaming/', 'showMovies')
SERIE_SERIES = ('http://url', 'showSeries') 
SERIE_VFS = (URL_MAIN +'index.php?do=cat&category=serie-en-vf-streaming', 'showMovies') 
SERIE_VOSTFRS = (URL_MAIN +'/index.php?do=cat&category=serie-en-vostfr-streaming', 'showMovies')
SERIE_GENRE = (True, 'showGenre')
SERIE_HDLIGHT = (URL_MAIN + 'index.php?do=cat&category=serie-en-hd-streaming','showSeries')
 
ANIM_NEWS = ('http://url', 'showAnimes') #anime nouveautés
ANIM_ANIMS = ('http://url', 'showAnimes') #anime vrac
ANIM_VFS = ('http://url', 'showAnimes') #anime VF
ANIM_VOSTFRS = ('http://url', 'showAnimes') #anime VOSTFR
ANIM_MOVIES = ('http://url', 'showAnimes') #anime film
ANIM_GENRES = (True, 'showGenre') #anime genre
 
DOC_DOCS = ('http://url', 'showOthers') #Documentaire
SPORT_SPORTS = ('http://url', 'showOthers') #sport
MOVIE_NETS = ('http://url', 'showOthers') #video du net
REPLAYTV_REPLAYTV = ('http://url', 'showOthers') #Replay
 
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
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films HD-Light', 'genres.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries VF nouveauté', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries Vostfr nouveauté', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries HD-Light', 'series.png', oOutputParameterHandler)
             
    oGui.setEndOfDirectory()
   
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0]+sSearchText +'&do=search&subaction=search'
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
 
def AlphaSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    dialog = cConfig().createDialog(SITE_NAME)
    
    for i in range(0,36) :
        cConfig().updateDialog(dialog, 36)
        if dialog.iscanceled():
            break
        
        if (i < 10):
            sTitle = chr(48+i)
        else:
            sTitle = chr(65+i-10)
            
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl + sTitle.lower() + '.html' )
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'AlphaDisplay', '[COLOR teal] Lettre [COLOR red]'+ sTitle +'[/COLOR][/COLOR]', 'genres.png', oOutputParameterHandler)
        
    cConfig().finishDialog(dialog)
    
    oGui.setEndOfDirectory()
        
def AlphaDisplay():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    print sUrl
    
    #recuperation de la page
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a href="(.+?)" class="list-name">&raquo;(.+?)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sTitle = aEntry[1]
            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', aEntry[0])
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, '', '','', oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)
        
        oGui.setEndOfDirectory()
        
def showMovies(sSearch = ''):
    oGui = cGui()
    
    oInputParameterHandler = cInputParameterHandler()
    
    dlenewssortby = False
    sType = ''
    
    if sSearch:
        sUrl = sSearch
        
        #partie en test
        oInputParameterHandler = cInputParameterHandler()
        sType = oInputParameterHandler.getValue('type')

      #sPattern = 'fullstreaming">.*?<img src="(.+?)".+?<h3.+?><a href="(.+?)">(.+?)<\/a><\/h3>.+?(?:<a href=".quality.+?">(.+?)<\/a>.+?)*Regarder<\/a>'
        sPattern = 'fullstreaming">.*?<img src="(.+?)".+?<h3.+?><a href="(.+?)">(.+?)<\/a>.+?(?:<a href=".quality.+?">(.+?)<\/a>.+?)*<span style="font-family:.+?>(.+?)<\/span>'
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sPattern = 'fullstreaming">.*?<img src="(.+?)".+?<h3.+?><a href="(.+?)">(.+?)<\/a>.+?(?:<a href=".quality.+?">(.+?)<\/a>.+?)*<span style="font-family:.+?>(.+?)<\/span>'
   
    #recuperation des tris
    
    # les plus noter dlenewssortby=rating&dledirection=desc&set_new_sort=dle_sort_cat&set_direction_sort=dle_direction_cat
    # les plus vue dlenewssortby=news_read&dledirection=desc&set_new_sort=dle_sort_cat&set_direction_sort=dle_direction_cat
    
    #les plus commenter dlenewssortby=comm_num&dledirection=desc&set_new_sort=dle_sort_main&set_direction_sort=dle_direction_main
    
    if ("rating" in sUrl or "news_read" in sUrl or "comm_num" in sUrl):
    
        oRequestHandler = cRequestHandler(URL_MAIN + 'movie')
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)        
        
        oRequestHandler.addParameters('dledirection', 'desc')
        oRequestHandler.addParameters('set_new_sort', 'dle_sort_cat')
        oRequestHandler.addParameters('set_direction_sort', 'dle_direction_cat')
        
        
        if ("rating" in sUrl):
            dlenewssortby = "rating"
        elif ("news_read" in sUrl):
            dlenewssortby = "news_read"
        elif ("comm_num" in sUrl):        
            dlenewssortby = "comm_num"
            
        oRequestHandler.addParameters('dlenewssortby', dlenewssortby)

    
    else :
        oRequestHandler = cRequestHandler(sUrl)
        
        if sType:
            if sType == "film":
                oRequestHandler.addParameters('catlist[]', '43')
            if sType == "serie":
                oRequestHandler.addParameters('catlist[]', '2')
            if sType == "anime":
                oRequestHandler.addParameters('catlist[]', '36')
        
    
    if oInputParameterHandler.getValue('dlenewssortby'):
    
        dlenewssortby = oInputParameterHandler.getValue('dlenewssortby')
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParameters('dlenewssortby', dlenewssortby)
        oRequestHandler.addParameters('dledirection', 'desc')
        oRequestHandler.addParameters('set_new_sort', 'dle_sort_cat')
        oRequestHandler.addParameters('set_direction_sort', 'dle_direction_cat')
        
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
            oOutputParameterHandler.addParameter('dlenewssortby', dlenewssortby)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()
   
def __checkForNextPage(sHtmlContent):
    sPattern = '<a href="([^"]+)">Suivant.+?<\/a><\/div>'
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
    
    # oRequestHandler = cRequestHandler(sUrl)
    # oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    # oRequestHandler.addParameters('login_name', 'vstream')
    # oRequestHandler.addParameters('login_password', 'vstream')
    # oRequestHandler.addParameters('Submit', '')
    # oRequestHandler.addParameters('login', 'submit')
    # sHtmlContent = oRequestHandler.request();
    
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
    
    #pour accelerer traitement
    sPattern = '<div id="fsElementsContainer">(.+?)<div class="series-player">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContentListFile = aResult[1][0]     
        
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
