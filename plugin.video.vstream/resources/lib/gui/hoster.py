# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.contextElement import cContextElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import dialog, addon, VSlog


class cHosterGui:
    SITE_NAME = 'cHosterGui'
    ADDON = addon()

    def showHoster(self, oGui, oHoster, sMediaUrl, sThumbnail='', bGetRedirectUrl=False):
        oHoster.setUrl(sMediaUrl)
        oOutputParameterHandler = cOutputParameterHandler()
        oInputParameterHandler = cInputParameterHandler()

        # Gestion NextUp
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        site = oInputParameterHandler.getValue('site')
        saisonUrl = oInputParameterHandler.getValue('saisonUrl')
        sSeason = oInputParameterHandler.getValue('sSeason')
        sEpisode = oInputParameterHandler.getValue('sEpisode')
        nextSaisonFunc = oInputParameterHandler.getValue('nextSaisonFunc')
        movieUrl = oInputParameterHandler.getValue('movieUrl')
        movieFunc = oInputParameterHandler.getValue('movieFunc')
        sLang = oInputParameterHandler.getValue('sLang')
        sRes = oInputParameterHandler.getValue('sRes')
        sYear = oInputParameterHandler.getValue('sYear')
        sDesc = oInputParameterHandler.getValue('sDesc')
        sTmdbId = oInputParameterHandler.getValue('sTmdbId')
        sFav = oInputParameterHandler.getValue('sFav')
        if not sFav:
            sFav = oInputParameterHandler.getValue('function')
        if not sRes:
            sRes = oHoster.getRes()

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('play')
        # oGuiElement.setMetaAddon(False)     # pas de gestion des metadata pour ce type de liens

        # Catégorie de lecture
        if oInputParameterHandler.exist('sCat'):
            sCat = oInputParameterHandler.getValue('sCat')
            if sCat == '4':  # Si on vient de passer par un menu "Saison" ...
                sCat = '8'   # ...  On est maintenant au niveau "Episode"
        else:
            sCat = '5'     # Divers
        oGuiElement.setCat(sCat)
        oOutputParameterHandler.addParameter('sCat', sCat)
        oGuiElement.setYear(sYear)
        oGuiElement.setDescription(sDesc)

        if (oInputParameterHandler.exist('sMeta')):
            sMeta = oInputParameterHandler.getValue('sMeta')
            oGuiElement.setMeta(sMeta)

        oGuiElement.setFileName(oHoster.getFileName())
        oGuiElement.getInfoLabel()
        oGuiElement.setIcon('host.png')
        if sThumbnail:
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setPoster(sThumbnail)

        sMediaFile = oHoster.getMediaFile()
        if sMediaFile:  # Afficher le nom du fichier plutot que le titre
            oGuiElement.setMediaUrl(sMediaFile)
            if self.ADDON.getSetting('display_info_file') == 'true':
