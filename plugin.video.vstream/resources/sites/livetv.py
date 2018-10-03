#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Ovni-crea
from resources.lib.gui.hoster import cHosterGui #systeme de recherche pour l'hote
from resources.lib.gui.gui import cGui #systeme d'affichage pour xbmc
from resources.lib.handler.inputParameterHandler import cInputParameterHandler #entree des parametres
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler #sortie des parametres
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.parser import cParser #recherche de code
from resources.lib.comaddon import progress, VSlog, xbmc #import du dialog progress
from resources.lib.util import cUtil #import du plugin cUtil
import re,urllib,urllib2
import base64

from resources.lib.packer import cPacker

SITE_IDENTIFIER = 'livetv'
SITE_NAME = 'Livetv.sx (beta)'
SITE_DESC = 'Site pour regarder du sport en direct gratuitement'

URL_MAIN = 'http://livetv.sx'
URL_MAIN2 = 'http://cdn.livetvcdn.net'
URL_SEARCH = (URL_MAIN + '/frx/fanclubs/?q=', 'showMovies4')
FUNCTION_SEARCH = 'showMovies4'

SPORT_SPORTS = (URL_MAIN + '/frx/allupcoming/', 'showMovies') #Les matchs en directs
#SPORT_SPORTSCLASS = (URL_MAIN + '/frx/calendar/411/', 'showClass')# Les classements
NETS_GENRES = (True, 'showGenres') #Les clubs de football
UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0 (Chrome)'

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher l équipe', 'search.png', oOutputParameterHandler)

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

def showMovies(sSearch = ''):#affiche les catégories qui on des lives'
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

            sTitle = str(aEntry[1])
            sTitle = sTitle.decode("iso-8859-1", 'ignore')
            sTitle = cUtil().unescape(sTitle)
            sTitle = sTitle.encode("utf-8", 'ignore')
            sUrl2 = str(aEntry[0])
            sThumb = ''
            #sLang = str(aEntry[3])
            #sQual = str(aEntry[4])
            sHoster = str(aEntry[2])
            sDesc = ''

            sTitle = sTitle.decode("iso-8859-1", 'ignore')
            sTitle = sTitle.encode("utf-8", 'ignore')
            sTitle = ('%s (%s)') % (sTitle, sHoster)
            sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl2', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showMovies2', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()

def showMovies2(sSearch = ''): #affiche les matchs en direct depuis la section showMovie
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl2 = oInputParameterHandler.getValue('siteUrl2')

    oRequestHandler = cRequestHandler(sUrl2)
    sHtmlContent = oRequestHandler.request()
    #VSlog(sHtmlContent)

    sPattern = '<a class="live" href="([^>]+)">([^>]+)</a>\s*(?:<br><img src="//cdn.livetvcdn.net/img/live.gif"><br>|<br>)\s*<span class="evdesc">([^>]+)\s*<br>\s*([^>]+)</span>'

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

            sTitle2 = str(aEntry[1]).replace('<br>',' ')
            sUrl3 = str(aEntry[0])
            sThumb = ''
            #sLang = str(aEntry[3])
            sQual = str(aEntry[3])
            sHoster = str(aEntry[2])
            sDesc = ''

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
            VSlog(sUrl3)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl3', sUrl3)
            oOutputParameterHandler.addParameter('sMovieTitle2', sTitle2)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showMovies3', sTitle2, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()

