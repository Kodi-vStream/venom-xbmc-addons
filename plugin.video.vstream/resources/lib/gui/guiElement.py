#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
from resources.lib.db import cDb

import os, re, urllib, string, xbmc

class cGuiElement:

    DEFAULT_FOLDER_ICON = 'icon.png'
    COUNT = 0

    def __init__(self):
        self.__sRootArt = cConfig().getRootArt()
        self.__sType = 'Video'
        self.__sMeta = 0
        self.__sPlaycount = 0
        self.__sTrailerUrl = ''
        self.__sMetaAddon = cConfig().getSetting('meta-view')
        self.__sTmdb = ''
        self.__sMediaUrl = ''
        self.__sSiteUrl = ''
        self.__sTitle = ''
        self.__sTitleSecond = ''
        self.__sFileName = ''
        self.__sDescription = ''
        self.__sThumbnail = ''
        self.__sIcon = self.DEFAULT_FOLDER_ICON
        self.__sFanart = self.__sRootArt+'fanart.jpg'
        
        self.__sFanart_search = self.__sRootArt+'search_fanart.jpg'
        self.__sFanart_tv = self.__sRootArt+'tv_fanart.jpg'
        self.__sFanart_films = self.__sRootArt+'films_fanart.jpg'
        self.__sFanart_series = self.__sRootArt+'series_fanart.jpg'
        self.__sFanart_animes = self.__sRootArt+'animes_fanart.jpg'
        self.__sFanart_doc = self.__sRootArt+'doc_fanart.jpg'
        self.__sFanart_sport = self.__sRootArt+'sport_fanart.jpg'
        self.__sFanart_buzz = self.__sRootArt+'buzz_fanart.jpg'
        self.__sFanart_mark = self.__sRootArt+'mark_fanart.jpg'
        self.__sFanart_host = self.__sRootArt+'host_fanart.jpg'
        self.__sFanart_download = self.__sRootArt+'download_fanart.jpg'
        
        self.__aItemValues = {}
        self.__aProperties = {}
        self.__aContextElements = []
        self.__sSiteName = ''
        self.__sCat = ''
        cGuiElement.COUNT += 1
        
    #def __len__(self): return self.__sCount
    
    def getCount(self): 
        return cGuiElement.COUNT

    def setType(self, sType):
        self.__sType = sType

    def getType(self):
        return self.__sType
        
    def setTmdb(self, sTmdb):
        self.__sTmdb = sTmdb

    def getTmdb(self):
        return self.__sTmdb
        
    def setCat(self, sCat):
        self.__sCat = sCat

    def getCat(self):
        return self.__sCat
     
    def setMetaAddon(self, sMetaAddon):
        self.__sMetaAddon = sMetaAddon

    def getMetaAddon(self):
        return self.__sMetaAddon
        
    def setTrailerUrl(self, sTrailerUrl):
        self.__sTrailerUrl = sTrailerUrl

    def getTrailerUrl(self):
        return self.__sTrailerUrl
        
    def setMeta(self, sMeta):
        self.__sMeta = sMeta

    def getMeta(self):
        return self.__sMeta

    def setMediaUrl(self, sMediaUrl):
        self.__sMediaUrl = sMediaUrl

    def getMediaUrl(self):
        return self.__sMediaUrl
        
    def setSiteUrl(self, sSiteUrl):
        self.__sSiteUrl = sSiteUrl

    def getSiteUrl(self):
        return self.__sSiteUrl

    def setSiteName(self, sSiteName):
        self.__sSiteName = sSiteName

    def getSiteName(self):
        return self.__sSiteName
         
    def setFileName(self, sFileName):
        self.__sFileName = self.str_conv(sFileName)

    def getFileName(self):
        return self.__sFileName
        
    def setFunction(self, sFunctionName):
        self.__sFunctionName = sFunctionName

    def getFunction(self):
        return self.__sFunctionName

    def setTitle(self, sTitle):
        self.__sTitle = sTitle;

    def getTitle(self):
        return self.__sTitle

    def setTitleSecond(self, sTitleSecond):
        self.__sTitleSecond = sTitleSecond

    def getTitleSecond(self):
        return self.__sTitleSecond

    def setDescription(self, sDescription):
        self.__sDescription = sDescription

    def getDescription(self):
        return self.__sDescription

    def setThumbnail(self, sThumbnail):
        self.__sThumbnail = sThumbnail

    def getThumbnail(self):
        return self.__sThumbnail
    
    def setFanart(self, sFanart):
        if (sFanart != ''):
            self.__sFanart = sFanart
        else:
            self.__sFanart = self.__sRootArt+'fanart.jpg'
            
            
    def setMovieFanart(self):
            self.__sFanart = self.__sFanart_films
            
    def setTvFanart(self):
            self.__sFanart = self.__sFanart_series
            
    def setDirectTvFanart(self):
            self.__sFanart = self.__sFanart_tv
        
    def setDirFanart(self, sIcon):
        if (sIcon == 'search.png'):
            self.__sFanart = cConfig().getSetting('images_cherches')
            
        elif (sIcon == 'searchtmdb.png'):
            self.__sFanart = cConfig().getSetting('images_cherchev')
            
        elif sIcon == 'tv.png':
            self.__sFanart = cConfig().getSetting('images_tvs')
        elif ('replay' in sIcon):
            self.__sFanart = cConfig().getSetting('images_replaytvs')
            
        elif ('films' in sIcon):
            self.__sFanart = cConfig().getSetting('images_films')
            
        elif ('series' in sIcon):
            self.__sFanart = cConfig().getSetting('images_series')
            
        elif ('animes' in sIcon):
            self.__sFanart = cConfig().getSetting('images_anims')
            
        elif sIcon == 'doc.png':
            self.__sFanart = cConfig().getSetting('images_docs')
            
        elif sIcon == 'sport.png':
            self.__sFanart = cConfig().getSetting('images_sports')
            
        elif sIcon == 'buzz.png':
            self.__sFanart = cConfig().getSetting('images_videos')
            
        elif sIcon == 'mark.png':
            self.__sFanart = cConfig().getSetting('images_marks')
            
        elif sIcon == 'host.png':
            self.__sFanart = cConfig().getSetting('images_hosts')
         
        elif sIcon == 'download.png':
            self.__sFanart = cConfig().getSetting('images_downloads')
        
        elif sIcon == 'update.png':
            self.__sFanart = cConfig().getSetting('images_updates')
            
        elif sIcon == 'library.png':
            self.__sFanart = cConfig().getSetting('images_librarys')
            
        elif xbmc.getInfoLabel('ListItem.Art(fanart)') != '':
            self.__sFanart = xbmc.getInfoLabel('ListItem.Art(fanart)')
            
        else :
            self.__sFanart = self.__sFanart

    def getFanart(self):
        return self.__sFanart

    def setIcon(self, sIcon):
        self.__sIcon = sIcon

    def getIcon(self):
        #return self.__sRootArt+self.__sIcon
        return os.path.join(unicode(self.__sRootArt, 'utf-8'), self.__sIcon)

    def addItemValues(self, sItemKey, mItemValue):
        self.__aItemValues[sItemKey] = mItemValue
        
    def getWatched(self):
        meta = {}
        meta['title'] = urllib.quote_plus(self.getTitle())
        meta['site'] = self.getSiteUrl()

        data = cDb().get_watched(meta)
        return data   
    
        
    def setWatched(self, sId, sTitle):
        try:
            watched = {}
            #sTitle = self.getTitle()
            #sId = self.getSiteName()
            watched_db = os.path.join(cConfig().getSettingCache(), "watched.db" )
            
            if not os.path.exists(watched_db):
                file(watched_db, "w").write("%r" % watched) 

            if os.path.exists(watched_db):
                watched = eval(open(watched_db).read() )
                watched[ sId ] = watched.get( sId ) or []
                #add to watched
                if sTitle not in watched[sId]:
                     watched[ sId ].append( sTitle )
                else:
                    del watched[ sId ][ watched[ sId ].index( sTitle ) ]
            
            file(watched_db, "w").write("%r" % watched)
            watched_db.close()
        except:
            return

    
    def str_conv(self, data):
        if isinstance(data, str):
            # Must be encoded in UTF-8
            data = data.decode('utf8')
        
        import unicodedata
        data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
        data=re.sub(r'\[.*\]|\(.*\)',r'',str(data))
        data=data.replace('VF','').replace('VOSTFR','').replace('FR','')
        data=re.sub(r'[0-9]+?',r'',str(data))
        data=data.replace('-','').replace('Saison','').replace('saison','').replace('Season','').replace('Episode','').replace('episode','')
        data = re.sub('[^%s]' % string.ascii_lowercase, ' ', data.lower())
        #data = urllib.quote_plus(data)
        
        #data = data.decode('string-escape')
        
        return data
        
    def getInfoLabel(self):
        meta = {
        'title': xbmc.getInfoLabel('ListItem.title'),
        'label': xbmc.getInfoLabel('ListItem.title'),         
        'originaltitle': xbmc.getInfoLabel('ListItem.originaltitle'), 
        'year': xbmc.getInfoLabel('ListItem.year'), 
        'genre': xbmc.getInfoLabel('ListItem.genre'), 
        'director': xbmc.getInfoLabel('ListItem.director'), 
        'country': xbmc.getInfoLabel('ListItem.country'), 
        'rating': xbmc.getInfoLabel('ListItem.rating'), 
        'votes': xbmc.getInfoLabel('ListItem.votes'), 
        'mpaa': xbmc.getInfoLabel('ListItem.mpaa'), 
        'duration': xbmc.getInfoLabel('ListItem.duration'), 
        'trailer': xbmc.getInfoLabel('ListItem.trailer'), 
        'writer': xbmc.getInfoLabel('ListItem.writer'), 
        'studio': xbmc.getInfoLabel('ListItem.studio'), 
        'tagline': xbmc.getInfoLabel('ListItem.tagline'), 
        'plotoutline': xbmc.getInfoLabel('ListItem.plotoutline'), 
        'plot': xbmc.getInfoLabel('ListItem.plot'),
        'cover_url': xbmc.getInfoLabel('ListItem.Art(thumb)'),
        'backdrop_url': xbmc.getInfoLabel('ListItem.Art(fanart)')
        }
        
        if meta['title']:
            meta['title'] = self.getTitle()
            
        for key, value in meta.items():
            self.addItemValues(key, value)
        
        if meta['backdrop_url']:
            self.addItemProperties('fanart_image', meta['backdrop_url'])
            self.__sFanart = meta['backdrop_url']
        if meta['trailer']:
            meta['trailer'] = meta['trailer'].replace(u'\u200e', '').replace(u'\u200f', '')
            self.__sTrailerUrl = meta['trailer']
        if meta['cover_url']:
            self.__sThumbnail = meta['cover_url']
        
        return
    def getMetadonne(self):
        # try:
            # from metahandler import metahandlers
            # grab = metahandlers.MetaData(preparezip=False)
        # except :
            # return
            
        #sTitle = self.__sTitle.decode('latin-1').encode("utf-8")
        #sTitle=re.sub(r'\[.*\]|\(.*\)',r'',str(self.__sFileName))
        #sTitle=sTitle.replace('VF','').replace('VOSTFR','').replace('FR','')

        if self.getMeta() == 1:
            try:
                from metahandler import metahandlers
                grab = metahandlers.MetaData(preparezip=False,  tmdb_api_key='92ab39516970ab9d86396866456ec9b6')
                meta = grab.get_meta('movie',self.__sFileName)
            except:
                return
        elif self.getMeta() == 2:
            try:
                from metahandler import metahandlers
                grab = metahandlers.MetaData(preparezip=False, tmdb_api_key='92ab39516970ab9d86396866456ec9b6')
            #sTitle=re.sub(r'[0-9]+?',r'',str(sTitle))
            #sTitle=sTitle.replace('-','').replace('Saison','').replace('saison','').replace('Season','').replace('Episode','').replace('episode','')
                meta = grab.get_meta('tvshow',self.__sFileName)
            except:
                return
        else:
            return
        del meta['playcount']
        del meta['trailer']
        
        if meta['title']:
            meta['title'] = self.getTitle()
            
        for key, value in meta.items():
            self.addItemValues(key, value)
         
        if meta['imdb_id']:
            self.__sImdb = meta['imdb_id']         
        if meta['backdrop_url']:
            self.addItemProperties('fanart_image', meta['backdrop_url'])
            self.__sFanart = meta['backdrop_url']
        # if meta['trailer_url']:
            # meta['trailer'] = meta['trailer'].replace(u'\u200e', '').replace(u'\u200f', '')
            # self.__sTrailerUrl = meta['trailer']
        if meta['cover_url']:
            self.__sThumbnail = meta['cover_url']
        return

    def getItemValues(self):
        self.__aItemValues['Title'] = self.getTitle()
        self.__aItemValues['Plot'] = self.getDescription()
        self.__aItemValues['Playcount'] = self.getWatched()
        self.addItemProperties('fanart_image', self.__sFanart)
        

        if self.getMeta() > 0 and self.getMetaAddon() == 'true':
            self.getMetadonne()
        return self.__aItemValues
    
    def addItemProperties(self, sPropertyKey, mPropertyValue):
        self.__aProperties[sPropertyKey] = mPropertyValue

    def getItemProperties(self):
        return self.__aProperties

    def addContextItem(self, oContextElement):
        self.__aContextElements.append(oContextElement)

    def getContextItems(self):
        return self.__aContextElements

