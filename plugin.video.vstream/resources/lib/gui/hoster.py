# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.contextElement import cContextElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.comaddon import dialog, addon, VSlog, xbmc

import re

class cHosterGui:

    SITE_NAME = 'cHosterGui'
    ADDON = addon()

    # step 1 - bGetRedirectUrl in ein extra optionsObject verpacken
    def showHoster(self, oGui, oHoster, sMediaUrl, sThumbnail, bGetRedirectUrl=False):
        oOutputParameterHandler = cOutputParameterHandler()
        oInputParameterHandler = cInputParameterHandler()

        # Gestion NextUp
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        site = oInputParameterHandler.getValue('site')
        saisonUrl = oInputParameterHandler.getValue('saisonUrl')
        nextSaisonFunc = oInputParameterHandler.getValue('nextSaisonFunc')
        movieUrl = oInputParameterHandler.getValue('movieUrl')
        movieFunc = oInputParameterHandler.getValue('movieFunc')
        sLang = oInputParameterHandler.getValue('sLang')
        sRes = oInputParameterHandler.getValue('sRes')
        sTmdbId = oInputParameterHandler.getValue('sTmdbId')
        sFav = oInputParameterHandler.getValue('sFav')
        if not sFav:
            sFav = oInputParameterHandler.getValue('function')

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        oGuiElement.setFunction('play')
        oGuiElement.setTitle(oHoster.getDisplayName())

        # Catégorie de lecture
        if oInputParameterHandler.exist('sCat'):
            sCat = oInputParameterHandler.getValue('sCat')
            if sCat == '4': # Si on vient de passer par un menu "Saison" ...
               sCat = '8'   #     ...  On est maintenant au niveau "Episode"
        else:
            sCat = '5'     # Divers
        oGuiElement.setCat(sCat)
        oOutputParameterHandler.addParameter('sCat', sCat)

        if (oInputParameterHandler.exist('sMeta')):
            sMeta = oInputParameterHandler.getValue('sMeta')
            oGuiElement.setMeta(int(sMeta))

        oGuiElement.setFileName(oHoster.getFileName())
        oGuiElement.getInfoLabel()
        if sThumbnail:
            oGuiElement.setThumbnail(sThumbnail)

        oGuiElement.setIcon('host.png')

        if sCat == "1":
            title = re.sub('\[.*\]|\(.*\)','', oHoster.getDisplayName())
        elif xbmc.getInfoLabel('ListItem.tagline'):
            title = xbmc.getInfoLabel('ListItem.tagline')
        else:
            title = oHoster.getDisplayName()

        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())
        oOutputParameterHandler.addParameter('sTitleWatched', oGuiElement.getTitleWatched())
        oOutputParameterHandler.addParameter('sTitle', title)
        oOutputParameterHandler.addParameter('sLang', sLang)
        oOutputParameterHandler.addParameter('sRes', sRes)
        oOutputParameterHandler.addParameter('sId', 'cHosterGui')
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
        
        # gestion NextUp
        oOutputParameterHandler.addParameter('sourceName', site)    # source d'origine
        oOutputParameterHandler.addParameter('sourceFav', sFav)    # source d'origine
        oOutputParameterHandler.addParameter('nextSaisonFunc', nextSaisonFunc)
        oOutputParameterHandler.addParameter('saisonUrl', saisonUrl)

        # gestion Lecture en cours
        oOutputParameterHandler.addParameter('movieUrl', movieUrl)
        oOutputParameterHandler.addParameter('movieFunc', movieFunc)

        # context playlist menu
        oContext = cContextElement()
        oContext.setFile('cHosterGui')
        oContext.setSiteName(self.SITE_NAME)
        oContext.setFunction('addToPlaylist')
        oContext.setTitle(self.ADDON.VSlang(30201))
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)

        # Download menu
        if oHoster.isDownloadable():
            oContext = cContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadList')
            oContext.setTitle(self.ADDON.VSlang(30202))
            oContext.setOutputParameterHandler(oOutputParameterHandler)
            oGuiElement.addContextItem(oContext)

        if oHoster.isDownloadable():
            # Beta context download and view menu
            oContext = cContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadListandview')
            oContext.setTitle(self.ADDON.VSlang(30326))
            oContext.setOutputParameterHandler(oOutputParameterHandler)
            oGuiElement.addContextItem(oContext)

        # Upload menu uptobox
        if cInputParameterHandler().getValue('site') != 'siteuptobox' and self.ADDON.getSetting('hoster_uptobox_premium') == 'true':
            host = oHoster.getPluginIdentifier()
            accept = ['uptobox', 'uptostream', 'onefichier', 'uploaded', 'uplea']
            for i in accept:
                if host == i:
                    oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'siteuptobox', 'siteuptobox', 'UptomyAccount', self.ADDON.VSlang(30325))

        # onefichier
        if cInputParameterHandler().getValue('site') != 'siteonefichier' and self.ADDON.getSetting('hoster_onefichier_premium') == 'true':
            host = oHoster.getPluginIdentifier()
            accept = 'onefichier'  # les autres ne fonctionnent pas
            if host == accept:
                oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'siteonefichier', 'siteonefichier', 'UptomyAccount', '1fichier')

        # context Library menu
        oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cLibrary', 'cLibrary', 'setLibrary', self.ADDON.VSlang(30324))

        oGui.addFolder(oGuiElement, oOutputParameterHandler, False)

    def checkHoster(self, sHosterUrl, debrid = True):
        # securite
        if not sHosterUrl:
            return False

        # Petit nettoyage
        sHosterUrl = sHosterUrl.split('|')[0]
        sHosterUrl = sHosterUrl.lower()

        # Recuperation du host
        try:
            sHostName = sHosterUrl.split('/')[2]
        except:
            sHostName = sHosterUrl

        if debrid:
            # L'user a active l'url resolver ?
            if self.ADDON.getSetting('UserUrlResolver') == 'true':
                import urlresolver
                hmf = urlresolver.HostedMediaFile(url=sHosterUrl)
                if hmf.valid_url():
                    tmp = self.getHoster('resolver')
                    RH = sHosterUrl.split('/')[2]
                    RH = RH.replace('www.', '')
                    tmp.setRealHost(RH.split('.')[0].upper())
                    return tmp
                
            # L'user a activé alldebrid ?
            if self.ADDON.getSetting('hoster_alldebrid_premium') == 'true':
                return self.getHoster('alldebrid')

            # L'user a activé debrid_link ?
            if self.ADDON.getSetting('hoster_debridlink_premium') == 'true':
                if "debrid.link" not in sHosterUrl:
                    return self.getHoster('debrid_link')
                else:
                    return self.getHoster("lien_direct")

        # Gestion classique
        if ('streamz' in sHostName):
            return self.getHoster('streamz')
        if ('streamax' in sHostName):
            return self.getHoster('streamax')
        if ('gounlimited' in sHostName):
            return self.getHoster('gounlimited')
        if ('xdrive' in sHostName):
            return self.getHoster('xdrive')
        if ('facebook' in sHostName):
            return self.getHoster('facebook')
        if ('mixdrop' in sHostName):
            return self.getHoster('mixdrop')
        if ('mixloads' in sHostName):
            return self.getHoster('mixloads')
        if ('vidoza' in sHostName):
            return self.getHoster('vidoza')
        if ('youtube' in sHostName) or ('youtu.be' in sHostName):
            return self.getHoster('youtube')
        if ('rutube' in sHostName):
            return self.getHoster('rutube')
        if ('vk.com' in sHostName):
            return self.getHoster('vk')
        if ('vkontakte' in sHostName):
            return self.getHoster('vk')
        if ('vkcom' in sHostName):
            return self.getHoster('vk')
        if ('megawatch' in sHostName):
            return self.getHoster('megawatch')
        if ('playvidto' in sHostName):
            return self.getHoster('vidto')
        # vidtodo et clone
        if ('vidtodo' in sHostName) or ('vixtodo' in sHostName):
            return self.getHoster('vidtodo')
        if ('viddoto' in sHostName):
            return self.getHoster('vidtodo')
        if ('vidstodo' in sHostName):
            return self.getHoster('vidtodo')

        if ('vidzi' in sHostName):
            return self.getHoster('vidzi')
        if ('vcstream' in sHostName):
            return self.getHoster('vidcloud')
        if ('filetrip' in sHostName):
            return self.getHoster('filetrip')
        if ('uptostream' in sHostName):
            return self.getHoster('uptostream')
        if ('dailymotion' in sHostName) or ('dai.ly' in sHostName):
            try:
                if 'stream' in sHosterUrl:
                    return self.getHoster('lien_direct')
            except:
                pass
            else:
                return self.getHoster('dailymotion')
        if ('livestream' in sHostName):
            return self.getHoster('lien_direct')
        if ('flashx' in sHostName):
            return self.getHoster('flashx')
        if ('filez' in sHostName):
            return self.getHoster('flashx')
        if ('mystream' in sHostName) or ('mstream' in sHostName):
            return self.getHoster('mystream')
        if ('streamingentiercom/videophp?type=speed' in sHosterUrl):
            return self.getHoster('speedvideo')
        if ('speedvideo' in sHostName):
            return self.getHoster('speedvideo')
        if ('speedvid' in sHostName):
            return self.getHoster('speedvid')
        #if ('netu' in sHostName) or ('hqq' in sHostName) or ('waaw' in sHostName) or ('vizplay' in sHostName):
        #    return self.getHoster('netu')
        if ('upstream' in sHostName):
            return self.getHoster('upstream')
        if ('mail.ru' in sHostName):
            return self.getHoster('mailru')
        if ('onevideo' in sHostName):
            return self.getHoster('onevideo')
        if ('googlevideo' in sHostName):
            return self.getHoster('googlevideo')
        if ('picasaweb' in sHostName):
            return self.getHoster('googlevideo')
        if ('googleusercontent' in sHostName):
            return self.getHoster('googlevideo')
        if ('playreplay' in sHostName):
            return self.getHoster('playreplay')
        if ('ok.ru' in sHostName) or ('odnoklassniki' in sHostName):
            return self.getHoster('ok_ru')
        if ('vimeo' in sHostName):
            return self.getHoster('vimeo')
        if ('prostream' in sHostName):
            return self.getHoster('prostream')
        if ('vidfast' in sHostName):
            return self.getHoster('vidfast')
        if ('thevideo' in sHostName) or ('video.tt' in sHostName) or ('vev.io' in sHostName):
            return self.getHoster('thevideo_me')
        if ('uqload' in sHostName):
            return self.getHoster('uqload')
        if ('letwatch' in sHostName):
            return self.getHoster('letwatch')
        if ('letsupload' in sHostName):
            return self.getHoster('letsupload')
        if ('filepup' in sHostName):
            return self.getHoster('filepup')
        if ('vimple.ru' in sHostName):
            return self.getHoster('vimple')
        if ('wstream' in sHostName):
            return self.getHoster('wstream')
        if ('watchvideo' in sHostName):
            return self.getHoster('watchvideo')
        if ('drive.google.com' in sHostName):
            return self.getHoster('googledrive')
        if ('docs.google.com' in sHostName):
            return self.getHoster('googledrive')
        if ('vidwatch' in sHostName):
            return self.getHoster('vidwatch')
        if ('up2stream' in sHostName):
            return self.getHoster('up2stream')
        if ('vidbm' in sHostName):
            return self.getHoster('vidbm')
        if ('tune' in sHostName):
            return self.getHoster('tune')
        if ('vidup' in sHostName):
            return self.getHoster('vidup')
        if ('vidbull' in sHostName):
            return self.getHoster('vidbull')
        # vidlox et clone
        if ('vidlox' in sHostName):
            return self.getHoster('vidlox')
        if ('videobin' in sHostName):
            return self.getHoster('videobin')

        if ('stagevu' in sHostName):
            return self.getHoster('stagevu')
        if ('movshare' in sHostName) or ('wholecloud' in sHostName):
            return self.getHoster('wholecloud')
        if ('gorillavid' in sHostName):
            return self.getHoster('gorillavid')
        if ('daclips' in sHostName):
            return self.getHoster('daclips')
        if ('estream' in sHostName) and not ('widestream' in sHostName):
            return self.getHoster('estream')
        if ('hdvid' in sHostName):
            return self.getHoster('hdvid')
        if ('vshare' in sHostName):
            return self.getHoster('vshare')
        if ('giga' in sHostName):
            return self.getHoster('giga')
        if ('vidbom' in sHostName):
            return self.getHoster('vidbom')
        if ('upvideo' in sHostName) or ('streamon' in sHostName):
            return self.getHoster('upvideo')
        if ('upvid' in sHostName):
            return self.getHoster('upvid')
        if ('cloudvid' in sHostName):
            return self.getHoster('cloudvid')
        if ('clipwatching' in sHostName) or ('highstream' in sHostName):
            return self.getHoster('clipwatching')
        if ('megadrive' in sHostName):
            return self.getHoster('megadrive')
        if ('downace' in sHostName):
            return self.getHoster('downace')
        if ('clickopen' in sHostName):
            return self.getHoster('clickopen')
        if ('iframe-secured' in sHostName):
            return self.getHoster('iframe_secured')
        if ('iframe-secure' in sHostName):
            return self.getHoster('iframe_secure')
        if ('goo.gl' in sHostName) or ('bit.ly' in sHostName) or ('streamcrypt' in sHostName) or ('opsktp' in sHosterUrl):
            return self.getHoster('allow_redirects')
        if ('jawcloud' in sHostName):
            return self.getHoster('jawcloud')
        if ('kvid' in sHostName):
            return self.getHoster('kvid')
        if ('soundcloud' in sHostName):
            return self.getHoster('soundcloud')
        if ('mixcloud' in sHostName):
            return self.getHoster('mixcloud')
        if ('ddlfr' in sHostName):
            return self.getHoster('ddlfr')
        if ('pdj' in sHostName):
            return self.getHoster('pdj')
        if ('vidzstore' in sHostName):
            return self.getHoster('vidzstore')
        if ('hd-stream' in sHostName):
            return self.getHoster('hd_stream')
        if ('rapidstream' in sHostName):
            return self.getHoster('rapidstream')
        if ('archive' in sHostName):
            return self.getHoster('archive')
        if ('jetload' in sHostName):
            return self.getHoster('jetload')
        if ('dustreaming' in sHostName):
            return self.getHoster('dustreaming')
        if ('vupload' in sHostName):
            return self.getHoster('vupload')

        # frenchvid et clone
        if ('french-vid' in sHostName) or ('yggseries' in sHostName):
            return self.getHoster('frenchvid')
        if ('fembed' in sHostName) or ('fem.tohds' in sHostName):
            return self.getHoster('frenchvid')
        if ('feurl' in sHostName) or ('fsimg' in sHostName):
            return self.getHoster('frenchvid')
        if ('core1player' in sHostName) or ('vfsplayer' in sHostName):
            return self.getHoster('frenchvid')
        if ('gotochus' in sHostName):
            return self.getHoster('frenchvid')

        if ('viki' in sHostName):
            return self.getHoster('viki')
        if ('flix555' in sHostName):
            return self.getHoster('flix555')
        if ('onlystream' in sHostName):
            return self.getHoster('onlystream')
        if ('pstream' in sHostName):
            return self.getHoster('pstream')
        if ('vudeo' in sHostName):
            return self.getHoster('vudeo')
        if ('sendvid' in sHostName):
            return self.getHoster('sendvid')
        if ('supervideo' in sHostName):
            return self.getHoster('supervideo')
        if ('dood' in sHostName):
            return self.getHoster('dood')
        if ('vidia' in sHostName):
            return self.getHoster('vidia')
        if ('streamtape' in sHostName):
            return self.getHoster('streamtape')
        if ('femax' in sHostName):
            return self.getHoster('femax')
        if ('vidbem' in sHostName):
            return self.getHoster('vidbem')
        if ('sibnet' in sHostName):
            return self.getHoster('sibnet')
        if ('vidplayer' in sHostName):
            return self.getHoster('vidplayer')
        if ('userload' in sHostName):
            return self.getHoster('userload')
        if ('aparat' in sHostName):
            return self.getHoster('aparat')
        if ('evoload' in sHostName):
            return self.getHoster('evoload')
        if ('vidshar' in sHostName):
            return self.getHoster('vidshar')
        if ('abcvideo' in sHostName):
            return self.getHoster('abcvideo')
        if ('plynow' in sHostName):
            return self.getHoster('plynow')
        if ('myvi.tv' in sHostName):
            return self.getHoster('myvitv')
        if ('playtube' in sHostName):
            return self.getHoster('playtube')
        if ('dwfull' in sHostName):
            return self.getHoster('dwfull')
        if ('directmoviedl' in sHostName) or ('moviesroot' in sHostName):
            return self.getHoster('directmoviedl')

        # Lien telechargeable a convertir en stream
        if ('1fichier' in sHostName):
            return self.getHoster('onefichier')
        if ('uptobox' in sHostName):
            return self.getHoster('uptobox')
        if ('uplea' in sHostName):
            return self.getHoster('uplea')
        if ('uploaded' in sHostName) or ('ul.to' in sHostName):
            if ('/file/forbidden' in sHosterUrl):
                return False
            return self.getHoster('uploaded')
        if ('vidload' in sHostName):
            return self.getHoster('vidload')
        if ('kaydo' in sHostName):
            return self.getHoster('lien_direct')
        if ('cloudhost' in sHostName):
            return self.getHoster('cloudhost')
        if ('rapidgator' in sHostName):
            return False
        if ('turbobit' in sHostName):
            return False
        if ('mega.nz' in sHostName) or ('mega.co.nz' in sHostName):
            return False
        if ('hitfile' in sHostName):
            return False
        if ('myfiles.alldebrid.com' in sHostName):
            return self.getHoster('lien_direct')
        if ('dl.free.fr' in sHostName):
            return False
        if ('easyload' in sHostName):
            return self.getHoster('easyload')
        if ('ninjastream' in sHostName):
            return self.getHoster('ninjastream')
        if ('megaup' in sHostName):
            return self.getHoster('megaup')            

        # Si aucun hebergeur connu on teste les liens directs
        if (sHosterUrl[-4:] in '.mp4.avi.flv.m3u8.webm.mkv'):
            return self.getHoster('lien_direct')
        # Cas special si parametre apres le lien_direct
        if (sHosterUrl.split('?')[0][-4:] in '.mp4.avi.flv.m3u8.webm.mkv'):
            return self.getHoster('lien_direct')

        return False

    def getHoster(self, sHosterFileName):
        exec ("from resources.hosters." + sHosterFileName + " import cHoster", globals())
        return cHoster()

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
        oDialog.VSinfo(sHosterName, 'Resolve')

        try:
            oHoster.setUrl(sMediaUrl)
            aLink = oHoster.getMediaLink()

            if aLink[0] or aLink[1] : # Le hoster ne sait pas résoudre mais a retourné une autre url
                if not aLink[0] :   # Voir exemple avec allDebrid qui : return False, URL
                    oHoster = self.checkHoster(aLink[1], debrid=False)
                    if oHoster:
                        oHoster.setFileName(sFileName)
                        sHosterName = oHoster.getDisplayName()
                        oDialog.VSinfo(sHosterName, 'Resolve')
                        oHoster.setUrl(sMediaUrl)
                        aLink = oHoster.getMediaLink()

                if aLink[0] :
                    oGuiElement = cGuiElement()
                    oGuiElement.setSiteName(self.SITE_NAME)
                    oGuiElement.setSiteUrl(siteUrl)
                    oGuiElement.setMediaUrl(aLink[1])
                    oGuiElement.setTitle(sTitle)
                    oGuiElement.setCat(sCat)
                    oGuiElement.getInfoLabel()
    
                    from resources.lib.player import cPlayer
                    oPlayer = cPlayer()
    
                    # sous titres ?
                    if len(aLink) > 2:
                        oPlayer.AddSubtitles(aLink[2])
    
                    return oPlayer.run(oGuiElement, oHoster.getFileName(), aLink[1])

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
            dialog().VSinfo(str(oHoster.getFileName()), 'Playlist')
            return

        oGui.setEndOfDirectory()

    def __getRedirectUrl(self, sUrl):
        from resources.lib.handler.requestHandler import cRequestHandler
        oRequest = cRequestHandler(sUrl)
        oRequest.request()
        return oRequest.getRealUrl()
