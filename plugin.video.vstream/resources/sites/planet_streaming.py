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
from resources.lib.player import cPlayer
import re,urllib2,urllib


SITE_IDENTIFIER = 'planet_streaming'
SITE_NAME = 'Planet Streaming'
SITE_DESC = 'Film de 1900 jusqu à 2016, contient du HD'

URL_MAIN = 'http://www.planet-streaming.com/'
 
MOVIE_NEWS = (URL_MAIN + 'regarder-film/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'regarder-film/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'xfsearch/hd/', 'showMovies')
 
MOVIE_GENRES = (True, 'showGenre')
 
URL_SEARCH = ('' , 'showMovies')
FUNCTION_SEARCH = 'showMovies'
   
def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveautes', 'news.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films HD', 'top.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MOVIE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MOVIE[1], 'Tout Les Films', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genre', 'genres.png', oOutputParameterHandler)
           
    oGui.setEndOfDirectory()
 
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        showMovies(sSearchText)
        oGui.setEndOfDirectory()
        return 

def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Animation',URL_MAIN + 'regarder-film/animation/'] )    
    liste.append( ['Action',URL_MAIN + 'regarder-film/action/'] )
    liste.append( ['Arts Martiaux',URL_MAIN + 'regarder-film/arts-martiaux/"'] )
    liste.append( ['Aventure',URL_MAIN + 'regarder-film/aventure/'] )
    liste.append( ['Biopic',URL_MAIN + 'regarder-film/biopic/'] )
    liste.append( ['Comedie Musicale',URL_MAIN + 'regarder-film/comedie-musicale/'] )
    liste.append( ['Comedie',URL_MAIN + 'regarder-film/comedie/'] )
    liste.append( ['Comedie Dramatique',URL_MAIN + 'regarder-film/comedie-dramatique/e'] )
    liste.append( ['Documentaire',URL_MAIN + 'regarder-film/documentaire/'] )
    liste.append( ['Drame',URL_MAIN + 'regarder-film/drame/'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'regarder-film/epouvante-horreur/'] )
    liste.append( ['Espionage',URL_MAIN + 'regarder-film/espionnage/'] )  
    liste.append( ['Fantastique',URL_MAIN + 'regarder-film/fantastique/'] )
    liste.append( ['Famille',URL_MAIN + 'regarder-film/famille/'] )
    liste.append( ['Guerre',URL_MAIN + 'regarder-film/guerre/'] )
    liste.append( ['Historique',URL_MAIN + 'regarder-film/historique/'] )
    liste.append( ['Musical',URL_MAIN + 'regarder-film/musical/'] )
    liste.append( ['Peplum',URL_MAIN + 'regarder-film/peplum/'] )
    liste.append( ['Policier',URL_MAIN + 'regarder-film/policier/r'] )
    liste.append( ['Romance',URL_MAIN + 'regarder-film/romance/'] )
    liste.append( ['Sciense Fiction',URL_MAIN + 'regarder-film/science-fiction/'] )
    liste.append( ['Thriller',URL_MAIN + 'regarder-film/thriller/'] )
    liste.append( ['Western',URL_MAIN + 'regarder-film/western/'] )
    liste.append( ['Divers',URL_MAIN + 'regarder-film/divers//'] )
               
    for sTitle,sUrl in liste:
       
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory()
    