#                oHoster.setDisplayName(sMediaFile)
                oGuiElement.setTitle(oHoster.getFileName())  # permet de calculer le cleanTitle
                oGuiElement.setRawTitle(oHoster.getDisplayName())  # remplace le titre par le lien
            else:
                oGuiElement.setTitle(oHoster.getDisplayName())
        else:
            oGuiElement.setTitle(oHoster.getDisplayName())

        title = oGuiElement.getCleanTitle()
        tvShowTitle = oGuiElement.getItemValue('tvshowtitle')

        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        oOutputParameterHandler.addParameter('sTitleWatched', oGuiElement.getTitleWatched())
        oOutputParameterHandler.addParameter('tvShowTitle', tvShowTitle)
        oOutputParameterHandler.addParameter('sTitle', title)
        oOutputParameterHandler.addParameter('sSeason', sSeason)
        oOutputParameterHandler.addParameter('sEpisode', sEpisode)
        oOutputParameterHandler.addParameter('sLang', sLang)
        oOutputParameterHandler.addParameter('sRes', sRes)
        oOutputParameterHandler.addParameter('sYear', sYear)
        oOutputParameterHandler.addParameter('sId', 'cHosterGui')
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)

        # gestion NextUp
        oOutputParameterHandler.addParameter('sourceName', site)  # source d'origine
        oOutputParameterHandler.addParameter('sourceFav', sFav)  # source d'origine
        oOutputParameterHandler.addParameter('nextSaisonFunc', nextSaisonFunc)
        oOutputParameterHandler.addParameter('saisonUrl', saisonUrl)
        oOutputParameterHandler.addParameter('realHoster', oHoster.getRealHost())

        # gestion Lecture en cours
        oOutputParameterHandler.addParameter('movieUrl', movieUrl)
        oOutputParameterHandler.addParameter('movieFunc', movieFunc)

        # Download menu
        if oHoster.isDownloadable():
            oContext = cContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadList')
            oContext.setTitle(self.ADDON.VSlang(30202))
            oContext.setOutputParameterHandler(oOutputParameterHandler)
            oGuiElement.addContextItem(oContext)

            # Beta context download and view menu
            oContext = cContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadListandview')
            oContext.setTitle(self.ADDON.VSlang(30326))
            oContext.setOutputParameterHandler(oOutputParameterHandler)
            oGuiElement.addContextItem(oContext)

        # Liste de lecture
        oContext = cContextElement()
        oContext.setFile('cHosterGui')
        oContext.setSiteName(self.SITE_NAME)
        oContext.setFunction('addToPlaylist')
        oContext.setTitle(self.ADDON.VSlang(30201))
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)

        # Dossier Media
        oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cLibrary', 'cLibrary', 'setLibrary', self.ADDON.VSlang(30324))

        # Upload menu uptobox
        if cInputParameterHandler().getValue('site') != 'siteuptobox' and self.ADDON.getSetting('hoster_uptobox_premium') == 'true':
            host = oHoster.getPluginIdentifier()
            accept = ['uptobox', 'uptostream', '1fichier', 'uploaded', 'uplea']
            for i in accept:
                if host == i:
                    oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'siteuptobox', 'siteuptobox', 'upToMyAccount', self.ADDON.VSlang(30325))
                    break

        # onefichier
        if cInputParameterHandler().getValue('site') != 'siteonefichier' and self.ADDON.getSetting('hoster_onefichier_premium') == 'true':
            host = oHoster.getPluginIdentifier()
            accept = '1fichier'  # les autres ne fonctionnent pas
            if host == accept:
                oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'siteonefichier', 'siteonefichier', 'upToMyAccount', '1fichier')

        oGui.addFolder(oGuiElement, oOutputParameterHandler, False)


    def checkHoster(self, sHosterUrl, debrid=True, tried_urls=None, depth=0, max_depth=3):
        # securite
        if not sHosterUrl:
            return False

        if tried_urls is None:
            tried_urls = set()
        if sHosterUrl in tried_urls or depth > max_depth:
            VSlog("Boucle évitée ou profondeur max atteinte pour %s" % sHosterUrl)
            return False
        tried_urls.add(sHosterUrl)

        fullURL = sHosterUrl

        # lien direct ?
        if any(x in sHosterUrl for x in ['.mp4', '.avi', '.flv', '.m3u8', '.webm', '.mkv', '.mpd']):
            return self.getHoster('lien_direct')

        # Petit nettoyage
        sHosterUrl = sHosterUrl.split('|')[0]
        sHosterUrl = sHosterUrl.split('?')[0]
        sHosterUrl = sHosterUrl.lower()

        # Recuperation du host
        try:
            from urllib.parse import urlparse
            sHostName = urlparse(sHosterUrl).hostname or sHosterUrl
        except Exception:
            sHostName = sHosterUrl

        if debrid: # premiere tentative avec debrideur, si on revient ici, ce sera pour tester sans debrideur

