#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#Venom.
from resources.lib.comaddon import addon, xbmc
from resources.lib.db import cDb
from resources.lib.util import QuoteSafe
import re, string

#rouge E26543
#jaune F7D571
#bleu clair 87CEEC  ou skyblue / hoster
#vert 37BCB5
#bleu foncer 08435A / non utiliser


class cGuiElement:

    DEFAULT_FOLDER_ICON = 'icon.png'
    #COUNT = 0
    ADDON = addon()
    DB = cDb()

    def __init__(self):

        #self.__sRootArt = cConfig().getRootArt()
        self.__sRootArt = 'special://home/addons/plugin.video.vstream/resources/art/'
        self.__sType = 'Video'
        self.__sMeta = 0
        self.__sPlaycount = 0
        self.__sTrailerUrl = ''
        self.__sMetaAddon = self.ADDON.getSetting('meta-view')
        self.__sImdb = ''
        self.__sTmdb = ''
        self.__sMediaUrl = ''
        self.__sSiteUrl = ''
        # contient le titre qui sera coloré
        self.__sTitle = ''
        # contient le titre propre
        self.__sCleanTitle = ''
        # titre considéré Vu
        self.__sTitleWatched = ''
        # contient le titre modifié pour BDD
        self.__sFileName = ''
        self.__sDescription = ''
        self.__sThumbnail = ''
        self.__sPoster = ''
        self.__Season = ''
        self.__Episode = ''
        self.__sIcon = self.DEFAULT_FOLDER_ICON
        self.__sFanart = 'special://home/addons/plugin.video.vstream/fanart.jpg'
        self.__sDecoColor = self.ADDON.getSetting('deco_color')

        # For meta search
        # TmdbId the movie database https://developers.themoviedb.org/
        self.__TmdbId = ''
        # ImdbId pas d'api http://www.imdb.com/
        self.__ImdbId = ''
        self.__Year = ''

        self.__aItemValues = {}
        self.__aProperties = {}
        self.__aContextElements = []
        self.__sSiteName = ''
        # categorie utiliser pour marque page et recherche.
        # 1 - movies , 2 - tvshow, - 3 misc,
        #oGuiElement.setCat(1)
        self.__sCat = ''
        #cGuiElement.COUNT += 1

    #def __len__(self): return self.__sCount

    # def getCount(self):
    #     return cGuiElement.COUNT

    def setType(self, sType):
        self.__sType = sType

    def getType(self):
        return self.__sType

    # utiliser setImdbId
    def setImdb(self, sImdb):
        self.__ImdbId = sImdb
    # utiliser  getImdbId
    def getImdb(self):
        return self.__ImdbId

    # utiliser  setTmdbId
    def setTmdb(self, sTmdb):
        self.__TmdbId = sTmdb
    # utiliser  getTmdbId
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

    def setTmdbId(self, data):
        self.__TmdbId = data

    def getTmdbId(self):
        return self.__TmdbId

    def setImdbId(self, data):
        self.__ImdbId = data

    def getImdbId(self):
        return self.__ImdbId

    def setYear(self, data):
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

        # convertion unicode ne fonctionne pas avec les accents

        try:
            # traitement du titre pour les caracteres speciaux
            sTitle = sTitle.replace('&#884;', '\'').replace('&#8212;', '-').replace('&#8217;', '\'').replace('&#8230;', '...').replace('&#8242;', '\'').replace('&lsquo;', '\'')
            # traitement du titre pour retirer le - quand c'est une Saison. Tiret, tiret moyen et cadratin
            sTitle = sTitle.replace(' - Saison', ' Saison').replace(' – Saison', ' Saison').replace(' — Saison', ' Saison')

            sTitle = sTitle.decode('utf-8')
        except:
            pass

        # recherche l'année, uniquement si entre caractere special a cause de 2001 odysse de l'espace ou k2000
        string = re.search('([^\w ][0-9]{4}[^\w ])', sTitle)
        if string:
            sTitle = sTitle.replace(string.group(0), '')
            self.__Year = str(string.group(0)[1:5])
            self.addItemValues('Year', self.__Year)

        # recherche une date
        string = re.search('([\d]{2}[\/|-]\d{2}[\/|-]\d{4})', sTitle)
        if string:
            sTitle = sTitle.replace(string.group(0), '')
            self.__Date = str(string.group(0))
            sTitle = '%s (%s) ' % (sTitle, self.__Date)

        #~ #recherche Lang
        #~ index = {' vostfr': ' [VOSTFR]', ' vf': ' [VF]', ' truefrench': ' [TrueFrench]'}
        #~ for cle in index:
            #~ sTitle = sTitle.replace(cle.upper(), index[cle]).replace(cle, index[cle]).replace('(%s)' % (cle), index[cle])

        #~ #recherche Qualiter
        #~ index = {'1080i': '(1080)', '1080p': '(1080)', '1080I': '(1080)', '1080P': '(1080)', '720i': '(720)', '720p': '(720)', '720I': '(720)', '720P': '(720)'}
        #~ for cle in index:
            #~ sTitle = sTitle.replace(cle, index[cle]).replace('[%s]' % (cle), index[cle])

        # Recherche saison et episode a faire pr serie uniquement
        if True:
            #m = re.search( ur'(?i)(\wpisode ([0-9\.\-\_]+))', sTitle, re.UNICODE)
            m = re.search('(?i)(?:^|[^a-z])((?:E|(?:\wpisode\s?))([0-9]+(?:[\-\.][0-9\?]+)*))', sTitle, re.UNICODE)
            if m:
                # ok y a des episodes
                sTitle = sTitle.replace(m.group(1), '')
                ep = m.group(2)
                if len(ep) == 1:
                    ep = '0' + ep
                self.__Episode = ep
                self.addItemValues('Episode', self.__Episode)

                # pour les saisons
                m = re.search('(?i)( s(?:aison +)*([0-9]+(?:\-[0-9\?]+)*))', sTitle, re.UNICODE)
                if m:
                    sTitle = sTitle.replace(m.group(1), '')
                    sa = m.group(2)
                    if len(sa) == 1:
                        sa = '0' + sa
                    self.__Season = sa
                    self.addItemValues('Season', self.__Season)

            else:
                # pas d'episode mais y a t il des saisons?
                m = re.search('(?i)( s(?:aison +)*([0-9]+(?:\-[0-9\?]+)*))', sTitle, re.UNICODE)
                if m:
                    sTitle = sTitle.replace(m.group(1), '')
                    sa = m.group(2)
                    if len(sa) == 1:
                        sa = '0' + sa
                    self.__Season = sa
                    self.addItemValues('Season', self.__Season)

        # vire doubles espaces
        sTitle = re.sub(' +', ' ', sTitle)
        # enleve les crochets et les parentheses si elle sont vides
        sTitle = sTitle.replace('()', '').replace('[]', '').replace('- -', '-')

        # vire espace a la fin et les - (attention, il y a 2 tirets differents meme si invisible a l'oeil nu et un est en unicode)
        sTitle = re.sub('[- –]+$', '', sTitle)
        # et au debut
        if sTitle.startswith(' '):
            sTitle = sTitle[1:]

        # recherche les Tags restant : () ou [] sauf tag couleur
        sTitle = re.sub('([\(|\[](?!\/*COLOR)[^\)\(\]\[]+?[\]|\)])', '[COLOR ' + self.__sDecoColor + ']\\1[/COLOR]', sTitle)

        # on reformate SXXEXX Titre [tag] (Annee)
        sTitle2 = ''
        if self.__Season:
            sTitle2 = sTitle2 + 'S' + self.__Season
        if self.__Episode:
            sTitle2 = sTitle2 + 'E' + self.__Episode

        # Titre unique pour pour marquer VU (avec numéro de l'épisode pour les séries)
        self.__sTitleWatched = self.str_conv(sTitle).replace(' ', '')
        if sTitle2:
            self.__sTitleWatched += '_' + sTitle2

        if sTitle2:
            sTitle2 = '[COLOR %s]%s[/COLOR] ' % (self.__sDecoColor, sTitle2)

        sTitle2 = sTitle2 + sTitle

        if self.__Year:
            sTitle2 = '%s [COLOR %s](%s)[/COLOR]' % (sTitle2, self.__sDecoColor, self.__Year)

        # on repasse en utf-8
        return sTitle2.encode('utf-8')

    def getEpisodeTitre(self, sTitle):

        string = re.search('(?i)(e(?:[a-z]+sode\s?)*([0-9]+))', str(sTitle))
        if string:
            sTitle = sTitle.replace(string.group(1), '')
            self.__Episode = ('%02d' % int(string.group(2)))
            sTitle = '%s [COLOR %s]E%s[/COLOR]' % (sTitle, self.__sDecoColor, self.__Episode)
            self.addItemValues('Episode', self.__Episode)
            return sTitle, True

        return sTitle, False

    def setTitle(self, sTitle):
        self.__sCleanTitle = sTitle
        if not sTitle.startswith('[COLOR'):
            self.__sTitle = self.TraiteTitre(sTitle)
        else:
            self.__sTitle = sTitle

    def getTitle(self):
        return self.__sTitle

    def getCleanTitle(self):
        return self.__sCleanTitle

