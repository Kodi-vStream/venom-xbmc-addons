#-*- coding: utf-8 -*-
#Venom.
from config import cConfig
from util import isKrypton,VStranslatePath
import xbmc, xbmcgui, xbmcaddon
import sys, os
import urllib, urllib2
import sqlite3

sLibrary = xbmc.translatePath(cConfig().getAddonPath())
sys.path.append (sLibrary) 

SITE_IDENTIFIER = 'runscript'
SITE_NAME = 'runscript'

class cClear:

    def __init__(self):
        self.main(sys.argv[1])
        #self.__sFunctionName = ''

    def main(self, env):
        
        if (env == 'urlresolver'):
            xbmcaddon.Addon('script.module.urlresolver').openSettings()
            return
            
        elif (env == 'metahandler'):
            xbmcaddon.Addon('script.module.metahandler').openSettings()
            return
        
        elif (env == 'changelog'):
            try:
                sUrl = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/plugin.video.vstream/changelog.txt'
                oRequest =  urllib2.Request(sUrl)
                oResponse = urllib2.urlopen(oRequest)
                sContent = oResponse.read()
                from about import cAbout
                cAbout().TextBoxes('vStream Changelog', sContent)
            except:            
                cConfig().error("%s,%s" % (cConfig().getlanguage(30205), sUrl))
            return
            
        elif (env == 'soutient'):
            try:
                sUrl = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/plugin.video.vstream/soutient.txt'
                oRequest =  urllib2.Request(sUrl)
                oResponse = urllib2.urlopen(oRequest)
                sContent = oResponse.read()
                from about import cAbout
                cAbout().TextBoxes('vStream Soutient', sContent)
            except:            
                cConfig().error("%s,%s" % (cConfig().getlanguage(30205), sUrl))
            return

        elif (env == 'addon'):
            dialog = xbmcgui.Dialog()
            if dialog.yesno('vStream', 'Êtes-vous sûr ?','','','Non', 'Oui'):
                
                cached_fav = cConfig().getFileFav()
                cached_DB = cConfig().getFileDB()
                cached_Cache = cConfig().getFileCache()
                self.ClearDir2(xbmc.translatePath(cached_fav),True)
                self.ClearDir2(xbmc.translatePath(cached_DB),True)
                self.ClearDir2(xbmc.translatePath(cached_Cache),True)
                xbmc.executebuiltin("XBMC.Notification(Clear Addon Cache,Successful,5000,"")")
            return

        elif (env == 'xbmc'):
            dialog = xbmcgui.Dialog()
            if dialog.yesno('vStream', 'Êtes-vous sûr ?','','','Non', 'Oui'):
                self.ClearDir(xbmc.translatePath('special://temp/'),True)
                xbmc.executebuiltin("XBMC.Notification(Clear XBMC Cache,Successful,5000,"")")
            return

        elif (env == 'fi'):
            dialog = xbmcgui.Dialog()
            if dialog.yesno('vStream', 'Êtes-vous sûr ?','','','Non', 'Oui'):
                xbmc.executebuiltin("XBMC.Notification(Clear .fi Files ,Successful,2000,"")")
                if isKrypton() == True:
                    path = VStranslatePath('special://temp/archive_cache/')
                else:
                    path = VStranslatePath('special://temp/')
                    
                filenames = next(os.walk(path))[2]
                for i in filenames:
                    if ".fi" in i:
                        os.remove(os.path.join(path, i))
            return
        
        elif (env == 'uplog'):
            dialog = xbmcgui.Dialog()
            if dialog.yesno('vStream', 'Êtes-vous sûr ?','','','Non', 'Oui'):
                path = xbmc.translatePath('special://logpath/')
                UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
                headers = { 'User-Agent' : UA }
                filenames = next(os.walk(path))[2]
                for i in filenames:
                    if 'kodi.log' in i:
                        post_data = {}
                        cUrl = 'http://slexy.org/index.php/submit'
                        logop = open(path + i,'r')
                        result = logop.read()
                        logop.close()
                        post_data['raw_paste'] = result
                        post_data['author'] = 'kodi.log'
                        post_data['language'] = 'text'
                        post_data['permissions'] = 1 #private
                        post_data['expire'] = 259200 #3j
                        post_data['submit'] = 'Submit+Paste'
                        request = urllib2.Request(cUrl,urllib.urlencode(post_data),headers)
                        reponse = urllib2.urlopen(request)
                        code = reponse.geturl().replace('http://slexy.org/view/','')
                        reponse.close()
                        cConfig().createDialogOK('Ce code doit être transmis lorsque vous ouvrez une issue veuillez le noter:' + '  ' + code)
            return 
        
        elif (env == 'search'):
        
            from resources.lib.handler.pluginHandler import cPluginHandler
            valid = '[COLOR green][x][/COLOR]'
            try:
                sDips = sys.argv[2]
            except: return
        

            
            class XMLDialog(xbmcgui.WindowXMLDialog):

                def __init__(self, *args, **kwargs):
                    xbmcgui.WindowXMLDialog.__init__( self )
                    pass

                def onInit(self):

                    self.container = self.getControl(6)
                    self.button = self.getControl(5)
                    self.getControl(3).setVisible(False)
                    self.getControl(1).setLabel(cConfig().getlanguage(30094))
                    self.button.setLabel('OK')
                    listitems = []    
                    oPluginHandler = cPluginHandler()
                    aPlugins = oPluginHandler.getSearchPlugins()
                    #aPlugins = ['Adkami.com', u'adkami_com', 'Bienvenue sur ADkami.com.']
                    for aPlugin in aPlugins:
                        #teste si deja dans le dsip
                        sPluginSettingsName = sDips+'_' +aPlugin[1]
                        bPlugin = cConfig().getSetting(sPluginSettingsName)
                        
                        icon = os.path.join(unicode(cConfig().getRootArt(), 'utf-8'), 'sites', aPlugin[1]+'.png')
                        stitle = aPlugin[0].replace('[COLOR violet]','').replace('[COLOR orange]','').replace('[/COLOR]','')
                        if (bPlugin == 'true'):
                            stitle = ('%s %s') % (stitle, valid) 
                        listitem = xbmcgui.ListItem(label = stitle)
                        listitem.setArt({'icon' : icon, 'thumb' : icon})
                        listitem.setProperty('Addon.Summary', aPlugin[2])
                        listitem.setProperty('sitename', aPlugin[1])
                        if (bPlugin == 'true'):
                            listitem.select(True) 
                            
                        listitems.append(listitem)
                    self.container.addItems(listitems)
                    
                    
                    self.setFocus(self.container)
                      
                def message(self, message):
                    dialog = xbmcgui.Dialog()
                    dialog.ok(" My message title", message)
      
                def onClick(self, controlId):
                    if controlId == 5:
                        self.close()
                        return
                    elif controlId == 99:
                        window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
                        del window
                        self.close()
                        return
                    elif controlId == 6:
                        item = self.container.getSelectedItem()
                        if item.isSelected() == True:
                            label = item.getLabel().replace(valid,'')
                            item.setLabel(label)
                            item.select(False)
                            sPluginSettingsName = ('%s_%s') % (sDips, item.getProperty('sitename'))
                            cConfig().setSetting(sPluginSettingsName, str('false')) 
                        else : 
                            label = ('%s %s') % (item.getLabel(), valid) 
                            item.setLabel(label)
                            item.select(True)
                            sPluginSettingsName = ('%s_%s') % (sDips, item.getProperty('sitename'))
                            cConfig().setSetting(sPluginSettingsName, str('true'))
                        return

                def onFocus(self, controlId):
                    self.controlId = controlId
                    
                def _close_dialog( self ):
                    self.close()

                # def onAction( self, action ):
                    # if action.getId() in ( 9, 10, 92, 216, 247, 257, 275, 61467, 61448, ):
                        # self.close()
          
            wd = XMLDialog('DialogSelect.xml', cConfig().getAddonPath(), "Default")
            wd.doModal()
            del wd
            return

        elif (env == 'thumb'):
            dialog = xbmcgui.Dialog()
            if dialog.yesno('vStream', 'Êtes-vous sûr ? Ceci effacera toutes les thumbnails ','','','Non', 'Oui'):
                xbmc.executebuiltin("XBMC.Notification(Clear Thumbnails ,Successful,2000,"")")
                path = xbmc.translatePath('special://userdata/Thumbnails/')
                path2 = xbmc.translatePath('special://userdata/Database/')
                for i in os.listdir(path):
                    folders = os.path.join(path, i)
                    if os.path.isdir(folders):
                        p = next(os.walk(folders))[2]
                        for x in p:
                            os.remove(os.path.join(folders, x))
                       
                filenames = next(os.walk(path2))[2]
                for x in filenames:
                    if "exture" in x:
                        con = sqlite3.connect(os.path.join(path2, x))
                        cursor = con.cursor()
                        cursor.execute("DELETE FROM texture")
                        con.commit()
                        cursor.close()
                        con.close()
            return

        else:
                return
        return

    def ClearDir(self, dir, clearNested = False):
        dir = dir.decode("utf8")
        for the_file in os.listdir(dir):
            file_path = os.path.join(dir, the_file)
            if clearNested and os.path.isdir(file_path):
                self.ClearDir(file_path, clearNested)
                try: os.rmdir(file_path)
                except Exception, e: print str(e)
            else:
                try:os.unlink(file_path)
                except Exception, e: print str(e)
                    
    def ClearDir2(self, dir, clearNested = False):
        dir = dir.decode("utf8")
        try:os.unlink(dir)
        except Exception, e: print str(e)

cClear()
