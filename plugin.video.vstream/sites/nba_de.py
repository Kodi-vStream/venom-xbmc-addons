from resources.lib.util import cUtil
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler

SITE_IDENTIFIER = 'nba_de'
SITE_NAME = 'NBA.de'

URL_PLAYLIST = 'http://www.nba.de/video/index.php/action/get-playlist-videos/playlist-id/'
URL_POST_FOR_MOVIE = 'http://akmi.kaltura.com//api_v3/index.php?service=multirequest&action=null'
URL_HIGHLIGHTS = 'http://www.nba.de/video/index.php/action/get-videos/category/'

def load():    
        
    oGui = cGui()
    __createMainMenuItem(oGui, 'Neuste Videos', 'listVideos', 'playlistId', '0_65ltkg6t')
    __createMainMenuItem(oGui, 'Meist gesehende', 'listVideos', 'playlistId', '0_mmdxlq9n')
    __createMainMenuItem(oGui, 'Highlights - alle', 'listHighlights', 'urlPart', '1_Highlights>Alle')
    __createMainMenuItem(oGui, 'Highlights - Daily Zap', 'listHighlights', 'urlPart', '1_Highlights>Daily Zap')
    __createMainMenuItem(oGui, 'Highlights - Mavericks', 'listHighlights', 'urlPart', '1_Highlights>Mavericks')

    oGui.setEndOfDirectory()

def __createMainMenuItem(oGui, sTitle, sFunction, sOutName, sOutValue):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sTitle)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter(sOutName, sOutValue)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def listHighlights():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('urlPart')):
        sUrlPart = oInputParameterHandler.getValue('urlPart')

        sUrl = URL_HIGHLIGHTS + sUrlPart
        
        sPattern = '{"mediaType":1,.*?"dataUrl":"([^"]+)".*?"duration":([^,]+),.*?"name":"([^"]+)".*?"thumbnailUrl":"([^"]+)".*?'
        
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        sHtmlContent = sHtmlContent.replace('\/', '/')
        sHtmlContent = sHtmlContent.replace('\\"', '"')
        
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sDurationFormatted = cUtil().formatTime(aEntry[1])
                sTitle = aEntry[2] + ' (' + sDurationFormatted + ')'
                __showHoster(oGui, sTitle, aEntry[0])
                
    oGui.setEndOfDirectory()

def listVideos():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('playlistId')):
        sPlaylistId = oInputParameterHandler.getValue('playlistId')

        sUrl = URL_PLAYLIST + str(sPlaylistId)
       
        sPattern = '<li><a href="#([^"]+)".*?><img src="([^"]+)".*?></div><div>([^"]+)</div></a></li>'

        # request
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        sHtmlContent = sHtmlContent.replace('\/', '/')
        sHtmlContent = sHtmlContent.replace('\\"', '"')
       
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sTitle = cUtil().removeHtmlTags(aEntry[2], ' ')
                sVideoUrl = __createVideoUrl(aEntry[1], aEntry[0])
                __showHoster(oGui, sTitle, sVideoUrl)
    
    oGui.setEndOfDirectory()

def __showHoster(oGui, sTitle, sUrl):
    oHoster = cHosterHandler().getHoster('nba')
    oHoster.setDisplayName(sTitle)
    oHoster.setFileName(sTitle)
    cHosterGui().showHoster(oGui, oHoster, sUrl)

def __createVideoUrl(sThumbnailUrl, sVideoId):
    aUrlParts = sThumbnailUrl.split('thumbnail');
    return str(aUrlParts[0]) + 'flvclipper/entry_id/' + str(sVideoId) + '/version/0'
    