from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.config import cConfig
import logger
from resources.lib.gui.gui import cGui
import xbmc

class cPlayer:
    
    def clearPlayList(self):
        oPlaylist = self.__getPlayList()
	oPlaylist.clear()

    def __getPlayList(self):
        return xbmc.PlayList(xbmc.PLAYLIST_VIDEO)

    def addItemToPlaylist(self, oGuiElement):
        oGui = cGui()
        oListItem =  oGui.createListItem(oGuiElement)
        self.__addItemToPlaylist(oGuiElement, oListItem)
	
    def __addItemToPlaylist(self, oGuiElement, oListItem):    
	oPlaylist = self.__getPlayList()	
	oPlaylist.add(oGuiElement.getMediaUrl(), oListItem )

    def startPlayer(self):
        logger.info('start player')
        sPlayerType = self.__getPlayerType()
        xbmcPlayer = xbmc.Player(sPlayerType)
        oPlayList = self.__getPlayList()
	xbmcPlayer.play(oPlayList)
        

        # dirty, but is works 
        if (cConfig().isDharma() == False):
            oInputParameterHandler = cInputParameterHandler()
            aParams = oInputParameterHandler.getAllParameter()

            oGui = cGui()
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(aParams['site'])
            oGuiElement.setFunction(aParams['function'])
            oGui.addFolder(oGuiElement)
            oGui.setEndOfDirectory()


    def __getPlayerType(self):
        oConfig = cConfig()
        sPlayerType = oConfig.getSetting('playerType')

        if (sPlayerType == '0'):
            logger.info('playertype from config: auto')
            return xbmc.PLAYER_CORE_AUTO

        if (sPlayerType == '1'):
            logger.info('playertype from config: mplayer')
            return xbmc.PLAYER_CORE_MPLAYER

        if (sPlayerType == '2'):
            logger.info('playertype from config: dvdplayer')
            return xbmc.PLAYER_CORE_DVDPLAYER
