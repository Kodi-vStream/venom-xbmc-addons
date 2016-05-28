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
import re,xbmcgui,unicodedata
from resources.lib.dl_deprotect import DecryptDlProtect

#clone de dpstreaming.tv

SITE_IDENTIFIER = 'streamingk_com'
SITE_NAME = 'Streamingk.com'
SITE_DESC = 'Film Streaming & Serie Streaming: Regardez films et series de qualité entièrement gratuit. Tout les meilleurs streaming en illimité.'

URL_MAIN = 'http://streamingk.com'

MOVIE_NEWS = ('http://streamingk.com/category/films/', 'showMovies')
MOVIE_MOVIE = ('http://streamingk.com/category/films/', 'showMovies')

MOVIE_GENRES = (True, 'showGenre')

SERIE_SERIES = ('http://streamingk.com/category/series-tv/', 'showMovies')
SERIE_NEWS = ('http://streamingk.com/category/series-tv/', 'showMovies')

ANIM_ANIMS = ('http://streamingk.com/category/mangas/', 'showMovies')
ANIM_NEWS = ('http://streamingk.com/category/mangas/', 'showMovies')

REPLAYTV_REPLAYTV = ('http://streamingk.com/category/emissions-tv/', 'showMovies')

#SPORT_SPORTS = ('http://streamingk.com/category/sport/', 'showMovies')

