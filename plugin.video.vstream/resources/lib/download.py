# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

try:
    import urllib2

except ImportError:
    import urllib.request as urllib2

import re
import threading
import xbmcplugin
import xbmcvfs
import xbmcgui
import xbmc

from resources.lib.comaddon import addon, dialog, progress, VSlog, VSupdate, VSPath, isMatrix
from resources.lib.db import cDb
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.player import cPlayer
from resources.lib.util import cUtil, UnquotePlus

SITE_IDENTIFIER = 'cDownload'

# http://kodi.wiki/view/Add-on:Common_plugin_cache
# https://pymotw.com/2/threading/
# https://code.google.com/p/navi-x/source/browse/trunk/Navi-X/src/CDownLoader.py?r=155

# status = 0 => pas telechargé
# status = 1 => en cours de DL (ou bloque si bug)
# status = 2 => fini de DL

# GetProperty('arret') = '0' => Telechargement en cours
# GetProperty('arret') = '1' => Arret demandé
# GetProperty('arret') = '' =>  Jamais eu de telechargement


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
                VSlog('Téléchargement en mode Turbo')
                self.__bFastMode = True

        threading.Thread.__init__(self)

        self.processIsCanceled = False
        self.oUrlHandler = None
        self.file = None
        self.__oDialog = None

    def createProcessDialog(self):
        self.__oDialog = xbmcgui.DialogProgressBG()
        self.__oDialog.create('Download')
        return self.__oDialog

    def _StartDownload(self):
        diag = self.createProcessDialog()
        xbmcgui.Window(10101).setProperty('arret', '0')
        headers = self.oUrlHandler.info()

        iTotalSize = -1
        if 'content-length' in headers:
            iTotalSize = int(headers['Content-Length'])
            
        
        chunk = 512 * 1024
        TotDown = 0

        # mise a jour pour info taille
        self.__updatedb(TotDown, iTotalSize)
        self.DIALOG.VSinfo(self.ADDON.VSlang(30086), self.ADDON.VSlang(30224), 5)

        while not (self.processIsCanceled or diag.isFinished()):
            data = self.oUrlHandler.read(chunk)
            if not data:
                VSlog('DL err')
                break

            self.file.write(data)
            TotDown = TotDown + data.__len__()
            self.__updatedb(TotDown, iTotalSize)

            self.__stateCallBackFunction(TotDown, iTotalSize)
            if xbmcgui.Window(10101).getProperty('arret') == '1':
                self.processIsCanceled = True

            # petite pause, ca ralentit le download mais evite de bouffer 100/100 ressources
            if not self.__bFastMode:
                xbmc.sleep(250)

        self.oUrlHandler.close()
        self.file.close()
        self.__oDialog.close()

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
                with cDb() as db:
                    db.update_download(meta)
                self.DIALOG.VSinfo(self.__sTitle, self.ADDON.VSlang(30003), 5)
                self.RefreshDownloadList()
            except:
                pass
        else:
            meta['status'] = 0
            try:
                with cDb() as db:
                    db.update_download(meta)
                self.DIALOG.VSinfo(self.__sTitle, self.ADDON.VSlang(30004), 5)
                self.RefreshDownloadList()
            except:
                pass
            return

        # ok tout est bon on continu ou pas?
        if xbmcgui.Window(10101).getProperty('SimpleDownloaderQueue') == '1':
            VSlog('Download suivant')
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
                with cDb() as db:
                    db.update_download(meta)
                self.RefreshDownloadList()
            except:
                pass

    def __stateCallBackFunction(self, iDownsize, iTotalSize):
        if self.__oDialog.isFinished():
            self.createProcessDialog()

        # barre de préchargement
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
            if len(self.__sUrl.split('|')) > 1:
                u = self.__sUrl.split('|')[1].split('&')
                for i in u:
                    headers[i.split('=')[0]] = i.replace(i.split('=')[0] + '=', '')

            # Rajout du user-agent si absent
            if not ('User-Agent' in headers):
                headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'

            req = urllib2.Request(url, None, headers)

            self.oUrlHandler = urllib2.urlopen(req, timeout=30)
            self.file = xbmcvfs.File(self.__fPath, 'w')
        except:
            VSlog('download error ' + self.__sUrl)
            self.DIALOG.VSinfo(self.ADDON.VSlang(30011), 'Download error', 5)
            return

        self._StartDownload()

    def __formatFileSize(self, iBytes):
        iBytes = int(iBytes)
        if iBytes == 0:
            return '0 MB'

        return "{:,.{}f} MB".format( iBytes/(1024*1024.0), 0 ).replace(',', ' ')

    def StopAll(self):
        self.processIsCanceled = True
        xbmcgui.Window(10101).setProperty('SimpleDownloaderQueue', '0')
        xbmcgui.Window(10101).setProperty('arret', '1')
        try:
            self.__oDialog.close()
        except:
            pass

        return

    def RefreshDownloadList(self):
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
        filename = filename.strip()
        return filename

    def __formatFileSize(self, iBytes):
        iBytes = int(iBytes)
        if iBytes == 0:
            return '0 MB'

        return "{:,.{}f} MB".format( iBytes/(1024*1024.0), 0 ).replace(',', ' ')
    
    def isDownloading(self):
        if not xbmc.getCondVisibility('Window.IsVisible(10151)'):
            return False
        return True

    def download(self, sDBUrl, sTitle, sDownloadPath, FastMode=False):
        if self.isDownloading():
            self.DIALOG.VSinfo(self.ADDON.VSlang(30012), 'Erreur', 5)
            return False

        self.__sTitle = sTitle

        # resolve url
        from resources.lib.gui.hoster import cHosterGui
        oHoster = cHosterGui().checkHoster(sDBUrl)
        oHoster.setUrl(sDBUrl)
        aLink = oHoster.getMediaLink()

        if aLink and aLink[0]:
            sUrl = aLink[1]
        else:
            VSlog('Lien non resolvable ou protégé')
            self.DIALOG.VSinfo(sTitle, self.ADDON.VSlang(30022), 5)
            return False

        if (not sUrl.startswith('http')) or sUrl.split('|')[0].endswith('.m3u8'):
            self.DIALOG.VSinfo(sTitle, self.ADDON.VSlang(30022), 5)
            return False

        try:
            VSlog('Download ' + str(sUrl))

            # background download task
            if FastMode:
                cDownloadProgressBar(title=self.__sTitle, url=sUrl, Dpath=sDownloadPath, FastMode=True).start()
            else:
                cDownloadProgressBar(title=self.__sTitle, url=sUrl, Dpath=sDownloadPath).start()

            VSlog('Download Ok ' + sDownloadPath)

        except:
            self.DIALOG.VSinfo(sTitle, self.ADDON.VSlang(30024), 5)
            VSlog('Unable to download')
            return False

        return True

    def __createTitle(self, sUrl, sTitle):

        extension = sTitle.rsplit('.')
        # Si deja extension
        if (len(extension) > 1):
            extension = extension[-1]
            m = re.search('(flv|avi|mp4|mpg|mpeg|mkv)', extension)
            if m:
                sTitle = sTitle[:-len(extension)]
            else:
                extension = None
        else:
            extension = None

        sTitle = cUtil().CleanName(sTitle)
        # sTitle = cUtil().FormatSerie(sTitle)

        if type(sTitle) is bytes:
            sTitle = sTitle.decode('utf-8')

        if extension:
            return sTitle + '.' +extension

        # recherche d'une extension
        sUrl = sUrl.lower()

        m = re.search('(flv|avi|mp4|mpg|mpeg|mkv)', sUrl)
        if m:
            sTitle = sTitle + '.' + m.group(0)
        else:
            sTitle = sTitle + '.mp4'  # Si quedale on en prend une au pif

        return sTitle

    def getDownload(self):

        sPluginHandle = cPluginHandler().getPluginHandle()
        sPluginPath = cPluginHandler().getPluginPath()
        sItemUrl = '%s?site=%s&function=%s&title=%s' % (sPluginPath, SITE_IDENTIFIER, 'StartDownloadList', 'title')
        item = xbmcgui.ListItem('Démarrer la liste')
        item.setArt({'icon':'special://home/addons/plugin.video.vstream/resources/art/download.png'})
        xbmcplugin.addDirectoryItem(sPluginHandle, sItemUrl, item, isFolder=False)

        oGui = cGui()
        oOutputParameterHandler = cOutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'StopDownloadList', self.ADDON.VSlang(30025), 'none.png', oOutputParameterHandler)
        oGui.addDir(SITE_IDENTIFIER, 'getDownloadList', self.ADDON.VSlang(30039), 'listes.png', oOutputParameterHandler)
        oGui.addDir(SITE_IDENTIFIER, 'CleanDownloadList', self.ADDON.VSlang(30040), 'trash.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()

    def CleanDownloadList(self):
        try:
            with cDb() as db:
                db.clean_download()
            self.DIALOG.VSinfo(self.ADDON.VSlang(30071), self.ADDON.VSlang(30224), 5)
        except:
            pass

        return

    def dummy(self):
        return

    def StartDownloadOneFile(self, meta=None):
        if meta is None:
            meta = []
        if not meta:
            meta = self.GetOnefile()

        xbmcgui.Window(10101).setProperty('SimpleDownloaderQueue', '0')
        return self.StartDownload(meta)

    def ResetDownload(self):
        oInputParameterHandler = cInputParameterHandler()
        url = oInputParameterHandler.getValue('sUrl')
        meta = {}
        meta['url'] = url

        try:
            with cDb() as db:
                db.reset_download(meta)
            self.DIALOG.VSinfo(self.ADDON.VSlang(30071), self.ADDON.VSlang(30224), 5)
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

        oPlayer = cPlayer()
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
                with cDb() as db:
                    db.del_download(meta)

                xbmcvfs.delete(path)
                self.DIALOG.VSinfo(self.ADDON.VSlang(30072), self.ADDON.VSlang(30224), 5)
                VSupdate()
            except:
                self.DIALOG.VSinfo(self.ADDON.VSlang(30073), self.ADDON.VSlang(30224), 5)

    def GetNextFile(self):
        with cDb() as db:
            row = db.get_download()

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

        with cDb() as db:
            row = db.get_download(meta)

        if not row:
            return None

        return row[0]

    def StartDownload(self, data):
        if not data:
            return False

        title = data[1]
        url = UnquotePlus(data[2])
        path = data[3]

        return self.download(url, title, path)

    def StartDownloadList(self):
        self.DIALOG.VSinfo(self.ADDON.VSlang(30075), self.ADDON.VSlang(30224), 5)

        xbmcgui.Window(10101).setProperty('SimpleDownloaderQueue', '1')
        data = self.GetNextFile()
        return self.StartDownload(data)

    def StopDownloadList(self):
        # thread actif
        if xbmcgui.Window(10101).getProperty('arret') == '0':
            xbmcgui.Window(10101).setProperty('arret', '1')
        # si bug
        else:
            cDownloadProgressBar().StopAll()

        with cDb() as db:
            db.cancel_download()

        VSupdate()

        return

    def getDownloadList(self):
        oGui = cGui()
        with cDb() as db:
            row = db.get_download()

        oOutputParameterHandler = cOutputParameterHandler()
        for data in row:

            title = data[1]
            url = UnquotePlus(data[2])
            path = data[3]
            # cat = data[4]
            thumbnail = UnquotePlus(data[5])

            # The url is unicode format ? Not managed yet
            try:
                thumbnail = str(thumbnail)
            except:
                thumbnail = ''

            size = data[6]
            totalsize = data[7]
            status = data[8]

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
                sStatus = '[COLOR=green][Fini] [/COLOR]'

            if size:
                if isMatrix():
                    try:
                        title = title.decode()
                    except:
                        pass

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
            with cDb() as db:
                db.del_download(meta)
            self.DIALOG.VSinfo(self.ADDON.VSlang(30071), self.ADDON.VSlang(30224), 5)
            VSupdate()
        except:
            pass

        return

    def AddDownload(self, meta):
        sTitle = meta['title']
        sUrl = meta['url']

        # resolve url ?
        from resources.lib.gui.hoster import cHosterGui
        oHoster = cHosterGui().checkHoster(sUrl)
        oHoster.setUrl(sUrl)
        aLink = oHoster.getMediaLink()
        if not aLink or not aLink[0]:
            VSlog('Lien non resolvable ou protégé')
            self.DIALOG.VSinfo(sTitle, self.ADDON.VSlang(30024), 5)
            return False

        # titre fichier
        sTitle = self.__createTitle(sUrl, sTitle)
        sTitle = self.__createDownloadFilename(sTitle)
        sTitle = cGui().showKeyBoard(sTitle)

        if sTitle:

            # chemin de sauvegarde
            sPath = VSPath(self.ADDON.getSetting('download_folder'))

            if sPath == '':
                dialog = xbmcgui.Dialog()
                sPath = dialog.browse(3, 'Dossier de sauvegarde', 'files', '', False, False)
                self.ADDON.setSetting('download_folder', sPath)
            if sPath != '':
                sDownloadPath = VSPath(sPath + '%s' % sTitle)

                if xbmcvfs.exists(sDownloadPath):
                    self.DIALOG.VSinfo(sTitle, self.ADDON.VSlang(30082), 5)
                    return self.AddDownload(meta)
                else:
                    xbmcvfs.File(sDownloadPath, 'w')

                try:
                    VSlog(self.ADDON.VSlang(30083) + ' : ' + str(sDownloadPath))
                    meta['title'] = sTitle
                    meta['path'] = sDownloadPath

                    with cDb() as db:
                        db.insert_download(meta)
                    return True

                except:
                    self.DIALOG.VSinfo(sTitle, self.ADDON.VSlang(30084), 5)
                    VSlog('Unable to download')

        return False

    def AddtoDownloadList(self):
        oInputParameterHandler = cInputParameterHandler()
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        meta = {}
        meta['url'] = sMediaUrl
        meta['cat'] = oInputParameterHandler.getValue('sCat')
        meta['title'] = sFileName
        meta['icon'] = xbmc.getInfoLabel('ListItem.Art(thumb)')

        if (self.AddDownload(meta)):
            # telechargement direct ou pas?
            if not self.isDownloading():
                with cDb() as db:
                    row = db.get_download(meta)
                if row:
                    self.StartDownloadOneFile(row[0])

            else:
                # notifier que la demande est prise en compte
                self.DIALOG.VSinfo(self.ADDON.VSlang(30228), self.ADDON.VSlang(30083), 5)
        return

    def AddtoDownloadListandview(self):
        oInputParameterHandler = cInputParameterHandler()
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        meta = {}
        meta['url'] = sMediaUrl
        meta['cat'] = oInputParameterHandler.getValue('sCat')
        meta['title'] = sFileName
        meta['icon'] = xbmc.getInfoLabel('ListItem.Art(thumb)')

        if (self.AddDownload(meta)):
            # Si pas de telechargement en cours on lance le notre
            if not self.isDownloading():
                with cDb() as db:
                    row = db.get_download(meta)

                if row:

                    title = row[0][1]
                    url = UnquotePlus(row[0][2])
                    path = row[0][3]
                    if self.download(url, title, path, True):  # Download in fastmode

                        # ok on attend un peu, et on lance le stream
                        tempo = 100
                        progress_ = progress().VScreate('Préchargement ...')

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

                        oPlayer = cPlayer()
                        oPlayer.clearPlayList()
                        oPlayer.addItemToPlaylist(oGuiElement)
                        oPlayer.startPlayer()

                    else:
                        self.DIALOG.VSinfo(self.ADDON.VSlang(30085), 'Erreur', 5)
            else:
                # notifier que la demande est prise en compte
                self.DIALOG.VSinfo(self.ADDON.VSlang(30228), self.ADDON.VSlang(30083), 5)
                
        return