#    def setTitleWatched(self, sTitleWatched):
#        self.__sTitleWatched = sTitleWatched

    def getTitleWatched(self):
        return self.__sTitleWatched

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
        try:
            self.__sIcon = unicode(sIcon, 'utf-8')
        except:
            self.__sIcon = sIcon
        self.__sIcon = self.__sIcon.encode('utf-8')
        self.__sIcon = QuoteSafe(self.__sIcon)

    def getIcon(self):
        #if 'http' in self.__sIcon:
        #    return urllib.unquote_plus(self.__sIcon)
        folder = 'special://home/addons/plugin.video.vstream/resources/art'
        path = '/'.join([folder, self.__sIcon])
        #return os.path.join(unicode(self.__sRootArt, 'utf-8'), self.__sIcon)
        return path

    def addItemValues(self, sItemKey, mItemValue):
        self.__aItemValues[sItemKey] = mItemValue

    def getWatched(self):

        # Fonctionne pour marquer lus un dossier
        if not self.getTitleWatched():
            return 0

        meta = {}
        meta['title'] = self.getTitleWatched()
        meta['site'] = self.getSiteUrl()

        data = self.DB.get_watched(meta)
        return data

    def str_conv(self, data):
        if isinstance(data, str):
            # Must be encoded in UTF-8
            data = data.decode('utf8')

        import unicodedata
        data = unicodedata.normalize('NFKD', data).encode('ascii', 'ignore')
        # cherche la saison et episode puis les balises [color]titre[/color]
        #data, saison = self.getSaisonTitre(data)
        #data, episode = self.getEpisodeTitre(data)
        # supprimer les balises
        data = re.sub(r'\[.*\]|\(.*\)', r'', str(data))
        data = data.replace('VF', '').replace('VOSTFR', '').replace('FR', '')
        #data=re.sub(r'[0-9]+?', r'', str(data))
        data = data.replace('-', ' ')  #on garde un espace pour que Orient-express ne devienne pas Orientexpress pour la recherche tmdb
        data = data.replace('Saison', '').replace('saison', '').replace('Season', '').replace('Episode', '').replace('episode', '')
        data = re.sub('[^%s]' % (string.ascii_lowercase + string.digits), ' ', data.lower())
        #data = urllib.quote_plus(data)

        #data = data.decode('string-escape')
        return data

    def getInfoLabel(self):
        meta = {
        'title': xbmc.getInfoLabel('ListItem.title'),
        #'label': xbmc.getInfoLabel('ListItem.title'),
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

        if 'title' in meta and meta['title']:
            meta['title'] = self.getTitle()

        for key, value in meta.items():
            self.addItemValues(key, value)

        if 'backdrop_url' in meta and meta['backdrop_url']:
            self.addItemProperties('fanart_image', meta['backdrop_url'])
            self.__sFanart = meta['backdrop_url']
        if 'trailer' in meta and meta['trailer']:
            meta['trailer'] = meta['trailer'].replace(u'\u200e', '').replace(u'\u200f', '')
            self.__sTrailerUrl = meta['trailer']
        if 'cover_url' in meta and meta['cover_url']:
            self.__sThumbnail = meta['cover_url']
            self.__sPoster = meta['cover_url']

        return

    def getMetadonne(self):

        sTitle = self.__sFileName

        #sTitle = self.__sTitle.decode('latin-1').encode('utf-8')
        #sTitle = re.sub(r'\[.*\]|\(.*\)', r'', str(self.__sFileName))
        #sTitle = sTitle.replace('VF', '').replace('VOSTFR', '').replace('FR', '')

        #get_meta(self, media_type, name, imdb_id='', tmdb_id='', year='', overlay=6, update=False):
        metaType = self.getMeta()

        # non media -> pas de fanart
        if metaType == 0:
            self.addItemProperties('fanart_image', '')
            return

        # Integrale de films, on nettoie le titre pour la recherche
        if metaType == 3 :
            sTitle=sTitle.replace('integrale', '')
            sTitle=sTitle.replace('2 films', '')
            sTitle=sTitle.replace('6 films', '')
            sTitle=sTitle.replace('7 films', '')
            sTitle=sTitle.replace('trilogie', '')
            sTitle=sTitle.replace('trilogy', '')
            sTitle=sTitle.replace('quadrilogie', '')
            sTitle=sTitle.replace('pentalogie', '')
            sTitle=sTitle.replace('octalogie', '')
            sTitle=sTitle.replace('hexalogie', '')
            sTitle=sTitle.replace('tetralogie', '')

        sType = str(metaType).replace('1', 'movie').replace('2', 'tvshow').replace('3', 'movie')

        if sType:
            from resources.lib.tmdb import cTMDb
            grab = cTMDb()
            args = (sType, sTitle)
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

        # Pour les films
        # if self.getMeta() == 1:
            # try:
                # from metahandler import metahandlers
                # grab = metahandlers.MetaData(preparezip=False, tmdb_api_key=cConfig().getSetting('api_tmdb'))
                # args = ('movie', self.__sFileName)
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
                # args = ('tvshow', self.__sFileName)
                # kwargs = {}
                # if (self.__TmdbId) or (self.__Year):
                    # dict = {}
                    # if (self.__ImdbId):
                        # kwargs['imdb_id'] = self.__ImdbId
                    # if (self.__TmdbId):
                        # kwargs['tmdb_id'] = self.__TmdbId
                    # if (self.__Year):
                        # kwargs['year'] = self.__Year
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
        except:
            pass

        try:
            if meta['tvdb_id']:
                self.__TmdbId = meta['tvdb_id']
        except:
            pass

        # Si fanart trouvé dans les meta alors on l'utilise, sinon on n'en met pas
        if meta['backdrop_url']:
            self.addItemProperties('fanart_image', meta['backdrop_url'])
            self.__sFanart = meta['backdrop_url']
        else:
            self.addItemProperties('fanart_image', '')

        # if meta['trailer_url']:
            # meta['trailer'] = meta['trailer'].replace(u'\u200e', '').replace(u'\u200f', '')
            # self.__sTrailerUrl = meta['trailer']

        # Pas de changement de cover pour les coffrets de films
        if metaType != 3:
            if 'cover_url' in meta and meta['cover_url']:
                self.__sThumbnail = meta['cover_url']
                self.__sPoster = meta['cover_url']
        return

    def getItemValues(self):
        self.__aItemValues['Title'] = self.getTitle()
        self.__aItemValues['Plot'] = self.getDescription()

        #tmdbid
        if self.getTmdbId():
            self.addItemProperties('TmdbId', str(self.getTmdbId()))

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

        #Used only if there is data in db, overwrite getMetadonne()
        w = self.getWatched()
        if w == 1:
            self.addItemValues('playcount', w)

        return self.__aItemValues

    def addItemProperties(self, sPropertyKey, mPropertyValue):
        self.__aProperties[sPropertyKey] = mPropertyValue

    def getItemProperties(self):
        return self.__aProperties

    def addContextItem(self, oContextElement):
        self.__aContextElements.append(oContextElement)

    def getContextItems(self):
        return self.__aContextElements
