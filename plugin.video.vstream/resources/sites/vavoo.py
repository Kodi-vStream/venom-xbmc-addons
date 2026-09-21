# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
#https://archive.org/details/logos_fr_tv
import re
import json
import string
import requests
import uuid
import time
from datetime import datetime
from resources.lib.comaddon import siteManager
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.util import cUtil
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.player import cPlayer
from resources.lib.comaddon import addon
from resources.lib.comaddon import VSlog


SITE_IDENTIFIER = 'vavoo'
SITE_NAME = 'Vavoo TV'
SITE_DESC = 'Chaines TV de vavoo'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_SEARCH = ('http://vavoo-search/%s', 'showLiveTV')
URL_CATALOG = URL_MAIN + 'mediahubmx-catalog.json'

SPORT_SPORTS = ('sport', 'showGenresTV')
SPORT_TV = ('sport', 'showGenresTV')
DOC_TV = ('doc', 'showGenresTV')

KID_KIDS = ('kid', 'showGenresTV')
KID_TV = ('kid', 'showGenresTV')

TV_TV = (URL_MAIN, 'showMenuLiveTV')
CHAINE_TV = (URL_MAIN, 'showMenuLiveTV')

PING_URLS = [
    "https://www.vypn.net/api/app/ping",
    "https://cache.vypn.net/api/app/ping",
]

BROWSER_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/124.0.0.0 Safari/537.36")

_headers = {
    "accept": "*/*",
    "user-agent": BROWSER_UA,
    "Accept-Encoding": "gzip, deflate",
    "Connection": "close"
}

def _build_payload():
    uid = str(uuid.uuid4())
    ts  = int(time.time() * 1000)
    return {
        "reason": "app-focus", "locale": "en", "theme": "dark",
        "metadata": {
            "device":  {"type": "desktop", "uniqueId": uid},
            "os":      {"name": "win32", "version": "Windows 10 Pro",
                        "abis": ["x64"], "host": "Lenovo"},
            "app":     {"platform": "electron"},
            "version": {"package": "net.vypn.app", "binary": "3.1.0", "js": "3.1.0"},
        },
        "appFocusTime": 0, "playerActive": False, "playDuration": 0,
        "devMode": False, "hasAddon": True, "castConnected": False,
        "package": "net.vypn.app", "version": "3.1.0", "process": "app",
        "firstAppStart": ts, "lastAppStart": ts, "ipLocation": None,
        "adblockEnabled": True,
        "proxy": {"supported": ["ss"], "engine": "Mu", "enabled": False, "autoServer": True},
        "iap": {"supported": False},
    }

def getAuthSignature():
    for url in PING_URLS:
        for attempt in range(3):
            try:
                resp = requests.post(url, json=_build_payload(), headers=_headers, timeout=15, verify=False)
                if resp.status_code == 200:
                    req = resp.json()
                    sig = (req.get("sig") or req.get("addonSig") or req.get("signature") or
                           req.get("mediahubmxSignature") or req.get("mediahubmx-signature") or
                           req.get("token") or "")
                    if sig:
                        return sig
            except Exception:
                pass
    return ""