def showMovies(sSearch = ''):
    oGui = cGui()
    
    if sSearch:

        sUrl = URL_SEARCH[0]
        
        #sPOST = 'do=search&subaction=search&story=' + sSearch
        #print sUrl
        #print sPOST
        
        oRequestHandler = cRequestHandler(URL_MAIN)
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        #oRequestHandler.addParameters('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
        oRequestHandler.addParameters('Content-Type', 'application/x-www-form-urlencoded')
        oRequestHandler.addParameters('Referer', 'http://www.planet-streaming.com/')
        oRequestHandler.addParameters('do', 'search')
        oRequestHandler.addParameters('subaction', 'search')
        oRequestHandler.addParameters('story', sSearch)
        sHtmlContent = oRequestHandler.request()
        
        # request = urllib2.Request(sUrl,sPOST)
        # request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
        # request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        # request.add_header('Referer', 'http://www.planet-streaming.com/')
        
        # reponse = urllib2.urlopen(request)
        # sHtmlContent = reponse.read()
        # reponse.close()
        
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()
    
    #print sUrl

    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
    
    oParser = cParser()  
    
    sPattern = '<div class="fullstream fullstreaming">\s*<img src="([^><"]+)"[^<>]+alt="([^"<>]+)".+?<h3 class="mov-title"><a href="([^><"]+)">.+?<strong>Version<\/strong>(.+?)<hr'

    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
           
            sThumbnail = aEntry[0]
            siteUrl = aEntry[2]
            sTitle = str(aEntry[1])
            sQual = cUtil().removeHtmlTags(str(aEntry[3]))
            sQual = sQual.replace(':','').replace(' ','')
            
            sDisplayTitle = '[' + sQual + '] ' + sTitle
            sDisplayTitle = cUtil().DecoTitle(sDisplayTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumbnail', sThumbnail)

            if '/seriestv/' in sUrl or 'saison' in siteUrl or re.match('.+?saison [0-9]+',sTitle,re.IGNORECASE):
                oGui.addTV(SITE_IDENTIFIER, 'serieHosters', sDisplayTitle, '', sThumbnail,'', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumbnail, '', oOutputParameterHandler)
           
        cConfig().finishDialog(dialog)
 
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]' , oOutputParameterHandler)
 
    if not sSearch:
        oGui.setEndOfDirectory()
         
def __checkForNextPage(sHtmlContent):
    
    sPattern = '<a href="([^<>"]+)">Suivant &#8594;<\/a>'
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
    sHtmlContent = oRequestHandler.request()

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
    
    oParser = cParser()
    
    #pour accelerer traitement
    sPattern = '<div id="fsElementsContainer">(.+?)<div class="series-player">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContentListFile = aResult[1][0]     
        
    sPattern = '<\/i> (VOSTFR|VF) *<\/div>|<a href="([^<>"]+)".+?<\/i> EPS ([0-9]+) |<a onclick="javascript:return false;" href="#" title="(.+?)" data-rel="episode([0-9]+)" class="fstab">'
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
                sMovieTitle2 = sMovieTitle + 'episode ' + aEntry[2]
                #sMovieTitle2 = re.sub(' en (VOSTFR|VF)','',sMovieTitle2)
                sDisplayTitle = cUtil().DecoTitle(sMovieTitle2)
        
                if (oHoster != False):
                    oHoster.setDisplayName(sDisplayTitle)
                    oHoster.setFileName(sMovieTitle2)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)

            elif aEntry[3]:
                    sPattern = '<div id="episode' + str(aEntry[4]) + '" class="fullsfeature">(.+?)<\/ul>'
                    aResult3 = oParser.parse(sHtmlContentListFile, sPattern)

                    if (aResult3[0] == True):
                        sPattern = '<a href="([^<>"]+?)" target="seriePlayer" class="fsctab">'
                        aResult2 = oParser.parse(aResult3[1][0], sPattern)

                        if (aResult2[0] == True):
                            for aEntry2 in aResult2[1]:
                                sMovieTitle2 = str(sMovieTitle) + ' '+  str(aEntry[3])
                                sDisplayTitle = cUtil().DecoTitle(sMovieTitle2)
                                
                                sHosterUrl = aEntry2
                                oHoster = cHosterGui().checkHoster(sHosterUrl)
                        
                                if (oHoster != False):
                                    oHoster.setDisplayName(sDisplayTitle)
                                    oHoster.setFileName(sMovieTitle2)
                                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail)              

        cConfig().finishDialog(dialog)
                
    oGui.setEndOfDirectory()
