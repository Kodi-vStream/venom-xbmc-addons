from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
import xbmc
import time

class runplayer(xbmc.Player):
    def __init__(self, *args):
        xbmc.Player.__init__(self)
        self.loadingStarting = time.time()

    def onPlayBackStarted(self):
        #xbmc commence a jouer un fichier
        cConfig().showInfo('vStream', 'Demarrer')

    def onPlayBackPaused(self):
        #utilisateur fait une pause un fichier de jeu.
        cConfig().showInfo('vStream', 'Pause')

    def onPlayBackResumed(self):
        #utilisateur reprend un fichier en pause .
        cConfig().showInfo('vStream', 'Pause')

    def onPlayBackEnded( self ):
        #xbmc arrete de jouer un fichier .
        cConfig().showInfo('vStream', 'Fichier endommage ou illisible')

    def onPlayBackStopped( self ):
        #utilisateur arrete xbmc lecture d'un fichier .
        cConfig().showInfo('vStream', 'Stop')


class cPlayer():
    
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
        sPlayerType = self.__getPlayerType()
        xbmcPlayer = xbmc.Player(sPlayerType)
        oPlayList = self.__getPlayList()
        xbmcPlayer.play(oPlayList)
        timer = int(cConfig().getSetting('param_timeout'))
        xbmc.sleep(timer)
        try:
            
            if xbmcPlayer.getPlayingFile(): 
                cConfig().log("Start Player " + xbmcPlayer.getPlayingFile())
                
        except:
            cConfig().showInfo('vStream', 'Timeout')
            cConfig().log("Start Player Impossible")

        #player = runplayer()
        #while not xbmc.abortRequested:
        #    xbmc.sleep(500)
        #del player

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
            cConfig().log("playertype from config: auto")
            return xbmc.PLAYER_CORE_AUTO

        if (sPlayerType == '1'):
            cConfig().log("playertype from config: mplayer")
            return xbmc.PLAYER_CORE_MPLAYER

        if (sPlayerType == '2'):
            cConfig().log("playertype from config: dvdplayer")
            return xbmc.PLAYER_CORE_DVDPLAYER
