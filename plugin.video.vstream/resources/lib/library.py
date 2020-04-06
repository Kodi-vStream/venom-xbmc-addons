#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
# from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
# from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil, QuotePlus
from resources.lib.comaddon import addon, dialog, xbmc#, window, VSlog
import xbmcvfs#, re

SITE_IDENTIFIER = 'cLibrary'
SITE_NAME = 'Library'

#sources.xml

class cLibrary:
    ADDON = addon()
    DIALOG = dialog()

    def __init__(self):
        self.__sMovieFolder = self.ADDON.getSetting('Library_folder_Movies')
        self.__sTVFolder = self.ADDON.getSetting('Library_folder_TVs')

        if not self.__sMovieFolder:
            #PathCache = cConfig().getSettingCache()
            #self.__sMovieFolder = os.path.join(PathCache, 'Movies\\').decode('utf-8')
            self.__sMovieFolder = 'special://userdata/addon_data/plugin.video.vstream/Films'
            self.ADDON.setSetting('Library_folder_Movies', self.__sMovieFolder)
        if not xbmcvfs.exists(self.__sMovieFolder):
            xbmcvfs.mkdir(self.__sMovieFolder)

        if not self.__sTVFolder:
            #PathCache = cConfig().getSettingCache()
            #self.__sTVFolder = os.path.join(PathCache, 'TVs\\').decode('utf-8')
            self.__sTVFolder = 'special://userdata/addon_data/plugin.video.vstream/Series'
            Self.ADDON.setSetting('Library_folder_TVs', self.__sTVFolder)
        if not xbmcvfs.exists(self.__sTVFolder):
            xbmcvfs.mkdir(self.__sTVFolder)

        self.__sTitle = ''

    def setLibrary(self):
        oInputParameterHandler = cInputParameterHandler()
        # sUrl = oInputParameterHandler.getValue('siteUrl')
        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sFileName = oInputParameterHandler.getValue('sFileName')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')

        ret = self.DIALOG.select('Sélectionner une catégorie', ['Film', 'Série'])
        if ret == 0:
            sCat = '1'
        elif ret == -1:
            return
        else:
            sCat = '2'

        #cConfig().log(oInputParameterHandler.getAllParameter())

        sMediaUrl = QuotePlus(sMediaUrl)
        sFileName = QuotePlus(sFileName)

        sLink = 'plugin://plugin.video.vstream/?function=play&site=cHosterGui&sFileName=' + sFileName + '&sMediaUrl=' + sMediaUrl + '&sHosterIdentifier=' + sHosterIdentifier

        sTitle = sFileName

        #folder = self.__sMovieFolder

        if sCat == '1':#film
            #folder = self.__sMovieFolder

            sTitle = cUtil().CleanName(sTitle)
            sTitle =  self.showKeyBoard(sTitle, 'Nom du dossier et du fichier')

            try:
                #folder = '%s%s/' % (folder, sTitle)
                sPath = '/'.join([self.__sMovieFolder, sTitle])

                # if not os.path.exists(folder):
                    # os.mkdir(folder)
                if not xbmcvfs.exists(sPath):
                    xbmcvfs.mkdir(sPath)

                self.MakeFile(sPath,sTitle,sLink)
                #xbmc.executebuiltin('UpdateLibrary(video, ' + folder + ')')
            except:
                self.DIALOG.VSinfo('Rajout impossible')

        elif sCat == '2':#serie

            #sTitle = cUtil().FormatSerie(sTitle)
            sTitle = cUtil().CleanName(sTitle)
            sFTitle =  self.showKeyBoard(sTitle, 'Recommandé Nomdeserie/Saison00')

            #sTitleGlobal = re.sub('((?:[s|e][0-9]+){1,2})', '', sTitle)

            # if sTitleGlobal.endswith(' '):
            #     sTitleGlobal = sTitleGlobal[:-1]
            # if sTitleGlobal.endswith('FINAL'):
            #      sTitleGlobal = sTitleGlobal[:-5]

            try:
                #print folder

                #folder2 = folder + '/' + sTitleGlobal + '/'
                #folder2 = '%s%s/' % (self.__sTVFolder, sTitleGlobal)
                sPath = '/'.join([self.__sTVFolder, sFTitle])

                #if not os.path.exists(folder2):
                    #os.mkdir(folder2)
                if not xbmcvfs.exists(sPath):
                    xbmcvfs.mkdir(sPath)

                sTitle =  self.showKeyBoard(sTitle, 'Recommandé NomdeserieS00E00')

                self.MakeFile(sPath,sTitle,sLink)
                #xbmc.executebuiltin('UpdateLibrary(video, ' + folder + ')')
            except:
                self.DIALOG.VSinfo('Rajout impossible')


    def MakeFile(self, folder, name, content):
        #stream = os.path.join(folder, str(name) + '.strm')
        #stream = '%s%s.strm' % (folder, str(name))
        stream = '/'.join([folder, str(name)]) + '.strm'
        #f = open(stream, 'w')
        f = xbmcvfs.File(stream, 'w')
        result = f.write(str(content))
        f.close()
        if result:
            self.DIALOG.VSinfo('Elément rajouté à la librairie')
        else:
            self.DIALOG.VSinfo('Rajout impossible')


    def getLibrary(self):
        xbmc.executebuiltin('Container.Update(special://userdata/addon_data/plugin.video.vstream/)', True)
        #xbmc.executebuiltin('ActivateWindow(Videos, 'special://userdata/addon_data/plugin.video.vstream/')', True)
        return True


    def Delfile(self):
        oInputParameterHandler = cInputParameterHandler()
        sFile = oInputParameterHandler.getValue('sFile')

        #os.remove(sFile)
        xbmcvfs.delete(sFile)

        runClean = self.DIALOG.VSyesno('Voulez vous mettre à jour la librairie maintenant (non conseillé)', 'Fichier supprimé')
        if(not runClean):
            return

        xbmc.executebuiltin('CleanLibrary(video)')

    def ShowContent(self):
        oInputParameterHandler = cInputParameterHandler()
        sFolder = oInputParameterHandler.getValue('folder')
        xbmc.executebuiltin('Container.Update(' + sFolder + ')')

    def showKeyBoard(self, sDefaultText = '', Heading = ''):
        keyboard = xbmc.Keyboard(sDefaultText)
        keyboard.setHeading(Heading) #optional
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            sSearchText = keyboard.getText()
            if (len(sSearchText)) > 0:
                return sSearchText

        return False
