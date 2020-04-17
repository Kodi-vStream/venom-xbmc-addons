# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.

# sLibrary = xbmc.translatePath('special://home/addons/plugin.video.vstream').decode('utf-8')
# sys.path.append (sLibrary)

from resources.lib.comaddon import addon, progress, dialog, window, VSlog, xbmc, xbmcgui
from resources.lib.handler.requestHandler import cRequestHandler
import urllib
import xbmcvfs
import datetime, time

try:
    import json
except:
    import simplejson as json

SITE_IDENTIFIER = 'about'
SITE_NAME = 'About'


class cAbout:

    # retourne True si les 2 fichiers sont present mais pas avec les memes tailles
    def checksize(self, filepath, size):
        try:
            # f=open(xbmc.translatePath(filepath))
            # Content = file.read()
            # file.close()
            # len(Content)

            f = xbmcvfs.File(filepath)
            s = f.size()
            f.close()

            if s == size:
                # ok fichier existe et meme taille
                return False
            # fichier existe mais pas la meme taille
            return True
        except:
            # fichier n'existe pas
            return False

        #au cas ou ....
        return False

    def getUpdate(self):
        addons = addon()
        service_time = addons.getSetting('service_time')
        service_version = addons.getSetting('service_version')
        # service_version = ''

        # Si pas d'heure indique = premiere install
        if not service_time:
            # On memorise la date d'aujourdhui
            addons.setSetting('service_time', str(datetime.datetime.now()))
            # Mais on force la maj avec une date a la con
            service_time = '2000-09-23 10:59:50.877000'

        if not service_version:
            # version de l'addon
            addons.setSetting('service_version', str(addons.getAddonInfo('version')))
            service_version = addons.getAddonInfo('version')

        # si addon = 0.7.0 et service_version 0.6.35 pas de mise ajour.
        if addons.getAddonInfo('version') > service_version:
            addons.setSetting('service_version', str(addons.getAddonInfo('version')))
            service_version = addons.getAddonInfo('version')

        if service_time:
            # delay mise a jour
            time_sleep = datetime.timedelta(hours = 72)
            time_now = datetime.datetime.now()
            time_service = self.__strptime(service_time, '%Y-%m-%d %H:%M:%S.%f')
            # pour test
            # if (time_sleep):
            if time_now - time_service > time_sleep:
                # verifier la nouvelle version

                sUrl = 'https://api.github.com/repos/Kodi-vStream/venom-xbmc-addons/releases/latest'
                oRequestHandler = cRequestHandler(sUrl)
                sHtmlContent = oRequestHandler.request()
                result = json.loads(sHtmlContent)

                # pour test
                # if (result['tag_name']):
                if result['tag_name'] > service_version:
                    addons.setSetting('service_futur', str(result['tag_name']))
                    addons.setSetting('home_update', str('true'))
                    addons.setSetting('service_time', str(datetime.datetime.now()))
                    dialog().VSinfo(addons.VSlang(30418))
                else:
                    addons.setSetting('service_time', str(datetime.datetime.now()))
                    addons.setSetting('home_update', str('false'))
                    VSlog(addons.VSlang(30048) + str(time_sleep + time_service))
        return

    # bug python
    def __strptime(self, date, format):
        try:
            date = datetime.datetime.strptime(date, format)
        except TypeError:
            date = datetime.datetime(*(time.strptime(date, format)[0:6]))
        return date

    def getRootPath(self, folder):

        path = 'special://home/addons'
        path = "/".join([path, folder])
        return path

    def resultGit(self):
        try:
            import json
        except:
            import simplejson as json

        try:
            sUrl = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/sites.json'
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()
            result = json.loads(sHtmlContent)

            sUrl = 'https://raw.githubusercontent.com/Kodi-vStream/venom-xbmc-addons/master/hosts.json'
            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()
            result += json.loads(sHtmlContent)
            # filtre trash & _init
            result = filter(lambda x: x['name'] != "trash", result)
            result = filter(lambda x: x['name'] != "__init__.py", result)
        except:
            return False
        return result

    def checkdownload(self):

        addons = addon()
        dialogs = dialog()
        if dialogs.VSyesno(addons.VSlang(30456)):

            service_futur = addons.getSetting('service_futur')
            service_version = addons.getSetting('service_version')
            if not service_futur:
                return self.getUpdate()
            if not service_version:
                return self.getUpdate()

            # result = self.resultGit()
            sUrl = 'https://api.github.com/repos/Kodi-vStream/venom-xbmc-addons/compare/%s...%s' % (service_version, service_futur)
            # pour test
            # sUrl = 'https://api.github.com/repos/Kodi-vStream/venom-xbmc-addons/compare/0.6.3...0.6.31'

            oRequestHandler = cRequestHandler(sUrl)
            sHtmlContent = oRequestHandler.request()
            result = json.loads(sHtmlContent)

            progress_ = progress()
            progress_.VScreate(addons.VSlang(30015))

            # site = ''
            sdown = 0
            add = 0
            dell = 0
            schange = 0
            text = ''
            listitems = []

            if result:

                # boucle download fichier
                total = len(result['files'])
                for i in result['files']:

                    if 'plugin.video.vstream' in i['filename']:
                        progress_.VSupdate(progress_, total)

                        rootpath = self.getRootPath(i['filename'])

                        try:
                            self.__download(i['raw_url'], rootpath)
                            # site += 'Add: [B]%s[/B] | Del: [B]%s[/B] | [COLOR green]%s[/COLOR][CR]' % (i['additions'], i['deletions'], i['filename'].encode('utf-8'))
                            add += i['additions']
                            dell += i['deletions']
                            sdown = sdown + 1
                            schange += i['changes']
                        except:
                            # site += "[COLOR red]" + i['filename'].encode("utf-8") + "[/COLOR][CR]"
                            sdown = sdown + 1
                            pass

                progress_.VSclose(progress_)

                # données fichiers
                sContent = 'Ajouter (%s) | Supprimer (%s) | Changement (%s) [CR]Fichiers mise à jour %s / %s' % (add, dell, schange, sdown, total)
                listitem = xbmcgui.ListItem(label = 'vStream', label2 = sContent)
                icon = 'special://home/addons/plugin.video.vstream/resources/art/update.png'
                listitem.setArt({'icon': icon, 'thumb': icon})
                listitems.append(listitem)

                # boucle commit
                for i in result['commits']:
                    try:
                        # text += '[B]%s[/B]: %s[CR]' % (i['commit']['author']['name'], i['commit']['message'].encode('utf-8'))
                        icon = i['author']['avatar_url']
                        login = i['author']['login']
                        desc = i['commit']['message'].encode('utf-8')
                        listitem = xbmcgui.ListItem(label = login, label2 = desc)
                        listitem.setArt({'icon': icon, 'thumb': icon})
                    except:
                        # text += '[B]%s[/B]: nop[CR]' % (i['commit']['author']['name'])
                        listitem = xbmcgui.ListItem(label = 'None', label2 = 'none')
                        pass
                    listitems.append(listitem)

                # sContent = 'Changement (%s) | Fichiers mise à jour %s / %s [CR]' % (schange, sdown, total)
                # sContent += '%s' % (text.encode('utf-8'))
                # sContent += '%s' % (site)

                addons.setSetting('service_time', str(datetime.datetime.now()))
                addons.setSetting('service_version', str(service_futur))
                addons.setSetting('home_update', str('false'))

                # fin = dialog().VSok(sContent)
                # fin = self.TextBoxes(sContent)
                fin = self.Box(listitems)
        return

    def __download(self, WebUrl, RootUrl):
        inf = urllib.urlopen(WebUrl)
        f = xbmcvfs.File(RootUrl, 'w')
        # save it
        line = inf.read()
        f.write(line)

        inf.close()
        f.close()

        return

    def TextBoxes(self, anounce):
        addons = addon()
        # activate the text viewer window
        xbmc.executebuiltin('ActivateWindow(%d)' % (10147))
        # get window
        win = window(10147)
        # win.show()
        # give window time to initialize
        xbmc.sleep(100)
        # set heading
        win.getControl(1).setLabel(addons.VSlang(30013))
        win.getControl(5).setText(anounce)
        while xbmc.getCondVisibility('Window.IsActive(10147)'):
            xbmc.sleep(100)
        ret = dialog().VSok(addons.VSlang(30014))
        return

    def Box(self, listitems):
        addons = addon()

        class XMLDialog(xbmcgui.WindowXMLDialog):

            def __init__(self, *args, **kwargs):
                xbmcgui.WindowXMLDialog.__init__(self)
                pass

            def onInit(self):

                self.container = self.getControl(6)
                self.button = self.getControl(5)
                self.getControl(3).setVisible(False)
                self.getControl(1).setLabel(addons.VSlang(30015))
                self.button.setLabel('OK')
                self.container.addItems(listitems)
                self.setFocus(self.container)

            def onClick(self, controlId):
                self.close()
                return

            def onFocus(self, controlId):
                self.controlId = controlId

            def _close_dialog(self):
                self.close()

        path = 'special://home/addons/plugin.video.vstream'
        wd = XMLDialog('DialogSelect.xml', path, 'Default')
        wd.doModal()
        del wd
        return
