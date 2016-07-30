from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from resources.lib.db import cDb


import xbmc, xbmcgui, xbmcplugin, sys
import xbmcaddon,xbmcvfs
import time

class cPlayer(xbmc.Player):
    
    def __init__(self, *args):
        xbmc.Player.__init__(self)
        self.loadingStarting = time.time()
        
        oInputParameterHandler = cInputParameterHandler()
        #aParams = oInputParameterHandler.getAllParameter()
        #xbmc.log(str(aParams))
        
        self.sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        self.sTitle = oInputParameterHandler.getValue('sTitle')
        #self.sSite = oInputParameterHandler.getValue('site')
        self.sSite = oInputParameterHandler.getValue('siteUrl')
        self.sThumbnail = xbmc.getInfoLabel('ListItem.Art(thumb)')
        
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
        
    def run(self, oGuiElement, sTitle, sUrl):
        sPluginHandle = cPluginHandler().getPluginHandle();
        #meta = oGuiElement.getInfoLabel()
        meta = {'label': sTitle, 'title': sTitle}
        item = xbmcgui.ListItem(path=sUrl, iconImage="DefaultVideo.png",  thumbnailImage=self.sThumbnail)
        
        item.setInfo( type="Video", infoLabels= meta )
                    
        if (cConfig().getSetting("playerPlay") == '0'):   
                            
            sPlayerType = self.__getPlayerType()
            xbmcPlayer = xbmc.Player(sPlayerType)
            xbmcPlayer.play( sUrl, item )
            xbmcplugin.endOfDirectory(sPluginHandle, True, False, False) 
            
        else:
            xbmcplugin.setResolvedUrl(sPluginHandle, True, item)
        
        timer = int(cConfig().getSetting('param_timeout'))
        xbmc.sleep(timer)
        
        while not xbmc.abortRequested:
            try: 
               self.currentTime = self.getTime()
               self.totalTime = self.getTotalTime()
            except: break
            xbmc.sleep(1000)

    def startPlayer(self):
        sPlayerType = self.__getPlayerType()
        xbmcPlayer = xbmc.Player(sPlayerType)
        oPlayList = self.__getPlayList()
        xbmcPlayer.play(oPlayList)
        timer = int(cConfig().getSetting('param_timeout'))
        xbmc.sleep(timer)            

        # while not xbmc.abortRequested:
            # try: 
               # self.currentTime = self.getTime()
               # self.totalTime = self.getTotalTime()
            # except: break
            # xbmc.sleep(1000)


    def onPlayBackEnded( self ):
        try:
            self.__setWatched()
        except: pass
        try:
            self.__setResume()
        except: pass
        #xbmc.executebuiltin( 'Container.Refresh' )

    def onPlayBackStopped( self ):
        try:
            self.__setWatched()
        except: pass
        try:
            self.__setResume()
        except: pass
        #xbmc.executebuiltin( 'Container.Refresh' )
        
    def onPlayBackStarted(self):       
        meta = {}      
        meta['title'] = self.sTitle
        #meta['hoster'] = self.sHosterIdentifier
        meta['site'] = self.sSite
        try:
            data = cDb().get_resume(meta)
            if not data == '':
                time = float(data[0][3]) / 60
                label = '%s %.2f minutes' % ('reprendre:', time)     
                oDialog = cConfig().createDialogYesNo(label)
                if (oDialog == 1):
                    seekTime = float(data[0][3])
                    self.seekTime(seekTime)
                else: 
                    pass
        except:
            pass
                
    def __setResume(self):
        meta = {}      
        meta['title'] = self.sTitle
        #meta['hoster'] = self.sHosterIdentifier
        meta['site'] = self.sSite
        meta['point'] = str(self.currentTime)
        try:
            cDb().insert_resume(meta)
        except:
            pass
            
    def __setWatched(self):
        meta = {}      
        meta['title'] = self.sTitle
        meta['site'] = self.sSite
        
        try:
            cDb().insert_watched(meta)
        except:
            pass
        
    def __getPlayerType(self):
        oConfig = cConfig()
        sPlayerType = oConfig.getSetting('playerType')
        
        try:
            if (sPlayerType == '0'):
                cConfig().log("playertype from config: auto")
                return xbmc.PLAYER_CORE_AUTO

            if (sPlayerType == '1'):
                cConfig().log("playertype from config: mplayer")
                return xbmc.PLAYER_CORE_MPLAYER

            if (sPlayerType == '2'):
                cConfig().log("playertype from config: dvdplayer")
                return xbmc.PLAYER_CORE_DVDPLAYER
        except: return False