def load():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30076), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_CATALOG)
    oGui.addDir(SITE_IDENTIFIER, 'showAlpha', 'Chaines (A-Z)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'sport')
    oGui.addDir(SITE_IDENTIFIER, 'showGenresTV', 'Chaines (Sports)', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'doc')
    oGui.addDir(SITE_IDENTIFIER, 'showGenresTV', 'Chaines (Doc / Reportage)', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'kid')
    oGui.addDir(SITE_IDENTIFIER, 'showGenresTV', 'Chaines (Jeunesse)', 'enfants.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_CATALOG)
    oGui.addDir(SITE_IDENTIFIER, 'showCountries', 'Chaines (Par pays)', 'host.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuLiveTV():
    oGui = cGui()
    addons = addon()

    oOutputParameterHandler = cOutputParameterHandler()
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', addons.VSlang(30076), 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_CATALOG)
    oGui.addDir(SITE_IDENTIFIER, 'showAlpha', 'Chaines (A-Z)', 'az.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', URL_CATALOG)
    oGui.addDir(SITE_IDENTIFIER, 'showCountries', 'Chaines (Par pays)', 'host.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        oUtil = cUtil()
        sSearchCleaned = oUtil.CleanName(sSearchText)
        showLiveTV(sSearchCleaned)


def showGenresTV():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    
    if 'sport' in sUrl:
        chaines = [
            ('LIGUE 1', 'https://www.lequipe.fr/_medias/img-photo-jpg/ligue-1-quelle-offre-d-abonnement-est-faite-pour-vous/1500000002258913/24:0,1176:768-828-552-75/dc2b0.jpg'),
            ('DAZN', 'https://www.leparisien.fr/resizer/8FSAVEdo2q647CsIBSewbUcPFzs=/932x582/cloudfront-eu-central-1.images.arcpublishing.com/lpguideshopping/3JMT5WW2B5AKREOR43CLU36ZK4.jpg'),
            ('CANAL +!', 'https://archive.org/download/logostvfr/canal-plus.png'),
            ('CANAL + FOOT', 'https://upload.wikimedia.org/wikipedia/commons/e/eb/Canal%2BFoot.png'),
            ('FOOT +', 'https://i.imgur.com/qsLLyn4.png'),
            ('CANAL + LIVE', 'https://thumb.canalplus.pro/bran/unsafe/384x/filters:quality(%7BimageQualityPercentage%7D)/image/66e020a7dbc19/uploads/media/CANALPENLIVE_FOND_NOIR.png'),
            ('CANAL + SPORT', 'https://i.imgur.com/EOXnU15.png'),
            ('CANAL + MOTO GP', 'https://i.imgur.com/CnJE2M0.png'),
            ('CANAL + TOP 14', 'https://archive.org/download/logostvfr/canal-plus-top-14-rugby.png'),
            ('EUROSPORT', 'https://i.imgur.com/s4jDnJh.png'),
            ('BEIN SPORTS', 'https://i.imgur.com/RLrMBlm.png'),
            ('ELEVEN', 'https://i.imgur.com/AOu4FXH.png'),
            ('AMAZON PRIME', 'https://archive.org/download/logostvfr/amazon-prime-1-hd.png'),
            ('RMC SPORT', 'https://play-lh.googleusercontent.com/q5ySKSzFqWTVr9kQQXI0F8aWe_F9tDmDyHHIsw-736EmCYN7RiLBgviytOyBAXhJ5lA'),
            ('AUTO MOTO', 'https://dn711502.ca.archive.org/0/items/logostvfr/automoto-la-chaine.png'),
            ('GOLF', 'https://i.imgur.com/WHnddkg.png'),
            ('INFOSPORT', 'https://thumb.canalplus.pro/bran/unsafe/1920x/filters:quality(%7BimageQualityPercentage%7D)/image/698c914948189/uploads/media/INFOSPORT.png'),
#            ('KOMBAT SPORT', 'https://archive.org/download/logostvfr/infosport.png'),
            ('EQUIPE', 'https://i.imgur.com/t35zhM9.png'),
            ('EQUIDIA', 'https://i.imgur.com/QPpbRcZ.png')
        ]
    elif 'doc' in sUrl:               # Documentaires
        chaines = [
            ('ANIMAUX', 'https://i.imgur.com/FM9FVAG.png'),
            ('ARTE', 'https://archive.org/download/logostvfr/arte.png'),
            ('CANAL+ DOCS', 'https://archive.org/download/logostvfr/canal-plus-docs.png'),
            ('CHASSE & PECHE', 'https://archive.org/download/logostvfr/chasse-et-peche.png'),
            ('CRIME DISTRICT', 'https://archive.org/download/logostvfr/crime-district.png'),
            ('DISCOVERY', 'https://archive.org/download/logostvfr/discovery-hd.png'),
            ('FRANCE 5', 'https://archive.org/download/logostvfr/france-5.png'),
            ('HISTOIRE', 'https://i.imgur.com/hxuJXll.png'),
            ('NAT GEO', 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Natgeologo.svg/960px-Natgeologo.svg.png'),
            ('NATURE TIME', 'https://naturetimetv.com/wp-content/uploads/2023/05/NatureTime_white_Primary.png'),
            ('PLANETE', 'https://i.imgur.com/RMbMGMg.png'),
            ('RMC DECOUVERTE', 'https://archive.org/download/logostvfr/rmc-decouverte.png'),
            ('RMC STORY', 'https://archive.org/download/logostvfr/rmc-story.png'),
            ('SCIENCE & VIE', 'https://i.imgur.com/9ELsSMI.png'),
            ('TREK', 'https://archive.org/download/logostvfr/trek.png'),
            ('USHUAIA', 'https://i.imgur.com/WjjlqbP.png'),
        ]
    else:               # Jeunesse
        chaines = [
            ('BABY TV', 'https://archive.org/download/logostvfr/baby-tv-fhd.png'),
            ('BOING', 'https://archive.org/download/logostvfr/boing.png'),
            ('BOOMERANG', 'https://archive.org/download/logostvfr/boomerang.png'),
            ('CANAL + KIDS', 'https://archive.org/download/logostvfr/canal-plus-kids.png'),
            ('CANAL J', 'https://archive.org/download/logostvfr/canal-j.png'),
            ('CARTOON NETWORK', 'https://archive.org/download/logostvfr/cartoon-network.png'),
            ('CINE+ FAMIZ', 'https://archive.org/download/logostvfr/cine-plus-family.png'),
            ('DISNEY', 'https://upload.wikimedia.org/wikipedia/commons/2/22/Official_Disney.com_Logo.jpg'),
            ('GAME ONE', 'https://archive.org/download/logostvfr/game-one.png'),
            ('GONG', 'https://upload.wikimedia.org/wikipedia/commons/d/d7/GONG.png'),
            ('GULLI', 'https://archive.org/download/logostvfr/gulli.png'),
            ('J ONE', 'https://archive.org/download/logostvfr/j-one.png'),
            ('NICK', 'https://archive.org/download/logostvfr/nickelodeon.png'),
            ('PIWI', 'https://archive.org/download/logostvfr/piwi-plus.png'),
            ('TELETOON', 'https://archive.org/download/logostvfr/teletoon-plus.png'),
            ('TIJI', 'https://archive.org/download/logostvfr/tiji.png'),
            ('TOONAMI', 'https://images.seeklogo.com/logo-png/62/1/toonami-logo-png_seeklogo-629720.png'),
        ]

    oOutputParameterHandler = cOutputParameterHandler()
    for sTitle, sThumb in chaines:
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        sDisplayTitle = sTitle.replace('!', '')
        oGui.addLink(SITE_IDENTIFIER, 'showLiveTV', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showCountries():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    liste = [
        ['Arabia', 'sa'],
        ['Bulgaria', 'bg'],
        ['Croatia', 'hr'],
        ['France', 'fr'],
        ['Germany', 'de'],
        ['Italy', 'it'],
        ['Netherlands', 'nl'],
        ['Poland', 'pl'],
        ['Portugal', 'pt'],
        ['Romania', 'ro'],
        ['Russia', 'ru'],
        ['Spain', 'es'],
        ['Turkey', 'tr'],
        ['United Kingdom', 'gb'],
    ]

    for sTitle, sGroup in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('group', sTitle)
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        sIcon = 'https://flagcdn.com/w320/%s.png' % sGroup
        oGui.addLink(SITE_IDENTIFIER, 'showLiveTV', sTitle, sIcon, sTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAlpha():
    oGui = cGui()
    sUrl = "https://vavoo.to/mediahubmx-catalog.json"
    for alpha in string.ascii_uppercase:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', alpha)
        oGui.addDir(SITE_IDENTIFIER, 'showSearchAlpha', 'Lettre [COLOR coral]%s[/COLOR]' % alpha, 'listes.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()


def getLogo(chan_name, group="france"):
    if not chan_name:
        return ""

    # 1. Nettoyage initial du nom
    clean = cUtil().formatUTF8(chan_name).lower()
    clean = re.sub(r'\.[a-z0-9]+\s*$', '', clean)
    clean = clean.replace('+', ' plus ')
    clean = re.sub(r'\b(hevc|rraw|backup|1080p|720p|fr|de|be|sd)\b', '', clean)
    clean = re.sub(r'\s+', ' ', clean).strip()
    
    # Detection du pays selon le groupe (France ou Germany)
    group_lower = str(group).lower()
    if 'germany' in group_lower or 'deutschland' in group_lower or 'allemagne' in group_lower:
        c_folder = "germany"
        c_suffix = "de"
    else:
        c_folder = "france"
        c_suffix = "fr"

    # URL Archive sans le c_folder
    mino_url = "https://archive.org/download/logostvfr/"
    base_url = "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/%s/" % c_folder 

    if c_folder == "germany":
        icons_map = {}
    else:
        icons_map = {
            "ab 1": "ab1",
            "ab1": "ab1",
            "ab 3": "ab3",
            "ab3": "ab3",
            "bfm tv": "bfm-tv",
            "bfm 1": "bfm-tv",
            "bfm hd": "bfm-tv",
            "bein sports 1": "bein-sports-1-french",
            "bein sport 1": "bein-sports-1-french",
            "bein sports 2": "bein-sports-2-french",
            "bein sport 2": "bein-sports-2-french",
            "bein sports 3": "bein-sports-3-french",
            "bein sport 3": "bein-sports-3-french",
            "bein sports": "bein-sports",
            "canal plus box office": "canal-plus-box-office",
            "canal plus docs": "canal-plus-docs",
            "canal plus foot": "canal-plus-foot",
            "canal plus formula": "canal-plus-formula1",
            "canal plus grand ecran": "canal-plus-grand-ecran",
            "cnews prime": "c-news-prime",
            "cnews": "c-news",
            "cstar": "c-star",
            "cine plus famiz": "cine-plus-family",
            "cine famiz": "cine-plus-family",            
            "cine emotion": "cine-plus-emotion",
            "cina plus classic": "cine-plus-classic",
            "cine classic": "cine-plus-classic",
            "cine frisson": "cine-plus-frisson",            
            "automoto": "automoto-la-chaine",
            "b smart": "b-smart",
            "canal j": "canal-j",
            "tf1 series films": "tf1-series-films",
            "tf1 series & film": "tf1-series-films",
            "ligue1 plus 10": "ligue-1plus-10",
            "ligue 1 plus 2": "ligue-1plus-2",
            "ligue1 plus 2": "ligue-1plus-2",
            "ligue 1 plus 3": "ligue-1plus-3",
            "ligue1 plus 3": "ligue-1plus-3",
            "ligue 1 plus 4": "ligue-1plus-4",
            "ligue1 plus 4": "ligue-1plus-4",
            "ligue 1 plus 5": "ligue-1plus-5",
            "ligue1 plus 5": "ligue-1plus-5",
            "ligue 1 plus 6": "ligue-1plus-6",
            "ligue1 plus 6": "ligue-1plus-6",
            "ligue 1 plus 7": "ligue-1plus-7",
            "ligue1 plus 7": "ligue-1plus-7",
            "ligue 1 plus 8": "ligue-1plus-8",
            "ligue1 plus 8": "ligue-1plus-8",
            "ligue 1 plus 9": "ligue-1plus-9",
            "ligue1 plus 9": "ligue-1plus-9",
            "ligue 1 plus": "ligue-1plus",
            "ligue1 plus": "ligue-1plus",
             "rtl 9": "rtl9",
             "rtl9": "rtl9"            
        }

    for key, filename in icons_map.items():
        if key in clean:
            return '%s%s-%s.png' % (base_url, filename, c_suffix)

    normalized = re.sub(r'[^a-z0-9]+', '-', clean).strip('-')
    if not normalized:
        return ""

    if any(k in clean for k in ["20", "6ter", "13 eme", "13eme", "ab moteurs", "animaux", "amazon", "action", "arte", "auto", "baby", "bet", "bfm", "boomerang", "boing", "box", "boxoffice", "c", "canal", "canal hd", "canal fhd", "canal decal hd", "cine", "dazn", "eleven", "elevensport", "euronews", "eurosport", "france", "ocs", "multisports", "kombat", "nat", "novelas", "nrj", "m6", "mangas", "mcm", "mdl", "mezzo", "mtv", "melody", "planet", "planete", "polar", "rmc", "tf1", "w9"]):
        return "%s%s.png" % (mino_url, normalized)
    
    return '%s%s-%s.png' % (base_url, normalized, c_suffix)


def showSearchAlpha():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    alpha = oInputParameterHandler.getValue('sMovieTitle')
    
    payload = {
        "language": "fr",
        "region": "FR",
        "catalogId": "iptv",
        "id": "",
        "adult": False,
        "search": alpha,
        "sort": "name",
        "filter": {"group": "France"},
        "cursor": None
    }

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'MediaHubMX/2'
    }

    try:
        r = requests.post(sUrl, data=json.dumps(payload), headers=headers, timeout=10, verify=False)
        data = r.json()
        items = data['items']

        # récupération de toutes les chaines !
        cursor = data.get('nextCursor', 0)
        if cursor > 0:
            payload = {
                "language": "fr",
                "region": "FR",
                "catalogId": "iptv",
                "id": "",
                "adult": False,
                "search": alpha,
                "sort": "name",
                "filter": {"group": "France"},
                "cursor": cursor
            }
            r = requests.post(sUrl, data=json.dumps(payload), headers=headers, timeout=10, verify=False)
            data2 = r.json()
            items += data2['items']

        trouve = False
        for item in items:
            sTitle = item.get('name', '_Sans titre_')

            if not sTitle.startswith(alpha):
                if trouve:
                    break
                continue

            if 'A LA CARTE' in sTitle or 'CANAL PLAY' in sTitle or 'CANALPLAY' in sTitle:
                continue

            trouve = True
            
            sTitle = sTitle.split(' .')[0]
            sIcon = item.get('logo', '')
            sUrlPlay = item.get('url', '')

            try:
                custom_icon = getLogo(sTitle)
                if custom_icon:
                    sIcon = custom_icon + "?reload=1"
            except:
                pass

            if sUrlPlay:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrlPlay)
                oGui.addMisc(SITE_IDENTIFIER, 'playLiveTV', sTitle, sIcon, sIcon, '', oOutputParameterHandler)

    except Exception:
        pass

    oGui.setEndOfDirectory()
    
    
def showLiveTV(sSearch = ''):    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    sSearchTitle = False
    if sSearch:
        sUrl = URL_SEARCH[0]
    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sSearch = oInputParameterHandler.getValue('sMovieTitle')
        if sSearch:
            sSearch = sSearch.replace('&', '')
            if '!' in sSearch:
                sSearchTitle = True
                sSearch = sSearch.replace('!', '')
        else:
            sSearch = ''

    sCursor = oInputParameterHandler.getValue('cursor')
    sGroup = oInputParameterHandler.getValue('group')

    # Récupération propre du groupe
    if sGroup and str(sGroup) not in ['False', 'None', '']:
        active_group = str(sGroup)
    else:
        active_group = "France"

    if active_group.upper() in ['ALL', 'ALL COUNTRIES', 'FALSE', 'NONE', '']:
        filter_val = {}
    else:
        filter_val = {"group": active_group}

    payload = {
        "language": "fr",
        "region": "FR",
        "catalogId": "iptv",
        "id": "",
        "adult": False,
        "search": sSearch,
        "sort": 'name',
        "filter": filter_val,
        "cursor": sCursor if (sCursor and sCursor != False and sCursor != 'None') else None,
        "clientVersion": "3.1.0"
    }

    target_url = "https://vavoo.to/mediahubmx-catalog.json"
    
    try:
        session = requests.Session()
        headers = {
            "User-Agent": "MediaHubMX/2",
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "Accept-Encoding": "gzip",
            "mediahubmx-signature": getAuthSignature()
        }
        
        response = session.post(
            target_url,
            json=payload,
            headers=headers,
            allow_redirects=True,
            timeout=10,
            verify=False
        )
        
        if response.status_code != 200:
            VSlog('[VAVOO] Erreur HTTP ' % response.status_code)
            oGui.setEndOfDirectory()
            return

        data = response.json()

    except Exception as e:
        VSlog('[VAVOO] Erreur : '+ str(e))
        oGui.setEndOfDirectory()
        return

    if data and 'items' in data:
        try:
            start_index = int(sCursor) + 1 if (sCursor and str(sCursor).isdigit()) else 1
        except:
            start_index = 1

        channels = data['items']
        
        for idx, item in enumerate(channels, start=start_index):
            sUrlPlay = item.get('url', '')
            if not sUrlPlay:
                continue

            raw_title = item.get('name', 'Sans titre').split(' .')[0]
            if 'A LA CARTE' in raw_title or 'CANAL PLAY' in raw_title or 'CANALPLAY' in raw_title:
                continue
            
            if sSearchTitle:
                titleToSearch = raw_title.replace(' SD', '').replace(' HD', '').replace(' FHD', '').replace(' 4K', '').replace(' ULTRA', '').replace('360', '').replace(' ', '')
                if (sSearch != raw_title) and titleToSearch not in sSearch.replace(' ', ''):
                    continue

            sTitle = raw_title
            sIcon = item.get('logo', '')
            
            # --- EPG & BARRE DE PROGRESSION ---
            sDesc = ""
            epg_data = item.get('epg')
            
            if epg_data and isinstance(epg_data, list) and len(epg_data) > 0:
                try:
                    curr = epg_data[0]
                    now_title = curr.get('name') or curr.get('title') or ''
                    if now_title and 'No Data' not in now_title:
                        start_ts = curr.get('start') or curr.get('startTime') or curr.get('time')
                        end_ts = curr.get('stop') or curr.get('endTime') or curr.get('end')
                        prog_desc = curr.get('description') or curr.get('overview') or ''
                        sDesc += '[COLOR darkgray]En cours :[/COLOR][CR][B]%s[/B]\n' % now_title
                        if start_ts:
                            try:
                                s_time = float(start_ts)
                                if s_time > 10000000000:
                                    s_time /= 1000.0
                                if end_ts:
                                    e_time = float(end_ts)
                                    if e_time > 10000000000:
                                        e_time /= 1000.0
                                else:
                                    e_time = s_time + 3600
                                    
                                now_time = time.time()
                                if e_time > s_time:
                                    total_duration = e_time - s_time
                                    elapsed = now_time - s_time
                                    percent = int((elapsed / total_duration) * 100)
                                    percent = max(0, min(100, percent))
                                    filled = int(10 * percent / 100)
                                    
                                    bar_rouge = '▬' * filled
                                    bar_grise = '▬' * (10 - filled)
                                    
                                    start_str = datetime.fromtimestamp(s_time).strftime('%H:%M')
                                    end_str = datetime.fromtimestamp(e_time).strftime('%H:%M')
                                    remaining_min = max(0, int((e_time - now_time) / 60))
                                    
                                    sDesc += '[COLOR red]%s[/COLOR][COLOR darkgray]%s[/COLOR] [COLOR red]%s%%[/COLOR] [COLOR white][CR](%s - %s | Reste %s min)[/COLOR]\n' % (bar_rouge, bar_grise, percent, start_str, end_str, remaining_min)
                            except Exception:
                                pass
                                
                    if prog_desc:
                        sDesc += '[COLOR white]%s[/COLOR]\n' % prog_desc[:300]
                
                    if len(epg_data) > 1:
                        next_item = epg_data[1]
                        next_title = next_item.get('name') or next_item.get('title') or ''
                        if next_title and 'No Data' not in next_title:
                            next_start = next_item.get('start') or next_item.get('startTime') or next_item.get('time')
                            next_time_str = ""
                            if next_start:
                                try:
                                    ns_time = float(next_start)
                                    if ns_time > 10000000000:
                                        ns_time /= 1000.0
                                    next_time_str = datetime.fromtimestamp(ns_time).strftime('%H:%M')
                                except Exception:
                                    pass
                            sDesc += '[CR][COLOR grey]A suivre à %s :[/COLOR][CR]%s' % (next_time_str, next_title)
                except Exception:
                    pass
            
            if not sDesc:
                sDesc = item.get('description', 'Aucun programme disponible')

            try:
                custom_icon = getLogo(raw_title, active_group)
                if custom_icon:
                    sIcon = custom_icon + "?reload=1"
            except:
                pass
            
            if sUrlPlay:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrlPlay)
                oOutputParameterHandler.addParameter('sMovieTitle', raw_title)
                oGui.addMisc(SITE_IDENTIFIER, 'playLiveTV', sTitle, sIcon, sIcon, sDesc, oOutputParameterHandler)

        if not sCursor:
            next_cursor = data.get('nextCursor', 0)
            if next_cursor and int(next_cursor) > 0:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('group', '' if sSearch else active_group)
                oOutputParameterHandler.addParameter('cursor', str(next_cursor))
                oGui.addNext(SITE_IDENTIFIER, 'showLiveTV', 'Suite', oOutputParameterHandler)
            
    oGui.setEndOfDirectory()

            
def playLiveTV():    
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    
    try:
        signature = getAuthSignature()
    except Exception:
        signature = ""

    headers = {
        "user-agent": "MediaHubMX/2",
        "accent": "application/json",
        "content-type": "application/json; charset=utf-8",
        "accept-encoding": "gzip",
        "mediahubmx-signature": signature,
        "Origin": "https://vavoo.to",
        "Referer": "https://vavoo.to/"
    }
    
    payload = {
        "language": "fr",
        "region": "FR",
        "url": sUrl,
        "clientVersion": "3.1.0"
    }
    
    target_url = "https://vavoo.to/mediahubmx-resolve.json"
    
    try:
        session = requests.Session()
        response = session.post(
            target_url, 
            json=payload, 
            headers=headers, 
            timeout=10, 
            verify=False
        )
        
        if response.status_code == 200:
            data = response.json()
            stream_url = ""

            if isinstance(data, list) and len(data) > 0:
                stream_url = data[0].get("url", "")
            elif isinstance(data, dict):
                stream_url = data.get("url", "")
                
            if stream_url:
                playable_url = stream_url + "|User-Agent=MediaHubMX/2"

                oGuiElement = cGuiElement()
                oGuiElement.setSiteName("VavooLive")
                oGuiElement.setTitle(sTitle if sTitle else "Live TV")
                oGuiElement.setMediaUrl(playable_url)
                if sThumb:
                    oGuiElement.setIcon(sThumb)

                oPlayer = cPlayer()
                oPlayer.clearPlayList()
                oPlayer.addItemToPlaylist(oGuiElement)
                
                oPlayer.startPlayer()
                return

    except Exception:
        pass
        
    oGui.setEndOfDirectory()
