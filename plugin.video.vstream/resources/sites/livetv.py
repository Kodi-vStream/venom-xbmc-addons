#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Ovni-crea
from resources.lib.gui.hoster import cHosterGui #systeme de recherche pour l'hote
from resources.lib.gui.gui import cGui #systeme d'affichage pour xbmc
from resources.lib.handler.inputParameterHandler import cInputParameterHandler #entree des parametres
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler #sortie des parametres
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.parser import cParser #recherche de code
from resources.lib.comaddon import progress, VSlog, dialog
from resources.lib.util import cUtil #import du plugin cUtil
import re, urllib, urllib2
import base64

from resources.lib.packer import cPacker

SITE_IDENTIFIER = 'livetv'
SITE_NAME = 'Live TV'
SITE_DESC = 'Site pour regarder du sport en direct gratuitement'

URL_MAIN = 'http://livetv.sx'
URL_SEARCH = (URL_MAIN + '/frx/fanclubs/?q=', 'showMovies4')
FUNCTION_SEARCH = 'showMovies4'

SPORT_SPORTS = (URL_MAIN + '/frx/allupcoming/', 'showMovies') #Les matchs en directs
#SPORT_SPORTSCLASS = (URL_MAIN + '/frx/calendar/411/', 'showClass')# Les classements
NETS_GENRES = (True, 'showGenres') #Les clubs de football

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher l\'équipe', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1], 'Les matchs en direct', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', NETS_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, NETS_GENRES[1], 'Les clubs de foot (urlresolver requis)', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies4(sUrl) #showMovies4 car c'est pour afficher le club recherché'
        oGui.setEndOfDirectory()
        return


