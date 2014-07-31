from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler

SITE_IDENTIFIER = 'simpsons_to'
SITE_NAME = 'Simpsons.to'

URL_MAIN = 'http://www.simpsons.to/'
URL_LOAD_PAGE = 'http://www.simpsons.to/load_page.php'
URL_PLAYER = 'http://stream.simpsons.to/streamlink/?'
URL_SEARCH = 'http://www.simpsons.to/functions/search.inc.php'

def load():
    oGui = cGui()

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('displaySeasions')
    oGuiElement.setTitle('Staffeln')
    oGui.addFolder(oGuiElement)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('displaySearch')
    oGuiElement.setTitle('Suche')
    oGui.addFolder(oGuiElement)

    oGui.setEndOfDirectory()

def __loadPageContent():
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sPage')):
        sPage = oInputParameterHandler.getValue('sPage')

        oRequest = cRequestHandler(URL_LOAD_PAGE)
        oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequest.addParameters('page', sPage)
        sHtmlContent = oRequest.request()
        return sHtmlContent

    return False

def displaySearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        __callSearch(sSearchText)

    oGui.setEndOfDirectory()

def __callSearch(sSearchText):
    oRequest = cRequestHandler(URL_SEARCH)
    oRequest.addParameters('myfield', sSearchText)
    sHtmlContent = oRequest.request()
    __parseEpisodes(sHtmlContent)
    
def displaySeasions():
    oGui = cGui()
    sPattern = '<div id="staffeln">(.*?)<div id='

    oRequest = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequest.request()    

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
  
    if (aResult[0] == True):
        sHtmlContent = aResult[1][0]
        
        sPattern = '<a href="([^"]+)">([^<]+)</a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showEpisodes')
            oGuiElement.setTitle(aEntry[1])
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sPage', aEntry[0])
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showEpisodes():
    oGui = cGui()

    sHtmlContent = __loadPageContent()
    if (sHtmlContent != False):
        __parseEpisodes(sHtmlContent)
        return

    oGui.setEndOfDirectory()

def __parseEpisodes(sHtmlContent):
    oGui = cGui()
    sPattern = '<h1 style="color:#000000;" title="([^"]+)">.*?<img src="([^"]+)" class="episoden_vorschau".*?<a href="([^"]+)" class="optionen_alle"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showHoster')            
            sTitle = __createTitle(aEntry[0], '')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setThumbnail(URL_MAIN + str(aEntry[1]))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sPage', aEntry[2])
            oOutputParameterHandler.addParameter('sTitle', sTitle)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()
    

def __createTitle(sTitle, sLanguage):
    if (sLanguage == 'gb'):
        return sTitle + ' (ENG)'

    if (sLanguage == 'de'):
        return sTitle + ' (DE)'

    return sTitle

def showHoster():
    oGui = cGui()

    sHtmlContent = __loadPageContent()
    if (sHtmlContent != False):

        oInputParameterHandler = cInputParameterHandler()
        sMovieTitle = oInputParameterHandler.getValue('sTitle')

        oParser = cParser()
        sPattern = "<b>Hoster:</b>(.*?)</div>.*?<a href='([^']+)' class='optionen_mirror'"
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sTitle = cUtil().removeHtmlTags(aEntry[0], '').replace(' ', '')

                oHoster = __checkHoster(sTitle)
                if (oHoster != False):
                    sPlayerId = __getPlayerId(aEntry[1])
                    sUrl = URL_PLAYER + str(sPlayerId)
		    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sUrl, True)

    oGui.setEndOfDirectory()

def __getPlayerId(sUrl):
    sUrl = str(sUrl)    
    aUrlParts = sUrl.split('-')  
    return aUrlParts[1]

def __checkHoster(sHosterName):
    sHosterName = sHosterName.lower()

    if (sHosterName == 'mystream.to'):
        return cHosterHandler().getHoster('mystream')

    if (sHosterName == 'megavideo.com'):
        return cHosterHandler().getHoster('megavideo')

    if (sHosterName == 'duckload.com'):
        return cHosterHandler().getHoster('duckload')

    if (sHosterName == 'zshare.net'):
        return cHosterHandler().getHoster('zshare')

    if (sHosterName == 'videoweed.com'):
       return cHosterHandler().getHoster('videoweed')

    if (sHosterName == 'tubeload.to'):
       return cHosterHandler().getHoster('tubeload')

    if (sHosterName == 'qip.ru'):
        return cHosterHandler().getHoster('qip')

    return False
           
