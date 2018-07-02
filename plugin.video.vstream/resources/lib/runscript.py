#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#Venom.
import xbmc, xbmcaddon
import sys, os
import urllib, urllib2

#vstream = xbmcaddon.Addon('plugin.video.vstream')
#sLibrary = xbmc.translatePath(vstream.getAddonInfo("path")).decode("utf-8")
#sys.path.append (sLibrary)

from resources.lib.config import cConfig

from resources.lib.comaddon import addon, dialog, VSlog, xbmcgui
#from util import VStranslatePath
#from resources.lib.util import VStranslatePath

try:
    from sqlite3 import dbapi2 as sqlite
    VSlog('SQLITE 3 as DB engine')
except:
    from pysqlite2 import dbapi2 as sqlite
    VSlog('SQLITE 2 as DB engine')


SITE_IDENTIFIER = 'runscript'
SITE_NAME = 'runscript'

class cClear:

    DIALOG = dialog()
    ADDON = addon()

    def __init__(self):
        self.main(sys.argv[1])
        #self.__sFunctionName = ''

    def main(self, env):

        if (env == 'urlresolver'):
            addon('script.module.urlresolver').openSettings()
            return

        elif (env == 'metahandler'):
            addon('script.module.metahandler').openSettings()
            return

        elif (env == 'changelog'):
            try:
                sUrl = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/plugin.video.vstream/changelog.txt'
                oRequest =  urllib2.Request(sUrl)
                oResponse = urllib2.urlopen(oRequest)
                sContent = oResponse.read()
                from resources.lib.about import cAbout
                cAbout().TextBoxes('vStream Changelog', sContent)
            except:
                self.DIALOG.VSerror("%s,%s" % (self.ADDON.VSlang(30205), sUrl))
            return

        elif (env == 'soutient'):
            try:
                sUrl = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/plugin.video.vstream/soutient.txt'
                oRequest =  urllib2.Request(sUrl)
                oResponse = urllib2.urlopen(oRequest)
                sContent = oResponse.read()
                from resources.lib.about import cAbout
                cAbout().TextBoxes('vStream Soutient', sContent)
            except:
                self.DIALOG.VSerror("%s,%s" % (self.ADDON.VSlang(30205), sUrl))
            return

        elif (env == 'addon'):
            dialog = xbmcgui.Dialog()
            if dialog.yesno('vStream', 'Êtes-vous sûr ?','','','Non', 'Oui'):
                cached_Cache = cConfig().getFileCache()
                cached_Cache = xbmc.translatePath(cached_Cache).decode("utf-8")
                self.ClearDir2(cached_Cache,True)
                self.DIALOG.VSinfo('Clear Addon Cache,Successful')
            return

        elif (env == 'clean'):
            liste = ['Historiques', 'Lecture en cours', 'Marqués vues', 'Marque-Pages', 'Téléchargements']
            ret = self.DIALOG.select('BDD à supprimer', liste)
            cached_DB = cConfig().getFileDB()

            sql_drop = ""

            if ret > -1:

                if ret == 0:
                    sql_drop = "DROP TABLE history"
                elif ret == 1:
                    sql_drop = "DROP TABLE resume"
                elif ret == 2:
                    sql_drop = "DROP TABLE watched"
                elif ret == 3:
                    sql_drop = "DROP TABLE favorite"
                elif ret == 4:
                    sql_drop = "DROP TABLE download"

                try:
                    db = sqlite.connect(cached_DB)
                    dbcur = db.cursor()
                    dbcur.execute(sql_drop)
                    db.commit()
                    dbcur.close()
                    db.close()
                    self.DIALOG.VSinfo("Suppression BDD,Successful")
                except:
                    self.DIALOG.VSerror("Suppresion BDD,Error")

            return

        elif (env == 'xbmc'):
            if self.DIALOG.VSyesno('Êtes-vous sûr ?'):
                temp = xbmc.translatePath('special://temp/').decode("utf-8")
                self.ClearDir(temp,True)
                xbmc.executebuiltin("XBMC.Notification(Clear XBMC Cache,Successful,5000,"")")
            return

        elif (env == 'fi'):
            if self.DIALOG.VSyesno('Êtes-vous sûr ?'):
                xbmc.executebuiltin("XBMC.Notification(Clear .fi Files ,Successful,2000,"")")
                path = xbmc.translatePath('special://temp/').decode("utf-8")
                filenames = next(os.walk(path))[2]
                for i in filenames:
                    if ".fi" in i:
                        os.remove(os.path.join(path, i))
            return

        elif (env == 'uplog'):
            if self.DIALOG.VSyesno('Êtes-vous sûr ?'):
                path = xbmc.translatePath('special://logpath/').decode("utf-8")
                UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
                headers = { 'User-Agent' : UA }
                filenames = next(os.walk(path))[2]
                for i in filenames:
                    if 'kodi.log' in i:
                        post_data = {}
                        cUrl = 'http://slexy.org/index.php/submit'
                        logop = open(path + i,'rb')
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
                        self.DIALOG.VSok('Ce code doit être transmis lorsque vous ouvrez une issue veuillez le noter:' + '  ' + code)
            return

        elif (env == 'search'):

            from resources.lib.handler.pluginHandler import cPluginHandler
            valid = '[COLOR green][x][/COLOR]'



            class XMLDialog(xbmcgui.WindowXMLDialog):

                ADDON = addon()

                def __init__(self, *args, **kwargs):
                    xbmcgui.WindowXMLDialog.__init__( self )
                    pass

                def onInit(self):

                    self.container = self.getControl(6)
                    self.button = self.getControl(5)
                    self.getControl(3).setVisible(False)
                    self.getControl(1).setLabel(self.ADDON.VSlang(30094))
                    self.button.setLabel('OK')
                    listitems = []
                    oPluginHandler = cPluginHandler()
                    aPlugins = oPluginHandler.getAllPlugins()

                    for aPlugin in aPlugins:
                        #teste si deja dans le dsip
                        sPluginSettingsName = 'plugin_' +aPlugin[1]
                        bPlugin = self.ADDON.getSetting(sPluginSettingsName)

                        icon = os.path.join(unicode(cConfig().getRootArt(), 'utf-8'), 'sites', aPlugin[1]+'.png')
                        stitle = aPlugin[0].replace('[COLOR violet]','').replace('[COLOR orange]','').replace('[/COLOR]','')
                        if (bPlugin == 'true'):
                            stitle = ('%s %s') % (stitle, valid)
                        listitem = xbmcgui.ListItem(label = stitle, label2 = aPlugin[2])
                        listitem.setArt({'icon' : icon, 'thumb' : icon})
                        listitem.setProperty('Addon.Summary', aPlugin[2])
                        listitem.setProperty('sitename', aPlugin[1])
                        if (bPlugin == 'true'):
                            listitem.select(True)

                        listitems.append(listitem)
                    self.container.addItems(listitems)


                    self.setFocus(self.container)

                def onClick(self, controlId):
                    if controlId == 5:
                        self.close()
                        return
                    elif controlId == 99:
                        window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
                        del window
                        self.close()
                        return
                    elif controlId == 7:
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
                            sPluginSettingsName = ('plugin_%s') % (item.getProperty('sitename'))
                            self.ADDON.setSetting(sPluginSettingsName, str('false'))
                        else :
                            label = ('%s %s') % (item.getLabel(), valid)
                            item.setLabel(label)
                            item.select(True)
                            sPluginSettingsName = ('plugin_%s') % (item.getProperty('sitename'))
                            self.ADDON.setSetting(sPluginSettingsName, str('true'))
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
 
            if self.DIALOG.VSyesno('Êtes-vous sûr ? Ceci effacera toutes les thumbnails '):
                self.DIALOG.VSinfo("Clear Thumbnails ,Successful")
                path = xbmc.translatePath('special://userdata/Thumbnails/').decode("utf-8")
                path2 = xbmc.translatePath('special://userdata/Database/').decode("utf-8")
                for i in os.listdir(path):
                    folders = os.path.join(path, i).encode('utf-8')
                    if os.path.isdir(folders):
                        p = next(os.walk(folders))[2]
                        for x in p:
                            os.remove(os.path.join(folders, x).encode('utf-8'))

                filenames = next(os.walk(path2))[2]
                for x in filenames:
                    if "exture" in x:
                        con = sqlite.connect(os.path.join(path2, x).encode('utf-8'))
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
        try:
            dir = dir.decode("utf8")
        except:
            pass
        for the_file in os.listdir(dir):
            file_path = os.path.join(dir, the_file).encode('utf-8')
            if clearNested and os.path.isdir(file_path):
                self.ClearDir(file_path, clearNested)
                try: os.rmdir(file_path)
                except Exception, e: print str(e)
            else:
                try:os.unlink(file_path)
                except Exception, e: print str(e)

    def ClearDir2(self, dir, clearNested = False):
        try:
            dir = dir.decode("utf8")
        except:
            pass
        try:os.unlink(dir)
        except Exception, e: print str(e)

cClear()