def showGenres(): #affiche les clubs de foot
    oGui = cGui()

    liste = []
    liste.append( ['PSG', URL_MAIN + '/frx/team/1_4_216_psg/fanclub/'] )
    liste.append( ['Marseille (OM)', URL_MAIN + '/frx/team/1_310_383_marseille/fanclub/'] )
    liste.append( ['Barcelone', URL_MAIN + '/frx/team/1_3_227_barcelona/fanclub/'] )
    liste.append( ['Real-Madrid', URL_MAIN + '/frx/team/1_163_317_real_madrid/fanclub/'] )
    liste.append( ['Marchester Utd', URL_MAIN + '/frx/team/1_350_421_manchester_utd/fanclub/'] )
    liste.append( ['Chelsea', URL_MAIN + '/frx/team/1_351_397_chelsea/fanclub/'] )
    liste.append( ['Bayern Munich', URL_MAIN + '/frx/team/1_5_227_bayern/fanclub/'] )
    liste.append( ['Juventus', URL_MAIN + '/frx/team/1_244_365_juventus/fanclub/'] )
    liste.append( ['Arsenal', URL_MAIN + '/frx/team/1_353_406_arsenal/fanclub/'] )
    liste.append( ['Liverpool', URL_MAIN + '/frx/team/1_352_412_liverpool/fanclub/'] )
    liste.append( ['Manchester City', URL_MAIN + '/frx/team/1_363_446_manchester_city/fanclub/'] )
    liste.append( ['France', URL_MAIN + '/frx/team/1_77_258_france/fanclub/'] )
    liste.append( ['Dortmund', URL_MAIN + '/frx/team/1_136_296_dortmund/fanclub/'] )
    liste.append( ['Monaco', URL_MAIN + '/frx/team/1_319_383_monaco/fanclub/'] )
    liste.append( ['Portugal', URL_MAIN + '/frx/team/1_79_269_portugal/fanclub/'] )
    liste.append( ['Argentine', URL_MAIN + '/frx/team/1_62_253_argentina/fanclub/'] )
    liste.append( ['Belgique', URL_MAIN + '/frx/team/1_83_270_belgium/fanclub/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMenu', sTitle, 'genres.png', oOutputParameterHandler)
        #showMenu car c'est pour afficher les infos du club seul resultat est fonctionnel pour l'instant''

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):#affiche les catégories qui ont des lives'

    oGui = cGui()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="main" href="([^"]+)"><b>([^"]+)</b>.+?\s*</td>\s*<td width=.+?>\s*<a class="small" href=".+?"><b>([^"]+)</b></a>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(str(aResult))

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sUrl2 = URL_MAIN + sUrl2

            sTitle = aEntry[1]
            sTitle = sTitle.decode("iso-8859-1", 'ignore')
            sTitle = cUtil().unescape(sTitle)
            sTitle = sTitle.encode("utf-8", 'ignore')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl2', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)

            oGui.addDir(SITE_IDENTIFIER, 'showMovies2', sTitle, 'sport.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()

def showMovies2(): #affiche les matchs en direct depuis la section showMovie
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl2 = oInputParameterHandler.getValue('siteUrl2')

    oRequestHandler = cRequestHandler(sUrl2)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="live" href="([^>]+)">([^>]+)</a>\s*(?:<br><img src=".+?/img/live.gif"><br>|<br>)\s*<span class="evdesc">([^>]+)\s*<br>\s*([^>]+)</span>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle2 = aEntry[1].replace('<br>', ' ')
            sUrl3 = aEntry[0]
            sThumb = ''
            #sLang = aEntry[3]
            sQual = aEntry[3]
            sHoster = aEntry[2]

            sTitle2 = sTitle2.decode("iso-8859-1", 'ignore')
            sTitle2 = cUtil().unescape(sTitle2)
            sTitle2 = sTitle2.encode("utf-8")

            sHoster = sHoster.decode("iso-8859-1", 'ignore')
            sHoster = cUtil().unescape(sHoster)
            sHoster = sHoster.encode("utf-8")

            sQual = sQual.decode("iso-8859-1", 'ignore')
            sQual = cUtil().unescape(sQual)
            sQual = sQual.encode("utf-8", 'ignore')

            sTitle2 = ('%s (%s) [COLOR yellow]%s[/COLOR]') % (sTitle2, sHoster, sQual)

            sUrl3 = URL_MAIN + sUrl3
            #VSlog(sUrl3)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl3', sUrl3)
            oOutputParameterHandler.addParameter('sMovieTitle2', sTitle2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addDir(SITE_IDENTIFIER, 'showMovies3', sTitle2, 'sport.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showMovies3(): #affiche les videos disponible du live
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl3 = oInputParameterHandler.getValue('siteUrl3')

    oRequestHandler = cRequestHandler(sUrl3)
    sHtmlContent = oRequestHandler.request()
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')

    sPattern = '<a title=".+?" *href="(.+?)"'
    oParser = cParser()

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = sMovieTitle2
            sUrl4 = aEntry
            sThumb = ''
            #sLang = aEntry[3]
            #sQual = aEntry[3]
            #sHoster = aEntry[2]
            #sDesc = ''

            sTitle = ('%s') % (sMovieTitle2)
            sUrl4 = "http:" + sUrl4

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl4', sUrl4)
            oOutputParameterHandler.addParameter('sMovieTitle2', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addDir(SITE_IDENTIFIER, 'showHosters', sTitle, 'sport.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters(): #affiche les videos disponible du live
    oGui = cGui()
    UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    oInputParameterHandler = cInputParameterHandler()
    sUrl4 = oInputParameterHandler.getValue('siteUrl4')
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl4)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<iframe.+?(?:allowFullScreen=|width).+?src="([^"]+)".+?</iframe>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0]):

        sHosterUrl = ''

        Referer =''
        url = aResult[1][0]

        #url = 'http://www.sporcanli.com/frame2.html' #a garder peut etre utils pour ajouter un hébergeur

        VSlog(url)

        if 'footballreal.xyz' in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern1 = '<iframe src="(.+?)"'
            aResult = re.findall(sPattern1, sHtmlContent2)
            if aResult:
                url = aResult[0]  # redirection vers un autre site
            
        if 'dailydeports.pw' in url:
            oRequestHandler = cRequestHandler(url)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', sUrl4)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<iframe src="(.+?)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                if 'cdnz.one' in aResult[0]:
                    url = aResult[0]  # redirection vers un autre site
            else:
                sPattern2 = 'str=\'(.+?)\''
                aResult = re.findall(sPattern2, sHtmlContent2)
                if aResult:
                    for aEntry in aResult:
                        aEntry=aEntry.replace('@', '')
                        data = bytearray.fromhex(aEntry).decode()
                        sPattern3 = '<iframe src="([^"]+)"'
                        aResult1 = re.findall(sPattern3, data)
                        if aResult1:
                            url = aResult1[0]  # redirection vers un autre site
                            break

        if 'emb.apl' in url:#Terminé - Supporte emb.aplayer et emb.apl3
            Referer = url
            oRequestHandler = cRequestHandler(url)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'source: *\'(.+?)\''
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0] + '|User-Agent=' + UA + '&referer=' + Referer
            else:
                sPattern2 = "pl.\init\('([^']+)'\);"
                aResult = re.findall(sPattern2, sHtmlContent2)
                if aResult:
                    sHosterUrl = aResult[0] + '|User-Agent=' + UA + '&referer=' + Referer
                
        if 'cdnz.one' in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern1 = '<iframe src=["\'](.+?)["\']'
            aResult = re.findall(sPattern1, sHtmlContent2)
            if aResult:
                Referer = url
                url = aResult[0]  # redirection vers un autre site
                
        if 'sport7.pw' in url or 'vip7stream' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'videoLink = \'(.+?)\''
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0] + '|User-Agent=' + UA + '&referer=' + url

        if 'totalsport.me' in url or 'airhdx' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            if (Referer):
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', Referer)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'source: ["\'](.+?)["\']'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0]

        if 'sportsbar.pw' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'videoLink = \'(.+?)\''
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0]

        if 'livesoccers.pw' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<iframe src=\'(.+?)\''
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl2 = aResult[0]
                oRequestHandler = cRequestHandler(sHosterUrl2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', sHosterUrl2)
                sHtmlContent3 = oRequestHandler.request()
                #VSlog(sHtmlContent3)
                sPattern3 = '<source src="([^"]+)"'
                aResult1 = re.findall(sPattern3, sHtmlContent3)
                if aResult1:
                    sHosterUrl = aResult1[0]

        if 'assia' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'file:"([^"]+)"|source: \'([^\']+)\''
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0][1]
            else:
                sPattern2 = '<source src=\'([^\']+)\''
                aResult = re.findall(sPattern2, sHtmlContent2)
                if aResult:
                    sHosterUrl = aResult[0]

        if 'sportlive.site' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<iframe src="(.+?)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl2 = aResult[0]
                #VSlog(str(sHosterUrl2))
                oRequestHandler = cRequestHandler(sHosterUrl2)
                sHtmlContent3 = oRequestHandler.request()
                sPattern3 = '<script type=\'text/javascript\'>id=\'(.+?)\''
                aResult2 = re.findall(sPattern3, sHtmlContent3)
                if aResult2:
                    sHosterUrl3 = aResult2[0]
                    sHosterUrl3 = "http://hdcast.pw/stream_jw2.php?id=" + sHosterUrl3
                    #VSlog(str(sHosterUrl3))
                    oRequestHandler = cRequestHandler(sHosterUrl3)
                    sHtmlContent4 = oRequestHandler.request()
                    sPattern4 = 'curl = "([^"]+)";'
                    aResult3 = re.findall(sPattern4, sHtmlContent4)
                    if aResult3:
                        sHosterUrl = aResult3[0]
                        sHosterUrl = base64.b64decode(sHosterUrl)
                        #VSlog(sHosterUrl)

        if 'stream365' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'var a[ 0-9]+="(.+?)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                gameId = int(aResult[2]) + int(aResult[0]) - int(aResult[1]) - int(aResult[2])
                sHosterUrl = 'http://91.192.80.210/edge0/xrecord/' + str(gameId) + '/prog_index.m3u8'

        if 'youtube' in url:#Je sais pas
            #dialog().VSinfo('Youtube peut ne pas marcher c\'est de la faute de Kodi', "Livetv", 15)
            sPattern2 = 'youtube.com/embed/(.+?)[?]autoplay=1'
            aResult = re.findall(sPattern2, url)

            if aResult:
                video_id = aResult[0]
                #VSlog(video_id)

                #url1 = url.replace('/embed/', '/watch?v=').replace('?autoplay=1', '')

                url2 = 'https://youtube.com/get_video_info?video_id=' + video_id + '&sts=17488&hl=fr'

                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                sHtmlContent3 = urllib2.unquote(oRequestHandler.request())

                sPattern3 = 'hlsManifestUrl":"(.+?)"'
                aResult = re.findall(sPattern3, sHtmlContent3)

                if aResult:
                    sHosterUrl = aResult[0] + '|User-Agent=' + UA + '&Host=manifest.googlevideo.com'

        if 'streamup.me' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<iframe src="([^"]+)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl2 = aResult[0]
                #VSlog(sHosterUrl2)
                oRequestHandler = cRequestHandler(sHosterUrl2)
                sHtmlContent3 = oRequestHandler.request()
                sHtmlContent3 = urllib.unquote(sHtmlContent3)
                #VSlog(sHtmlContent3)
                sPattern3 = 'src: "\/\/(.+?)"'
                aResult = re.findall(sPattern3, sHtmlContent3)
                if aResult:
                    sHosterUrl = 'http://' + aResult[0]

        if 'livestream' in url:#fixé
            sPattern2 = '<td bgcolor=".+?" *align="center".+?\s*<iframe.+?src="https://([^"]+)/player?.+?</iframe>'
            aResult = re.findall(sPattern2, sHtmlContent)
            if aResult:
                accountid = aResult[0]
                jsonUrl = 'https://player-api.new.' + accountid + '?format=short'
                oRequestHandler = cRequestHandler(jsonUrl)
                sHtmlContent = oRequestHandler.request()
                sPattern3 = '"m3u8_url":"(.+?)"'
                aResult = re.findall(sPattern3, sHtmlContent)
            if aResult:
                sHosterUrl = aResult[0]

        if 'forbet.tv' in url:#Probleme ssl
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'file: "([^"]+)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0]

        if 'p.hd24.watch' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'data-channel="([^"]+)">'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                Host = '190-2-146-56.livesports24.online'
                sHosterUrl = 'https://' + Host + '/' + aResult[0] + '.m3u8'

        if 'hdsoccerstreams.net' in url:#Pas terminer
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<script>fid="(.+?)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                fid = aResult[0]
                #VSlog(fid)

            url2 = 'http://webtv.ws/embed.php?live=spstream' + fid + '&vw=700&vh=440'
            Referer = url
            oRequestHandler = cRequestHandler(url2)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', Referer)
            sHtmlContent3 = oRequestHandler.request()
            #VSlog(sHtmlContent3)

        if 'thesports4u.net' in url or 'soccerstreams' in url:#Fini
            if 'thesports4u' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = oRequestHandler.request()
                sPattern2 = '<script>fid="(.+?)"'
                aResult = re.findall(sPattern2, sHtmlContent2)

                if aResult:
                    url2 = 'http://wlive.tv/embed.php?player=desktop&live=' + aResult[0] + '&vw=700&vh=440'
                    oRequestHandler = cRequestHandler(url2)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Referer', 'http://thesports4u.net/')
                    oRequestHandler.addHeaderEntry('Host', 'www.wlive.tv')
                    sHtmlContent3 = oRequestHandler.request()

            if 'soccerstreams' in url:
                oRequestHandler = cRequestHandler(url)
                sHtmlContent = oRequestHandler.request()
                url = url.replace('/hds', '/hdss/ch')

                oRequestHandler = cRequestHandler(url)
                sHtmlContent1 = oRequestHandler.request()
                sPattern = '<script>fid="(.+?)"'
                aResult = re.findall(sPattern, sHtmlContent1)

                if aResult:
                    url2 = 'http://wlive.tv/embedra.php?player=desktop&live=' + aResult[0] + '&vw=700&vh=440'
                    oRequestHandler = cRequestHandler(url2)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Referer', url)
                    oRequestHandler.addHeaderEntry('Host', 'www.wlive.tv')
                    sHtmlContent3 = oRequestHandler.request()

            m = re.search('return.*?\[(.*?)\].*?\+\s+(.*)\.join.*document.*?"(.*?)"', sHtmlContent3)
            if m:
                timeVar = m.group(2)
                hashVar = m.group(3)

                #http://tv.wlive.tv/tv/lu2mIWw6KZ20180321/playlist.m3u8?hlsendtime=1542297480&hlsstarttime=0&hlshash=jhTrgemr-kGm9E01YIVfqkZ9VPobibqbDRiov2psf_A=
                url3 = ''.join(m.group(1).split(','))
                url3 = 'http:' + url3.replace('"', '').replace('\/', '/')

                m = re.search(timeVar + '.*?\[(.*?)\]', sHtmlContent3)
                if m:
                    timeStr = ''.join(m.group(1).split(',')).replace('"', '')
                    url3 = url3 + timeStr

                m = re.search(hashVar + '>(.*?)<', sHtmlContent3)
                if m:
                    hashStr = ''.join(m.group(1).split(',')).replace('"', '')
                    url3 = url3 + hashStr
                    sHosterUrl = url3

        if 'sports-stream.net' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'sports-stream.+?ch=(.+?)"'
            aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:
                fid = aResult[0]
                url2 = 'http://webtv.ws/embeds.php?live=spstream' + fid + '&vw=700&vh=440'
                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', 'http://www.sports-stream.net/chtv/sps.php?ch=' + fid)
                sHtmlContent2 = oRequestHandler.request()
    
                sPattern3 = 'source src="(.+?)".+?">'
                aResult = re.findall(sPattern3, sHtmlContent2)
                if aResult:
                    sHosterUrl = aResult[0]

        if 'sports-stream.link' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'sports-stream.+?ch=(.+?)"'
            aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:
                fid = aResult[0]
                url2 = 'https://www.airhdx.com/embedd.php?live=spstream' + fid + '&vw=700&vh=440'
                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', 'http://www.sports-stream.link/chtv/sps.php?ch=' + fid)
                sHtmlContent2 = oRequestHandler.request()
    
                sPattern3 = 'source: "(.+?)",'
                aResult = re.findall(sPattern3, sHtmlContent2)
                if aResult:
                    sHosterUrl = aResult[0] + '|referer=' + url2

        if 'foot.futbol' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<iframe src=\'(.+?)\''
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl2 = aResult[0]
                #VSlog(sHosterUrl2)
                Referer = sHosterUrl2
                oRequestHandler = cRequestHandler(sHosterUrl2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', Referer)
                sHtmlContent3 = oRequestHandler.request()
                #VSlog(sHtmlContent3)
                sPattern3 = '<source src="([^"]+)"'
                aResult2 = re.findall(sPattern3, sHtmlContent3)
                if aResult2:
                    sHosterUrl = aResult2[0]

        if 'viewhd.me' in url:#Pas terminer je sais pas comment on trouve le m3u dans hdstream
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<script>fid="([^"]+)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl2 = 'http://www.hdstream.live/embed.php?player=desktop&live=' + aResult[0] + '&vw=620&vh=490'
                #VSlog(sHosterUrl2)
                Referer = sHosterUrl2
                oRequestHandler = cRequestHandler(sHosterUrl2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', Referer)
                sHtmlContent3 = oRequestHandler.request()
                #VSlog(sHtmlContent3)

        if 'socolive.net' in url:#Probleme avec ea et autre (tout changé lol)
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'channel=\'(.+?)\', g=\'(.+?)\''
            aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:
                for aEntry in aResult:
                    channel = aEntry[0]
                    g = aEntry[1]
                    #VSlog(channel)
                    #VSlog(g)

            url2 = 'https://www.ucasterplayer.com/hembedplayer/' + channel + '/' + g + '/700/480'
            #VSlog(url2)
            oRequestHandler = cRequestHandler(url2)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', 'http://socolive.net/ch=.+?')
            sHtmlContent2 = oRequestHandler.request()
            #VSlog(sHtmlContent2)

            sPattern3 = '"src", "https://" \+ ea \+ "([^"]+)"'
            sPattern4 = 'url: ".+?" \+ (.+?) \+'
            aResult2 = re.findall(sPattern4, sHtmlContent2)
            aResult1 = re.findall(sPattern3, sHtmlContent2)
            if aResult2:
                urldomaine = 'https://www.lquest123b.top/loadbalancer?' + aResult2[0] + '&'
                oRequestHandler = cRequestHandler(urldomaine)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', urldomaine)
                sHtmlContent3 = oRequestHandler.request()
                sPattern5 = 'redirect=(.+?top)'
                aResult3 = re.findall(sPattern5, sHtmlContent3)
                if aResult3:
                    domaine = aResult3[0]

            if aResult1:
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                Referer = url2
                sHosterUrl = 'https://' + domaine + aResult1[0] + '|User-Agent=' + UA + '&referer=' + Referer
                #VSlog(sHosterUrl)

        if 'socolive.xyz' in url or 'sportsfix' in url: #Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'iframe src="(.+?)"'
            aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:
                url2 = "http:" + aResult[0]
                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', url)
                sHtmlContent2 = oRequestHandler.request()

                sPattern2 = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
                aResult = re.findall(sPattern2, sHtmlContent2)

                if aResult:
                    str2 = aResult[0]
                    if not str2.endswith(';'):
                        str2 = str2 + ';'
    
                    strs = cPacker().unpack(str2)
                    sPattern3 = '{source:"([^"]+)"'
                    aResult1 = re.findall(sPattern3, strs)
                    if aResult1:
                        sHosterUrl = aResult1[0]
    
        if '1me.club' in url or 'sportz' in url or 'streamhd' in url or 'hdsportslive' in url or 'cricfree' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()

            if 'hdsportslive' in url or 'cricfree' in url:
                sPattern2 = 'document.write\(unescape\(\'(.+?)\'\)\)'
                aResult = re.findall(sPattern2, sHtmlContent2)
                unQuote = urllib2.unquote(aResult[0])

                sPattern2 = '<iframe.+?src="(.+?)"'
                aResult = re.findall(sPattern2, unQuote)

                if not str(aResult[0]).startswith('http'):
                    url = 'https:'+aResult[0]
                else:
                    url = aResult[0]

                oRequestHandler = cRequestHandler(url)
                sHtmlContent2 = oRequestHandler.request()

                sPattern2 = '<iframe.+?src=\'(.+?)\''
                aResult = re.findall(sPattern2, sHtmlContent2)

            else:
                sPattern2 = '<iframe src="(.+?)"'
                aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:

                if 'wstream.to' or 'streamcdn' in aResult[0]:#Terminé
                    embedUrl = aResult[0]
                    VSlog(embedUrl)

                    if embedUrl.startswith('//'):
                        embedUrl = 'https:' + embedUrl

                    if 'sportz' in url or 'hdsportslive' in url or 'cricfree' in url:
                        Referer = url
                    else:
                        Referer = 'http://1me.club'

                    #VSlog(aResult[0])
                    oRequestHandler = cRequestHandler(embedUrl)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Referer', Referer)
                    sHtmlContent3 = oRequestHandler.request()

                    sPattern2 = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
                    aResult = re.findall(sPattern2, sHtmlContent3)

                    if aResult:
                        str2 = aResult[0]
                    if not str2.endswith(';'):
                        str2 = str2 + ';'

                    strs = cPacker().unpack(str2)
                    sPattern3 = '{source:"([^"]+)"'
                    aResult1 = re.findall(sPattern3, strs)
                    if aResult1:
                        sHosterUrl = aResult1[0]

                if 'widestream.io' in aResult[0]:#Terminé
                    oRequestHandler = cRequestHandler(aResult[0])
                    sHtmlContent3 = oRequestHandler.request()
                    sPattern3 = 'file:"([^"]+)"'
                    aResult1 = re.findall(sPattern3, sHtmlContent3)
                    if aResult1:
                        sHosterUrl = aResult1[0]

        if 'sportlevel' in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = "manifestUrl: '(.+?)',"
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = 'http://d.sportlevel.com' + aResult[0]

        if ('shd' in url) or ('hd' in url and not 'streamhd' in url and not 'hdsportslive' in url and not 'airhdx' in url):
            urlApi = 'https://api.livesports24.online/gethost'
            channel = url.split('/')[4]

            oRequestHandler = cRequestHandler(urlApi)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', url)
            oRequestHandler.addHeaderEntry('Origin', 'https://'+url.split('/')[2])
            sHtmlContent2 = oRequestHandler.request()

            sPattern1 = '([^"]+)'
            aResult = re.findall(sPattern1, sHtmlContent2)
            if aResult:
                host = aResult[0]

            sHosterUrl = 'https://' + host + '/' + channel + '.m3u8'

        if 'sportgol7' in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern1 = '<source src="(.+?)"'
            aResult = re.findall(sPattern1, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0]

        if 'nowlive.pro' in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent3 = oRequestHandler.request()
            sPattern3 = 'src%3A%20%22//([^"]+)%3A([^"]+)m3u8'
            aResult1 = re.findall(sPattern3, sHtmlContent3)
            if aResult1:
                ip = aResult1[0][0]
                name = aResult1[0][1]
                sHosterUrl = 'http://'+ip+':'+name+'m3u8'

        if 'harleyquinn' in url: #Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'fid="(.+?)"; v_width=(.+?); v_height=(.+?);'
            aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:
                fid = aResult[0][0]
                vw=aResult[0][1]
                vh=aResult[0][2]

                url2 = 'http://www.jokerplayer.net/embed.php?u=' + fid + '&vw='+vw+'&vh='+vh
                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', url)
                sHtmlContent2 = oRequestHandler.request()
                sPattern3 = 'src=http://(.+?)/(.+?) '
                aResult = re.findall(sPattern3, sHtmlContent2)
                if aResult:
                    ip = aResult[0][0]
                    url3 = 'http://' + ip + '/' + aResult[0][1]
                    oRequestHandler = cRequestHandler(url3)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Referer', url2)
                    sHtmlContent2 = oRequestHandler.request()
                    sPattern3 = 'src=.+?e=(.+?)&st=(.+?)&'
                    aResult = re.findall(sPattern3, sHtmlContent2)
                    if aResult:
                        e = aResult[0][0]
                        st = aResult[0][1]
                        sHosterUrl = 'http://' + ip+'/live/'+fid + '.m3u8'+'?e='+e+'&st='+st

                if sHosterUrl == '':
                    url2 = 'http://player.jokehd.com/one.php?u=' + fid + '&vw='+vw+'&vh='+vh
                    oRequestHandler = cRequestHandler(url2)
                    oRequestHandler.addHeaderEntry('User-Agent', UA)
                    oRequestHandler.addHeaderEntry('Referer', url)
                    sHtmlContent2 = oRequestHandler.request()
                    sPattern3 = 'source: \'(.+?)\''
                    aResult = re.findall(sPattern3, sHtmlContent2)
                    if aResult:
                        sHosterUrl = aResult[0]

        if 'baltak.biz' in url: #Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<iframe src="\/blok.php\?id=(.+?)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                url2 = aResult[0]
                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', 'http://baltak.biz/blok.php?id=' + url2)
                sHtmlContent2 = oRequestHandler.request()

                sPattern2 = 'source: \'(.+?)\''
                aResult = re.findall(sPattern2, sHtmlContent2)
                if aResult:
                    sHosterUrl = aResult[0]
            else:
                sPattern2 = 'source: \"(.+?)\"'
                aResult = re.findall(sPattern2, sHtmlContent2)
                if aResult:
                    sHosterUrl = aResult[0]

        if 'footballstream' in url: #Terminé
            url = url.replace('/streams', '/hdstreams')
            oRequestHandler = cRequestHandler(url)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'fid="(.+?)"; v_width=(.+?); v_height=(.+?);'
            aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:
                fid = aResult[0][0]
                vw=aResult[0][1]
                vh=aResult[0][2]

                embedded = "mobile" # "desktop"

                url2 = 'http://www.b4ucast.me/embedra.php?player='+ embedded +'&live='+ fid +'&vw='+vw+'&vh='+vh
                oRequestHandler = cRequestHandler(url2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', url)
                sHtmlContent2 = oRequestHandler.request()

                sPattern3 = 'source: *["\'](.+?)["\']'
                aResult = re.findall(sPattern3, sHtmlContent2)
                if aResult:
                    sHosterUrl = 'http:'+aResult[0]

        if 'tennistvgroup' in url: #Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            
            print(sHtmlContent2)
            
            sPattern2 = 'source: *["\'](.+?)["\']'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0]

        if 'box-live.stream' in url: #Terminé
            oRequestHandler = cRequestHandler(url)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', sUrl4)

            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'source: \'(.+?)\''
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0] + '|User-Agent=' + UA + '&referer=' + url
            else:
                sPattern2 = 'var source = \"(.+?)\"'
                aResult = re.findall(sPattern2, sHtmlContent2)
                if aResult:
                    sHosterUrl = aResult[0]
                else:
                    sPattern2 = '<iframe.+?src="(http.+?)".+?</iframe>'
                    aResult = re.findall(sPattern2, sHtmlContent2)
                    if aResult:
                        Referer = url
                        url = aResult[0]    # decryptage plus bas (telerium)
            
        if 'telerium.tv' in url: #WIP
            oRequestHandler = cRequestHandler(url)
            if(Referer):
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', Referer)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
            aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:
                str2 = aResult[0]
                if not str2.endswith(';'):
                    str2 = str2 + ';'

                strs = cPacker().unpack(str2)
