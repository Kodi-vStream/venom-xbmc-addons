# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re, random, uuid, string
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler 
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, addon
from resources.lib.util import Quote

UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0"

SITE_IDENTIFIER = 'pluto_tv'
SITE_NAME = 'Pluto TV'
SITE_DESC = 'Chaine gratuite legal, VOD de programme divers'

URL_MAIN = 'https://api.pluto.tv'

CHAINE_DIRECT = (URL_MAIN + '/v2/channels.json?', 'showTV')
VOD = (URL_MAIN + '/v3/vod/categories?includeItems=true&deviceType=web', 'showGenre')

def getData():
    if addon().getSetting("PlutoTV_sid"):
        deviceID = addon().getSetting("PlutoTV_deviceID")
        clientID = addon().getSetting("PlutoTV_clientID")
        sid = addon().getSetting("PlutoTV_sid")

    else:
        sid = str(uuid.uuid1().hex)
        deviceID = str(uuid.uuid4().hex)
        clientID = Quote(''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + '=' + '+') for _ in range(24)))

        addon().setSetting("PlutoTV_deviceID", deviceID)
        addon().setSetting("PlutoTV_clientID", clientID)
        addon().setSetting("PlutoTV_sid", sid)
    return clientID, deviceID, sid

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', CHAINE_DIRECT[0])
    oGui.addDir(SITE_IDENTIFIER, CHAINE_DIRECT[1], 'Chaine en direct', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', VOD[0])
    oGui.addDir(SITE_IDENTIFIER, VOD[1], 'Programme disponible en VOD', 'search.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showTV():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    clientID, deviceID, sid = getData()

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent',UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    if (sHtmlContent):
        total = len(sHtmlContent)
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in sHtmlContent:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
        
            sThumb = aEntry["featuredImage"]["path"]
            sTitle = aEntry["name"]
            sUrl2 = "https://boot.pluto.tv/v4/start?deviceId=" + deviceID + "&deviceMake=Firefox&deviceType=web&deviceVersion=87.0&deviceModel=web&DNT=0&appName=web&appVersion=5.14.0-0f5ca04c21649b8c8aad4e56266a23b96d73b83a&serverSideAds=true&channelSlug=" + aEntry["slug"] + "&episodeSlugs=&clientID=" + clientID + "&clientModelNumber=na"
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('referer', sUrl)

            oGui.addDir(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showGenre():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent',UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    sID = 1
    if (sHtmlContent):
        total = len(sHtmlContent)
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in sHtmlContent["categories"]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
        
            sThumb = ''
            sTitle = aEntry["name"]
            sDesc = ''

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sID', int(sID))
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            sID = sID + 1

            oGui.addDir(SITE_IDENTIFIER, 'showVOD', sTitle, sThumb, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showVOD():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sID = oInputParameterHandler.getValue('sID')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent',UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    if (sHtmlContent):
        total = len(sHtmlContent["categories"][int(sID) - 1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in sHtmlContent["categories"][int(sID) - 1]["items"]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry["featuredImage"]["path"]
            sTitle = aEntry["name"]
            ids = aEntry["_id"]
            sDesc = aEntry["description"]

            oOutputParameterHandler.addParameter('sID', ids)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if aEntry["type"] == "series":
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif aEntry["type"] == "Anime":
                oGui.addAnime(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'seriesHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def ShowSerieSaisonEpisodes():
    oGui = cGui()
    oOutputParameterHandler = cOutputParameterHandler()

    oInputParameterHandler = cInputParameterHandler()
    sID = oInputParameterHandler.getValue('sID')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler("https://service-vod.clusters.pluto.tv/v3/vod/series/" + sID + "/seasons?includeItems=true&deviceType=web")
    oRequestHandler.addHeaderEntry('User-Agent',UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    if (sHtmlContent):
        total = len(sHtmlContent)
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in sHtmlContent["seasons"]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            
            for a in aEntry["episodes"]:
                sTitle = sMovieTitle + " S" + str(a["season"]) + " E" + str(a["number"])
                sID = a["_id"]

                oOutputParameterHandler.addParameter('sID', sID)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addEpisode(SITE_IDENTIFIER, 'seriesHosters', sTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)
                # il y a aussi addAnime pour les mangas
                # oGui.addAnime(SITE_IDENTIFIER, 'seriesHosters', sTitle, 'animes.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent',UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    sHosterUrl = "https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/" + sHtmlContent["startingChannel"]["id"] + "/master.m3u8?" + sHtmlContent["stitcherParams"]

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def seriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sID = oInputParameterHandler.getValue('sID')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')

    clientID, deviceID, sid = getData()

    sHosterUrl = "https://service-stitcher.clusters.pluto.tv/stitch/hls/episode/" + sID + "/master.m3u8?appName=web&appVersion=5.14.0-0f5ca04c21649b8c8aad4e56266a23b96d73b83a&deviceDNT=false&deviceId=" + deviceID + "&deviceMake=Firefox&deviceModel=web&deviceType=web&deviceVersion=87.0&includeExtendedEvents=false&marketingRegion=FR&sid=" + sid + "&serverSideAds=true"

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
