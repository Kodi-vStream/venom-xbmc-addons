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

SITE_IDENTIFIER = 'streamzer_net'
SITE_NAME = 'Streamzer.net'
SITE_DESC = 'Regarder des films et series en streaming illimite avec Youwatch, VK streaming. Streamzer le streaming sans limite avec Youwatch et VK stream.'

URL_MAIN = 'http://www.streamzer.net/'

MOVIE_MOVIE = ('http://www.streamzer.net/index.php?file=Films&op=classe&secid=&orderby=news&p=1#stream', 'showMovies')
MOVIE_NEWS = ('http://www.streamzer.net/index.php?file=Films&op=classe&secid=&orderby=news&p=1#stream', 'showMovies')
MOVIE_GENRES = ('http://www.streamzer.net/index.php?file=Films&op=classe&secid=&orderby=news&p=1#stream', 'showGenre')
MOVIE_VIEWS = ('http://www.streamzer.net/films-streaming-populaires#stream', 'showMovies')
MOVIE_NOTES = ('http://www.streamzer.net/meilleurs-films-streaming#stream', 'showMovies')

SERIE_SERIES = ('http://www.streamzer.net/index.php?file=Series&op=classe&secid=&orderby=news&p=1#stream', 'showMovies')
SERIE_NEWS = ('http://www.streamzer.net/index.php?file=Series&op=classe&secid=&orderby=news&p=1#stream', 'showMovies')

DOC_NEWS = ('http://www.streamzer.net/index.php?file=Docus&op=classe&secid=&orderby=news&p=1#stream', 'showMovies')
DOC_GENRES = ('http://www.streamzer.net/index.php?file=Docus&op=classe&secid=&orderby=news&p=1#stream', 'docuGenre')
DOC_DOCS = ('http://', 'load')

SPORT_SPORTS = ('http://www.streamzer.net/index.php?file=Replay&op=classe&secid=&orderby=news&p=1#stream', 'showReplay')

MOVIE_NETS = ('http://www.streamzer.net/index.php?file=Videos&op=classe&secid=&orderby=news&p=1#stream', 'showReplay')

URL_SEARCH = ('http://www.streamzer.net/index.php?file=Search&op=mod_search&main=', 'resultSearch')
FUNCTION_SEARCH = 'resultSearch'


