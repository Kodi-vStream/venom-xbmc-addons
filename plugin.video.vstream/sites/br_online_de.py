from resources.lib.util import cUtil
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler

SITE_IDENTIFIER = 'br_online_de'
SITE_NAME = 'Br-Online.de'

URL_MAIN = 'http://www.br-online.de'
URL_CENTAURI = 'http://www.br-online.de/br-alpha/alpha-centauri/alpha-centauri-harald-lesch-videothek-ID1207836664586.xml'
URL_DARWIN = 'http://www.br-online.de/br-alpha/charles-darwin/charles-darwin-evolution-videothek-ID1256655423519.xml'
URL_DENKER = 'http://www.br-online.de/br-alpha/denker-des-abendlandes/denker-lesch-vossenkuhl-ID1221136938708.xml'
URL_GEISTundGEHIRN = 'http://www.br-online.de/br-alpha/geist-und-gehirn/index.xml'
URL_KANT1 = 'http://www.br-online.de/br-alpha/kant-fuer-anfaenger/kant-reine-vernunft-philosophie-ID661188595418.xml'
URL_KANT2 = 'http://www.br-online.de/br-alpha/kant-fuer-anfaenger/kant-kategorischer-imperativ-philosophie-ID661188595399.xml'
URL_MATHE = 'http://www.br-online.de/br-alpha/mathematik-zum-anfassen/index.xml'
URL_MYTHEN = 'http://www.br-online.de/br-alpha/mythen/index.xml'
URL_PHYSIK_EINSTEIN = 'http://www.br-online.de/br-alpha/die-physik-albert-einsteins/die-physik-albert-einsteins-lesch-einstein-ID1221487435226.xml'
URL_ELEMENTE = 'http://www.br-online.de/br-alpha/die-4-elemente/die-4-elemente-elemente-harald-lesch-ID1225290580446.xml'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_CENTAURI)
    __createMenuEntry(oGui, 'showBRonlineVideothek', 'Alpha-Centauri', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_DARWIN)
    __createMenuEntry(oGui, 'showBRonlineMovies', 'Charles Darwin', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_DENKER)
    __createMenuEntry(oGui, 'showBRonlineMovies', 'Denker des Abendlandes', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_GEISTundGEHIRN)
    __createMenuEntry(oGui, 'showBRonlineVideothekSeasons', 'Geist und Gehirn', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_KANT1)
    __createMenuEntry(oGui, 'showBRonlineMovies', 'Kant fuer Anfaenger - Die Kritik der reinen Vernunft', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_KANT2)
    __createMenuEntry(oGui, 'showBRonlineMovies', 'Kant fuer Anfaenger - Der kategorische Imperativ', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MATHE)
    __createMenuEntry(oGui, 'showBRonlineVideothekSeasons', 'Mathematik zum Anfassen', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MYTHEN)
    __createMenuEntry(oGui, 'showBRonlineVideothekSeasons', 'Mythen', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_PHYSIK_EINSTEIN)
    __createMenuEntry(oGui, 'showBRonlineMovies', 'Die Physik Albert Einsteins', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_ELEMENTE)
    __createMenuEntry(oGui, 'showBRonlineMovies', 'Die 4 Elemente', oOutputParameterHandler)
    
    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showBRonlineVideothekSeasons():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<ul class="ebene1">(.*?)</ul>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]

        sPattern = '<li><a href="([^"]+)">(.*?)</a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showBRonlineMovies')
                oGuiElement.setTitle(aEntry[1])

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]))
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showBRonlineVideothek():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<h3 class="teaserHead">.*?<a href="([^"]+)".*?<img src="([^"]+)".*?<span class="versteckt">(.*?)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showBRonlineMovies')
            oGuiElement.setThumbnail(URL_MAIN + str(aEntry[1]))
            oGuiElement.setTitle(aEntry[2])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()
    
def showBRonlineMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();
    
    sPattern = '<h3 class="teaserHead">.*?<a href="([^"]+)".*?<span class="versteckt">(.*?)</span>'
    __showBRonlineMovies(oGui, sHtmlContent, sPattern)

    sPattern = '<h3 class="linkPkt">.*?<a href="([^"]+)".*?<span class="versteckt">(.*?)</span>'
    __showBRonlineMovies(oGui, sHtmlContent, sPattern)

    oGui.setEndOfDirectory()

def __showBRonlineMovies(oGui, sHtmlContent, sPattern):
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('getMovieUrls')
            oGuiElement.setTitle(aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

def getMovieUrls():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sTitle = __getMovieTitle(sHtmlContent)

    sPattern = "player.avaible_url\['microsoftmedia'\]\['1'\] = \"([^\"]+)\""
    __getMovieUrls(oGui, sHtmlContent, sPattern, 'WMV - low Quality', sTitle)

    sPattern = "player.avaible_url\['microsoftmedia'\]\['2'\] = \"(.*?)\""
    __getMovieUrls(oGui, sHtmlContent, sPattern, 'WMV - high Quality', sTitle)

    sPattern = "player.avaible_url\['flashmedia'\]\['1'\] = \"(.*?)\""
    __getMovieUrls(oGui, sHtmlContent, sPattern, 'FLASH - low Quality', sTitle)

    sPattern = "player.avaible_url\['flashmedia'\]\['2'\] = \"(.*?)\""
    __getMovieUrls(oGui, sHtmlContent, sPattern, 'FLASH - high Quality', sTitle)

    oGui.setEndOfDirectory()

def __getMovieTitle(sHtmlContent):
    sPattern = '<div class="videoText"><p><strong>(.*?)<span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
	return cUtil().removeHtmlTags(str(aResult[1][0]))

    return False

def __getMovieUrls(oGui, sHtmlContent, sPattern, sLabel, sTitle):
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
  
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oHoster = cHosterHandler().getHoster('bronline')
            oHoster.setDisplayName(sLabel)
	    if (sTitle != False):
		oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, str(aEntry))