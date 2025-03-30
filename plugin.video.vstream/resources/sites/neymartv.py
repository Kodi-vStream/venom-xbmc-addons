# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.comaddon import siteManager, isMatrix
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser


SITE_IDENTIFIER = 'neymartv'
SITE_NAME = 'NeymarTV'
SITE_DESC = 'Toutes les chaines de Sport'
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

SPORT_SPORTS = ('/', 'load')
SPORT_GENRES = ('p/all-sports-tv-schedule.html', 'showGenres')

TV_TV = ('/', 'load')
SPORT_TV = ('31-site-pour-regarder-les-chaines-de-sport.html', 'showTV')

HEURE_HIVER = False

# chaines
channels = [
    
#    ['DAZN 1', ['https://poscitechs.lol/live/stream-106.php', 'https://images.beinsports.com/n43EXNeoR62GvZlWW2SXKuQi0GA=/788708-HD1.png']],
    
    ['bein Sports 1', ['2025/03/bein-sports-1-full-hd-france.html', 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_1_Australia.png']],
    ['bein Sports 2', ['2025/03/bein-sports-2-full-hd-france.html', 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_2_Australia.png']],
    ['bein Sports 3', ['2025/03/bein-sports-3-full-hd-france.html', 'https://r2.thesportsdb.com/images/media/channel/logo/BeIn_Sports_3_Australia.png']],

    ['RMC Sport 1', ['2025/03/rmc-sport-1-full-hd.html', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT1_PNG_500x500px.png?w=500&ssl=1']],
    ['RMC Sport 2', ['2025/03/rmc-sport-2-full-hd.html', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT2_PNG_500x500px.png?fit=500%2C500&ssl=1']],

    ['Canal+', ['2025/03/canal-france-full-hd.html', 'https://thumb.canalplus.pro/http/unsafe/epg.canal-plus.com/mycanal/img/CHN43FN/PNG/213X160/CHN43FB_301.PNG']],
    ['Canal+ Sports', ['2025/03/canal-sport-full-hd.html', 'https://matchpint-cdn.matchpint.cloud/shared/imagenes/channels/284_logo_1599851988.png']],

    ['eurosport 1', ['2025/03/all-eurosport-channels-france-full-hd.html', 'https://2.bp.blogspot.com/-qEkUoydNN-E/WvMoKma36fI/AAAAAAAAG_0/ov-d571uhZ443Nai7gdU9sSIV2IBOkquQCLcBGAs/s1600/europsort-1-HD.jpg']],
    ['eurosport 2', ['2025/03/all-eurosport-channels-france-full-hd.html', 'https://4.bp.blogspot.com/-1bHZ8b5ZnW0/VzDh6KfzayI/AAAAAAAABsI/lKDWcPmyBSk7etoAj2DVr7nvQ5SsMPwzgCLcB/s1600/fhuxmcp92wg1w4y9pd2v4zjz3xs1vmjm.jpg']],

    ['L\'equipe TV', ['2025/03/lequipe-tv-full-hd.html', 'https://www.cse.fr/wp-content/uploads/2016/02/LEquipe_logo-300x200-300x150.png']],
    # ['Golf Channel', ['2023/01/all-canal-channels-france-full-hd.html', 'https://www.golfchannel.fr/upload/media/golf-channel-600af6fe955c3.png']],

    ['bein Sports MAX', ['2025/03/all-bein-sports-channels-france.html', 'https://c.clc2l.com/t/b/e/bein-sports-Q3N2zb.jpg']],
    # ['bein Sports MAX 4', ['2023/01/all-bein-sports-channels-france.html', 'https://images.beinsports.com/owLVmBRH9cHk6K9JSocpTw0Oc4E=/788713-4MAX.png']],
    # ['bein Sports MAX 5', ['2023/01/all-bein-sports-channels-france.html', 'https://images.beinsports.com/FE2dOGMxn1waqAFYxqsGxXKkvCo=/788714-5MAX.png']],
    # ['bein Sports MAX 6', ['2023/01/all-bein-sports-channels-france.html', 'https://images.beinsports.com/beNacZewwA5WqFglPAwOaD4n5QA=/788715-6MAX.png']],
    # ['bein Sports MAX 7', ['2023/01/all-bein-sports-channels-france.html', 'https://images.beinsports.com/6IXXUorOrK_n756SjT6a2Ko7jiM=/788716-7MAX.png']],
    # ['bein Sports MAX 8', ['2023/01/all-bein-sports-channels-france.html', 'https://images.beinsports.com/6aOfeAugcgMy93nrOfk8NAacALs=/788717-8MAX.png']],
    # ['bein Sports MAX 9', ['2023/01/all-bein-sports-channels-france.html', 'https://images.beinsports.com/etM_TIm1DmhWr0TZ_CbWGJvaTdQ=/788718-9MAX.png']],
    # ['bein Sports MAX 10', ['2023/01/all-bein-sports-channels-france.html', 'https://images.beinsports.com/LxFG3ZG88jlFsOyWo_C7o4mdY7M=/788719-10MAX.png']],

    # ['RMC SPORT 3', ['2022/03/rmc-sport-3-full-hd.html', 'https://i0.wp.com/www.planetecsat.com/wp-content/uploads/2018/07/RMC_SPORT3_PNG_500x500px.png?w=500&ssl=1']],
    # ['RMC SPORT 4', ['2022/03/rmc-sport-4-full-hd.html', 'https://w0rld.tv/wp-content/uploads/2020/09/rmc-sport-4.png']],
    # ['RMC SPORT LIVE 5', ['p/all-sports-tv-channels-full-hd.html', 'https://www.planetecsat.com/wp-content/uploads/2022/09/Entete-RMC-Sport.png']],
    # ['RMC SPORT LIVE 6', ['p/all-sports-tv-channels-full-hd.html', 'https://www.planetecsat.com/wp-content/uploads/2022/09/Entete-RMC-Sport.png']],
    # ['RMC SPORT LIVE 7', ['p/all-sports-tv-channels-full-hd.html', 'https://www.planetecsat.com/wp-content/uploads/2022/09/Entete-RMC-Sport.png']],
    # ['RMC SPORT LIVE 8', ['p/all-sports-tv-channels-full-hd.html', 'https://www.planetecsat.com/wp-content/uploads/2022/09/Entete-RMC-Sport.png']],
    # ['RMC SPORT LIVE 9', ['p/all-sports-tv-channels-full-hd.html', 'https://www.planetecsat.com/wp-content/uploads/2022/09/Entete-RMC-Sport.png']],
    # ['RMC SPORT LIVE 10', ['p/all-sports-tv-channels-full-hd.html', 'https://www.planetecsat.com/wp-content/uploads/2022/09/Entete-RMC-Sport.png']]

    ]


def load():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'Sports (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_TV[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_TV[1], 'Chaines TV Sports', 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showTV():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    for sDisplayTitle, value in channels:
        sUrl = value[0]
        sThumb = value[1]
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        
        oGui.addLink(SITE_IDENTIFIER, 'showHoster', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)
#        oGui.addLink(SITE_IDENTIFIER, 'showHoster', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenres():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    oRequestHandler = cRequestHandler(URL_MAIN + sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<iframe src="([^"]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sUrl = aResult[1][0]
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        start = 'SCHEDULE TIME'
        end = 'NO EVENTS TODAY'
        sHtmlContent = oParser.abParse(sHtmlContent, start, end)
    
        sPattern = '<h3> (.+?) <\/h3> *<div'
        aResult = oParser.parse(sHtmlContent, sPattern)
    
        if not aResult[0]:
            oGui.addText(SITE_IDENTIFIER)
        else:
            sportGenre = {}
            oOutputParameterHandler = cOutputParameterHandler()
            for sTitle in aResult[1]:
                if 'TV SHOWS' in sTitle:
                    continue
                sDisplayTitle = sTitle
                sDisplayTitle = sDisplayTitle.replace('ALPINE SKI', 'SKI')
                sDisplayTitle = sDisplayTitle.replace('BOXING', 'BOXE')
                sDisplayTitle = sDisplayTitle.replace('CLIMBING', 'ESCALADE')
                sDisplayTitle = sDisplayTitle.replace('CYCLING', 'CYCLISME')
                sDisplayTitle = sDisplayTitle.replace('DARTS', 'FLECHETTES')
                sDisplayTitle = sDisplayTitle.replace('HORSE RACING', 'COURSES DE CHEVAUX')
                sDisplayTitle = sDisplayTitle.replace('ICE HOCKEY', 'HOCKEY SUR GLACE')
                sDisplayTitle = sDisplayTitle.replace('RUGBY UNION', 'RUGBY')
                sDisplayTitle = sDisplayTitle.replace('SAILING/BOATING', 'VOILE')
                sDisplayTitle = sDisplayTitle.replace('SOCCER', 'FOOTBALL')
                sDisplayTitle = sDisplayTitle.replace('TABLE TENNIS', 'TENNIS DE TABLE')
                sportGenre[sDisplayTitle] = sTitle
    
            for sDisplayTitle, sTitle in sorted(sportGenre.items()):
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sDisplayTitle, 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    if 'http' not in sUrl:
        sUrl = URL_MAIN + sUrl

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    
    # Recherche du sport sélectionné
    # il faut echapper les parenthese qui peuvent apparaitre dans les noms
    sPattern = '<h3> %s <.+?<h3>' % sTitle.replace('(', '\(').replace(')', '\)')
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sPattern = '(\d+:\d+) (.+?)(<|")'
        for aEntry in aResult[1]:
            aResult = oParser.parse(aEntry, sPattern)
            if aResult[0]:
                oOutputParameterHandler = cOutputParameterHandler()
                for aEntry in aResult[1]:
                    sTitle = aEntry[1].strip()
        
                    # heure d'été/hiver
                    sDate = aEntry[0]
                    heure = int(sDate[0:2])
                    heure += 1 if HEURE_HIVER else 2
                    if heure == 24:
                        heure = 0
                    sDisplayTitle = '%02d:%s - %s' % (heure, sDate[3:], sTitle.replace('.php', ')').strip())
        
                    sTitle = sDate + ' ' + sTitle
        
                    oOutputParameterHandler.addParameter('siteUrl', sUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)
                    oGui.addDir(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMoviesLinks():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # on enleve l'heure qui peut être fausse, heure d'été/hiver
    sMovieTitle = sMovieTitle[5:]

    sPattern = sMovieTitle#.replace("'", "&#8217;").replace("-", "&#8211;")
    sHtmlContent = oParser.abParse(sHtmlContent, sPattern, '<br')

    sPattern = '(<span style|\|\|([^<]+)).+?href="(.+?)" target="_blank" rel="noopener"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sMovieTitle = sMovieTitle.replace('.php', ')')
    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        iLien = 0
        for aEntry in aResult[1]:
            sChannel = aEntry[1]
            sUrl = aEntry[2]
            #link = aEntry[1].replace('CH-', 'Lien ').replace('LINK', '1').strip()
            if sChannel:
                sTitle = sChannel
                sDisplayTitle = sMovieTitle + ' - (%s)' % sChannel
            else:
                iLien = iLien + 1
                sDisplayTitle = sMovieTitle + ' - (Lien %d)' % iLien
                sTitle = sDisplayTitle

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showLink', sDisplayTitle, 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


# tous les liens d'une chaine à partir de son nom
def showMoviesLink():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = URL_MAIN + 'p/all-sports-tv-channels-full-hd.html'

    # ajouter un espace devant les chiffres
    sMovieTitle = re.sub('(\S)(\d+)', r'\1 \2', sMovieTitle)
    
    sTitle = sMovieTitle.lower().replace('+', "").replace('canal sport france', 'canal sport')
    sTitle = sTitle.replace('poland', 'polska')
    sTitle = re.sub(' es$', ' spain', sTitle)
    sTitle = re.sub(' fr$', ' france', sTitle)
    sTitle = "[^']+"+sTitle.replace(' ', "[^']+")+"[^']+"

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = "<button class=\"button-24\" onclick=\"document\.location='(%s)'" % sTitle

    aResult = oParser.parse(sHtmlContent, sPattern)

    # on enleve l'heure qui peut être fausse, heure d'été/hiver
    sTitle = sTitle[5:]
    
    if not aResult[0]:
        showLink()
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        aEntry = aResult[1][0]
            
        sUrl = aEntry.strip()
        sDisplayTitle = sMovieTitle

        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)
        oGui.addDir(SITE_IDENTIFIER, 'showHoster', sDisplayTitle, 'sport.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()



def showHoster():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    displayHoster = False
    if not sUrl.startswith('http'):
        sUrl = URL_MAIN + sUrl

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<li movieurl=["\']([^"]+)["\']><a>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:  # si les boutons ne sont pas CH1, CH2, etc, ce sont les noms de chaines
        sPattern = '<button class="dropbtn" data-src=["\']([^"]+)["\'].*?>([^<]+)'
        aResult = oParser.parse(sHtmlContent, sPattern)
        displayHoster = True
    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        blackList = ('.tutele.sx', 'leet365', 'casadelfutbol.net', 'yrsport.top', 'cdn.sportcast.life', '.ustreamix.su',
                     'sportzonline.to', 'sportkart1.xyz', 'olasports.xyz', 'cricplay2.xyz', 's2watch.link', 
                     'cricfree.live', '2024tv.ru', 'sportzlive.shop', 'dlhd.so')
        oOutputParameterHandler = cOutputParameterHandler()
        numLien = 1
        allUrls = []
        for aEntry in aResult[1]: 
            sUrl = aEntry[0]

            # On retire les doublons
            sUrl = sUrl.replace( # poscitechs.lol=arlive.shop=footballstreams.lol
                'poscitechs.lol/live', 'footballstreams.lol/embed'
            ).replace(
                'arlive.shop/player', 'footballstreams.lol/embed')
            if sUrl in allUrls:
                continue
            allUrls.append(sUrl)

            for out in blackList:
                if out in sUrl:
                    sUrl = None
                    break

            if not sUrl:
                continue

            if displayHoster:
                sTitle = aEntry[1]
                sDisplayTitle = sTitle
            else:
                sDisplayTitle = "%s (Lien %d)" % (sTitle, numLien)
            numLien += 1

            if 'http' not in sUrl:
                sUrl = URL_MAIN[:-1] + sUrl

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sDesc', sDisplayTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addLink(SITE_IDENTIFIER, 'showLink', sDisplayTitle, sThumb, sDisplayTitle, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    siterefer = oInputParameterHandler.getValue('siterefer')

    bvalid, sHosterUrl = getHosterIframe(sUrl, siterefer)
    if bvalid:
        sHosterUrl = sHosterUrl.strip()
        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if oHoster:
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


# Traitement générique
def getHosterIframe(url, referer):

    if 'youtube.com' in url:
        return False, False

    if not url.startswith('http'):
        url = URL_MAIN + url

    oRequestHandler = cRequestHandler(url)
    
    if referer:
        oRequestHandler.addHeaderEntry('Referer', referer)
#    oRequestHandler.disableSSL()
    sHtmlContent = str(oRequestHandler.request())
    # import xbmcvfs
    # f = xbmcvfs.File('special://userdata/addon_data/plugin.video.vstream/test.txt','w')
    # f.write(sHtmlContent)
    # f.close()

#    cook = oRequestHandler.GetCookies()

    if not sHtmlContent or sHtmlContent == 'False':
        return False, False

    if 'webxzplay' in url:
        return getPkpakiUrl(url, sHtmlContent, referer)

    
    referer = oRequestHandler.getRealUrl()


    sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        from resources.lib.packer import cPacker
        sstr = aResult[0]
        if not sstr.endswith(';'):
            sstr = sstr + ';'
        sHtmlContent = cPacker().unpack(sstr)

    sPattern = '.atob\("(.+?)"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        import base64
        for code in aResult:
            try:
                if isMatrix():
                    code = base64.b64decode(code).decode('ascii')
                else:
                    code = base64.b64decode(code)
                if '.m3u8' in code:
                    return True, code + '|Referer=' + referer
            except Exception as e:
                pass

    sPattern = '<iframe.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        for url in aResult:
            if url.startswith("./"):
                url = url[1:]
            if not url.startswith("http"):
                if not url.startswith("//"):
                    url = '//' + referer.split('/')[2] + url  # ajout du nom de domaine
                url = "https:" + url
            b, url = getHosterIframe(url, referer)
            if b:
                return True, url

    sPattern = 'player.load\({source: (.+?)\('
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        func = aResult[0]
        sPattern = 'function %s\(\) +{\n + return\(\[([^\]]+)' % func
        aResult = re.findall(sPattern, sHtmlContent)
        if aResult:
            sHosterUrl = aResult[0].replace('"', '').replace(',', '').replace('\\', '').replace('////', '//')
            return True, sHosterUrl + '|referer=' + referer

    sPattern = ';var.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        for url in aResult:
            if '.m3u8' in url:
                return True, url + '|referer=' + referer

    sPattern = '[^/]source.+?["\'](https.+?)["\']'
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
                # oRequestHandler = cRequestHandler(sHosterUrl)
                # h = oRequestHandler.request()
                return True, sHosterUrl + '|referer=' + referer

    sPattern = 'file: *["\'](https.+?\.m3u8)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        oRequestHandler = cRequestHandler(aResult[0])
        oRequestHandler.request()
        sHosterUrl = oRequestHandler.getRealUrl()
        return True, sHosterUrl + '|referer=' + referer
    
    sPattern = 'new Player\("100%","100%","player","(.+?)".+?,"([^"]+)"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sHosterUrl = 'https://%s/hls/%s/live.m3u8' % (aResult[0][1], aResult[0][0])
        return True, sHosterUrl + '|referer=' + referer

    sPattern = r'new Player\("100%","100%","player","(.+?)".+?,"([^"]+)"'
    aResult = re.findall(sPattern, sHtmlContent)
    if not aResult:
        sPattern = r'new Player\("100%","100%","player","(.+?)".+?,"([^"]+)"'
        aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sHosterUrl = 'https://%s/hls/%s/live.m3u8' % (aResult[0][1], aResult[0][0])
        return True, sHosterUrl + '|referer=' + referer
    
    sPattern = r"new Player\('(.+?=)'\)"
    aResult = re.findall(sPattern, sHtmlContent.replace('\\', ''))
    if aResult:
        # VSlog('Lien chiffré par cryptographie non encore supporté')
        #TODO Convertir en python la fonction Player(opts) dans /player-bundle-min.js : encrypted_json_string=opts,passphrase="jzAqXKPaoDu4KSaYsOne3rNOGGBXK71JoUFfkZ0DXrloaGcZmrwv9B0jmsHVruq",obj_json=JSON.parse(atob(encrypted_json_string)),encrypted=obj_json.ciphertext,salt=CryptoJS.enc.Hex.parse(obj_json.salt),iv=CryptoJS.enc.Hex.parse(obj_json.iv),key=CryptoJS.PBKDF2(passphrase,salt,{hasher:CryptoJS.algo.SHA512,keySize:8,iterations:1}),opts=CryptoJS.AES.decrypt(encrypted,key,{iv:iv}).toString(CryptoJS.enc.Utf8)
        return False

    sPattern = r'''<script src="https://([^/]+)/embed.min.js\?v=3" +onload="ThePlayerJS\('.+?','(.+?)'\);"></script>'''
    html = sHtmlContent.replace('\\','')
    aResult = re.findall(sPattern, html)
    if aResult:
        url = r'https://%s/player/%s' % (aResult[0][0], aResult[0][1])
        b, url = getHosterIframe(url, referer)
        if b:
            return True, url

    sPattern = r'https://(.+?\.xyz)/mono.php\?id=([0-9]+)'
    result = re.findall(sPattern, referer)
    if result:
        domain = result[0][0]
        id = result[0][1]

        oRequestHandler = cRequestHandler('https://' + domain + '/server_lookup.php?channel_id=mono' + id)
        response = oRequestHandler.request(jsonDecode=True)
        serverKey = response['server_key']
        channelKey = "mono" + id
        return True, "https://" + serverKey + "new.koskoros.ru/" + serverKey + "/" + channelKey + "/mono.m3u8|Referer=" + referer

    decoded = reveal_pipe_split(sHtmlContent)
    if decoded:
        b, url = getHosterIframe(decoded, referer)
        if b:
            return True, url
    
    decoded = reveal_char_by_char_url(sHtmlContent)
    if decoded and '.m3u8' in decoded:
        url = decoded + '|referer=' + referer
        if url:
            return True, url

    return False, False


def getPkpakiUrl(url, sHtmlContent, referer):
    
    premiumId = url.split('=')[1]
    oRequestHandler = cRequestHandler('https://webxzplay.cfd/server_lookup.php?channel_id=premium' + premiumId)
    response = oRequestHandler.request(jsonDecode=True)
    serverKey = response['server_key']
    result = re.findall('https://top1\.([^\.]+)', sHtmlContent)
    if result:
        return True, 'https://%snew.%s.ru/%s/premium%s/mono.m3u8|Referer=%s' % (serverKey, result[0], serverKey, premiumId, url)
    return False, False

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
    result = re.findall(pattern, html)
    if not result:
        return
    mask = result[0][0]
    keywords = result[0][1].split('|')
    def replaceNumber(match):
        num = int(match.group(0))
        if num < len(keywords):
            return keywords[num]
        return match.group(0)
    text = re.sub('([0-9]+)',replaceNumber, mask)
    return text
