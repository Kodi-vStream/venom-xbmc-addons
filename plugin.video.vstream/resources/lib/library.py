#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.util import cUtil
from resources.lib.gui.gui import cGui

import xbmcvfs
import os,re
import urllib,re
import xbmc,xbmcgui

SITE_IDENTIFIER = 'cLibrary'
SITE_NAME = 'Library'

#sources.xml

class cLibrary:

    def __init__(self):
        self.__sMovieFolder = xbmc.translatePath(cConfig().getSetting('Library_folder_Movies')).decode("utf-8")
        self.__sTVFolder = xbmc.translatePath(cConfig().getSetting('Library_folder_TVs')).decode("utf-8")

        if not self.__sMovieFolder:
            PathCache = cConfig().getSettingCache()
            self.__sMovieFolder = os.path.join(PathCache,'Movies\\').decode("utf-8")
            cConfig().setSetting('Library_folder_Movies',self.__sMovieFolder)
        if not xbmcvfs.exists(self.__sMovieFolder):
                xbmcvfs.mkdir(self.__sMovieFolder)

        if not self.__sTVFolder:
            PathCache = cConfig().getSettingCache()
            self.__sTVFolder = os.path.join(PathCache,'TVs\\').decode("utf-8")
            cConfig().setSetting('Library_folder_TVs',self.__sTVFolder)
        if not xbmcvfs.exists(self.__sTVFolder):
                xbmcvfs.mkdir(self.__sTVFolder)

        self.__sTitle = ''

    def setLibrary(self):
        oInputParameterHandler = cInputParameterHandler()

        dialog = xbmcgui.Dialog()
        ret = dialog.select('Selectionner une categorie',['Film','Serie'])
        if ret == 0:
            sCat = '1'
        elif ret == -1:
            return
        else:
            sCat = '2'

        sUrl = oInputParameterHandler.getValue('siteUrl')
        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sFileName = oInputParameterHandler.getValue('sFileName')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')

        #cConfig().log(oInputParameterHandler.getAllParameter())

        sMediaUrl = urllib.quote(sMediaUrl)

        sLink = 'plugin://plugin.video.vstream/?function=play&site=cHosterGui&sFileName=' + sFileName + '&sMediaUrl=' + sMediaUrl + '&sHosterIdentifier=' + sHosterIdentifier

        sTitle = sFileName

        folder = self.__sMovieFolder

        #film
        if sCat == '1':
            folder = self.__sMovieFolder

            sTitle = cUtil().CleanName(sTitle)
            sTitle = cGui().showKeyBoard(sTitle)

            try:
                # folder = folder + '/' + sTitle + '/'

                # if not os.path.exists(folder):
                    # os.mkdir(folder)

                self.MakeFile(folder,sTitle,sLink)
                cConfig().showInfo('vStream', 'Element rajouté a la librairie')
                #xbmc.executebuiltin('UpdateLibrary(video, '+ folder + ')')
            except:
                cConfig().showInfo('Erreur', 'Rajout impossible')

        #serie
        elif sCat == '2':
            folder = self.__sTVFolder

            sTitle = cUtil().FormatSerie(sTitle)
            sTitle = cUtil().CleanName(sTitle)
            sTitleGlobal = re.sub('((?:[s|e][0-9]+){1,2})','',sTitle)
            if sTitleGlobal.endswith(' '):
                sTitleGlobal = sTitleGlobal[:-1]

            try:
                #print folder

                if sTitleGlobal.endswith('FINAL'):
                     sTitleGlobal = sTitleGlobal[:-5]

                folder2 = folder + '/' + sTitleGlobal + '/'

                if not os.path.exists(folder2):
                    os.mkdir(folder2)

                self.MakeFile(folder2,sTitle,sLink)
                cConfig().showInfo('vStream', 'Element rajouté a la librairie')
                #xbmc.executebuiltin('UpdateLibrary(video, '+ folder + ')')
            except:
                cConfig().showInfo('Erreur', 'Rajout impossible')


    def MakeFile(self,folder,name,content):
        stream = os.path.join(folder, str(name) + '.strm')
        f = open(stream, 'w')
        f.write(str(content))
        f.close()

    def getLibrary(self):
        xbmc.executebuiltin("Container.Update(special://userdata/addon_data/plugin.video.vstream/)")
        return True


    def Delfile(self):
        oInputParameterHandler = cInputParameterHandler()
        sFile = oInputParameterHandler.getValue('sFile')

        os.remove(sFile)

        runClean = xbmcgui.Dialog().yesno("Fichier supprime","Voulez vous mettre a jour la librairie maintenant (non conseille)")
        if(not runClean):
            return

        xbmc.executebuiltin("CleanLibrary(video)")

    def ShowContent(self):
        oInputParameterHandler = cInputParameterHandler()
        sFolder = oInputParameterHandler.getValue('folder')
        xbmc.executebuiltin("Container.Update(" + sFolder + ")")
