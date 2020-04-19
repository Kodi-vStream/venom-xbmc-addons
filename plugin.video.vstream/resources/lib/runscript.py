# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.

# vstream = xbmcaddon.Addon('plugin.video.vstream')
# sLibrary = xbmc.translatePath(vstream.getAddonInfo("path")).decode("utf-8")
# sys.path.append (sLibrary)

from resources.lib.comaddon import addon, dialog, VSlog, xbmc, xbmcgui, window
import xbmcvfs
import sys
import urllib
import urllib2
# from util import VStranslatePath
# from resources.lib.util import VStranslatePath

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
        # self.__sFunctionName = ''

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

                        listitem = xbmcgui.ListItem(label = login, label2 = desc)
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

            # path = cConfig().getAddonPath()
            path = "special://home/addons/plugin.video.vstream"
            wd = XMLDialog('DialogSelect.xml', path, "Default")
            wd.doModal()
            del wd
            return

        elif (env == 'soutient'):
            try:
                sUrl = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/plugin.video.vstream/soutient.txt'
                oRequest =  urllib2.Request(sUrl)
                oResponse = urllib2.urlopen(oRequest)
                sContent = oResponse.read()
                self.TextBoxes('vStream Soutient', sContent)
            except:
                self.DIALOG.VSerror("%s, %s" % (self.ADDON.VSlang(30205), sUrl))
            return

        elif (env == 'addon'):
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                # cached_Cache = cConfig().getFileCache()
                # cached_Cache = xbmc.translatePath(cached_Cache).decode("utf-8")
                cached_Cache = "special://home/userdata/addon_data/plugin.video.vstream/video_cache.db"
                # self.ClearDir2(cached_Cache, True)
                try:
                    xbmcvfs.delete(cached_Cache)
                    self.DIALOG.VSinfo(self.ADDON.VSlang(30089))
                except:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30087))

            return

        elif (env == 'clean'):
            liste = ['Historiques', 'Lecture en cours', 'Marqués vues', 'Marque-Pages', 'Téléchargements']
            ret = self.DIALOG.select(self.ADDON.VSlang(30110), liste)
            # cached_DB = cConfig().getFileDB()
            cached_DB = "special://home/userdata/addon_data/plugin.video.vstream/vstream.db"
            # important seul xbmcvfs peux lire le special
            cached_DB = xbmc.translatePath(cached_DB).decode("utf-8")

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
                    self.DIALOG.VSok(self.ADDON.VSlang(30090))
                except:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30091))

            return

        elif (env == 'xbmc'):
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                # temp = xbmc.translatePath('special://temp/').decode("utf-8")
                path = "special://temp/"
                # self.ClearDir(temp,True)
                try:
                    xbmcvfs.rmdir(path, True)
                    self.DIALOG.VSok(self.ADDON.VSlang(30092))
                except:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30093))
            return

        elif (env == 'fi'):
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                # path = xbmc.translatePath('special://temp/').decode("utf-8")
                path = "special://temp/archive_cache/"
                try:
                    xbmcvfs.rmdir(path, True)
                    self.DIALOG.VSok(self.ADDON.VSlang(30095))
                except:
                    self.DIALOG.VSerror(self.ADDON.VSlang(30096))
                # filenames = next(os.walk(path))[2]
                # for i in filenames:
                #     if ".fi" in i:
                #         os.remove(os.path.join(path, i))
            return

        elif (env == 'uplog'):
            if self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                # path = xbmc.translatePath('special://logpath/').decode("utf-8")
                path = "special://logpath/kodi.log"
                UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
                headers = {'User-Agent': UA}
                # filenames = next(os.walk(path))[2]
                # for i in filenames:
                if xbmcvfs.exists(path):
                    post_data = {}
                    cUrl = 'http://slexy.org/index.php/submit'
                    # logop = open(path + i, 'rb')
                    logop = xbmcvfs.File(path, 'rb')
                    result = logop.read()
                    logop.close()
                    post_data['raw_paste'] = result
                    post_data['author'] = 'kodi.log'
                    post_data['language'] = 'text'
                    post_data['permissions'] = 1  # private
                    post_data['expire'] = 259200  # 3j
                    post_data['submit'] = 'Submit+Paste'
                    request = urllib2.Request(cUrl, urllib.urlencode(post_data), headers)
                    reponse = urllib2.urlopen(request)
                    code = reponse.geturl().replace('http://slexy.org/view/', '')
                    reponse.close()
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

                        # icon = os.path.join(unicode(cConfig().getRootArt(), 'utf-8'), 'sites', aPlugin[1] + '.png')
                        icon = "special://home/addons/plugin.video.vstream/resources/art/sites/%s.png" % aPlugin[1]
                        stitle = aPlugin[0].replace('[COLOR violet]', '').replace('[COLOR orange]', '').replace('[/COLOR]', '').replace('[COLOR dodgerblue]', '').replace('[COLOR coral]', '')
                        if (bPlugin == 'true'):
                            stitle = ('%s %s') % (stitle, valid)
                        listitem = xbmcgui.ListItem(label = stitle, label2 = aPlugin[2])
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
                    # if action.getId() in (9, 10, 92, 216, 247, 257, 275, 61467, 61448, ):
                        # self.close()

            # path = cConfig().getAddonPath()
            path = "special://home/addons/plugin.video.vstream"
            wd = XMLDialog('DialogSelect.xml', path, "Default")
            wd.doModal()
            del wd
            return

        elif (env == 'thumb'):

            if self.DIALOG.VSyesno(self.ADDON.VSlang(30098)):

                text = False
                # path = xbmc.translatePath('special://userdata/Thumbnails/').decode("utf-8")
                path = "special://userdata/Thumbnails/"
                path_DB = "special://userdata/Database"
                try:
                    xbmcvfs.rmdir(path, True)
                    text = 'Clear Thumbnail Folder, Successful[CR]'
                except:
                    text = 'Clear Thumbnail Folder, Error[CR]'
                # for i in os.listdir(path):
                    # folders = os.path.join(path, i).encode('utf-8')
                    # if os.path.isdir(folders):
                    #     p = next(os.walk(folders))[2]
                    #     for x in p:
                    #         os.remove(os.path.join(folders, x).encode('utf-8'))

                # filenames = next(os.walk(path2))[2]
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
                # for x in filenames:
                #     if "exture" in x:
                #         con = sqlite.connect(os.path.join(path2, x).encode('utf-8'))
                #         cursor = con.cursor()
                #         cursor.execute("DELETE FROM texture")
                #         con.commit()
                #         cursor.close()
                #         con.close()
            return

        elif (env == 'sauv'):
            # dialog.select('Choose a playlist', ['Playlist #1', 'Playlist #2, 'Playlist #3'])
            select = self.DIALOG.VSselect(['Import', 'Export'])
            DB = "special://home/userdata/addon_data/plugin.video.vstream/vstream.db"
            if select >= 0:
                new = self.DIALOG.browse(3, 'vStream', "files")
                if new:
                    try:
                        if select == 0:
                            xbmcvfs.delete(DB)
                            # copy(source, destination)--copy file to destination, returns true/false.
                            xbmcvfs.copy(new + 'vstream.db', DB)
                        elif select == 1:
                            # copy(source, destination)--copy file to destination, returns true/false.
                            xbmcvfs.copy(DB, new + 'vstream.db')
                        self.DIALOG.VSinfo(self.ADDON.VSlang(30099))
                    except:
                        self.DIALOG.VSerror(self.ADDON.VSlang(30100))

                return

        else:
            return

        return

    # def ClearDir(self, dir, clearNested = False):
    #     try:
    #         dir = dir.decode("utf8")
    #     except:
    #         pass
    #     for the_file in os.listdir(dir):
    #         file_path = os.path.join(dir, the_file).encode('utf-8')
    #         if clearNested and os.path.isdir(file_path):
    #             self.ClearDir(file_path, clearNested)
    #             try: os.rmdir(file_path)
    #             except Exception, e: print str(e)
    #         else:
    #             try:os.unlink(file_path)
    #             except Exception, e: print str(e)

    # def ClearDir2(self, dir, clearNested = False):
    #     try:
    #         dir = dir.decode("utf8")
    #     except:
    #         pass
    #     try:os.unlink(dir)
    #     except Exception, e: print str(e)

    def TextBoxes(self, heading, anounce):
        # activate the text viewer window
        xbmc.executebuiltin("ActivateWindow(%d)" % (10147))
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
