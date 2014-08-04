#-*- coding: utf-8 -*-
#Venom.
from resources.lib.handler.jdownloaderHandler import cJDownloaderHandler
from resources.lib.download import cDownload
from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.contextElement import cContextElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.player import cPlayer
from resources.lib.handler.requestHandler import cRequestHandler
import logger

class cHosterGui:

    SITE_NAME = 'cHosterGui'

    # step 1 - bGetRedirectUrl in ein extra optionsObject verpacken
    def showHoster(self, oGui, oHoster, sMediaUrl, sThumbnail, bGetRedirectUrl = False):
        
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        #oGuiElement.setFunction('showHosterMenu')
        oGuiElement.setFunction('play')
        oGuiElement.setTitle(oHoster.getDisplayName())
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setIcon('host.png')
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        
        #context menu
        oContext = cContextElement()
        oContext.setFile('cHosterGui')
        oContext.setSiteName(self.SITE_NAME)
        oContext.setFunction('addToPlaylist')
        oContext.setTitle('Add to playlist')
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)

        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def checkHoster(self, sHosterUrl): 
    
    
        if ('novamov' in sHosterUrl):
            return cHosterHandler().getHoster('novamov')
        if ('divxstage' in sHosterUrl):
            return cHosterHandler().getHoster('divxstage')
        if ('filestage' in sHosterUrl):
            return cHosterHandler().getHoster('filestage')
        if ('vidxden' in sHosterUrl):
            return cHosterHandler().getHoster('vidxden')
        if ('vidbux' in sHosterUrl):
            return cHosterHandler().getHoster('vidbux')
        if ('megavideo' in sHosterUrl):
            return cHosterHandler().getHoster('megavideo')
        if ('videoweed' in sHosterUrl):
            return cHosterHandler().getHoster('videoweed')
        if ('youwatch' in sHosterUrl):
            return cHosterHandler().getHoster('youwatch')
        if ('turbovid' in sHosterUrl):
            return cHosterHandler().getHoster('turbovid')
        if ('youtube' in sHosterUrl):
            return cHosterHandler().getHoster('youtube')   
        if ('rutube' in sHosterUrl):
            return cHosterHandler().getHoster('rutube')
        if ('exashare' in sHosterUrl):
            return cHosterHandler().getHoster('exashare')
        if ('nowvideo' in sHosterUrl):
            return cHosterHandler().getHoster('nowvideo')
        if ('vk' in sHosterUrl):
            return cHosterHandler().getHoster('vk')
        if ('videomega' in sHosterUrl):
            return cHosterHandler().getHoster('videomega')
        if ('vidto' in sHosterUrl):
            return cHosterHandler().getHoster('vidto')
        if ('vidzi' in sHosterUrl):
            return cHosterHandler().getHoster('vidzi')

        return False
        # step 2
    def showHosterMenu(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
	sFileName = oInputParameterHandler.getValue('sFileName')

        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
	oHoster.setFileName(sFileName)

        # play
        self.__showPlayMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl)

	# playlist
	self.__showPlaylistMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl)

        # download
        if (oHoster.isDownloadable() == True):
            self.__showDownloadMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl)        

        # JD
        if (oHoster.isJDownloaderable() == True):
            self.__showJDMenu(oGui, sMediaUrl, oHoster, bGetRedirectUrl)	

        oGui.setEndOfDirectory()

    def __showPlayMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('play')
        oGuiElement.setTitle('play')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
	oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def __showDownloadMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('download')
        oGuiElement.setTitle('download ueber XBMC')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
	oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def __showJDMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)        
        oGuiElement.setTitle('an JDownloader senden')
        oGuiElement.setFunction('sendToJDownbloader')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
	oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def __showPlaylistMenu(self, oGui, sMediaUrl, oHoster, bGetRedirectUrl):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('addToPlaylist')
        oGuiElement.setTitle('add to playlist')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
	oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def play(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
	sFileName = oInputParameterHandler.getValue('sFileName')

        if (bGetRedirectUrl == 'True'):            
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        logger.info('call play: ' + sMediaUrl)
        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
	oHoster.setFileName(sFileName)

        #try:
        
        oHoster.setUrl(sMediaUrl)
        aLink = oHoster.getMediaLink()
        
        if (aLink[0] == True):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(aLink[1])
	    oGuiElement.setTitle(oHoster.getFileName())

            oPlayer = cPlayer()
	    oPlayer.clearPlayList()
            oPlayer.addItemToPlaylist(oGuiElement)
            oPlayer.startPlayer()
            return

        #except:
        #    logger.fatal('could not load plugin: ' + sHosterFileName)

        oGui.setEndOfDirectory()

    def addToPlaylist(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')
        
        print sMediaUrl

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        logger.info('call play: ' + sMediaUrl)
        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
	oHoster.setFileName(sFileName)

        #try:

        oHoster.setUrl(sMediaUrl)
        aLink = oHoster.getMediaLink()

        if (aLink[0] == True):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(aLink[1])
	    oGuiElement.setTitle(oHoster.getFileName())

            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            oGui.showInfo('Playlist', str(oHoster.getFileName()), 5);
            return

        #except:
        #    logger.fatal('could not load plugin: ' + sHosterFileName)

        oGui.setEndOfDirectory()

    def download(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
	sFileName = oInputParameterHandler.getValue('sFileName')

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        logger.info('call download: ' + sMediaUrl)

        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
	oHoster.setFileName(sFileName)

        #try:
        oHoster.setUrl(sMediaUrl)
        aLink = oHoster.getMediaLink()
        if (aLink[0] == True):
            oDownload = cDownload()
            oDownload.download(aLink[1], oHoster.getFileName())
            return

        #except:
        #    logger.fatal('could not load plugin: ' + sHosterFileName)

        oGui.setEndOfDirectory()

    def sendToJDownbloader(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
	sFileName = oInputParameterHandler.getValue('sFileName')

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        oHoster = cHosterHandler().getHoster(sHosterIdentifier)
	oHoster.setFileName(sFileName)
        oHoster.setUrl(sMediaUrl)
        sMediaUrl = oHoster.getUrl()

        logger.info('call send to JDownloader: ' + sMediaUrl)

        cJDownloaderHandler().sendToJDownloader(sMediaUrl)

        

    def __getRedirectUrl(self, sUrl):
        oRequest = cRequestHandler(sUrl)
        oRequest.request()
        return oRequest.getRealUrl()
