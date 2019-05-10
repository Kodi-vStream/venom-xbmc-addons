#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.contextElement import cContextElement
from resources.lib.gui.guiElement import cGuiElement

#from resources.lib.config import cConfig
from resources.lib.db import cDb
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.parser import cParser
from resources.lib import util

from resources.lib.comaddon import listitem, addon, dialog, isKrypton, window, xbmc

import xbmcplugin
import urllib
import unicodedata, re


class cGui():

    SITE_NAME = 'cGui'
    CONTENT = 'files'
    searchResults = []
    #modif 22/06
    listing = []
    ADDON = addon()

    if isKrypton():
        CONTENT = 'addons'


    def addMovie(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler = ''):
        cGui.CONTENT = "movies"
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setPoster(sThumbnail)
        oGuiElement.setMeta(1)
        oGuiElement.setDescription(sDesc)
        #oGuiElement.setMovieFanart()
        oGuiElement.setCat(1)

        if oOutputParameterHandler.getValue('sMovieTitle'):
            sTitle = oOutputParameterHandler.getValue('sMovieTitle')
            oGuiElement.setFileName(sTitle)

        self.addFolder(oGuiElement, oOutputParameterHandler)


    def addTV(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler = ''):
        cGui.CONTENT = "tvshows"
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setPoster(sThumbnail)
        oGuiElement.setMeta(2)
        oGuiElement.setDescription(sDesc)
        #oGuiElement.setTvFanart()
        oGuiElement.setCat(2)

        # if oOutputParameterHandler.getValue('season'):
            # sSeason = oOutputParameterHandler.getValue('season')
            # oGuiElement.addItemValues('Season', sSeason)

        # if oOutputParameterHandler.getValue('episode'):
            # sSeason = oOutputParameterHandler.getValue('episode')
            # oGuiElement.addItemValues('Episode', sSeason)

        if oOutputParameterHandler.getValue('sMovieTitle'):
            sTitle = oOutputParameterHandler.getValue('sMovieTitle')
            oGuiElement.setFileName(sTitle)


        self.addFolder(oGuiElement, oOutputParameterHandler)

    def addMisc(self, sId, sFunction, sLabel, sIcon, sThumbnail, sDesc, oOutputParameterHandler = ''):
        #cGui.CONTENT = "movies"
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setThumbnail(sThumbnail)
        #oGuiElement.setPoster(sThumbnail)
        oGuiElement.setMeta(0)
        #oGuiElement.setDirFanart(sIcon)
        oGuiElement.setCat(5)

        oGuiElement.setDescription(sDesc)

        if oOutputParameterHandler.getValue('sMovieTitle'):
            sTitle = oOutputParameterHandler.getValue('sMovieTitle')
            oGuiElement.setFileName(sTitle)

        self.createContexMenuWatch(oGuiElement, oOutputParameterHandler)
        #self.createContexMenuinfo(oGuiElement, oOutputParameterHandler)
        self.createContexMenuFav(oGuiElement, oOutputParameterHandler)

        self.addFolder(oGuiElement, oOutputParameterHandler)

    #non utiliser le 18/04
    #def addFav(self, sId, sFunction, sLabel, sIcon, sThumbnail, fanart, oOutputParameterHandler = ''):
        #cGui.CONTENT = "files"
        #oGuiElement = cGuiElement()
        #oGuiElement.setSiteName(sId)
        #oGuiElement.setFunction(sFunction)
        #oGuiElement.setTitle(sLabel)
        #oGuiElement.setIcon(sIcon)
        #oGuiElement.setMeta(0)
        #oGuiElement.setThumbnail(sThumbnail)
        #oGuiElement.setFanart(fanart)

        #self.createContexMenuDelFav(oGuiElement, oOutputParameterHandler)

        #self.addFolder(oGuiElement, oOutputParameterHandler)


    def addLink(self, sId, sFunction, sLabel, sThumbnail, sDesc, oOutputParameterHandler = ''):
        cGui.CONTENT = "files"
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        #oGuiElement.setIcon(sIcon)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setPoster(sThumbnail)
        oGuiElement.setDescription(sDesc)
        oGuiElement.setMeta(0)
        #oGuiElement.setDirFanart('')

        oInputParameterHandler = cInputParameterHandler()
        sCat = oInputParameterHandler.getValue('sCat')
        if sCat:
            oGuiElement.setCat(sCat)


        self.addFolder(oGuiElement, oOutputParameterHandler)


    def addDir(self, sId, sFunction, sLabel, sIcon, oOutputParameterHandler = ''):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setThumbnail(oGuiElement.getIcon())
        oGuiElement.setMeta(0)
        #oGuiElement.setDirFanart(sIcon)

        oOutputParameterHandler.addParameter('sFav', sFunction)

        #context parametre
        if isKrypton():
            self.createContexMenuSettings(oGuiElement, oOutputParameterHandler)

        self.addFolder(oGuiElement, oOutputParameterHandler)

    def addNext(self, sId, sFunction, sLabel, oOutputParameterHandler):
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon('next.png')
        oGuiElement.setThumbnail(oGuiElement.getIcon())
        oGuiElement.setMeta(0)
        #oGuiElement.setDirFanart('next.png')
        oGuiElement.setCat(5)

        self.createContexMenuPageSelect(oGuiElement, oOutputParameterHandler)
        self.createContexMenuFav(oGuiElement, oOutputParameterHandler)

        self.addFolder(oGuiElement, oOutputParameterHandler)

    #utiliser oGui.addText(SITE_IDENTIFIER)
    def addNone(self, sId):
        return self.addText(sId)


    def addText(self, sId, sLabel="", sIcon='none.png'):
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

        self.addFolder(oGuiElement, oOutputParameterHandler)

    #non utiliser depuis le 22/04
    def addMovieDB(self, sId, sFunction, sLabel, sIcon, sThumbnail, sFanart, oOutputParameterHandler = ''):

        cGui.CONTENT = "movies"
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setMeta(1)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setFanart(sFanart)
        oGuiElement.setCat(7)

        if oOutputParameterHandler.getValue('sMovieTitle'):
            sTitle = oOutputParameterHandler.getValue('sMovieTitle')
            oGuiElement.setFileName(sTitle)

        self.addFolder(oGuiElement, oOutputParameterHandler)

    #non utiliser 22/04
    def addTVDB(self, sId, sFunction, sLabel, sIcon, sThumbnail, sFanart, oOutputParameterHandler = ''):

        cGui.CONTENT = "tvshows"
        oGuiElement = cGuiElement()
        oGuiElement.setSiteName(sId)
        oGuiElement.setFunction(sFunction)
        oGuiElement.setTitle(sLabel)
        oGuiElement.setIcon(sIcon)
        oGuiElement.setMeta(2)
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setFanart(sFanart)
        oGuiElement.setCat(7)

        if oOutputParameterHandler.getValue('sMovieTitle'):
            sTitle = oOutputParameterHandler.getValue('sMovieTitle')
            oGuiElement.setFileName(sTitle)

        self.addFolder(oGuiElement, oOutputParameterHandler)

    #afficher les liens non playable
    def addFolder(self, oGuiElement, oOutputParameterHandler='', _isFolder=True):

        #recherche append les reponses
        if  window(10101).getProperty('search') == 'true':
            import copy
            cGui.searchResults.append({'guiElement':oGuiElement, 'params':copy.deepcopy(oOutputParameterHandler)})
            return

        #Des infos a rajouter ?
        params = {
            "siteUrl": oGuiElement.setSiteUrl,#indispensable
            "sTmdbId": oGuiElement.setTmdbId,
            "sImbdId": oGuiElement.setImdbId,#inutile ?
            "sYear": oGuiElement.setYear,
        }

        for sParam, callback in params.iteritems():
            value = oOutputParameterHandler.getValue(sParam)
            if value:
                callback(value)

        oListItem = self.createListItem(oGuiElement)
        oListItem.setProperty("IsPlayable", "false")

        #affiche tag HD
        # if '1080' in oGuiElement.getTitle():
        #     oListItem.addStreamInfo('video', { 'aspect': '1.78', 'width':1920, 'height' : 1080 })
        # elif '720' in oGuiElement.getTitle():
        #     oListItem.addStreamInfo('video', { 'aspect': '1.50', 'width':1280, 'height' : 720 })
        # elif '2160'in oGuiElement.getTitle():
        #     oListItem.addStreamInfo('video', { 'aspect': '1.78', 'width':3840, 'height' : 2160 })
        #oListItem.addStreamInfo('audio', {'language': 'fr'})

        # if oGuiElement.getMeta():
        #oOutputParameterHandler.addParameter('sMeta', oGuiElement.getMeta())
        if oGuiElement.getCat():
            oOutputParameterHandler.addParameter('sCat', oGuiElement.getCat())


        sItemUrl = self.__createItemUrl(oGuiElement, oOutputParameterHandler)

        #new context prend en charge les metas
        if (oGuiElement.getMeta() > 0):
            if cGui.CONTENT == "movies":
                self.createContexMenuWatch(oGuiElement, oOutputParameterHandler)
                self.createContexMenuFav(oGuiElement, oOutputParameterHandler)
                
                self.createContexMenuinfo(oGuiElement, oOutputParameterHandler)
                self.createContexMenuba(oGuiElement, oOutputParameterHandler)
                
                if self.ADDON.getSetting("bstoken"):
                    self.createContexMenuTrakt(oGuiElement, oOutputParameterHandler)
                if self.ADDON.getSetting('tmdb_account'):
                    self.createContexMenuTMDB(oGuiElement, oOutputParameterHandler)
                self.createContexMenuSimil(oGuiElement, oOutputParameterHandler)


            elif cGui.CONTENT == "tvshows":
                self.createContexMenuWatch(oGuiElement, oOutputParameterHandler)
                self.createContexMenuFav(oGuiElement, oOutputParameterHandler)
                
                self.createContexMenuinfo(oGuiElement, oOutputParameterHandler)
                self.createContexMenuba(oGuiElement, oOutputParameterHandler)
                
                if self.ADDON.getSetting("bstoken"):
                    self.createContexMenuTrakt(oGuiElement, oOutputParameterHandler)
                if self.ADDON.getSetting('tmdb_account'):
                    self.createContexMenuTMDB(oGuiElement, oOutputParameterHandler)
                self.createContexMenuSimil(oGuiElement, oOutputParameterHandler)

        oListItem = self.__createContextMenu(oGuiElement, oListItem)

        sPluginHandle = cPluginHandler().getPluginHandle()
        #modif 22/06
        #xbmcplugin.addDirectoryItem(sPluginHandle, sItemUrl, oListItem, isFolder=_isFolder)
        self.listing.append((sItemUrl, oListItem, _isFolder))


    def createListItem(self, oGuiElement):

        oListItem = listitem(oGuiElement.getTitle())
        oListItem.setInfo(oGuiElement.getType(), oGuiElement.getItemValues())
        #oListItem.setThumbnailImage(oGuiElement.getThumbnail())
        #oListItem.setIconImage(oGuiElement.getIcon())

        #krypton et sont comportement
        oListItem.setArt({'poster': oGuiElement.getPoster(), 'thumb': oGuiElement.getThumbnail(), 'icon': oGuiElement.getIcon(), 'fanart': oGuiElement.getFanart() })

        aProperties = oGuiElement.getItemProperties()
        for sPropertyKey in aProperties.keys():
            oListItem.setProperty(sPropertyKey, aProperties[sPropertyKey])

        return oListItem

    #affiche les liens playable
    def addHost(self, oGuiElement, oOutputParameterHandler=''):

        if isKrypton():
            cGui.CONTENT = 'movies'

        if oOutputParameterHandler.getValue('siteUrl'):
            sSiteUrl = oOutputParameterHandler.getValue('siteUrl')
            oGuiElement.setSiteUrl(sSiteUrl)

        oListItem = self.createListItem(oGuiElement)
        oListItem.setProperty("IsPlayable", "true")
        oListItem.setProperty("Video", "true")

        oListItem.addStreamInfo('video', {})

        sItemUrl = self.__createItemUrl(oGuiElement, oOutputParameterHandler)

        oListItem = self.__createContextMenu(oGuiElement, oListItem)

        sPluginHandle = cPluginHandler().getPluginHandle()

        #modif 13/09
        #xbmcplugin.addDirectoryItem(sPluginHandle, sItemUrl, oListItem, isFolder=False)
        self.listing.append((sItemUrl, oListItem, False))

    #Marquer vu/Non vu
    def createContexMenuWatch(self, oGuiElement, oOutputParameterHandler= ''):
        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cGui', oGuiElement.getSiteName(), 'setWatched', self.ADDON.VSlang(30206))

    def createContexMenuPageSelect(self, oGuiElement, oOutputParameterHandler):
        #sSiteUrl = oGuiElement.getSiteName()

        oContext = cContextElement()

        oContext.setFile('cGui')
        oContext.setSiteName('cGui')

        oContext.setFunction('selectpage')
        oContext.setTitle('[COLOR azure]Selectionner page[/COLOR]')
        oOutputParameterHandler.addParameter('OldFunction', oGuiElement.getFunction())
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)

        oContext = cContextElement()

        oContext.setFile('cGui')
        oContext.setSiteName('cGui')

        oContext.setFunction('viewback')
        oContext.setTitle('[COLOR azure]Retour Site[/COLOR]')
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oContext.setOutputParameterHandler(oOutputParameterHandler)
        oGuiElement.addContextItem(oContext)


    #marque page
    def createContexMenuFav(self, oGuiElement, oOutputParameterHandler= ''):
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oOutputParameterHandler.addParameter('sFav', oGuiElement.getFunction())
        oOutputParameterHandler.addParameter('sCat', oGuiElement.getCat())

        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cFav', 'cFav', 'setFavorite', self.ADDON.VSlang(30207))

    def createContexMenuTrakt(self, oGuiElement, oOutputParameterHandler= ''):

        oOutputParameterHandler.addParameter('sImdbId', oGuiElement.getImdbId())
        oOutputParameterHandler.addParameter('sTmdbId', oGuiElement.getTmdbId())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())

        sType = cGui.CONTENT.replace('tvshows', 'shows')
        oOutputParameterHandler.addParameter('sType', sType)
        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cTrakt', 'cTrakt', 'getAction', self.ADDON.VSlang(30214))

    def createContexMenuTMDB(self, oGuiElement, oOutputParameterHandler= ''):

        oOutputParameterHandler.addParameter('sImdbId', oGuiElement.getImdbId())
        oOutputParameterHandler.addParameter('sTmdbId', oGuiElement.getTmdbId())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())

        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'themoviedb_org', 'themoviedb_org', 'getAction', 'TMDB')

    def createContexMenuDownload(self, oGuiElement, oOutputParameterHandler= '', status = '0'):

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


    #Information
    def createContexMenuinfo(self, oGuiElement, oOutputParameterHandler= ''):

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sTitle', oGuiElement.getTitle())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())
        oOutputParameterHandler.addParameter('sId', oGuiElement.getSiteName())
        oOutputParameterHandler.addParameter('sMeta', oGuiElement.getMeta())

        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cGui', oGuiElement.getSiteName(), 'viewinfo', self.ADDON.VSlang(30208))

    def createContexMenuba(self, oGuiElement, oOutputParameterHandler= ''):

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sTitle', oGuiElement.getTitle())
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())

        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cGui', oGuiElement.getSiteName(), 'viewBA', self.ADDON.VSlang(30212))


    def createContexMenuSimil(self, oGuiElement, oOutputParameterHandler= ''):

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('sFileName', oGuiElement.getFileName())
        oOutputParameterHandler.addParameter('sTitle', oGuiElement.getTitle())
        oOutputParameterHandler.addParameter('sCat', oGuiElement.getCat())

        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cGui', oGuiElement.getSiteName(), 'viewsimil', self.ADDON.VSlang(30213))

    def CreateSimpleMenu(self,oGuiElement, oOutputParameterHandler, file, name, function, title):
        oContext = cContextElement()
        oContext.setFile(file)
        oContext.setSiteName(name)
        oContext.setFunction(function)
        oContext.setTitle(title)

        oContext.setOutputParameterHandler(oOutputParameterHandler)

        oGuiElement.addContextItem(oContext)

    def createContexMenuDelFav(self, oGuiElement, oOutputParameterHandler= ''):
        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'cFav', 'cFav', 'delFavouritesMenu', self.ADDON.VSlang(30209))

    def createContexMenuSettings(self, oGuiElement, oOutputParameterHandler= ''):
        self.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, 'globalParametre', 'globalParametre', 'opensetting', self.ADDON.VSlang(30023))


    def __createContextMenu(self, oGuiElement, oListItem):
        sPluginPath = cPluginHandler().getPluginPath()
        aContextMenus = []

        #Menus classiques reglés a la base
        if (len(oGuiElement.getContextItems()) > 0):
            for oContextItem in oGuiElement.getContextItems():
                oOutputParameterHandler = oContextItem.getOutputParameterHandler()
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)
                aContextMenus+= [ ( oContextItem.getTitle(), "XBMC.RunPlugin(%s)" % (sTest,),)]

            oListItem.addContextMenuItems(aContextMenus, True)

        return oListItem

    def __ContextMenu(self, oGuiElement, oListItem):
        sPluginPath = cPluginHandler().getPluginPath()
        aContextMenus = []

        if (len(oGuiElement.getContextItems()) > 0):
            for oContextItem in oGuiElement.getContextItems():
                oOutputParameterHandler = oContextItem.getOutputParameterHandler()
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)
                aContextMenus+= [ ( oContextItem.getTitle(), "XBMC.RunPlugin(%s)" % (sTest,),)]

            oListItem.addContextMenuItems(aContextMenus)
            #oListItem.addContextMenuItems(aContextMenus, True)

        return oListItem

    def __ContextMenuPlay(self, oGuiElement, oListItem):
        sPluginPath = cPluginHandler().getPluginPath()
        aContextMenus = []

        if (len(oGuiElement.getContextItems()) > 0):
            for oContextItem in oGuiElement.getContextItems():
                oOutputParameterHandler = oContextItem.getOutputParameterHandler()
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, oContextItem.getFile(), oContextItem.getFunction(), sParams)
                aContextMenus+= [ ( oContextItem.getTitle(), "XBMC.RunPlugin(%s)" % (sTest,),)]

            oListItem.addContextMenuItems(aContextMenus)
            #oListItem.addContextMenuItems(aContextMenus, True)

        return oListItem

    def setEndOfDirectory(self, ForceViewMode = False):

        iHandler = cPluginHandler().getPluginHandle()
        #modif 22/06
        if not self.listing:
            self.addText('cGui')

        xbmcplugin.addDirectoryItems(iHandler, self.listing, len(self.listing))

        xbmcplugin.setPluginCategory(iHandler, "")
        xbmcplugin.setContent(iHandler, cGui.CONTENT)
        xbmcplugin.addSortMethod(iHandler, xbmcplugin.SORT_METHOD_NONE)
        xbmcplugin.endOfDirectory(iHandler, succeeded=True, cacheToDisc=True)
        #reglage vue
        #50 = liste / 51 grande liste / 500 icone / 501 gallerie / 508 fanart /
        if (ForceViewMode):
            xbmc.executebuiltin('Container.SetViewMode(' + str(ForceViewMode) + ')')
        else:
            if (self.ADDON.getSetting('active-view') == 'true'):
                if cGui.CONTENT == "movies":
                    #xbmc.executebuiltin('Container.SetViewMode(507)')
                    xbmc.executebuiltin('Container.SetViewMode(%s)' % self.ADDON.getSetting('movie-view'))
                elif cGui.CONTENT == "tvshows":
                    xbmc.executebuiltin('Container.SetViewMode(%s)' % self.ADDON.getSetting('serie-view'))
                elif cGui.CONTENT == "files":
                    xbmc.executebuiltin('Container.SetViewMode(%s)' % self.ADDON.getSetting('default-view'))

        #bug affichage Kodi 18
        del self.listing [:]

    def updateDirectory(self):
        xbmc.executebuiltin("Container.Refresh")

    def viewback(self):
        sPluginPath = cPluginHandler().getPluginPath()
        oInputParameterHandler = cInputParameterHandler()
        sParams = oInputParameterHandler.getAllParameter()

        sId = oInputParameterHandler.getValue('sId')

        sTest = '%s?site=%s' % (sPluginPath, sId)
        xbmc.executebuiltin('XBMC.Container.Update(%s, replace)' % sTest )

    def viewsimil(self):
        sPluginPath = cPluginHandler().getPluginPath()
        oInputParameterHandler = cInputParameterHandler()
        sFileName = oInputParameterHandler.getValue('sFileName')
        sTitle = oInputParameterHandler.getValue('sTitle')
        sCat = oInputParameterHandler.getValue('sCat')

        oOutputParameterHandler = cOutputParameterHandler()
        #oOutputParameterHandler.addParameter('searchtext', sFileName)
        oOutputParameterHandler.addParameter('searchtext', util.cUtil().CleanName(sTitle))
        oOutputParameterHandler.addParameter('sCat', sCat)

        oOutputParameterHandler.addParameter('readdb', 'False')

        sParams = oOutputParameterHandler.getParameterAsUri()
        sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, 'globalSearch', 'globalSearch', sParams)
        xbmc.executebuiltin('XBMC.Container.Update(%s)' % sTest )
        return False


    def selectpage(self):
        sPluginPath = cPluginHandler().getPluginPath()
        oInputParameterHandler = cInputParameterHandler()
        #sParams = oInputParameterHandler.getAllParameter()

        sId = oInputParameterHandler.getValue('sId')
        sFunction = oInputParameterHandler.getValue('OldFunction')
        siteUrl = oInputParameterHandler.getValue('siteUrl')

        oParser = cParser()
        oldNum = oParser.getNumberFromString(siteUrl)
        newNum = 0
        if oldNum:
            newNum = self.showNumBoard()
        if newNum:
            try:
                siteUrl = siteUrl.replace(oldNum, newNum)

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                sParams = oOutputParameterHandler.getParameterAsUri()
                sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, sId, sFunction, sParams)
                xbmc.executebuiltin('XBMC.Container.Update(%s)' % sTest )
            except:
                return False

        return False


    def selectpage2(self):
        sPluginPath = cPluginHandler().getPluginPath()
        oInputParameterHandler = cInputParameterHandler()

        sParams = oInputParameterHandler.getAllParameter()


        sId = oInputParameterHandler.getValue('sId')
        siteUrl = oInputParameterHandler.getValue('siteUrl')
        sFunction = oInputParameterHandler.getValue('OldFunction')

        selpage = self.showNumBoard()

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', siteUrl)
        oOutputParameterHandler.addParameter('Selpage', selpage)

        sParams = oOutputParameterHandler.getParameterAsUri()
        sTest = '%s?site=%s&function=%s&%s' % (sPluginPath, sId, sFunction, sParams)
        xbmc.executebuiltin('XBMC.Container.Update(%s, replace)' % sTest )

    def setWatched(self):
        if (True):
            #Use database
            oInputParameterHandler = cInputParameterHandler()

            aParams = oInputParameterHandler.getAllParameter()

            sSite = oInputParameterHandler.getValue('siteUrl')
            sTitle = xbmc.getInfoLabel('ListItem.label')

            meta = {}
            meta['title'] = sTitle
            meta['site'] = sSite

            row = cDb().get_watched(meta)
            if row:
                cDb().del_watched(meta)
                cDb().del_resume(meta)
            else:
                cDb().insert_watched(meta)
                
            xbmc.executebuiltin( 'Action(ToggleWatched)' )
            
        else:
            # Use kodi buildin feature
            xbmc.executebuiltin( 'Action(ToggleWatched)' )

        #Not usefull ?
        #xbmc.executebuiltin( 'Container.Refresh' )


    def viewBA(self):
        oInputParameterHandler = cInputParameterHandler()
        sFileName = oInputParameterHandler.getValue('sFileName')

        from resources.lib.ba import cShowBA
        cBA = cShowBA()
        cBA.SetSearch(sFileName)
        cBA.SearchBA()


    def viewinfo(self):

        from resources.lib.config import WindowsBoxes

        oGuiElement = cGuiElement()
        oInputParameterHandler = cInputParameterHandler()

        sTitle = oInputParameterHandler.getValue('sTitle')
        sId = oInputParameterHandler.getValue('sId')
        sFileName = oInputParameterHandler.getValue('sFileName')
        sYear = oInputParameterHandler.getValue('sYear')
        sMeta = oInputParameterHandler.getValue('sMeta')

        #sMeta = 1 >> film sMeta = 2 >> serie
        sCleanTitle = util.cUtil().CleanName(sFileName)

        #on vire saison et episode
        if (True):#sMeta == 2:
            sCleanTitle = re.sub('(?i).pisode [0-9]+', '', sCleanTitle)
            sCleanTitle = re.sub('(?i)saison [0-9]+', '', sCleanTitle)
            sCleanTitle = re.sub('(?i)S[0-9]+E[0-9]+', '', sCleanTitle)
            sCleanTitle = re.sub('(?i)[S|E][0-9]+', '', sCleanTitle)

        ui = WindowsBoxes(sTitle, sCleanTitle, sMeta, sYear)

    def __createItemUrl(self, oGuiElement, oOutputParameterHandler=''):
        if (oOutputParameterHandler == ''):
            oOutputParameterHandler = cOutputParameterHandler()

        sParams = oOutputParameterHandler.getParameterAsUri()
        #cree une id unique
        # if oGuiElement.getSiteUrl():
            # print  str(hash(oGuiElement.getSiteUrl()))


        sPluginPath = cPluginHandler().getPluginPath()

        if (len(oGuiElement.getFunction()) == 0):
            sItemUrl = '%s?site=%s&title=%s&%s' % (sPluginPath, oGuiElement.getSiteName(), urllib.quote_plus(oGuiElement.getCleanTitle()), sParams)
        else:
            sItemUrl = '%s?site=%s&function=%s&title=%s&%s' % (sPluginPath, oGuiElement.getSiteName(), oGuiElement.getFunction(), urllib.quote_plus(oGuiElement.getCleanTitle()), sParams)

        #print sItemUrl
        return sItemUrl
    
    def showKeyBoard(self, sDefaultText='', heading = ''):
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
        numboard = dialogs.numeric(0, 'Entrer la page', sDefaultNum)
        #numboard.doModal()
        if numboard != None:
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
