# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
import re
import string
import json
import time
import resources.sites.freebox


from resources.lib.packer import cPacker
from resources.lib.comaddon import addon, isMatrix
from resources.lib.epg import cePg
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil, Quote

from datetime import datetime, timedelta

SITE_IDENTIFIER = 'channelstream'
SITE_NAME = 'Channel Stream'
SITE_DESC = 'Chaines TV en directs'

URL_MAIN = "https://channelstream.watch"
SPORT_SPORTS = (True, 'load')
SPORT_LIVE = (URL_MAIN + '/programme.php', 'showMovies')

TV_FRENCH = (URL_MAIN + "/chaine-tv.php", 'showMovies')

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'


def load():
    oGui = cGui()

    liste = []
    liste.append(['Généraliste', 'Chaîne de télévision généraliste', 'tv.png', False])
    liste.append(['Cinéma', 'Chaîne consacrée aux Film', 'films.png', False])
    liste.append(['Sport', 'Chaîne Sportive', 'sport.png', False])
    liste.append(['Science et Nature', 'Chaîne axés sur les sciences', 'buzz.png', False])
    if addon().getSetting('contenu_adulte') == 'true':
        liste.append(['Adulte', 'Chaîne consacrée aux Film', 'buzz.png', True])

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_LIVE[1], 'Sports (En direct)', 'replay.png', oOutputParameterHandler)

    for sTitle, sFiltre, sIcon, bAdulte in liste:
        oOutputParameterHandler.addParameter('siteUrl', TV_FRENCH[0])
        oOutputParameterHandler.addParameter('sFiltre', sFiltre)
        oOutputParameterHandler.addParameter('bAdulte', bAdulte)
        oGui.addDir(SITE_IDENTIFIER, TV_FRENCH[1], sTitle, sIcon, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sFiltre = oInputParameterHandler.getValue('sFiltre')
    bAdulte = oInputParameterHandler.getValue('bAdulte')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    if isMatrix():
        sHtmlContent = sHtmlContent.replace('Ã®', 'î').replace('Ã©', 'é')

    if "programme" in sUrl:
        sPattern = "colspan='7'.+?<b>([^<]+)</b>.+?location\.href = '([^']+).+?text-align.+?>(.+?)</td>.+?src='([^']+).+?text-align.+?>([^<]+).+?text-align: left.+?>([^<]+)"
    else:
        sPattern = 'location.href = \'\.(.+?)\'.+?src=\'(.+?)\'.+?<div align="center">(.+?)</div>'
        sHtmlContent = oParser.abParse(sHtmlContent, sFiltre, '<!-- Type Chaîne -->')

    aResult = oParser.parse(sHtmlContent, sPattern)

    # try:
        # EPG = cePg().get_epg('', 'direct')
    # except:
        # EPG = ""

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            if "programme" in sUrl:
                sUrl2 = aEntry[1]
                sDate = aEntry[2].replace('<br />', ' ')
                sThumb = aEntry[3]
                sdesc1 = aEntry[4]
                sdesc2 = aEntry[5]

                sTitle = ''
                if sdesc1:
                    sTitle = sdesc1 + ' - ' + sdesc2 + ' - '
                sTitle += aEntry[0]
                if sDate:
                    try:
                        d = datetime(*(time.strptime(sDate, '%Hh%M %d-%m-%Y')[0:6]))
                        sDate = d.strftime("%d/%m/%y %H:%M")
                    except Exception as e:
                        pass
                    sTitle += ' - ' + sDate
                sDisplayTitle = sTitle
                sDesc = sDisplayTitle

            else:
                # Trie des chaines adultes
                if "+18" in str(aEntry[2]):
                    if not bAdulte:
                        continue
                elif bAdulte:
                    continue

                sTitle = aEntry[2]
                if "<" in sTitle:
                    sTitle = sTitle.split('<')[0]

                if 'Canal + Série' in sTitle:
                    sTitle = 'Canal + Séries'

                sUrl2 = URL_MAIN + aEntry[0]
                sThumb = URL_MAIN + '/' + aEntry[1]
#                sDesc = getEPG(EPG, sTitle)
                sDesc = sTitle
            
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if "programme" in sUrl:
                oGui.addMisc(SITE_IDENTIFIER, 'showHoster', sTitle, sThumb, sThumb, sDisplayTitle, oOutputParameterHandler)
            else:
                oGui.addMisc(SITE_IDENTIFIER, 'showHoster', sTitle, sThumb, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHoster():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = sTitle
    sCat = 6
    sMeta = 0

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    # try:
        # info = cePg().getChannelEpg(sTitle)
        # sDesc = info['plot']
        #
        # sMovieTitle = info['title']
        # if not sMovieTitle:
            # sMovieTitle = sTitle
            #
        # sMeta = 0
        # sCat = info['media_type']
        # if sCat:
            # if 'Film' in sCat:
                # sMeta = 1
            # if 'Série' in sCat:
                # sMeta = 2
        # sYear = info['year']
        # coverUrl = info['cover_url']
        # if coverUrl:
            # sThumb = coverUrl
    # except:
        # sMovieTitle = sTitle
        # info = ""
        # sYear = ""
        # coverUrl = sThumb
        # sDesc = ""
        # sMeta = 0

    # Double Iframe a passer.
    sPattern = '<iframe.+?src="([^"]+)" webkitallowfullscreen'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[1]:  # Pas de flux
        oGui.setEndOfDirectory()
        return

    for entry in aResult[1]:
        oOutputParameterHandler = cOutputParameterHandler()
        iframeURL1 = entry

        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumbnail', sThumb)
#        oOutputParameterHandler.addParameter('sYear', sYear)
        oOutputParameterHandler.addParameter('sDesc', sDesc)

        oGuiElement = cGuiElement()
        oGuiElement.setTitle(sMovieTitle)
        oGuiElement.setDescription(sDesc)
        oGuiElement.setFileName(sMovieTitle)
        oGuiElement.setSiteName(resources.sites.freebox.SITE_IDENTIFIER)
        oGuiElement.setFunction('play__')
        oGuiElement.setIcon('tv.png')
        oGuiElement.setMeta(sMeta)
        oGuiElement.setThumbnail(sThumb)
        oGuiElement.setDirectTvFanart()
        oGuiElement.setCat(sCat)
        oGuiElement.setMeta(sMeta)

        # oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, resources.sites.freebox.SITE_IDENTIFIER, SITE_IDENTIFIER, 'direct_epg', 'Guide tv Direct')
        # oGui.CreateSimpleMenu(oGuiElement, oOutputParameterHandler, resources.sites.freebox.SITE_IDENTIFIER, SITE_IDENTIFIER, 'soir_epg', 'Guide tv Soir')
        if addon().getSetting('enregistrement_activer') == 'true':
            oGui.createSimpleMenu(oGuiElement, oOutputParameterHandler, resources.sites.freebox.SITE_IDENTIFIER, SITE_IDENTIFIER, 'enregistrement', 'Enregistrement')

        # Menu pour les films
        if sCat == 1:
            oGui.createContexMenuinfo(oGuiElement, oOutputParameterHandler)
            oGui.createContexMenuba(oGuiElement, oOutputParameterHandler)
            oGui.createContexMenuSimil(oGuiElement, oOutputParameterHandler)
            oGui.createContexMenuWatch(oGuiElement, oOutputParameterHandler)

        if 'dailymotion' in iframeURL1:
            oOutputParameterHandler.addParameter('sHosterIdentifier', 'dailymotion')
            oOutputParameterHandler.addParameter('sMediaUrl', iframeURL1)
            oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
            oOutputParameterHandler.addParameter('sFileName', sMovieTitle)
            oGuiElement.setFunction('play')
            oGuiElement.setSiteName('cHosterGui')
            oGui.addHost(oGuiElement, oOutputParameterHandler)
            cGui.CONTENT = 'movies'
            oGui.setEndOfDirectory()
            return

        elif "telerium" in iframeURL1:
            oRequestHandler = cRequestHandler(iframeURL1)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Referer', iframeURL)
            sHtmlContent2 = oRequestHandler.request()

            if sHtmlContent2:
                sPattern2 = 'var\s+cid[^\'"]+[\'"]{1}([0-9]+)'
                aResult2 = re.findall(sPattern2, sHtmlContent2)

                if aResult2:
                    str2 = aResult2[0]
                    datetoken = int(getTimer()) * 1000

                    jsonUrl = 'https://telerium.digital/streams/' + str2 + '/' + str(datetoken) + '.json'
                    tokens = getRealTokenJson(jsonUrl, iframeURL1)
                    m3url = tokens['url']
                    nxturl = 'https://telerium.digital' + tokens['tokenurl']

                    realtoken = getRealTokenJson(nxturl, iframeURL1)[10][::-1]

                    try:
                        m3url = m3url.decode("utf-8")
                    except:
                        pass

                    sHosterUrl = 'https:' + m3url + realtoken + '|User-Agent=' + UA
                    sHosterUrl += '&Referer=' + Quote(iframeURL1) + '&Sec-Fetch-Mode=cors&Origin=https://telerium.tv'
            else:
                sHosterUrl = ""

        elif "channel.stream" in iframeURL1:
            oRequestHandler = cRequestHandler(iframeURL1)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            # oRequestHandler.addHeaderEntry('Referer', siterefer) # a verifier
            sHtmlContent = oRequestHandler.request()

            sHosterUrl = ''
            oParser = cParser()
            sPattern = '<iframe.+?src="([^"]+)'
            aResult2 = oParser.parse(sHtmlContent, sPattern)
            try:
                # Lien telerium qui ne marche pas
                # Mais qui n'est pas toujours present
                iframeURL1 = aResult2[1][1]
            except:
                iframeURL1 = aResult2[1][0]

        if 'allfoot' in iframeURL1 or "sportsonline" in iframeURL1:
            oRequestHandler = cRequestHandler(iframeURL1)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            # oRequestHandler.addHeaderEntry('Referer', siterefer) # a verifier
            sHtmlContent = oRequestHandler.request()

            oParser = cParser()
            sPattern = '<iframe.+?src="([^"]+)'
            aResult2 = oParser.parse(sHtmlContent, sPattern)

            if aResult2[1]:
                for stream in aResult2[1]:
                    if 'ragnarp' in stream or 'wigistream' in stream or 'worlwidestream' in stream:
                        sHosterUrl = Hoster_Wigistream(stream, iframeURL1)
                        if sHosterUrl:
                            oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
                            oGui.addFolder(oGuiElement, oOutputParameterHandler)

    cGui.CONTENT = 'movies'
    oGui.setEndOfDirectory()


def Hoster_Wigistream(url, referer):
    url = url.strip()
    if not url.startswith('http'):
        url = 'http:'+url
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = oRequestHandler.request()

    sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    aResult = re.findall(sPattern, sHtmlContent)

    if aResult:
        sstr = aResult[0]
        if not sstr.endswith(';'):
            sstr = sstr + ';'
        sUnpack = cPacker().unpack(sstr)
        sPattern = 'src="(.+?)"'
        aResult = re.findall(sPattern, sUnpack)
        if aResult:
            return aResult[0] + '|User-Agent=' + UA + '&Referer=' + Quote(url)

    return False


def getRealTokenJson(link, referer):
    # cookies = {'elVolumen': '100', '__ga': '100'}

    # headers = {'Host': 'telerium.tv',
               # 'User-Agent': UA, 'Accept': 'application/json, text/javascript, */*; q=0.01',
               # 'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3', 'X-Requested-With': 'XMLHttpRequest',
               # 'Referer': referer}

    oRequestHandler = cRequestHandler(link)
    # oRequestHandler.addHeaderEntry('Host', 'telerium.tv')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    # oRequestHandler.addHeaderEntry('Accept', 'application/json, text/javascript, */*; q=0.01')
    oRequestHandler.addHeaderEntry('Accept-Language', 'pl,en-US;q=0.7,en;q=0.3')
    oRequestHandler.addHeaderEntry('X-Requested-With', 'XMLHttpRequest')
    oRequestHandler.addHeaderEntry('Referer', referer)
    oRequestHandler.addCookieEntry('elVolumen', '100')
    oRequestHandler.addCookieEntry('__ga', '100')
    realResp = oRequestHandler.request()
    return json.loads(realResp)


def getTimer():
    datenow = datetime.utcnow().replace(second=0, microsecond=0)
    datenow = datenow + timedelta(days=1)
    epoch = datetime(1970, 1, 1)

    return (datenow - epoch).total_seconds() // 1


def getEPG(EPG, sTitle):

    oParser = cParser()

    sTitle = sTitle.replace('+', 'plus')

    try:
        sTitle = cUtil().CleanName(sTitle)
    except:
        pass

    sTitle = re.sub('[^%s]' % (string.ascii_lowercase + string.digits), '', sTitle.lower())

    sPattern = '(.+?)\/>(.+?)<'
    aResult = oParser.parse(EPG, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sChannel = aEntry[0]

            sChannel = re.sub('[^%s]' % (string.ascii_lowercase + string.digits), '', sChannel.lower())
            if sChannel == sTitle:
                sDesc = aEntry[1].replace('[COLOR khaki]', '\r\n\t[COLOR khaki]')
                sDesc = sDesc.replace('[/COLOR]', '[/COLOR]\r\n')
                return sDesc

    return ''
