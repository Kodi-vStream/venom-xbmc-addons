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

SITE_IDENTIFIER = 'full_stream_org'
SITE_NAME = 'Full-Stream.org'
SITE_DESC = 'Film Serie et Anime en Streaming HD - Vk.Com - Netu.tv - ExaShare - YouWatch'

URL_MAIN = 'http://full-stream.org/'

MOVIE_MOVIE = (URL_MAIN, 'showMovies')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'films-en-streaming/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'index.php?do=les-plus-vues/', 'showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'index.php?do=les-plus-commentes/', 'showMovies')
MOVIE_GENRES = (True, 'showGenre')

SERIE_SERIES = (URL_MAIN + 'liste-des-series/', 'AlphaSearch')
SERIE_NEWS = (URL_MAIN + 'seriestv/', 'showMovies')
SERIE_VFS = (URL_MAIN + 'seriestv/vf/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'seriestv/vostfr/', 'showMovies')

ANIM_ANIMS = (URL_MAIN + 'liste-des-mangas/','AlphaSearch')
ANIM_NEWS = (URL_MAIN + 'mangas/','showMovies')
ANIM_VFS = (URL_MAIN + 'mangas/mangas-vf/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'mangas/mangas-vostfr/', 'showMovies')

URL_SEARCH = (URL_MAIN + 'index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=', 'showMovies')
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
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genre', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus Notés', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus Vues', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Les plus Commentés', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Séries Nouveautés', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Liste Serie', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries VF', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Séries VOSTFR', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés Nouveautés', 'animes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Liste Animés', 'animes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Animés VF', 'animes.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animés VOSTFR', 'animes.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        #sSearchText = cUtil().urlEncode(sSearchText)
        sUrl = URL_MAIN + 'index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&story='+sSearchText  
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
    
    
def getPremiumUser():
    sUrl = URL_MAIN
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequestHandler.addParameters('login_name', 'vstream')
    oRequestHandler.addParameters('login_password', 'vstream')
    oRequestHandler.addParameters('Submit', '')
    oRequestHandler.addParameters('login', 'submit')
    oRequestHandler.request()

    aHeader = oRequestHandler.getResponseHeader()
    sReponseCookie = aHeader.getheader("Set-Cookie")

    return sReponseCookie


def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['HD/HQ',URL_MAIN + 'films-en-vk-streaming/haute-qualite/'] )
    liste.append( ['Action',URL_MAIN + 'films-en-vk-streaming/action/'] )
    liste.append( ['Aventure',URL_MAIN + 'films-en-vk-streaming/aventure/'] )
    liste.append( ['Animation',URL_MAIN + 'films-en-vk-streaming/animation/'] )
    liste.append( ['Walt Disney',URL_MAIN + 'film/Walt+Disney/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'films-en-vk-streaming/arts-martiaux/'] )
    liste.append( ['Biopic',URL_MAIN + 'films-en-vk-streaming/biopic/'] )
    liste.append( ['Comedie',URL_MAIN + 'films-en-vk-streaming/comedie/'] )
    liste.append( ['Comedie Dramatique',URL_MAIN + 'films-en-vk-streaming/comedie-dramatique/'] )
    liste.append( ['Comedie Musicale',URL_MAIN + 'films-en-vk-streaming/comedie-musicale/'] )
    liste.append( ['Drame',URL_MAIN + 'films-en-vk-streaming/drame/'] )
    liste.append( ['Documentaire',URL_MAIN + 'films-en-vk-streaming/documentaire/'] ) 
    liste.append( ['Horreur',URL_MAIN + 'films-en-vk-streaming/horreur/'] )
    liste.append( ['Fantastique',URL_MAIN + 'films-en-vk-streaming/fantastique/'] )
    liste.append( ['Guerre',URL_MAIN + 'films-en-vk-streaming/guerre/'] )
    liste.append( ['Policier',URL_MAIN + 'films-en-vk-streaming/policier/'] )
    liste.append( ['Romance',URL_MAIN + 'films-en-vk-streaming/romance/'] )
    liste.append( ['Science fiction',URL_MAIN + 'films-en-vk-streaming/science-fiction/'] )
    liste.append( ['Spectacles Scetchs',URL_MAIN + 'films-en-vk-streaming/spectacles/'] )
    liste.append( ['Thriller',URL_MAIN + 'films-en-vk-streaming/thriller/'] )
    liste.append( ['Western',URL_MAIN + 'xfsearch/vkplayer/'] )
    liste.append( ['Sur VK-Streaming',URL_MAIN + 'films-en-vk-streaming/western/'] )
    liste.append( ['Sur YouTube',URL_MAIN + 'xfsearch/Youtube/'] )
    liste.append( ['Sur Dailymotion',URL_MAIN + 'xfsearch/Dailymotion/'] )
    liste.append( ['Sur YouWatch',URL_MAIN + 'xfsearch/YouWatch/'] )
    liste.append( ['Sur Exachare',URL_MAIN + 'films-en-vk-streaming/western/'] )
    liste.append( ['En VOSTFR',URL_MAIN + 'xfsearch/VOSTFR/'] )
    liste.append( ['En VFSTF',URL_MAIN + 'xfsearch/VFSTF/'] )
    liste.append( ['Derniers ajouts',URL_MAIN + 'lastnews/'] )
               
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
    
    if sSearch:
        sUrl = sSearch
        
        sDisp = oInputParameterHandler.getValue('disp')
       
        if (sDisp == 'search3'):#anime
            sUrl = sUrl + '&catlist[]=36'
        elif (sDisp == 'search2'):#serie
            sUrl = sUrl + '&catlist[]=2'
        elif (sDisp == 'search1'):#film
            sUrl = sUrl + '&catlist[]=43'   
        else:#tout le reste
            sUrl = sUrl
        
        #sPattern = 'fullstreaming">.*?<img src="(.+?)".+?<h3.+?><a href="(.+?)">(.+?)<\/a><\/h3>.+?(?:<a href=".quality.+?">(.+?)<\/a>.+?)*Regarder<\/a>'
        sPattern = 'fullstreaming">.*?<img src=".+?src=(.+?)(?:&.+?)*".+?<h3.+?><a href="(.+?)">(.+?)<\/a>.+?(?:<a href=".quality.+?">(.+?)<\/a>.+?)*<span style="font-family:.+?>(.+?)<\/span>'
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sPattern = 'fullstreaming">.*?<img src=".+?src=(.+?)(?:&.+?)*".+?<h3.+?><a href="(.+?)">(.+?)<\/a>.+?(?:<a href=".quality.+?">(.+?)<\/a>.+?)*<span style="font-family:.+?>(.+?)<\/span>'
   
    #recuperation de la page
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

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
                
            sThumb = str(aEntry[0])
            sTitle = aEntry[2]
            if aEntry[3] :
                sTitle = sTitle + ' (' + aEntry[3] + ')'
            sTitle = sTitle.replace('Haute-qualité','HQ')
                
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            # if not 'http' in sThumb:
                # sThumb = URL_MAIN + sThumb

            #if sSearch:
            #    sCom = ''
            #else:
            sCom = aEntry[4]

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
    sPattern = '<div class="navigation.*?".+? <span.+? <a href="(.+?)">'
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
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = str(aEntry[0])
            oHoster = cHosterGui().checkHoster(aEntry[1].lower())                   
            oHoster = cHosterGui().checkHoster(aEntry[0].lower())                   
        
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
    
    oParser = cParser()
    
    #pour accelerer traitement
    sPattern = '<div id="fsElementsContainer">(.+?)<div class="series-player">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContentListFile = aResult[1][0]     
        
    sPattern = '<\/i> (VOSTFR|VF) *<\/div>|<a href="([^<>"]+)" title="([^<]+)" target="seriePlayer".+?>|<a onclick="javascript:return false;" href="#" title="(.+?)" data-rel="episode([0-9]+)" class="fstab">'
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
                
            elif aEntry[1]:
                sHosterUrl = str(aEntry[1])
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                sDisplayTitle = re.sub(' en (VOSTFR|VF)','',aEntry[2])
                sDisplayTitle = cUtil().DecoTitle(sDisplayTitle)
        
                if (oHoster != False):
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

            elif aEntry[3]:
                    sPattern = '<div id="episode' + str(aEntry[4]) + '" class="fullsfeature">(.+?)<\/ul>'
                    aResult3 = oParser.parse(sHtmlContentListFile, sPattern)

                    if (aResult3[0] == True):
                        sPattern = '<a href="([^<>"]+?)" target="seriePlayer" class="fsctab">'
                        aResult2 = oParser.parse(aResult3[1][0], sPattern)

                        if (aResult2[0] == True):
                            for aEntry2 in aResult2[1]:
                                sDisplayTitle = str(sMovieTitle) + ' '+  str(aEntry[3])
                                sDisplayTitle = cUtil().DecoTitle(sDisplayTitle)
                                
                                sHosterUrl = aEntry2
                                oHoster = cHosterGui().checkHoster(sHosterUrl)
                        
                                if (oHoster != False):
                                    oHoster.setDisplayName(sDisplayTitle)
                                    oHoster.setFileName(sMovieTitle)
                                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)              

        cConfig().finishDialog(dialog)
                
    oGui.setEndOfDirectory()
