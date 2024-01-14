# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import json
import re

from resources.lib.comaddon import progress, addon, dialog
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

SITE_IDENTIFIER = 'debrid_link'
SITE_NAME = '[COLOR violet]Debrid Link[/COLOR]'
SITE_DESC = 'Débrideur de lien premium'

URL_HOST = "https://debrid-link.fr"


def load():
    oGui = cGui()
    oAddon = addon()

    URL_HOST = "https://debrid-link.fr"
    ALL_ALL = (URL_HOST + '/api/v2/downloader/list?page=0&perPage=20', 'showLiens')
    ALL_MAGNETS = (URL_HOST + '/api/v2/seedbox/list?page=0&perPage=20', 'showLiens')
    ALL_INFORMATION = (URL_HOST + '/infos/downloader', 'showInfo')

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ALL_ALL[0])
    oGui.addDir(SITE_IDENTIFIER, ALL_ALL[1], 'Liens', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ALL_MAGNETS[0])
    oGui.addDir(SITE_IDENTIFIER, ALL_MAGNETS[1], 'Magnets', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ALL_INFORMATION[0])
    oGui.addDir(SITE_IDENTIFIER, ALL_INFORMATION[1], 'Information sur les hébergeurs ', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showLiens(sSearch=''):
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    numPage = oInputParameterHandler.getValue('numPage')
    if not numPage:
        numPage = 0
    numPage = int(numPage)

    Token_debrid_link = "Bearer " + addon().getSetting('hoster_debridlink_token')
    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.addHeaderEntry('Accept', 'application/json')
    oRequestHandler.addHeaderEntry('Authorization', Token_debrid_link)
    r = json.loads(oRequestHandler.request())

    if (r["success"] == False):
        oGui.addText(SITE_IDENTIFIER)
        if (r["error"] == 'badToken'):
            New_token = RenewToken()

            oRequestHandler = cRequestHandler(sUrl)
            oRequestHandler.addHeaderEntry('Accept', 'application/json')
            oRequestHandler.addHeaderEntry('Authorization', New_token)
            r = json.loads(oRequestHandler.request())

    if (r["success"] == True):
        progress_ = progress().VScreate(SITE_NAME)

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in r["value"]:

            progress_.VSupdate(progress_, len(aEntry["name"]))
            if progress_.iscanceled():
                break

            if 'seedbox' in sUrl:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry["name"] + '[/COLOR]')

                sTitle = aEntry["files"][0]["name"]
                sUrl2 = aEntry["files"][0]["downloadUrl"]

            else:
                sTitle = aEntry["name"]
                sUrl2 = aEntry["downloadUrl"]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addEpisode(SITE_IDENTIFIER, 'showHosters', sTitle, '', '', '', oOutputParameterHandler)
            progress_.VSclose(progress_)

        if not sSearch:
            numPage += 1
            sUrl = re.sub('page=([0-9])', 'page=' + str(numPage), sUrl)
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('numPage', numPage)
            oGui.addNext(SITE_IDENTIFIER, 'showLiens', 'Page ' + str(numPage), oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    sHosterUrl = sUrl
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sMovieTitle)

    oGui.setEndOfDirectory()


def showInfo():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<i class="sprite sprite-.+?"></i>.+?<li tooltip="([^"]+)" class="([^"]+)">'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sDisponible = aEntry[1].replace('on', 'Disponible')\
                                   .replace('off', 'Non Disponible')
            sHebergeur = aEntry[0]

            sDisplayTitle = ('%s (%s)') % (sHebergeur, sDisponible)

            oOutputParameterHandler.addParameter('sMovieTitle', sDisplayTitle)

            oGui.addText(SITE_IDENTIFIER, sDisplayTitle)

        progress_.VSclose(progress_)

        oGui.setEndOfDirectory()


def RenewToken():
    refreshTok = addon().getSetting('hoster_debridlink_tokenrefresh')
    if refreshTok == "":
        oRequestHandler = cRequestHandler(URL_HOST + "/api/oauth/device/code")
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequestHandler.addParameters('client_id', addon().getSetting('hoster_debridlink_ID'))
        r = json.loads(oRequestHandler.request())

        dialog().VSok('Allez sur la page : https://debrid-link.fr/device\n et rentrer le code ' + r["user_code"] + ' pour autorisez la connection')

        oRequestHandler = cRequestHandler(URL_HOST + "/api/oauth/token")
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequestHandler.addParameters('client_id', addon().getSetting('hoster_debridlink_ID'))
        oRequestHandler.addParameters("code", r["device_code"])
        oRequestHandler.addParameters("grant_type", "http://oauth.net/grant_type/device/1.0")
        r = json.loads(oRequestHandler.request())

        addon().setSetting('hoster_debridlink_tokenrefresh', r["refresh_token"])
        addon().setSetting('hoster_debridlink_token', r["access_token"])
        return r["access_token"]

    else:
        oRequestHandler = cRequestHandler(URL_HOST + "/api/oauth/token")
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
        oRequestHandler.addParameters('client_id', addon().getSetting('hoster_debridlink_ID'))
        oRequestHandler.addParameters("refresh_token", refreshTok)
        oRequestHandler.addParameters("grant_type", "refresh_token")
        r = json.loads(oRequestHandler.request())

        addon().setSetting('hoster_debridlink_token', r["access_token"])
        return r["access_token"]
