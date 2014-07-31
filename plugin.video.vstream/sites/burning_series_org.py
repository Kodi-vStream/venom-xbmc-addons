from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler

SITE_IDENTIFIER = 'burning_series_org'
SITE_NAME = 'Burning-Series.org'

URL_MAIN = 'http://www.burning-series.org/'
URL_SERIES = 'http://www.burning-series.org/andere-serien'

def load():
    oGui = cGui()
    __createMenuEntry(oGui, 'showAllSeries', 'Serien', URL_SERIES)   
    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, sUrl):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showAllSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<ul id="serSeries">(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        sPattern = '<li><a href="([^"]+)">(.*?)</a></li>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
             for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showSeasons')
                oGuiElement.setTitle(aEntry[1])

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]))
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeasons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<ul class="pages">(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        sPattern = '<a href="([^"]+)">(.*?)</a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
             for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showSeries')
                oGuiElement.setTitle('Staffel ' + str(aEntry[1]))

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]))
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSeries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<table>(.*?)</table>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]
        
        sPattern = '<a href="([^"]+)"><strong>(.*?)</strong>.*?<span lang="en">(.*?)</span></a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
             for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showHosters')
                oGuiElement.setTitle(str(aEntry[1]) + ' - ' + str(aEntry[2]))

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]))
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();    

    sPattern = '<h3>Hoster dieser Episode(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        sPattern = '<a href="([^"]+)">.*?title="([^"]+)" />(.*?)</a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
             for aEntry in aResult[1]:
                oHoster = __checkHoster(str(aEntry[1]))
                if (oHoster != False):
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('getHosterUrlandPlay')
                    oGuiElement.setTitle(str(aEntry[2]))

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]))
                    oOutputParameterHandler.addParameter('hosterName', oHoster.getPluginIdentifier())
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __getMovieTitle(sHtmlContent):
    sPattern = '</ul><h2>(.*?)<small id="titleEnglish" lang="en">(.*?)</small>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
	for aEntry in aResult[1]:
	    return str(aEntry[0]).strip() + ' - ' + str(aEntry[1]).strip()

    return False

def getHosterUrlandPlay():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sHoster = oInputParameterHandler.getValue('hosterName')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    
    sTitle = __getMovieTitle(sHtmlContent)

    sPattern = '<div id="video_actions">.*?<a href="([^"]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sStreamUrl = aResult[1][0]

        oHoster = cHosterHandler().getHoster(sHoster)
	if (sTitle != False):
	    oHoster.setFileName(sTitle)

        cHosterGui().showHoster(oGui, oHoster, sStreamUrl)
        oGui.setEndOfDirectory()
        return

    oGui.setEndOfDirectory()

def __checkHoster(sHosterName):
    if (sHosterName == 'Megavideo'):
        return cHosterHandler().getHoster('megavideo')

    if (sHosterName == 'zShare'):
        return cHosterHandler().getHoster('zshare')

    if (sHosterName == 'Duckload'):
        return cHosterHandler().getHoster('duckload')

    if (sHosterName == 'FileBase'):
        return cHosterHandler().getHoster('filebase')

    if (sHosterName == 'MyStream'):
        return cHosterHandler().getHoster('mystream')

    return False