URL_SEARCH = ('http://streamingk.com/?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'



def load(): 
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMoviesSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautés', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Series Nouveautés', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANIMS[1], 'Animes Nouveautés', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_REPLAYTV[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_REPLAYTV[1], 'Emissions TV', 'series.png', oOutputParameterHandler)
    
    # oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    # oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1], 'Sport', 'series.png', oOutputParameterHandler)   

    oGui.setEndOfDirectory()

def showMoviesSearch():
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

    liste.append( ['Action','http://streamingk.com/category/films/action/'] )
    liste.append( ['Emission TV','http://streamingk.com/category/emissions-tv/'] )
    liste.append( ['Animation','http://streamingk.com/category/films/animation/'] )
    liste.append( ['Arts Martiaux','http://streamingk.com/category/films/arts-martiaux/'] )
    liste.append( ['Aventure','http://streamingk.com/category/films/aventure-films/'] )
    liste.append( ['Comedie','http://streamingk.com/category/films/comedie/'] )
    liste.append( ['Documentaire','http://streamingk.com/category/documentaire/'] )
    liste.append( ['Drame','http://streamingk.com/category/films/drame/'] )
    liste.append( ['Espionnage','http://streamingk.com/category/films/espionnage/'] )
    liste.append( ['Famille','http://streamingk.com/category/films/famille/'] )
    liste.append( ['Fantastique','http://streamingk.com/category/films/fantastique/'] )
    liste.append( ['Guerre','http://streamingk.com/category/films/guerre/'] )
    liste.append( ['Historique','http://streamingk.com/category/films/historique/'] )
    liste.append( ['Epouvante-Horreur','http://streamingk.com/category/films/horreur/'] )
    liste.append( ['Musical','http://streamingk.com/category/films/musical/'] )
    liste.append( ['Policier','http://streamingk.com/category/films/policier/'] )
    liste.append( ['Romance','http://streamingk.com/category/films/romance/'] )
    liste.append( ['Science-Fiction','http://streamingk.com/category/films/science-fiction/'] )
    liste.append( ['Spectacle','http://streamingk.com/category/films/spectacle/'] )
    liste.append( ['Thriller','http://streamingk.com/category/films/thriller/'] )
    liste.append( ['Western','http://streamingk.com/category/films/western/'] )

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
    sHtmlContent = oRequestHandler.request()
    #Meilleure resolution sthumbnail
    sHtmlContent = sHtmlContent.replace('119x125','125x160')
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    #Magouille pour virer les 3 ligne en trop en cas de recherche
    if sSearch:
        sHtmlContent = sHtmlContent.replace('quelle-est-votre-serie-preferee','<>')
        sHtmlContent = sHtmlContent.replace('top-series-du-moment','<>')
        sHtmlContent = sHtmlContent.replace('listes-des-series-annulees-et-renouvelees','<>')
        
    oParser = cParser()
    sPattern = '<div class="moviefilm"> *<a href=".+?"> *<img src="([^<>"]+)".+?\/><\/a><div class="movief"><a href="([^<]+)">([^<]+)<\/a><\/div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[2]
            sTitle = sTitle.replace(' [Streaming]','')
            sTitle = sTitle.replace(' [Telecharger]','')
            sTitle = sTitle.replace(' [Complète]','')
            sTitle = sTitle.replace(' [Complete]','')
            
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            if '-filmographie-streaming' in aEntry[1]:
                pass
            elif 'series' in sUrl or re.match('.+?saison [0-9]+',sTitle,re.IGNORECASE):
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sDisplayTitle, '', aEntry[0], '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', aEntry[0], '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def showSeries(sLoop = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sHtmlContent = sHtmlContent.decode('utf-8',"replace")
    sHtmlContent = unicodedata.normalize('NFD', sHtmlContent).encode('ascii', 'ignore').decode("unicode_escape")#vire accent et '\'
    sHtmlContent = sHtmlContent.encode('utf-8')#On remet en utf-8
    
    oParser = cParser()
 
    sPattern = '<span style="color: #33cccc;[^<>"]*">(?:<strong>)*((?:Stream|Telec)[^<>]+)|>(Episode[^<]{2,12})<(?!\/a>)(.{0,10}a href="http.+?)(?:<.p|<br|<.div)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    #astuce en cas d'episode unique
    if (aResult[0] == False) and (sLoop == False):
        #oGui.setEndOfDirectory()
        showHosters(True)
        return;
    
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
                oGui.addMisc(SITE_IDENTIFIER, 'showSeries', '[COLOR red]'+str(aEntry[0])+'[/COLOR]', 'series.png', sThumbnail, '', oOutputParameterHandler)
            else:
                sTitle = sMovieTitle + ' ' + aEntry[1]
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[2]))
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMisc(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = '<span class=\'current\'>.+?</span><a class="page larger" href="(.+?)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sUrl = aResult[1][0]
        return sUrl

    return False


def showHosters(sLoop = False):
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','')
    sHtmlContent = sHtmlContent.replace("src='https://ad.a-ads.com",'')

    oParser = cParser()

    #1 er version
    sPattern = '<iframe[^<>]+?src=[\'|"](http.+?)[\'|"]'
    aResult1 = re.findall( sPattern, sHtmlContent)
    
    #seconde version
    sPattern = '<a class="large button .+?" href="(.+?)" target="vid">'
    aResult2 = re.findall( sPattern, sHtmlContent)
    
    #3eme version
    sPattern = '<a href="([^<>"]+?)" target="_blank">Regarder<\/a>'
    aResult3 = re.findall( sPattern, sHtmlContent)
    
    #fusion des resultats
    aResult = []
    aResult = aResult1 + aResult2 + aResult3
        
    #Si il y a rien a afficher c'est peut etre une serie
    if (len(aResult) == 0) and (sLoop == False):
        #oGui.setEndOfDirectory()
        showSeries(True)
        return        
        
    if (len(aResult) > 0):
        total = len(aResult)
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult:
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


def serieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oParser = cParser()
    
    liste = False
    
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    #1 - liste fichier
    if 'dl-protect.com' in sUrl:
        sPattern = 'href="([^<]+)" target="_blank.+?>(.+?)<.a>'
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            
            UrlList =''
            vid_list = []
            hoster_list = []
     
            if len(aResult[1]) > 1:
                for i in aResult[1]:
                    vid_list.extend([i[0]])
                    hoster_list.extend([i[1]])
            if len(aResult[1]) == 1:
                UrlList = aResult[1][0][0]
            else:
                result = xbmcgui.Dialog().select('Choose a link list', hoster_list)
                if result != -1:
                    UrlList = vid_list[result]

            if (UrlList):
                sHtmlContent = DecryptDlProtect(UrlList)
                if sHtmlContent:
                    sPattern = '<br .><a href="(.+?)" target="_blank">http:.+?<.a>'
                    aResult = oParser.parse(sHtmlContent, sPattern)
                    liste = True
            else:
                return
    else:
        #2 - Normal
        sPattern = 'href="([^<]+)" target="_blank"[^<>]*>.+?<\/a>'
        aResult = oParser.parse(sUrl, sPattern)
    
    #affichage
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        index = 1
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sTitle = sMovieTitle
            if liste:
                sTitle = sTitle + ' (' + str(index) + ') '
                index = index + 1

            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)

            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