#                 print strs
#                fh = open('f:\\test.txt', "w")
#                fh.write(strs)
#                fh.close()

                sPattern3 = '{url:window\.atob\((.+?)\)\.slice.+?\+window\.atob\((.+?)\)'
                aResult1 = re.findall(sPattern3, strs)
                if aResult1:
                    m3u=aResult1[0][0]
                    sPatternM3u = m3u+'="(.+?)"'
                    m3u = re.findall(sPatternM3u, strs)
                    m3u = base64.b64decode(m3u[0])[14:]
                    
                    token=aResult1[0][1]
                    sPatterntoken = token+'="(.+?)"'
                    token = re.findall(sPatterntoken, strs)
                    token = base64.b64decode(token[0])

                    sHosterUrl = 'https://telerium.tv/'+m3u+token + '|referer='+url

        #TODO A TESTER
        if 'usasports.live' in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern1 = 'var sou = "  (.+?)"'
            aResult = re.findall(sPattern1, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0]

        #TODO A TESTER
        if 'wiz1' in url:
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern1 = '"iframe" src="(.+?)"'
            aResult = re.findall(sPattern1, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0]

        #TODO A TESTER
        if 'livesportone' in url :
            url = url.replace('livesportone.com', 'sportes.pw')
            
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<iframe src=\'(.+?)\''
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl2 = aResult[0] + '|User-Agent=' + UA + '&referer=' + url
                oRequestHandler = cRequestHandler(sHosterUrl2)
                oRequestHandler.addHeaderEntry('User-Agent', UA)
                oRequestHandler.addHeaderEntry('Referer', url)
                sHtmlContent3 = oRequestHandler.request()
