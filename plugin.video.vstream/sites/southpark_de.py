from resources.lib.config import cConfig
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.player import cPlayer
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler


SITE_IDENTIFIER = 'southpark_de'
SITE_NAME = 'Southpark.de'

URL_MAIN = 'http://www.southpark.de'
URL_SEASION = 'http://www.southpark.de/ajax/seasonepisode/'
URL_EPISODE = 'http://www.southpark.de/alleEpisoden/'
URL_MTVN_SERVICES = 'http://media.mtvnservices.com/'
URL_FEEDS = 'http://www.southpark.de/feeds/as3player/config.php'

def load():
    oConfig = cConfig()
    oGui = cGui()

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('displaySeasions')
    oGuiElement.setTitle(oConfig.getLocalizedString(30302))
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('language', '')
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('displaySeasions')
    oGuiElement.setTitle(oConfig.getLocalizedString(30303))
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('language', 'en')
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def displaySeasions():
    oConfig = cConfig()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('language')):
        sLanguage = oInputParameterHandler.getValue('language')
    else:
        sLanguage = ''

    oGui = cGui()
    sPattern = '<li><a href="/guide/episoden([^"]+)">([^<]+)</a></li>'
    
    # request
    oRequest = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequest.request()

    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('displayEpisodes')
            sTitle = oConfig.getLocalizedString(30305) % (str(aEntry[1]))
            oGuiElement.setTitle(sTitle)

            sUrl = URL_SEASION + str(aEntry[1])
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('language', sLanguage)
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def displayEpisodes():
      
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('language')):
        sLanguage = oInputParameterHandler.getValue('language')
    else:
        sLanguage = ''

    ## todo mit json machen
    oGui = cGui()    
    sPattern = '{ "airdate" : "([^"]+)".*?"description" : "([^"]+)".*?"episodenumber" : "([^"]+)".*?"thumbnail_190" : "([^"]+)".*?"title" : "([^"]+)"'
   
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('siteUrl')):
        sSiteUrl = oInputParameterHandler.getValue('siteUrl')
        
        # request
        oRequest = cRequestHandler(sSiteUrl)
        sHtmlContent = oRequest.request()
       
        # parse content
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)               

        if (aResult[0] == True):
            iCounter = 1
            for aEntry in aResult[1]:
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('parseMovieFromSite')

                sTitle = str(iCounter) + '. ' + str(aEntry[4])
                oGuiElement.setTitle(sTitle)
                oGuiElement.setThumbnail(aEntry[3]);

                sUrl = URL_EPISODE + str(aEntry[2]) + '/?lang=' + str(sLanguage)
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oGui.addFolder(oGuiElement, oOutputParameterHandler)
                iCounter = iCounter + 1
                
    oGui.setEndOfDirectory()

def parseMovieFromSite():
    oConfig = cConfig()
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('siteUrl')):
        sSiteUrl = oInputParameterHandler.getValue('siteUrl')
        
         # request
        oRequest = cRequestHandler(sSiteUrl)
        sHtmlContent = oRequest.request()

        # parse content
        sPattern = 'swfobject.embedSWF\("([^"<]+)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)        
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sUrl = aEntry
                sUrl = sUrl.replace(URL_MTVN_SERVICES, '')
                
                oRequestHandler = cRequestHandler(URL_FEEDS)
                oRequestHandler.addParameters('group', 'entertainment')
                oRequestHandler.addParameters('type', 'error')
                oRequestHandler.addParameters('uri', sUrl)
                sUrl = oRequestHandler.getRequestUri()
                                
                oRequest = cRequestHandler(sUrl)
                sHtmlContent = oRequest.request()                

                sPattern = '<media:content url="([^"]+)" type="text/xml" medium="video" duration="([^"]+)" isDefault="true" />'
                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern)
               
                aAllParts = []
                iDuration = 0
                if (aResult[0] == True):
                    for aPart in aResult[1]:
                        sPartUrl = aPart[0]
                        aAllParts.append(sPartUrl)

                        iPartDuration = aPart[1]
                        iEndDuration = iDuration + int(iPartDuration)

                        oHoster = cHosterHandler().getHoster('southpark')
                        sTitle = oConfig.getLocalizedString(30306) % (str(iDuration), str(iEndDuration))
                        oHoster.setDisplayName(sTitle)
			oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sPartUrl)
                     
                        iDuration = iEndDuration

                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(SITE_IDENTIFIER)
                    oGuiElement.setFunction('playAllMovieParts')
                    oGuiElement.setTitle(oConfig.getLocalizedString(30307))
                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('aParts', aAllParts)
                    oGui.addFolder(oGuiElement, oOutputParameterHandler)
                                
        
    oGui.setEndOfDirectory()

def playAllMovieParts():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('aParts')):
        sParts = oInputParameterHandler.getValue('aParts')
        aParts = eval(sParts)

        oPlayer = cPlayer()
	oPlayer.clearPlayList()
        for sPartUrl in aParts:
            oHoster = cHosterHandler().getHoster('southpark')
            oHoster.setUrl(sPartUrl)
           
            aLink = oHoster.getMediaLink()            
            if (aLink[0] == True):
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setMediaUrl(aLink[1])
                oPlayer.addItemToPlaylist(oGuiElement)
       
        oPlayer.startPlayer()
        return
        
    oGui.setEndOfDirectory()