#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.gui.gui import cGui
from resources.lib.comaddon import addon, dialog, xbmc, isKrypton, VSlog
import xbmcplugin

#pour les sous titres
#https://github.com/amet/service.subtitles.demo/blob/master/service.subtitles.demo/service.py
#player API
#http://mirrors.xbmc.org/docs/python-docs/stable/xbmc.html#Player

class cPlayer(xbmc.Player):

    ADDON = addon()

    def __init__(self, *args):

        sPlayerType = self.__getPlayerType()
        xbmc.Player.__init__(self,sPlayerType)

        self.Subtitles_file = []
        self.SubtitleActive = False

        oInputParameterHandler = cInputParameterHandler()
        #aParams = oInputParameterHandler.getAllParameter()
        #xbmc.log(str(aParams))

        self.sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        self.sTitle = oInputParameterHandler.getValue('sTitle')
        #self.sSite = oInputParameterHandler.getValue('site')
        self.sSite = oInputParameterHandler.getValue('siteUrl')
        self.sThumbnail = xbmc.getInfoLabel('ListItem.Art(thumb)')

        self.playBackEventReceived = False
        self.playBackStoppedEventReceived = False
        self.forcestop = False

        VSlog('player initialized')

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

    def AddSubtitles(self, files):
        if isinstance(files, basestring):
            self.Subtitles_file.append(files)
        else:
            self.Subtitles_file = files

    def run(self, oGuiElement, sTitle, sUrl):

        self.totalTime = 0
        self.currentTime = 0

        sPluginHandle = cPluginHandler().getPluginHandle()

        oGui = cGui()
        item = oGui.createListItem(oGuiElement)
        item.setPath(oGuiElement.getMediaUrl())

        #meta = {'label': oGuiElement.getTitle(), 'title': oGuiElement.getTitle()}
        #item = xbmcgui.ListItem(path=sUrl, iconImage='DefaultVideo.png', thumbnailImage=self.sThumbnail)
        #item.setInfo(type='Video', infoLabels=meta)

        #Sous titres
        if (self.Subtitles_file):
            try:
                item.setSubtitles(self.Subtitles_file)
                VSlog('Load SubTitle :' + str(self.Subtitles_file))
                self.SubtitleActive = True
            except:
                VSlog("Can't load subtitle:" + str(self.Subtitles_file))

        player_conf = self.ADDON.getSetting('playerPlay')

        #Si lien dash, methode prioritaire
        if sUrl.endswith('.mpd'):
            if isKrypton() == True:
                self.enable_addon('inputstream.adaptive')
                item.setProperty('inputstreamaddon','inputstream.adaptive')
                item.setProperty('inputstream.adaptive.manifest_type', 'mpd')
                xbmcplugin.setResolvedUrl(sPluginHandle, True, listitem=item)
                VSlog('Player use inputstream addon')
            else:
                dialog().VSerror('Nécessite kodi 17 minimum')
                return
        #1 er mode de lecture
        elif (player_conf == '0'):
            self.play(sUrl,item)
            VSlog('Player use Play() method')
        #2 eme mode non utilise
        elif (player_conf == 'neverused'):
            xbmc.executebuiltin('PlayMedia(' + sUrl + ')')
            VSlog('Player use PlayMedia() method')
        #3 eme mode (defaut)
        else:
            xbmcplugin.setResolvedUrl(sPluginHandle, True, item)
            VSlog('Player use setResolvedUrl() method')

        #Attend que le lecteur demarre, avec un max de 20s
        if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
            for _ in range(20):
                if self.playBackEventReceived:
                    break
                xbmc.sleep(1000)
        else:
            for _ in xrange(20):
                if self.playBackEventReceived:
                    break
                xbmc.sleep(1000)

        #active/desactive les sous titres suivant l'option choisie dans la config
        if (self.SubtitleActive):
            if (self.ADDON.getSetting('srt-view') == 'true'):
                self.showSubtitles(True)
                dialog().VSinfo('Sous-titres chargés', 'Sous-Titres', 5)
            else:
                self.showSubtitles(False)
                dialog().VSinfo('Sous-titres chargés, vous pouvez les activer', 'Sous-Titres', 15)

        while self.isPlaying() and not self.forcestop:
        #while not xbmc.abortRequested:
            try:
                self.currentTime = self.getTime()
                self.totalTime = self.getTotalTime()

                #xbmc.log(str(self.currentTime))

            except:
                pass
                #break
            xbmc.sleep(1000)

        if not self.playBackStoppedEventReceived:
            self.onPlayBackStopped()

        #Uniquement avec la lecture avec play()
        if (player_conf == '0'):
            r = xbmcplugin.addDirectoryItem(handle=sPluginHandle, url=sUrl, listitem=item, isFolder=False)
            #xbmcplugin.endOfDirectory(sPluginHandle, True, False, False)
            return r

        VSlog('Closing player')

    #fonction light servant par exmple pour visualiser les DL ou les chaines de TV
    def startPlayer(self, window=False):
        oPlayList = self.__getPlayList()
        self.play(oPlayList, windowed=window)

    def onPlayBackEnded(self):
        self.onPlayBackStopped()

    #Attention pas de stop, si on lance une seconde video sans fermer la premiere
    def onPlayBackStopped(self):
        VSlog('player stoped')
        self.playBackStoppedEventReceived = True

        #calcul le temp de lecture
        pourcent =  0
        if self.totalTime > 0:
            pourcent = float('%.2f' % (self.currentTime / self.totalTime))
        if (pourcent > 0.90):

            # Marqué VU dans la BDD Vstream
            cGui().setWatched()

            # Marqué VU dans les comptes perso
            try:
                tmdb_session = self.ADDON.getSetting('tmdb_session')
                if tmdb_session:
                    self.__getWatchlist('tmdb')
                bstoken = self.ADDON.getSetting('bstoken')
                if bstoken:
                    self.__getWatchlist('trakt')
            except:
                pass

        #xbmc.executebuiltin('Container.Refresh')

    def onPlayBackStarted(self):
        VSlog('player started')

        #Si on recoit une nouvelle fois l'event, c'est que ca buggue, on stope tout
        if self.playBackEventReceived:
            self.forcestop = True
            return

        self.playBackEventReceived = True

    def __getWatchlist(self, sAction):

        if sAction == 'tmdb':
            plugins = __import__('resources.sites.themoviedb_org', fromlist=['themoviedb_org'])
            function = getattr(plugins, 'getWatchlist')
            function()
        elif sAction == 'trakt':
            #plugins = __import__('resources.lib.trakt', fromlist=['cTrakt'])
            plugins = __import__('resources.lib.trakt', fromlist=['trakt']).cTrakt()
            function = getattr(plugins, 'getWatchlist')
            function()

        return

    def __getPlayerType(self):
        sPlayerType = self.ADDON.getSetting('playerType')

        try:
            if (sPlayerType == '0'):
                VSlog('playertype from config: auto')
                return xbmc.PLAYER_CORE_AUTO

            if (sPlayerType == '1'):
                VSlog('playertype from config: mplayer')
                return xbmc.PLAYER_CORE_MPLAYER

            if (sPlayerType == '2'):
                VSlog('playertype from config: dvdplayer')
                return xbmc.PLAYER_CORE_DVDPLAYER
        except:
            return False

    def enable_addon(self,addon):
        #import json
        #sCheck = {'jsonrpc': '2.0','id': 1,'method': 'Addons.GetAddonDetails','params': {'addonid':'inputstream.adaptive','properties': ['enabled']}}
        #response = xbmc.executeJSONRPC(json.dumps(sCheck))
        #data = json.loads(response)
        #if not 'error' in data.keys():
        #if data['result']['addon']['enabled'] == False:

        if xbmc.getCondVisibility('System.HasAddon(inputstream.adaptive)') == 0:
            do_json = '{"jsonrpc":"2.0","id":1,"method":"Addons.SetAddonEnabled","params":{"addonid":"inputstream.adaptive","enabled":true}}'
            query = xbmc.executeJSONRPC(do_json)
            VSlog("Activation d'inputstream.adaptive")
        else:
            VSlog('inputstream.adaptive déjà activé')
