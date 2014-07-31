from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'wwitv_com'
SITE_NAME = 'wwiTV.com'

URL_MAIN = 'http://wwitv.com/'
URL_MENU = 'http://wwitv.com/menu_left.htm'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MENU)
    __createMenuEntry(oGui, 'showCountries', 'nach Laender', oOutputParameterHandler)

    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    #__createMenuEntry(oGui, 'showCharacters', 'Kategorien', oOutputParameterHandler)
    
    #oOutputParameterHandler = cOutputParameterHandler()
    #oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    #__createMenuEntry(oGui, 'showCharacters', 'Am besten bewerted', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __createMenuEntry(oGui, sFunction, sLabel, oOutputParameterHandler = ''):
    oGuiElement = cGuiElement()
    oGuiElement.setSiteName(SITE_IDENTIFIER)
    oGuiElement.setFunction(sFunction)
    oGuiElement.setTitle(sLabel)
    oGui.addFolder(oGuiElement, oOutputParameterHandler)

def showCountries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<a class="rb" href="([^"]+)" target="_parent">(.*?)</a>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(SITE_IDENTIFIER)
            oGuiElement.setFunction('getStreams')
            sTitle = __formatTitle(str(aEntry[1]))
            oGuiElement.setTitle(sTitle)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]))
            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()

def __formatTitle(sTitle):
    return sTitle

def getStreams():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sPattern = '<a class="travel" href="([^"]+)">(.*?)</a></td><td class="qe" width="11"><img src="([^"]+)" width="50" height="24">.*?<a.*?>(.*?)</a>.*?font class="hd2">(.*?)</td></tr>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if (__isStream(str(aEntry[3]))):


                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(SITE_IDENTIFIER)
                oGuiElement.setFunction('parseStream')
                sTitle = __createStreamTitle(str(aEntry[1]), str(aEntry[3]), str(aEntry[4]))
                oGuiElement.setTitle(sTitle)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + str(aEntry[0]).replace('http://wwitv.com/', '').replace('../', ''))
                oGui.addFolder(oGuiElement, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def __createStreamTitle(sName, sBitRate, sDescription):
    return sName + ' (' + sBitRate + ') - ' + sDescription;

def __isStream(sValue):
    if (sValue == 'website'):
        return False
    return True

def parseStream():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request();

    sStreamUrl = __isAsx(sHtmlContent)
    if (sStreamUrl != False):
        #print 'ASX'
        oHoster = cHosterHandler().getHoster('asx')
        cHosterGui().showHoster(oGui, oHoster, sStreamUrl)
        oGui.setEndOfDirectory()
        return

    sStreamUrl = __isSilverlight(sHtmlContent)
    if (sStreamUrl != False):
        #print 'SILVERLIGHT'
        oHoster = cHosterHandler().getHoster('silverlight')
        cHosterGui().showHoster(oGui, oHoster, sStreamUrl)
        oGui.setEndOfDirectory()
        return
    
    sStreamUrl = __isRtmp(sHtmlContent)
    if (sStreamUrl != False):
        #print 'RTMP WITH FLV'
        oHoster = cHosterHandler().getHoster('silverlight')
        cHosterGui().showHoster(oGui, oHoster, sStreamUrl)
        oGui.setEndOfDirectory()
        return

    if (__isIFrameWithSwf(sHtmlContent)):
        print 'SWF - FUUU'

    if (__isJustinTv(sHtmlContent)):
        print 'JUSTIN - FUUU'

    

    oGui.setEndOfDirectory()

def __isSilverlight(sHtmlContent):
    sPattern = '<param Name="initParams" value="VideoSource=([^,]+),'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0] == True):
        sStreamUrl = aResult[1][0]
        if (sStreamUrl.endswith('.asx')):
            return False
        return sStreamUrl

    return False

def __isAsx(sHtmlContent):
    sPattern = '<param name="src" value="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0] == True):
        sStreamUrl = aResult[1][0]
        if (sStreamUrl.endswith('.asx')):
            return sStreamUrl

    sPattern = '<param Name="initParams" value="VideoSource=([^,]+),'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0] == True):
        sStreamUrl = aResult[1][0]
        if (sStreamUrl.endswith('.asx')):
            return sStreamUrl

    return False

def __isIFrameWithSwf(sHtmlContent):
    sPattern = '<div align="center"><u><iframe src="([^"]+)" marginwidth="0" marginheight="0"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0] == True):
        sStreamUrl = aResult[1][0]
        if (sStreamUrl.endswith('.swf')):
            return sStreamUrl

    return False

def __isJustinTv(sHtmlContent):
    sPattern = 'id="live_embed_player_flash" data="http://www.justin.tv([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0] == True):
        return True

    return False

def __isRtmp(sHtmlContent):
    sPattern = '"rtmp://(.*?)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0] == True):
        sStreamUrl = 'rtmp://' + aResult[1][0]
        return sStreamUrl

    sPattern = 'rtmp://(.*?)&'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)    
    if (aResult[0] == True):
        sStreamUrl = 'rtmp://' + aResult[1][0]
        return sStreamUrl

    return False
    






