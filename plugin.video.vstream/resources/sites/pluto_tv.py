# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import random
import string
import uuid

from resources.lib.comaddon import progress, addon, isMatrix, siteManager
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.util import Quote

UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0"

SITE_IDENTIFIER = 'pluto_tv'
SITE_NAME = 'Pluto TV'
SITE_DESC = 'Chaine gratuite légal, VOD de programme divers'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

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
        clientID = Quote(''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + '=+') for _ in range(24)))

        addon().setSetting("PlutoTV_deviceID", deviceID)
        addon().setSetting("PlutoTV_clientID", clientID)
        addon().setSetting("PlutoTV_sid", sid)

    return clientID, deviceID, sid


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', CHAINE_DIRECT[0])
    oGui.addDir(SITE_IDENTIFIER, CHAINE_DIRECT[1], 'Chaines en direct', 'tv.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', VOD[0])
    oGui.addDir(SITE_IDENTIFIER, VOD[1], 'Programmes disponibles en VOD', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showTV():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    clientID, deviceID, sid = getData()

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    if sHtmlContent:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in sHtmlContent:
            sThumb = aEntry["featuredImage"]["path"]
            sTitle = aEntry["name"]
            if not isMatrix():
                sTitle = sTitle.encode('utf8')

            sUrl2 = "https://boot.pluto.tv/v4/start?deviceId=" + deviceID
            sUrl2 += "&deviceMake=Firefox&deviceType=web&deviceVersion=87.0&deviceModel=web&DNT=0&appName=web"
            sUrl2 += "&appVersion=5.14.0-0f5ca04c21649b8c8aad4e56266a23b96d73b83a&serverSideAds=true&channelSlug="
            sUrl2 += aEntry["slug"] + "&episodeSlugs=&clientID=" + clientID + "&clientModelNumber=na"

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'tv.png', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showGenre():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    sID = 1
    if sHtmlContent:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in sHtmlContent["categories"]:
            sTitle = aEntry["name"]
            if not isMatrix():
                sTitle = sTitle.encode('utf8')

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sID', int(sID))
            sID = sID + 1

            oGui.addDir(SITE_IDENTIFIER, 'showVOD', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showVOD():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sID = oInputParameterHandler.getValue('sID')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    if sHtmlContent:
        items = sHtmlContent["categories"][int(sID) - 1]["items"]
        total = len(items)
        progress_ = progress().VScreate(SITE_NAME)

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in items:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry["featuredImage"]["path"]
            sTitle = aEntry["name"]
            # /!\ ces replace sont différents
            sTitle = sTitle.replace(' : Saison', ' saison').replace(' : Saison', ' saison')
            ids = aEntry["_id"]
            sDesc = aEntry["description"]
            if not isMatrix():
                sTitle = sTitle.encode('utf8')
                sDesc = sDesc.encode('utf8')

            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            VOD_SERIES = "https://service-vod.clusters.pluto.tv/v3/vod/series/"
            if aEntry["type"] == "series":
                sUrl = VOD_SERIES + ids + "/seasons?includeItems=true&deviceType=web"
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oGui.addTV(SITE_IDENTIFIER, 'showSerieSxE', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif aEntry["type"] == "Anime":
                sUrl = VOD_SERIES + ids + "/seasons?includeItems=true&deviceType=web"
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oGui.addAnime(SITE_IDENTIFIER, 'showSerieSxE', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                siteUrl = "https://service-stitcher.clusters.pluto.tv/stitch/hls/episode/" + ids + "/master.m3u8"
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oGui.addMovie(SITE_IDENTIFIER, 'seriesHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showSerieSxE():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    if sHtmlContent:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in sHtmlContent["seasons"]:
            for a in aEntry["episodes"]:
                sTitle = sMovieTitle + " S" + str(a["season"]) + " E" + str(a["number"])
                sID = a["_id"]

                siteUrl = "https://service-stitcher.clusters.pluto.tv/stitch/hls/episode/" + sID + "/master.m3u8"
                oOutputParameterHandler.addParameter('siteUrl', siteUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addEpisode(SITE_IDENTIFIER, 'seriesHosters', sTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    sHtmlContent = oRequestHandler.request(jsonDecode=True)

    sHosterUrl = "https://service-stitcher.clusters.pluto.tv/stitch/hls/channel/"
    sHosterUrl += sHtmlContent["startingChannel"]["id"] + "/master.m3u8?" + sHtmlContent["stitcherParams"]

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster != False:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def seriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    clientID, deviceID, sid = getData()

    sHosterUrl = sUrl
    sHosterUrl += "?appName=web&appVersion=5.14.0-0f5ca04c21649b8c8aad4e56266a23b96d73b83a&deviceDNT=false"
    sHosterUrl += "&deviceId=" + deviceID + "&deviceMake=Firefox&deviceModel=web&deviceType=web&deviceVersion=87.0"
    sHosterUrl += "&includeExtendedEvents=false&marketingRegion=FR&sid=" + sid + "&serverSideAds=true"

    oHoster = cHosterGui().checkHoster(sUrl)
    if oHoster != False:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
