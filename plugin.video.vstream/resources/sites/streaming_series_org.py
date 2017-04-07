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

SITE_IDENTIFIER = 'streaming_series_org'
SITE_NAME = 'Streaming-Séries'
SITE_DESC = 'Séries en streaming vf gratuitement sur Streaming-Séries'

URL_MAIN = 'http://www.streamingseries.info/'

SERIE_SERIES = (URL_MAIN, 'showMovies')
SERIE_NEWS = (URL_MAIN, 'showMovies')
SERIE_VIEWS = (URL_MAIN + 'series-les-plus-vues/', 'showMovies')
SERIE_COMMENTS = (URL_MAIN + 'series-les-plus-commentees/', 'showMovies')
SERIE_NOTES = (URL_MAIN + 'series-les-plus-aimees/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSerieSearch', 'Recherche', 'search.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries (Derniers ajouts)', 'series_news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VIEWS[1], 'Séries (Les plus Vues)', 'series_views.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_COMMENTS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_COMMENTS[1], 'Séries (Les plus Commentés)', 'series_comments.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NOTES[1], 'Séries (Les mieux Notés)', 'series_notes.png', oOutputParameterHandler)
 
    oGui.setEndOfDirectory()
 
def showSerieSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = URL_MAIN + '?s='+sSearchText  
            showMovies(sUrl)
            oGui.setEndOfDirectory()
            return
            
def showGenres():
    oGui = cGui()
 
    liste = []
    liste.append( ['Action',URL_MAIN + '/category/action/'] )
    liste.append( ['Afro',URL_MAIN + '/category/afro/'] )
    liste.append( ['Animation',URL_MAIN + '/category/animation/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + '/category/arts-martiaux/'] )
    liste.append( ['Aventure',URL_MAIN + '/category/aventure/'] )
    liste.append( ['Comédie',URL_MAIN + '/category/comedie/'] )
    liste.append( ['Disney',URL_MAIN + '/category/disney/'] )
    liste.append( ['Documentaire',URL_MAIN + '/category/documentaire/'] )
    liste.append( ['Drame',URL_MAIN + '/category/drame/'] )  
    liste.append( ['Espionnage',URL_MAIN + '/category/espionnage/'] )
    liste.append( ['Famille',URL_MAIN + '/category/famille/'] ) 
    liste.append( ['Fantastique',URL_MAIN + '/category/fantastique/'] ) 
    liste.append( ['Guerre',URL_MAIN + '/category/guerre/'] )
    liste.append( ['Historique',URL_MAIN + '/category/historique/'] )         
    liste.append( ['Horreur',URL_MAIN + '/category/horreur/'] )
    liste.append( ['Musical',URL_MAIN + '/category/musical/'] ) 
    liste.append( ['Non classé',URL_MAIN + '/category/non-classe/'] )  
    liste.append( ['Policier',URL_MAIN + '/category/policier/'] )
    liste.append( ['Romance',URL_MAIN + '/category/romance/'] )
    liste.append( ['Science fiction',URL_MAIN + '/category/science-fiction/'] )
    liste.append( ['Spectacle',URL_MAIN + '/category/spectacle/'] )
    liste.append( ['Thriller',URL_MAIN + '/category/thriller/'] )
    liste.append( ['Western',URL_MAIN + '/category/western/'] )
               
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
    sHtmlContent = sHtmlContent.replace('//ad.advertstream.com/', '').replace('http://www.adcash.com/', '').replace('http://regie.espace-plus.net/', '')
    sPattern = '<div class="moviefilm"><a href=".+?"><img src="([^<]+)" alt=".+?" height=".+?" width=".+?" /></a><div class="movief"><a href="([^<]+)">([^<]+)</a></div><div class="movies"><small>(.+?)</small></div></div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            #Si recherche et trop de resultat, on nettoye
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch.replace(URL_SEARCH[0],''),aEntry[2]) == 0:
                    continue
                    
            sThumb = aEntry[0].replace('-119x125','') #qual thumbs
            sSmall = aEntry[3].replace('<span class="likeThis">', '').replace('</span>', '')
            sSmall = sSmall.replace('Yorum','Commentaire')
            sTitle = aEntry[2]+' - [COLOR azure]'+sSmall+'[/COLOR]'
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[2]))
            oOutputParameterHandler.addParameter('sThumbnail', sThumb)
            if 'series' in sUrl:
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                oGui.addTV(SITE_IDENTIFIER, 'showSeries', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                sDisplayTitle = cUtil().DecoTitle(sTitle)
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

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

    sUrl = sUrl + '100/'
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<a href="([^<]+)"><span>([^"]+(?<!Infos série))</span></a>' #vire non épisode
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
            sDisplayTitle = cUtil().DecoTitle(sTitle)
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumbnail, '', oOutputParameterHandler)

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

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src="//www.facebook.com/','')
    sHtmlContent = sHtmlContent.replace('\r','')

    sPattern = '(VF|VOSTFR)<\/b><\/p>|<iframe.+?src=[\'|"](.+?)[\'|"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
                
            #langue
            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addMisc(SITE_IDENTIFIER, 'showSeries', '[COLOR red]'+str(aEntry[0])+'[/COLOR]', 'series.png', sThumbnail, '', oOutputParameterHandler)
            #episode
            else:
                sHosterUrl = str(aEntry[1])

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    sDisplayTitle = cUtil().DecoTitle(sMovieTitle)
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
