# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import copy
import json
import threading
import xbmc
import xbmcplugin
import sys

from resources.lib.comaddon import listitem, addon, dialog, window, isNexus, progress, VSlog
from resources.lib.gui.contextElement import cContextElement
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.util import QuotePlus, cUtil
#from resources.lib.util import , Unquote


class cGui:

    SITE_NAME = 'cGui'
    CONTENT = ''
    listing = []
    thread_listing = []
    episodeListing = []  # Pour gérer l'enchainement des episodes
    ADDON = addon()
    displaySeason = ADDON.getSetting('display_season_title')

    # Gérer les résultats de la recherche
    searchResults = {}
    searchResultsSemaphore = threading.Semaphore()

    def getEpisodeListing(self):
        return self.episodeListing

    def addNewDir(self, Type, sId, sFunction, sLabel, sIcon, sThumbnail='', sDesc='', oOutputParameterHandler=cOutputParameterHandler(), sMeta=0, sCat=None):
        oGuiElement = cGuiElement()
        # dir ou link => CONTENT par défaut = files
        if Type != 'dir' and Type != 'link':
            cGui.CONTENT = Type
        if sCat is not None:
            oGuiElement.setCat(sCat)
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setIcon(sIcon)

        if sThumbnail == '':
            oGuiElement.setThumbnail(oGuiElement.getIcon())
        else:
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setPoster(sThumbnail)

        oGuiElement.setDescription(sDesc)

        # Pour addLink on recupere le sCat et sMeta precedent.
        oInputParameterHandler = None
        if Type == 'link':
            oInputParameterHandler = cInputParameterHandler()
            sCat = oInputParameterHandler.getValue('sCat')
            if sCat:
                sCat = int(sCat)
                oGuiElement.setCat(sCat)

            sMeta = oInputParameterHandler.getValue('sMeta')
            if sMeta:
                sMeta = int(sMeta)
                oGuiElement.setMeta(sMeta)
        else:
            oOutputParameterHandler.addParameter('sMeta', sMeta)
            oGuiElement.setMeta(sMeta)

        # a faire après avoir déterminé la cat et le meta
        oGuiElement.setTitle(sLabel)


        # Si pas d'id TMDB pour un episode, on recupère le précédent qui vient de la série
        sTmdbId = oOutputParameterHandler.getValue('sTmdbId')
        if sCat and not sTmdbId:
            # pas pendant la recherche globale
            if window(10101).getProperty('search') != 'true':
                if not sMeta:
                    if not oInputParameterHandler:
                        oInputParameterHandler = cInputParameterHandler()
                    sMeta = int(oInputParameterHandler.getValue('sMeta'))
                if 0 < sMeta < 7:
                    if not oInputParameterHandler:
                        oInputParameterHandler = cInputParameterHandler()
                    sTmdbId = oInputParameterHandler.getValue('sTmdbId')
                    if sTmdbId:
                        oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)

        oOutputParameterHandler.addParameter('sFav', sFunction)

        resumeTime = oOutputParameterHandler.getValue('ResumeTime')
        if resumeTime:
            oGuiElement.setResumeTime(resumeTime)
            oGuiElement.setTotalTime(oOutputParameterHandler.getValue('TotalTime'))

        # Lecture en cours
        isViewing = oOutputParameterHandler.getValue('isViewing')
        if isViewing:
            oGuiElement.addItemProperties('isViewing', True)

        sTitle = oOutputParameterHandler.getValue('sMovieTitle')
        if sTitle:
            oGuiElement.setFileName(sTitle)
        else:
            oGuiElement.setFileName(sLabel)

        # si pas d'info fourni en spécifique, récupéré celle de la navigation précédente
        if sCat and not sThumbnail and not sTmdbId:
            oGuiElement.getInfoLabel()

        try:
            return self.addFolder(oGuiElement, oOutputParameterHandler)
        except Exception as error:
            VSlog("addNewDir error: " + str(error))

    #    Categorie       Meta          sCat     CONTENT
    #    Film            1             1        movies
    #    Serie           2             2        tvshows
    #    Anime           4             3        tvshows
    #    Saison          5             4        episodes
    #    Divers          0             5        videos
    #    IPTV (Officiel) 0             6        files
    #    Saga            3             7        movies
    #    Episodes        6             8        episodes
    #    Drama           2             9        tvshows
    #    Person          7             /        artists
    #    Network         8             /        files

    def addMovie(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        movieUrl = oOutputParameterHandler.getValue('siteUrl')
        oOutputParameterHandler.addParameter('movieUrl', QuotePlus(movieUrl))
        oOutputParameterHandler.addParameter('movieFunc', sFunction)
        return self.addNewDir('movies', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 1, 1)

    def addTV(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        # Pour gérer l'enchainement des épisodes
        saisonUrl = oOutputParameterHandler.getValue('siteUrl')
        if saisonUrl:
            oOutputParameterHandler.addParameter('saisonUrl', QuotePlus(saisonUrl))
            oOutputParameterHandler.addParameter('nextSaisonFunc', sFunction)

        return self.addNewDir('tvshows', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 2, 2)

    def addAnime(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        # Pour gérer l'enchainement des épisodes
        saisonUrl = oOutputParameterHandler.getValue('siteUrl')
        if saisonUrl:
            oOutputParameterHandler.addParameter('saisonUrl', QuotePlus(saisonUrl))
            oOutputParameterHandler.addParameter('nextSaisonFunc', sFunction)

        return self.addNewDir('tvshows', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 4, 3)

    def addDrama(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        # Pour gérer l'enchainement des épisodes
        saisonUrl = oOutputParameterHandler.getValue('siteUrl')
        if saisonUrl:
            oOutputParameterHandler.addParameter('saisonUrl', QuotePlus(saisonUrl))
            oOutputParameterHandler.addParameter('nextSaisonFunc', sFunction)

        return self.addNewDir('tvshows', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 2, 9)

    def addMisc(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        if sThumbnail or sDesc:
            cat = 'videos'
        else:
            cat = 'files'
        movieUrl = oOutputParameterHandler.getValue('siteUrl')
        oOutputParameterHandler.addParameter('movieUrl', QuotePlus(movieUrl))
        oOutputParameterHandler.addParameter('movieFunc', sFunction)
        return self.addNewDir(cat, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 0, 5)

    def addMoviePack(self, sId, sFunction, sLabel, sThumbnail, sDesc, oOutputParameterHandler=''):
        return self.addNewDir('sets', sId, sFunction, sLabel, 'no-image.png', sThumbnail, sDesc, oOutputParameterHandler, 3, 7)

    def addGenre(self, sId, sFunction, sLabel, oOutputParameterHandler='', sDesc=""):
        sIcon = 'genres/%s.png' % str(cUtil().formatUTF8(sLabel))
        sIcon = sIcon.replace(' & ', '_').replace(' ', '_').replace("'", '_').replace("-", '_')
        return self.addNewDir('dir', sId, sFunction, sLabel, sIcon, '', sDesc, oOutputParameterHandler, 0, None)

    def addDir(self, sId, sFunction, sLabel, sIcon, oOutputParameterHandler=cOutputParameterHandler(), sDesc=""):
        return self.addNewDir('dir', sId, sFunction, sLabel, sIcon, '', sDesc, oOutputParameterHandler, 0, None)

    def addLink(self, sId, sFunction, sLabel, sThumbnail, sDesc, oOutputParameterHandler=''):
        # Pour gérer l'enchainement des épisodes
        oInputParameterHandler = cInputParameterHandler()
        oOutputParameterHandler.addParameter('saisonUrl', oInputParameterHandler.getValue('saisonUrl'))
        oOutputParameterHandler.addParameter('nextSaisonFunc', oInputParameterHandler.getValue('nextSaisonFunc'))
        oOutputParameterHandler.addParameter('movieUrl', oInputParameterHandler.getValue('movieUrl'))
        oOutputParameterHandler.addParameter('movieFunc', oInputParameterHandler.getValue('movieFunc'))

        if not oOutputParameterHandler.getValue('sLang'):
            oOutputParameterHandler.addParameter('sLang', oInputParameterHandler.getValue('sLang'))

        if not oOutputParameterHandler.getValue('sRes'):
            oOutputParameterHandler.addParameter('sRes', oInputParameterHandler.getValue('sRes'))

        sIcon = sThumbnail
        return self.addNewDir('link', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 0, None)

    def addSeason(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        # Pour gérer l'enchainement des épisodes
        saisonUrl = oOutputParameterHandler.getValue('siteUrl')
        oOutputParameterHandler.addParameter('saisonUrl', QuotePlus(saisonUrl))
        oOutputParameterHandler.addParameter('nextSaisonFunc', sFunction)

        return self.addNewDir('seasons', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 5, 4)

    def addEpisode(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        # Pour gérer l'enchainement des épisodes, l'URL de la saison
        oInputParameterHandler = cInputParameterHandler()
        saisonUrl = oInputParameterHandler.getValue('saisonUrl')
        if saisonUrl:   # Retenu depuis "addSeason"
            oOutputParameterHandler.addParameter('saisonUrl', saisonUrl)
            oOutputParameterHandler.addParameter('nextSaisonFunc', oInputParameterHandler.getValue('nextSaisonFunc'))
        else:           # calculé depuis l'url qui nous a emmené ici sans passé par addSeason
            oOutputParameterHandler.addParameter('saisonUrl', oInputParameterHandler.getValue('siteUrl'))
            oOutputParameterHandler.addParameter('nextSaisonFunc', oInputParameterHandler.getValue('function'))

        if not oOutputParameterHandler.getValue('sLang'):
            oOutputParameterHandler.addParameter('sLang', oInputParameterHandler.getValue('sLang'))

        if not oOutputParameterHandler.getValue('sRes'):
            oOutputParameterHandler.addParameter('sRes', oInputParameterHandler.getValue('sRes'))

        return self.addNewDir('episodes', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 6, 8)

    # Affichage d'une personne (acteur, réalisateur, ..)
    def addPerson(self, sId, sFunction, sLabel, sIcon, sThumbnail, oOutputParameterHandler=''):
        sDesc = ''
        return self.addNewDir('artists', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 7, None)

    # Affichage d'un réseau de distribution du média
    def addNetwork(self, sId, sFunction, sLabel, sIcon, oOutputParameterHandler=''):
        sThumbnail = ''
        sDesc = ''
        return self.addNewDir('', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 8, None)

    def addNext(self, sId, sFunction, sLabel, oOutputParameterHandler):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        
        sDecoColor = self.ADDON.getSetting('deco_color')

        oGuiElement.setTitle('[COLOR %s]%s >[/COLOR]' % (sDecoColor, sLabel))
        oGuiElement.setIcon('next.png')
        oGuiElement.setThumbnail(oGuiElement.getIcon())
        oGuiElement.setMeta(0)
        # oGuiElement.setCat(5)

        self.createContexMenuPageSelect(oGuiElement, oOutputParameterHandler)
#        self.createContexMenuViewBack(oGuiElement, oOutputParameterHandler)
        return self.addFolder(oGuiElement, oOutputParameterHandler)

    # utiliser oGui.addText(SITE_IDENTIFIER)
    def addNone(self, sId):
        return self.addText(sId)

    def addText(self, sId, sLabel='', sIcon='none.png'):
        # Pas de texte lors des recherches globales
        if window(10101).getProperty('search') == 'true':
            return

        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction('DoNothing')
        if not sLabel:
            sLabel = self.ADDON.VSlang(30204)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setThumbnail(oGuiElement.getIcon())
        oGuiElement.setMeta(0)

        oOutputParameterHandler = cOutputParameterHandler()
        return self.addFolder(oGuiElement, oOutputParameterHandler)

    # afficher les liens non playable
    def addFolder(self, oGuiElement, oOutputParameterHandler='', _isFolder=True):
        if _isFolder is False:
            cGui.CONTENT = 'files'

        # recherche append les reponses
        if window(10101).getProperty('search') == 'true':
            self.addSearchResult(oGuiElement, oOutputParameterHandler)
            return

        # Des infos a rajouter ?
        params = {'siteUrl': oGuiElement.setSiteUrl,
                  'sTmdbId': oGuiElement.setTmdbId,
                  'sYear': oGuiElement.setYear,
                  'sRes': oGuiElement.setRes}

        try:  # Py2
            for sParam, callback in params.iteritems():
                value = oOutputParameterHandler.getValue(sParam)
                if value:
                    callback(value)

        except AttributeError:  # py3
            for sParam, callback in params.items():
                value = oOutputParameterHandler.getValue(sParam)
                if value:
                    callback(value)

        oListItem = self.createListItem(oGuiElement)

        sCat = oGuiElement.getCat()
        if sCat:
            cGui.sCat = sCat
            oOutputParameterHandler.addParameter('sCat', sCat)

        sItemUrl = self.__createItemUrl(oGuiElement, oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sTitleWatched', oGuiElement.getTitleWatched())

        oListItem = self.__createContextMenu(oGuiElement, oListItem)

        if _isFolder is True:
            # oListItem.setProperty('IsPlayable', 'true')
            if sCat:    # 1 = movies, moviePack; 2 = series, animes, episodes; 5 = MISC
                if oGuiElement.getMeta():
                    self.createContexMenuinfo(oGuiElement, oOutputParameterHandler)
                    self.createContexMenuba(oGuiElement, oOutputParameterHandler)
                if not oListItem.getProperty('isBookmark'):
                    self.createContexMenuBookmark(oGuiElement, oOutputParameterHandler)

                if sCat in (1, 2, 3, 4, 8, 9):
                    if self.ADDON.getSetting('bstoken') != '':
                        self.createContexMenuTrakt(oGuiElement, oOutputParameterHandler)
                    if self.ADDON.getSetting('tmdb_account') != '':
                        self.createContexMenuTMDB(oGuiElement, oOutputParameterHandler)
                if sCat in (1, 2, 3, 4, 9):
                    self.createContexMenuSimil(oGuiElement, oOutputParameterHandler)
                if sCat != 6:
                    self.createContexMenuWatch(oGuiElement, oOutputParameterHandler)
        else:
            oListItem.setProperty('IsPlayable', 'true')
            self.createContexMenuWatch(oGuiElement, oOutputParameterHandler)

        oListItem = self.__createContextMenu(oGuiElement, oListItem)
        self.listing.append((sItemUrl, oListItem, _isFolder))

        # Vider les paramètres pour être recyclé
        oOutputParameterHandler.clearParameter()
        return oListItem

    def createListItem(self, oGuiElement):

        # Récupération des metadonnées par thread
        if oGuiElement.getMeta() and oGuiElement.getMetaAddon() == 'true':
            return self.createListItemThread(oGuiElement)

        # pas de meta, appel direct
        return self._createListItem(oGuiElement)

    # Utilisation d'un Thread pour un chargement des metas en parallèle
    def createListItemThread(self, oGuiElement):
        itemTitle = oGuiElement.getTitle()
        oListItem = listitem(itemTitle)
        t = threading.Thread(target=self._createListItem, name=itemTitle, args=(oGuiElement, oListItem))
        self.thread_listing.append(t)
        t.start()
        return oListItem

    def _createListItem(self, oGuiElement, oListItem=None):

        # Enleve les elements vides
        data = {key: val for key, val in oGuiElement.getItemValues().items() if val != ""}

        itemTitle = oGuiElement.getTitle()

        sMediaUrl = oGuiElement.getMediaUrl()

        # Formatage nom episode
        sCat = oGuiElement.getCat()
        if sCat and int(sCat) == 8:  # Nom de l'épisode
            try:
                if 'tagline' in data and data['tagline']:
                    episodeTitle = data['tagline']
                else:
                    episodeTitle = 'Episode ' + str(data['episode'])
                host = ''
                if 'tvshowtitle' in data:
                    idxTitle = itemTitle.split(data['tvshowtitle'])
                    if len(idxTitle) >= 2:
                        host = idxTitle[1]
                if self.displaySeason == "true":
                    itemTitle = str(data['season']) + "x" + str(data['episode']) + ". " + episodeTitle
                else:
                    itemTitle = episodeTitle
                if len(host) > 3:
                    itemTitle += " " + host
                data['title'] = itemTitle
            except:
                data['title'] = itemTitle
                pass
            
            # release du lien
            if sMediaUrl:
                if self.ADDON.getSetting('display_info_file') == 'true':
                    data['plot'] = sMediaUrl
        else:
            # Permet d'afficher toutes les informations pour les films.
            data['title'] = itemTitle
            if sMediaUrl:   # release du lien
                if self.ADDON.getSetting('display_info_file') == 'true':
                    data['tagline'] = sMediaUrl
            
    # affiche tag HD
        # https://alwinesch.github.io/group__python__xbmcgui__listitem.html#ga99c7bf16729b18b6378ea7069ee5b138
        sRes = oGuiElement.getRes()
        if ":" in str(data.get('duration')):
            # Convertion en seconde, utile pour le lien final.
            data['duration'] = (sum(x * int(t) for x, t in zip([1, 60, 3600], reversed(data.get('duration', '').split(":")))))

        if not oListItem:
            oListItem = listitem(itemTitle)

        if data.get('cast'):
            casts = json.loads(data['cast'])
            data['cast'] = []
            for i in casts:
                if isNexus():
                    data['cast'].append(xbmc.Actor(i['name'], i['character'], i['order'], i.get('thumbnail', "")))
                else:
                    data['cast'].append((i['name'], i['character'], i['order'], i.get('thumbnail', "")))

        if not isNexus():
            # voir : https://kodi.wiki/view/InfoLabels
            oListItem.setInfo(oGuiElement.getType(), data)
            if sRes:
                if '2160' in sRes:
                    oListItem.addStreamInfo('video', {'width': 3840, 'height': 2160})
                elif '1080' in sRes:
                    oListItem.addStreamInfo('video', {'width': 1920, 'height': 1080})
                elif '720' in sRes:
                    oListItem.addStreamInfo('video', {'width': 1280, 'height': 720})
                elif '480' in sRes:
                    oListItem.addStreamInfo('video', {'width': 720, 'height': 576})
        else:
            videoInfoTag = oListItem.getVideoInfoTag()

            # https://alwinesch.github.io/class_x_b_m_c_addon_1_1xbmc_1_1_info_tag_video.html
            # https://alwinesch.github.io/group__python___info_tag_video.html
            # gestion des valeurs par defaut si non renseignées
            videoInfoTag.setMediaType(data.get('mediatype', ''))
            videoInfoTag.setTitle(data.get('title', ""))
            videoInfoTag.setTvShowTitle(data.get('tvshowtitle', ''))
            videoInfoTag.setOriginalTitle(data.get('originaltitle', ""))
            videoInfoTag.setPlot(data.get('plot', ""))
            videoInfoTag.setPlotOutline(data.get('tagline', ""))
            videoInfoTag.setYear(int(data.get('year', 0)))
            videoInfoTag.setRating(float(data.get('rating', 0.0)))
            videoInfoTag.setMpaa(data.get('mpaa', ""))
            videoInfoTag.setDuration(int(data.get('duration', 0)))
            videoInfoTag.setPlaycount(int(data.get('playcount', 0)))
            # inutilisé ? et fragile 
            # videoInfoTag.setCountries(data.get('country', ['']))
            videoInfoTag.setTrailer(data.get('trailer', ""))
            videoInfoTag.setTagLine(data.get('tagline', ""))
            videoInfoTag.setStudios(list(data.get('studio', '').split("/")))
            videoInfoTag.setWriters(list(data.get('writer', '').split("/")))
            videoInfoTag.setDirectors(list(data.get('director', '').split("/")))
            videoInfoTag.setGenres(''.join(data.get('genre', [""])).split('/'))
            videoInfoTag.setSeason(int(data.get('season') or "-1"))
            videoInfoTag.setEpisode(int(data.get('episode') or "-1"))
            videoInfoTag.setResumePoint(float(data.get('resumetime', 0.0)), float(data.get('totaltime', 0.0)))

            videoInfoTag.setCast(data.get('cast', []))

            if sRes:
                width = None
                if '2160' in sRes:
                    width = 3840
                    height = 2160
                elif '1080' in sRes:
                    width = 1920
                    height = 1080
                elif '720' in sRes:
                    width = 1280
                    height = 720
                elif '480' in sRes:
                    width = 720
                    height = 576
                
                if width:
                    # [width, height, aspect, duration, codec, stereoMode, language])
                    videoStreamDetail = xbmc.VideoStreamDetail(width=width, height=height)
                    videoInfoTag.addVideoStream(videoStreamDetail)

    
        oListItem.setArt({
                          'poster': oGuiElement.getPoster(),
                          'thumb': oGuiElement.getThumbnail(),
                          'icon': oGuiElement.getIcon(),
                          'fanart': oGuiElement.getFanart()})

        aProperties = oGuiElement.getItemProperties()
        for sPropertyKey, sPropertyValue in aProperties.items():
            oListItem.setProperty(sPropertyKey, str(sPropertyValue))

        return oListItem

    # Marquer vu/Non vu
    def createContexMenuWatch(self, oGuiElement, oOutputParameterHandler=''):
        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cGui', oGuiElement.getSiteName(), 'setWatched', self.ADDON.VSlang(30206))

    def createContexMenuPageSelect(self, oGuiElement, oOutputParameterHandler):
        oContext = cContextElement()
        oContext.setFile('cGui')
        oContext.setSiteName('cGui')
        oContext.setFunction('selectPage')
        oContext.setTitle(self.ADDON.VSlang(30017))
        oOutputParameterHandler.addParameter('OldFunction', oGuiElement.getFunction())
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)

    def createContexMenuViewBack(self, oGuiElement, oOutputParameterHandler):
        oContext = cContextElement()
        oContext.setFile('cGui')
        oContext.setSiteName('cGui')
        oContext.setFunction('viewBack')
        oContext.setTitle(self.ADDON.VSlang(30018))
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)

    # marque page
    def createContexMenuBookmark(self, oGuiElement, oOutputParameterHandler=''):
        oOutputParameterHandler.addParameter('sCleanTitle', oGuiElement.getCleanTitle())
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oOutputParameterHandler.addParameter('sFav', oGuiElement.getFunction())
        oOutputParameterHandler.addParameter('sCat', oGuiElement.getCat())

        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cFav', 'cFav', 'setBookmark', self.ADDON.VSlang(30210))

    def createContexMenuTrakt(self, oGuiElement, oOutputParameterHandler=''):
        oOutputParameterHandler.addParameter('sImdbId', oGuiElement.getImdbId())
        oOutputParameterHandler.addParameter('sTmdbId', oGuiElement.getTmdbId())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())

        sType = cGui.CONTENT.replace('tvshows', 'shows')
        oOutputParameterHandler.addParameter('sType', sType)
        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cTrakt', 'cTrakt', 'getAction', self.ADDON.VSlang(30214))

    def createContexMenuTMDB(self, oGuiElement, oOutputParameterHandler=''):
        oOutputParameterHandler.addParameter('sImdbId', oGuiElement.getImdbId())
        oOutputParameterHandler.addParameter('sTmdbId', oGuiElement.getTmdbId())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())

        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'themoviedb_org', 'themoviedb_org', 'getAction', 'TMDB')

    def createContexMenuDownload(self, oGuiElement, oOutputParameterHandler='', status='0'):
        if status == '0':
            self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'StartDownloadOneFile', self.ADDON.VSlang(30215))

        if status == '0' or status == '2':
            self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'delDownload', self.ADDON.VSlang(30216))
            self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'DelFile', self.ADDON.VSlang(30217))

        if status == '1':
            self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'StopDownloadList', self.ADDON.VSlang(30218))

        if status == '2':
            self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'ReadDownload', self.ADDON.VSlang(30219))
            self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'ResetDownload', self.ADDON.VSlang(30220))

    # Information
    def createContexMenuinfo(self, oGuiElement, oOutputParameterHandler=''):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sTitle', oGuiElement.getCleanTitle())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oOutputParameterHandler.addParameter('sMeta', oGuiElement.getMeta())
        oOutputParameterHandler.addParameter('sYear', oGuiElement.getYear())
        oOutputParameterHandler.addParameter('sFav', oGuiElement.getFunction())
        oOutputParameterHandler.addParameter('sCat', oGuiElement.getCat())

        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cGui', oGuiElement.getSiteName(), 'viewInfo', self.ADDON.VSlang(30208))

    # Bande annonce
    def createContexMenuba(self, oGuiElement, oOutputParameterHandler=''):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sTitle', oGuiElement.getTitle())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())
        oOutputParameterHandler.addParameter('sYear', oGuiElement.getYear())
        oOutputParameterHandler.addParameter('sTrailerUrl', oGuiElement.getTrailer())
        oOutputParameterHandler.addParameter('sMeta', oGuiElement.getMeta())

        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cGui', oGuiElement.getSiteName(), 'viewBA', self.ADDON.VSlang(30212))

    # Recherche similaire
    def createContexMenuSimil(self, oGuiElement, oOutputParameterHandler=''):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', oGuiElement.getCat())
        oOutputParameterHandler.addParameter('sTitle', oGuiElement.getTitle())
        sFileName = oGuiElement.getItemValue('tvshowtitle')
        if not sFileName:
            sFileName = oGuiElement.getFileName()
        oOutputParameterHandler.addParameter('sFileName', sFileName)

        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cGui', oGuiElement.getSiteName(), 'viewSimil', self.ADDON.VSlang(30213))

    def createSimpleMenu(self, oGuiElement, oOutputParameterHandler, sFile, sName, sFunction, sTitle):
        oContext = cContextElement()
        oContext.setFile(sFile)
        oContext.setSiteName(sName)
        oContext.setFunction(sFunction)
        oContext.setTitle(sTitle)

        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)

    def createContexMenuDelFav(self, oGuiElement, oOutputParameterHandler=''):
        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'cFav', 'cFav', 'delBookmarksMenu', self.ADDON.VSlang(30209))

    def createContexMenuSettings(self, oGuiElement, oOutputParameterHandler=''):
        self.createSimpleMenu(oGuiElement, oOutputParameterHandler, 'globalParametre', 'globalParametre', 'opensetting', self.ADDON.VSlang(30023))

    def __createContextMenu(self, oGuiElement, oListItem):
        sPluginPath = cPluginHandler().getPluginPath()
        aContextMenus = []

        # Menus classiques reglés a la base
        nbContextMenu = len(oGuiElement.getContextItems())
        if nbContextMenu > 0:
            sDecoColor = self.ADDON.getSetting('deco_color')
            for oContextItem in oGuiElement.getContextItems():
                oOutputParameterHandler = oContextItem.getOutputParameterHandler()
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)
                titleMenu = '[COLOR %s]%s[/COLOR]' % (sDecoColor, oContextItem.getTitle())
                aContextMenus += [(titleMenu, 'RunPlugin(%s)' % sTest)]

            oListItem.addContextMenuItems(aContextMenus)
        oListItem.setProperty('nbcontextmenu', str(nbContextMenu))

        return oListItem

    def __createItemUrl(self, oGuiElement, oOutputParameterHandler=''):
        if oOutputParameterHandler == '':
            oOutputParameterHandler = cOutputParameterHandler()

        # On descend l'id TMDB dans les saisons et les épisodes
        oOutputParameterHandler.addParameter('sTmdbId', oGuiElement.getTmdbId())

        # Pour gérer l'enchainement des épisodes
        oOutputParameterHandler.addParameter('sSeason', oGuiElement.getSeason())
        oOutputParameterHandler.addParameter('sEpisode', oGuiElement.getEpisode())

        sParams = oOutputParameterHandler.getParameterAsUri()

        sPluginPath = cPluginHandler().getPluginPath()

        if len(oGuiElement.getFunction()) == 0:
            sItemUrl = '%s?site=%s&title=%s&%s' % (sPluginPath, oGuiElement.getSiteName(), QuotePlus(oGuiElement.getCleanTitle()), sParams)
        else:
            sItemUrl = '%s?site=%s&function=%s&title=%s&%s' % (sPluginPath, oGuiElement.getSiteName(), oGuiElement.getFunction(), QuotePlus(oGuiElement.getCleanTitle()), sParams)

        return sItemUrl

    def setEndOfDirectory(self, forceViewMode=False):
        iHandler = cPluginHandler().getPluginHandle()

        if not self.listing:
            self.addText('cGui')

        # attendre l'arret des thread utilisés pour récupérer les métadonnées
        total = len(self.thread_listing)
        if total > 0:
            progress_ = progress().VScreate(self.ADDON.VSlang(30141))
            for thread in self.thread_listing:
                progress_.VSupdate(progress_, total)
                thread.join(100)
            progress_.VSclose(progress_)

        del self.thread_listing[:]

        xbmcplugin.addDirectoryItems(iHandler, self.listing, len(self.listing))
        xbmcplugin.setPluginCategory(iHandler, '')
        xbmcplugin.setContent(iHandler, cGui.CONTENT)
        if cGui.CONTENT == 'episodes':
            xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_EPISODE)
        else:
            xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(iHandler, succeeded=True, cacheToDisc=True)
        # reglage vue
        # 50 = liste / 51 grande liste / 500 icone / 501 gallerie / 508 fanart /
        if forceViewMode:
            xbmc.executebuiltin('Container.SetViewMode(' + str(forceViewMode) + ')')
        else:
            if self.ADDON.getSetting('active-view') == 'true':
                if cGui.CONTENT == 'movies' or cGui.CONTENT == 'artists':
                    # xbmc.executebuiltin('Container.SetViewMode(507)')
                    xbmc.executebuiltin('Container.SetViewMode(%s)' % self.ADDON.getSetting('movies-view'))
                elif cGui.CONTENT in ['tvshows', 'seasons', 'episodes']:
                    xbmc.executebuiltin('Container.SetViewMode(%s)' % self.ADDON.getSetting(cGui.CONTENT + '-view'))
                elif cGui.CONTENT == 'files':
                    xbmc.executebuiltin('Container.SetViewMode(%s)' % self.ADDON.getSetting('default-view'))

        del self.episodeListing[:]  # Pour l'enchainement des episodes
        self.episodeListing.extend(self.listing)

        del self.listing[:]

    def updateDirectory(self):  # refresh the content
        xbmc.executebuiltin('Container.Refresh')
        xbmc.sleep(600)    # Nécessaire pour laisser le temps du refresh

    def viewBA(self):
        oInputParameterHandler = cInputParameterHandler()
        sFileName = oInputParameterHandler.getValue('sFileName')
        sYear = oInputParameterHandler.getValue('sYear')
        sTrailerUrl = oInputParameterHandler.getValue('sTrailerUrl')
        sMeta = oInputParameterHandler.getValue('sMeta')

        from resources.lib.ba import cShowBA
        cBA = cShowBA()
        cBA.SetSearch(sFileName)
        cBA.SetYear(sYear)
        cBA.SetTrailerUrl(sTrailerUrl)
        cBA.SetMetaType(sMeta)
        cBA.SearchBA()

    def viewBack(self):
        sPluginPath = cPluginHandler().getPluginPath()
        oInputParameterHandler = cInputParameterHandler()
        # sParams = oInputParameterHandler.getAllParameter()
        sId = oInputParameterHandler.getValue('sId')
        sTest = '%s?site=%s' % (sPluginPath, sId)

        xbmc.executebuiltin('Container.Update(%s, replace)' % sTest)

    def viewInfo(self):
        if self.ADDON.getSetting('information-view') == "false":
            from resources.lib.config import WindowsBoxes

            oInputParameterHandler = cInputParameterHandler()
            sCleanTitle = oInputParameterHandler.getValue('sTitle') if oInputParameterHandler.exist('sTitle') else xbmc.getInfoLabel('ListItem.Title')
            sMeta = oInputParameterHandler.getValue('sMeta') if oInputParameterHandler.exist('sMeta') else xbmc.getInfoLabel('ListItem.Property(sMeta)')
            sYear = oInputParameterHandler.getValue('sYear') if oInputParameterHandler.exist('sYear') else xbmc.getInfoLabel('ListItem.Year')
            sUrl = oInputParameterHandler.getValue('siteUrl') if oInputParameterHandler.exist('siteUrl') else xbmc.getInfoLabel('ListItem.Property(siteUrl)')
            sSite = oInputParameterHandler.getValue('sId') if oInputParameterHandler.exist('sId') else xbmc.getInfoLabel('ListItem.Property(sId)')
            sFav = oInputParameterHandler.getValue('sFav') if oInputParameterHandler.exist('sFav') else xbmc.getInfoLabel('ListItem.Property(sFav)')
            sCat = oInputParameterHandler.getValue('sCat') if oInputParameterHandler.exist('sCat') else xbmc.getInfoLabel('ListItem.Property(sCat)')

            WindowsBoxes(sCleanTitle, sUrl, sMeta, sYear, sSite, sFav, sCat)
        else:
            # On appel la fonction integrée a Kodi pour charger les infos.
            xbmc.executebuiltin('Action(Info)')

    def viewSimil(self):
        sPluginPath = cPluginHandler().getPluginPath()

        oInputParameterHandler = cInputParameterHandler()
        if oInputParameterHandler.exist('sFileName'):
            sCleanTitle = oInputParameterHandler.getValue('sFileName') 
        else:
            sCleanTitle = oInputParameterHandler.getValue('sTitle') if oInputParameterHandler.exist('sTitle') else xbmc.getInfoLabel('ListItem.Title')
            # sCleanTitle = cUtil().titleWatched(sCleanTitle)
            
        sCat = oInputParameterHandler.getValue('sCat') if oInputParameterHandler.exist('sCat') else xbmc.getInfoLabel('ListItem.Property(sCat)')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('searchtext', sCleanTitle)
        oOutputParameterHandler.addParameter('sCat', sCat)

        sParams = oOutputParameterHandler.getParameterAsUri()
        sTest = '?site=%s&function=%s&%s' % ('globalSearch', 'globalSearch', sParams)
        sys.argv[2] = sTest
        sTest = sPluginPath + sTest

        # Si lancé depuis la page Home de Kodi, il faut d'abord en sortir pour lancer la recherche
        if xbmc.getCondVisibility('Window.IsVisible(home)'):
            xbmc.executebuiltin('ActivateWindow(%d)' % 10025)

        xbmc.executebuiltin('Container.Update(%s)' % sTest)
        return True

    def selectPage(self):
        from resources.lib.parser import cParser
        sPluginPath = cPluginHandler().getPluginPath()
        oInputParameterHandler = cInputParameterHandler()
        # sParams = oInputParameterHandler.getAllParameter()
        sId = oInputParameterHandler.getValue('sId')
        sFunction = oInputParameterHandler.getValue('OldFunction')
        siteUrl = oInputParameterHandler.getValue('siteUrl')

        if siteUrl.endswith('/'):  # for the url http.://www.1test.com/annee-2020/page-2/
            urlSource = siteUrl.rsplit('/', 2)[0]
            endOfUrl = siteUrl.rsplit('/', 2)[1] + '/'
        else:  # for the url http.://www.1test.com/annee-2020/page-2 or /page-2.html
            urlSource = siteUrl.rsplit('/', 1)[0]
            endOfUrl = siteUrl.rsplit('/', 1)[1]

        oParser = cParser()
        oldNum = oParser.getNumberFromString(endOfUrl)
        newNum = 0
        if oldNum:
            newNum = self.showNumBoard()
        if newNum:
            try:
                siteUrl = urlSource + '/' + endOfUrl.replace(oldNum, newNum, 1)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, sId, sFunction, sParams)
                xbmc.executebuiltin('Container.Update(%s)' % sTest)
            except:
                return False

        return False

    def selectPage2(self):
        sPluginPath = cPluginHandler().getPluginPath()
        oInputParameterHandler = cInputParameterHandler()
        sId = oInputParameterHandler.getValue('sId')
        sFunction = oInputParameterHandler.getValue('OldFunction')
        siteUrl = oInputParameterHandler.getValue('siteUrl')

        selpage = self.showNumBoard()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('Selpage', selpage)

        sParams = oOutputParameterHandler.getParameterAsUri()
        sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, sId, sFunction, sParams)
        xbmc.executebuiltin('Container.Update(%s, replace)' % sTest)

    def setWatched(self):
        if True:
            # Use vStream database
            oInputParameterHandler = cInputParameterHandler()
            sSite = oInputParameterHandler.getValue('sId')
            sSiteUrl = oInputParameterHandler.getValue('siteUrl')
            sTitle = oInputParameterHandler.getValue('sMovieTitle')
            sTitleWatched = oInputParameterHandler.getValue('sTitleWatched')
            sCat = oInputParameterHandler.getValue('sCat')
            sFav = oInputParameterHandler.getValue('sFav')
            sSeason = oInputParameterHandler.getValue('sSeason')
            sTmdbId = oInputParameterHandler.getValue('sTmdbId')
            sSeasonUrl = oInputParameterHandler.getValue('saisonUrl')
            sSeasonFunc = oInputParameterHandler.getValue('nextSaisonFunc')
            
            if not sTitle:
                return

            meta = {}
            meta['title'] = sTitle
            meta['titleWatched'] = sTitleWatched
            meta['site'] = sSite
            meta['siteurl'] = sSiteUrl
            meta['cat'] = sCat
            meta['fav'] = sFav
            meta['season'] = sSeason
            meta['seasonUrl'] = sSeasonUrl
            meta['seasonFunc'] = sSeasonFunc
            meta['tmdbId'] = sTmdbId
             
            from resources.lib.db import cDb
            with cDb() as db:
                row = db.get_watched(meta)
                if row:
                    db.del_watched(meta)
                    db.del_resume(meta)
                else:
                    db.insert_watched(meta)
                    db.del_viewing(meta)

        else:
            # Use kodi buildin feature
            xbmc.executebuiltin('Action(ToggleWatched)')

        self.updateDirectory()

    def showKeyBoard(self, sDefaultText='', heading=''):
        keyboard = xbmc.Keyboard(sDefaultText)
        keyboard.setHeading(heading)
        keyboard.doModal()
        if keyboard.isConfirmed():
            sSearchText = keyboard.getText()
            if (len(sSearchText)) > 0:
                return sSearchText

        return False

    def showNumBoard(self, sTitle="", sDefaultNum=''):
        dialogs = dialog()
        if not sTitle:
            sTitle = self.ADDON.VSlang(30019)
        numboard = dialogs.numeric(0, sTitle, sDefaultNum)
        # numboard.doModal()
        if numboard is not None:
            return numboard

        return False

    def openSettings(self):
        return False

    def showNofication(self, sTitle, iSeconds=0):
        return False

    def showError(self, sTitle, sDescription, iSeconds=0):
        return False

    def showInfo(self, sTitle, sDescription, iSeconds=0):
        return False

    def getSearchResult(self):
        cGui.searchResultsSemaphore.acquire()
        result = copy.deepcopy(cGui.searchResults)
        cGui.searchResultsSemaphore.release()
        return result

    def addSearchResult(self, oGuiElement, oOutputParameterHandler):
        cGui.searchResultsSemaphore.acquire()
        searchSiteId = oOutputParameterHandler.getValue('searchSiteId')
        if not searchSiteId:
            searchSiteId = oGuiElement.getSiteName()

        if searchSiteId not in cGui.searchResults:
            cGui.searchResults[searchSiteId] = []

        cGui.searchResults[searchSiteId].append({'guiElement': oGuiElement,
                                                 'params': copy.deepcopy(oOutputParameterHandler)})
        cGui.searchResultsSemaphore.release()

    def resetSearchResult(self):
        cGui.searchResultsSemaphore.acquire()
        cGui.searchResults = {}
        cGui.searchResultsSemaphore.release()
