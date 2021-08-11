# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import xbmcplugin
import xbmc

from resources.lib.comaddon import listitem, addon, dialog, isKrypton, window, VSlog, isNexus
from resources.lib.gui.contextElement import cContextElement
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.parser import cParser
from resources.lib.util import QuotePlus

class cGui:

    SITE_NAME = 'cGui'
    CONTENT = 'files'
    searchResults = []
    listing = []
    episodeListing = [] # Pour gérer l'enchainement des episodes
    ADDON = addon()

    if isKrypton():
        CONTENT = 'addons'

    def getEpisodeListing(self):
        return self.episodeListing
    
    def addNewDir(self, Type, sId, sFunction, sLabel, sIcon, sThumbnail='', sDesc='', oOutputParameterHandler='', sMeta=0, sCat=None):
        oGuiElement = cGuiElement()
        # dir ou link => CONTENT par défaut = files
        if Type != 'dir' and Type != 'link':
            cGui.CONTENT = Type
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)

        if sThumbnail == '':
            oGuiElement.setThumbnail(oGuiElement.getIcon())
            
        else:       
            oGuiElement.setThumbnail(sThumbnail)
            oGuiElement.setPoster(sThumbnail)

        oGuiElement.setDescription(sDesc)

        if sCat is not None:
            oGuiElement.setCat(sCat)
            
        # Pour addLink on recupere le sCat et sMeta precedent.
        if Type == 'link':
            oInputParameterHandler = cInputParameterHandler()
            sCat = oInputParameterHandler.getValue('sCat')
            if sCat:
                oGuiElement.setCat(sCat)

            sMeta = oInputParameterHandler.getValue('sMeta')
            if sMeta:
                oGuiElement.setMeta(sMeta)
        else:
            oOutputParameterHandler.addParameter('sMeta', sMeta)
            oGuiElement.setMeta(sMeta)

        # Si pas d'id TMDB on recupère le précedent
        if not oOutputParameterHandler.getValue('sTmdbId'):
            oInputParameterHandler = cInputParameterHandler()
            sTmdbID = oInputParameterHandler.getValue('sTmdbId')
            if sTmdbID:
                oOutputParameterHandler.addParameter('sTmdbId', sTmdbID)
            
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

        try:
            return self.addFolder(oGuiElement, oOutputParameterHandler)
        except Exception as e:
            pass


    #    Categorie       sCat          Meta     CONTENT
    #    Film            1             1        movies
    #    Serie           2             2        tvshows
    #    Anime           3             4        tvshows
    #    Saison          4             5        episodes
    #    Divers          5             0        videos
    #    IPTV (Officiel) 6             0        files
    #    Saga            7             3        movies
    #    Episodes        8             6        episodes
    #    Person          /             7        artists
    #    Nerwork         /             8        files

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

    def addMisc(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        if sThumbnail or sDesc:
            type = 'videos'
        else:
            type = 'files'
        movieUrl = oOutputParameterHandler.getValue('siteUrl')
        oOutputParameterHandler.addParameter('movieUrl', QuotePlus(movieUrl))
        oOutputParameterHandler.addParameter('movieFunc', sFunction)
        return self.addNewDir(type, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 0, 5)

    def addMoviePack(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        return self.addNewDir('movies', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 3, 7)

    def addDir(self, sId, sFunction, sLabel, sIcon, oOutputParameterHandler='', sDesc=""):
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

        # # Affichage du pourcentage de lecture en cours, non utilisé car pas très eronomique au niveau des liens lorsqu'il y a beaucoup de liens
        # oOutputParameterHandler.addParameter('ResumeTime', oInputParameterHandler.getValue('ResumeTime'))
        # oOutputParameterHandler.addParameter('TotalTime', oInputParameterHandler.getValue('TotalTime'))

        sIcon = sThumbnail
        return self.addNewDir('link', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 0, None)

    def addSeason(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler=''):
        # Pour gérer l'enchainement des épisodes
        saisonUrl = oOutputParameterHandler.getValue('siteUrl')
        oOutputParameterHandler.addParameter('saisonUrl', QuotePlus(saisonUrl))
        oOutputParameterHandler.addParameter('nextSaisonFunc', sFunction)

        return self.addNewDir('episodes', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 5, 4)

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

        return self.addNewDir('episodes', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 6, 8)

    # Affichage d'une personne (acteur, réalisateur, ..)
    def addPerson(self, sId, sFunction, sLabel, sIcon, sThumbnail, oOutputParameterHandler=''):
        sThumbnail = ''
        sDesc = ''
        return self.addNewDir('artists', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 7, None)

    # Affichage d'un réseau de distribution du média
    def addNetwork(self, sId, sFunction, sLabel, sIcon, oOutputParameterHandler=''):
        sThumbnail = ''
        sDesc = ''
        return self.addNewDir('files', sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler, 8, None)

    def addNext(self, sId, sFunction, sLabel, oOutputParameterHandler):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle('[COLOR teal]' + sLabel + ' >>>[/COLOR]')
        oGuiElement.setIcon('next.png')
        oGuiElement.setThumbnail(oGuiElement.getIcon())
        oGuiElement.setMeta(0)
        oGuiElement.setCat(5)

        self.createContexMenuPageSelect(oGuiElement, oOutputParameterHandler)
        self.createContexMenuViewBack(oGuiElement, oOutputParameterHandler)
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

        # recherche append les reponses
        if window(10101).getProperty('search') == 'true':
            import copy
            cGui.searchResults.append({'guiElement': oGuiElement, 'params': copy.deepcopy(oOutputParameterHandler)})
            return

        # Des infos a rajouter ?
        params = {'siteUrl': oGuiElement.setSiteUrl,
                  'sTmdbId': oGuiElement.setTmdbId,
                  'sYear': oGuiElement.setYear}
 
        try:
            for sParam, callback in params.iteritems():
                value = oOutputParameterHandler.getValue(sParam)
                if value:
                    callback(value)
 
        except AttributeError:
            for sParam, callback in params.items():
                value = oOutputParameterHandler.getValue(sParam)
                if value:
                    callback(value)

        oListItem = self.createListItem(oGuiElement)
        oListItem.setProperty('IsPlayable', 'false')

        sCat = oGuiElement.getCat()
        if sCat:
            cGui.sCat = sCat
            oOutputParameterHandler.addParameter('sCat', sCat)

        sItemUrl = self.__createItemUrl(oGuiElement, oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sTitleWatched', oGuiElement.getTitleWatched())

        if sCat:    # 1 = movies, moviePack; 2 = series, animes, episodes; 5 = MISC
            if oGuiElement.getMeta():
                self.createContexMenuinfo(oGuiElement, oOutputParameterHandler)
                self.createContexMenuba(oGuiElement, oOutputParameterHandler)
            if not oListItem.getProperty('isBookmark'):
                self.createContexMenuBookmark(oGuiElement, oOutputParameterHandler)

            if sCat in (1, 2, 3, 4, 8):
                if self.ADDON.getSetting('bstoken') != '':
                    self.createContexMenuTrakt(oGuiElement, oOutputParameterHandler)
                if self.ADDON.getSetting('tmdb_account') != '':
                    self.createContexMenuTMDB(oGuiElement, oOutputParameterHandler)
            if sCat in (1, 2, 3):
                self.createContexMenuSimil(oGuiElement, oOutputParameterHandler)
            if sCat != 6:
                self.createContexMenuWatch(oGuiElement, oOutputParameterHandler)

        oListItem = self.__createContextMenu(oGuiElement, oListItem)
        self.listing.append((sItemUrl, oListItem, _isFolder))
        
        # Vider les paramètres pour être recyclé
        oOutputParameterHandler.clearParameter()
        
        return oListItem

    # affiche les liens playable
    def addHost(self, oGuiElement, oOutputParameterHandler=''):
        oInputParameterHandler = cInputParameterHandler()

        # # Affichage du pourcentage de lecture en cours, non utilisé car pas très eronomique au niveau des liens lorsqu'il y a beaucoup de liens
        # resumeTime = oInputParameterHandler.getValue('ResumeTime')
        # if resumeTime:
            # oGuiElement.setResumeTime(resumeTime)
            # oGuiElement.setTotalTime(oInputParameterHandler.getValue('TotalTime'))
        
        cGui.CONTENT = 'files'

        if oOutputParameterHandler.getValue('siteUrl'):
            sSiteUrl = oOutputParameterHandler.getValue('siteUrl')
            oGuiElement.setSiteUrl(sSiteUrl)

        sCat = oOutputParameterHandler.getValue('sCat')
        if not sCat:
            # On récupere le sCat du niveau précédent
            sCat = oInputParameterHandler.getValue('sCat')
        if sCat:
            oGuiElement.setCat(sCat)

        oListItem = self.createListItem(oGuiElement)
        oListItem.setProperty('IsPlayable', 'true')
        # oListItem.setProperty('Video', 'true')

        sItemUrl = self.__createItemUrl(oGuiElement, oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sTitleWatched', oGuiElement.getTitleWatched())
        self.createContexMenuWatch(oGuiElement, oOutputParameterHandler)

        oListItem = self.__createContextMenu(oGuiElement, oListItem)

        self.listing.append((sItemUrl, oListItem, False))

    def createListItem(self, oGuiElement):
        # Enleve les elements vides
        data = {key:val for key, val in oGuiElement.getItemValues().items() if val != ""}

        itemTitle = oGuiElement.getTitle()
        if oGuiElement.getMeta() == 6 and data.get('tagline'): # Nom de l'épisode
            itemTitle += ' - ' + str(data.get('tagline'))
            data['title'] = itemTitle   # kodi 19

        oListItem = listitem(itemTitle)

        if not isNexus():
            # voir : https://kodi.wiki/view/InfoLabels
            oListItem.setInfo(oGuiElement.getType(), data)
            
        else:
            videoInfoTag = oListItem.getVideoInfoTag()

            # gestion des valeurs par defaut si non renseignées
            videoInfoTag.setMediaType(data.get('mediatype'))
            videoInfoTag.setTitle(itemTitle)
            videoInfoTag.setOriginalTitle(data.get('originaltitle'))
            videoInfoTag.setPlot(data.get('plot'))
            videoInfoTag.setPlotOutline(data.get('plotoutline'))
            videoInfoTag.setYear(int(data.get('year',0)))       
            videoInfoTag.setRating(float(data.get('rating',0.0)))
            videoInfoTag.setMpaa(data.get('mpaa'))
            try:
                videoInfoTag.setDuration(int(data.get('duration',0)))     
            except:
                #Pour convertir le temps en seconde.
                videoInfoTag.setDuration(sum(x * int(t) for x, t in zip([3600, 60, 1], data.get('duration').split(":"))))
            videoInfoTag.setPlaycount(int(data.get('playcount',0)))
            videoInfoTag.setCountries(data.get('country',[""]))
            videoInfoTag.setTrailer(data.get('trailer'))
            videoInfoTag.setTagLine(data.get('tagline'))
            videoInfoTag.setStudios(list(data.get('studio','').split("/")))
            videoInfoTag.setWriters(list(data.get('writer','').split("/")))
            videoInfoTag.setDirectors(list(data.get('director','').split("/")))
            videoInfoTag.setGenres(''.join(data.get('genre',[""])).split('/'))
            videoInfoTag.setSeason(int(data.get('season',0)))
            videoInfoTag.setEpisode(int(data.get('episode',0)))

            # TODO Gestion du pourcentage de lecture
            # v20 Python API changes:
            # ResumeTime and TotalTime deprecated. Use InfoTagVideo.setResumePoint() instead.


            try:
                credits = eval(data.get('credits'))['cast']
            except:
                credits = None

            cast = []
            if credits is not None:
                for actor in credits:
                    thumbnail = actor['profile_path']
                    cast.append(xbmc.Actor(actor['name'], actor['character'], actor['order'], thumbnail))
                videoInfoTag.setCast(cast)

        oListItem.setArt({'poster': oGuiElement.getPoster(),
                          'thumb': oGuiElement.getThumbnail(),
                          'icon': oGuiElement.getIcon(),
                          'fanart': oGuiElement.getFanart()})

        aProperties = oGuiElement.getItemProperties()
        for sPropertyKey, sPropertyValue in aProperties.items():
            oListItem.setProperty(sPropertyKey, str(sPropertyValue))

        return oListItem

    # Marquer vu/Non vu
    def createContexMenuWatch(self, oGuiElement, oOutputParameterHandler=''):
        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cGui', oGuiElement.getSiteName(), 'setWatched', self.ADDON.VSlang(30206))

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

        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cFav', 'cFav', 'setBookmark', self.ADDON.VSlang(30210))

    def createContexMenuTrakt(self, oGuiElement, oOutputParameterHandler= ''):
        oOutputParameterHandler.addParameter('sImdbId', oGuiElement.getImdbId())
        oOutputParameterHandler.addParameter('sTmdbId', oGuiElement.getTmdbId())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())

        sType = cGui.CONTENT.replace('tvshows', 'shows')
        oOutputParameterHandler.addParameter('sType', sType)
        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cTrakt', 'cTrakt', 'getAction', self.ADDON.VSlang(30214))

    def createContexMenuTMDB(self, oGuiElement, oOutputParameterHandler = ''):
        oOutputParameterHandler.addParameter('sImdbId', oGuiElement.getImdbId())
        oOutputParameterHandler.addParameter('sTmdbId', oGuiElement.getTmdbId())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())

        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'themoviedb_org', 'themoviedb_org', 'getAction', 'TMDB')

    def createContexMenuDownload(self, oGuiElement, oOutputParameterHandler='', status='0'):
        if status == '0':
            self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'StartDownloadOneFile', self.ADDON.VSlang(30215))

        if status == '0' or status == '2':
            self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'delDownload', self.ADDON.VSlang(30216))
            self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'DelFile', self.ADDON.VSlang(30217))

        if status == '1':
            self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'StopDownloadList', self.ADDON.VSlang(30218))

        if status == '2':
            self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'ReadDownload', self.ADDON.VSlang(30219))
            self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cDownload', 'cDownload', 'ResetDownload', self.ADDON.VSlang(30220))

    # Information
    def createContexMenuinfo(self, oGuiElement, oOutputParameterHandler=''):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sTitle', oGuiElement.getTitle())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oOutputParameterHandler.addParameter('sMeta', oGuiElement.getMeta())
        oOutputParameterHandler.addParameter('sYear', oGuiElement.getYear())

        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cGui', oGuiElement.getSiteName(), 'viewInfo', self.ADDON.VSlang(30208))

    # Bande annonce
    def createContexMenuba(self, oGuiElement, oOutputParameterHandler=''):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sTitle', oGuiElement.getTitle())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())
        oOutputParameterHandler.addParameter('sYear', oGuiElement.getYear())
        oOutputParameterHandler.addParameter('sTrailerUrl', oGuiElement.getTrailer())
        oOutputParameterHandler.addParameter('sMeta', oGuiElement.getMeta())

        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cGui', oGuiElement.getSiteName(), 'viewBA', self.ADDON.VSlang(30212))

    # Recherche similaire
    def createContexMenuSimil(self, oGuiElement, oOutputParameterHandler=''):
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())
        oOutputParameterHandler.addParameter('sTitle', oGuiElement.getTitle())
        oOutputParameterHandler.addParameter('sCat', oGuiElement.getCat())

        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cGui', oGuiElement.getSiteName(), 'viewSimil', self.ADDON.VSlang(30213))

    def CreateSimpleMenu(self, oGuiElement, oOutputParameterHandler, sFile, sName, sFunction, sTitle):
        oContext = cContextElement()
        oContext.setFile(sFile)
        oContext.setSiteName(sName)
        oContext.setFunction(sFunction)
        oContext.setTitle(sTitle)

        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)

    def createContexMenuDelFav(self, oGuiElement, oOutputParameterHandler=''):
        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cFav', 'cFav', 'delBookmarksMenu', self.ADDON.VSlang(30209))

    def createContexMenuSettings(self, oGuiElement, oOutputParameterHandler=''):
        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'globalParametre', 'globalParametre', 'opensetting', self.ADDON.VSlang(30023))

    def __createContextMenu(self, oGuiElement, oListItem):
        sPluginPath = cPluginHandler().getPluginPath()
        aContextMenus = []

        # Menus classiques reglés a la base
        nbContextMenu = len(oGuiElement.getContextItems())
        if nbContextMenu > 0:
            for oContextItem in oGuiElement.getContextItems():
                oOutputParameterHandler = oContextItem.getOutputParameterHandler()
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)
                aContextMenus += [(oContextItem.getTitle(), 'RunPlugin(%s)' % sTest)]

            oListItem.addContextMenuItems(aContextMenus)
        oListItem.setProperty('nbcontextmenu', str(nbContextMenu))
        return oListItem

    # def __ContextMenu(self, oGuiElement, oListItem):
        # sPluginPath = cPluginHandler().getPluginPath()
        # aContextMenus = []
        #
        # if len(oGuiElement.getContextItems()) > 0:
            # for oContextItem in oGuiElement.getContextItems():
                # oOutputParameterHandler = oContextItem.getOutputParameterHandler()
                # sParams = oOutputParameterHandler.getParameterAsUri()
                # sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)
                # aContextMenus += [(oContextItem.getTitle(), 'RunPlugin(%s)' % sTest)]
                #
            # oListItem.addContextMenuItems(aContextMenus)
            #
        # return oListItem
        #
    # def __ContextMenuPlay(self, oGuiElement, oListItem):
        # sPluginPath = cPluginHandler().getPluginPath()
        # aContextMenus = []
        #
        # if len(oGuiElement.getContextItems()) > 0:
            # for oContextItem in oGuiElement.getContextItems():
                # oOutputParameterHandler = oContextItem.getOutputParameterHandler()
                # sParams = oOutputParameterHandler.getParameterAsUri()
                # sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)
                # aContextMenus += [(oContextItem.getTitle(), 'RunPlugin(%s)' % sTest)]
                #
            # oListItem.addContextMenuItems(aContextMenus)
            #
        # return oListItem

    def __createItemUrl(self, oGuiElement, oOutputParameterHandler=''):
        if (oOutputParameterHandler == ''):
            oOutputParameterHandler = cOutputParameterHandler()

        # On descend l'id TMDB dans les saisons et les épisodes
        oOutputParameterHandler.addParameter('sTmdbId', oGuiElement.getTmdbId())

        # Pour gérer l'enchainement des épisodes
        oOutputParameterHandler.addParameter('sSeason', oGuiElement.getSeason())
        oOutputParameterHandler.addParameter('sEpisode', oGuiElement.getEpisode())

        sParams = oOutputParameterHandler.getParameterAsUri()

        sPluginPath = cPluginHandler().getPluginPath()

        if (len(oGuiElement.getFunction()) == 0):
            sItemUrl = '%s?site=%s&title=%s&%s' % (sPluginPath, oGuiElement.getSiteName(), QuotePlus(oGuiElement.getCleanTitle()), sParams)
        else:
            sItemUrl = '%s?site=%s&function=%s&title=%s&%s' % (sPluginPath, oGuiElement.getSiteName(), oGuiElement.getFunction(), QuotePlus(oGuiElement.getCleanTitle()), sParams)

        return sItemUrl

    def setEndOfDirectory(self, forceViewMode=False):
        iHandler = cPluginHandler().getPluginHandle()

        if not self.listing:
            self.addText('cGui')

        xbmcplugin.addDirectoryItems(iHandler, self.listing, len(self.listing))
        xbmcplugin.setPluginCategory(iHandler, '')
        xbmcplugin.setContent(iHandler, cGui.CONTENT)
        xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(iHandler, succeeded=True, cacheToDisc=True)
        # reglage vue
        # 50 = liste / 51 grande liste / 500 icone / 501 gallerie / 508 fanart /
        if forceViewMode:
            xbmc.executebuiltin('Container.SetViewMode(' + str(forceViewMode) + ')')
        else:
            if self.ADDON.getSetting('active-view') == 'true':
                if cGui.CONTENT == 'movies' or  cGui.CONTENT == 'artists':
                    # xbmc.executebuiltin('Container.SetViewMode(507)')
                    xbmc.executebuiltin('Container.SetViewMode(%s)' % self.ADDON.getSetting('movie-view'))
                elif cGui.CONTENT == 'tvshows':
                    xbmc.executebuiltin('Container.SetViewMode(%s)' % self.ADDON.getSetting('serie-view'))
                elif cGui.CONTENT == 'files' or cGui.CONTENT == 'episodes':
                    xbmc.executebuiltin('Container.SetViewMode(%s)' % self.ADDON.getSetting('default-view'))

        del self.episodeListing[:] # Pour l'enchainement des episodes
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
        if addon().getSetting('information-view') == "false":
            from resources.lib.config import WindowsBoxes

            oInputParameterHandler = cInputParameterHandler()
            sCleanTitle = oInputParameterHandler.getValue('sFileName') if oInputParameterHandler.exist('sFileName') else xbmc.getInfoLabel('ListItem.Property(sCleanTitle)')
            sMeta = oInputParameterHandler.getValue('sMeta') if oInputParameterHandler.exist('sMeta') else xbmc.getInfoLabel('ListItem.Property(sMeta)')
            sYear = oInputParameterHandler.getValue('sYear') if oInputParameterHandler.exist('sYear') else xbmc.getInfoLabel('ListItem.Year')

            WindowsBoxes(sCleanTitle, sCleanTitle, sMeta, sYear)
        else:
            # On appel la fonction integrer a Kodi pour charger les infos.
            xbmc.executebuiltin('Action(Info)')

    def viewSimil(self):
        sPluginPath = cPluginHandler().getPluginPath()

        oInputParameterHandler = cInputParameterHandler()
        sCleanTitle = oInputParameterHandler.getValue('sFileName') if oInputParameterHandler.exist('sFileName') else xbmc.getInfoLabel('ListItem.Property(sCleanTitle)')
        sCat = oInputParameterHandler.getValue('sCat') if oInputParameterHandler.exist('sCat') else xbmc.getInfoLabel('ListItem.Property(sCat)')

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('searchtext', sCleanTitle)
        oOutputParameterHandler.addParameter('sCat', sCat)
        oOutputParameterHandler.addParameter('readdb', 'False')

        sParams = oOutputParameterHandler.getParameterAsUri()
        sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, 'globalSearch', 'globalSearch', sParams)

        # Si lancé depuis la page Home de Kodi, il faut d'abord en sortir pour lancer la recherche
        if xbmc.getCondVisibility('Window.IsVisible(home)'):
            xbmc.executebuiltin('ActivateWindow(%d)' % (10028))

        xbmc.executebuiltin('Container.Update(%s)' % sTest)

        return False

    def selectPage(self):
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
            sSite = oInputParameterHandler.getValue('siteUrl')
            sTitle = oInputParameterHandler.getValue('sTitleWatched')
            sCat = oInputParameterHandler.getValue('sCat')
            if not sTitle:
                return

            meta = {}
            meta['title'] = sTitle
            meta['titleWatched'] = sTitle
            meta['site'] = sSite
            meta['cat'] = sCat

            from resources.lib.db import cDb
            db = cDb()
            row = db.get_watched(meta)
            if row:
                db.del_watched(meta)
                db.del_resume(meta)
            else:
                db.insert_watched(meta)
                db.del_viewing(meta)
            # To test
            # updateDirectory()

        else:
            # Use kodi buildin feature
            xbmc.executebuiltin('Action(ToggleWatched)')

        self.updateDirectory()

    def showKeyBoard(self, sDefaultText='', heading=''):
        keyboard = xbmc.Keyboard(sDefaultText)
        keyboard.setHeading(heading)
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            sSearchText = keyboard.getText()
            if (len(sSearchText)) > 0:
                return sSearchText

        return False

    def showNumBoard(self, sDefaultNum=''):
        dialogs = dialog()
        numboard = dialogs.numeric(0, self.ADDON.VSlang(30019), sDefaultNum)
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