#                 print(sHtmlContent3)
                sPattern3 = 'source: "([^"]+)"'
                aResult1 = re.findall(sPattern3, sHtmlContent3)
                if aResult1:
                    sHosterUrl = aResult1[0] + '|User-Agent=' + UA + '&referer=' + url

        if sHosterUrl:
            oHoster = cHosterGui().checkHoster("m3u8")
            if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle2) #nom affiche
                    oHoster.setFileName(sMovieTitle2) #idem
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        oGui.setEndOfDirectory()

def showMovies4(sSearch = ''):#Afficher le club recherché
    oGui = cGui()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)"><span class="sltitle">([^<>]+)</span></a>\s*<br>\s*<font color=".+?">([^<>]+)</font>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(str(aResult))

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[1]
            sUrl2 = aEntry[0]
            sThumb = ''
            #sLang = aEntry[3]
            #sQual = aEntry[4]
            sHoster = aEntry[2]
            sDesc = ''

            sTitle = sTitle.decode("iso-8859-1", 'ignore')
            sTitle = sTitle.encode("utf-8", 'ignore')
            sTitle = ('%s (%s)') % (sTitle, sHoster)

            sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMenu', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()

def showMenu(sSearch = ''):#affiche le menu du club
    oGui = cGui()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<a href="([^"]+)" *class="white">(.+?)</a></td>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(str(aResult))

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[1]
            sUrl2 = aEntry[0]
            sThumb = ''
            #sLang = aEntry[3]
            #sQual = aEntry[4]
            #sHoster = aEntry[2]
            sDesc = ''

            sTitle = sTitle.decode("iso-8859-1", 'ignore')
            sTitle = sTitle.encode("utf-8", 'ignore')
            sTitle = ('%s') % (sTitle)

            sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showResult', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()

