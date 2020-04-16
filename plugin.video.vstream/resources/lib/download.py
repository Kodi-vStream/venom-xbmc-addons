# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.player import cPlayer
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.db import cDb
from resources.lib.util import cUtil, UnquotePlus
from resources.lib.comaddon import addon, dialog, progress, VSlog, VSupdate, xbmc , xbmcgui
import urllib2
import xbmcplugin
import xbmcvfs
import re, sys
import threading

# try:
#     import StorageServer
#     Memorise = StorageServer.StorageServer('VstreamDownloader')
# except:
#     print 'Le download ne marchera pas correctement'


SITE_IDENTIFIER = 'cDownload'

# http://kodi.wiki/view/Add-on:Common_plugin_cache
# https://pymotw.com/2/threading/
# https://code.google.com/p/navi-x/source/browse/trunk/Navi-X/src/CDownLoader.py?r=155


#status = 0 => pas telechargé
#status = 1 => en cours de DL (ou bloque si bug)
#status = 2 => fini de DL

#GetProperty('arret') = '0' => Telechargement en cours
#GetProperty('arret') = '1' => Arret demandé
#GetProperty('arret') = '' =>  Jamais eu de telechargement


class cDownloadProgressBar(threading.Thread):
    DIALOG = dialog()
    ADDON = addon()

    def __init__(self, *args, **kwargs):

        self.__sTitle = ''
        self.__sUrl = ''
        self.__fPath = ''
        self.__bFastMode = False

        if kwargs:
            self.__sTitle = kwargs['title']
            self.__sUrl = kwargs['url']
            self.__fPath = kwargs['Dpath']
            if 'FastMode' in kwargs:
                print 'Téléchargement en mode Turbo'
                self.__bFastMode = True

        threading.Thread.__init__(self)

        self.processIsCanceled = False
        self.oUrlHandler = None
        self.file = None
        self.__oDialog = None

        # self.currentThread = threading.Thread(target=self.run)
        # self.currentThread.start()

    def createProcessDialog(self):
        self.__oDialog = xbmcgui.DialogProgressBG()
        self.__oDialog.create('Download')
        # xbmc.sleep(1000)
        return self.__oDialog

    def _StartDownload(self):

        # print 'Thread actuel'
        # print threading.current_thread().getName()

        diag = self.createProcessDialog()
        # diag.isFinished()

        xbmcgui.Window(10101).setProperty('arret', '0')
        # self.Memorise.set('VstreamDownloaderWorking', '1')

        headers = self.oUrlHandler.info()

        # print headers

        iTotalSize = -1
        if 'content-length' in headers:
            iTotalSize = int(headers['Content-Length'])

        chunk = 16 * 1024
        TotDown = 0

        # mise a jour pour info taille
        self.__updatedb(TotDown, iTotalSize)
        self.DIALOG.VSinfo(self.ADDON.VSlang(30086))

        while not (self.processIsCanceled or diag.isFinished()):

            data = self.oUrlHandler.read(chunk)
            if not data:
                print 'DL err'
                break

            self.file.write(data)
            TotDown = TotDown + data.__len__()
            self.__updatedb(TotDown, iTotalSize)

            self.__stateCallBackFunction(TotDown, iTotalSize)
            # if self.Memorise.get('VstreamDownloaderWorking') == '0':
                # self.processIsCanceled = True
            if xbmcgui.Window(10101).getProperty('arret') == '1':
                self.processIsCanceled = True

            # petite pause, ca ralentit le download mais evite de bouffer 100/100 ressources
            if not self.__bFastMode:
                xbmc.sleep(300)

        self.oUrlHandler.close()
        self.file.close()
        self.__oDialog.close()

        # On autorise le prochain DL
        # ????????????????
        # Memorise.unlock('VstreamDownloaderLock')

        # fait une pause pour fermer le Dialog
        xbmc.sleep(900)

        # if download finish
        meta = {}
        meta['path'] = self.__fPath
        meta['size'] = TotDown
        meta['totalsize'] = iTotalSize

        if (TotDown == iTotalSize) and (iTotalSize > 10000):
            meta['status'] = 2
            try:
                cDb().update_download(meta)
                self.DIALOG.VSinfo(self.ADDON.VSlang(30003), self.__sTitle)
                self.RefreshDownloadList()
            except:
                pass
        else:
            meta['status'] = 0
            try:
                cDb().update_download(meta)
                self.DIALOG.VSinfo(self.ADDON.VSlang(30004), self.__sTitle)
                self.RefreshDownloadList()
            except:
                pass
            return

        # ok tout est bon on continu ou pas?
        # if Memorise.get('SimpleDownloaderQueue') == '1':
        if xbmcgui.Window(10101).getProperty('SimpleDownloaderQueue') == '1':
            print 'Download suivant'
            tmp = cDownload()
            data = tmp.GetNextFile()
            tmp.StartDownload(data)

    def __updatedb(self, TotDown, iTotalSize):
        # percent 3 chiffre
        percent = '{0:.2f}'.format(min(100 * float(TotDown) / float(iTotalSize), 100))
        if percent in ['0.00', '10.00', '20.00', '30.00', '40.00', '50.00', '60.00', '70.00', '80.00', '90.00']:
            meta = {}
            meta['path'] = self.__fPath
            meta['size'] = TotDown
            meta['totalsize'] = iTotalSize
            meta['status'] = 1

            try:
                cDb().update_download(meta)
                self.RefreshDownloadList()
            except:
                pass

    def __stateCallBackFunction(self, iDownsize, iTotalSize):

        if self.__oDialog.isFinished():
            self.createProcessDialog()

        iPercent = int(float(iDownsize * 100) / iTotalSize)
        self.__oDialog.update(iPercent, self.__sTitle, self.__formatFileSize(float(iDownsize)) + '/' + self.__formatFileSize(iTotalSize))

        if (self.__oDialog.isFinished()) and not (self.__processIsCanceled):
            self.__processIsCanceled = True
            self.__oDialog.close()

    def run(self):

        try:
            # Recuperation url simple
            url = self.__sUrl.split('|')[0]
            # Recuperation des headers du lien
            headers = {}
            if len (self.__sUrl.split('|')) > 1:
                u = self.__sUrl.split('|')[1].split('&')
                for i in u:
                    headers[i.split('=')[0]] = i.replace(i.split('=')[0] + '=', '')

            # Rajout du user-agent si abscent
            if not ('User-Agent' in headers):
                headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

            req = urllib2.Request(url, None, headers)

            self.oUrlHandler = urllib2.urlopen(req, timeout = 30)
            # self.__instance = repr(self)
            self.file = xbmcvfs.File(self.__fPath, 'w')
        except:
            VSlog('download error', self.__sUrl)
            self.DIALOG.VSinfo('Download error', self.ADDON.VSlang(30011))
            return

        # if not Memorise.lock('VstreamDownloaderLock'):
        #     self.DIALOG.VSinfo('Téléchargements déjà démarrés', 'Download error')
        #     return

        if xbmc.getCondVisibility('Window.IsVisible(10151)'):
            self.DIALOG.VSinfo('Erreur', self.ADDON.VSlang(30012))
            return

        self._StartDownload()

    def __formatFileSize(self, iBytes):
        iBytes = int(iBytes)
        if (iBytes == 0):
            return '%.*f %s' % (2, 0, 'MB')

        return '%.*f %s' % (2, iBytes/(1024*1024.0), 'MB')

    def StopAll(self):

        self.processIsCanceled = True
        # Memorise.unlock('VstreamDownloaderLock')
        # Memorise.set('SimpleDownloaderQueue', '0')
        xbmcgui.Window(10101).setProperty('SimpleDownloaderQueue', '0')

        xbmcgui.Window(10101).setProperty('arret', '1')
        try:
            self.__oDialog.close()
        except:
            pass

        return

    def RefreshDownloadList(self):
        # print xbmc.getInfoLabel('Container.FolderPath')
        if 'function=getDownload' in xbmc.getInfoLabel('Container.FolderPath'):
            VSupdate()


