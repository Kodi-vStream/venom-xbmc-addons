from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
import time
import random

SITE_IDENTIFIER = 'bild_de'
SITE_NAME = 'Bild.de'

URL_MAIN = 'http://film.bild.de'
URL_VIDEOS = 'http://film.bild.de/nav.aspx'
URL_VIDEO_DETAILS = 'http://film.bild.de:80/movie'



def load():    
    oGui = cGui()
    __createMainMenuItem(oGui, 'Alle Filme', '2147483647')
    __createMainMenuItem(oGui, 'Action / Thriller' , '22')
    __createMainMenuItem(oGui, 'Drama', '6')
    __createMainMenuItem(oGui, 'Horror', '8')
    __createMainMenuItem(oGui, 'Komoedie', '75')
    __createMainMenuItem(oGui, 'Krimi', '11')
    __createMainMenuItem(oGui, 'Romance', '23')
    __createMainMenuItem(oGui, 'Serie', '58')
    oGui.setEndOfDirectory()

def __createMainMenuItem(oGui, sTitle, iId):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('listVideos')
    oGuiElement.setTitle(sTitle)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('iPage', 1)
    oOutputParameterHandler.addParameter('iId', iId)  
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def listVideos():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('iPage') and oInputParameterHandler.exist('iId')):
        iPage = oInputParameterHandler.getValue('iPage')
        iId = oInputParameterHandler.getValue('iId')
      
        sRandom = random.random()
        oRequest = cRequestHandler(URL_VIDEOS)
        oRequest.addParameters('s', 'list')
        oRequest.addParameters('c', iId)
        oRequest.addParameters('p', iPage)
        oRequest.addParameters('r', sRandom)
        sHtmlContent = oRequest.request()

        sPattern = '<a href="javascript:onPlayMovieDialog\(([^,]+),([^,]+)\);.*?<div class="naw_tipBox_movieTitle">([^<]+)</div>'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                oHoster = cHosterHandler().getHoster('bild')
                oHoster.setDisplayName(aEntry[2])
		oHoster.setFileName(aEntry[2])

                sRandom = random.random()              
	        sMilli = str(time.time()).split('.')[1]
                sUrl = URL_VIDEO_DETAILS + str(sMilli) + str(sRandom) + '.xml?s=xml' + str(aEntry[0])
                
                cHosterGui().showHoster(oGui, oHoster, sUrl)

        if (__checkForNextPage(sHtmlContent, iPage) == True):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('listVideos')            
            oGuiElement.setTitle('mehr ..')

            iNextPage = int(iPage) + 1
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('iPage', iNextPage)
            oOutputParameterHandler.addParameter('iId', iId)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)            

    oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent, iCurrentPage):
    sPattern = '<a href="#s=list&c=.*?">(.{1,2})</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
       
    iLastPage = 0
    if (aResult[0] == True):         
        iLastPage = int(aResult[1][-1])
            

    if (int(iLastPage) > int(iCurrentPage)):
        return True
    return False