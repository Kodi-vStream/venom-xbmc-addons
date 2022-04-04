# -*- coding: utf-8 -*-
import json
import xbmc
import xbmcaddon
import xbmcvfs
import sys
import re
from base64 import b64encode
from resources.lib.comaddon import dialog, addon, addonManager, VSlog, isMatrix
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.util import UnquotePlus

# Utilisation de l'extension UpNext
# Documentation : https://github.com/im85288/service.upnext/wiki/Integration


class UpNext:
    # Prépare le lien du prochain épisode d'une série
    def nextEpisode(self, guiElement):

        # tester s'il s'agit d'une série
        if not guiElement.getItemValue('mediatype') == "episode":
            return

        # Demander d'installer l'extension
        if not self.use_up_next():
            return

        # La source
        oInputParameterHandler = cInputParameterHandler()
        sSiteName = oInputParameterHandler.getValue('sourceName')
        if not sSiteName:
            return

        # La saison
        sSaison = oInputParameterHandler.getValue('sSeason')

        # Calcule l'épisode suivant à partir de l'épisode courant
        sEpisode = oInputParameterHandler.getValue('sEpisode')
        if not sEpisode:
            sEpisode = str(guiElement.getEpisode())
            if not sEpisode:
                return  # impossible de déterminer l'épisode courant

        # tvShowTitle n'est pas toujours disponible.
        tvShowTitle = guiElement.getItemValue('tvshowtitle')
        if not tvShowTitle:
            tvShowTitle = re.search('\[\/COLOR\](.+?)\[COLOR', guiElement.getItemValue('title')).group(1)

        sMovieTitle = tvShowTitle

        numEpisode = int(sEpisode)
        nextEpisode = numEpisode + 1
        sNextEpisode = '%02d' % nextEpisode

        saisonUrl = oInputParameterHandler.getValue('saisonUrl')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', saisonUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        sParams = oOutputParameterHandler.getParameterAsUri()

        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        nextSaisonFunc = oInputParameterHandler.getValue('nextSaisonFunc')
        sLang = oInputParameterHandler.getValue('sLang')
        sTmdbId = oInputParameterHandler.getValue('sTmdbId')

        try:
            sHosterIdentifier, sMediaUrl, nextTitle, sDesc, sThumb = self.getMediaUrl(sSiteName, nextSaisonFunc, sParams, sSaison, nextEpisode, sLang, sHosterIdentifier)
            if not sMediaUrl:
                return

            sFileName = tvShowTitle.replace(' & ', ' and ')   # interdit dans un titre
            sFileName += ' - '
            if sSaison:
                sFileName += 'S%s' % sSaison
            sFileName += 'E%s' % sNextEpisode
            nextTitle = UnquotePlus(nextTitle)

            if sLang:
                nextTitle += ' (%s)' % sLang

            episodeTitle = nextTitle

            saisonUrl = oInputParameterHandler.getValue('saisonUrl')
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('sHosterIdentifier', sHosterIdentifier)
            oOutputParameterHandler.addParameter('sourceName', sSiteName)
            oOutputParameterHandler.addParameter('sFileName', sFileName)
            oOutputParameterHandler.addParameter('sTitle', sFileName)
            oOutputParameterHandler.addParameter('sCat', 8)  # Catégorie épisode
            oOutputParameterHandler.addParameter('sMeta', 6)  # Meta épisode
            oOutputParameterHandler.addParameter('sFav', 'play')
            oOutputParameterHandler.addParameter('sMediaUrl', str(sMediaUrl))
            oOutputParameterHandler.addParameter('saisonUrl', saisonUrl)
            oOutputParameterHandler.addParameter('nextSaisonFunc', nextSaisonFunc)
            oOutputParameterHandler.addParameter('sSeason', sSaison)
            oOutputParameterHandler.addParameter('sEpisode', sNextEpisode)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oOutputParameterHandler.addParameter('tvshowtitle', tvShowTitle)
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)

            sParams = oOutputParameterHandler.getParameterAsUri()
            url = 'plugin://plugin.video.vstream/?site=cHosterGui&function=play&%s' % sParams

            # sThumbnail = guiElement.getThumbnail()
            sThumbnail = sThumb

            nextInfo = dict(
                current_episode=dict(
                    episodeid=numEpisode,
                    tvshowid=0,
                    showtitle=tvShowTitle,
                    season=sSaison if sSaison else '',
                    episode='%02d' % numEpisode,
                    title='',
                    plot='',
                    art={
                        'thumb': sThumbnail,
                        'tvshow.clearart': '',
                        'tvshow.clearlogo': '',
                        'tvshow.fanart': '',
                        'tvshow.landscape': '',
                        'tvshow.poster': '',
                    },
                ),
                next_episode=dict(
                    episodeid=nextEpisode,
                    tvshowid=0,
                    showtitle=tvShowTitle,
                    season=sSaison if sSaison else '',  # déjà dans le titre
                    episode=sNextEpisode,  # déjà dans le titre
                    title=nextTitle,  # titre de l'épisode
                    plot=sDesc,
                    art={
                        'thumb': sThumbnail,
                        'tvshow.clearart': '',
                        'tvshow.clearlogo': '',
                        'tvshow.fanart': sThumbnail,  # guiElement.getFanart(),
                        'tvshow.landscape': sThumbnail,  # guiElement.getPoster(),
                        'tvshow.poster': sThumbnail,  # guiElement.getPoster(),
                    },
                ),
                play_url=url  # provide either `play_info` or `play_url`
            )

            self.notifyUpnext(nextInfo)
        except Exception as e:
            VSlog('UpNext : %s' % e)

    def getMediaUrl(self, sSiteName, sFunction, sParams, sSaison, iEpisode, sLang, sHosterIdentifier, sTitle='', sDesc='', sThumb=''):

        try:
            sys.argv[2] = '?%s' % sParams
            plugins = __import__('resources.sites.%s' % sSiteName, fromlist=[sSiteName])
            function = getattr(plugins, sFunction)
            function()
        except Exception as e:
            VSlog('could not load site: ' + sSiteName + ' error: ' + str(e))
            return None, None, None, None, None

        sMediaUrl = ''
        for sUrl, listItem, isFolder in cGui().getEpisodeListing():
            sParams = sUrl.split('?', 1)[1]
            aParams = dict(param.split('=') for param in sParams.split('&'))
            sFunction = aParams['function']
            if sFunction == 'DoNothing':
                continue

            if sLang and 'sLang' in aParams and UnquotePlus(aParams['sLang']) != sLang:
                continue           # La langue est connue, mais ce n'est pas la bonne

            if sSaison and 'sSeason' in aParams and aParams['sSeason'] and int(aParams['sSeason']) != int(sSaison):
                continue           # La saison est connue, mais ce n'est pas la bonne

            if 'sEpisode' in aParams and aParams['sEpisode'] and int(aParams['sEpisode']) != iEpisode:
                continue           # L'épisode est connu, mais ce n'est pas le bon

            sMediaUrl = aParams['sMediaUrl'] if 'sMediaUrl' in aParams else None
            infoTag = listItem.getVideoInfoTag()
            tagLine = infoTag.getTagLine()
            if tagLine:
                sTitle = tagLine
            else:
                sTitle = listItem.getLabel()

            if not sDesc:
                sDesc = infoTag.getPlot()

            if not sTitle:
                sTitle = UnquotePlus(aParams['sTitle']) if 'sTitle' in aParams else None
            if 'sHost' in aParams and aParams['sHost']:
                oHoster = cHosterGui().checkHoster(aParams['sHost'])
                if not oHoster:
                    continue
                hostName = oHoster.getPluginIdentifier()
                if hostName != sHosterIdentifier:
                    continue

            hostName = sHosterIdentifier
            if 'sHosterIdentifier' in aParams:
                hostName = aParams['sHosterIdentifier']
                if hostName != sHosterIdentifier:
                    continue

            sThumb = listItem.getArt('thumb')
            if 'sThumb' in aParams and aParams['sThumb']:
                sThumb = UnquotePlus(aParams['sThumb'])
            if not sDesc and 'sDesc' in aParams and aParams['sDesc']:
                sDesc = UnquotePlus(aParams['sDesc'])

            if sMediaUrl:
                return hostName, sMediaUrl, sTitle, sDesc, sThumb

            # if sFunction != 'play':
            return self.getMediaUrl(sSiteName, sFunction, sParams, sSaison, iEpisode, sLang, sHosterIdentifier, sTitle, sDesc, sThumb)

        if sMediaUrl:    # si on n'a pas trouvé le bon host on en retourne un autre, il pourrait fonctionner
            return hostName, sMediaUrl, sTitle, sDesc, sThumb

        return None, None, None, None, None

    # Envoi des infos à l'addon UpNext
    def notifyUpnext(self, data):

        try:
            next_data = json.dumps(data)
            # if not isinstance(next_data, bytes):
            next_data = next_data.encode('utf-8')
            data = b64encode(next_data)
            if isMatrix():
                data = data.decode('ascii')

            jsonrpc_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "JSONRPC.NotifyAll",
                "params": {
                    "sender": "%s.SIGNAL" % 'plugin.video.vStream',
                    "message": 'upnext_data',
                    "data": [data],
                }
            }

            request = json.dumps(jsonrpc_request)
            response = xbmc.executeJSONRPC(request)
            response = json.loads(response)
            return response['result'] == 'OK'

        except Exception as e:
            import traceback
            traceback.print_exc()
            return False

    # Charge l'addon UpNext, ou l'installe à la demande
    def use_up_next(self):

        addons = addon()
        if addons.getSetting('upnext') == 'false':
            return False

        upnext_id = 'service.upnext'
        try:
            # tente de charger UpNext pour tester sa présence
            xbmcaddon.Addon(upnext_id)
            return True
        except RuntimeError:    # Addon non installé ou désactivé
            if not dialog().VSyesno(addons.VSlang(30505)):  # Voulez-vous l'activer ?
                addons.setSetting('upnext', 'false')
                return False

            addon_xml = xbmc.translatePath('special://home/addons/%s/addon.xml' % upnext_id)
            if xbmcvfs.exists(addon_xml):  # si addon.xml existe, add-on présent mais désactivé

                # Impossible d'activer UpNext ou si on confirme de ne pas vouloir l'utiliser
                if not addonManager().enableAddon(upnext_id):
                    addons.setSetting('upnext', 'false')
                    return False

                return True  # addon activé
            else:                          # UpNext non installé, on l'installe et on l'utilise
                addonManager().installAddon(upnext_id)
                # ce n'est pas pris en compte à l'installation de l'addon, donc return False, il faudra attendre le prochain épisode
                return False
