#-*- coding: utf-8 -*-
#Venom.
from config import cConfig
   
import urllib, urllib2
import xbmc, xbmcgui, xbmcaddon
import xbmcvfs
import sys, datetime, time, os
import hashlib, md5
try:    import json
except: import simplejson as json

sLibrary = xbmc.translatePath(cConfig().getAddonPath())
sys.path.append (sLibrary) 

from resources.lib.handler.requestHandler import cRequestHandler

SITE_IDENTIFIER = 'about'
SITE_NAME = 'About'


class cAbout:

    def __init__(self):
        self.main(sys.argv[1])
        #self.__sFunctionName = ''

    def get_remote_md5_sum(self, url, max_file_size=100*1024*1024):
        try:
            remote = urllib2.urlopen(url)
            hash = hashlib.md5()
         
            total_read = 0
            while True:
                data = remote.read(4096)
                total_read += 4096
         
                if not data or total_read > max_file_size:
                    break
         
                hash.update(data)
         
            return hash.hexdigest()
        except:            
            cConfig().error("%s,%s" % (cConfig().getlanguage(30205), url))
            return False
            
    def get_root_md5_sum(self, root, max_file_size=100*1024*1024):
        try:
            remote = open(root,'r')
            hash = hashlib.md5()
         
            total_read = 0
            while True:
                data = remote.read(4096)
                total_read += 4096
         
                if not data or total_read > max_file_size:
                    break
         
                hash.update(data)
         
            return hash.hexdigest()
        except:            
            cConfig().error("%s,%s" % (cConfig().getlanguage(30205), url))
            return False
     
    def __getFileNamesFromFolder(self, sFolder):
        aNameList = []
        items = os.listdir(sFolder)
        for sItemName in items:
            sFilePath = os.path.join(sFolder, sItemName)
            # xbox hack
            sFilePath = sFilePath.replace('\\', '/')
            
            sUrlPath = "https://raw.githubusercontent.com/LordVenom/venom-xbmc-addons/master/plugin.video.vstream/resources/sites/"+sItemName
            
            if (os.path.isdir(sFilePath) == False):
                if (str(sFilePath.lower()).endswith('py')):   
                    aNameList.append([sFilePath,sUrlPath,sItemName])
        return aNameList
        
    def getPlugins(self):

        sFolder = cConfig().getAddonPath()
        sFolder = os.path.join(sFolder, 'resources/sites')

        # xbox hack        
        sFolder = sFolder.replace('\\', '/')
        
        aFileNames = self.__getFileNamesFromFolder(sFolder)
        return aFileNames
      

    def main(self, env):
        

        if (env == 'changelog'):
            try:
                oRequest =  urllib2.Request(sUrl)
                oResponse = urllib2.urlopen(oRequest)
                sContent = oResponse.read()
                self.TextBoxes('vStream Changelog', sContent)
            except:            
                cConfig().error("%s,%s" % (cConfig().getlanguage(30205), sUrl))
            return

        if (env == 'update'):            
            self.__checkupdate('true')
            return
            #return  xbmc.executebuiltin("SendClick(10)")

        else :
            #service
            service_time = cConfig().getSetting('service_time')
            if (service_time != ''):
                #delay mise a jour            
                time_sleep = datetime.timedelta(hours=48)
                time_now = datetime.datetime.now()
                time_service = self.__strptime(service_time, "%Y-%m-%d %H:%M:%S.%f")
                #pour test
                #time_service = time_service - datetime.timedelta(hours=50)
                if (time_now - time_service > time_sleep):
                    self.__checkversion()
                    self.__checkupdate('false')
                    #Function update auto
            else:
                cConfig().setSetting('service_time', str(datetime.datetime.now()))
                
        return
     
    #bug python
    def __strptime(self, date, format):
        try:
            date = datetime.datetime.strptime(date, format)
        except TypeError:
            date = datetime.datetime(*(time.strptime(date, format)[0:6]))
        return date
     
    def __checkversion(self):
            service_version = cConfig().getSetting('service_version')
            if (service_version != ''):          
                version = cConfig().getAddonVersion()
                if (version > service_version):
                    try:
                        sUrl = 'https://raw.githubusercontent.com/LordVenom/venom-xbmc-addons/master/plugin.video.vstream/changelog.txt'
                        oRequest =  urllib2.Request(sUrl)
                        oResponse = urllib2.urlopen(oRequest)
                        sContent = oResponse.read()
                        self.TextBoxes('Changelog', sContent)
                        cConfig().setSetting('service_version', str(cConfig().getAddonVersion()))
                        return
                    except:            
                        cConfig().error("%s,%s" % (cConfig().getlanguage(30205), sUrl))
                        return
            else:
                cConfig().setSetting('service_version', str(cConfig().getAddonVersion()))
                return
                
    def __checkupdate(self, download):
            service_time = cConfig().getSetting('service_time')
            service_md5 = cConfig().getSetting('service_md5')         
            try:
                #sUrl = 'https://api.github.com/repos/LordVenom/venom-xbmc-addons/commits/master'
                sUrl = 'https://raw.githubusercontent.com/LordVenom/venom-xbmc-addons/master/updates.xml.md5'
                oRequestHandler = cRequestHandler(sUrl)
                sHtmlContent = oRequestHandler.request();
                if not service_md5:
                    cConfig().setSetting('service_md5', sHtmlContent)
                    service_md5 = sHtmlContent
                
                if (service_md5 != sHtmlContent):
                    if (download == 'true'):
                        self.__checkdownload()
                    cConfig().setSetting('home_update', str('true'))
                else:
                    if (download == 'true'):
                        cConfig().showInfo('vStream', 'Fichier a jour')
                        
                    cConfig().setSetting('home_update', str('false'))
            except:
                return
            return
    
    def __checkdownload(self):
            aPlugins = self.getPlugins()
            total = len(aPlugins)
            dialog = cConfig().createDialog('Update')
            sContent = ""
            sdown = 0

            for aPlugin in aPlugins:
                cConfig().updateDialog(dialog, total)
                RootUrl = aPlugin[0]
                WebUrl = aPlugin[1]
                ItemName = aPlugin[2]
                PlugWeb = self.get_remote_md5_sum(WebUrl)
                PlugRoot = self.get_root_md5_sum(RootUrl)
                if (PlugWeb != PlugRoot) and (PlugWeb):
                    try:
                        self.__download(WebUrl, RootUrl)
                        sContent += "[COLOR green]"+ItemName+"[/COLOR] \n"
                        sdown = sdown+1
                    except:
                        sContent += "[COLOR red]"+ItemName+"[/COLOR] \n"
              
            cConfig().finishDialog(dialog)
            sContent += "Fichier mise à jour %s / %s" %  (sdown, total)
            #self.TextBoxes('vStream mise à Jour', sContent)
            cConfig().setSetting('service_time', str(datetime.datetime.now()))
            cConfig().createDialogOK(sContent)
            return
            
    def __download(self, WebUrl, RootUrl):
            inf = urllib.urlopen(WebUrl)
            
            f = xbmcvfs.File(RootUrl, 'w')
            #if (xbmcvfs.exists(RootUrl)):
                #xbmcvfs.delete()
            #save it
            line = inf.read()         
            f.write(line)
            
            inf.close()
            f.close()
            
        
    def TextBoxes(self, heading, anounce):
        class TextBox():
            # constants
            WINDOW = 10147
            CONTROL_LABEL = 1
            CONTROL_TEXTBOX = 5

            def __init__( self, *args, **kwargs):
                # activate the text viewer window
                xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
                # get window
                self.win = xbmcgui.Window( self.WINDOW )
                # give window time to initialize
                xbmc.sleep( 500 )
                self.setControls()

            def setControls( self ):
                # set heading
                self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
                try:
                    f = open(anounce)
                    text = f.read()
                except: text=anounce
                self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
                return
        TextBox()

cAbout()
