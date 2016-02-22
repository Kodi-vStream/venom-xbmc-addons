#-*- coding: utf-8 -*-
from resources.lib.config import cConfig
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
#from resources.lib.handler.hosterHandler import cHosterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.player import cPlayer
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.db import cDb
from resources.lib.util import cUtil


import urllib2,urllib
import xbmcplugin, xbmc
import xbmcgui
import xbmcvfs
import re
import threading

try:
    import StorageServer
    Memorise = StorageServer.StorageServer("VstreamDownloader")
except:
    print 'Le download ne marchera pas correctement'


SITE_IDENTIFIER = 'cDownload'

#http://kodi.wiki/view/Add-on:Common_plugin_cache
#https://pymotw.com/2/threading/
#https://code.google.com/p/navi-x/source/browse/trunk/Navi-X/src/CDownLoader.py?r=155


#status = 0 => pas telechargé
#status = 1 => en cours de DL (ou bloque si bug)
#status = 2 => fini de DL

#GetProperty('arret') = '0' => Telechargement en cours
#GetProperty('arret') = '1' => Arret demandé
#GetProperty('arret') = '' =>  Jamais eu de telechargement


#Create queue objects
class _Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(_Singleton('SingletonMeta', (object,), {})): pass
 #to use it
 #class cDownloadProgressBar(Singleton):


class cDownloadProgressBar(threading.Thread):
    def __init__(self, *args, **kwargs):

        self.__sTitle = ''
        self.__sUrl = ''
        self.__fPath = ''
    
        if (kwargs):
            self.__sTitle = kwargs['title']
            self.__sUrl = kwargs['url']
            self.__fPath = kwargs['Dpath']
        
        threading.Thread.__init__(self)
        
        self.processIsCanceled = False
        self.oUrlHandler = None
        self.file = None
        self.__oDialog = None
   
        #queue = self.Memorise.get("SimpleDownloaderQueue")
        #if self.Memorise.lock("SimpleDownloaderQueueLock"):
        #self.Memorise.set("SimpleDownloaderQueue", repr(items))       
        
    def createProcessDialog(self):
        self.__oDialog = xbmcgui.DialogProgressBG()
        self.__oDialog.create('Download')            
        #xbmc.sleep(1000)
        return self.__oDialog        
        
    def _StartDownload(self): 

        #print 'Thread actuel'
        #print threading.current_thread().getName()
        
        diag = self.createProcessDialog()
        #diag.isFinished()
        
        xbmcgui.Window(10101).setProperty('arret', '0')
        #self.Memorise.set("VstreamDownloaderWorking", "1")

        headers = self.oUrlHandler.info()
        
        #print headers
        
        iTotalSize = -1
        if "content-length" in headers:
            iTotalSize = int(headers["Content-Length"])
        
        chunk = 16 * 1024
        
        TotDown = 0
        
        #mise a jour pour info taille
        self.__updatedb(TotDown,iTotalSize)
        cConfig().showInfo('vStream', 'Téléchargement Démarré')
        
        while not (self.processIsCanceled or diag.isFinished()):
            
            data = self.oUrlHandler.read(chunk)
            if not data: break
            self.file.write(data)
            TotDown = TotDown + data.__len__()
            self.__updatedb(TotDown,iTotalSize)
            
            self.__stateCallBackFunction(TotDown, iTotalSize)
            #if self.Memorise.get("VstreamDownloaderWorking") == "0":
            #    self.processIsCanceled = True
            if xbmcgui.Window(10101).getProperty('arret') == '1':
                self.processIsCanceled = True    
                                
            #petite pause, ca ralentit le download mais evite de bouffer 100/100 ressources
            xbmc.sleep(300)
        
        self.oUrlHandler.close()
        self.file.close()
        self.__oDialog.close()
        
        #On autorise le prochain DL
        Memorise.unlock("VstreamDownloaderLock")
        
        #if download finish
        meta = {}      
        meta['path'] = self.__fPath
        meta['size'] = TotDown
        meta['totalsize'] = iTotalSize
        
        if (TotDown == iTotalSize) and (iTotalSize > 10000):
            meta['status'] = 2           
            try:
                cDb().update_download(meta)
                cConfig().showInfo('Téléchargements Termine', self.__sTitle)
                print 'Téléchargements Termine : %s' % self.__sTitle
                self.RefreshDownloadList()
            except:
                pass
        else:
            meta['status'] = 0            
            try:
                cDb().update_download(meta)
                cConfig().showInfo('Téléchargements Arrete', self.__sTitle)
                print 'Téléchargements Arrete : %s' % self.__sTitle
                self.RefreshDownloadList()
            except:
                pass
            return
            
        #ok tout est bon on contiinu ou pas ?
        if Memorise.get('SimpleDownloaderQueue') == '1':
            print 'Download suivant'
            tmp = cDownload()
            data = tmp.GetNextFile()
            tmp.StartDownload(data)


    def __updatedb(self, TotDown, iTotalSize):
        #percent 3 chiffre
        percent = '{0:.2f}'.format(min(100 * float(TotDown) / float(iTotalSize), 100))
        if percent in ['0.00','10.00','20.00','30.00','40.00','50.00','60.00','70.00','80.00','90.00']:
            meta = {}      
            meta['path'] = self.__fPath
            meta['size'] = TotDown
            meta['totalsize'] = iTotalSize
            meta['status'] = 1
            
            try:
                cDb().update_download(meta)
                #cConfig().update()
                self.RefreshDownloadList()
            except:
                pass
        
        
    def __stateCallBackFunction(self, iDownsize, iTotalSize):
        
        if self.__oDialog.isFinished():
            self.createProcessDialog()

        iPercent = int(float(iDownsize * 100) / iTotalSize)
        self.__oDialog.update(iPercent, self.__sTitle, self.__formatFileSize(float(iDownsize))+'/'+self.__formatFileSize(iTotalSize))
        
        if (self.__oDialog.isFinished()) and not (self.__processIsCanceled):
            self.__processIsCanceled = True
            self.__oDialog.close()

    def run(self):
        
        try:
            #1 seul header a l'air necessaire pour le moment
            headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' }
            url = self.__sUrl.split('|')[0]
            req = urllib2.Request(url, None, headers)
            self.oUrlHandler = urllib2.urlopen(req,timeout=30)
            #self.__instance = repr(self)
            self.file = xbmcvfs.File(self.__fPath, 'w')
        except:
            print 'download error'
            print self.__sUrl
            cConfig().showInfo('Erreur initialisation', 'Download error')
            return
        
        if not Memorise.lock("VstreamDownloaderLock"):
            cConfig().showInfo('Telechargements deja demarrés', 'Download error')
            #self.oUrlHandler.close()
            return
        
        self._StartDownload()
        
    def __formatFileSize(self, iBytes):
        iBytes = int(iBytes)
        if (iBytes == 0):
            return '%.*f %s' % (2, 0, 'MB')
        
        return '%.*f %s' % (2, iBytes/(1024*1024.0) , 'MB')
        
    def StopAll(self):
        
        self.processIsCanceled = True
        Memorise.unlock("VstreamDownloaderLock")
        Memorise.set('SimpleDownloaderQueue', '0')
        #self.Memorise.set("VstreamDownloaderWorking", "0")
        xbmcgui.Window(10101).setProperty('arret', '1')
        try:
            self.__oDialog.close()
        except:
            pass
                
        return
        
    def RefreshDownloadList(self):
        #print xbmc.getInfoLabel('Container.FolderPath')
        if 'function=getDownload' in xbmc.getInfoLabel('Container.FolderPath'):
            cConfig().update()  
     
        
