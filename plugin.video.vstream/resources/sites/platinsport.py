# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Ovni-crea
import base64
import re
import xbmc

from resources.lib.comaddon import progress, isMatrix, siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.packer import cPacker
from resources.lib.parser import cParser
from resources.lib.util import cUtil, Unquote
from resources.lib.comaddon import VSlog, addon

try:
    import json
except:
    import simplejson as json

addons = addon()

SITE_IDENTIFIER = 'platinsport'
SITE_NAME = 'PlatinSport' + " " + addons.VSlang(350000)
SITE_DESC = 'Evénements sportifs en direct'

#URL_MAIN = 'https://www.platinsport.com/'
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

# SPORT_GENRES = (URL_MAIN + '/frx/allupcoming/', 'showMovies')  # Liste de diffusion des sports
SPORT_LIVE = (URL_MAIN + '', 'showLive')  # streaming Actif
SPORT_SPORTS = (True, 'load')


def load():
    oGui = cGui()
    
    oOutputParameterHandler = cOutputParameterHandler()

    #oOutputParameterHandler.addParameter('siteUrl', SPORT_GENRES[0])
    #oGui.addDir(SITE_IDENTIFIER, SPORT_GENRES[1], 'Les sports (Genres)', 'genres.png', oOutputParameterHandler)
    

    oOutputParameterHandler.addParameter('siteUrl', SPORT_LIVE[0] )
    oGui.addDir(SITE_IDENTIFIER, SPORT_LIVE[1], 'Les sports (En direct)', 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLive():
    VSlog(SITE_NAME+ ' - showLive - URL_MAIN'+ URL_MAIN)
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    VSlog(SITE_NAME + ' - showLive - puling: '+ sUrl)
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    #sPattern = '<a class="live" href="([^"]+)">([^<]+)<.a>\s*<br>\s*<a\s*class="live.+?span class="evdesc">([^<]+)'
    #sPattern = '<tr(.*?)ACESTREAM'
    #sPattern="<tr(.*?)<td>[^<](.*?)<(.*?)https(.*?)php(.*?)ACESTREAM"
    sPattern="<tr(.*?)</td><td>(.*?)<(.*?)https(.*?)php(.*?)ACESTREAM"
    
    
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        total = len(aResult[1])
        VSlog(SITE_NAME + ' - aResult[0] True, total:'+ str(total))

        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            for y, txt in enumerate(aEntry):
                VSlog(SITE_NAME + ' - ' + ' aEntry['+str(y)+']=' + txt + '. ')

            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl3 = "https" + aEntry[3] + "php"
            sTitle2 = aEntry[1]



#            try:
#                sTitle2 = sTitle2.decode("iso-8859-1", 'ignore')
#            except:
#                pass
#            sTitle2 = cUtil().unescape(sTitle2)
#            try:
#                sTitle2 = sTitle2.encode("utf-8", 'ignore')
#                sTitle2 = str(sTitle2, encoding="utf-8", errors='ignore')
#            except:
#                pass

            oOutputParameterHandler.addParameter('siteUrl3', sUrl3)
            oOutputParameterHandler.addParameter('sMovieTitle2', sTitle2)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies3', sTitle2, 'sport.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()



def showMovies3():  # affiche les videos disponible du live
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl3 = oInputParameterHandler.getValue('siteUrl3')

    VSlog(SITE_NAME + ' - showMovies3 - puling: '+ sUrl3)

    oRequestHandler = cRequestHandler(sUrl3)
    sHtmlContent = oRequestHandler.request()
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')


    
    sPattern="([A-Z]{2,2})\](.*?)(\r\n)(.*?)[\[<]"
    aMatches = re.compile(sPattern, re.MULTILINE | re.DOTALL).findall(sHtmlContent)
    
   
    if len(aMatches)<1:
        oGui.addText(SITE_IDENTIFIER)

    else:
        total=len(aMatches)
        VSlog(SITE_NAME + ' - aResult[0] True, total:'+ str(total))

        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()

        for y, txt in enumerate(aMatches):
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
        
            VSlog(txt )
    
            sPattern = "acestream://[a-z0-9]{10,}"
            aMatchesACE = re.compile(sPattern, re.MULTILINE).findall(txt[3])

            for aEntry in aMatchesACE:

                #for y, txt in enumerate(aEntry):
                #    VSlog(SITE_NAME + ' - showMovies3 - ' + ' aEntry['+str(y)+']=' + txt + '. ')

                sUrl4 = ''.join(aEntry)
                sMovieTitle2 = txt[0]+ " " + txt[1]
                sThumb = ''

                VSlog(SITE_NAME + ' - showMovies3 - ' + ' sUrl4=' + sUrl4 + '. sMovieTitle2 .' + sMovieTitle2 + '.')
                oOutputParameterHandler.addParameter('siteUrl4', sUrl4)
                oOutputParameterHandler.addParameter('sMovieTitle2', sMovieTitle2)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addDir(SITE_IDENTIFIER, 'showHosters', sMovieTitle2, 'sport.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showHosters():  # affiche les videos disponible du live
    oGui = cGui()
    #UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    oInputParameterHandler = cInputParameterHandler()
    streamurl = oInputParameterHandler.getValue('siteUrl4')
    sMovieTitle2 = oInputParameterHandler.getValue('sMovieTitle2')
    # sThumb = oInputParameterHandler.getValue('sThumb')

    # iHandler = cPluginHandler().getPluginHandle()

    if streamurl.count('sopcast') >0:
        #streamurl = urllib.quote_plus(streamurl)
        #lien = "ActivateWindow(10025,plugin://program.plexus/?url="+streamurl+"&mode=2&name=SportDevils)"
        lien = 'XBMC.RunPlugin(plugin://program.plexus/?url='+streamurl+'&mode=2&name='+sMovieTitle2+')'
        xbmc.executebuiltin( lien )

    if streamurl.count('acestream') > 0:
        #streamurl = urllib.quote_plus(streamurl)
        #lien = "ActivateWindow(10025,plugin://program.plexus/?url="+streamurl+"&mode=1&name=SportDevils)"
        lien = 'XBMC.RunPlugin(plugin://program.plexus/?url='+streamurl+'&mode=1&name='+sMovieTitle2+')'
        xbmc.executebuiltin( lien )

    # play_item = xbmcgui.ListItem(path=streamurl,label=sMovieTitle2)
    # play_item.setInfo(type="Video", infoLabels={"title": sMovieTitle2,'plot':sMovieTitle2})
    # xbmcplugin.setResolvedUrl(iHandler, True, listitem=play_item)
    



def getHosterVar16(url, referer):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'file:\"([^"]+)\"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return aResult[0] + '|referer=' + url

    sPattern = 'src=\"(.+?)\"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        referer = url
        url = 'http://var16.ru/' + aResult[0]
        return getHosterVar16(url, referer)


# Traitement générique
def getHosterIframe(url, referer):
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('Referer', referer)
    sHtmlContent = str(oRequestHandler.request())
    if not sHtmlContent:
        return False

    referer = url
    

    sPattern = '(\s*eval\s*\(\s*function(?:.|\s)+?{}\)\))'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        sstr = aResult[0]
        if not sstr.endswith(';'):
            sstr = sstr + ';'
        sHtmlContent = cPacker().unpack(sstr)

    sPattern = '.atob\("(.+?)"'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        import base64
        code = aResult[0]
        try:
            if isMatrix():
                code = base64.b64decode(code).decode('ascii')
            else:
                code = base64.b64decode(code)
#            return code + '|User-Agent=' + UA + '&Referer=' + Quote(referer)
            return code + '|Referer=' + referer
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
                    url = '//'+referer.split('/')[2] + url  # ajout du nom de domaine
                url = "https:" + url
            url = getHosterIframe(url, referer)
            if url:
                return url

    sPattern = ';var.+?src=["\']([^"\']+)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        url = aResult[0]
        if '.m3u8' in url:
            return url

    sPattern = '[^/]source.+?["\'](https.+?)["\']'
    aResult = re.findall(sPattern, sHtmlContent)
    if aResult:
        return aResult[0] + '|referer=' + referer

    return False


