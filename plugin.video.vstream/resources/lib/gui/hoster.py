#-*- coding: utf-8 -*-
# Venom.
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.gui.contextElement import cContextElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.player import cPlayer
from resources.lib.db import cDb
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.config import cConfig
from resources.lib import util


class cHosterGui:

    SITE_NAME = 'cHosterGui'

    # step 1 - bGetRedirectUrl in ein extra optionsObject verpacken
    def showHoster(self, oGui, oHoster, sMediaUrl, sThumbnail, bGetRedirectUrl = False):

        oInputParameterHandler = cInputParameterHandler()
        sMovieTitle = oInputParameterHandler.getValue('title')

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(self.SITE_NAME)
        #oGuiElement.setFunction('showHosterMenu')
        oGuiElement.setFunction('play')
        oGuiElement.setTitle(oHoster.getDisplayName())
        #oGuiElement.setThumbnail(sThumbnail)
        # if (oInputParameterHandler.exist('sMeta')):
            # sMeta = oInputParameterHandler.getValue('sMeta')
            # oGuiElement.setMeta(int(sMeta))

        oGuiElement.setFileName(oHoster.getFileName())
        oGuiElement.getInfoLabel()
        oGuiElement.setCat(4)
        #oGuiElement.setThumbnail(xbmc.getInfoLabel('ListItem.Art(thumb)'))
        if sThumbnail:
            oGuiElement.setThumbnail(sThumbnail)

        #oGuiElement.setMeta(1)
        oGuiElement.setIcon('host.png')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sMediaUrl', sMediaUrl)
        #oOutputParameterHandler.addParameter('sThumbnail', oGuiElement.getThumbnail())

        oOutputParameterHandler.addParameter('sHosterIdentifier', oHoster.getPluginIdentifier())
        oOutputParameterHandler.addParameter('bGetRedirectUrl', bGetRedirectUrl)
        oOutputParameterHandler.addParameter('sFileName', oHoster.getFileName())

        oOutputParameterHandler.addParameter('sTitle', oHoster.getDisplayName())
        oOutputParameterHandler.addParameter('sId', 'cHosterGui')
        oOutputParameterHandler.addParameter('siteUrl', sMediaUrl)
        #oOutputParameterHandler.addParameter('sFav', 'play')
        #oOutputParameterHandler.addParameter('sCat', '4')

        #existe dans le menu krypton 17
        if not util.isKrypton():
            oGui.createContexMenuWatch(oGuiElement, oOutputParameterHandler)

        #context playlit menu
        oContext = cContextElement()
        oContext.setFile('cHosterGui')
        oContext.setSiteName(self.SITE_NAME)
        oContext.setFunction('addToPlaylist')
        oContext.setTitle(util.VSlang(30201))
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)

        #Download menu
        if (oHoster.isDownloadable() == True):
            oContext = cContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadList')
            oContext.setTitle(util.VSlang(30202))
            oContext.setOutputParameterHandler(oOutputParameterHandler)
            oGuiElement.addContextItem(oContext)

        if (oHoster.isDownloadable() == True):
            #Beta context download and view menu
            oContext = cContextElement()
            oContext.setFile('cDownload')
            oContext.setSiteName('cDownload')
            oContext.setFunction('AddtoDownloadListandview')
            oContext.setTitle(util.VSlang(30326))
            oContext.setOutputParameterHandler(oOutputParameterHandler)
            oGuiElement.addContextItem(oContext)
        #Upload menu
        if cInputParameterHandler().getValue('site') != 'siteuptobox' and cConfig().getSetting('hoster_uptobox_premium') == 'true' and oHoster.getPluginIdentifier() == 'uptobox' or oHoster.getPluginIdentifier() == 'uptostream':
            oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'siteuptobox', 'siteuptobox', 'AddmyAccount', util.VSlang(30325))

        #Upload url vers upto
        if cConfig().getSetting('hoster_uptobox_premium') == 'true' and oHoster.getPluginIdentifier() == 'onefichier' or oHoster.getPluginIdentifier() == 'uplea':
            oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'siteuptobox', 'siteuptobox', 'UptomyAccount', util.VSlang(30325))

        #context FAV menu
        oGui.createContexMenuFav(oGuiElement, oOutputParameterHandler)

        #context Library menu
        oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cLibrary', 'cLibrary', 'setLibrary', util.VSlang(30324))

        #bug
        oGui.addHost(oGuiElement, oOutputParameterHandler)

        #oGui.addFolder(oGuiElement, oOutputParameterHandler)

    def checkHoster(self, sHosterUrl):

        #securitee
        if (not sHosterUrl):
            return False

        #Petit nettoyage
        sHosterUrl = sHosterUrl.split('|')[0]

        #Recuperation du host
        try:
            sHostName = sHosterUrl.split('/')[2]
        except:
            sHostName = sHosterUrl

        #L'user a active l'url resolver ?
        if cConfig().getSetting('UserUrlResolver') == 'true':
            import urlresolver
            hmf = urlresolver.HostedMediaFile(url=sHosterUrl)
            if hmf.valid_url():
                tmp = self.getHoster('resolver')
                RH = sHosterUrl.split('/')[2]
                RH = RH.replace('www.','')
                tmp.setRealHost( RH[:3].upper() )
                return tmp

        #Gestion classique
        if ('facebook' in sHostName):
            return self.getHoster('facebook')
        if ('novamov' in sHostName):
            return self.getHoster('novamov')
        if ('auroravid' in sHostName):
            return self.getHoster('auroravid')
        if (('divxstage' in sHostName) or ('cloudtime' in sHostName)):
            return self.getHoster('divxstage')
        if (('raptu.com' in sHostName) or ('rapidvideo' in sHostName)):
            return self.getHoster('raptu')
        if ('watchers.to' in sHostName):
            return self.getHoster('watchers')
        if (('videoweed' in sHostName) or ('bitvid' in sHostName)):
            return self.getHoster('videoweed')
        if ('vidoza.' in sHostName):
            return self.getHoster('vidoza')
        if (('youtube' in sHostName) or ('youtu.be' in sHostName)):
            return self.getHoster('youtube')
        if ('rutube' in sHostName):
            return self.getHoster('rutube')
        if ('nowvideo' in sHostName):
            return self.getHoster('nowvideo')
        if ('vk.com' in sHostName):
            return self.getHoster('vk')
        if ('vkontakte' in sHostName):
            return self.getHoster('vk')
        if ('vkcom' in sHostName):
            return self.getHoster('vk')
        if ('megawatch' in sHostName):
            return self.getHoster('megawatch')
        if ('vidto.me' in sHostName):
            return self.getHoster('vidto')
        if ('vidtodo.com' in sHostName):
            return self.getHoster('vidtodo')
        if ('vidzi' in sHostName):
            return self.getHoster('vidzi')
        if ('cloudy' in sHostName):
            return self.getHoster('cloudy')
        if ('filetrip' in sHostName):
            return self.getHoster('filetrip')
        if ('uptostream' in sHostName):
            return self.getHoster('uptostream')
        if (('dailymotion' in sHostName) or ('dai.ly' in sHostName)):
            return self.getHoster('dailymotion')
        if ('filez.' in sHostName):
            return self.getHoster('filez')
        if ('vodlocker' in sHostName):
            return self.getHoster('vodlocker')
        if ('mystream' in sHostName):
            return self.getHoster('mystream')
        if ('streamingentiercom/videophp?type=speed' in sHosterUrl):
            return self.getHoster('speedvideo')
        if ('speedvideo' in sHostName):
            return self.getHoster('speedvideo')
        if ('speedvid' in sHostName):
            return self.getHoster('speedvid')
        if (('netu' in sHostName) or ('hqq' in sHostName)):
            return self.getHoster('netu')
        if ('waaw' in sHostName):
            return self.getHoster('netu')
        if ('mail.ru' in sHostName):
            return self.getHoster('mailru')
        if ('videoraj' in sHostName):
            return self.getHoster('videoraj')
        if ('videohut' in sHostName):
            return self.getHoster('videohut')
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
        if ('streamin.to' in sHostName):
            return self.getHoster('streaminto')
        if ('vodlocker' in sHostName):
            return self.getHoster('vodlocker')
        if ('flashx' in sHostName):
            return self.getHoster('flashx')
        if ('easywatch' in sHostName):
            return self.getHoster('easywatch')
        if (('ok.ru' in sHostName) or ('odnoklassniki' in sHostName)):
            return self.getHoster('ok_ru')
        if ('vimeo.com' in sHostName):
            return self.getHoster('vimeo')
        if ('openload' in sHostName):
            return self.getHoster('openload')
        if ('oload.' in sHostName):
            return self.getHoster('openload')
        if (('thevideo.me' in sHostName) or ('video.tt' in sHostName)):
            return self.getHoster('thevideo_me')
        if ('vid.me' in sHostName):
            return self.getHoster('vidme')
        if ('zstream' in sHostName):
            return self.getHoster('zstream')
        if ('uqload.' in sHostName):
            return self.getHoster('uqload')
        if ('letwatch' in sHostName):
            return self.getHoster('letwatch')
        if ('easyvid' in sHostName):
            return self.getHoster('easyvid')
        if ('www.amazon' in sHostName):
            return self.getHoster('amazon')
        if ('filepup' in sHostName):
            return self.getHoster('filepup')
        if ('thevid' in sHostName):
            return self.getHoster('thevid')
        if ('nosvideo' in sHostName):
            return self.getHoster('nosvideo')
        if ('vimple.ru' in sHostName):
            return self.getHoster('vimple')
        if ('allmyvideos.net' in sHostName):
            return self.getHoster('allmyvideos')
        if ('idowatch' in sHostName):
            return self.getHoster('idowatch')
        if ('wstream.' in sHostName):
            return self.getHoster('wstream')
        if ('watchvideo.' in sHostName):
             return self.getHoster('watchvideo')
        if ('drive.google.com' in sHostName):
            return self.getHoster('googledrive')
        if ('docs.google.com' in sHostName):
            return self.getHoster('googledrive')
        if ('vidwatch' in sHostName):
            return self.getHoster('vidwatch')
        if ('up2stream' in sHostName):
            return self.getHoster('up2stream')
        if ('stream.moe' in sHostName):
            return self.getHoster('streammoe')
        if ('tune' in sHostName):
            return self.getHoster('tune')
        if ('sendvid' in sHostName):
            return self.getHoster('sendvid')
        if ('vidup' in sHostName):
            return self.getHoster('vidup')
        if ('vidbull' in sHostName):
            return self.getHoster('vidbull')
        if ('vidlox' in sHostName):
            return self.getHoster('vidlox')
        if ('stagevu' in sHostName):
            return self.getHoster('stagevu')
        if ('veehd.' in sHostName):
            return self.getHoster('veehd')
        if (('movshare' in sHostName) or ('wholecloud' in sHostName)):
            return self.getHoster('wholecloud')
        if ('gorillavid' in sHostName):
            return self.getHoster('gorillavid')
        if ('daclips' in sHostName):
            return self.getHoster('daclips')
        if ('kvid' in sHostName):
            return self.getHoster('kvid')
        if ('estream' in sHostName):
            return self.getHoster('estream')
        if ('hdvid' in sHostName):
            return self.getHoster('hdvid')
        if ('streamango' in sHostName):
            return self.getHoster('streamango')
        if ('vidabc' in sHostName):
            return self.getHoster('vidabc')
        if ('vshare' in sHostName):
            return self.getHoster('vshare')
        if ('giga' in sHostName):
            return self.getHoster('giga')
        if ('vidbom' in sHostName):
            return self.getHoster('vidbom')
        if ('upvid.' in sHostName):
            return self.getHoster('upvid')
        if ('cloudvid' in sHostName):
            return self.getHoster('cloudvid')
        if ('clickopen' in sHostName):
            return self.getHoster('clickopen')
        if ('iframe-secured' in sHostName):
            return self.getHoster('iframe_secured')
        if ('goo.gl' in sHostName or 'bit.ly' in sHostName):
            return self.getHoster('allow_redirects')


        #Lien telechargeable a convertir en stream
        if ('1fichier' in sHostName):
            return self.getHoster('onefichier')
        if ('uptobox' in sHostName):
            return self.getHoster('uptobox')
        if ('uplea.com' in sHostName):
            return self.getHoster('uplea')
        if ('uploaded' in sHostName or 'ul.to' in sHostName):
            return self.getHoster('uploaded')

        if ('kaydo.ws' in sHostName):
            return self.getHoster('lien_direct')

        #Si aucun hebergeur connu on teste les liens directs
        if (sHosterUrl[-4:] in '.mp4.avi.flv.m3u8.webm'):
            return self.getHoster('lien_direct')

        return False

    def getHoster(self, sHosterFileName):
        exec "from resources.hosters." + sHosterFileName + " import cHoster"

        return cHoster()

    def play(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')
        sTitle = oInputParameterHandler.getValue('title')
        #sThumbnail = oInputParameterHandler.getValue('sThumbnail')

        if not sTitle:
            sTitle = sFileName

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        util.VSlog("Hoster - play " + sMediaUrl)

        oHoster = self.getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        sHosterName = oHoster.getDisplayName()
        cConfig().showInfo(sHosterName, 'Resolve')

        try:

            oHoster.setUrl(sMediaUrl)
            aLink = oHoster.getMediaLink()

            if (aLink[0] == True):
                oGuiElement = cGuiElement()
                oGuiElement.setSiteName(self.SITE_NAME)
                oGuiElement.setMediaUrl(aLink[1])
                oGuiElement.setTitle(sTitle)
                #oGuiElement.setTitle(oHoster.getFileName())
                oGuiElement.getInfoLabel()

                oPlayer = cPlayer()

                #sous titres ?
                if len(aLink) > 2:
                    oPlayer.AddSubtitles(aLink[2])

                oPlayer.run(oGuiElement, oHoster.getFileName(), aLink[1])
                return
            else:
                cConfig().error("Fichier introuvable")
                return

        except:
            cConfig().error("Fichier introuvable")
            return

        oGui.setEndOfDirectory()

    def addToPlaylist(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')
        bGetRedirectUrl = oInputParameterHandler.getValue('bGetRedirectUrl')
        sFileName = oInputParameterHandler.getValue('sFileName')

        if (bGetRedirectUrl == 'True'):
            sMediaUrl = self.__getRedirectUrl(sMediaUrl)

        util.VSlog("Hoster - play " + sMediaUrl)
        oHoster = self.getHoster(sHosterIdentifier)
        oHoster.setFileName(sFileName)

        oHoster.setUrl(sMediaUrl)
        aLink = oHoster.getMediaLink()

        if (aLink[0] == True):
            oGuiElement = cGuiElement()
            oGuiElement.setSiteName(self.SITE_NAME)
            oGuiElement.setMediaUrl(aLink[1])
            oGuiElement.setTitle(oHoster.getFileName())

            oPlayer = cPlayer()
            oPlayer.addItemToPlaylist(oGuiElement)
            oGui.showInfo('Playlist', str(oHoster.getFileName()), 5)
            return

        oGui.setEndOfDirectory()

    def __getRedirectUrl(self, sUrl):
        oRequest = cRequestHandler(sUrl)
        oRequest.request()
        return oRequest.getRealUrl()
