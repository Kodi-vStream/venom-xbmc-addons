# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import time
import datetime

from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler


SITE_IDENTIFIER = 'livewatch'
SITE_NAME = 'LiveWatch'
SITE_DESC = 'Chaines TV en direct'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_API = siteManager().getDefaultProperty(SITE_IDENTIFIER, 'url_api')

SPORT_SPORTS = ('sport', 'showGenresTV')
SPORT_GENRES = ('/api/sports', 'showGenres')
#SPORT_LIVE = ('json.php', 'showMovies')
SPORT_TV = ('sport', 'showGenresTV')
DOC_TV = ('doc', 'showGenresTV')

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'


# logo de chaines "imgur" trouvé sur https://iptv-org.github.io/
channelsSport = [
    ('LIGUE 1', 'https://www.lequipe.fr/_medias/img-photo-jpg/ligue-1-quelle-offre-d-abonnement-est-faite-pour-vous/1500000002258913/24:0,1176:768-828-552-75/dc2b0.jpg'),
    ('DAZN', 'https://www.leparisien.fr/resizer/8FSAVEdo2q647CsIBSewbUcPFzs=/932x582/cloudfront-eu-central-1.images.arcpublishing.com/lpguideshopping/3JMT5WW2B5AKREOR43CLU36ZK4.jpg'),
    ('BEIN SPORTS', 'https://i.imgur.com/RLrMBlm.png'),
    ('CANAL+!', 'https://i.imgur.com/5HcyMnW.png'),
    ('CANAL+ FOOT', 'https://upload.wikimedia.org/wikipedia/commons/e/eb/Canal%2BFoot.png'),
    ('FOOT+', 'https://i.imgur.com/qsLLyn4.png'),
    ('CANAL+ LIVE', 'https://thumb.canalplus.pro/bran/unsafe/384x/filters:quality(%7BimageQualityPercentage%7D)/image/66e020a7dbc19/uploads/media/CANALPENLIVE_FOND_NOIR.png'),
    ('CANAL+ SPORT', 'https://i.imgur.com/EOXnU15.png'),
    ('CANAL+ MOTO GP', 'https://i.imgur.com/CnJE2M0.png'),
#    'CANAL+ CHAMPIONS',
#    'CANAL+ PREMIER LEAGUE',
    ('EUROSPORT', 'https://i.imgur.com/s4jDnJh.png'),
    ('ELEVENSPORT', 'https://i.imgur.com/AOu4FXH.png'),
    ('AMAZON PRIME', 'https://actuneuf.com/sites/actuneuf.com/files/logo-prime-video_0.png'),
    ('RMC SPORT', 'https://play-lh.googleusercontent.com/q5ySKSzFqWTVr9kQQXI0F8aWe_F9tDmDyHHIsw-736EmCYN7RiLBgviytOyBAXhJ5lA'),
    ('AUTOMOTO', 'https://i.imgur.com/ebf2uc7.png'),
    ('GOLF', 'https://i.imgur.com/WHnddkg.png'),
    ('EQUIPE', 'https://i.imgur.com/t35zhM9.png'),
    ('EQUIDIA', 'https://i.imgur.com/QPpbRcZ.png')
]

