# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

# Import enregistrement
import subprocess
import xbmcvfs
import xbmc

from datetime import datetime
from resources.lib.comaddon import addon, VSlog, VSPath, isMatrix, siteManager
from resources.lib.update import cUpdate


if isMatrix():
    # Import Serveur
    import threading
    from socketserver import ThreadingMixIn
    from http.server import HTTPServer, ThreadingHTTPServer


def service():
    # mise à jour des setting si nécessaire
    cUpdate().getUpdateSetting()

    # les flux TV ne permettent plus d'être enregistrés
    return

    # gestion des enregistrements en cours
    ADDON = addon()
    recordIsActivate = ADDON.getSetting('enregistrement_activer')
    if recordIsActivate == 'false':
        return

    pathRecording = 'special://userdata/addon_data/plugin.video.vstream/Enregistrement'
#    pathRecording = ADDON.getSetting('path_enregistrement_programmation')
    path = ''.join([pathRecording])
    if not xbmcvfs.exists(path):
        xbmcvfs.mkdir(path)

    # enregistrement TV
    recordList = xbmcvfs.listdir(path)
    interval = 55  # Vérifier toutes les minutes si un enregistrement est programmé
    ADDON.setSetting('path_enregistrement_programmation', path)
    recordInProgress = False
    monitor = xbmc.Monitor()

    del ADDON

    while not monitor.abortRequested() and recordInProgress is not True:
        if monitor.waitForAbort(int(interval)):
            break

        hour = datetime.now().strftime('%d-%H-%M') + '.py'
        if hour in str(recordList):
            hour = path + '/' + hour
            hour = VSPath(hour)
            recordInProgress = True
            VSlog('python ' + hour)
            command = 'python ' + hour
            proc = subprocess.Popen(command, stdout=subprocess.PIPE)
            p_status = proc.wait()

    # server_thread.join()


if __name__ == '__main__':
    service()

    if isMatrix():
        sitesManager = siteManager()
        if sitesManager.isActive('toonanime') or sitesManager.isActive('kaydo_ws'):
            class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
                """Handle requests in a separate thread."""

            def runServer():
                from resources.lib.proxy.ProxyHTTPRequestHandler import ProxyHTTPRequestHandler

                server_address = ('127.0.0.1', 2424)
                httpd = ThreadingHTTPServer(server_address, ProxyHTTPRequestHandler)

                server_thread = threading.Thread(target=httpd.serve_forever)
                server_thread.start()
                VSlog("Server Start")

                monitor = xbmc.Monitor()

                while not monitor.abortRequested():
                    if monitor.waitForAbort(1):
                        break

                httpd.shutdown()
