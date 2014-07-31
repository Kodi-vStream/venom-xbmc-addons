from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler

SITE_IDENTIFIER = 'shoutcast_com'
SITE_NAME = 'ShoutCast.com'

URL_MAIN = 'http://www.shoutcast.com'
URL_GENRE_CHILDS = 'http://www.shoutcast.com/genre.jsp'
URL_GENRE_AJAX = 'http://www.shoutcast.com/genre-ajax/'
URL_SEARCH = 'http://www.shoutcast.com/search-ajax/'

COUNT_OF_ENTRIES = 10

def load():
    oGui = cGui()
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('loadGenre')
    oGuiElement.setTitle('Genre')
    oGui.addFolder(oGuiElement)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('loadSearch')
    oGuiElement.setTitle('Suche')
    oGui.addFolder(oGuiElement)

    oGui.setEndOfDirectory()

def loadGenre():
    oGui = cGui()

    oRequest = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequest.request()

    sPattern = '<li class="prigen" id="([^"]+)"><div class="arrowup"></div>.*?<a href="([^"]+)">([^<]+)</a></li>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showGenreChilds')
            oGuiElement.setTitle(aEntry[2])
          
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('iId', aEntry[0])
            oOutputParameterHandler.addParameter('sGenre', aEntry[2])
            oOutputParameterHandler.addParameter('sUrl', aEntry[1])
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenreChilds():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sGenre') and oInputParameterHandler.exist('sUrl') and oInputParameterHandler.exist('iId')):
        sGenre = oInputParameterHandler.getValue('sGenre')      
        iId = oInputParameterHandler.getValue('iId')

        oRequest = cRequestHandler(URL_GENRE_CHILDS)
        oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequest.addParameters('genre', sGenre)
        oRequest.addParameters('id', iId)
        sHtmlContent = oRequest.request()

         # maingenre
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showGenreContent')
        oGuiElement.setTitle(sGenre)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sGenre', sGenre)
        oOutputParameterHandler.addParameter('iStartIndex', 0)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

        sPattern = '<a href="([^"]+)">([^<]+)</a>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('showGenreContent')
                oGuiElement.setTitle(aEntry[1])
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sGenre', aEntry[1])
                oOutputParameterHandler.addParameter('iStartIndex', 0)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenreContent():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sGenre') and oInputParameterHandler.exist('iStartIndex')):
        sGenre = oInputParameterHandler.getValue('sGenre')
        iStartIndex = oInputParameterHandler.getValue('iStartIndex')

        sUrl = URL_GENRE_AJAX + str(sGenre.replace(' ', '+'))
        oRequest = cRequestHandler(sUrl)
        oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequest.addParameters('ajax', 'true')
        oRequest.addParameters('count', COUNT_OF_ENTRIES)
        oRequest.addParameters('mode', 'listeners')
        oRequest.addParameters('order', 'desc')
        oRequest.addParameters('strIndex', iStartIndex)
        sHtmlContent = oRequest.request()

        __parseContent(oGui, sHtmlContent, sGenre, iStartIndex)

    oGui.setEndOfDirectory()

def showSearchContent():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sSearchText') and oInputParameterHandler.exist('iStartIndex')):
        sSearchText = oInputParameterHandler.getValue('sSearchText')
        iStartIndex = oInputParameterHandler.getValue('iStartIndex')

        sUrl = URL_SEARCH + str(sSearchText)
        oRequest = cRequestHandler(sUrl)
        oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequest.addParameters('ajax', 'true')
        oRequest.addParameters('count', COUNT_OF_ENTRIES)
        oRequest.addParameters('strIndex', iStartIndex)
        sHtmlContent = oRequest.request()

        __parseContent(oGui, sHtmlContent, sSearchText, iStartIndex)

    oGui.setEndOfDirectory()

def __parseContent(oGui, sHtmlContent, sValue, iStartIndex):
    sPattern = '<div class="stationcol".*?<a class="playbutton clickabletitle".*?title="([^"]+)" href="([^"]+)">.*?<div class="dirbitrate">([^<]+)</div>.*?<div class="dirtype">([^<]+)</div>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oHoster = cHosterHandler().getHoster('shoutcast')
            sTitle = str(aEntry[3]) + ' - ' + str(aEntry[2]) + ' - ' + str(aEntry[0])
            oHoster.setDisplayName(sTitle)
	    oHoster.setFileName(sTitle)
            cHosterGui().showHoster(oGui, oHoster, str(aEntry[1]))

    if (__checkForNextPage(sHtmlContent)):
        iNextPage = int(iStartIndex) + COUNT_OF_ENTRIES

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('showGenreContent')
        oGuiElement.setTitle('mehr ..')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sGenre', sValue)
        oOutputParameterHandler.addParameter('iStartIndex', iNextPage)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

def __checkForNextPage(sHtmlContent):
    sPattern = '<div id="showmorehome" class="([^"]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
  
    if (aResult[0] == True):
        return True
    return False

def loadSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        __search(oGui, sSearchText, 0)
        
    oGui.setEndOfDirectory()    

def __search(oGui, sSearchText, iStartIndex):
    sSearchText = sSearchText.replace(' ', '+')
    sUrl = URL_SEARCH + sSearchText

    oRequest = cRequestHandler(sUrl)
    oRequest.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
    oRequest.addParameters('ajax', 'true')
    oRequest.addParameters('count', COUNT_OF_ENTRIES)
    oRequest.addParameters('strIndex', 0)
    sHtmlContent = oRequest.request()

    __parseContent(oGui, sHtmlContent, sSearchText, iStartIndex)