class cDownload:  
    def __init__(self):
        pass

    def __createDownloadFilename(self, sTitle):
        sTitle = re.sub(' +',' ',sTitle) #Vire double espace
        valid_chars = "-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        filename = ''.join(c for c in sTitle if c in valid_chars)
        filename = filename.replace(' .','.')
        if filename.startswith(' '):
            filename = filename[1:]
        #filename = filename.replace(' ','_') #pas besoin de ca, enfin pr moi en tout cas
        return filename
        
    def __formatFileSize(self, iBytes):
        iBytes = int(iBytes)
        if (iBytes == 0):
            return '%.*f %s' % (2, 0, 'MB')
        
        return '%.*f %s' % (2, iBytes/(1024*1024.0) , 'MB')
        
    def isDownloading(self):

        if not Memorise.get('VstreamDownloaderLock'):
            return False
        return True
   
    def download(self, sDBUrl, sTitle,sDownloadPath):
        
        if self.isDownloading():
            cConfig().showInfo('Telechargements deja demarrés', 'Erreur')
            return

        self.__sTitle = sTitle
        
        #resolve url
        from resources.lib.gui.hoster import cHosterGui
        oHoster = cHosterGui().checkHoster(sDBUrl)
        oHoster.setUrl(sDBUrl)
        aLink = oHoster.getMediaLink()

        #aLink = (True,'https://github.com/LordVenom/venom-xbmc-addons-beta/blob/master/plugin.video.vstream/Thumbs.db?raw=true')

        if (aLink[0] == True):
            sUrl = aLink[1]
        else:
            cConfig().showInfo('Lien non resolvable', sTitle)
            return
            
        if not sUrl.startswith('http') or sUrl.endswith('.m3u8'):
            cConfig().showInfo('Format non supporte', sTitle)
            print sUrl
            return           
        
        try:
            cConfig().log("Telechargement " + str(sUrl))
            
            #background download task
            cDownloadProgressBar(title = self.__sTitle , url = sUrl , Dpath = sDownloadPath ).start()

            cConfig().log("Telechargement ok")

        except:
            #print_exc()
            cConfig().showInfo('Telechargement impossible', sTitle)
            cConfig().log("Telechargement impossible")
            pass
            

    def __createTitle(self, sUrl, sTitle):
        
        #sTitle = re.sub('[\(\[].+?[\)\]]',' ', sTitle)
        sTitle = cUtil().FormatSerie(sTitle)
        sTitle = cUtil().CleanName(sTitle)
               
        aTitle = sTitle.rsplit('.')
        #Si deja extension
        if (len(aTitle) > 1):
            return sTitle
        
        #recherche d'une extension
        sUrl = sUrl.lower()
        m = re.search('(flv|avi|mp4|mpg|mpeg)', sUrl)
        if m:
            sTitle = sTitle + '.' + m.group(0)
        else:
            sTitle = sTitle + '.flv' #Si quedale on en prend une au pif
            
            
        return sTitle

        
    def getDownload(self):

        oGui = cGui()
        sPluginHandle = cPluginHandler().getPluginHandle()
        sPluginPath = cPluginHandler().getPluginPath()
        sItemUrl = '%s?site=%s&function=%s&title=%s' % (sPluginPath, SITE_IDENTIFIER, 'StartDownloadList', 'tittle')
        meta = {'title': 'Demarrer la liste'}
        item = xbmcgui.ListItem('Demarrer la liste', iconImage=cConfig().getRootArt()+'download.png')
        item.setProperty("Fanart_Image", cConfig().getSetting('images_downloads'))
        
        #item.setInfo(type="Video", infoLabels = meta)
        
        #item.setProperty("Video", "false")
        #item.setProperty("IsPlayable", "false")

        xbmcplugin.addDirectoryItem(sPluginHandle,sItemUrl,item,isFolder=False)
        
        oOutputParameterHandler = cOutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'StopDownloadList', 'Arreter les Téléchargements', 'download.png', oOutputParameterHandler)

        oOutputParameterHandler = cOutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'getDownloadList', 'Liste de Téléchargement', 'download.png', oOutputParameterHandler)
        
        oOutputParameterHandler = cOutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'CleanDownloadList', 'Nettoyer la liste (Fichiers finis)', 'download.png', oOutputParameterHandler)
          
        oGui.setEndOfDirectory()   
    
    def CleanDownloadList(self):
        
        try:
            cDb().clean_download()
            cConfig().showInfo('vStream', 'Liste mise a jour')
            #cConfig().update()
        except:
            pass

        return
    
    def dummy(self):
        return
    
    def StartDownloadOneFile(self,meta = []):
        if not meta:
            meta = self.GetOnefile()

        self.StartDownload(meta) 
        
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
        oPlayer.run(oGuiElement, sTitle, path)
        #oPlayer.startPlayer()
        
    def DelFile(self):
        oInputParameterHandler = cInputParameterHandler()
        path = oInputParameterHandler.getValue('sPath')
        
        oDialog = cConfig().createDialogYesNo('Voulez vous vraiment supprimer ce fichier ? Operation non reversible.')
        if (oDialog == 1):
            meta = {}
            meta['url'] = ''
            meta['path'] = path
            
            try:
                cDb().del_download(meta)
                xbmcvfs.delete(path)
                cConfig().showInfo('vStream', 'Fichier supprimé')
                cConfig().update()
            except:
                cConfig().showInfo('vStream', 'Erreur, fichier non supprimable')
        
    def GetNextFile(self):
        row = cDb().get_Download()

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
    
        row = cDb().get_Download(meta)
        
        if not (row):
            return None
        
        return row[0]
        
        
    def StartDownload(self,data):     
        if not (data):
            return
        
        title = data[1]
        url = urllib.unquote_plus(data[2])
        path = data[3]
        thumbnail = data[4]
        status = data[8]
                            
        self.download(url,title,path)
                
    def StartDownloadList(self):
        cConfig().showInfo('Information', 'Demarrage de la liste complete')
        Memorise.set('SimpleDownloaderQueue', '1')
        data = self.GetNextFile()
        self.StartDownload(data)

    def StopDownloadList(self):
        
        #oInputParameterHandler = cInputParameterHandler()
        #path = oInputParameterHandler.getValue('sPath')
        #status = oInputParameterHandler.getValue('sStatus')
        

        #WINDOW_PROGRESS = xbmcgui.Window( 10101 )
        #WINDOW_PROGRESS.close()        
        #xbmcgui.Window(10101).setProperty('arret', '1')
        #xbmc.executebuiltin("Dialog.Close(%s, true)" % 10101)
        #xbmc.getCondVisibility('Window.IsActive(10101)'))
        
        #thread actif
        if xbmcgui.Window(10101).getProperty('arret') == '0':
            xbmcgui.Window(10101).setProperty('arret', '1')
        #si bug
        else:
            cDownloadProgressBar().StopAll()
        
        #On remet tout les status a 0 ou 2
        cDb().Cancel_download()
        
        cConfig().update()
  
        return
   
    def getDownloadList(self):
    
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        row = cDb().get_Download()
        
        for data in row:

            title = data[1]
            url = urllib.unquote_plus(data[2])
            cat = data[4]
            thumbnail = data[5]
            size = data[6]
            totalsize = data[7]
            status = data[8]
            path = data[3]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sUrl', url)
            oOutputParameterHandler.addParameter('sMovieTitle', title)
            oOutputParameterHandler.addParameter('sThumbnail', thumbnail)
            oOutputParameterHandler.addParameter('sPath', path)
            oOutputParameterHandler.addParameter('sStatus', status)
            
            if status == '0':
                sStatus = ''
            elif status == '1':
                sStatus='[COLOR=red][En cours] [/COLOR]'
            elif status == '2':
                sStatus='[COLOR=green][Fini] [/COLOR]'
                               
            if size:
                sTitle = sStatus + title + ' (' + self.__formatFileSize(size)+'/'+self.__formatFileSize(totalsize)+')'
            else:
                sTitle = sStatus + title
                
            oGuiElement = cGuiElement()
            
            if not thumbnail or thumbnail == 'False':
                thumbnail = "mark.png"

            oGuiElement.setSiteName(SITE_IDENTIFIER)
            if status == '2':
                oGuiElement.setFunction('ReadDownload')
            else:
                #oGuiElement.setFunction('StartDownloadOneFile') #marche pas a cause de fenetre xbmc
                oGuiElement.setFunction('ReadDownload')
            oGuiElement.setTitle(sTitle)
            oGuiElement.setIcon('download.png')
            oGuiElement.setFanart(cConfig().getRootArt()+'download_fanart.jpg')
            oGuiElement.setMeta(0)
            oGuiElement.setThumbnail(thumbnail)
            
            oGui.createContexMenuDownload(oGuiElement, oOutputParameterHandler,status)
            
            oGui.addFolder(oGuiElement, oOutputParameterHandler, False)


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
            cConfig().showInfo('vStream', 'Liste mise a jour')
            cConfig().update()
        except:
            pass

        return
        
    def AddDownload(self,meta):
        
        sTitle = meta['title']
        sUrl = meta['url']
        
        oGui = cConfig()
        
        #titre fichier
        sTitle = self.__createTitle(sUrl, sTitle)
        sTitle = self.__createDownloadFilename(sTitle)
        sTitle = oGui.showKeyBoard(sTitle)
        
        if (sTitle != False and len(sTitle) > 0):

            #chemin de sauvegarde
            sPath2 = xbmc.translatePath(cConfig().getSetting('download_folder'))

            dialog = xbmcgui.Dialog()
            sPath = dialog.browse(3, 'Downloadfolder', 'files', '', False, False , sPath2)
            
            if (sPath != ''):
                cConfig().setSetting('download_folder',sPath)
                
                sDownloadPath = xbmc.translatePath(sPath +  '%s' % (sTitle, ))
                if xbmcvfs.exists(sDownloadPath):
                    cConfig().showInfo('Téléchargement en double', sTitle)
                    return self.AddDownload(meta)
                else:
                    xbmcvfs.File(sDownloadPath, 'w')

                try:
                    cConfig().log("Rajout en liste de telechargement " + str(sUrl))
                    meta['title'] = sTitle
                    meta['path'] = sDownloadPath
                    cDb().insert_download(meta)
                    
                    #telechargement direct ou pas ?
                    if not self.isDownloading(): 
                        row = cDb().get_Download(meta)
                        if row:
                            self.StartDownloadOneFile(row[0])
                except:
                    #print_exc()
                    cConfig().showInfo('Telechargement impossible', sTitle)
                    cConfig().log("Telechargement impossible")
                    pass
  
  
    def AddtoDownloadList(self):

        oInputParameterHandler = cInputParameterHandler()
        
        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        #bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        #if (bGetRedirectUrl == 'True'):
        #    sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        cConfig().log("Telechargement " + sMediaUrl)

        meta = {}
        meta['url'] = sMediaUrl
        meta['cat'] = oInputParameterHandler.getValue('sCat')
        meta['title'] = sFileName
        meta['icon'] = xbmc.getInfoLabel('ListItem.Art(thumb)')
    
        self.AddDownload(meta)
            
        return   
