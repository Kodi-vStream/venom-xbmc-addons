import os
import sys
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import unicodedata

DIALOG2 = None

#-----------------------
#     Cookies gestion
#------------------------

class GestionCookie():
    PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo("profile")).decode("utf-8")

    def DeleteCookie(self,Domain):
        file = os.path.join(self.PathCache,'Cookie_'+ str(Domain) +'.txt')
        os.remove(os.path.join(self.PathCache,file))

    def SaveCookie(self,Domain,data):
        Name = os.path.join(self.PathCache,'Cookie_'+ str(Domain) +'.txt')

        #save it
        file = open(Name,'w')
        file.write(data)

        file.close()

    def Readcookie(self,Domain):
        Name = os.path.join(self.PathCache,'Cookie_'+ str(Domain) +'.txt')

        try:
            file = open(Name,'r')
            data = file.read()
            file.close()
        except:
            return ''

        return data

    def AddCookies(self):
        cookies = self.Readcookie(self.__sHosterIdentifier)
        return 'Cookie=' + cookies


#-------------------------------
#     Configuration gestion
#-------------------------------

class cConfig():

    COUNT = 0
    ERROR = []


    def __check(self):
        try:
            import xbmcaddon
            self.__bIsDharma = True
        except ImportError:
            self.__bIsDharma = False

        try:
            version = xbmc.getInfoLabel('system.buildversion')
            if version[0:2] >= "17":
                self.__bIsKrypton = True
            else :
                self.__bIsKrypton = False
        except:
            self.__bIsKrypton = False


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
            self.__sFileFav = os.path.join(self.__oCache,'favourite.db').decode("utf-8")
            self.__sFileDB = os.path.join(self.__oCache,'vstream.db').decode("utf-8")
            self.__sFileCache = os.path.join(self.__oCache,'video_cache.db').decode("utf-8")


    def isDharma(self):
        return self.__bIsDharma

    def isKrypton(self):
        return self.__bIsKrypton

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

    def getFileCache(self):
        return self.__sFileCache

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
	global DIALOG2
        if DIALOG2 == None:
            oDialog = xbmcgui.DialogProgress()
            oDialog.create(sSite)
            DIALOG2 = oDialog
            return oDialog
        else: return DIALOG2

    def updateDialog(self, dialog, total):
        if xbmcgui.Window(10101).getProperty('search') != 'true':
            iPercent = int(float(cConfig.COUNT * 100) / total)
            dialog.update(iPercent, 'Chargement: '+str(cConfig.COUNT)+'/'+str(total))
            cConfig.COUNT += 1

    def updateDialogSearch(self, dialog, total, site, resetCount = False):

        if (resetCount == True):
            cConfig.COUNT=0

        iPercent = int(float(cConfig.COUNT * 100) / total)
        dialog.update(iPercent, 'Chargement: '+str(site))
        cConfig.COUNT += 1

    def updateDialog2(self, dialog, label = ''):
        dialog.update(0, 'Chargement: '+str(label))

    def finishDialog(self, dialog):
        if xbmcgui.Window(10101).getProperty('search') != 'true':
            dialog.close()
            xbmc.log('\t[PLUGIN] Vstream: close dialog')
            del dialog
            return False

    def showInfo(self, sTitle, sDescription, iSeconds=0,sound = True):
        if (self.__bIsDharma == False):
            return

        if (iSeconds == 0):
                iSeconds = 1000
        else:
                iSeconds = iSeconds * 1000

        if self.getSetting('Block_Noti_sound') == 'true':
            sound = False

        xbmcgui.Dialog().notification(str(sTitle), str(sDescription),self.__sIcon,iSeconds,sound)
        #xbmc.executebuiltin("Notification(%s,%s,%s,%s)" % (str(sTitle), (str(sDescription)), iSeconds, self.__sIcon))

    def update(self):
        xbmc.executebuiltin("Container.Refresh")

    def show_busy_dialog():
        xbmc.executebuiltin('ActivateWindow(busydialog)')

    def hide_busy_dialog():
        xbmc.executebuiltin('Dialog.Close(busydialog)')
        while xbmc.getCondVisibility('Window.IsActive(busydialog)'):
            xbmc.sleep(100)

    def error(self, e):
        xbmc.executebuiltin("Notification(%s,%s,%s,%s)" % ('Vstream', ('Erreur: '+str(e)), '10000', self.__sIcon))
        xbmc.log('\t[PLUGIN] Vstream Erreur: '+str(e))
        #cConfig().ERROR.append(e)

    def log(self, e):
        xbmc.log('\t[PLUGIN] Vstream: '+str(e), xbmc.LOGNOTICE)

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

        API = self.getSetting('api_tmdb')

        #Presence de l'addon ExtendedInfo ?
        try:
            if (xbmcaddon.Addon('script.extendedinfo') and self.getSetting('extendedinfo-view') == 'true'):
                if num == "2":
                    self.showInfo('vStream', 'Lancement de ExtendInfo')
                    xbmc.executebuiltin('XBMC.RunScript(script.extendedinfo, info=extendedtvinfo, name=%s)' % sFileName)
                    return
                elif num == "1":
                    self.showInfo('vStream', 'Lancement de ExtendInfo')
                    xbmc.executebuiltin('XBMC.RunScript(script.extendedinfo, info=extendedinfo, name=%s)' % sFileName)
                    return
        except:
            pass

        #Sinon on gere par Vstream via la lib TMDB
        if num == "1":
            try:
                from resources.lib.tmdb import cTMDb
                grab = cTMDb(api_key=self.getSetting('api_tmdb'))
                meta = grab.get_meta('movie',sFileName, '', xbmc.getInfoLabel('ListItem.Property(TmdbId)'))
            except:
                pass
        elif num == "2":
            try:
                from resources.lib.tmdb import cTMDb
                grab = cTMDb(api_key=self.getSetting('api_tmdb'))
                meta = grab.get_meta('tvshow',sFileName, '', xbmc.getInfoLabel('ListItem.Property(TmdbId)'))
            except:
                pass

        #si rien ne marche
        if (not meta['imdb_id'] and not ['tmdb_id'] and not ['tvdb_id']):
            #dialog par defaut
            #xbmc.executebuiltin("Action(Info)")
            #fenetre d'erreur
            self.showInfo('Vstream', self.getlanguage(30204))

            return

        #affichage du dialog perso
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
                color = cConfig().getSetting('deco_color')
                xbmcgui.Window(10000).setProperty('color', color)

                self.getControl(50).setVisible(False)
                self.getControl(50).reset()
                self.getControl(5500).setVisible(False)
                listitems = []
                try:
                    for slabel, slabel2, sicon, sid in meta['cast']:
                        listitem = xbmcgui.ListItem(label = slabel, label2=slabel2, iconImage=sicon)
                    #listitem.setInfo('video', {'Title': 'test', 'RatingAndVotes':'6.8'})
                        listitem.setProperty('id', str(sid))
                        listitems.append(listitem)
                    self.getControl(50).addItems(listitems)
                except: pass
                #title
                #self.getControl(1).setLabel(meta['title'])
                meta['title'] = sTitle

                #self.getControl(49).setVisible(True)
                #self.getControl(2).setImage(meta['cover_url'])
                #self.getControl(3).setLabel(meta['rating'])
                for e in meta:
                    property = 'ListItem.%s' %(e)
                    if isinstance(meta[e], unicode):
                        xbmcgui.Window(10000).setProperty(property, meta[e].encode('utf-8'))
                    else:
                        xbmcgui.Window(10000).setProperty(property, str(meta[e]))


            def credit(self, meta=""):
                self.getControl(5200).reset()
                listitems = []

                try:
                    for i in meta:
                        try:
                            sTitle = unicodedata.normalize('NFKD', i['title']).encode('ascii','ignore')
                        except: sTitle = "Aucune information"
                        try:
                            sThumbnail = 'https://image.tmdb.org/t/p/w396' + i['poster_path']
                        except:
                            sThumbnail = ''
                        sId = i['id']

                        listitem = xbmcgui.ListItem(label = sTitle, iconImage=sThumbnail)
                        #listitem.setInfo('video', {'Title': 'test', 'RatingAndVotes':'6.8'})
                        #listitem.setProperty('id', str(sId))
                        listitems.append(listitem)
                    self.getControl(5200).addItems(listitems)
                except: pass
                self.getControl(5500).setVisible(True)
                self.setFocusId(5200)
                #self.setFocus(self.getControl(5200))


            def person(self, sid=""):
                from resources.lib.tmdb import cTMDb
                grab = cTMDb(api_key=API, lang='en')
                sUrl = 'person/' + str(sid)
                meta = grab.getUrl(sUrl)

                listitems = []

                try:
                    try:
                        sTitle = unicodedata.normalize('NFKD', meta['name']).encode('ascii','ignore')
                    except: sTitle = "Aucune information"
                    #xbmcgui.Window(10000).setProperty('person_name', sTitle)
                    try:
                        sThumbnail = 'https://image.tmdb.org/t/p/w396' + meta['profile_path']
                    except:
                        sThumbnail = ''
                    sId = meta['id']


                    bio = meta['biography'].replace('\n\n', '[CR]').replace('\n', '[CR]')

                    #self.getControl(5300).setLabel('[COLOR gold]test[/COLOR]')
                    #print meta

                    xbmcgui.Window(10000).setProperty('biography', bio)
                    xbmcgui.Window(10000).setProperty('birthday', meta['birthday'])
                    xbmcgui.Window(10000).setProperty('place_of_birth', meta['place_of_birth'])
                    xbmcgui.Window(10000).setProperty('deathday', meta['deathday'])

                    #self.getControl(20).setVisible(True)
                except: pass


                #description
                #self.getControl(400).setText(meta['plot'])

            def onClick(self, controlId):
                if controlId == 5:
                    self.getControl(400).setVisible(False)
                    self.getControl(50).setVisible(True)
                    self.setFocusId(20)
                    return
                elif controlId == 20:
                    self.getControl(50).setVisible(False)
                    self.getControl(400).setVisible(True)
                    self.setFocusId(5)
                    return
                elif controlId == 7:
                    return
                elif controlId == 11:
                    from resources.lib.ba import cShowBA
                    cBA = cShowBA()
                    cBA.SetSearch(sFileName)
                    cBA.SearchBA()
                    self.close()
                    return
                elif controlId == 30:
                    self.close()
                    return
                elif controlId == 50:
                    #print self.getControl(50).ListItem.Property('id')
                    xbmcgui.Window(10000).setProperty('nav', '1')
                    item = self.getControl(50).getSelectedItem()
                    sid = item.getProperty('id')

                    from resources.lib.tmdb import cTMDb
                    grab = cTMDb(api_key=API)
                    sUrl = 'person/' + str(sid) + '/movie_credits'
                    try:
                        meta = grab.getUrl(sUrl)
                        meta = meta['cast']
                        self.credit(meta)
                    except: return
                    #self.getControl(50).setVisible(True)
                #click sur similaire
                elif controlId == 9:
                    #print self.getControl(9000).ListItem.tmdb_id
                    sid = xbmcgui.Window(10000).getProperty("ListItem.tmdb_id")
                    xbmcgui.Window(10000).setProperty('nav', '2')

                    from resources.lib.tmdb import cTMDb
                    grab = cTMDb(api_key=API)
                    sUrl = 'movie/%s/similar' % str(sid)
                    try:
                        meta = grab.getUrl(sUrl)
                        meta = meta['results']
                        self.credit(meta)
                    except: return
                #click sur recommendations
                elif controlId == 13:
                    #print self.getControl(9000).ListItem.tmdb_id
                    sid = xbmcgui.Window(10000).getProperty("ListItem.tmdb_id")
                    xbmcgui.Window(10000).setProperty('nav', '3')

                    from resources.lib.tmdb import cTMDb
                    grab = cTMDb(api_key=API)
                    sUrl = 'movie/%s/recommendations' % str(sid)
                    try:
                        meta = grab.getUrl(sUrl)
                        meta = meta['results']
                        self.credit(meta)
                    except: return

                elif controlId == 5200:
                #click sur un film acteur
                    import sys
                    from resources.lib.util import cUtil
                    item = self.getControl(5200).getSelectedItem()
                    sTitle = item.getLabel()

                    try:
                        sTitle = sTitle.encode("utf-8")
                        sTitle = cUtil().CleanName(sTitle)
                    except: return

                    sTest = '%s?site=globalSearch&searchtext=%s&sCat=1' % (sys.argv[0], sTitle)
                    xbmc.executebuiltin('XBMC.Container.Update(%s)' % sTest )
                    self.close()
                    return

                #dans le futur permet de retourne le texte du film
                # elif controlId == 5200:
                #     item = self.getControl(5200).getSelectedItem()
                #     sid = item.getLabel()
                #     print sid
                #     return

            def onFocus(self, controlId):
                self.controlId = controlId
                if controlId != 5200:
                    #self.getControl(5500).reset()
                    self.getControl(5500).setVisible(False)
                if controlId == 50:
                    item = self.getControl(50).getSelectedItem()
                    sid = item.getProperty('id')
                    self.person(sid)

            def _close_dialog( self ):
                self.close()

            def onAction( self, action ):
                if action.getId() in ( 104, 105, 1, 2):
                    if self.controlId == 50:
                        item = self.getControl(50).getSelectedItem()
                        sid = item.getProperty('id')
                        self.person(sid)

                if action.getId() in ( 9, 10, 11, 30, 92, 216, 247, 257, 275, 61467, 61448, ):
                    self.close()

        wd = XMLDialog('DialogInfo.xml', self.__oPath.decode("utf-8") , 'default', '720p')
        wd.doModal()
        del wd
