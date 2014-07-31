from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler

SITE_IDENTIFIER = 'kino_de'
SITE_NAME = 'Kino.de'

URL_MAIN = 'http://www.kino.de'
URL_TRAILERS = 'http://www.kino.de/showroom/trailer/film'


ENTRIES_PER_PAGE = 30

def load():    

    oGui = cGui()
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('showTrailers')
    oGuiElement.setTitle('neuste / beste Trailers')
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sUrl', URL_TRAILERS)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)
       
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('showCharacters')
    oGuiElement.setTitle('Trailers A bis Z')
    oGui.addFolder(oGuiElement)
    oGui.setEndOfDirectory()

def showCharacters():
    oGui = cGui()
    __createCharacters(oGui, 'A')
    __createCharacters(oGui, 'B')
    __createCharacters(oGui, 'C')
    __createCharacters(oGui, 'D')
    __createCharacters(oGui, 'E')
    __createCharacters(oGui, 'F')
    __createCharacters(oGui, 'G')
    __createCharacters(oGui, 'H')
    __createCharacters(oGui, 'I')
    __createCharacters(oGui, 'J')
    __createCharacters(oGui, 'K')
    __createCharacters(oGui, 'L')
    __createCharacters(oGui, 'N')
    __createCharacters(oGui, 'O')
    __createCharacters(oGui, 'Q')
    __createCharacters(oGui, 'R')
    __createCharacters(oGui, 'S')
    __createCharacters(oGui, 'T')
    __createCharacters(oGui, 'U')
    __createCharacters(oGui, 'V')
    __createCharacters(oGui, 'W')
    __createCharacters(oGui, 'X')
    __createCharacters(oGui, 'Y')
    __createCharacters(oGui, 'Z')
    __createCharacters(oGui, '0-9')
    oGui.setEndOfDirectory()

def __createCharacters(oGui, sCharacter):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('showTrailers')
    oGuiElement.setTitle(sCharacter)

    sUrl = URL_TRAILERS + '/' + str(sCharacter)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sUrl', sUrl)
    oOutputParameterHandler.addParameter('page', '1')
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showTrailers():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')
        
        iPage = 0
        if (oInputParameterHandler.exist('page')):
            iPage = oInputParameterHandler.getValue('page')

        sTrailerUrl = sUrl
        if (iPage > 0):
            sTrailerUrl = sTrailerUrl + '/' + str(iPage)

        oRequest = cRequestHandler(sTrailerUrl)
        sHtmlContent = oRequest.request()

        sPattern = '<li class="showroomListItem" title="([^"]+)".+?>.*?<a href="([^"]+)"><img src=\'([^\']+)\'.*?>'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
             for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showTrailerDetails')
                oGuiElement.setTitle(aEntry[0])
                oGuiElement.setThumbnail(aEntry[2])

                sTrailerDetailUrl = URL_MAIN + str(aEntry[1])
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', sTrailerDetailUrl)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

        if (iPage > 0):
            bShowNextButton = __checkForNextPage(iPage, sHtmlContent)
            if (bShowNextButton == True):
                iNextPage = int(iPage) + 1

                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showTrailers')
                oGuiElement.setTitle('mehr ..')                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', sUrl)
                oOutputParameterHandler.addParameter('page', iNextPage)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oGui.setEndOfDirectory()

def __checkForNextPage(iPage, sHtmlContent):
    sPattern = '<a href=\'.*?\'>(.{1,2})</a></span>    <span class="nextLink">'   

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        iLastPage = aResult[1][0]
        if (int(iPage) < int(iLastPage)):
            return True

    return False    

def showTrailerDetails():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = '<div class="srTrailerListItem .*?">.*?<a href="([^"]+)">.*?<img src="([^"]+)".+?/>.*?<a.+?>(.*?)<br class'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sTitle = cUtil().removeHtmlTags(aEntry[2], '')
                sTitle = oParser.replace('[ ]{2,}', ' ', sTitle)
                
                oHoster = cHosterHandler().getHoster('kinode')
                oHoster.setDisplayName(sTitle)
		oHoster.setFileName(sTitle)

                sUrl = URL_MAIN + str(aEntry[0])               
                cHosterGui().showHoster(oGui, oHoster, sUrl)

    oGui.setEndOfDirectory()