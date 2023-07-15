# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import xbmc

from resources.lib.comaddon import addon, isMatrix, isNexus
from resources.lib.db import cDb
from resources.lib.util import cUtil, QuoteSafe

# rouge E26543
# jaune F7D571
# bleu clair 87CEEC  ou skyblue / hoster
# vert 37BCB5
# bleu foncé 08435A / non utilisé


class cGuiElement:

    DEFAULT_FOLDER_ICON = 'icon.png'

    def __init__(self):

        self.addons = addon()

        # self.__sRootArt = cConfig().getRootArt()
        self.__sFunctionName = ''
        self.__sRootArt = 'special://home/addons/plugin.video.vstream/resources/art/'
        self.__sType = 'video'
        self.__sMeta = 0
        self.__sTrailer = ''
        self.__sMetaAddon = self.addons.getSetting('meta-view')
        self.__sMediaUrl = ''
        self.__sSiteUrl = ''
        # contient le titre qui sera coloré
        self.__sTitle = ''
        # contient le titre propre
        self.__sCleanTitle = ''
        # titre considéré Vu
        self.__sTitleWatched = ''
        self.__ResumeTime = 0   # Durée déjà lue de la vidéo
        self.__TotalTime = 0    # Durée totale de la vidéo

        # contient le titre modifié pour BDD
        self.__sFileName = ''
        self.__sDescription = ''
        self.__sGenre = ''
        self.__sThumbnail = ''
        self.__sPoster = ''
        self.__Season = ''
        self.__Episode = ''
        self.__sIcon = self.DEFAULT_FOLDER_ICON
        self.__sFanart = 'special://home/addons/plugin.video.vstream/fanart.jpg'
        self.poster = 'https://image.tmdb.org/t/p/%s' % self.addons.getSetting('poster_tmdb')
        self.fanart = 'https://image.tmdb.org/t/p/%s' % self.addons.getSetting('backdrop_tmdb')
        # For meta search
        # TmdbId the movie database https://developers.themoviedb.org/
        self.__TmdbId = ''
        # ImdbId pas d'api http://www.imdb.com/
        self.__ImdbId = ''
        self.__Year = ''

        self.__sRes = ''  # resolution

        self.__aItemValues = {}
        self.__aProperties = {}
        self.__aContextElements = []
        self.__sSiteName = ''

        # categorie utilisé pour marque-page et recherche.
        # 1 - movies/saga , 2 - tvshow/episode/anime, 5 - misc/Next
        self.__sCat = ''

    # def __len__(self): return self.__sCount

    # def getCount(self):
    #     return cGuiElement.COUNT

    def setType(self, sType):
        self.__sType = sType

    def getType(self):
        return self.__sType

    def setCat(self, sCat):
        self.__sCat = sCat

    def getCat(self):
        return self.__sCat

    def setMetaAddon(self, sMetaAddon):
        self.__sMetaAddon = sMetaAddon

    def getMetaAddon(self):
        return self.__sMetaAddon

    def setTrailer(self, sTrailer):
        self.__sTrailer = sTrailer

    def getTrailer(self):
        return self.__sTrailer

    def setTmdbId(self, data):
        self.__TmdbId = data if data != '0' else ''

    def getTmdbId(self):
        return self.__TmdbId

    def setImdbId(self, data):
        self.__ImdbId = data

    def getImdbId(self):
        return self.__ImdbId

    def setYear(self, data):
        self.__Year = data

    def getYear(self):
        return self.__Year

    def setRes(self, data):
        if data.upper() in ('1080P', 'FHD', 'FULLHD'):
            data = '1080p'
        elif data.upper() in ('720P', 'DVDRIP', 'DVDSCR', 'HD', 'HDLIGHT', 'HDRIP', 'BDRIP', 'BRRIP'):
            data = '720p'
        elif data.upper() in ('4K', 'UHD', '2160P'):
            data = '2160p'

        self.__sRes = data

    def getRes(self):
        return self.__sRes

    def setGenre(self, genre):
        self.__sGenre = genre

    def getGenre(self):
        return self.__sGenre

    def getSeason(self):
        return self.__Season

    def getEpisode(self):
        return self.__Episode

    def setTotalTime(self, data):
        self.__TotalTime = data

    def getTotalTime(self):
        return self.__TotalTime

    def setResumeTime(self, data):
        self.__ResumeTime = data

    def getResumeTime(self):
        return self.__ResumeTime

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
        self.__sFileName = cUtil().titleWatched(sFileName)

    def getFileName(self):
        return self.__sFileName

    def setFunction(self, sFunctionName):
        self.__sFunctionName = sFunctionName

    def getFunction(self):
        return self.__sFunctionName

    def TraiteTitre(self, sTitle):

        # convertion unicode ne fonctionne pas avec les accents
        try:
            # traitement du titre pour retirer le - quand c'est une Saison. Tiret, tiret moyen et cadratin
            sTitle = sTitle.replace('Season', 'saison').replace('season', 'saison').replace('SEASON', 'saison')\
                           .replace('Saison', 'saison').replace('SAISON', 'saison')
            sTitle = sTitle.replace(' - saison', ' saison').replace(' – saison', ' saison')\
                           .replace(' — saison', ' saison')

            if not isMatrix():
                sTitle = sTitle.decode('utf-8')
        except:
            pass

        """ Début du nettoyage du titre """
        # vire doubles espaces et double points
        sTitle = re.sub(' +', ' ', sTitle)
        sTitle = re.sub('\.+', '.', sTitle)

        # enleve les crochets et les parentheses si elles sont vides
        sTitle = sTitle.replace('()', '').replace('[]', '').replace('- -', '-')

        # vire espace et - a la fin
        sTitle = re.sub('[- –_\.\[]+$', '', sTitle)
        # et au debut
        sTitle = re.sub('^[- –_\.]+', '', sTitle)

        """ Fin du nettoyage du titre """

        # recherche l'année, uniquement si entre caractere special a cause de 2001 odysse de l'espace ou k2000
        string = re.search('[^\w ]([0-9]{4})[^\w ]', sTitle)
        if string:
            sTitle = sTitle.replace(string.group(0), '')
            self.__Year = str(string.group(1))
            self.addItemValues('year', self.__Year)

        # recherche une date
        string = re.search('([\d]{2}[\/|-]\d{2}[\/|-]\d{4})', sTitle)
        if string:
            sTitle = sTitle.replace(string.group(0), '')
            self.__Date = str(string.group(0))
            sTitle = '%s (%s) ' % (sTitle, self.__Date)

        # recherche les Tags restant : () ou [] sauf tag couleur
        sDecoColor = self.addons.getSetting('deco_color')
        sTitle = re.sub('([\(|\[](?!\/*COLOR)[^\)\(\]\[]+?[\]|\)])', '[COLOR ' + sDecoColor + ']\\1[/COLOR]', sTitle)

        # Recherche saisons et episodes
        sa = ep = ''
        m = re.search('(|S|saison)(\s?|\.)(\d+)(\s?|\.)(E|Ep|x|\wpisode)(\s?|\.)(\d+)', sTitle, re.UNICODE)
        if m:
            sTitle = sTitle.replace(m.group(0), '')
            sa = m.group(3)
            ep = m.group(7)
        else:  # Juste l'épisode
            m = re.search('(^|\s|\.)(E|Ep|\wpisode)(\s?|\.)(\d+)', sTitle, re.UNICODE)
            if m:
                sTitle = sTitle.replace(m.group(0), '')
                ep = m.group(4)
            else:  # juste la saison
                m = re.search('( S|saison)(\s?|\.)(\d+)', sTitle, re.UNICODE)
                if m:
                    sTitle = sTitle.replace(m.group(0), '')
                    sa = m.group(3)

        # enleve les crochets et les parentheses si elles sont vides
        if sa or ep:
            sTitle = sTitle.replace('()', '').replace('[]', '').replace('- -', '-')
            # vire espace et - a la fin
            sTitle = re.sub('[- –_\.\[]+$', '', sTitle)

        if sa:
            self.__Season = sa
            self.addItemValues('Season', self.__Season)
        if ep:
            self.__Episode = ep
            self.addItemValues('Episode', self.__Episode)

        # on repasse en utf-8
        if not isMatrix():
            try:
                sTitle = sTitle.encode('utf-8')
            except:
                pass

        # on reformate SXXEXX Titre [tag] (Annee)
        sTitle2 = ''
        if self.__Season:
            sTitle2 = sTitle2 + 'S%02d' % int(self.__Season)
        if self.__Episode:
            sTitle2 = sTitle2 + 'E%02d' % int(self.__Episode)

        # Titre unique pour marquer VU (avec numéro de l'épisode pour les séries)
        self.__sTitleWatched = cUtil().titleWatched(sTitle).replace(' ', '')
        if sTitle2:
            self.addItemValues('tvshowtitle', cUtil().getSerieTitre(sTitle))
            self.__sTitleWatched += '_' + sTitle2
        self.addItemValues('originaltitle', self.__sTitleWatched)

        if sTitle2:
            sTitle2 = '[COLOR %s]%s[/COLOR] ' % (sDecoColor, sTitle2)

        sTitle2 = sTitle2 + sTitle

        if self.__Year:
            sTitle2 = '%s [COLOR %s](%s)[/COLOR]' % (sTitle2, sDecoColor, self.__Year)

        return sTitle2

    # Permet de forcer le titre sans aucun traitement
    def setRawTitle(self, sTitle):
        self.__sTitle = sTitle
        
    def setTitle(self, sTitle):
        # Nom en clair sans les langues, qualités, et autres décorations
        self.__sCleanTitle = re.sub('\[.*\]|\(.*\)', '', sTitle)
        if not self.__sCleanTitle:
            self.__sCleanTitle = re.sub('\[.+?\]|\(.+?\)', '', sTitle)
            if not self.__sCleanTitle:
                self.__sCleanTitle = sTitle.replace('[', '').replace(']', '').replace('(', '').replace(')', '')

        if isMatrix():
            # Python 3 decode sTitle
            try:
                sTitle = str(sTitle.encode('latin-1'), 'utf-8')
            except:
                pass
        else:
            try:
                sTitle = str(sTitle.strip().decode('utf-8'))
            except:
                pass

        if not sTitle.startswith('[COLOR'):
            self.__sTitle = self.TraiteTitre(sTitle)
        else:
            self.__sTitle = sTitle

    def getTitle(self):
        return self.__sTitle

    def getCleanTitle(self):
        return self.__sCleanTitle

    def getTitleWatched(self):
        return self.__sTitleWatched

    def setDescription(self, sDescription):
        # Py3
        if isMatrix():
            try:
                if 'Ã' in sDescription or '\\xc' in sDescription:
                    self.__sDescription = str(sDescription.encode('latin-1'), 'utf-8')
                else:
                    self.__sDescription = sDescription
            except:
                self.__sDescription = sDescription
        else:
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
        if sFanart != '':
            self.__sFanart = sFanart

    def setMovieFanart(self):
        self.__sFanart = self.__sFanart

    def setTvFanart(self):
        self.__sFanart = self.__sFanart

    def setDirectTvFanart(self):
        self.__sFanart = self.__sFanart

    def setDirFanart(self, sIcon):
        self.__sFanart = self.__sFanart

    def getFanart(self):
        return self.__sFanart

    def setIcon(self, sIcon):
        if not sIcon:
            self.__sIcon = ''
            return
        try:
            self.__sIcon = unicode(sIcon, 'utf-8')
        except:
            self.__sIcon = sIcon
        self.__sIcon = self.__sIcon.encode('utf-8')
        self.__sIcon = QuoteSafe(self.__sIcon)

    def getIcon(self):
        # if 'http' in self.__sIcon:
        #    return UnquotePlus(self.__sIcon)
        folder = 'special://home/addons/plugin.video.vstream/resources/art'
        path = '/'.join([folder, self.__sIcon])
        # return os.path.join(unicode(self.__sRootArt, 'utf-8'), self.__sIcon)
        return path

    def addItemValues(self, sItemKey, mItemValue):
        self.__aItemValues[sItemKey] = mItemValue

    def getItemValue(self, sItemKey):
        if sItemKey not in self.__aItemValues:
            return
        return self.__aItemValues[sItemKey]

    def getWatched(self):

        # Fonctionne pour marquer lus un dossier
        if not self.getTitleWatched():
            return 0

        meta = {'titleWatched': self.getTitleWatched(),
                'site': self.getSiteUrl(),
                'cat': self.getCat()
                }

        with cDb() as db:
            data = db.get_watched(meta)
        return data

    def getInfoLabel(self):
        meta = {'title': xbmc.getInfoLabel('ListItem.title'),
                # 'label': xbmc.getInfoLabel('ListItem.title'),
                # 'originaltitle': xbmc.getInfoLabel('ListItem.originaltitle'),
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
                'poster_path': xbmc.getInfoLabel('ListItem.Art(thumb)'),
                'backdrop_path': xbmc.getInfoLabel('ListItem.Art(fanart)'),
                'imdbnumber': xbmc.getInfoLabel('ListItem.IMDBNumber'),
                'season': xbmc.getInfoLabel('ListItem.season'),
                'episode': xbmc.getInfoLabel('ListItem.episode'),
                'tvshowtitle': xbmc.getInfoLabel('ListItem.tvshowtitle')
                }

        if 'title' in meta and meta['title']:
            meta['title'] = self.getTitle()

        if 'backdrop_path' in meta and meta['backdrop_path']:
            url = meta.pop('backdrop_path')
            self.addItemProperties('fanart_image', url)
            self.__sFanart = url

        if 'trailer' in meta and meta['trailer']:
            self.__sTrailer = meta['trailer']

        if 'poster_path' in meta and meta['poster_path']:
            url = meta.pop('poster_path')
            self.__sThumbnail = url
            self.__sPoster = url

        # Completer au besoin
        for key, value in meta.items():
            if value:
                self.addItemValues(key, value)

        return

    def getMetadonne(self):
        metaType = self.getMeta()
        if metaType == 0:  # non media -> on sort, et on enleve le fanart
            self.addItemProperties('fanart_image', '')
            return

        from resources.lib.tmdb import cTMDb
        TMDb = cTMDb()

        sTitle = self.__sFileName

        # sTitle = self.__sTitle.decode('latin-1').encode('utf-8')
        # sTitle = re.sub(r'\[.*\]|\(.*\)', r'', str(self.__sFileName))
        # sTitle = sTitle.replace('VF', '').replace('VOSTFR', '').replace('FR', '')

        # On nettoie le titre pour la recherche
        sTitle = sTitle.replace('version longue', '')

        # Integrale de films, on nettoie le titre pour la recherche
        if metaType == 3:
            sTitle = sTitle.replace('integrales', '')
            sTitle = sTitle.replace('integrale', '')
            sTitle = sTitle.replace('2 films', '')
            sTitle = sTitle.replace('6 films', '')
            sTitle = sTitle.replace('7 films', '')
            sTitle = sTitle.replace('trilogie', '')
            sTitle = sTitle.replace('trilogy', '')
            sTitle = sTitle.replace('quadrilogie', '')
            sTitle = sTitle.replace('pentalogie', '')
            sTitle = sTitle.replace('octalogie', '')
            sTitle = sTitle.replace('hexalogie', '')
            sTitle = sTitle.replace('tetralogie', '')
            sTitle = sTitle.strip()
            if sTitle.endswith(' les'):
                sTitle = sTitle[:-4]
            elif sTitle.endswith(' la'):
                sTitle = sTitle[:-3]
            elif sTitle.endswith(' l'):
                sTitle = sTitle[:-2]
            sTitle = sTitle.strip()

        # tvshow
        if metaType in (2, 4, 5, 6):
            tvshowtitle = self.getItemValue('tvshowtitle')
            if tvshowtitle:
                sTitle = tvshowtitle

        sType = str(metaType).replace('1', 'movie').replace('2', 'tvshow').replace('3', 'collection')\
                             .replace('4', 'anime').replace('5', 'season').replace('6', 'episode')\
                             .replace('7', 'person').replace('8', 'network')

        meta = {}
        try:
            if sType:
                args = (sType, sTitle)
                kwargs = {}
                if self.__ImdbId:
                    kwargs['imdb_id'] = self.__ImdbId
                if self.__TmdbId:
                    kwargs['tmdb_id'] = self.__TmdbId
                if self.__Year:
                    kwargs['year'] = self.__Year
                if self.__Season:
                    kwargs['season'] = self.__Season
                if self.__Episode:
                    kwargs['episode'] = self.__Episode

                meta = TMDb.get_meta(*args, **kwargs)
                if not meta:
                    return
            else:
                return
        except:
            return

        if 'media_type' in meta:
            meta.pop('media_type')

        if 'imdb_id' in meta:
            imdb_id = meta.pop('imdb_id')
            if imdb_id:
                self.__ImdbId = imdb_id

        if 'tmdb_id' in meta:
            tmdb_id = meta.pop('tmdb_id')
            if tmdb_id:
                self.__TmdbId = tmdb_id

        if 'tvdb_id' in meta:
            meta.pop('tvdb_id')

        if 'backdrop_path' in meta:
            url = meta.pop('backdrop_path')
            if url:
                self.addItemProperties('fanart_image', url)
                self.__sFanart = url
            else:
                self.addItemProperties('fanart_image', '')

        if 'poster_path' in meta:
            url = meta.pop('poster_path')
            if url:
                self.__sThumbnail = url
                self.__sPoster = url

        if 'trailer' in meta and meta['trailer']:
            self.__sTrailer = meta['trailer']

        if 'guest_stars' in meta:
            meta.pop('guest_stars')

        if 'nbseasons' in meta:
            meta['season'] = meta.pop('nbseasons')

        # Retrait des tags intermédiaires
        if 'vote' in meta:
            meta.pop('vote')
        if 'runtime' in meta:
            meta.pop('runtime')
        if 'crew' in meta:
            meta.pop('crew')
        if 'overview' in meta:
            meta.pop('overview')
        if 'vote_average' in meta:
            meta.pop('vote_average')
        if 'vote_count' in meta:
            meta.pop('vote_count')
        if 'backdrop_url' in meta:
            meta.pop('backdrop_url')

        for key, value in meta.items():
            self.addItemValues(key, value)

        return

    def getItemValues(self):
        self.addItemValues('title', self.getTitle())

        # https://kodi.wiki/view/InfoLabels
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14

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

        if self.getMetaAddon() == 'true':
            self.getMetadonne()

        # tmdbid
        if self.getTmdbId():
            self.addItemProperties('TmdbId', str(self.getTmdbId()))
            # only for library content : self.addItemValues('DBID', str(self.getTmdbId()))

        # imdbid
        if self.getImdbId():
            self.addItemProperties('ImdbId', str(self.getImdbId()))
            # self.addItemValues('imdbnumber', str(self.getTmdbId()))

        # Utilisation des infos connues si non trouvées
        if not self.getItemValue('plot') and self.getDescription():
            self.addItemValues('plot', self.getDescription())
        if not self.getItemValue('year') and self.getYear():
            self.addItemValues('year', self.getYear())
        if not self.getItemValue('genre') and self.getGenre():
            self.addItemValues('genre', self.getGenre())
        # if not self.getItemValue('cover_url') and self.getThumbnail():
            # self.addItemValues('cover_url', self.getThumbnail())
        # if not self.getItemValue('backdrop_path') and self.getPoster():
            # self.addItemValues('backdrop_path', self.getPoster())
        if not self.getItemValue('trailer'):
            if self.getTrailer():
                self.addItemValues('trailer', self.getTrailer())
            else:
                self.addItemValues('trailer', 'plugin')  # Faux trailer qui ne se lance pas mais evite une erreur
                # self.addItemValues('trailer', self.getDefaultTrailer())

        # Used only if there is data in db, overwrite getMetadonne()
        sCat = str(self.getCat())
        try:
            if sCat and int(sCat) in (1, 2, 3, 4, 5, 8, 9):  # Vérifier seulement si de type média
                if self.getWatched():
                    self.addItemValues('playcount', 1)
        except:
            sCat = False

        self.addItemProperties('siteUrl', self.getSiteUrl())
        self.addItemProperties('sCleanTitle', self.getFileName())
        self.addItemProperties('sId', self.getSiteName())
        self.addItemProperties('sFav', self.getFunction())
        self.addItemProperties('sMeta', str(self.getMeta()))
        if isNexus():
            self.addItemValues('resumetime', self.getResumeTime())
            self.addItemValues('totaltime', self.getTotalTime())
        else:
            self.addItemProperties('resumetime', self.getResumeTime())
            self.addItemProperties('totaltime', self.getTotalTime())

        if sCat:
            self.addItemProperties('sCat', sCat)
            mediatypes = {'1': 'movie', '2': 'tvshow', '3': 'tvshow', '4': 'season', '5': 'video',
                          '6': 'video', '7': 'season', '8': 'episode', '9': 'tvshow'}
            if sCat in mediatypes.keys():
                mediatype = mediatypes.get(sCat)
                self.addItemValues('mediatype', mediatype)  # video, movie, tvshow, season, episode, musicvideo

        if self.getSeason():
            self.addItemValues('season', int(self.getSeason()))

        if self.getEpisode():
            self.addItemValues('episode', int(self.getEpisode()))

        return self.__aItemValues

    def addItemProperties(self, sPropertyKey, mPropertyValue):
        self.__aProperties[sPropertyKey] = mPropertyValue

    def getItemProperties(self):
        return self.__aProperties

    def addContextItem(self, oContextElement):
        self.__aContextElements.append(oContextElement)

    def getContextItems(self):
        return self.__aContextElements
