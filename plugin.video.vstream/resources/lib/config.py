import os
import sys
import xbmc
import xbmcplugin
import xbmcgui

class cConfig():

    COUNT = 0
    ERROR = []


    def __check(self):
        try:
            import xbmcaddon           
            self.__bIsDharma = True            
        except ImportError:
            self.__bIsDharma = False

    def __init__(self):
        self.__check()

        if (self.__bIsDharma):
            import xbmcaddon
            self.__oSettings = xbmcaddon.Addon(self.getPluginId())
            self.__aLanguage = self.__oSettings.getLocalizedString
            self.__setSetting = self.__oSettings.setSetting
            self.__getSetting = self.__oSettings.getSetting
            self.__oVersion = self.__oSettings.getAddonInfo("version")
            self.__oId = self.__oSettings.getAddonInfo("id")
            self.__oPath = self.__oSettings.getAddonInfo("path")
            self.__oName = self.__oSettings.getAddonInfo("name")
            self.__oCache = xbmc.translatePath(self.__oSettings.getAddonInfo("profile"))
            self.__sRootArt = os.path.join(self.__oPath, 'resources' , 'art', '')
            self.__sIcon = os.path.join(self.__oPath,'resources', 'art','icon.png')
            self.__sFanart = os.path.join(self.__oPath,'resources','art','fanart.jpg')
            self.__sFileFav = os.path.join(self.__oCache,'favourite.db')
            self.__sFileDB = os.path.join(self.__oCache,'vstream.db')


    def isDharma(self):
        return self.__bIsDharma

    def getPluginId(self):
        return 'plugin.video.vstream'
        
    def getAddonId(self):
        return self.__oId
    
    def getSettingCache(self):
        return self.__oCache

    def getAddonPath(self):
        return self.__oPath

    def getRootArt(self):
        return self.__sRootArt

    def getAddonVersion(self):
        return self.__oVersion
    
    def getFileFav(self):
        return self.__sFileFav
    
    def getFileDB(self):
        return self.__sFileDB

    def getFileIcon(self):
        return self.__sIcon

    def getFileFanart(self):
        return self.__sFanart

    def showSettingsWindow(self):
        if (self.__bIsDharma):
            self.__oSettings.openSettings()
        else:
            try:
                xbmcplugin.openSettings( sys.argv[ 0 ] )
            except:
		pass

    def getSetting(self, sName):
        if (self.__bIsDharma):
            return self.__oSettings.getSetting(sName)
        else:
            try:                
                return xbmcplugin.getSetting(sName)
            except:
		return ''
        
    def html_decode(self, s):
        htmlCodes = [
        ["'", "&#39;"],
        ["'", "&#039;"],
        ["<", "&lt;"],
        [">", "&gt;"],
        [" ", "&quot;"],
        ]
        for code in htmlCodes:
            s = s.replace(code[1], code[0])
        return s

    def setSetting(self, sName, sValue):
        if (self.__bIsDharma):
            return self.__oSettings.setSetting(sName, sValue)
        else:
            return xbmcplugin.setSetting(sName, sValue)
        return

    def getlanguage(self, sCode):
        if (self.__bIsDharma):
            return self.__aLanguage(sCode).encode("utf-8")
        else:
            try:		
		return xbmc.getLocalizedString(sCode).encode("utf-8")
            except:
		return ''
        
    def showKeyBoard(self, sDefaultText=''):
        keyboard = xbmc.Keyboard(sDefaultText)
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            sSearchText = keyboard.getText()
            if (len(sSearchText)) > 0:
                return sSearchText

        return False

    def createDialogOK(self, label):
        oDialog = xbmcgui.Dialog()
        oDialog.ok('vStream', label)  
        return oDialog
        
    def createDialogYesNo(self, label):
        oDialog = xbmcgui.Dialog()
        qst = oDialog.yesno("vStream", label)
        return qst
        
    def createDialog(self, sSite):
        oDialog = xbmcgui.DialogProgress()
        oDialog.create(sSite)  
        return oDialog

    def updateDialog(self, dialog, total):
        iPercent = int(float(cConfig.COUNT * 100) / total)
        dialog.update(iPercent, 'Chargement: '+str(cConfig.COUNT)+'/'+str(total))
        cConfig.COUNT += 1

    def updateDialog2(self, dialog, label = ''):
        dialog.update(0, 'Chargement: '+str(label))

    def finishDialog(self, dialog):
        dialog.close()
        del dialog
        return False
        
    def showInfo(self, sTitle, sDescription, iSeconds=0):
        if (self.__bIsDharma == False):
            return

        if (iSeconds == 0):
                iSeconds = 1000
        else:
                iSeconds = iSeconds * 1000
        
        xbmc.executebuiltin("Notification(%s,%s,%s,%s)" % (str(sTitle), (str(sDescription)), iSeconds, self.__sIcon))
        
    def update(self):
        xbmc.executebuiltin("Container.Refresh")


    def error(self, e):
        xbmc.executebuiltin("Notification(%s,%s,%s,%s)" % ('Vstream', ('Erreur: '+str(e)), '10000', self.__sIcon))
        xbmc.log('\t[PLUGIN] Vstream Erreur: '+str(e))
        #cConfig().ERROR.append(e)

    def log(self, e):
        xbmc.log('\t[PLUGIN] Vstream: '+str(e))
    
    def openerror(self):
        xbmc.executebuiltin( "ActivateWindow(10147)" )
        self.win = xbmcgui.Window(10147)
        xbmc.sleep( 500 )
        value = ''
        for text in cConfig().ERROR:
            text = text.replace(',', '\n')
            value += '\n'+text+'\n'
        
        self.win.getControl(1).setLabel("vStream popup Erreur")
        self.win.getControl(5).setText(str(value))
        
    def TextBoxes(self, heading, anounce):
        class TextBox():
            # constants
            WINDOW = 10147
            CONTROL_LABEL = 1
            CONTROL_TEXTBOX = 5

            def __init__( self, *args, **kwargs):
                # activate the text viewer window
                xbmc.executebuiltin( "ActivateWindow(%d)" % ( self.WINDOW, ) )
                # get window
                self.win = xbmcgui.Window( self.WINDOW )
                # give window time to initialize
                xbmc.sleep( 500 )
                self.setControls()

            def setControls( self ):
                # set heading
                self.win.getControl( self.CONTROL_LABEL ).setLabel(heading)
                try:
                    f = open(anounce)
                    text = f.read()
                except: text=anounce
                self.win.getControl( self.CONTROL_TEXTBOX ).setText(text)
                return
        TextBox()
        
    def WindowsBoxes(self, sTitle, sFileName, num,year = ''):
        
        if self.getSetting('meta-view') == 'true':
            xbmc.executebuiltin("Action(Info)")
            return
        
        if num == "1":
            try:
                from metahandler import metahandlers
                grab = metahandlers.MetaData(preparezip=False, tmdb_api_key='92ab39516970ab9d86396866456ec9b6')
                meta = grab.get_meta('movie',sFileName)
            except:         
                xbmc.executebuiltin("Action(Info)")
                return
        elif num == "2":
            try:
                from metahandler import metahandlers
                grab = metahandlers.MetaData(preparezip=False, tmdb_api_key='92ab39516970ab9d86396866456ec9b6')
                meta = grab.get_meta('tvshow',sFileName)
            except:
                xbmc.executebuiltin("Action(Info)")
                return
        

        if (not meta['imdb_id']):
            xbmc.executebuiltin("Action(Info)")
            return
                
        class XMLDialog(xbmcgui.WindowXMLDialog):
            """
            Dialog class that asks user about rating of movie.
            """
            def __init__(self, *args, **kwargs):
                xbmcgui.WindowXMLDialog.__init__( self )
                pass

            # def message(self, message):
                # """
                # Shows xbmc dialog with OK and message.
                # """
                # dialog = xbmcgui.Dialog()
                # dialog.ok(" My message title", message)
                # self.close()

            def onInit(self):
                #par default le resumer#                    
                self.getControl(50).setVisible(False)
                #title
                #self.getControl(1).setLabel(meta['title'])
                meta['title'] = sTitle
                
                self.getControl(49).setVisible(True)
                #self.getControl(2).setImage(meta['cover_url'])
                #self.getControl(3).setLabel(meta['rating'])
                for e in meta:
                    property = 'ListItem.%s' %(e)
                    if isinstance(meta[e], unicode):
                        xbmcgui.Window(10000).setProperty(property, meta[e].encode('utf-8'))
                    else:
                        if (property == "ListItem.cast"):
                            cast = ''
                            try:
                                for real, act in meta[e]:
                                    cast += real+' est '+act+',  ' 
                                xbmcgui.Window(10000).setProperty(property, cast.encode('utf-8'))
                            except:
                                for act in meta[e]:
                                    cast += act+', '
                                xbmcgui.Window(10000).setProperty(property, str(cast))
                                
                        else:
                            xbmcgui.Window(10000).setProperty(property, str(meta[e]))
                
                

                
                #description
                #self.getControl(400).setText(meta['plot'])

            def onClick(self, controlId):
                if controlId == 5:
                    self.getControl(400).setVisible(False)
                    self.getControl(50).setVisible(True)
                    return
                elif controlId == 20:
                    self.getControl(50).setVisible(False)
                    self.getControl(400).setVisible(True)
                    return
                elif controlId == 15:
                    return
                self.close()

            def onFocus(self, controlId):
                self.controlId = controlId
                
            def _close_dialog( self ):
                self.close()

            def onAction( self, action ):
                if action.getId() in ( 9, 10, 92, 216, 247, 257, 275, 61467, 61448, ):
                    self.close()
          
        wd = XMLDialog('DialogInfo.xml', self.__oPath, 'default', '720p')
        wd.doModal()
        del wd

        
        
        
