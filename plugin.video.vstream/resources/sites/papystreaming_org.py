#-*- coding: utf-8 -*-
#johngf.
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
import re,xbmc

SITE_IDENTIFIER = 'papystreaming_org'  
SITE_NAME = 'Papystreaming.org' 
SITE_DESC = 'films et series en streaming'

URL_MAIN = 'http://papystreaming.org/'

MOVIE_MOVIE = (URL_MAIN + 'film-streaming/' , 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'nouveaux-films/','showMovies')
MOVIE_COMMENTS = (URL_MAIN + 'populaire/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'de-visite/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'de-vote/', 'showMovies')
MOVIE_GENRES = (True, 'showGenre')

SERIE_SERIES = (URL_MAIN + 'series-streaming/' , 'showSeries')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH2 = (URL_MAIN + '?s=', 'showSeries')
FUNCTION_SEARCH = 'showMovies'
#serie et film melangé sur certaine fonction tri obligatoire qui bloque l'optimisation

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMSearch', 'Recherche film', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSSearch', 'Recherche serie', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler) 
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Series', 'series.png', oOutputParameterHandler)   

    oGui.setEndOfDirectory()
    
def showMenuFilms():
    oGui = cGui()
       
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Films', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films derniers ajouts', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_COMMENTS[1], 'Films les plus commentés', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films les plus vues', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films les mieux notés', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genre', 'genres.png', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()
    
def showMenuSeries():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Series', 'series.png', oOutputParameterHandler) 
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'populaire/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Series les plus commentés', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'de-visite/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Series les plus vues', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'de-vote/')
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Series les mieux notés', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def showGenre():
    oGui = cGui()
 
    liste = []
    liste.append( ['Action',URL_MAIN + 'category/action/'] )
    liste.append( ['Action_Aventure',URL_MAIN + 'category/action-adventure/'] )
    liste.append( ['Animation',URL_MAIN + 'category/animation/'] )
    liste.append( ['Aventure',URL_MAIN + 'category/aventure/'] )
    liste.append( ['Comédie',URL_MAIN + 'category/comedie/'] )
    liste.append( ['Crime',URL_MAIN + 'category/crime/'] )
    liste.append( ['Documentaire',URL_MAIN + 'category/documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'category/drame/'] )
    liste.append( ['Familial',URL_MAIN + 'category/familial/'] )
    liste.append( ['Fantastique',URL_MAIN + 'category/fantastique/'] )  
    liste.append( ['Guerre',URL_MAIN + 'category/guerre/'] )
    liste.append( ['Histoire',URL_MAIN + 'category/histoire/'] )
    liste.append( ['Horreur',URL_MAIN + 'category/horreur/'] )   
    liste.append( ['Musique',URL_MAIN + 'category/musique/'] )        
    liste.append( ['Mystère',URL_MAIN + 'category/mystere/'] )
    liste.append( ['Romance',URL_MAIN + 'category/romance/'] )
    liste.append( ['Science_Fiction',URL_MAIN + 'category/science-fiction/'] )
    liste.append( ['Science_Fiction_Fantastique',URL_MAIN + 'category/science-fiction-fantastique/'] )
    liste.append( ['Thriller',URL_MAIN + 'category/thriller/'] )
    liste.append( ['Western',URL_MAIN + 'category/western/'] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

       
    oGui.setEndOfDirectory() 

def showMSearch(): 
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl) 
        oGui.setEndOfDirectory()
        return
        
def showSSearch(): 
    oGui = cGui()
    sSearchText = oGui.showKeyBoard() 
    if (sSearchText != False):
        sUrl = URL_SEARCH2[0] + sSearchText
        showSeries(sUrl) 
        oGui.setEndOfDirectory()
        return 
        
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
    
    sPattern = '<a class="poster" href="([^"]+)" title="([^"]+)".+?<img src="([^"]+)"' 
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sUrl = aEntry[0]
            if 'serie' in sUrl:
                continue
            sThumb = aEntry[2]
            sTitle =  aEntry[1]

            sDisplayTitle = cUtil().DecoTitle(sTitle)
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumb, '', oOutputParameterHandler)


        cConfig().finishDialog(dialog)
           
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()        
    
def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="current">.+?<\/span><\/li><li><a href="([^"]+)"'
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
    sHtmlContent = sHtmlContent.replace('http://www.google.com/s2/favicons?domain=','')
    oParser = cParser()
        
    papylink = ''
    sPattern = '<script type="text/javascript">.+?{"link":"([^"]+)","type":".+?"}'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        papylink = aResult[1][0]
        if not papylink.startswith('http'):
           papylink = 'http:' + aResult[1][0]
           
    sPattern = '<img class="btn btn-serv" src="([^"]+)".+?<img class="btn-language" src="([^"]+)"/>.+?<td>(.+?)</td>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            
            if 'vf' in aEntry[1]:
                sLang = 'Vf' 
            else:
                sLang = 'Vostfr'
            
            
            if 'papystreaming' in aEntry[0]:
                sDisplayTitle = cUtil().DecoTitle('[' + aEntry[2] + '-' + sLang + ']' + ' ' + sMovieTitle)
                sDisplayTitle = sDisplayTitle + ' [COLOR skyblue]PapyLink[/COLOR]'
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', papylink)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
                oGui.addMisc(SITE_IDENTIFIER, 'ShowPapyLink', sDisplayTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
            else:
                sHosterUrl = aEntry[0]
                
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    sDisplayTitle = cUtil().DecoTitle('[' + aEntry[2] + '-' + sLang + ']' + ' ' + sMovieTitle)
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
       
    oGui.setEndOfDirectory()
    
def ShowPapyLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
        
    sPattern = '"file":"([^"]+)",.+?,"label":"(\d+p)"'   #'<iframe.+?src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = aEntry[0]
            sLabel = aEntry[1]
            
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle + '[' + sLabel + ']')
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)
       
    oGui.setEndOfDirectory()  
    