# NON, Il faut passer par alldebrid car darkibox est bloqué dans certains pays
            # Priorité au compte darkibox pour les liens darkino
            # if self.ADDON.getSetting('hoster_darkibox_premium') == 'true':
            #     sRealHost = self.checkHoster(sHosterUrl, False)
            #     if sRealHost and 'darkibox' in sRealHost.getPluginIdentifier():
            #         return sRealHost

            # L'user a activé alldebrid ?
            if self.ADDON.getSetting('hoster_alldebrid_premium') == 'true':
                f = self.getHoster('alldebrid')
                #mise a jour du nom
                sRealHost = self.checkHoster(sHosterUrl, False)
                if sRealHost:
                    sHostName = sRealHost.getPluginIdentifier()
                f.setRealHost(sHostName)
                return f

            # L'user a activé realbrid ?
            if self.ADDON.getSetting('hoster_realdebrid_premium') == 'true':
                f = self.getHoster('realdebrid')
                #mise a jour du nom
                sRealHost = self.checkHoster(sHosterUrl, False)
                if sRealHost:
                    sHostName = sRealHost.getPluginIdentifier()
                f.setRealHost(sHostName)
                return f

            # L'user a activé debrid_link ?
            if self.ADDON.getSetting('hoster_debridlink_premium') == 'true':
                if "debrid.link" not in sHosterUrl:
                    return self.getHoster('debrid_link')
                else:
                    return self.getHoster("lien_direct")

        supported_player = ['streamz', 'streamax', 'gounlimited', 'xdrive', 'facebook', 'mixdrop', 'mixloads', 'vidoza',
                            'rutube', 'megawatch', 'vidzi', 'filetrip', 'speedvid', 'letsupload', 'fsvid',
                            'onevideo', 'playreplay', 'vimeo', 'prostream', 'vidfast', 'uqload', 'letwatch', 'mail.ru',
                            'filepup', 'vimple', 'wstream', 'watchvideo', 'vidwatch', 'up2stream', 'tune', 'playtube',
                            'vidup', 'vidbull', 'vidlox', 'megaup', '33player' 'easyload', 'ninjastream', 'cloudhost',
                            'videobin', 'stagevu', 'gorillavid', 'daclips', 'hdvid', 'vshare', 'streamlare', 'vidload',
                            'giga', 'vidbom', 'cloudvid', 'megadrive', 'downace', 'clickopen', 'supervideo', 'turbovid',
                            'jawcloud', 'kvid', 'soundcloud', 'mixcloud', 'ddlfr', 'vupload', 'dwfull', 'vidzstore',
                            'pdj', 'rapidstream', 'archive', 'dustreaming', 'viki', 'flix555', 'onlystream', 'filemoon',
                            'upstream', 'pstream', 'vudeo', 'vidia', 'streamtape', 'vidbem', 'uplea', 'vido', 'vidmoly',
                            'sibnet', 'vidplayer', 'userload', 'aparat', 'evoload', 'vidshar', 'abcvideo', 'plynow',
                            'tomacloud', 'myvi', 'videovard', 'viewsb', 'yourvid', 'vf-manga', 'darkibox', 'mustardshock']

