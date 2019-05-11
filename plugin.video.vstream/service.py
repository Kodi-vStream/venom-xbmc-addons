import time, os, subprocess, xbmcvfs
from resources.lib.comaddon import progress, addon, xbmc, xbmcgui, VSlog, dialog
from datetime import datetime

def service():
    ADDON = addon()
    intervalle = ADDON.getSetting('heure_verification')
    enregistrementIsActif = ADDON.getSetting('enregistrement_activer')
    if enregistrementIsActif == 'false':
        return

    PathProgrammation = "special://userdata/addon_data/plugin.video.vstream/Enregistrement"
    path = "".join([PathProgrammation])
    if not xbmcvfs.exists(path):
        xbmcvfs.mkdir(path)

    ListeEnregistrement = xbmcvfs.listdir(path)
    ADDON.setSetting('path_enregistrement_programmation', path)
    EnregistrementEnCours = False
    monitor = xbmc.Monitor()

    while not monitor.abortRequested() and not EnregistrementEnCours == True:
        if monitor.waitForAbort(int(intervalle)):
            break

        heure = datetime.now().strftime('%d-%H-%M') + '.py'
        if heure in str(ListeEnregistrement):
            heure = path + '/' + heure
            heure = xbmc.translatePath(heure)
            EnregistrementEnCours = True
            VSlog('python ' + heure)
            command ='python ' + heure
            proc = subprocess.Popen(command, stdout=subprocess.PIPE)
            p_status = proc.wait()

if __name__ == '__main__':
    service()
