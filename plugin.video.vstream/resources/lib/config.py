#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import addon, dialog, window, listitem, xbmc, xbmcgui
from resources.lib.tmdb import cTMDb

#import os
#import xbmcaddon
import unicodedata
import xbmcvfs

#-----------------------
#     Cookies gestion
#------------------------

class GestionCookie():
    #PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo('profile')).decode('utf-8')
    PathCache = 'special://userdata/addon_data/plugin.video.vstream'

    def DeleteCookie(self, Domain):
        #file = os.path.join(self.PathCache, 'Cookie_' + str(Domain) + '.txt')
        Name = '/'.join([self.PathCache, 'cookie_%s.txt']) % (Domain)
        #os.remove(os.path.join(self.PathCache, file))
        xbmcvfs.delete(Name)

    def SaveCookie(self, Domain, data):
        #Name = os.path.join(self.PathCache, 'Cookie_' + str(Domain) + '.txt')
        Name = '/'.join([self.PathCache, 'cookie_%s.txt']) % (Domain)

        #save it
        #file = open(Name, 'w')
        #file.write(data)
        #file.close()

        f = xbmcvfs.File(Name, 'w')
        f.write(data)
        f.close()

    def Readcookie(self, Domain):
        #Name = os.path.join(self.PathCache, 'Cookie_' + str(Domain) + '.txt')
        Name = '/'.join([self.PathCache, 'cookie_%s.txt']) % (Domain)

        # try:
        #     file = open(Name,'r')
        #     data = file.read()
        #     file.close()
        # except:
        #     return ''

        try:
            f = xbmcvfs.File(Name)
            data = f.read()
            f.close()
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

    # def __init__(self):

        # import xbmcaddon
        # self.__oSettings = xbmcaddon.Addon(self.getPluginId())
        # self.__aLanguage = self.__oSettings.getLocalizedString
        # self.__setSetting = self.__oSettings.setSetting
        # self.__getSetting = self.__oSettings.getSetting
        # self.__oVersion = self.__oSettings.getAddonInfo('version')
        # self.__oId = self.__oSettings.getAddonInfo('id')
        # self.__oPath = self.__oSettings.getAddonInfo('path')
        # self.__oName = self.__oSettings.getAddonInfo('name')
        # self.__oCache = xbmc.translatePath(self.__oSettings.getAddonInfo('profile'))
        # self.__sRootArt = os.path.join(self.__oPath, 'resources' , 'art', '')
        # self.__sIcon = os.path.join(self.__oPath,'resources', 'art','icon.png')
        # self.__sFanart = os.path.join(self.__oPath,'resources','art','fanart.jpg')
        # self.__sFileFav = os.path.join(self.__oCache,'favourite.db').decode('utf-8')
        # self.__sFileDB = os.path.join(self.__oCache,'vstream.db').decode('utf-8')
        # self.__sFileCache = os.path.join(self.__oCache,'video_cache.db').decode('utf-8')


    def isDharma(self):
        return self.__bIsDharma

    def getSettingCache(self):
        return False

    def getAddonPath(self):
        return False

    def getRootArt(self):
        return False

    def getFileFav(self):
        return False

    def getFileDB(self):
        return False

    def getFileCache(self):
        return False