def showSaisons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()
    
    sSyn = ''
    sPattern = '<p class=".+?">([^<]+)<\/p>'
    aResult = oParser.parse(sHtmlContent,sPattern)
    if aResult[0]:
        sSyn = aResult[1][0]
        
    sPattern = '<a class="expand-season-trigger" data-toggle="collapse" href="([^"]+)".+?<\/span>([^<]+)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                        
            vUrl = sUrl + aEntry[0]
            sSaison = sMovieTitle + aEntry[1]
            sSaison = sSaison.replace('N/A','')
            sFilter = oParser.getNumberFromString(aEntry[1])
            sFilter = 'saison-' + sFilter + '/'
            
            sDisplayTitle = cUtil().DecoTitle(sSaison)   
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', vUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sSyn', sSyn)
            oOutputParameterHandler.addParameter('sFilter', sFilter)
            oGui.addTV(SITE_IDENTIFIER, 'showEpisodes', sDisplayTitle, '', sThumbnail, sSyn, oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
           
    oGui.setEndOfDirectory()
    
def showEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')
    sFilter = oInputParameterHandler.getValue('sFilter')
    sSyn = oInputParameterHandler.getValue('sSyn')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    oParser = cParser()

    sPattern = '<div class="larr episode-header">.+?<a href="([^"]+)" title="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                        
            sUrl = aEntry[0]
            sTitle = sMovieTitle + aEntry[1]
            sTitle = sTitle.replace('N/A','').replace(',','')
            if not sFilter in sUrl:
               continue
            sDisplayTitle = cUtil().DecoTitle(sTitle)   
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, sSyn, oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
           
    oGui.setEndOfDirectory()    

def showSeries(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<a class="poster" href="([^"]+)" title="([^"]+)".+?<img src="([^"]+)"'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            sUrl = aEntry[0]
            if 'film' in sUrl:
                continue
            sThumb = aEntry[2]
            sTitle =  aEntry[1]

            sDisplayTitle = cUtil().DecoTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, 'series.png', sThumb, '', oOutputParameterHandler)

        cConfig().finishDialog(dialog)
           
        sNextPage = __checkForNextPage2(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showSeries', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()
        
def __checkForNextPage2(sHtmlContent):
    sPattern = '<span class="current">.+?<\/span><\/li><li><a href="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False