def showResult(sSearch = ''):# le menu resultat quand on a choisi le club
    oGui = cGui()
    if sSearch:
        sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<span class="date">([^<>]+)</span>.+?<span class="graydesc">([^<>]+)</span>.+?<td align="right">([^<>]+).+?<td align="center">\s*<b>([^<>]+)</b>.+?<td>([^<>]+)</td>.+?<font color=".+?">.+?</font>.+?<a class="small" *href="([^"]+)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(str(aResult))

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sTitle = aEntry[2] + aEntry[4]
            sUrl2 = aEntry[5]
            sDate = aEntry[0]
            sComp = aEntry[1]
            sEquip = aEntry[2]
            sScore = aEntry[3]
            sEquipe = aEntry[4]
            sThumb = ''
            #sLang = aEntry[3]
            #sQual = aEntry[4]
            #sHoster = aEntry[2]
            sDesc = ''

            sTitle = sTitle.decode("iso-8859-1", 'ignore')
            sTitle = cUtil().unescape(sTitle)
            sTitle = sTitle.encode("utf-8", 'ignore')

            sDate = sDate.decode("iso-8859-1", 'ignore')
            sDate = cUtil().unescape(sDate)
            sDate = sDate.encode("utf-8", 'ignore')

            sScore = sScore.decode("iso-8859-1", 'ignore')
            sScore = cUtil().unescape(sScore)
            sScore = sScore.encode("utf-8", 'ignore')

            sComp = sComp.decode("iso-8859-1", 'ignore')
            sComp = cUtil().unescape(sComp)
            sComp = sComp.encode("utf-8", 'ignore')
            sTitle = ('%s  [%s] (%s) [COLOR]%s[/COLOR]]') % (sTitle, sScore, sDate, sComp)
            sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitlebis', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters2', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()

#def showDecode(): #les hosters des lives celui que je suis bloqué
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '.+?(http://.+?).+?'
    #urllib.unquote(sPattern)

    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(str(aResult))

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = str(aEntry)
            sHosterUrl = sHosterUrl.decode("iso-8859-1", 'ignore')
            #sHosterUrl = cUtil().unescape(sHosterUrl)
            sHosterUrl = sHosterUrl.encode("utf-8", 'ignore')
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle2)
                oHoster.setFileName(sMovieTitle2)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def showHosters2(): #Les hosters des videos (pas des lives attentions)
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitlebis = oInputParameterHandler.getValue('sMovieTitlebis')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<iframe.+?src="(http.+?)".+?</iframe>'

    aResult = oParser.parse(sHtmlContent, sPattern)
    #VSlog(str(aResult))

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry
            #sHosterUrl = sHosterUrl.decode("iso-8859-1", 'ignore')
            #sHosterUrl = cUtil().unescape(sHosterUrl)
            #sHosterUrl = sHosterUrl.encode("utf-8", 'ignore')
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitlebis)
                oHoster.setFileName(sMovieTitlebis)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