def showMovies3(sSearch = ''): #affiche les videos disponible du live
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl3 = oInputParameterHandler.getValue('siteUrl3')

    oRequestHandler = cRequestHandler(sUrl3)
    sHtmlContent = oRequestHandler.request()
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')

    sPattern = '<a title=".+?" *href="//cdn.livetvcdn.net(.+?)"'
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

            sTitle = sMovieTitle2
            sUrl4 = str(aEntry)
            sThumb = ''
            #sLang = str(aEntry[3])
            #sQual = str(aEntry[3])
            #sHoster = str(aEntry[2])
            sDesc = ''

            sTitle = ('%s') % (sMovieTitle2)
            sUrl4 = URL_MAIN2 + sUrl4

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl4', sUrl4)
            oOutputParameterHandler.addParameter('sMovieTitle2', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        oGui.setEndOfDirectory()

def showHosters(sSearch = ''): #affiche les videos disponible du live
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl4 = oInputParameterHandler.getValue('siteUrl4')
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl4)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    if not 'aliez' in sUrl4:
        sPattern = '<td bgcolor=".+?" *align="center".+?\s*<iframe.+?src="([^"]+)".+?</iframe>'
    elif 'youtube' or 'aliez' or 'laola1tv' in sUrl4:
        sPattern = '</script>\s*<iframe.+?src="([^"]+)".+?</iframe>\s*</td>'
    else:
        sPattern = '<td bgcolor=".+?" *align="center".+?\s*<iframe.+?src="([^"]+)".+?</iframe>'

    liste_url = []

    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0]):

        sHosterUrl = ''

        url = aResult[1][0]
        
        #url = 'http://www.sporcanli.com/frame2.html' #a garder peut etre utils pour ajouter un hébergeur
        
        VSlog(url)
        if 'emb.aliez.me' in url:#Terminer
        	Referer = url
        	UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
        	oRequestHandler = cRequestHandler(url)
        	oRequestHandler.addHeaderEntry('User-Agent',UA)
        	sHtmlContent2 = oRequestHandler.request()
        	sPattern2 = 'source: *\'(.+?)\''
        	aResult = re.findall(sPattern2, sHtmlContent2)
        	if aResult:
        		sHosterUrl = aResult[0] + '|User-Agent=' + UA + '&referer=' + Referer
        		VSlog(sHosterUrl)
        		
        if 'emb.aliez.me' in url:#obligatoire pour fixer bug 403
        	UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
        	oRequestHandler = cRequestHandler(url)
        	oRequestHandler.addHeaderEntry('User-Agent',UA)
        	sHtmlContent2 = oRequestHandler.request()
        	sPattern2 = 'source: *\'(http://a3.aliez.me.+?)\''
        	aResult = re.findall(sPattern2, sHtmlContent2)
        	if aResult:
        		sHosterUrl = aResult[0] + '|User-Agent=' + UA 
        		VSlog(sHosterUrl)

        if 'sport7.pw' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'videoLink = \'(.+?)\''
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult:
                sHosterUrl = aResult[0]

        if 'totalsport.me' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'source: "(.+?)"'
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
        		UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
        		oRequestHandler = cRequestHandler(sHosterUrl2)
        		oRequestHandler.addHeaderEntry('User-Agent',UA)
        		oRequestHandler.addHeaderEntry('Referer',sHosterUrl2)
        		sHtmlContent3 = oRequestHandler.request()
        		#VSlog(sHtmlContent3)
        		sPattern3 = '<source src="([^"]+)"'
        		aResult1 = re.findall(sPattern3, sHtmlContent3)
        		if aResult1:
        			sHosterUrl = aResult1[0]
        		
        if 'assia' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = 'file:"([^"]+)"'
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
        				VSlog(sHosterUrl)

        if 'sport-stream365' in url:#Terminé
            sPattern2 = '<td bgcolor=".+?" *align="center".+?\s*<iframe.+?src="http://sport-stream365.com.+?/?game=([^"]+)&ta.+?".+?</iframe>'
            aResult = re.findall(sPattern2, sHtmlContent)
            if aResult:
                gameId = aResult[0]
                sHosterUrl = 'http://91.192.80.210/edge0/xrecord/' + gameId + '/prog_index.m3u8'

        if 'youtube' in url:#Je sais pas
            sPattern2 = 'youtube.com/embed/(.+?)[?]autoplay=1'
            aResult = re.findall(sPattern2, url)

            if aResult:
                video_id = aResult[0]
                VSlog(video_id)

            url = url.replace('/embed/','/watch?v=')
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()

            sPattern2 = '\W[\'"]?t[\'"]?: ?[\'"](.+?)[\'"]'
            aResult = re.findall(sPattern2, sHtmlContent2)

            if aResult:
                token = aResult[0]
                #VSlog(token)

            params = {
                'video_id': video_id,
                'el': '$el',
                'ps': 'default',
                'eurl': 'https://youtube.googleapis.com/v/'+video_id,
                'hl': 'fr_FR',
                't': urllib2.quote(token)}

            url2 = 'https://youtube.com/get_video_info?video_id=' +video_id#+ urllib.parse.urlencode(params)

            req = urllib2.Request(url2)

            response = urllib2.urlopen(req)
            sHtmlContent3 = response.read().decode('utf-8')
            #VSlog(sHtmlContent3)

            sPattern3 = '&hlsvp=(.+?).m3u8.+?'
            aResult = re.findall(sPattern3, sHtmlContent3)

            if aResult:
                sHosterUrl = urllib2.unquote(aResult[0])
                sHosterUrl = urllib2.unquote(sHosterUrl)
                sHosterUrl = sHosterUrl + '.m3u8'
                #VSlog(sHosterUrl)
            
        if 'streamup.me' in url:#Terminé
        	oRequestHandler = cRequestHandler(url)
        	sHtmlContent2 = oRequestHandler.request()
        	sPattern2 = '<iframe src="([^"]+)"'
        	aResult = re.findall(sPattern2, sHtmlContent2)
        	if aResult:
        		sHosterUrl2 = aResult[0]
        		VSlog(sHosterUrl2)
        		oRequestHandler = cRequestHandler(sHosterUrl2)
        		sHtmlContent3 = oRequestHandler.request()
        		sHtmlContent3 = urllib.unquote(sHtmlContent3)
        		VSlog(sHtmlContent3)
        		sPattern3 = 'src: "\/\/(.+?)"'
        		aResult = re.findall(sPattern3, sHtmlContent3)
        		if aResult:
        			sHosterUrl = 'http://'+aResult[0]

        if 'livestream' in url:#Je sais pas ne démarre pas de temps en temps
            sPattern2 = '<td bgcolor=".+?" *align="center".+?\s*<iframe.+?src="https://([^"]+)/player?.+?</iframe>'
            aResult = re.findall(sPattern2, sHtmlContent)
            if aResult:
            	accountId = aResult[0]
            jsonUrl = 'https://player-api.new.' + accountId + '?format=short'

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
        		sHosterUrl = 'https://'+Host+'/'+aResult[0]+'.m3u8' 
        		
        if 'hdsoccerstreams.net' in url:#Pas terminer
        	oRequestHandler = cRequestHandler(url)
        	sHtmlContent2 = oRequestHandler.request()
        	sPattern2 = '<script>fid="(.+?)"'
        	aResult = re.findall(sPattern2, sHtmlContent2)
        	if aResult:
        		fid = aResult[0]
        		VSlog(fid)
        		
        	UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
        	url2 = 'http://webtv.ws/embed.php?live=spstream'+ fid +'&vw=700&vh=440'
        	Referer = url
        	oRequestHandler = cRequestHandler(url2)
        	oRequestHandler.addHeaderEntry('User-Agent',UA)
        	oRequestHandler.addHeaderEntry('Referer',Referer)
        	sHtmlContent3 = oRequestHandler.request()
        	#VSlog(sHtmlContent3)
        	
        if 'thesports4u.net' in url:#Pas terminer leurs hosters est down (erreur 404)
        	oRequestHandler = cRequestHandler(url)
        	sHtmlContent2 = oRequestHandler.request()
        	sPattern2 = '<script>fid="(.+?)"'
        	aResult = re.findall(sPattern2, sHtmlContent2)
        	if aResult:
        		fid = aResult[0]
        		VSlog(fid)
        		
        	UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
        	url2 = 'http://wlive.tv/embed.php?player=desktop&live='+fid+'&vw=700&vh=440'
        	oRequestHandler = cRequestHandler(url2)
        	oRequestHandler.addHeaderEntry('User-Agent',UA)
        	oRequestHandler.addHeaderEntry('Referer',url2)
        	sHtmlContent3 = oRequestHandler.request()
        	VSlog(sHtmlContent3)
        	
       	
        if 'sports-stream.net' in url:#Terminé
           oRequestHandler = cRequestHandler(url)
           sHtmlContent2 = oRequestHandler.request()
           sPattern2 = 'sports-stream.+?ch=(.+?)"'
           aResult = re.findall(sPattern2, sHtmlContent2)

           if aResult:
               fid = aResult[0]

           UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
           url2 = 'http://webtv.ws/embeds.php?live=spstream'+ fid +'&vw=700&vh=440'
           oRequestHandler = cRequestHandler(url2)
           oRequestHandler.addHeaderEntry('User-Agent',UA)
           oRequestHandler.addHeaderEntry('Referer','http://www.sports-stream.net/chtv/sps.php?ch='+fid)
           sHtmlContent2 = oRequestHandler.request()

           sPattern3 = 'source src="(.+?)".+?">'
           aResult = re.findall(sPattern3, sHtmlContent2)
           if aResult:
               sHosterUrl = aResult[0]
               
        if 'foot.futbol' in url:#Terminé
        	oRequestHandler = cRequestHandler(url)
        	sHtmlContent2 = oRequestHandler.request()
        	sPattern2 = '<iframe src=\'(.+?)\''
        	aResult = re.findall(sPattern2, sHtmlContent2)
        	if aResult:
        		sHosterUrl2 = aResult[0]
        		VSlog(sHosterUrl2)
        		Referer = sHosterUrl2
        		UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        		oRequestHandler = cRequestHandler(sHosterUrl2)
        		oRequestHandler.addHeaderEntry('User-Agent',UA)
        		oRequestHandler.addHeaderEntry('Referer',Referer)
        		sHtmlContent3 = oRequestHandler.request()
        		VSlog(sHtmlContent3)
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
        		sHosterUrl2 = 'http://www.hdstream.live/embed.php?player=desktop&live='+aResult[0]+'&vw=620&vh=490'
        		VSlog(sHosterUrl2)
        		Referer = sHosterUrl2
        		UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        		oRequestHandler = cRequestHandler(sHosterUrl2)
        		oRequestHandler.addHeaderEntry('User-Agent',UA)
        		oRequestHandler.addHeaderEntry('Referer',Referer)
        		sHtmlContent3 = oRequestHandler.request()
        		VSlog(sHtmlContent3)
        	

        #if 'socolive.net' in url:#Probleme avec ea et autre (tout changé lol)
            #oRequestHandler = cRequestHandler(url)
            #sHtmlContent2 = oRequestHandler.request()
            #sPattern2 = 'channel=\'(.+?)\', g=\'(.+?)\''
            #aResult = re.findall(sPattern2, sHtmlContent2)
            #VSlog(aResult)

            #if aResult:
                #for aEntry in aResult:
                    #channel = aEntry[0]
                    #g = aEntry[1]
                    #VSlog(channel)
                    #VSlog(g)

            #UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
            #url2 = 'https://www.ucasterplayer.com/hembedplayer/'+ channel +'/'+ g +'/700/480'
            #VSlog(url2)
            #oRequestHandler = cRequestHandler(url2)
            #oRequestHandler.addHeaderEntry('User-Agent',UA)
            #oRequestHandler.addHeaderEntry('Referer','http://socolive.net/ch=.+?')
            #sHtmlContent2 = oRequestHandler.request()
            #VSlog(sHtmlContent2)
            
            #sPattern3 = '"src", "https://" \+ ea \+ "([^"]+)"'
            #sPattern4 = 'ea = "([^"]+)"'
            #aResult2 = re.findall(sPattern4, sHtmlContent2)
            #aResult1 = re.findall(sPattern3, sHtmlContent2)
            #if aResult2:
                #urldomaine = aResult2[0]
                #VSlog(urldomaine)
            #if aResult1:
                #oRequestHandler.addHeaderEntry('User-Agent',UA)
                #Referer = url2
                #UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
                #sHosterUrl = 'http://'+ 'p15.quest123.top' + aResult1[0] + '|User-Agent=' + UA + '&referer=' + Referer
                #VSlog(sHosterUrl)

        if '1me.club' in url:#Terminé
            oRequestHandler = cRequestHandler(url)
            sHtmlContent2 = oRequestHandler.request()
            sPattern2 = '<iframe src="(.+?)"'
            aResult = re.findall(sPattern2, sHtmlContent2)
            if aResult[0]:
            	
            	if 'whostreams.net' in aResult[0]:#Terminé
            		Referer = 'http://1me.club'
                	UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
                	VSlog(aResult[0])
                	oRequestHandler = cRequestHandler(aResult[0])
                	oRequestHandler.addHeaderEntry('User-Agent',UA)
                	oRequestHandler.addHeaderEntry('Referer',Referer)              
                	sHtmlContent3 = oRequestHandler.request()
                
                	sPattern2 = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
                	aResult = re.findall(sPattern2, sHtmlContent3)
                
                	if aResult:
                		str2 = aResult[0]
                	if not str2.endswith(';'):
                		str2 = str2 + ';'
                		
                	str = cPacker().unpack(str2)
                	VSlog(str)
                	sPattern3 = '{source:"([^"]+)"'
                	aResult1 = re.findall(sPattern3, str)
                	if aResult1:
                		sHosterUrl = aResult1[0]
                		
                if 'widestream.io' in aResult[0]:#Terminé
                	oRequestHandler = cRequestHandler(aResult[0])
                	sHtmlContent3 = oRequestHandler.request()
                	sPattern3 = 'file:"([^"]+)"'
                	aResult1 = re.findall(sPattern3, sHtmlContent3)
                	if aResult1:
                		sHosterUrl = aResult1[0]
          	
        #VSlog(sHosterUrl)
        xbmc.Player().play(sHosterUrl)
        return

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

            sTitle = str(aEntry[1])
            sUrl2 = str(aEntry[0])
            sThumb = ''
            #sLang = str(aEntry[3])
            #sQual = str(aEntry[4])
            sHoster = str(aEntry[2])
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

            sTitle = str(aEntry[1])
            sUrl2 = str(aEntry[0])
            sThumb = ''
            #sLang = str(aEntry[3])
            #sQual = str(aEntry[4])
            #sHoster = str(aEntry[2])
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

            sTitle = str(aEntry[2])  + str(aEntry[4])
            sUrl2 = str(aEntry[5])
            sDate = str(aEntry[0])
            sComp = str(aEntry[1])
            sEquip = str(aEntry[2])
            sScore = str(aEntry[3])
            sEquipe = str(aEntry[4])
            sThumb = ''
            #sLang = str(aEntry[3])
            #sQual = str(aEntry[4])
            #sHoster = str(aEntry[2])
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
    VSlog(str(aResult))

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

            sHosterUrl = str(aEntry)
            #sHosterUrl = sHosterUrl.decode("iso-8859-1", 'ignore')
            #sHosterUrl = cUtil().unescape(sHosterUrl)
            #sHosterUrl = sHosterUrl.encode("utf-8", 'ignore')
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitlebis)
                oHoster.setFileName(sMovieTitlebis)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
