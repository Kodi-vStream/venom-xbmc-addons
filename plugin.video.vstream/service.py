# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
import subprocess  # , time, os
import xbmcvfs
from datetime import datetime
from resources.lib.comaddon import addon, xbmc, VSlog  # , xbmcgui, progress, dialog


def service():
    ADDON = addon()
    interval = ADDON.getSetting('heure_verification')
    recordIsActivate = ADDON.getSetting('enregistrement_activer')
    if recordIsActivate == 'false':
        return

    pathRecording = 'special://userdata/addon_data/plugin.video.vstream/Enregistrement'
    path = ''.join([pathRecording])
    if not xbmcvfs.exists(path):
        xbmcvfs.mkdir(path)

    recordList = xbmcvfs.listdir(path)
    ADDON.setSetting('path_enregistrement_programmation', path)
    recordInProgress = False
    monitor = xbmc.Monitor()

    while not monitor.abortRequested() and not recordInProgress == True:
        if monitor.waitForAbort(int(interval)):
            break

        hour = datetime.now().strftime('%d-%H-%M') + '.py'
        if hour in str(recordList):
            hour = path + '/' + hour
            hour = xbmc.translatePath(hour)
            recordInProgress = True
            VSlog('python ' + hour)
            command = 'python ' + hour
            proc = subprocess.Popen(command, stdout=subprocess.PIPE)
            p_status = proc.wait()


if __name__ == '__main__':
    service()
