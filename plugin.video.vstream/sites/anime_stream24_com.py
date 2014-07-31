from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'anime_stream24_com'
SITE_NAME = 'Anime-Stream24.com'

URL_MAIN = 'http://www.anime-stream24.com'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    __createMenuEntry(oGui, 'showAnimesAlphabetic', 'Animes von A - Z', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    __createMenuEntry(oGui, 'showCurrentMovies', 'Aktuelle Anime Folgen', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showCurrentMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<h2>Aktuelle Anime Folgen</h2>(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        sPattern = "<a href='([^']+)'>(.*?)<"
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showHosters')
                oGuiElement.setTitle(str(aEntry[1]))

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
		oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showAnimesAlphabetic():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<h2>Animes von A - Z</h2>(.*?)</select>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        sPattern = "<option value='([^']+)'>(.*?)<"
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showMovieTitles')
                oGuiElement.setTitle(str(aEntry[1]))

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovieTitles():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
        
    sUrl = sUrl.replace(' ', '%20').replace(':', '%3A').replace('+', '%2B')
    sUrl = sUrl.replace('http%3A//', 'http://')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = "<h3 class='title-only'><a href='([^']+)'>(.*?)</a></h3>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showHosters')
            oGuiElement.setTitle(str(aEntry[1]))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(aEntry[0]))
	    oOutputParameterHandler.addParameter('sMovieTitle', str(aEntry[1]))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    sNextPage = __checkForNextPage(sHtmlContent)
    if (sNextPage != False):       
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showMovieTitles')
        oGuiElement.setTitle('next ..')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sNextPage)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = "<a class='blog-pager-older-link' href='([^']+)'"
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

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = "<h3 class='post-title entry-title'>(.*?)<div style='clear: both;'></div>"
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]
        sHtmlContent = str(sHtmlContent).lower()

        sPattern = "src=([^ ]+) "
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sHosterUrl = str(aEntry).replace("'", '').replace('"', '')
                
                oHoster = __checkHoster(sHosterUrl)               
                if (oHoster != False):
		    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl)

    oGui.setEndOfDirectory()

def __checkHoster(sHosterUrl):    
    if (sHosterUrl.startswith('http://embed.novamov.com/')):
        return cHosterHandler().getHoster('novamov')
    
    if (sHosterUrl.startswith('http://embed.divxstage.net/')):
        return cHosterHandler().getHoster('divxstage')

    if (sHosterUrl.startswith('http://www.filestage.to/')):
        return cHosterHandler().getHoster('filestage')

    if (sHosterUrl.startswith('http://www.vidxden.com/')):
        return cHosterHandler().getHoster('vidxden')

    if (sHosterUrl.startswith('http://www.vidbux.com/')):
        return cHosterHandler().getHoster('vidbux')

    if (sHosterUrl.startswith('http://www.megavideo.com/')):
        return cHosterHandler().getHoster('megavideo')

    if (sHosterUrl.startswith('http://www.dankfile.com/')):
        return cHosterHandler().getHoster('dankfile')

    return False