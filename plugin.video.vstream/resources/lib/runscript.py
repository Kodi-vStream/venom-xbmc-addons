#-*- coding: utf-8 -*-
#Venom.
from config import cConfig

import xbmc, xbmcgui, xbmcaddon
import sys, os
import urllib, urllib2


try:
    from sqlite3 import dbapi2 as sqlite
    cConfig().log('SQLITE 3 as DB engine')
except:
    from pysqlite2 import dbapi2 as sqlite
    cConfig().log('SQLITE 2 as DB engine')

sLibrary = xbmc.translatePath(cConfig().getAddonPath()).decode("utf-8")
sys.path.append (sLibrary)

#from resources.lib.util import VStranslatePath
from util import VStranslatePath


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

                #cached_fav = cConfig().getFileFav()
                #cached_DB = cConfig().getFileDB()
                cached_Cache = cConfig().getFileCache()
                #self.ClearDir2(VStranslatePath(cached_fav),True)
                #self.ClearDir2(VStranslatePath(cached_DB),True)
                self.ClearDir2(VStranslatePath(cached_Cache),True)
                xbmc.executebuiltin("XBMC.Notification(Clear Addon Cache,Successful,5000,"")")
            return

        elif (env == 'clean'):
            dialog = xbmcgui.Dialog()
            liste = ['Historiques', 'Lecture en cours', 'Marqués vues', 'Marque-Pages', 'Téléchargements']
            ret = dialog.select('BDD à supprimer', liste)
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
                    xbmc.executebuiltin("XBMC.Notification(Suppression BDD,Successful,5000,"")")
                except:
                    xbmc.executebuiltin("XBMC.Notification(Suppresion BDD,Error,5000,"")")

            return

        elif (env == 'xbmc'):
            dialog = xbmcgui.Dialog()
            if dialog.yesno('vStream', 'Êtes-vous sûr ?','','','Non', 'Oui'):
                self.ClearDir(VStranslatePath('special://temp/'),True)
                xbmc.executebuiltin("XBMC.Notification(Clear XBMC Cache,Successful,5000,"")")
            return

        elif (env == 'fi'):
            dialog = xbmcgui.Dialog()
            if dialog.yesno('vStream', 'Êtes-vous sûr ?','','','Non', 'Oui'):
                xbmc.executebuiltin("XBMC.Notification(Clear .fi Files ,Successful,2000,"")")
                path = VStranslatePath('special://temp/')
                filenames = next(os.walk(path))[2]
                for i in filenames:
                    if ".fi" in i:
                        os.remove(os.path.join(path, i))
            return

        elif (env == 'uplog'):
            dialog = xbmcgui.Dialog()
            if dialog.yesno('vStream', 'Êtes-vous sûr ?','','','Non', 'Oui'):
                path = VStranslatePath('special://logpath/')
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
                        cConfig().createDialogOK('Ce code doit être transmis lorsque vous ouvrez une issue veuillez le noter:' + '  ' + code)
            return

        elif (env == 'search'):

            from resources.lib.handler.pluginHandler import cPluginHandler
            valid = '[COLOR green][x][/COLOR]'



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

                    for aPlugin in aPlugins:
                        #teste si deja dans le dsip
                        sPluginSettingsName = 'plugin_' +aPlugin[1]
                        bPlugin = cConfig().getSetting(sPluginSettingsName)

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
                            cConfig().setSetting(sPluginSettingsName, str('false'))
                        else :
                            label = ('%s %s') % (item.getLabel(), valid)
                            item.setLabel(label)
                            item.select(True)
                            sPluginSettingsName = ('plugin_%s') % (item.getProperty('sitename'))
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
                path = VStranslatePath('special://userdata/Thumbnails/')
                path2 = VStranslatePath('special://userdata/Database/')
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