def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Films Nouveautés', 'films.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genre', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Series', 'series.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.streamzer.net/index.php?file=Series&op=classe&secid=&orderby=news&p=1#stream')
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Series Genre', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showMovies', 'Documentaires', 'doc.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DOC_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'docuGenre', 'Documentaires Genre', 'genres.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showReplay', 'Sport Replay', 'replay.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.streamzer.net/index.php?file=Replay&op=classe&secid=&orderby=news&p=1#stream')
    oGui.addDir(SITE_IDENTIFIER, 'replayGenre', 'Sport Replay Genre', 'genres.png', oOutputParameterHandler)
    

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NETS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showReplay', 'Buzz', 'buzz.png', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.streamzer.net/index.php?file=Videos&op=classe&secid=&orderby=news&p=1#stream')
    oGui.addDir(SITE_IDENTIFIER, 'buzzGenre', 'Buzz Genre', 'genres.png', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()

    
def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
            sUrl = 'http://www.streamzer.net/index.php?file=Search&op=mod_search&main='+sSearchText
            resultSearch(sUrl)
            oGui.setEndOfDirectory()
            return  
    
    
def resultSearch(sSearch = ''):
    oGui = cGui()  
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sPattern = "<a href='([^<]+)' title=.([^<]+).>.*?<img src='([^<]+)' width='160px'.+?"
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[2]))
            if '/series' in aEntry[0]:
                oGui.addMisc(SITE_IDENTIFIER, 'showSerieHosters', aEntry[1], '', aEntry[2], '', oOutputParameterHandler)
            else:
                oGui.addMisc(SITE_IDENTIFIER, 'showHosters', aEntry[1], '', aEntry[2], '', oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'resultSearch', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    if not sSearch:       
        oGui.setEndOfDirectory()
 
def docuGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ["Astro-Science","http://www.streamzer.net/documentaires-astro-science"] )
    liste.append( ["Fait Divers-Tragédie","http://www.streamzer.net/documentaires-fait-divers-tragedie"] )
    liste.append( ["Histoire-Civilisation","http://www.streamzer.net/documentaires-histoire-civilisation"] )
    liste.append( [ "Légende-Mythe","http://www.streamzer.net/documentaires-legende-mythe"] )
    liste.append( ["Musique","http://www.streamzer.net/documentaires-musique"] )
    liste.append( ["Nature","http://www.streamzer.net/documentaires-nature"] )
    liste.append( ["Paranormal","http://www.streamzer.net/documentaires-paranormal"] )
    liste.append( ["Science","http://www.streamzer.net/documentaires-science"] )
    liste.append( ["Société","http://www.streamzer.net/documentaires-societe"] )
    liste.append( ["Sport","http://www.streamzer.net/documentaires-sport"] )
    liste.append( ["UFO-OVNI","http://www.streamzer.net/documentaires-ufo-ovni"] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
    
def replayGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    liste = []
    liste.append( ['Équipe du Dimanche','http://www.streamzer.net/replay-equipe-du-dimanche'] )
    liste.append( ['Téléfoot','http://www.streamzer.net/replay-telefoot'] )
    liste.append( ['Jour de foot','http://www.streamzer.net/replay-jour-de-foot'] )
    liste.append( ['Canal Football Club','http://www.streamzer.net/replay-canal-football-club'] )
    liste.append( ['J+1','http://www.streamzer.net/replay-j-plus-1'] )
    liste.append( ['Les Spécialistes Ligue 1','http://www.streamzer.net/replay-specialistes-ligue-1'] )
    liste.append( ['The Specialists','http://www.streamzer.net/replay-the-specialists'] )
    liste.append( ['Champions League','http://www.streamzer.net/replay-champions-league'] )
    liste.append( ['Europa League','http://www.streamzer.net/replay-europa-league'] )
    liste.append( ['Foot Europe Express','http://www.streamzer.net/replay-foot-europe-express'] )   
    liste.append( ['Liga BBVA','http://www.streamzer.net/replay-liga-bbva'] )
    liste.append( ['Premier League','http://www.streamzer.net/replay-premier-league'] )
    liste.append( ['Ligue 1','http://www.streamzer.net/replay-ligue-1'] )
    liste.append( ['Serie A','http://www.streamzer.net/replay-seria-a'] )
    liste.append( ['Bundesliga','http://www.streamzer.net/replay-bundesliga'] )
    liste.append( ['Premier League World','http://www.streamzer.net/replay-premier-league-world'] )
    liste.append( ['Rugby: Top 14','http://www.streamzer.net/replay-top-14'] )
    liste.append( ['Rugby: Les Spécialistes Rugby','http://www.streamzer.net/replay-specialistes-rugby'] )
    liste.append( ['F1: Grands-Prix F1','http://www.streamzer.net/replay-grands-prix-f1'] )
    liste.append( ['F1: Formula One','http://www.streamzer.net/replay-formula-one'] )
    liste.append( ['F1: Les spécialistes F1','http://www.streamzer.net/replay-specialistes-f1'] )
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showReplay', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
 
    sPattern = "<td class='td-categ' style='height:21px;'><a href='([^<]+)'><span style='font-size:12px;'>(.+?)</td>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            siteUrl = URL_MAIN+aEntry[0]
            sTitle = str(aEntry[1]).replace('</a>', '')
            sTitle = sTitle.decode('latin-1').encode("utf-8")
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
           
    oGui.setEndOfDirectory()
    
def buzzGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
 
    sPattern = "<td class='td-categ' style='height:21px;'><a href='([^<]+)'><span style='font-size:12px;'>(.+?)</td>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            siteUrl = URL_MAIN+aEntry[0]
            sTitle = str(aEntry[1]).replace('</a>', '')
            sTitle = sTitle.decode('latin-1').encode("utf-8")
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', siteUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showReplay', sTitle, 'genres.png', oOutputParameterHandler)
           
    oGui.setEndOfDirectory()

