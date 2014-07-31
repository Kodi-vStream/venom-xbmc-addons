from resources.lib.util import cUtil
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.config import cConfig
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.parser import cParser
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler

SITE_IDENTIFIER = 'myp2p_eu'
SITE_NAME = 'MyP2P.eu'

URL_MAIN = 'http://www.myp2p.eu/'
URL_COUNTRY_SITE = 'http://www.myp2p.eu/channel.php?&part=channel&sel_country=yes'
URL_LIVE_TV = 'http://myp2p.eu/channel.php'

def load():
    
    oConfig = cConfig()
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    __createMenuEntry(oGui, 'showCountrySite', oConfig.getLocalizedString(30402), oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_LIVE_TV)
    __createMenuEntry(oGui, 'showLiveTvSite', 'Live Tv', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showLiveTvSite():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<td onclick="window.open\(\\\'([^\']+)\\\'\); return false;" style="cursor: pointer; padding-top: 1px; padding-bottom: 1px;">([^"]+)</td>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oHoster = cHosterHandler().getHoster('myp2p')
            oHoster.setDisplayName(cUtil().removeHtmlTags(aEntry[1]))
	    oHoster.setFileName(cUtil().removeHtmlTags(aEntry[1]))
            cHosterGui().showHoster(oGui, oHoster, aEntry[0])

    oGui.setEndOfDirectory()

def showCountrySite():
    oGui = cGui()

    sPattern = '<td onclick="window.location.href=\'([^;]+)\'; return false;" style="cursor: pointer; padding-top: 1px; padding-bottom: 1px;"><div style="width: 25px; margin-right: 15px; float: left;"><img src="([^"]+)" border="1" /></div>([^<]+)</td>'
   
    # request
    oRequest = cRequestHandler(URL_COUNTRY_SITE)
    sHtmlContent = oRequest.request()
  
    # parse content
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
     
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('showSubChannels')
            oGuiElement.setTitle(aEntry[2])
            oGuiElement.setThumbnail(aEntry[1])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('channelUrl', URL_MAIN + str(aEntry[0]))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSubChannels():    
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('channelUrl')):
        sChannelUrl = oInputParameterHandler.getValue('channelUrl')

        __createSubChannel(oGui, 'nicht zugeordnet', sChannelUrl, 0)
        __createSubChannel(oGui, 'Unterhaltung', sChannelUrl, 1)
        __createSubChannel(oGui, 'Kinder', sChannelUrl, 2)
        __createSubChannel(oGui, 'Musik', sChannelUrl, 3)
        __createSubChannel(oGui, 'Nachrichten', sChannelUrl, 4)
        __createSubChannel(oGui, 'Sport', sChannelUrl, 5)
        __createSubChannel(oGui, 'Alle anzeigen', sChannelUrl, 6)

    oGui.setEndOfDirectory()

def __createSubChannel(oGui, sTitle, sChannelUrl, iChannelType):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction('parseSubChannels')
    oGuiElement.setTitle(sTitle)
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('channelUrl', sChannelUrl)
    oOutputParameterHandler.addParameter('channelType', iChannelType)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def parseSubChannels():    
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    if (oInputParameterHandler.exist('channelUrl') and oInputParameterHandler.exist('channelType')):
        sChanellUrl = oInputParameterHandler.getValue('channelUrl')

        iChannelType = oInputParameterHandler.getValue('channelType')

        sCategoryName = 'No category'

        if (iChannelType == '0'):
            sCategoryName = 'No category'

        if (iChannelType == '1'):
            sCategoryName = 'Entertainment'

        if (iChannelType == '2'):
            sCategoryName = 'Kids'

        if (iChannelType == '3'):
            sCategoryName = 'Music'

        if (iChannelType == '4'):
            sCategoryName = 'News'

        if (iChannelType == '5'):
            sCategoryName = 'Sports'

        if (iChannelType == '5'):
            sCategoryName = '.+?'

        sPattern ='<tr><td class="competition"[^>]+>' + str(sCategoryName) + '</td></tr><tr><td></td><td><table[^>]+>(.+?)</table>'

        # request
        oRequest = cRequestHandler(sChanellUrl)
        sHtmlContent = oRequest.request()

        # parse content
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sHtmlContent = aEntry                
                sPattern = '<td onclick="window.open\(\\\'([^\']+)\\\'\); return false;" style="cursor: pointer; padding-top: 1px; padding-bottom: 1px;">([^"]+)</td>'

                oParser = cParser()
                aResult = oParser.parse(sHtmlContent, sPattern)
                
                if (aResult[0] == True):
                    for aEntry in aResult[1]:
                        oHoster = cHosterHandler().getHoster('myp2p')
                        oHoster.setDisplayName(aEntry[1])
			oHoster.setFileName(str(aEntry[1]))
                        cHosterGui().showHoster(oGui, oHoster, aEntry[0])

    oGui.setEndOfDirectory()