def WindowsBoxes(sTitle, sFileName, num, year = ''):

    ADDON = addon()
    DIALOG = dialog()

    #Presence de l'addon ExtendedInfo?
    try:
        if (addon('script.extendedinfo') and ADDON.getSetting('extendedinfo-view') == 'true'):
            if num == '2':
                DIALOG.VSinfo('Lancement de ExtendInfo')
                xbmc.executebuiltin('XBMC.RunScript(script.extendedinfo, info=extendedtvinfo, name=%s)' % sFileName)
                return
            elif num == '1':
                DIALOG.VSinfo('Lancement de ExtendInfo')
                xbmc.executebuiltin('XBMC.RunScript(script.extendedinfo, info=extendedinfo, name=%s)' % sFileName)
                return
    except:
        pass

    #Sinon on gere par vStream via la lib TMDB
    if num == '1':
        try:
            grab = cTMDb()
            meta = grab.get_meta('movie', sFileName, '', xbmc.getInfoLabel('ListItem.Property(TmdbId)'))
        except:
            pass
    elif num == '2':
        try:
            grab = cTMDb()
            meta = grab.get_meta('tvshow', sFileName, '', xbmc.getInfoLabel('ListItem.Property(TmdbId)'))
        except:
            pass

    #si rien ne marche
    if (not meta['imdb_id'] and not ['tmdb_id'] and not ['tvdb_id']):
        #dialog par defaut
        #xbmc.executebuiltin('Action(Info)')
        #fenetre d'erreur
        DIALOG.VSinfo(ADDON.VSlang(30204))

        return

    #affichage du dialog perso
    class XMLDialog(xbmcgui.WindowXMLDialog):

        ADDON = addon()
        """
        Dialog class that asks user about rating of movie.
        """
        def __init__(self, *args, **kwargs):
            xbmcgui.WindowXMLDialog.__init__(self)
            pass

        # def message(self, message):
            # """
            # Shows xbmc dialog with OK and message.
            # """
            # dialog = xbmcgui.Dialog()
            # dialog.ok(' My message title', message)
            # self.close()

        def onInit(self):
            #par default le resumer#
            color = ADDON.getSetting('deco_color')
            window(10000).setProperty('color', color)

            self.getControl(50).setVisible(False)
            self.getControl(5200).setVisible(False)
            #synopsis_first
            self.setFocusId(36)

            #self.getControl(50).reset()
            listitems = []
            cast = []

            try:
                for slabel, slabel2, sicon, sid in meta['cast']:
                    listitem_ = listitem(label = slabel, label2 = slabel2, iconImage = sicon)
                #listitem.setInfo('video', {'Title': 'test', 'RatingAndVotes':'6.8'})
                    listitem_.setProperty('id', str(sid))
                    listitems.append(listitem_)
                    cast.append(slabel.encode('ascii', 'ignore'))
                self.getControl(50).addItems(listitems)
                window(10000).setProperty('ListItem.casting', str(cast))
            except:
                pass
            #title
            #self.getControl(1).setLabel(meta['title'])
            meta['title'] = sTitle

            #self.getControl(49).setVisible(True)
            #self.getControl(2).setImage(meta['cover_url'])
            #self.getControl(3).setLabel(meta['rating'])

            for e in meta:
                property = 'ListItem.%s' % (e)
                if isinstance(meta[e], unicode):
                    window(10000).setProperty(property, meta[e].encode('utf-8'))
                else:
                    window(10000).setProperty(property, str(meta[e]))

        def credit(self, meta = ''):
            self.getControl(5200).reset()
            listitems = []

            try:
                for i in meta:
                    try:
                        sTitle = unicodedata.normalize('NFKD', i['title']).encode('ascii', 'ignore')
                    except: sTitle = 'Aucune information'
                    try:
                        sThumbnail = 'https://image.tmdb.org/t/p/w342' + i['poster_path']
                    except:
                        sThumbnail = ''
                    sId = i['id']

                    listitem_ = listitem(label = sTitle, iconImage = sThumbnail)
                    try:
                        listitem_.setInfo('video', {'rating': i['vote_average'].encode('utf-8') })
                    except:
                        listitem_.setInfo('video', {'rating': str(i['vote_average'])})

                    #listitem.setProperty('id', str(sId))
                    listitems.append(listitem_)
                self.getControl(5200).addItems(listitems)

            except:
                pass
            self.getControl(5200).setVisible(True)
            self.setFocusId(5200)
            #self.setFocus(self.getControl(5200))

        def person(self, sid = ''):
            grab = cTMDb(lang = 'en')
            sUrl = 'person/' + str(sid)
            meta = grab.getUrl(sUrl)

            listitems = []

            try:
                try:
                    sTitle = unicodedata.normalize('NFKD', meta['name']).encode('ascii', 'ignore')
                except: sTitle = 'Aucune information'
                #xbmcgui.Window(10000).setProperty('person_name', sTitle)
                try:
                    sThumbnail = 'https://image.tmdb.org/t/p/w396' + meta['profile_path']
                except:
                    sThumbnail = ''

                sId = meta['id']
                bio = meta['biography'].replace('\n\n', '[CR]').replace('\n', '[CR]')

                #self.getControl(5300).setLabel('[COLOR gold]test[/COLOR]')

                #window(10000).setProperty('biography', bio)
                window(10000).setProperty('birthday', meta['birthday'])
                window(10000).setProperty('place_of_birth', meta['place_of_birth'])
                window(10000).setProperty('deathday', meta['deathday'])

                #self.getControl(20).setVisible(True)
            except:
                pass


            #description
            #self.getControl(400).setText(meta['plot'])

        def onClick(self, controlId):
            print controlId
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
                self.getControl(50).setVisible(True)
                self.setFocusId(50)
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
                item = self.getControl(50).getSelectedItem()
                sid = item.getProperty('id')

                grab = cTMDb()
                sUrl = 'person/' + str(sid) + '/movie_credits'
                try:
                    meta = grab.getUrl(sUrl)
                    meta = meta['cast']
                    self.credit(meta)
                except:
                    return
                #self.getControl(50).setVisible(True)
            #click sur similaire
            elif controlId == 9:
                #print self.getControl(9000).ListItem.tmdb_id
                sid = window(10000).getProperty('ListItem.tmdb_id')

                grab = cTMDb()
                sUrl = 'movie/%s/similar' % str(sid)
                try:
                    meta = grab.getUrl(sUrl)
                    meta = meta['results']
                    if meta:
                        self.credit(meta)
                    else:
                        self.getControl(9).setLabel('Aucune Information')
                except:
                    return
            #click sur recommendations
            elif controlId == 13:
                #print self.getControl(9000).ListItem.tmdb_id
                sid = window(10000).getProperty('ListItem.tmdb_id')

                grab = cTMDb()
                sUrl = 'movie/%s/recommendations' % str(sid)
                try:
                    meta = grab.getUrl(sUrl)
                    meta = meta['results']
                    if meta:
                        self.credit(meta)
                    else:
                        self.getControl(13).setLabel('Aucune Information')

                except:
                    return

            elif controlId == 5200:
            #click sur un film acteur
                import sys
                from resources.lib.util import cUtil
                item = self.getControl(5200).getSelectedItem()
                sTitle = item.getLabel()

                try:
                    sTitle = sTitle.encode('utf-8')
                    sTitle = cUtil().CleanName(sTitle)
                except:
                    return

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
                self.getControl(5200).setVisible(False)
            if controlId != 50:
                self.getControl(50).setVisible(False)
            #if controlId == 50:
                #item = self.getControl(50).getSelectedItem()
                #sid = item.getProperty('id')
                #self.person(sid)

        def _close_dialog(self):
            self.close()

        def onAction(self, action):
            if action.getId() in (104, 105, 1, 2):
                # if self.controlId == 50:
                #     item = self.getControl(50).getSelectedItem()
                #     sid = item.getProperty('id')
                #     self.person(sid)
                return

            if action.getId() in (9, 10, 11, 30, 92, 216, 247, 257, 275, 61467, 61448):
                self.close()


    #path = xbmc.translatePath('special://home/addons/plugin.video.vstream').decode('utf-8')
    path = 'special://home/addons/plugin.video.vstream'
    #self.__oPath.decode('utf-8')
    wd = XMLDialog('DialogInfo2.xml', path , 'default', '720p')
    wd.doModal()
    del wd
