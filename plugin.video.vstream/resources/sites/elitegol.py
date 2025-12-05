# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re
import datetime

from resources.lib.packer import cPacker
from resources.lib.comaddon import isMatrix, siteManager, VSlog
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler


SITE_IDENTIFIER = 'elitegol'
SITE_NAME = 'Elitegol'
SITE_DESC = 'Chaines TV en directs'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
URL_LINK = siteManager().getDefaultProperty(SITE_IDENTIFIER, 'url_link')


SPORT_SPORTS = (True, 'load')
#SPORT_GENRES = ('json.php', 'showGenres')  # FOOT
#SPORT_LIVE = ('json.php', 'showMovies')
SPORT_TV = ('lecteur/', 'showTV')

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'

# chaines dans l'ordre d'affichage
channels = {
    20: ['Ligue 1+', 'https://www.lensois.com/wp-content/uploads/2025/07/ligue-1-1.jpg'],
    21: ['Ligue 1+ CH2', 'https://www.monpetitforfait.com/comparateur-box-internet/wp-content/uploads/2025/07/ligue-1-plus-2.png'],
    22: ['Ligue 1+ CH3', 'https://www.monpetitforfait.com/comparateur-box-internet/wp-content/uploads/2025/07/ligue-1plus-3-box-internet-300x95.png'],
    39: ['Ligue 1+ CH4', 'https://www.monpetitforfait.com/comparateur-box-internet/wp-content/uploads/2025/07/ligue-1plus-4-box-internet-300x106.png'],
    40: ['Ligue 1+ CH5', 'https://www.monpetitforfait.com/comparateur-box-internet/wp-content/uploads/2025/07/ligue-1-plus-5.png'],
    1: ['bein Sports 1', 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_1_Australia.png'],
#    20: ['DAZN1', 'https://cdn.sincroguia.tv/uploads/images/e/q/k/xdazn1.jpg.pagespeed.ic.oaUemASdvr.jpg'],
    # 21: ['DAZN2', 'https://cdn.sincroguia.tv/uploads/images/g/8/t/xdazn2.jpg.pagespeed.ic.SKK2xVfOfw.jpg'],
    # 22: ['DAZN3', 'https://cdn.sincroguia.tv/uploads/images/7/9/t/xdazn3.jpg.pagespeed.ic.BXBiZkQLdS.jpg'],
    # 40: ['DAZN4', 'https://cdn.sincroguia.tv/uploads/images/m/w/t/xdazn4.jpg.pagespeed.ic.eFrCKmRmJ6.jpg'],
    # 20: ['prime video ligue 2', 'https://i.imgur.com/PvpkxgG.png'],
    11: ['Canal+', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_301.PNG'],
    12: ['Canal+ Foot', 'https://upload.wikimedia.org/wikipedia/fr/3/3b/C%2B_Foot.png'],
    13: ['Canal+ sport', 'https://upload.wikimedia.org/wikipedia/fr/2/2c/C%2B_Sport_%282023%29.png'],
    14: ['Canal+ sport 360', 'https://upload.wikimedia.org/wikipedia/fr/1/11/C%2B_Sport_360.png'],
    # : ['Canal+ décalé', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_257.PNG'],
    15: ['eurosport 1', 'https://2.bp.blogspot.com/-qEkUoydNN-E/WvMoKma36fI/AAAAAAAAG_0/ov-d571uhZ443Nai7gdU9sSIV2IBOkquQCLcBGAs/s1600/europsort-1-HD.jpg'],
    16: ['eurosport 2', 'https://4.bp.blogspot.com/-1bHZ8b5ZnW0/VzDh6KfzayI/AAAAAAAABsI/lKDWcPmyBSk7etoAj2DVr7nvQ5SsMPwzgCLcB/s1600/fhuxmcp92wg1w4y9pd2v4zjz3xs1vmjm.jpg'],
    17: ['RMC Sport 1', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT1_PNG_500x500px.png?w=500&ssl=1'],
    18: ['RMC Sport 2', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT2_PNG_500x500px.png?fit=500%2C500&ssl=1'],
    19: ['L\'equipe', 'https://www.cse.fr/wp-content/uploads/2016/02/LEquipe_logo-300x200-300x150.png'],
    23: ['Automoto', 'https://moto-station.com/wp-content/uploads/2021/05/05/Automoto-La-Chaine-logo_0.png.jpg'],
    31: ['Canal+ Live 1', 'https://www.lyngsat.com/logo/tv/cc/canal-plus-live-1-fr.png'],
    32: ['Canal+ Live 2', 'https://www.lyngsat.com/logo/tv/cc/canal-plus-live-2-fr.png'],
    33: ['Canal+ Live 3', 'https://www.lyngsat.com/logo/tv/cc/canal-plus-live-3-fr.png'],
    2: ['bein Sports 2', 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_2_Australia.png'],
    3: ['bein Sports 3', 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_3_Australia.png'],
    4: ['bein Sports MAX 4', 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_Max_4.png'],
    5: ['bein Sports MAX 5', 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_Max_5.png'],
    6: ['bein Sports MAX 6', 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_Max_6.png'],
    7: ['bein Sports MAX 7', 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_Max_7.png'],
    8: ['bein Sports MAX 8', 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_Max_8.png'],
    9: ['bein Sports MAX 9', 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_Max_9.png'],
    10: ['bein Sports MAX 10', 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_Max_10.png'],
    # 31: ['multisport+ 1', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    # 32: ['multisport+ 2', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    # 33: ['multisport+ 3', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    # 34: ['multisport+ 4', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    # 35: ['multisport+ 5', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    # 36: ['multisport+ 6', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_562.PNG'],
    # 24: ['TF1', 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/TF1_logo_2013.png/800px-TF1_logo_2013.png'],
    # 25: ['TMC', ''],
    # 26: ['M6', ''],
    # 27: ['W9', ''],
    # 28: ['France 2', 'https://i.imgur.com/PvpkxgG.png'],
    # 29: ['France 3', 'https://i.imgur.com/PvpkxgG.png'],
    # 30: ['France 2', 'https://www.ffp.asso.fr/wp-content/uploads/2018/10/France-2.png'],
    # 38: ['France 3', 'https://static.wikia.nocookie.net/hdl-logopedia/images/0/0a/Logo-france-3.png/revision/latest/scale-to-width-down/220?cb=20180220171302&path-prefix=fr']
    # 40: ['FFFtv', 'https://upload.wikimedia.org/wikipedia/commons/e/e2/Tmc_2016.png']
    }

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_TV[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_TV[1], 'Chaines', 'tv.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    # oGui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'Par genres', 'genre_sport.png', oOutputParameterHandler)
    #
    # oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    # oGui.addDir(SITE_IDENTIFIER, SPORT_LIVE[1], 'En cours', 'replay.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showGenres():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(URL_MAIN + sUrl)
    links = oRequestHandler.request(jsonDecode=True)

    types = set()
    oOutputParameterHandler = cOutputParameterHandler()
    for link in links:
        types.add(link['type'].capitalize())

    for sTitle in sorted(types):
        sDiplayTitle = sTitle.replace('Footus', 'Foot US')
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sDesc', sTitle)
        
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sDiplayTitle, "sport.png", oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showTV():
    oGui = cGui()

    chaines = [20, 21, 22, 39, 40, 11, 12, 13, 14, 17, 18, 15, 16, 19, 23, 31, 32, 33, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # if 'sport' in sUrl:
    # chaines = [1, 4, 21, 20, 5, 6, 7, 8, 18, 19, 9, 2, 3, 10, 11, 12, 13, 14, 15, 16, 22, 23, 24, 25, 26, 27, 28, 37, 31, 32, 33, 34, 35, 36]
    # else: # Chaines ciné
    # chaines = [21, 22, 23, 29, 30, 38, 5, 17, 39]

    oOutputParameterHandler = cOutputParameterHandler()
    for iChannel in chaines:
        channel = channels.get(iChannel)
        sThumb = channel[1]

        sDisplayTitle = channel[0]
        sHostUrl = URL_LINK + '/%d' % iChannel
        oOutputParameterHandler.addParameter('siteUrl', sHostUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addLink(SITE_IDENTIFIER, 'showLink', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showTVLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')

    oOutputParameterHandler = cOutputParameterHandler()
    for numChannel in range(1, 6):
        sHostUrl = URL_LINK + "/%d/%s" % (numChannel, sUrl)
        sDisplayTitle = '%s - Lien %d' % (sTitle, numChannel)
        oOutputParameterHandler.addParameter('siteUrl', sHostUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oGui.addLink(SITE_IDENTIFIER, 'showLink', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sSearchType = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(URL_MAIN + sUrl)
    links = oRequestHandler.request(jsonDecode=True)

    oOutputParameterHandler = cOutputParameterHandler()
    for link in links:
        sType = link['type']
        if sSearchType and sType.capitalize() != sSearchType:  # filtrage du genre recherché
            continue
        
        time = link['time']
        home = link['home']
        away = link['away']
        league = link['league']
        
        time = datetime.datetime.fromtimestamp(int(time)/1000)
#        time = datetime.datetime.strftime(time, '%d/%m/%Y %H:%M:%S')
        time = datetime.datetime.strftime(time, '%H:%M:%S')
        
        if away:
            sTitle = '%s - %s / %s (%s)' % (time, home, away, league)
        else:
            sTitle = '%s - %s (%s)' % (time, home, league)
        
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
        oOutputParameterHandler.addParameter('sDesc', sTitle)

        oGui.addDir(SITE_IDENTIFIER, 'showMovieLinks', sTitle, "sport.png", oOutputParameterHandler)
        
    oGui.setEndOfDirectory()


def showMovieLinks():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sSearchTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    links = oRequestHandler.request(jsonDecode=True)

    oOutputParameterHandler = cOutputParameterHandler()
    for link in links:
        time = link['time']
        home = link['home']
        away = link['away']
        league = link['league']
        
        time = datetime.datetime.fromtimestamp(int(time)/1000)
#        time = datetime.datetime.strftime(time, '%d/%m/%Y %H:%M:%S')
        time = datetime.datetime.strftime(time, '%H:%M:%S')
        
        if away:
            sTitle = '%s - %s / %s (%s)' % (time, home, away, league)
        else:
            sTitle = '%s - %s (%s)' % (time, home, league)
        
        if sSearchTitle != sTitle:  # le titre recherché
            continue
        
        for streams in link['streams']:
            channel = streams['ch']
            sHostUrl = '%s/%s' % (URL_LINK, channel)

            lang = streams['lang']
            sDisplayTitle = '%s [%s]' % (sTitle, lang.upper())
            
            oOutputParameterHandler.addParameter('siteUrl', sHostUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
            oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', 'sport.png')
    
            oGui.addDir(SITE_IDENTIFIER, 'showLink', sDisplayTitle, 'sport.png', oOutputParameterHandler)
        
    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    allUrls = [(sUrl % a) for a in (2, 4, 3, 1)]
    numLien = 1
    oOutputParameterHandler = cOutputParameterHandler()
    for sHostUrl in allUrls:  # on parcourt les liens à l'envers car le premier n'est pas le meilleur
        oOutputParameterHandler.addParameter('siteUrl', sHostUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sDesc', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        sDisplayTitle = '%s - Lien %d' % (sMovieTitle, numLien)
        oGui.addLink(SITE_IDENTIFIER, 'showHoster', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)
        numLien = numLien + 1

    oGui.setEndOfDirectory()


def showHoster():
    oGui = cGui()
    oHosterGui = cHosterGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = URL_MAIN + oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    sHosterUrl = getHosterIframe(sUrl, sUrl)
    if sHosterUrl:
        sHosterUrl = sHosterUrl.strip()
        oHoster = oHosterGui.checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            oHosterGui.showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()



# Traitement générique
def getHosterIframe(url, referer):
    
    if 'youtube.com' in url:
        return None

    if not url.startswith('http'):
        url = URL_MAIN + url

    oRequestHandler = cRequestHandler(url)
    if referer:
        oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = str(oRequestHandler.request())
    if not sHtmlContent or sHtmlContent == 'False':
        return False

    referer = oRequestHandler.getRealUrl()
    
    return getUrl(sHtmlContent, referer)


def getUrl(sHtmlContent, referer):

    sPattern = r'(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))' # Recherche "eval(function(...{}))"
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        for sstr in aResult:
            if not sstr.endswith(';'):
                sstr = sstr + ';'
            html = cPacker().unpack(sstr)
            html = html.replace('\\', '')
            url = getUrl(html, referer)
            if url:
                return url

    sPattern = r'.atob\("(.+?)"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        import base64
        for code in aResult:
            try:
                if isMatrix():
                    code = base64.b64decode(code).decode('ascii')
                else:
                    code = base64.b64decode(code)
                if '.m3u' in code:
                    return code + '|Referer=' + referer
            except Exception as e:
                pass
    
    sPattern = r'<iframe.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        for url in aResult:
            if url.startswith("./"):
                url = url[1:]
            if not url.startswith("http"):
                if not url.startswith("//"):
                    url = '//'+referer.split('/')[2] + url  # ajout du nom de domaine
                url = "https:" + url
            url = getHosterIframe(url, referer)
            if url:
                return url

    sPattern = r'player.load\({source: (.+?)\('
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        func = aResult[0]
        sPattern = r'function %s\(\) +{\n + return\(\[([^\]]+)' % func
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            sHosterUrl = aResult[0].replace('"', '').replace(',', '').replace('\\', '').replace('////', '//')
            return sHosterUrl + '|referer=' + referer

    sPattern = r';var.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        for url in aResult:
            if '.m3u8' in url:
                return url + '|Referer=' + referer

    sPattern = r'[^/]source.+?["\'](https.+?)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        for sHosterUrl in aResult:
            if '.m3u8' in sHosterUrl:
                if 'fls/cdn/' in sHosterUrl:
                    sHosterUrl = sHosterUrl.replace('/playlist.', '/tracks-v1a1/mono.')
                else:
                    oRequestHandler = cRequestHandler(sHosterUrl)
                    oRequestHandler.addHeaderEntry('Referer', referer)
                    oRequestHandler.request()
                    sHosterUrl = oRequestHandler.getRealUrl()
    #            sHosterUrl = sHosterUrl.replace('index', 'mono')
                return sHosterUrl + '|referer=' + referer

    sPattern = r'file: *["\'](https.+?\.m3u8)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        oRequestHandler = cRequestHandler(aResult[0])
        oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()
        return sHosterUrl + '|referer=' + referer


    sPattern = r'new Player\("100%","100%","player","(.+?)",{"(.+?)":'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sHosterUrl = 'https://%s/hls/%s/live.m3u8' % (aResult[0][1], aResult[0][0])
        return sHosterUrl + '|referer=' + referer

    sPattern = r'new Player\("100%","100%","player","(.+?)".+?,"([^"]+)"'
    aResult = re.findall(sPattern, sHtmlContent)
    if not aResult:
        sPattern = r'new Player\("100%","100%","player","(.+?)".+?,"([^"]+)"'
        aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sHosterUrl = 'https://%s/hls/%s/live.m3u8' % (aResult[0][1], aResult[0][0])
        return sHosterUrl + '|referer=' + referer
    
    sPattern = r"new Player\('(.+?=)'\)"
    aResult = re.findall(sPattern, sHtmlContent.replace('\\', ''))
    if aResult:
        VSlog('Lien chiffré par cryptographie non encore supporté')
        #TODO Convertir en python la fonction Player(opts) dans /player-bundle-min.js : encrypted_json_string=opts,passphrase="jzAqXKPaoDu4KSaYsOne3rNOGGBXK71JoUFfkZ0DXrloaGcZmrwv9B0jmsHVruq",obj_json=JSON.parse(atob(encrypted_json_string)),encrypted=obj_json.ciphertext,salt=CryptoJS.enc.Hex.parse(obj_json.salt),iv=CryptoJS.enc.Hex.parse(obj_json.iv),key=CryptoJS.PBKDF2(passphrase,salt,{hasher:CryptoJS.algo.SHA512,keySize:8,iterations:1}),opts=CryptoJS.AES.decrypt(encrypted,key,{iv:iv}).toString(CryptoJS.enc.Utf8)
        return False

    sPattern = r'''<script src="https://([^/]+)/embed.min.js\?v=3" +onload="ThePlayerJS\('.+?','(.+?)'\);"></script>'''
    html = sHtmlContent.replace('\\','')
    aResult = re.findall(sPattern, html)
    if aResult:
        sHosterUrl = r'https://%s/player/%s' % (aResult[0][0], aResult[0][1])
        return getHosterIframe(sHosterUrl, referer)
    
    decoded = reveal_pipe_split(sHtmlContent)
    if decoded:
        return getUrl(decoded, referer)
    
    decoded = reveal_char_by_char_url(sHtmlContent)
    if decoded and '.m3u8' in decoded:
        return decoded + '|referer=' + referer

    return False


def reveal_char_by_char_url(html):
    html = html.replace('\\','')
    pattern = r'((?:".",)+".")\].join\(""\)'
    result = re.findall(pattern, html)
    if result:
        text = ''
        for char in result[0].split(','):
            text += char.replace('"','')
        return text

def reveal_pipe_split(html):
    pattern = r"return p\}(\(.*),'(.*?)'.split\('\|'\)"
    html = html.replace('\\', '')
    results = re.findall(pattern, html)
    
    if not results:
        return
    
    def is_numeric_mode():
        for char in list('abcdefghij'):
            if not re.search(r"\b{}\b".format(char), html):
                return True
        return False
    
    numeric_mode = is_numeric_mode()

    def tokenToInt(token):
        if numeric_mode:
            return int(token)
        if token.isalpha() and not token.isupper(): # a-z
            return ord(token) - 87   # -> 10-35
        elif token.isupper():                         # A-Z
            return ord(token) - 29   # -> 36-61
        elif len(token) == 1:                         # 0-9
            return int(token)        # -> 0-9
        return int(token) + 52   # -> 62-151
    
    def replaceNumber(match):
        token = match.group(0)
        num = tokenToInt(token)

        if num < len(keywords):
            if keywords[num]:
                return keywords[num]
            else:
                return token
        return token
    
    text = ''
    for result in results:
        mask = result[0]
        keywords = result[1].split('|')
        text += re.sub('([0-9a-zA-Z]+)',replaceNumber, mask)
    return text
