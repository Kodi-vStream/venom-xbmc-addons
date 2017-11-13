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
        self.__sImdb = ''
        self.__sTmdb = ''
        self.__sMediaUrl = ''
        self.__sSiteUrl = ''
        #contient le titre qui seras colorer
        self.__sTitle = ''
        #contient le titre propre
        self.__sCleanTitle = ''
        #vide
        self.__sTitleSecond = ''
        #contient le titre modifier pour BDD
        self.__sFileName = ''
        self.__sDescription = ''
        self.__sThumbnail = ''
        self.__sPoster = ''
        self.__Season = ''
        self.__Episode = ''
        self.__sIcon = self.DEFAULT_FOLDER_ICON
        self.__sFanart = self.__sRootArt+'fanart.jpg'
        self.__sDecoColor = cConfig().getSetting('deco_color')

        #For meta search
        #TmdbId the movie database https://developers.themoviedb.org/
        self.__TmdbId = ''
        #ImdbId pas d'api http://www.imdb.com/
        self.__ImdbId = ''
        self.__Year = ''

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
        #categorie utiliser pour marque page et recherche.
        #1 - movies , 2 - tvshow, - 3 misc,
        #oGuiElement.setCat(1)
        self.__sCat = ''
        cGuiElement.COUNT += 1

    #def __len__(self): return self.__sCount

    def getCount(self):
        return cGuiElement.COUNT

    def setType(self, sType):
        self.__sType = sType

    def getType(self):
        return self.__sType

    #utiliser setImdbId
    def setImdb(self, sImdb):
        self.__ImdbId = sImdb
    #utiliser  getImdbId
    def getImdb(self):
        return self.__ImdbId

    #utiliser  setTmdbId
    def setTmdb(self, sTmdb):
        self.__TmdbId = sTmdb
    #utiliser  getTmdbId
    def getTmdb(self):
        return self.__TmdbId

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

    def setTmdbId(self,data):
        self.__TmdbId = data

    def getTmdbId(self):
        return self.__TmdbId

    def setImdbId(self,data):
        self.__ImdbId = data

    def getImdbId(self):
        return self.__ImdbId

    def setYear(self,data):
        self.__Year = data

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

    def TraiteTitre(self, sTitle):

        # Format Obligatoire a traiter via le fichier site
        #-------------------------------------------------
        # Episode 7 a 9 > Episode 7-9
        # Saison 1 à ? > Saison 1-?
        # Format de date > 11/22/3333 ou 11-22-3333

        #convertion unicode ne fonctionne pas avec les accents

        try:
            sTitle = sTitle.decode("utf-8")
        except:
            pass

        #recherche l'année, uniquement si entre caractere special a cause de 2001 odysse de l'espace ou k2000
        string = re.search('([^\w ][0-9]{4}[^\w ])', sTitle)
        if string:
            sTitle = sTitle.replace(string.group(0),'')
            self.__Year = str(string.group(0)[1:5])
            self.addItemValues('Year', self.__Year)

        #recherche une date
        string = re.search('([\d]{2}[\/|-]\d{2}[\/|-]\d{4})', sTitle)
        if string:
            sTitle = sTitle.replace(string.group(0),'')
            self.__Date = str(string.group(0))
            sTitle = "%s (%s) " %(sTitle ,self.__Date)

        #~ #recherche Lang
        #~ index = { ' vostfr' : ' [VOSTFR]', ' vf' : ' [VF]', ' truefrench' : ' [TrueFrench]' }
        #~ for cle in index:
            #~ sTitle=sTitle.replace(cle.upper(), index[cle]).replace(cle, index[cle]).replace('(%s)' % (cle), index[cle])

        #~ #recherche Qualiter
        #~ index = { '1080i' : '(1080)', '1080p' : '(1080)', '1080I' : '(1080)', '1080P' : '(1080)', '720i' : '(720)', '720p' : '(720)', '720I' : '(720)', '720P' : '(720)' }
        #~ for cle in index:
            #~ sTitle=sTitle.replace(cle, index[cle]).replace('[%s]' % (cle), index[cle])

        #Recherche saison et episode a faire pr serie uniquement
        if (True):
            SXEX = ''

            #m = re.search( ur'(?i)(\wpisode ([0-9\.\-\_]+))',sTitle,re.UNICODE)
            m = re.search(ur'(?i)(?:^|[^a-z])((?:E|(?:\wpisode\s?))([0-9]+(?:[\-\.][0-9\?]+)*))', sTitle,re.UNICODE)
            if m:
                #ok y a des episodes
                sTitle = sTitle.replace(m.group(1),'')
                ep = m.group(2)
                if len(ep) == 1:
                    ep = '0' + ep
                self.__Episode = ep
                self.addItemValues('Episode', self.__Episode)

                #pr les saisons
                m = re.search(ur'(?i)(s(?:aison +)*([0-9]+(?:\-[0-9\?]+)*))', sTitle,re.UNICODE)
                if m:
                    sTitle = sTitle.replace(m.group(1),'')
                    sa = m.group(2)
                    if len(sa) == 1:
                        sa = '0' + sa
                    self.__Season = sa
                    self.addItemValues('Season', self.__Season)

            else:
                #pas d'episode mais y a t il des saisons ?
                #m = re.search('(?i)(s(?:aison +)*([0-9]+[0-9\-\?]*))(?:$| )', sTitle)
                m = re.search(ur'(?i)(s(?:aison +)*([0-9]+(?:\-[0-9\?]+)*))', sTitle,re.UNICODE)
                if m:
                    sTitle = sTitle.replace(m.group(1),'')
                    sa = m.group(2)
                    if len(sa) == 1:
                        sa = '0' + sa
                    self.__Season = sa
                    self.addItemValues('Season', self.__Season)

        #supr les -
        #sTitle = sTitle.replace('-',' ') # A gerer dans le fichier site plutot, car il peut etre utile dans certain cas
        #vire doubles espaces
        sTitle = re.sub(' +',' ',sTitle)
        sTitle = sTitle.replace('()','').replace('- -','-')

        #vire espace a la fin et les - (attention, il y a 2 tirets differents meme si invisible a l'oeuil nu et un est en unicode)
        sTitle = re.sub(ur'[- –]+$','',sTitle)
        #et en debut
        if sTitle.startswith(' '):
            sTitle = sTitle[1:]

        #recherche les Tags restant : () ou [] sauf tag couleur
        sTitle = re.sub(ur'([\(|\[](?!\/*COLOR)[^\)\(\]\[]+?[\]|\)])','[COLOR '+self.__sDecoColor+']\\1[/COLOR]', sTitle)

        #on reformate SXXEXX Titre [tag] (Annee)
        sTitle2 = ''
        if self.__Season:
            sTitle2 = sTitle2 + 'S' + self.__Season
        if self.__Episode:
            sTitle2 = sTitle2 + 'E' + self.__Episode
        if sTitle2:
            sTitle2 = "[COLOR %s]%s[/COLOR] "%(self.__sDecoColor,sTitle2)

        sTitle2 = sTitle2 + sTitle

        if self.__Year:
            sTitle2 = "%s [COLOR %s](%s)[/COLOR]"%(sTitle2,self.__sDecoColor,self.__Year)

        #xbmc.log('>>' + sTitle2, xbmc.LOGNOTICE)

        #on repasse en utf-8
        return sTitle2.encode('utf-8')

    def getEpisodeTitre(self, sTitle):

        string = re.search('(?i)(e(?:[a-z]+sode\s?)*([0-9]+))', str(sTitle))
        if string:
            sTitle = sTitle.replace(string.group(1),'')
            self.__Episode = ("%02d" % int(string.group(2)))
            sTitle = "%s [COLOR %s]E%s[/COLOR]"%(sTitle, self.__sDecoColor, self.__Episode)
            self.addItemValues('Episode', self.__Episode)
            return sTitle, True

        return sTitle, False

    def setTitle(self, sTitle):
        self.__sTitle = sTitle

    def getTitle(self):

        sTitle = self.__sTitle
        if type(sTitle) is dict:
            sTitle = self.RangeTitle(sTitle)
        #titre normal
        else:
            if not sTitle.startswith('[COLOR'):
                sTitle = self.TraiteTitre(sTitle)
        return sTitle

    def getCleanTitle(self):
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

    def setPoster(self, sPoster):
        self.__sPoster = sPoster

    def getPoster(self):
        return self.__sPoster

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

        elif sIcon == 'trakt.png':
            self.__sFanart = cConfig().getSetting('images_trakt')

        elif sIcon == 'actor.png':
            self.__sFanart = self.__sFanart

        elif sIcon == 'star.png':
            self.__sFanart = self.__sFanart

        elif xbmc.getInfoLabel('ListItem.Art(fanart)') != '':
            self.__sFanart = xbmc.getInfoLabel('ListItem.Art(fanart)')

        else :
            self.__sFanart = self.__sFanart
        return self.__sFanart

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

        #Fonctionne pour marquer lus un dossier
        if not self.getTitle():
            return ''

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
            watched_db = os.path.join(cConfig().getSettingCache(), "watched.db" ).decode("utf-8")

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
        #cherche la saison et episode puis les balises [color]titre[/color]
        #data, saison = self.getSaisonTitre(data)
        #data, episode = self.getEpisodeTitre(data)
        #supprimer les balises
        data=re.sub(r'\[.*\]|\(.*\)',r'',str(data))
        data=data.replace('VF','').replace('VOSTFR','').replace('FR','')
        #data=re.sub(r'[0-9]+?',r'',str(data))
        data=data.replace('-','')
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
        'backdrop_url': xbmc.getInfoLabel('ListItem.Art(fanart)'),
        'imdb_id': xbmc.getInfoLabel('ListItem.IMDBNumber'),
        'season': xbmc.getInfoLabel('ListItem.season'),
        'episode': xbmc.getInfoLabel('ListItem.episode')
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
            self.__sPoster = meta['cover_url']

        return

    def getMetadonne(self):

        #sTitle = self.__sTitle.decode('latin-1').encode("utf-8")
        #sTitle=re.sub(r'\[.*\]|\(.*\)',r'',str(self.__sFileName))
        #sTitle=sTitle.replace('VF','').replace('VOSTFR','').replace('FR','')

        #get_meta(self, media_type, name, imdb_id='', tmdb_id='', year='', overlay=6, update=False):
        sType = '1'
        sType = str(self.getMeta()).replace('1','movie').replace('2','tvshow')

        if sType:
            from resources.lib.tmdb import cTMDb
            grab = cTMDb(api_key=cConfig().getSetting('api_tmdb'))
            args = (sType, self.__sFileName)
            kwargs = {}
            if (self.__ImdbId):
                kwargs['imdb_id'] = self.__ImdbId
            if (self.__TmdbId):
                kwargs['tmdb_id'] = self.__TmdbId
            if (self.__Year):
                kwargs['year'] =  self.__Year
            if (self.__Season):
                kwargs['season'] =  self.__Season
            if (self.__Episode):
                kwargs['episode'] =  self.__Episode
            meta = grab.get_meta(*args, **kwargs)

        else :
            return

        #Pour les films
        # if self.getMeta() == 1:
            # try:
                # from metahandler import metahandlers
                # grab = metahandlers.MetaData(preparezip=False,  tmdb_api_key=cConfig().getSetting('api_tmdb'))
                # args = ("movie", self.__sFileName)
                # kwargs = {}
                # if (self.__TmdbId) or (self.__Year):
                    # if (self.__ImdbId):
                        # kwargs['imdb_id'] = self.__ImdbId
                    # if (self.__TmdbId):
                        # kwargs['tmdb_id'] = self.__TmdbId
                    # if (self.__Year):
                        # kwargs['year'] =  self.__Year
                # meta = grab.get_meta(*args, **kwargs)
            # except:
                # return

        #Pour les series
        # elif self.getMeta() == 2:
            # try:
                # from metahandler import metahandlers
                # grab = metahandlers.MetaData(preparezip=False, tmdb_api_key=cConfig().getSetting('api_tmdb'))
               # Nom a nettoyer ?
                #attention l'annee peut mettre le bordel a cause des differences de sortie
                # args = ("tvshow", self.__sFileName)
                # kwargs = {}
                # if (self.__TmdbId) or (self.__Year):
                    # dict = {}
                    # if (self.__ImdbId):
                        # kwargs['imdb_id'] = self.__ImdbId
                    # if (self.__TmdbId):
                        # kwargs['tmdb_id'] = self.__TmdbId
                    # if (self.__Year):
                        # kwargs['year'] =  self.__Year
                # meta = grab.get_meta(*args, **kwargs)
            # except:
                # return
        # else:
            # return

        del meta['playcount']
        del meta['trailer']

        if meta['title']:
            meta['title'] = self.getTitle()

        for key, value in meta.items():
            self.addItemValues(key, value)

        if meta['imdb_id']:
            self.__ImdbId = meta['imdb_id']

        try:
            if meta['tmdb_id']:
                self.__TmdbId = meta['tmdb_id']
        except: pass

        try:
            if meta['tvdb_id']:
                self.__TmdbId = meta['tvdb_id']
        except: pass

        if meta['backdrop_url']:
            self.addItemProperties('fanart_image', meta['backdrop_url'])
            self.__sFanart = meta['backdrop_url']
        # if meta['trailer_url']:
            # meta['trailer'] = meta['trailer'].replace(u'\u200e', '').replace(u'\u200f', '')
            # self.__sTrailerUrl = meta['trailer']
        if meta['cover_url']:
            self.__sThumbnail = meta['cover_url']
            self.__sPoster = meta['cover_url']
        return

    def getItemValues(self):
        self.__aItemValues['Title'] = self.getTitle()
        self.__aItemValues['Plot'] = self.getDescription()
        self.__aItemValues['Playcount'] = self.getWatched()
        #tmdbid
        if self.getTmdbId():
            self.addItemProperties('TmdbId', str(self.getTmdbId()))

        #self.addItemProperties('fanart_image', self.__sFanart)

         # - Video Values:
        # - genre : string (Comedy)
        # - year : integer (2009)
        # - episode : integer (4)
        # - season : integer (1)
        # - top250 : integer (192)
        # - tracknumber : integer (3)
        # - rating : float (6.4) - range is 0..10
        # - watched : depreciated - use playcount instead
        # - playcount : integer (2) - number of times this item has been played
        # - overlay : integer (2) - range is 0..8. See GUIListItem.h for values
        # - cast : list (Michal C. Hall)
        # - castandrole : list (Michael C. Hall|Dexter)
        # - director : string (Dagur Kari)
        # - mpaa : string (PG-13)
        # - plot : string (Long Description)
        # - plotoutline : string (Short Description)
        # - title : string (Big Fan)
        # - originaltitle : string (Big Fan)
        # - sorttitle : string (Big Fan)
        # - duration : string (3:18)
        # - studio : string (Warner Bros.)
        # - tagline : string (An awesome movie) - short description of movie
        # - writer : string (Robert D. Siegel)
        # - tvshowtitle : string (Heroes)
        # - premiered : string (2005-03-04)
        # - status : string (Continuing) - status of a TVshow
        # - code : string (tt0110293) - IMDb code
        # - aired : string (2008-12-07)
        # - credits : string (Andy Kaufman) - writing credits
        # - lastplayed : string (Y-m-d h:m:s = 2009-04-05 23:16:04)
        # - album : string (The Joshua Tree)
        # - artist : list (['U2'])
        # - votes : string (12345 votes)
        # - trailer : string (/home/user/trailer.avi)
        # - dateadded : string (Y-m-d h:m:s = 2009-04-05 23:16:04)


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
