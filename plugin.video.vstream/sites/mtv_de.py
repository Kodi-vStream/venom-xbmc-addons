from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler

SITE_IDENTIFIER = 'mtv_de'
SITE_NAME = 'MTV.de'

URL_MAIN = 'http://www.mtv.de'
URL_VIDEOS = 'http://www.mtv.de/videos'
URL_SHOWS = 'http://www.mtv.de/videos/mtv-shows'
URL_CHARTS = 'http://www.mtv.de/charts/germany'
URL_VIDEOCHARTS = 'http://www.mtv.de/charts/videocharts'
URL_XML = 'http://de.esperanto.mtvi.com/www/xml/flv/flvgen.jhtml'
URL_SEARCH = 'http://www.mtv.de/videos/search'

ENTRIES_PER_PAGE = 30

def load():
    oGui = cGui()
    __createMainMenuItem(oGui, 'Neuste Videos', 'listVideos', 'latest')
    __createMainMenuItem(oGui, 'Meist gesehende Videos', 'listVideos', 'views')
    __createMainMenuItem(oGui, 'Beste Bewertungs Videos', 'listVideos', 'rating')
    __createMainMenuItem(oGui, 'Shows', 'showShows')
    __createMainMenuItem(oGui, 'Charts', 'showCharts')
    __createMainMenuItem(oGui, 'VideoCharts', 'showVideoCharts')
    __createMainMenuItem(oGui, 'Suche', 'showSearch')
    oGui.setEndOfDirectory()

def __createMainMenuItem(oGui, sTitle, sFunction, sOrderBy = False):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sTitle)
    if (sOrderBy != False):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('orderBy', sOrderBy)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)
    else:
        oGui.addFolder(oGuiElement)

def listVideos():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('orderBy')):
        sOrderBy = oInputParameterHandler.getValue('orderBy')

        iPage = 1
        if (oInputParameterHandler.exist('page')):
            iPage = oInputParameterHandler.getValue('page')      

        oRequest = cRequestHandler(URL_VIDEOS)
        oRequest.addParameters('page', iPage)
        oRequest.addParameters('order', sOrderBy)
        sHtmlContent = oRequest.request()

        sPattern = '<li class="fourth">    <p><a title="([^"]+)" href="([^"]+)">.*?<img class="smallImgTeaser" src="([^"]+)".*?/>'
        
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sUrl = URL_MAIN + str(aEntry[1])
                __showHoster(oGui, aEntry[0], sUrl)

            __createNextButtonForVideos(iPage, sOrderBy, oGui)
                
    oGui.setEndOfDirectory()

def listShow():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('showUrl')):
        sShowUrl = oInputParameterHandler.getValue('showUrl')

        sPattern = '<li class="fourth">    <p><a title="([^"]+)" href="([^"]+)">.*?<img class="smallImgTeaser" src="([^"]+)".*?/>'

        oRequest = cRequestHandler(sShowUrl)
        sHtmlContent = oRequest.request()
     
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sUrl = URL_MAIN + str(aEntry[1])
                __showHoster(oGui, aEntry[0], sUrl)

    oGui.setEndOfDirectory()

def __createNextButtonForVideos(iPage, sOrderBy, oGui):
    if (iPage == 1):       
        iNextPage = 2  
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setFunction('listVideos')
        oGuiElement.setTitle('mehr ..')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('orderBy', sOrderBy)
        oOutputParameterHandler.addParameter('page', iNextPage)
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    return

def showVideoCharts():
    __parseCharts(URL_VIDEOCHARTS)
    
def showCharts():
    __parseCharts(URL_CHARTS)

