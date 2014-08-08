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
import string

SITE_IDENTIFIER = 'anime_no_paradise_com'
SITE_NAME = 'anime-no-paradise.com'

URL_MAIN = 'http://www.anime-no-paradise.com/'

def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.anime-no-paradise.com/page-7751108.html')
    __createMenuEntry(oGui, 'showMovies', 'Animes', 'animes.png', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.anime-no-paradise.com/page-7751108.html')
    __createMenuEntry(oGui, 'showAZ', 'Animes A-Z', 'az.png', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.anime-no-paradise.com/page-7947543.html')
    __createMenuEntry(oGui, 'showMovies', 'Animes Films & OAVS', 'animes.png', '', '', oOutputParameterHandler)
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://www.anime-no-paradise.com/page-7947543.html')
    __createMenuEntry(oGui, 'showAZ', 'Animes Films & OAVS A-Z', 'az.png', '', '', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGuiElement.setIcon(sIcon)
    oGuiElement.setThumbnail(sThumbnail)
    oGuiElement.setDescription(cUtil().removeHtmlTags(sDesc))
    
    oGui.addFolder(oGuiElement, oOutputParameterHandler)
 
def showAZ():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('AZ', '.')
    __createMenuEntry(oGui, 'showMoviesAZ', '.', 'az.png', '', '', oOutputParameterHandler)          
    for i in string.ascii_uppercase:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('AZ', i)
        __createMenuEntry(oGui, 'showMoviesAZ', i, 'az.png', '', '', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 

def showMoviesAZ():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sAZ = oInputParameterHandler.getValue('AZ')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sPattern = '<a href="([^<]+)" style=".*?line-height: 21px;"><font color="#234656">([^<]+)</font></a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if len(sAZ)>0 and aEntry[1].upper()[0] == sAZ :

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
                oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
                __createMenuEntry(oGui, 'showHosters', aEntry[1], 'animes.png', '', '', oOutputParameterHandler)
            

    oGui.setEndOfDirectory()
    
def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
 
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    sPattern = '<a href="([^<]+)" style=".*?line-height: 21px;"><font color="#234656">([^<]+)</font></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):    
        for aEntry in aResult[1]:
            
            sTitle = aEntry[1].decode('latin-1').encode("utf-8")
            sUrl = aEntry[0].replace(' ', '%20').lower()
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle))
            __createMenuEntry(oGui, 'showHosters', sTitle, 'animes.png', '', '', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = sUrl.replace(' ', '%20').lower()
    
    iPage = 1
    if (oInputParameterHandler.exist('page')):
            iPage = oInputParameterHandler.getValue('page')
            
    mUrl = sUrl + str(iPage)

    oRequestHandler = cRequestHandler(mUrl)
    sHtmlContent = oRequestHandler.request();
    sHtmlContent = sHtmlContent.replace('<param name="src" value="http://anme-no-paradise.chatango.com/group">', '')


    sPattern = '<a href=".+?" class="titreArticle" title=".+?">([^<]+)</a>.+?<span style="font-size: 12pt; color: #ff6600;">([^<]+)</span>|<param name="src" value="(.+?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sHosterUrl = str(aEntry[2])
            #oHoster = __checkHoster(sHosterUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            
            if aEntry[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(sUrl))
                oOutputParameterHandler.addParameter('sMovieTitle', str(sMovieTitle))
                __createMenuEntry(oGui, 'showHosters', '[COLOR red]'+str(aEntry[0])+'[/COLOR]', 'host.png', '', '', oOutputParameterHandler)
                   
        
            if (oHoster != False):
                sTitle = str(aEntry[0]) + ' - ' + str(aEntry[1])
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '') 
                
        sNextPage = True
        if (sNextPage != False):
            iNextPage = int(iPage) + 1
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('page', iNextPage)
            __createMenuEntry(oGui, 'showHosters', '[COLOR teal]Next >>>[/COLOR]', 'next.png', '', '', oOutputParameterHandler)


    oGui.setEndOfDirectory()
    
def __checkForNextPage(ipage, sUrl):
    sPattern = 'anime-no-paradise.com/tag/.+?/(.{1,2})'
    oParser = cParser()
    aResult = oParser.parse(sUrl, sPattern)
    print aResult
    if (aResult[0] == True):
        return True

    return False