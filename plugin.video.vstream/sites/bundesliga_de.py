from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.player import cPlayer

SITE_IDENTIFIER = 'bundesliga_de'
SITE_NAME = 'Bundesliga.de'

URL_MAIN = 'http://www.bundesliga.de'
URL_TV = 'http://www.bundesliga.de/de/bundesliga-tv/navigation.php?area='
URL_GET_STREAM = 'http://btd-flv-lbwww-01.odmedia.net/bundesliga/'

def load():
    oGui = cGui()
    __createMainMenuItem(oGui, 'Aktuell', 'aktuell')    
    __createMainMenuItem(oGui, 'Spieltag', 'spieltag')
    __createMainMenuItem(oGui, 'Stars', 'stars')
    __createMainMenuItem(oGui, 'Insider', 'insider')
    __createMainMenuItem(oGui, 'Historie', 'historie')
    __createMainMenuItem(oGui, 'Vereine', 'vereine')
    oGui.setEndOfDirectory()

def __createMainMenuItem(oGui, sTitle, sPlaylistId):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('listVideos')
    oGuiElement.setTitle(sTitle)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('playlistId', sPlaylistId)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def listVideos():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('playlistId')):
        sPlaylistId = oInputParameterHandler.getValue('playlistId')

        sUrl = URL_TV + str(sPlaylistId)
                
        sPattern = '<div class="zeile">.*?<img src="([^"]+)" id="bild" class="previewImg".*?<a href="javascript:showVideoSnippet\(\'(.*?)\'\).*?<div class="describe">(.*?)</div>'
      
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
       
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('play')
                oGuiElement.setTitle(aEntry[2])
                sThumbnail = URL_MAIN + str(aEntry[0])
                oGuiElement.setThumbnail(sThumbnail)

                sUrl = URL_MAIN + str(aEntry[1])
                
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('sUrl', sUrl)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def play():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('sUrl')):
        sUrl = oInputParameterHandler.getValue('sUrl')

        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()

        sPattern = 'ake_playlist.php%3Fflv%3D(.*?)%26'

        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            sUrl = URL_GET_STREAM + str(aResult[1][0])
            
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setMediaUrl(sUrl)

            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            oPlayer.startPlayer()
        return
    oGui.setEndOfDirectory()