# désactivé 'uptostream', 'uptobox'

        val = next((x for x in supported_player if x in sHostName), None)
        if val:
            return self.getHoster(val.replace('.', ''))


        # Gestion classique
        if ('vidbm' in sHostName) or ('vedbom' in sHostName):
            return self.getHoster('vidbm')

        if ('embedwish' in sHostName) or ('streamwish' in sHostName) or ('warda' in sHostName):
            return self.getHoster('streamwish')

        if ('guccihide' in sHostName) or ('streamhide' in sHostName) or ('wishonly' in sHostName):
            return self.getHoster('streamhide')

        # if ('youtube' in sHostName) or ('youtu.be' in sHostName):
        #     return self.getHoster('youtube')

        if ('oneupload' in sHostName) or ('tipfly' in sHostName):
            return self.getHoster('oneupload')

        if ('vk.com' in sHostName) or ('vkontakte' in sHostName) or ('vkcom' in sHostName):
            return self.getHoster('vk')

        if ('vidguard' in sHostName) or ('fertoto' in sHostName) or ('vgembed' in sHostName) or ('vgfplay' in sHostName) or ('jetload' in sHostName):
            return self.getHoster('vidguard')

        if ('filelions' in sHostName) or ('shoooot' in sHostName) or ('vidhide' in sHostName) or ('nejma' in sHostName):
            return self.getHoster('filelions')

        if ('playvidto' in sHostName):
            return self.getHoster('vidto')

        if ('hd-stream' in sHostName):
            return self.getHoster('hd_stream')

        if ('vcstream' in sHostName):
            return self.getHoster('vidcloud')

        if ('livestream' in sHostName):
            return self.getHoster('lien_direct')

        if ('mustardshock' in sHostName):
            return self.getHoster('lien_direct')

        # vidtodo et clone
        val = next((x for x in ['vidtodo', 'vixtodo', 'viddoto', 'vidstodo'] if x in sHostName), None)
        if val:
            return self.getHoster('vidtodo')

        if ('dailymotion' in sHostName) or ('dai.ly' in sHostName):
            try:
                if 'stream' in sHosterUrl:
                    return self.getHoster('lien_direct')
            except:
                pass
            else:
                return self.getHoster('dailymotion')
        if ('flashx' in sHostName) or ('filez' in sHostName):
            return self.getHoster('flashx')

        if ('xcoic' in sHostName):
            return self.getHoster('filemoon')

        if ('mystream' in sHostName) or ('mstream' in sHostName):
            return self.getHoster('mystream')

        if ('streamingentiercom/videophp' in sHosterUrl) or ('speedvideo' in sHostName):
            return self.getHoster('speedvideo')

        if ('googlevideo' in sHostName) or ('picasaweb' in sHostName) or ('googleusercontent' in sHostName):
            return self.getHoster('googlevideo')

        if ('ok.ru' in sHostName) or ('odnoklassniki' in sHostName):
            return self.getHoster('ok_ru')

        if ('iframe-secured' in sHostName):
            return self.getHoster('iframe_secured')

        if ('iframe-secure' in sHostName):
            return self.getHoster('iframe_secure')

        if ('thevideo' in sHostName) or ('video.tt' in sHostName) or ('vev.io' in sHostName):
            return self.getHoster('thevideo_me')

        if ('drive.google.com' in sHostName) or ('docs.google.com' in sHostName):
            return self.getHoster('googledrive')

        if ('movshare' in sHostName) or ('wholecloud' in sHostName):
            return self.getHoster('wholecloud')

        if ('moacloud' in sHostName) or ('duxcloud' in sHostName):
            return self.getHoster('vidzstore')

        if ('upvideo' in sHostName) or ('streamon' in sHostName):
            return self.getHoster('upvideo')

        if ('upvid' in sHostName) or ('opvid' in sHostName) or ('illvid' in sHostName) or ('golvid' in sHostName):
            return self.getHoster('upvid')

        if ('estream' in sHostName) and not ('widestream' in sHostName):
            return self.getHoster('estream')

        if ('clipwatching' in sHostName) or ('highstream' in sHostName):
            return self.getHoster('clipwatching')

        # if ('flixeo' in sHostName):
        #     return self.getHoster('allow_redirects')

        if ('bigwarp' in sHostName):
            return self.getHoster('flix555')
 
        if sHostName.replace('o','').replace('0','').replace('stream','').split('.')[0] == 'dd':
            return self.getHoster('dood')
        if ('ds2play' in sHostName) or ('ds2video' in sHostName) or ('dooodster' in sHostName) or ('vidply' in sHostName):
            return self.getHoster('dood')

        if ('voe' in sHostName) or ('jamessoundcost' in sHostName) or ('magasavor' in sHostName)  or ('sandratableother' in sHostName) or ('alejandrocenturyoil' in sHostName):
            return self.getHoster('voe')

        if ('goo.gl' in sHostName) or ('bit.ly' in sHostName) or ('streamcrypt' in sHostName) or ('opsktp' in sHosterUrl):
            return self.getHoster('allow_redirects')

        if ('netu' in sHostName) or ('waaw' in sHostName) or ('hqq' in sHostName) or ('doplay' in sHostName) or ('vizplay' in sHostName) or ('netzues' in sHostName):
            return self.getHoster('netu')

        if ('tapepops' in sHostName):
            return self.getHoster('streamtape')


        # frenchvid et clone
        val = next((x for x in ['french-vid', 'yggseries', 'fembed', 'fem.tohds', 'feurl', 'fsimg', 'core1player',
                                'vfsplayer', 'gotochus', 'sendvid', 'femax'] if x in sHostName), None)
        if val:
            return self.getHoster("frenchvid")

        if ('directmoviedl' in sHostName) or ('moviesroot' in sHostName):
            return self.getHoster('directmoviedl')

        # Lien telechargeable a convertir en stream
        if ('1fichier' in sHostName):
            return self.getHoster('1fichier')

        if ('uploaded' in sHostName) or ('ul.to' in sHostName):
            if ('/file/forbidden' in sHosterUrl):
                return False
            return self.getHoster('uploaded')

        if ('myfiles.alldebrid.com' in sHostName):
            return self.getHoster('lien_direct')

        # Si on a rien trouvé mais que le lien semble valide (ex: /e/ dans l'URL)
        if "/e/" in fullURL:
            try:
                from resources.lib.handler.requestHandler import cRequestHandler
                oRequest = cRequestHandler(fullURL)
                html = oRequest.request()
                sHosterUrl2 = None
                import re
                if 'content="VOE">' in html or re.search(r'voe', html, re.I):
                    # Reconstruit l'URL pour voe
                    sHosterUrl2 = 'https://voe.com/%s' % (fullURL.split('/e/', 1)[1])
                elif 'filemoon' in html:
                    sHosterUrl2 = 'https://filemoon.com/%s' % (fullURL.split('/e/', 1)[1])
                if sHosterUrl2:
                    return self.checkHoster(sHosterUrl2, debrid, tried_urls, depth+1, max_depth)
            except Exception as e:
                pass

        return False

    def getHoster(self, sHosterFileName):
        mod = __import__('resources.hosters.' + sHosterFileName, fromlist=['cHoster'])
        klass = getattr(mod, 'cHoster')
        return klass()

    def play(self):
        oGui = cGui()
        oDialog = dialog()

        oInputParameterHandler = cInputParameterHandler()
        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')
        sTitle = oInputParameterHandler.getValue('sTitle')
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        sCat = oInputParameterHandler.getValue('sCat')
        sMeta = oInputParameterHandler.getValue('sMeta')

        if not sTitle:
            sTitle = sFileName

        if bGetRedirectUrl == 'True':
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        try:
            mediaDisplay = sMediaUrl.split('/')
            VSlog('Hoster - play : %s/ ... /%s' % ('/'.join(mediaDisplay[0:3]), mediaDisplay[-1]))
        except:
            VSlog('Hoster - play : ' + sMediaUrl)

        oHoster = self.getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        sHosterName = oHoster.getDisplayName()
        oDialog.VSinfo(sHosterName, self.ADDON.VSlang(30142))

        try:
            oHoster.setUrl(sMediaUrl)
            aLink = oHoster.getMediaLink()

            if aLink and (aLink[0] or aLink[1]):  # Le hoster ne sait pas résoudre mais a retourné une autre url
                if not aLink[0]:  # Voir exemple avec allDebrid qui : return False, URL
                    oHoster = self.checkHoster(aLink[1], debrid=False)
                    if oHoster:
                        oHoster.setFileName(sFileName)
                        sHosterName = oHoster.getDisplayName()
                        oDialog.VSinfo(sHosterName, self.ADDON.VSlang(30142))
                        oHoster.setUrl(aLink[1])
                        aLink = oHoster.getMediaLink()

                if aLink[0]:
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(self.SITE_NAME)
                    oGuiElement.setSiteUrl(siteUrl)
                    oGuiElement.setMediaUrl(aLink[1])
                    oGuiElement.setFileName(sFileName)
                    oGuiElement.setCat(sCat)
                    oGuiElement.setMeta(sMeta)
                    oGuiElement.setTitle(sTitle)
                    oGuiElement.getInfoLabel()

                    from resources.lib.player import cPlayer
                    oPlayer = cPlayer()

                    # sous-titres ?
                    if len(aLink) > 2:
                        oPlayer.AddSubtitles(aLink[2])

                    return oPlayer.run(oGuiElement, aLink[1])

            oDialog.VSerror(self.ADDON.VSlang(30020))
            return

        except Exception as e:
            oDialog.VSerror(self.ADDON.VSlang(30020))
            import traceback
            traceback.print_exc()
            return

        oGui.setEndOfDirectory()

    def addToPlaylist(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()
        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if bGetRedirectUrl == 'True':
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        VSlog('Hoster - playlist ' + sMediaUrl)
        oHoster = self.getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        oHoster.setUrl(sMediaUrl)
        aLink = oHoster.getMediaLink()

        if aLink[0]:
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(aLink[1])
            oGuiElement.setTitle(oHoster.getFileName())

            from resources.lib.player import cPlayer
            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            dialog().VSinfo(str(oHoster.getFileName()), 'Liste de lecture')
            return

        oGui.setEndOfDirectory()

    def __getRedirectUrl(self, sUrl):
        from resources.lib.handler.requestHandler import cRequestHandler
        oRequest = cRequestHandler(sUrl)
        oRequest.request()
        return oRequest.getRealUrl()
