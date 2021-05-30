# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

# vstream = xbmcaddon.Addon('plugin.video.vstream')
# sLibrary = VSPath(vstream.getAddonInfo("path")).decode("utf-8")
# sys.path.append (sLibrary)
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import addon, dialog, VSlog, window, VSPath, xbmc
from resources.lib.util import urlEncode

try:  # Python 2
    import urllib2

except ImportError:  # Python 3
    import urllib.request as urllib2

import xbmcvfs
import sys
import xbmc
import xbmcgui

try:
    from sqlite3 import dbapi2 as sqlite
    VSlog('SQLITE 3 as DB engine')
except:
    from pysqlite2 import dbapi2 as sqlite
    VSlog('SQLITE 2 as DB engine')

try:
    import json
except:
    import simplejson as json

SITE_IDENTIFIER = 'runscript'
SITE_NAME = 'runscript'


class cClear:

    DIALOG = dialog()
    ADDON = addon()

    def __init__(self):
        self.main(sys.argv[1])

    def main(self, env):

        if (env == 'urlresolver'):
            addon('script.module.urlresolver').openSettings()
            return

        elif (env == 'metahandler'):
            addon('script.module.metahandler').openSettings()
            return

        elif (env == 'changelog_old'):
            try:
                sUrl = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/plugin.video.vstream/changelog.txt'
                oRequest = urllib2.Request(sUrl)
                oResponse = urllib2.urlopen(oRequest)

                # En python 3 on doit décoder la reponse
                if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                    sContent = oResponse.read().decode('utf-8')
                else:
                    sContent = oResponse.read()

                self.TextBoxes('vStream Changelog', sContent)
            except:
                self.DIALOG.VSerror("%s, %s" % (self.ADDON.VSlang(30205), sUrl))
            return

        elif (env == 'changelog'):

            class XMLDialog(xbmcgui.WindowXMLDialog):

                def __init__(self, *args, **kwargs):
                    xbmcgui.WindowXMLDialog.__init__(self)
                    pass

                def onInit(self):

                    self.container = self.getControl(6)
                    self.button = self.getControl(5)
                    self.getControl(3).setVisible(False)
                    self.getControl(1).setLabel('ChangeLog')
                    self.button.setLabel('OK')

                    sUrl = 'https://api.github.com/repos/Kodi-vStream/venom-xbmc-addons/commits'
                    oRequest = urllib2.Request(sUrl)
                    oResponse = urllib2.urlopen(oRequest)

                    # En python 3 on doit décoder la reponse
                    if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                        sContent = oResponse.read().decode('utf-8')
                    else:
                        sContent = oResponse.read()

                    result = json.loads(sContent)
                    listitems = []

                    for item in result:
                        # autor
                        icon = item['author']['avatar_url']
                        login = item['author']['login']
                        # message
                        try:
                            desc = item['commit']['message'].encode("utf-8")
                        except:
                            desc = 'None'

                        listitem = xbmcgui.ListItem(label=login, label2=desc)
                        listitem.setArt({'icon': icon, 'thumb': icon})

                        listitems.append(listitem)

                    self.container.addItems(listitems)
                    self.setFocus(self.container)

                def onClick(self, controlId):
                    self.close()
                    return

                def onFocus(self, controlId):
                    self.controlId = controlId

                def _close_dialog(self):
                    self.close()

            path = "special://home/addons/plugin.video.vstream"
            wd = XMLDialog('DialogSelect.xml', path, "Default")
            wd.doModal()
            del wd
            return

        elif (env == 'soutient'):
            try:
                sUrl = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/plugin.video.vstream/soutient.txt'
                oRequest = urllib2.Request(sUrl)
                oResponse = urllib2.urlopen(oRequest)

                # En python 3 on doit décoder la reponse
                if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                    sContent = oResponse.read().decode('utf-8')
                else:
                    sContent = oResponse.read()

                self.TextBoxes('vStream Soutient', sContent)
            except:
                self.DIALOG.VSerror("%s, %s" % (self.ADDON.VSlang(30205), sUrl))
            return

        elif (env == 'addon'): # Vider le cache des métadonnées
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                cached_Cache = "special://home/userdata/addon_data/plugin.video.vstream/video_cache.db"
                # important seul xbmcvfs peux lire le special
                try:
                    cached_Cache = VSPath(cached_Cache).decode("utf-8")
                except AttributeError:
                    cached_Cache = VSPath(cached_Cache)
                
                try:
                    db = sqlite.connect(cached_Cache)
                    dbcur = db.cursor()
                    dbcur.execute('DELETE FROM movie')
                    dbcur.execute('DELETE FROM tvshow')
                    dbcur.execute('DELETE FROM season')
                    dbcur.execute('DELETE FROM episode')
                    db.commit()
                    dbcur.close()
                    db.close()
                    self.DIALOG.VSinfo(self.ADDON.VSlang(30090))
                except:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30091))
            return

        elif (env == 'clean'):
            liste = ['Historiques', 'Lecture en cours', 'Marqués vues', 'Marque-Pages', 'Téléchargements']
            ret = self.DIALOG.VSselect(liste, self.ADDON.VSlang(30110))
            cached_DB = "special://home/userdata/addon_data/plugin.video.vstream/vstream.db"
            # important seul xbmcvfs peux lire le special
            try:
                cached_DB = VSPath(cached_DB).decode("utf-8")
            except AttributeError:
                cached_DB = VSPath(cached_DB)

            sql_drop = ""

            if ret > -1:

                if ret == 0:
                    sql_drop = 'DELETE FROM history'
                elif ret == 1:
                    sql_drop = 'DELETE FROM resume'
                elif ret == 2:
                    sql_drop = 'DELETE FROM watched'
                elif ret == 3:
                    sql_drop = 'DELETE FROM favorite'
                elif ret == 4:
                    sql_drop = 'DELETE FROM download'

                try:
                    db = sqlite.connect(cached_DB)
                    dbcur = db.cursor()
                    dbcur.execute(sql_drop)
                    db.commit()
                    dbcur.close()
                    db.close()
                    self.DIALOG.VSok(self.ADDON.VSlang(30090))
                except Exception as err:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30091))
                    VSlog("Exception runscript sql_drop: {0}".format(err))
            return

        elif (env == 'xbmc'):
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                path = "special://temp/"
                try:
                    xbmcvfs.rmdir(path, True)
                    self.DIALOG.VSok(self.ADDON.VSlang(30092))
                except:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30093))
            return

        elif (env == 'fi'):
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                path = "special://temp/archive_cache/"
                try:
                    xbmcvfs.rmdir(path, True)
                    self.DIALOG.VSok(self.ADDON.VSlang(30095))
                except:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30096))
            return

        elif (env == 'uplog'):
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                path = "special://logpath/kodi.log"
                UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
                headers = {'User-Agent': UA}
                if xbmcvfs.exists(path):
                    post_data = {}
                    cUrl = 'http://slexy.org/index.php/submit'
                    logop = xbmcvfs.File(path, 'rb')
                    result = logop.read()
                    logop.close()

                    oRequestHandler = cRequestHandler(cUrl)
                    oRequestHandler.setRequestType(1)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addParameters('raw_paste',result)
                    oRequestHandler.addParameters('author', "kodi.log")
                    oRequestHandler.addParameters('language', "text")
                    oRequestHandler.addParameters('permissions',1) # private
                    oRequestHandler.addParameters('expire', 259200)  # 3j
                    oRequestHandler.addParameters('submit', 'Submit+Paste') 
                    sHtmlContent = oRequestHandler.request()
                    code = oRequestHandler.getRealUrl().replace('http://slexy.org/view/', '')

                    self.ADDON.setSetting('service_log', code)
                    self.DIALOG.VSok(self.ADDON.VSlang(30097) + '  ' + code)
            return

        elif (env == 'search'):

            from resources.lib.handler.pluginHandler import cPluginHandler
            valid = '[COLOR green][x][/COLOR]'

            class XMLDialog(xbmcgui.WindowXMLDialog):

                ADDON = addon()

                def __init__(self, *args, **kwargs):
                    xbmcgui.WindowXMLDialog.__init__(self)
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
                        # teste si deja dans le dsip
                        sPluginSettingsName = 'plugin_' + aPlugin[1]
                        bPlugin = self.ADDON.getSetting(sPluginSettingsName)

                        icon = "special://home/addons/plugin.video.vstream/resources/art/sites/%s.png" % aPlugin[1]
                        stitle = aPlugin[0].replace('[COLOR violet]', '').replace('[COLOR orange]', '')\
                                           .replace('[/COLOR]', '').replace('[COLOR dodgerblue]', '')\
                                           .replace('[COLOR coral]', '')
                        if (bPlugin == 'true'):
                            stitle = ('%s %s') % (stitle, valid)
                        listitem = xbmcgui.ListItem(label=stitle, label2=aPlugin[2])
                        listitem.setArt({'icon': icon, 'thumb': icon})
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
                            label = item.getLabel().replace(valid, '')
                            item.setLabel(label)
                            item.select(False)
                            sPluginSettingsName = ('plugin_%s') % (item.getProperty('sitename'))
                            self.ADDON.setSetting(sPluginSettingsName, str('false'))
                        else:
                            label = ('%s %s') % (item.getLabel(), valid)
                            item.setLabel(label)
                            item.select(True)
                            sPluginSettingsName = ('plugin_%s') % (item.getProperty('sitename'))
                            self.ADDON.setSetting(sPluginSettingsName, str('true'))
                        return

                def onFocus(self, controlId):
                    self.controlId = controlId

                def _close_dialog(self):
                    self.close()

                # def onAction(self, action):
                    # if action.getId() in (9, 10, 92, 216, 247, 257, 275, 61467, 61448):
                        # self.close()

            path = "special://home/addons/plugin.video.vstream"
            wd = XMLDialog('DialogSelect.xml', path, "Default")
            wd.doModal()
            del wd
            return

        elif (env == 'thumb'):

            if self.DIALOG.VSyesno(self.ADDON.VSlang(30098)):

                text = False
                path = "special://userdata/Thumbnails/"
                path_DB = "special://userdata/Database"
                try:
                    xbmcvfs.rmdir(path, True)
                    text = 'Clear Thumbnail Folder, Successful[CR]'
                except:
                    text = 'Clear Thumbnail Folder, Error[CR]'

                folder, items = xbmcvfs.listdir(path_DB)
                items.sort()
                for sItemName in items:
                    if "extures" in sItemName:
                        cached_Cache = "/".join([path_DB, sItemName])
                        try:
                            xbmcvfs.delete(cached_Cache)
                            text += 'Clear Thumbnail DB, Successful[CR]'
                        except:
                            text += 'Clear Thumbnail DB, Error[CR]'

                if text:
                    text = "%s (Important relancer Kodi)" % text
                    self.DIALOG.VSok(text)
            return

        elif (env == 'sauv'):
            select = self.DIALOG.VSselect(['Import', 'Export'])
            DB = "special://home/userdata/addon_data/plugin.video.vstream/vstream.db"
            if select >= 0:
                try:
                    if select == 0:
                        # sélection d'un fichier
                        new = self.DIALOG.VSbrowse(1, 'vStream', "files")
                        if new:
                            xbmcvfs.delete(DB)
                            xbmcvfs.copy(new, DB)
                            self.DIALOG.VSinfo(self.ADDON.VSlang(30099))
                    elif select == 1:
                        # sélection d'un répertoire
                        new = self.DIALOG.VSbrowse(3, 'vStream', "files")
                        if new:
                            xbmcvfs.copy(DB, new + 'vstream.db')
                            self.DIALOG.VSinfo(self.ADDON.VSlang(30099))
                except:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30100))

                return

        else:
            return

        return

    # def ClearDir(self, dir, clearNested=False):
    #     try:
    #         dir = dir.decode("utf8")
    #     except:
    #         pass
    #     for the_file in os.listdir(dir):
    #         file_path = os.path.join(dir, the_file).encode('utf-8')
    #         if clearNested and os.path.isdir(file_path):
    #             self.ClearDir(file_path, clearNested)
    #             try: os.rmdir(file_path)
    #             except Exception as e:
    #                 print(str(e))
    #         else:
    #             try:os.unlink(file_path)
    #             except Exception as e:
    #                 print str(e)

    # def ClearDir2(self, dir, clearNested=False):
    #     try:
    #         dir = dir.decode("utf8")
    #     except:
    #         pass
    #     try:os.unlink(dir)
    #     except Exception as e:
    #         print(str(e))

    def TextBoxes(self, heading, anounce):
        # activate the text viewer window
        xbmc.executebuiltin("ActivateWindow(%d)" % 10147)
        # get window
        win = window(10147)
        # win.show()
        # give window time to initialize
        xbmc.sleep(100)
        # set heading
        win.getControl(1).setLabel(heading)
        win.getControl(5).setText(anounce)
        return


cClear()