class cDownload:
    DIALOG = dialog()
    ADDON = addon()

    def __init__(self):
        pass

    def __createDownloadFilename(self, sTitle):
        sTitle = re.sub(' +', ' ', sTitle)  # Vire double espace
        valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        filename = ''.join(c for c in sTitle if c in valid_chars)
        filename = filename.replace(' .', '.')
        if filename.startswith(' '):
            filename = filename[1:]
        # filename = filename.replace(' ', '_')  # pas besoin de ca, enfin pr moi en tout cas
        return filename

    def __formatFileSize(self, iBytes):
        iBytes = int(iBytes)
        if iBytes == 0:
            return '%.*f %s' % (2, 0, 'MB')

        return '%.*f %s' % (2, iBytes/(1024*1024.0), 'MB')

    def isDownloading_old(self):

        if not Memorise.get('VstreamDownloaderLock'):
            return False
        return True

    def isDownloading(self):

        if not xbmc.getCondVisibility('Window.IsVisible(10151)'):
            return False
        return True

    def download(self, sDBUrl, sTitle, sDownloadPath, FastMode=False):

        if self.isDownloading():
            self.DIALOG.VSinfo('Erreur', self.ADDON.VSlang(30012))
            return False

        self.__sTitle = sTitle

        # resolve url
        from resources.lib.gui.hoster import cHosterGui
        oHoster = cHosterGui().checkHoster(sDBUrl)
        oHoster.setUrl(sDBUrl)
        aLink = oHoster.getMediaLink()
        # aLink = (True,'https://github.com/LordVenom/venom-xbmc-addons-beta/blob/master/plugin.video.vstream/Thumbs.db?raw=true')

        if aLink[0]:
            sUrl = aLink[1]
        else:
            print 'Lien non resolvable'
            self.DIALOG.VSinfo(self.ADDON.VSlang(30022), sTitle)
            return False

        if (not sUrl.startswith('http')) or sUrl.split('|')[0].endswith('.m3u8'):
            self.DIALOG.VSinfo(self.ADDON.VSlang(30022), sTitle)
            return False

        try:
            VSlog('Download', str(sUrl))

            # background download task
            if FastMode:
                cDownloadProgressBar(title=self.__sTitle, url=sUrl, Dpath=sDownloadPath, FastMode=True ).start()
            else:
                cDownloadProgressBar(title = self.__sTitle, url = sUrl, Dpath = sDownloadPath ).start()

            VSlog('Download Ok', sDownloadPath)

        except:
            self.DIALOG.VSinfo(self.ADDON.VSlang(30024), sTitle)
            VSlog('Unable to download')
            return False

        return True

    def __createTitle(self, sUrl, sTitle):

        #sTitle = re.sub('[\(\[].+?[\)\]]',' ', sTitle)
        sTitle = cUtil().FormatSerie(sTitle)
        sTitle = cUtil().CleanName(sTitle)

        aTitle = sTitle.rsplit('.')
        # Si deja extension
        if (len(aTitle) > 1):
            return sTitle

        # recherche d'une extension
        sUrl = sUrl.lower()
        m = re.search('(flv|avi|mp4|mpg|mpeg|mkv)', sUrl)
        if m:
            sTitle = sTitle + '.' + m.group(0)
        else:
            sTitle = sTitle + '.flv'  # Si quedale on en prend une au pif

        return sTitle

    def getDownload(self):

        oGui = cGui()
        sPluginHandle = cPluginHandler().getPluginHandle()
        sPluginPath = cPluginHandler().getPluginPath()
        sItemUrl = '%s?site=%s&function=%s&title=%s' % (sPluginPath, SITE_IDENTIFIER, 'StartDownloadList', 'title')
        meta = {'title': 'Démarrer la liste'}
        item = xbmcgui.ListItem('Démarrer la liste', iconImage = 'special://home/addons/plugin.video.vstream/resources/art/download.png')

        # item.setInfo(type='Video', infoLabels=meta)
        # item.setProperty('Video', 'false')
        # item.setProperty('IsPlayable', 'false')

        xbmcplugin.addDirectoryItem(sPluginHandle, sItemUrl, item, isFolder=False)

        oOutputParameterHandler = cOutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'StopDownloadList', self.ADDON.VSlang(30025), 'download.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'getDownloadList', self.ADDON.VSlang(30039), 'listes.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'CleanDownloadList', self.ADDON.VSlang(30040), 'download.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def CleanDownloadList(self):

        try:
            cDb().clean_download()
            self.DIALOG.VSinfo(self.ADDON.VSlang(30071))
        except:
            pass

        return

    def dummy(self):
        return

    def StartDownloadOneFile(self, meta=[]):
        if not meta:
            meta = self.GetOnefile()

        xbmcgui.Window(10101).setProperty('SimpleDownloaderQueue', '0')
        self.StartDownload(meta)

    def ResetDownload(self):
        oInputParameterHandler = cInputParameterHandler()
        url = oInputParameterHandler.getValue('sUrl')
        meta = {}
        meta['url'] = url

        try:
            cDb().reset_download(meta)
            self.DIALOG.VSinfo(self.ADDON.VSlang(30071))
            VSupdate()
        except:
            pass

        return

    def ReadDownload(self):
        oInputParameterHandler = cInputParameterHandler()
        path = oInputParameterHandler.getValue('sPath')
        sTitle = oInputParameterHandler.getValue('sMovieTitle')

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(SITE_IDENTIFIER)
        oGuiElement.setMediaUrl(path)
        oGuiElement.setTitle(sTitle)
        #oGuiElement.getInfoLabel()

        oPlayer = cPlayer()
        #oPlayer.clearPlayList()
        #oPlayer.addItemToPlaylist(oGuiElement)
        if not (sys.argv[ 1 ] == '-1'):
            oPlayer.run(oGuiElement, sTitle, path)
        else:
            oPlayer.clearPlayList()
            oPlayer.addItemToPlaylist(oGuiElement)
            oPlayer.startPlayer()

    def DelFile(self):
        oInputParameterHandler = cInputParameterHandler()
        path = oInputParameterHandler.getValue('sPath')

        oDialog = self.DIALOG.VSyesno(self.ADDON.VSlang(30074))
        if (oDialog == 1):
            meta = {}
            meta['url'] = ''
            meta['path'] = path

            try:
                cDb().del_download(meta)
                xbmcvfs.delete(path)
                self.DIALOG.VSinfo(self.ADDON.VSlang(30072))
                VSupdate()
            except:
                self.DIALOG.VSinfo(self.ADDON.VSlang(30073))

    def GetNextFile(self):
        row = cDb().get_download()

        for data in row:
            status = data[8]

            if status == '0':
                return data

        return None

    def GetOnefile(self):
        oInputParameterHandler = cInputParameterHandler()
        url = oInputParameterHandler.getValue('sUrl')

        meta = {}
        meta['url'] = url

        row = cDb().get_download(meta)

        if not (row):
            return None

        return row[0]

    def StartDownload(self,data):
        if not (data):
            return

        title = data[1]
        url = UnquotePlus(data[2])
        path = data[3]
        #thumbnail = UnquotePlus(data[4])
        #status = data[8]

        self.download(url,title,path)

    def StartDownloadList(self):
        self.DIALOG.VSinfo(self.ADDON.VSlang(30075))
        #Memorise.set('SimpleDownloaderQueue', '1')
        xbmcgui.Window(10101).setProperty('SimpleDownloaderQueue', '1')
        data = self.GetNextFile()
        self.StartDownload(data)

    def StopDownloadList(self):

        #oInputParameterHandler = cInputParameterHandler()
        #path = oInputParameterHandler.getValue('sPath')
        #status = oInputParameterHandler.getValue('sStatus')


        #WINDOW_PROGRESS = xbmcgui.Window(10101)
        #WINDOW_PROGRESS.close()
        #xbmcgui.Window(10101).setProperty('arret', '1')
        #xbmc.executebuiltin('Dialog.Close(%s, true)' % 10101)
        #xbmc.getCondVisibility('Window.IsActive(10101)')

        #thread actif
        if xbmcgui.Window(10101).getProperty('arret') == '0':
            xbmcgui.Window(10101).setProperty('arret', '1')
        #si bug
        else:
            cDownloadProgressBar().StopAll()

        #On remet tout les status a 0 ou 2
        cDb().cancel_download()

        VSupdate()

        return

    def getDownloadList(self):
        oGui = cGui()
        # oInputParameterHandler = cInputParameterHandler()

        row = cDb().get_download()

        for data in row:

            title = data[1]
            url = UnquotePlus(data[2])
            path = data[3]
            # cat = data[4]
            thumbnail = UnquotePlus(data[5])
            #The url is unicode format? Not managed yet
            try:
                thumbnail = str(thumbnail)
            except:
                thumbnail = ''

            size = data[6]
            totalsize = data[7]
            status = data[8]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sUrl', url)
            oOutputParameterHandler.addParameter('sMovieTitle', title)
            oOutputParameterHandler.addParameter('sThumbnail', thumbnail)
            oOutputParameterHandler.addParameter('sPath', path)
            oOutputParameterHandler.addParameter('sStatus', status)

            if status == '0':
                sStatus = ''
            elif status == '1':
                sStatus = '[COLOR=red][En cours] [/COLOR]'
            elif status == '2':
                sStatus='[COLOR=green][Fini] [/COLOR]'

            if size:
                sTitle = sStatus + title + ' (' + self.__formatFileSize(size) + '/' + self.__formatFileSize(totalsize) + ')'
            else:
                sTitle = sStatus + title

            oGuiElement = cGuiElement()

            if not thumbnail or thumbnail == 'False':
                thumbnail = 'mark.png'

            oGuiElement.setSiteName(SITE_IDENTIFIER)
            if status == '2':
                oGuiElement.setFunction('ReadDownload')
            else:
                #oGuiElement.setFunction('StartDownloadOneFile')  # marche pas a cause de fenetre xbmc
                oGuiElement.setFunction('ReadDownload')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setIcon('download.png')
            oGuiElement.setMeta(0)
            oGuiElement.setThumbnail(thumbnail)

            oGui.createContexMenuDownload(oGuiElement, oOutputParameterHandler, status)

            oGui.addFolder(oGuiElement, oOutputParameterHandler)

        oGui.setEndOfDirectory()

        return

    def delDownload(self):

        oInputParameterHandler = cInputParameterHandler()
        url = oInputParameterHandler.getValue('sUrl')
        meta = {}
        meta['url'] = url
        meta['path'] = ''

        try:
            cDb().del_download(meta)
            self.DIALOG.VSinfo(self.ADDON.VSlang(30071))
            VSupdate()
        except:
            pass

        return

    def AddDownload(self, meta):

        sTitle = meta['title']
        sUrl = meta['url']

        #titre fichier
        sTitle = self.__createTitle(sUrl, sTitle)
        sTitle = self.__createDownloadFilename(sTitle)
        sTitle =  cGui().showKeyBoard(sTitle)

        if (sTitle != False and len(sTitle) > 0):

            #chemin de sauvegarde
            sPath2 = xbmc.translatePath(self.ADDON.getSetting('download_folder'))

            dialog = xbmcgui.Dialog()
            sPath = dialog.browse(3, 'Downloadfolder', 'files', '', False, False, sPath2)

            if (sPath != ''):
                self.ADDON.setSetting('download_folder', sPath)
                sDownloadPath = xbmc.translatePath(sPath + '%s' % (sTitle))

                if xbmcvfs.exists(sDownloadPath):
                    self.DIALOG.VSinfo(self.ADDON.VSlang(30082), sTitle)
                    return self.AddDownload(meta)
                else:
                    xbmcvfs.File(sDownloadPath, 'w')

                try:
                    VSlog(self.ADDON.VSlang(30083), str(sUrl))
                    meta['title'] = sTitle
                    meta['path'] = sDownloadPath

                    cDb().insert_download(meta)

                    return True

                except:
                    #print_exc()
                    self.DIALOG.VSinfo(self.ADDON.VSlang(30084), sTitle)
                    VSlog('Unable to download')

        return False

    def AddtoDownloadList(self):

        oInputParameterHandler = cInputParameterHandler()
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')
        # sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        #bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')

        #if (bGetRedirectUrl == 'True'):
        #    sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        VSlog('Download', sMediaUrl)

        meta = {}
        meta['url'] = sMediaUrl
        meta['cat'] = oInputParameterHandler.getValue('sCat')
        meta['title'] = sFileName
        meta['icon'] = xbmc.getInfoLabel('ListItem.Art(thumb)')

        if (self.AddDownload(meta)):
            # telechargement direct ou pas?
            if not self.isDownloading():
                row = cDb().get_download(meta)
                if row:
                    self.StartDownloadOneFile(row[0])

        return

    def AddtoDownloadListandview(self):

        oInputParameterHandler = cInputParameterHandler()
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')
        # sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')

        VSlog('Download', sMediaUrl)

        meta = {}
        meta['url'] = sMediaUrl
        meta['cat'] = oInputParameterHandler.getValue('sCat')
        meta['title'] = sFileName
        meta['icon'] = xbmc.getInfoLabel('ListItem.Art(thumb)')

        if (self.AddDownload(meta)):
            # Si pas de telechargement en cours on lance le notre
            if not self.isDownloading():
                row = cDb().get_download(meta)
                if row:

                    title = row[0][1]
                    url = UnquotePlus(row[0][2])
                    path = row[0][3]
                    # thumbnail = UnquotePlus(row[0][4])
                    # status = row[0][8]
                    if (self.download(url, title, path, True) == True):  # Download in fastmode

                        # ok on attend un peu, et on lance le stream
                        tempo = 100
                        progress_ = progress().VScreate('Bufferisation')

                        while (tempo > 0):
                            # if canceled do nothing
                            if progress_.iscanceled():
                                break
                            progress_.VSupdate(progress_, 100)
                            tempo = tempo - 1
                            xbmc.sleep(500)

                        progress_.VSclose(progress_)

                        oGuiElement = cGuiElement()
                        oGuiElement.setSiteName(SITE_IDENTIFIER)
                        oGuiElement.setMediaUrl(path)
                        oGuiElement.setTitle(title)
                        # oGuiElement.getInfoLabel()

                        oPlayer = cPlayer()

                        if not (sys.argv[1] == '-1'):
                            oPlayer.run(oGuiElement, title, path)
                        else:
                            oPlayer.clearPlayList()
                            oPlayer.addItemToPlaylist(oGuiElement)
                            oPlayer.startPlayer()

                    else:
                        self.DIALOG.VSinfo('Erreur', self.ADDON.VSlang(30085))
        return