def __parseCharts(sUrl):
    oGui = cGui()

    sPattern = '<td class="ch_place">.*?"/>(.*?)</td>.*?<td class="ch_last">(.*?)</td>.*?<td class="ch_artist">(.*?)</td>.*?<td class="ch_track">(.*?)</td>.*?<td class="ch_buy">(.*?)</td>'

    oRequest = cRequestHandler(sUrl)
    sHtmlContent = oRequest.request()

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sInterpretName = cUtil().removeHtmlTags(str(aEntry[2]), '')
            sTitle = str(aEntry[0]) + ' (' + str(aEntry[1]) + ') : ' + sInterpretName + ' - ' + str(aEntry[3])

            sPattern = '.*?<a href="([^"]+)".*?<img.*?<img.*?src="([^"]+)"'
            sCode = aEntry[4]
            oParser = cParser()
            aResultMeta = oParser.parse(sCode, sPattern)
            if (aResultMeta[0] == True):
                sLink = aResultMeta[1][0][0]                
                
                sUrl = URL_MAIN + str(sLink)
                __showHoster(oGui, sTitle, sUrl)

    oGui.setEndOfDirectory()

def showShows():
    oGui = cGui()

    sPattern = '<div class="bigImageTeaser">.*?<img src="([^"]+)".*?title="([^"]+)".*?<a href="/tv([^"]+)">'

    oRequest = cRequestHandler(URL_SHOWS)
    sHtmlContent = oRequest.request()
    
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('listShow')

            sTitle = aEntry[1].replace('Foto', '')
            oGuiElement.setTitle(sTitle)
            sThumbnail = str(aEntry[0])
            oGuiElement.setThumbnail(sThumbnail)

            sUrl = URL_MAIN + '/tv/' + str(aEntry[2])
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('showUrl', sUrl)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)
            
    oGui.setEndOfDirectory()

def showSearch():    
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        __callSearch(sSearchText, 0)
                            
    oGui.setEndOfDirectory()

def search():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    if (oInputParameterHandler.exist('searchText') and oInputParameterHandler.exist('start')):
        sSearchText = oInputParameterHandler.getValue('searchText')
        iStart = oInputParameterHandler.getValue('start')
        __callSearch(sSearchText, iStart)
        return
    
    oGui.setEndOfDirectory()

def __callSearch(sSearchText, iStart):
    oGui = cGui()

    oRequest = cRequestHandler(URL_SEARCH)
    oRequest.addParameters('q', sSearchText)
    oRequest.addParameters('x', 0)
    oRequest.addParameters('y', 0)
    oRequest.addParameters('n', ENTRIES_PER_PAGE)
    oRequest.addParameters('s', iStart)
    sHtmlContent = oRequest.request()

    sPattern = '<div class="smallVideoTeaser"><a href="([^"]+)" title="([^"]+)"><img .+?><img src="([^"]+)".*?/>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oHoster = cHosterHandler().getHoster('mtv')
            oHoster.setDisplayName(aEntry[1])

            sUrl = URL_MAIN + str(aEntry[0])
            cHosterGui().showHoster(oGui, oHoster, sUrl)            

        __createNextButtonForSearch(oGui, iStart, sSearchText, sHtmlContent)
            
    oGui.setEndOfDirectory()

def __createNextButtonForSearch(oGui, iCurrentStart, sSearchText, sHtmlContent):    
    sPattern = '<p class="textPadding">    <strong>([^ ]+) '
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        iCount = aResult[1][0]
        
        iNextStart = __calculateNextPage(iCount, iCurrentStart)
        if (iNextStart > 0):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('search')
            oGuiElement.setTitle('mehr ..')
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('searchText', sSearchText)
            oOutputParameterHandler.addParameter('start', iNextStart)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        
def __calculateNextPage(iCount, iCurrentStart):
    iNextStart = int(iCurrentStart) + ENTRIES_PER_PAGE  
    if (iNextStart < int(iCount)):        
        return iNextStart
    
    return 0

def __showHoster(oGui, sTitle, sUrl):
    oHoster = cHosterHandler().getHoster('mtv')
    oHoster.setDisplayName(sTitle)
    oHoster.setFileName(sTitle)
    cHosterGui().showHoster(oGui, oHoster, sUrl)