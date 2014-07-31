#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
import re

SITE_IDENTIFIER = 'streamzer_net'
SITE_NAME = 'streamzer.net'

URL_MAIN = 'http://www.streamzer.net/'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.streamzer.net/index.php?file=Films&op=classe&secid=&orderby=news&p=1#stream')
    __createMenuEntry(oGui, 'showMovies', 'Films', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.streamzer.net/index.php?file=Films&op=classe&secid=&orderby=news&p=1#stream')
    __createMenuEntry(oGui, 'showGenre', 'Films Genre', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.streamzer.net/index.php?file=Series&op=classe&secid=&orderby=news&p=1#stream')
    __createMenuEntry(oGui, 'showMovies', 'Series', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.streamzer.net/index.php?file=Series&op=classe&secid=&orderby=news&p=1#stream')
    __createMenuEntry(oGui, 'showGenre', 'Series Genre', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.streamzer.net/index.php?file=Docus&op=classe&secid=&orderby=news&p=1#stream')
    __createMenuEntry(oGui, 'showMovies', 'Documentaires', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.streamzer.net/index.php?file=Docus&op=classe&secid=&orderby=news&p=1#stream')
    __createMenuEntry(oGui, 'docuGenre', 'Documentaires Genre', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.streamzer.net/index.php?file=Replay&op=classe&secid=&orderby=news&p=1#stream')
    __createMenuEntry(oGui, 'showReplay', 'Sport Replay', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.streamzer.net/index.php?file=Replay&op=classe&secid=&orderby=news&p=1#stream')
    __createMenuEntry(oGui, 'replayGenre', 'Sport Replay Genre', '', '', oOutputParameterHandler)
    

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.streamzer.net/index.php?file=Videos&op=classe&secid=&orderby=news&p=1#stream')
    __createMenuEntry(oGui, 'showReplay', 'Buzz', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.streamzer.net/index.php?file=Videos&op=classe&secid=&orderby=news&p=1#stream')
    __createMenuEntry(oGui, 'buzzGenre', 'Buzz Genre', '', '', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, sThumbnail, sDesc, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGuiElement.setThumbnail(sThumbnail)
    oGuiElement.setDescription(cUtil().removeHtmlTags(sDesc))
    oGui.addFolder(oGuiElement, oOutputParameterHandler)
 
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
        __createMenuEntry(oGui, 'showMovies', sTitle, '', '', oOutputParameterHandler)
       
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
        __createMenuEntry(oGui, 'showReplay', sTitle, '', '', oOutputParameterHandler)
       
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
            __createMenuEntry(oGui, 'showMovies', sTitle, '', '', oOutputParameterHandler)
           
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
            __createMenuEntry(oGui, 'showReplay', sTitle, '', '', oOutputParameterHandler)
           
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
        for aEntry in aResult[1]:
            sTitle = aEntry[2].decode('latin-1').encode("utf-8")

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            __createMenuEntry(oGui, 'showHosters', sTitle, aEntry[0], aEntry[3], oOutputParameterHandler)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            __createMenuEntry(oGui, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', '', '', oOutputParameterHandler)

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
        for aEntry in aResult[1]:
            sTitle = aEntry[2].decode('latin-1').encode("utf-8")
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[1]))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            if 'Videos' in sUrl:
                __createMenuEntry(oGui, 'showHosters2', sTitle, aEntry[0], '', oOutputParameterHandler)
            else:
                __createMenuEntry(oGui, 'showHosters', sTitle, aEntry[0], '', oOutputParameterHandler)
            
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            __createMenuEntry(oGui, 'showReplay', '[COLOR teal]Next >>>[/COLOR]', '', '', oOutputParameterHandler)

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

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();


    sPattern = "<span style='font-size:10px; color: #CD371A;'><b>(.+?)</b><span>|<a href='([^<]+)' target='player'>(.+?)<div class='mirroir'>([^<]+)"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = str(aEntry[1])
            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            
            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                __createMenuEntry(oGui, 'showHosters', '[COLOR red]'+str(aEntry[0])+'[/COLOR]', '', '', oOutputParameterHandler)
                   
        
            if (oHoster != False):
                sMovieTitle=re.sub(r'\[.*\]',r'',sMovieTitle)
                if 'replay' in sUrl:
                    sTitle = str(sMovieTitle)+' - '+str(aEntry[2])+' - '+str(aEntry[3])
                else:
                    sTitle = str(sMovieTitle) + ' - ' + str(aEntry[3])
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl) 

    oGui.setEndOfDirectory()
    
def showHosters2():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();


    sPattern = '<iframe.+?src="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            mediaID=re.findall('//([^<]+)',aEntry)[0]
            sHosterUrl='http://'+mediaID
            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
        
            if (oHoster != False):
                sTitle = str(sMovieTitle)
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl)    

    oGui.setEndOfDirectory()