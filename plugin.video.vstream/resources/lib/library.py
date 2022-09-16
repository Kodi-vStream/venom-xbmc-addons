# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import os
import sys

import xbmcgui
import xbmcplugin
import xbmcvfs
import xbmc

from resources.lib.comaddon import addon, dialog, VSPath
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.util import cUtil, QuotePlus

SITE_IDENTIFIER = 'cLibrary'
SITE_NAME = 'Library'

# sources.xml


class cLibrary:
    ADDON = addon()

    def __init__(self):
        self.__sMovieFolder = self.ADDON.getSetting('Library_folder_Movies')
        self.__sTVFolder = self.ADDON.getSetting('Library_folder_TVs')

        if not self.__sMovieFolder:
            self.__sMovieFolder = 'special://userdata/addon_data/plugin.video.vstream/Films'
            self.ADDON.setSetting('Library_folder_Movies', self.__sMovieFolder)
        if not xbmcvfs.exists(self.__sMovieFolder):
            xbmcvfs.mkdir(self.__sMovieFolder)

        if not self.__sTVFolder:
            self.__sTVFolder = 'special://userdata/addon_data/plugin.video.vstream/Series'
            self.ADDON.setSetting('Library_folder_TVs', self.__sTVFolder)
        if not xbmcvfs.exists(self.__sTVFolder):
            xbmcvfs.mkdir(self.__sTVFolder)

        self.__sTitle = ''

    def setLibrary(self):
        oInputParameterHandler = cInputParameterHandler()
        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sFileName = oInputParameterHandler.getValue('sFileName')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')

        ret = dialog().VSselect(['Film', 'Série'], 'Sélectionner une catégorie')
        if ret == 0:
            sCat = '1'
        elif ret == -1:
            return
        else:
            sCat = '2'

        sMediaUrl = QuotePlus(sMediaUrl)
        #sFileName = QuotePlus(sFileName)

        sLink = 'plugin://plugin.video.vstream/?function=play&site=cHosterGui&sFileName='
        sLink += sFileName + '&sMediaUrl=' + sMediaUrl + '&sHosterIdentifier=' + sHosterIdentifier

        sTitle = sFileName

        if sCat == '1':  # film
            #sTitle = cUtil().CleanName(sTitle)
            sTitle = self.showKeyBoard(sTitle, 'Nom du fichier')

            try:
                sPath = '/'.join([self.__sMovieFolder, sTitle])

                if not xbmcvfs.exists(sPath):
                    xbmcvfs.mkdir(sPath)

                self.MakeFile(sPath, sTitle, sLink)
            except:
                dialog().VSinfo('Rajout impossible')

        elif sCat == '2':  # serie
            #sTitle = cUtil().CleanName(sTitle)
            sFTitle = self.showKeyBoard(sTitle, 'Saison : Recommandé NomDeSerie/Saison01')

            try:

                sPath = '/'.join([self.__sTVFolder, sFTitle])

                if not xbmcvfs.exists(sPath):
                    xbmcvfs.mkdir(sPath)

                sTitle = self.showKeyBoard(sTitle, 'Épisode : Recommandé NomDeSerie S01E01')

                self.MakeFile(sPath, sTitle, sLink)
            except:
                dialog().VSinfo('Rajout impossible')

    def MakeFile(self, folder, name, content):
        stream = '/'.join([folder, str(name)]) + '.strm'
        f = xbmcvfs.File(stream, 'w')
        result = f.write(str(content))
        f.close()
        if result:
            dialog().VSinfo('Elément rajouté à la librairie')
        else:
            dialog().VSinfo('Rajout impossible')

    def getLibrary(self):
        oGui = cGui()
        oOutputParameterHandler = cOutputParameterHandler()

        folder = self.ADDON.getSetting('Library_folder_Movies')
        oOutputParameterHandler.addParameter('siteUrl', folder)
        oGui.addDir(SITE_IDENTIFIER, 'openLibrary', self.ADDON.VSlang(30120), 'films.png', oOutputParameterHandler)

        folder = self.ADDON.getSetting('Library_folder_TVs')
        oOutputParameterHandler.addParameter('siteUrl', folder)
        oGui.addDir(SITE_IDENTIFIER, 'openLibrary', self.ADDON.VSlang(30121), 'series.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()


    def getRecords(self):
        oGui = cGui()

        folder = self.ADDON.getSetting('path_enregistrement')
        if not folder:
            folder = 'special://userdata/addon_data/plugin.video.vstream/Enregistrement"/>'
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', folder)
        oGui.addDir(SITE_IDENTIFIER, 'openLibrary', self.ADDON.VSlang(30225), 'download.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def openLibrary(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()
        sFile = oInputParameterHandler.getValue('siteUrl')

        listDir = xbmcvfs.listdir(sFile)

        if listDir[0]:
            data = listDir[0]
        else:
            data = listDir[1]

        addon_handle = None
        for i in data:
            path = VSPath(sFile + '/' + i)  # Suppression du special: pour plus tard
            sTitle = os.path.basename(path)  # Titre du fichier .strm

            if '.strm' in i:
                sHosterUrl = sFile + '/' + i
                addon_handle = int(sys.argv[1])
                xbmcplugin.setContent(addon_handle, 'video')
                li = xbmcgui.ListItem(sTitle)
                xbmcplugin.addDirectoryItem(handle=addon_handle, url=sHosterUrl, listitem=li)

            else:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sFile + '/' + i)
                oGui.addDir(SITE_IDENTIFIER, 'openLibrary', sTitle, 'films.png', oOutputParameterHandler)

        if addon_handle:
            xbmcplugin.endOfDirectory(addon_handle)
        else:
            oGui.setEndOfDirectory()

    def Delfile(self):
        oInputParameterHandler = cInputParameterHandler()
        sFile = oInputParameterHandler.getValue('sFile')

        xbmcvfs.delete(sFile)

        runClean = self.DIALOG.VSyesno('Voulez vous mettre à jour la librairie maintenant (non conseillé)', 'Fichier supprimé')
        if not runClean:
            return

        xbmc.executebuiltin('CleanLibrary(video)')

    def ShowContent(self):
        oInputParameterHandler = cInputParameterHandler()
        sFolder = oInputParameterHandler.getValue('folder')
        xbmc.executebuiltin('Container.Update(' + sFolder + ')')

    def showKeyBoard(self, sDefaultText='', Heading=''):
        keyboard = xbmc.Keyboard(sDefaultText)
        keyboard.setHeading(Heading)  # optional
        keyboard.doModal()
        if keyboard.isConfirmed():
            sSearchText = keyboard.getText()
            if (len(sSearchText)) > 0:
                return sSearchText

        return False
