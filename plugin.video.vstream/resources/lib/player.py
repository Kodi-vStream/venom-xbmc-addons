#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.gui.gui import cGui
from resources.lib.upnext import UpNext
from resources.lib.comaddon import addon, dialog, xbmc, isKrypton, VSlog, addonManager
from resources.lib.db import cDb
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

        self.sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        self.sTitle = oInputParameterHandler.getValue('sTitle')
        self.sSite = oInputParameterHandler.getValue('siteUrl')
        self.sThumbnail = xbmc.getInfoLabel('ListItem.Art(thumb)')

        self.playBackEventReceived = False
        self.playBackStoppedEventReceived = False
        self.forcestop = False
        self.multi = False  # Plusieurs vidéos se sont enchainées

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
        try:
            basestring
        except:
            basestring = str
            
        if len(files) == 1:
            self.Subtitles_file = files[0]
        elif isinstance(files, basestring):
            self.Subtitles_file.append(files)
        else:
            self.Subtitles_file = files

    def run(self, oGuiElement, sTitle, sUrl):

        # Lancement d'une vidéo sans avoir arreté la précedente
        if self.isPlaying():
            self.multi = True
            self._setWatched() # la vidéo en cours doit être marquée comme VUE
            
        self.totalTime = 0
        self.currentTime = 0

        sPluginHandle = cPluginHandler().getPluginHandle()

        oGui = cGui()
        item = oGui.createListItem(oGuiElement)
        item.setPath(oGuiElement.getMediaUrl())

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
        if sUrl.endswith('.mpd') or sUrl.split('?')[0][-4:] in '.mpd':
            if isKrypton() == True:
                addonManager().enableAddon('inputstream.adaptive')
                item.setProperty('inputstream','inputstream.adaptive')
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
        for _ in range(20):
            if self.playBackEventReceived:
                break
            xbmc.sleep(1000)

        #active/desactive les sous titres suivant l'option choisie dans la config
        if self.isPlaying and self.getAvailableSubtitleStreams():
            if (self.ADDON.getSetting('srt-view') == 'true'):
                self.showSubtitles(True)
            else:
                self.showSubtitles(False)
                dialog().VSinfo('Des sous-titres sont disponibles', 'Sous-Titres', 4)

        waitingNext = 0
        
        while self.isPlaying() and not self.forcestop:
            try:
                self.currentTime = self.getTime()

                waitingNext += 1
                if waitingNext == 8: # attendre un peu avant de chercher le prochain épisode d'une série
                    self.totalTime = self.getTotalTime()
                    self.infotag = self.getVideoInfoTag()
                    UpNext().nextEpisode(oGuiElement)

            except Exception as err:
                VSlog("Exception run: {0}".format(err))

            xbmc.sleep(1000)

        if not self.playBackStoppedEventReceived:
            self.onPlayBackStopped()

        #Uniquement avec la lecture avec play()
        if (player_conf == '0'):
            r = xbmcplugin.addDirectoryItem(handle=sPluginHandle, url=sUrl, listitem=item, isFolder=False)
            return r

        VSlog('Closing player')
        return True

    #fonction light servant par exemple pour visualiser les DL ou les chaines de TV
    def startPlayer(self, window=False):
        oPlayList = self.__getPlayList()
        self.play(oPlayList, windowed=window)

    def onPlayBackEnded(self):
        self.onPlayBackStopped()

    #Attention pas de stop, si on lance une seconde video sans fermer la premiere
    def onPlayBackStopped(self):
        VSlog('player stopped')
        self.playBackStoppedEventReceived = True

        self._setWatched()


    # MARQUER VU
    # utilise les informations de la vidéo qui vient d'etre lue
    # qui n'est pas celle qui a été lancée si plusieurs vidéos se sont enchainées
    def _setWatched(self):

        try:
            if self.isPlaying():
                self.totalTime = self.getTotalTime()
                self.currentTime = self.getTime()
                self.infotag = self.getVideoInfoTag()
    
            if self.totalTime > 0:
                pourcent = float('%.2f' % (self.currentTime / self.totalTime))
    
                #calcul le temp de lecture
                # Dans le cas ou ont a vu intégralement le contenu, percent = 0.0
                # Mais on a tout de meme terminé donc le temps actuel est egal au temps total.
                if (pourcent > 0.90) or (pourcent == 0.0 and self.currentTime == self.totalTime):
    
                    # Marquer VU dans la BDD Vstream
                    # infotag = self.getVideoInfoTag()
                    siteUrl = self.infotag.getPath()
                    sTitleWatched = self.infotag.getOriginalTitle()
                    if sTitleWatched:
                        db = cDb()
                        meta = {}
                        meta['title'] = sTitleWatched
                        meta['site'] = siteUrl
                        db.insert_watched(meta)
    
                        # RAZ du point de reprise
                        db.del_resume(meta)
                    
                    # Marquer VU dans les comptes perso
                    # NE FONCTIONNE PAS SI PLUSIEURS VIDEOS SE SONT ENCHAINEES (cas des épisodes)
                    if not self.multi:
                        tmdb_session = self.ADDON.getSetting('tmdb_session')
                        if tmdb_session:
                            self.__getWatchlist('tmdb')
    
                        bstoken = self.ADDON.getSetting('bstoken')
                        if bstoken:
                            self.__getWatchlist('trakt')

                # Sauvegarde du point de lecture pour une reprise
                elif self.currentTime > 180.0:
                    sTitleWatched = self.infotag.getOriginalTitle()
                    if sTitleWatched:
                        db = cDb()
                        meta = {}
                        meta['title'] = sTitleWatched
                        meta['site'] = self.sSite
                        meta['point'] = self.currentTime
                        matchedrow = db.insert_resume(meta)

        except Exception as err:
            VSlog("ERROR Player_setWatched : {0}".format(err))

    #def onPlayBackStarted(self):
    def onAVStarted(self):
        VSlog('player started')

        #Si on recoit une nouvelle fois l'event, c'est que ca buggue, on stope tout
        if self.playBackEventReceived:
            self.forcestop = True
            return

        self.playBackEventReceived = True

        # Reprendre la lecture
        if self.getTime() < 180:  # si supérieur à 3 minutes, la gestion de la reprise est assuré par KODI
            self.infotag = self.getVideoInfoTag()
            sTitleWatched = self.infotag.getOriginalTitle()
            if sTitleWatched:
                db = cDb()
                meta = {}
                meta['title'] = sTitleWatched
                resumePoint = db.get_resume(meta)
                if resumePoint:
                    h = resumePoint//3600
                    ms = resumePoint-h*3600
                    m = ms//60
                    s = ms-m*60
                    ret = dialog().VSselect(['Reprendre depuis %02d:%02d:%02d' %(h, m, s), 'Lire depuis le début'], 'Reprendre la lecture')
                    if ret == 0:
                        self.seekTime(resumePoint)
                    elif ret == 1:
                        self.seekTime(0.0)
                        # RAZ du point de reprise
                        db.del_resume(meta)


    def __getWatchlist(self, sAction):

        if sAction == 'tmdb':
            plugins = __import__('resources.sites.themoviedb_org', fromlist=['themoviedb_org'])
            function = getattr(plugins, 'getWatchlist')
            function()
        elif sAction == 'trakt':
            plugins = __import__('resources.lib.trakt', fromlist=['trakt']).cTrakt()
            function = getattr(plugins, 'getAction')
            function(Action="SetWatched")

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

