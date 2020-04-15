# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
import subprocess  # , time, os
import xbmcvfs
from datetime import datetime
from resources.lib.comaddon import addon, xbmc, VSlog  # , xbmcgui, progress, dialog


def service():
    ADDON = addon()
    interval = ADDON.getSetting('heure_verification')
    record_is_activate = ADDON.getSetting('enregistrement_activer')
    if record_is_activate == 'false':
        return

    path_recording = 'special://userdata/addon_data/plugin.video.vstream/Enregistrement'
    path = ''.join([path_recording])
    if not xbmcvfs.exists(path):
        xbmcvfs.mkdir(path)

    record_list = xbmcvfs.listdir(path)
    ADDON.setSetting('path_enregistrement_programmation', path)
    record_in_progress = False
    monitor = xbmc.Monitor()

    while not monitor.abortRequested() and not record_in_progress == True:
        if monitor.waitForAbort(int(interval)):
            break

        hour = datetime.now().strftime('%d-%H-%M') + '.py'
        if hour in str(record_list):
            hour = path + '/' + hour
            hour = xbmc.translatePath(hour)
            record_in_progress = True
            VSlog('python ' + hour)
            command = 'python ' + hour
            proc = subprocess.Popen(command, stdout=subprocess.PIPE)
            p_status = proc.wait()


if __name__ == '__main__':
    service()