def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sPattern = "<img src='([^<]+)' width='160px' height='213px'>.+?<a href=\"([^<]+)\"><span style='font-size:20px; color:#2793E9'>(.+?)</span></a>.+?<span style='color:#000000;'>(.+?)<span>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[2].decode('latin-1').encode("utf-8")
            sTitle=re.sub('(.*)(\[.*\])','\\1 [COLOR azure]\\2[/COLOR]', str(sTitle))
            sMovieTitle=re.sub('(\[.*\])','', str(sTitle))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            if '/series/' in aEntry[1]:
                oGui.addTV(SITE_IDENTIFIER, 'showSerieHosters', sTitle, '', aEntry[0], aEntry[3], oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], aEntry[3], oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showReplay():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
 
    sPattern = "<img src='([^<]+)' width='.+?px' height='.+?px'>.+?<a href=\"([^<]+)\"><span style='font-size:.+?px; color:#2793E9'>(.+?)</span></a>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sTitle = aEntry[2].decode('latin-1').encode("utf-8")
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            oOutputParameterHandler.addParameter('sThumbnail', str(aEntry[0]))
            if 'Videos' in sUrl:
                oGui.addMisc(SITE_IDENTIFIER, 'showHosters2', sTitle, '', aEntry[0], '', oOutputParameterHandler)
            else:
                oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, '', aEntry[0], '', oOutputParameterHandler)
        
        cConfig().finishDialog(dialog)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showReplay', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    sPattern = 'background-color:#969696; color:#FFFFFF;.+?<a href="([^<]+)"<span style="display:inline; padding-left: 3px; padding-right: 3px; border : 1px solid #CCCCCC; background-color:#F4F4F4; color:#333333;">.+?</span></a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return URL_MAIN+aResult[1][0]

    return False
    

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace("<a href='http://www.youtube.com/", "")


    sPattern = "<span style='font-size:10px; color: #CD371A;'><b>(.+?)</b><span>|<td class='td-liens'><a href='([^<]+)' target='player'>(.+?)<div class='mirroir'>([^<]+)"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            sHosterUrl = cUtil().unescape(str(aEntry[1]))
            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            
            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addDir(SITE_IDENTIFIER, 'showHosters', '[COLOR red]'+str(aEntry[0])+'[/COLOR]', 'host.png', oOutputParameterHandler)
                   
        
            if (oHoster != False):
                sMovieTitle=re.sub(r'\[.*\]',r'',sMovieTitle)
                if 'replay' in sUrl:
                    sTitle = str(sMovieTitle)+' - '+str(aEntry[2])+' - '+str(aEntry[3])
                else:
                    sTitle = str(sMovieTitle) + ' - ' + str(aEntry[3])
                
                sTitle = sTitle.decode('latin-1').encode("utf-8")
                    
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
    
def showHosters2():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<iframe src=\'http://www.canalflux.com/pub.html\'','').replace('<iframe src=\'http://www.webzer.fr/pub.html\'','').replace('<iframe src=\'http://www.webzer.fr/pub2.html\'','')


    sPattern = '<iframe.+?src=[\'|"](.+?)[\'|"]'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)    
 
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            #mediaID=re.findall('//([^<]+)',aEntry)[0]
            aEntry = aEntry.replace('http://', '')
            aEntry = aEntry.replace('www.', '')
            aEntry = aEntry.replace('//', '')
            aEntry = 'http://www.'+aEntry
            
            #sHosterUrl='http://'+mediaID
            #oHoster = __checkHoster(sHosterUrl)
            sHosterUrl = str(aEntry)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
        
            if (oHoster != False):
                sTitle = str(sMovieTitle)
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 

        cConfig().finishDialog(dialog)   

    oGui.setEndOfDirectory()


def showSerieHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumbnail = oInputParameterHandler.getValue('sThumbnail')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace("<a href='http://www.youtube.com/", "").replace("<a href='http://www.allocine.fr/", "")


    sPattern = "<span style='font-size:11px; color:#333333;'><b>(.+?)</b></span>|<a href='([^<]+)' target='player'>(.+?)</td>"
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

            sHosterUrl = str(aEntry[1])
            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            
            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                oOutputParameterHandler.addParameter('sThumbnail', str(sThumbnail))
                oGui.addDir(SITE_IDENTIFIER, 'showHosters', '[COLOR red]'+str(aEntry[0])+'[/COLOR]', 'host.png', oOutputParameterHandler)
                   
        
            if (oHoster != False):
                sTitle=re.sub(r'\[.*\]',r'',sMovieTitle)
                sTitle = str(sTitle) + ' - ' + str(aEntry[2])
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumbnail) 

        cConfig().finishDialog(dialog)

    oGui.setEndOfDirectory()
