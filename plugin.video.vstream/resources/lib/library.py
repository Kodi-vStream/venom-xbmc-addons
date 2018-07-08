#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil
from resources.lib.comaddon import addon, dialog, VSlog, xbmc

import xbmcvfs
import urllib,re


SITE_IDENTIFIER = 'cLibrary'
SITE_NAME = 'Library'

#sources.xml

class cLibrary:

    ADDON = addon()
    DIALOG = dialog()

    def __init__(self):
        self.__sMovieFolder = xbmc.translatePath(self.ADDON.getSetting('Library_folder_Movies')).decode("utf-8")
        self.__sTVFolder = xbmc.translatePath(self.ADDON.getSetting('Library_folder_TVs')).decode("utf-8")

        if not self.__sMovieFolder:
            #PathCache = cConfig().getSettingCache()
            #self.__sMovieFolder = os.path.join(PathCache,'Movies\\').decode("utf-8")
            self.__sMovieFolder = "special://userdata/addon_data/plugin.video.vstream/Films/"
            self.ADDON.setSetting('Library_folder_Movies',self.__sMovieFolder)
        if not xbmcvfs.exists(self.__sMovieFolder):
                xbmcvfs.mkdir(self.__sMovieFolder)

        if not self.__sTVFolder:
            #PathCache = cConfig().getSettingCache()
            #self.__sTVFolder = os.path.join(PathCache,'TVs\\').decode("utf-8")
            self.__sTVFolder = "special://userdata/addon_data/plugin.video.vstream/Series"
            Self.ADDON.setSetting('Library_folder_TVs',self.__sTVFolder)
        if not xbmcvfs.exists(self.__sTVFolder):
                xbmcvfs.mkdir(self.__sTVFolder)

        self.__sTitle = ''

    def setLibrary(self):
        oInputParameterHandler = cInputParameterHandler()

        ret = self.DIALOG.select('Selectionner une categorie',['Film','Serie'])
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

        sMediaUrl = urllib.quote_plus(sMediaUrl)
        sFileName = urllib.quote_plus(sFileName)

        sLink = 'plugin://plugin.video.vstream/?function=play&site=cHosterGui&sFileName=' + sFileName + '&sMediaUrl=' + sMediaUrl + '&sHosterIdentifier=' + sHosterIdentifier

        sTitle = sFileName

        folder = self.__sMovieFolder

        #film
        if sCat == '1':
            folder = self.__sMovieFolder

            sTitle = cUtil().CleanName(sTitle)
            sTitle =  cGui().showKeyBoard(sTitle)

            try:
                # folder = folder + '/' + sTitle + '/'

                # if not os.path.exists(folder):
                    # os.mkdir(folder)

                self.MakeFile(folder,sTitle,sLink)
                #xbmc.executebuiltin('UpdateLibrary(video, '+ folder + ')')
            except:
                self.DIALOG.VSinfo('Rajout impossible')

        #serie
        elif sCat == '2':
            folder = self.__sTVFolder

            sTitle = cUtil().FormatSerie(sTitle)
            sTitle = cUtil().CleanName(sTitle)
            sTitle =  cGui().showKeyBoard(sTitle)
            
            sTitleGlobal = re.sub('((?:[s|e][0-9]+){1,2})','',sTitle)
            
            if sTitleGlobal.endswith(' '):
                sTitleGlobal = sTitleGlobal[:-1]
            if sTitleGlobal.endswith('FINAL'):
                 sTitleGlobal = sTitleGlobal[:-5]

            try:
                #print folder

                folder2 = folder + '/' + sTitleGlobal + '/'

                #if not os.path.exists(folder2):
                    #os.mkdir(folder2)
                if not xbmcvfs.exists(folder2):
                    xbmcvfs.mkdir(folder2)

                self.MakeFile(folder2,sTitle,sLink)
                #xbmc.executebuiltin('UpdateLibrary(video, '+ folder + ')')
            except:
                self.DIALOG.VSinfo('Rajout impossible')


    def MakeFile(self,folder,name,content):
        #stream = os.path.join(folder, str(name) + '.strm')
        stream = "%s%s.strm" % (folder, str(name))
        #f = open(stream, 'w')
        f = xbmcvfs.File(stream, 'w', True)
        result = f.write(str(content))
        f.close()
        if result:
            self.DIALOG.VSinfo('Element rajouté a la librairie')
        else:
            self.DIALOG.VSinfo('Rajout impossible')


    def getLibrary(self):
        xbmc.executebuiltin("Container.Update(special://userdata/addon_data/plugin.video.vstream/)")
        return True


    def Delfile(self):
        oInputParameterHandler = cInputParameterHandler()
        sFile = oInputParameterHandler.getValue('sFile')

        #os.remove(sFile)
        xbmcvfs.delete(sFile)

        runClean = self.DIALOG.VSyesno("Voulez vous mettre a jour la librairie maintenant (non conseille)", "Fichier supprime")
        if(not runClean):
            return

        xbmc.executebuiltin("CleanLibrary(video)")

    def ShowContent(self):
        oInputParameterHandler = cInputParameterHandler()
        sFolder = oInputParameterHandler.getValue('folder')
        xbmc.executebuiltin("Container.Update(" + sFolder + ")")