channelsDoc = [
    ('ANIMAUX', 'https://i.imgur.com/FM9FVAG.png'),
    ('DISCOVERY', 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/2019_Discovery_logo.svg/960px-2019_Discovery_logo.svg.png'),
    ('HISTOIRE', 'https://i.imgur.com/hxuJXll.png'),
    ('NATIONAL GEO', 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Natgeologo.svg/960px-Natgeologo.svg.png'),
    ('PLANETE', 'https://i.imgur.com/RMbMGMg.png'),
    ('SCIENCE & VIE', 'https://i.imgur.com/9ELsSMI.png'),
    ('USHUAIA', 'https://i.imgur.com/WjjlqbP.png')
]


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_TV[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_TV[1], 'Chaines sportives', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_TV[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_TV[1], 'Chaines documentaires', 'doc.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    # oGui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'Par genres', 'genre_sport.png', oOutputParameterHandler)
    #
    # oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    # oGui.addDir(SITE_IDENTIFIER, SPORT_LIVE[1], 'En cours', 'replay.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()
    oRequestHandler = cRequestHandler(URL_API + 'sports')
    links = oRequestHandler.request(jsonDecode=True)
    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle in sorted(links['sports']):
        sDisplayTitle = sTitle.capitalize().replace('-', ' ')
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showSports', sDisplayTitle, 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenresTV():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    if 'sport' in sUrl:
        chaines = channelsSport
    else:
        chaines = channelsDoc

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sThumb in chaines:
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        sDisplayTitle = sTitle.replace('!', '')
        oGui.addLink(SITE_IDENTIFIER, 'showTV', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def channelSort(channel):
    name = channel['name']
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r'(\d+)', name)
    ]


def showTV():
    oGui = cGui()
    oRequestHandler = cRequestHandler(URL_API + 'channels?country=France') # &limit=0&category=Sport
    links = oRequestHandler.request(jsonDecode=True)

    oInputParameterHandler = cInputParameterHandler()
    sGenreTitle = oInputParameterHandler.getValue('sMovieTitle').replace(' ', '')

    #epgs = {}

    oOutputParameterHandler = cOutputParameterHandler()
    for channel in sorted(links['channels'], key=channelSort):
        sTitle = channel['name']
        
        if ('!' in sGenreTitle and sGenreTitle.replace('!', '') == sTitle) or sGenreTitle in sTitle.replace(' ', ''):
            
            if 'PPV' in sTitle:
                continue
            
            sDesc = sTitle
            # EPG
#             sDesc = epgs.get(sTitle)
#             if not sDesc:
#                 sDesc = sTitle
#                 urlEpg = '%sepg/now?name=%s' % (URL_API, sTitle.replace(' ', '%20'))
#                 oRequestHandler = cRequestHandler(urlEpg)
#                 oRequestHandler.addHeaderEntry('Referer', URL_MAIN)
#                 programme = oRequestHandler.request(jsonDecode=True)
#                 if programme:
#                     current = programme.get('current', None)
#                     if current:
#                         # Parse avec timezone
#                         dt = datetime.datetime(*(time.strptime(current['start_iso'][:19], '%Y-%m-%dT%H:%M:%S')[0:6]))
#                         # Conversion
#                         sDate = dt.strftime("%d/%m %H:%M")
#                         sDesc = '%s - %s' % (current.get('title', ''), current.get('desc', ''))
#                         sDesc = ('%s - %s') % (sDate, sDesc)
#                 epgs[sTitle] = sDesc
            
            sDisplayTitle = sTitle
            source = channel.get('source', '')
            quality = channel.get('quality', '')
            sDisplayTitle += ' [%s %s]' % (source.capitalize() if source else '', quality if quality else '')
            
            sHostUrl = 'stream/' + channel['id']
            sThumb = channel['logo']
            oOutputParameterHandler.addParameter('siteUrl', sHostUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHoster', sDisplayTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSports():
    oGui = cGui()
    oRequestHandler = cRequestHandler(URL_API + 'sports')
    links = oRequestHandler.request(jsonDecode=True)

    oInputParameterHandler = cInputParameterHandler()
    sGenreTitle = oInputParameterHandler.getValue('sMovieTitle')

    oOutputParameterHandler = cOutputParameterHandler()
    for sports in links['events']:
        sSportGenre = sports['sport']
        if sSportGenre != sGenreTitle:
            continue

        sTitle = sports['title']
        sTitleID = sports['id']
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('siteUrl', sTitleID)
        oGui.addDir(SITE_IDENTIFIER, 'showLinks', sTitle, 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLinks():
    oGui = cGui()
    oRequestHandler = cRequestHandler(URL_API + 'sports')
    links = oRequestHandler.request(jsonDecode=True)

    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sTitleId = oInputParameterHandler.getValue('siteUrl')

    oOutputParameterHandler = cOutputParameterHandler()
    for sports in links['events']:
        sportId = sports['id']
        if sTitleId != sportId:
            continue
        
        for source in sports['sources']:
            sourceName = source['source']
            hostId = source['id']
            sHostUrl = 'action=streams&id=%s&source=%s' % (hostId, sourceName)
            oOutputParameterHandler.addParameter('siteUrl', sHostUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            sDisplayTitle = '%s [%s]' % (sTitle, sourceName)
            oGui.addLink(SITE_IDENTIFIER, 'showLink', sDisplayTitle, 'sport.png', sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    siteUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(URL_API + 'sports?' + siteUrl)
    links = oRequestHandler.request(jsonDecode=True)

    oOutputParameterHandler = cOutputParameterHandler()
    for link in links:
        lang = link['language']
        isHD = link['hd']
        sHostUrl = link['embedUrl']

        oOutputParameterHandler.addParameter('siteUrl', sHostUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        sDisplayTitle = '%s [%s] (%s)' % (sTitle, 'HD' if isHD else '', lang)
        oGui.addLink(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'sport.png', sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHoster():
    oGui = cGui()
    oHosterGui = cHosterGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    
    sUrl = URL_API + sUrl
    oRequestHandler = cRequestHandler(sUrl)
    links = oRequestHandler.request(jsonDecode=True)
    if 'proxy_url' in links:
        sHosterUrl = URL_MAIN[:-1] + links['proxy_url']
        oHoster = oHosterGui.getHoster('lien_direct')
        if oHoster:
            sDisplayTitle = sMovieTitle
            oHoster.setDisplayName(sDisplayTitle)
            oHoster.setFileName(sMovieTitle)
            oHoster.setMediaInfo(sDesc)
            oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
