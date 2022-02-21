# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import json
import re
import xbmc
import xbmcgui

try:  # Python 2
    import urllib2
    from urllib2 import URLError as UrlError

except ImportError:  # Python 3
    import urllib.request as urllib2
    from urllib.error import URLError as UrlError
    from urllib.parse import urlencode

from resources.lib.comaddon import progress, dialog, addon, isMatrix
from resources.lib.config import GestionCookie
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import MPencode
from resources.lib.parser import cParser
from resources.lib.util import Quote

SITE_IDENTIFIER = 'siteuptobox'
SITE_NAME = '[COLOR dodgerblue]Compte UpToBox[/COLOR]'
SITE_DESC = 'Fichiers sur compte UpToBox'
URL_MAIN = 'https://uptobox.com/'
BURL = URL_MAIN + '?op=my_files'
API_URL = 'https://uptobox.com/api/user/files?token=none&orderBy=file_created&dir=desc&offset=0&limit=100&path='

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
headers = {'User-Agent': UA}


def load():
    oGui = cGui()
    addons = addon()
    oPremiumHandler = cPremiumHandler('uptobox')

    if (addons.getSetting('hoster_uptobox_username') == '') and (addons.getSetting('hoster_uptobox_password') == ''):
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + 'Nécessite un Compte Uptobox Premium ou Gratuit' + '[/COLOR]')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
        oGui.addDir(SITE_IDENTIFIER, 'opensetting', addons.VSlang(30023), 'none.png', oOutputParameterHandler)
    else:
        if (GestionCookie().Readcookie('uptobox') != ''):

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
            oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

            oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
            oGui.addDir(SITE_IDENTIFIER, 'showFile', 'Mes Fichiers et Dossiers', 'genres.png', oOutputParameterHandler)

        else:
            Connection = oPremiumHandler.Authentificate()
            if (Connection == False):
                dialog().VSinfo('Connexion refusée')
                return

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
            oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

            oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
            oGui.addDir(SITE_IDENTIFIER, 'showFile', 'Mes Fichiers et Dossiers', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def opensetting():
    addon().openSettings()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrlSearch = '&searchField=file_name&search=' + sSearchText
        showFile(sUrlSearch)


def showFile(sSearch=''):

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    # VSlog('input   ' + str(sUrl))
    oParser = cParser()

    sOffset = 0
    if (oInputParameterHandler.exist('sOffset')):
        sOffset = int(oInputParameterHandler.getValue('sOffset'))

    sNext = 0
    if (oInputParameterHandler.exist('sNext')):
        sNext = int(oInputParameterHandler.getValue('sNext'))

    sToken = ''
    if (oInputParameterHandler.exist('sToken')):
        sToken = oInputParameterHandler.getValue('sToken')

    sFoldername = ''
    if (oInputParameterHandler.exist('sFoldername')):
        sFoldername = oInputParameterHandler.getValue('sFoldername')
        sUrl = sUrl + Quote(sFoldername).replace('//', '%2F%2F')
        # VSlog('folder   ' + str(sUrl))

    sPath = ''
    if (oInputParameterHandler.exist('sPath')):
        sPath = oInputParameterHandler.getValue('sPath')
        sUrl = sUrl + Quote(sPath).replace('//', '%2F%2F')
        # VSlog('sPath   ' + str(sUrl))

    oPremiumHandler = cPremiumHandler('uptobox')

    if 'uptobox.com' in sUrl:
        sHtmlContent = oPremiumHandler.GetHtml(sUrl)

    else:
        if sToken == '':
            sHtmlContent = oPremiumHandler.GetHtml(BURL)
            sPattern = 'token":"(.+?)",'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                sToken = aResult[1][0]

            if sSearch:
                sHtmlContent = oPremiumHandler.GetHtml(API_URL.replace('none', sToken) + '%2F%2F' + sSearch)
            else:
                sHtmlContent = oPremiumHandler.GetHtml(API_URL.replace('none', sToken) + '%2F%2F')

    content = json.loads(sHtmlContent)
    content = content['data']

    if content:
        total = len(content)
        progress_ = progress().VScreate(SITE_NAME)
        sPath = getpath(content)
        for contentType in content:

            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if contentType == 'files':

                for file in content[contentType]:
                    if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                        sTitle = file['file_name']
                    else:
                        sTitle = file['file_name'].encode('utf-8')

                    sHosterUrl = URL_MAIN + file['file_code']

                    oHoster = cHosterGui().checkHoster(sHosterUrl)
                    if (oHoster != False):
                        oHoster.setDisplayName(sTitle)
                        oHoster.setFileName(sTitle)
                        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
                    sNext += 1

            if not sSearch and contentType == 'folders':

                for folder in content[contentType]:
                    if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                        sTitle = folder['name']
                        sFoldername = folder['fld_name']
                    else:
                        sTitle = folder['name'].encode('utf-8')
                        sFoldername = folder['fld_name'].encode('utf-8')

                    sUrl = API_URL.replace('none', sToken)

                    oOutputParameterHandler = cOutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', sUrl)
                    oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                    oOutputParameterHandler.addParameter('sFoldername', sFoldername)
                    oOutputParameterHandler.addParameter('sToken', sToken)
                    oGui.addDir(SITE_IDENTIFIER, 'showFile', sTitle, 'genres.png', oOutputParameterHandler)

            if not sSearch and contentType == 'currentFolder':
                if content[contentType]['fileCount'] != int(sNext):
                    oOutputParameterHandler = cOutputParameterHandler()

                    sOffset = int(sOffset) + 100

                    oOutputParameterHandler.addParameter('siteUrl', API_URL.replace('none', sToken).replace('offset=0', 'offset=' + str(sOffset)))
                    oOutputParameterHandler.addParameter('sToken', sToken)
                    oOutputParameterHandler.addParameter('sNext', sNext)
                    oOutputParameterHandler.addParameter('sOffset', sOffset)
                    oOutputParameterHandler.addParameter('sPath', sPath)
                    oGui.addNext(SITE_IDENTIFIER, 'showFile', 'Suite', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def getpath(content):
    for x in content:
        if x == 'path':
            sPath = Quote(content[x].encode('utf-8')).replace('//', '%2F%2F')
            # VSlog(sPath)
            return sPath


def AddmyAccount():
    UptomyAccount()


def UptomyAccount():
    addons = addon()

    if (addons.getSetting('hoster_uptobox_username') == '') and (addons.getSetting('hoster_uptobox_password') == ''):
        return
    oInputParameterHandler = cInputParameterHandler()
    sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')

    oPremiumHandler = cPremiumHandler('uptobox')

    sHtmlContent = oPremiumHandler.GetHtml(URL_MAIN)
    cookies = GestionCookie().Readcookie('uptobox')

    aResult = re.search('<form id="fileupload" action="([^"]+)"', sHtmlContent, re.DOTALL)
    if (aResult):
        upUrl = aResult.group(1).replace('upload?', 'remote?')

        if upUrl.startswith('//'):
            upUrl = 'https:' + upUrl

        fields = {'urls': '["' + sMediaUrl + '"]'}
        mpartdata = list(MPencode(fields))

        if isMatrix():
            mpartdata[1] = mpartdata[1].encode("utf-8")

        req = urllib2.Request(upUrl, mpartdata[1], headers)
        req.add_header('Content-Type', mpartdata[0].replace(',', ';'))
        req.add_header('Cookie', cookies)
        req.add_header('Content-Length', len(mpartdata[1]))

        # penible ce dialog auth
        xbmc.executebuiltin('Dialog.Close(all,true)')
        xbmcgui.Dialog().notification('Requête envoyée', 'vous pouvez faire autre chose', xbmcgui.NOTIFICATION_INFO, 4000, False)

        try:
            rep = urllib2.urlopen(req)
        except UrlError:
            return ''

        sHtmlContent = rep.read()
        rep.close()

        sPattern = '{"id":.+?,(?:"size":|"progress":)([0-9]+)'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            total = aResult[1][0]
            del aResult[1][0]

            dialog = xbmcgui.DialogProgressBG()
            dialog.create(SITE_NAME, 'Transfert de fichiers sur votre compte Uptobox')

            for aEntry in aResult[1]:
                if isMatrix():
                    dialog.update(int(aEntry) * 100 // int(total), 'Upload en cours...')
                else:
                    dialog.update(int(aEntry) * 100 / int(total), 'Upload en cours...')

                xbmc.sleep(500)
            dialog.close()

        else:
            # penible ce dialog auth
            xbmc.executebuiltin('Dialog.Close(all,true)')
            xbmcgui.Dialog().notification('Info upload', 'Fichier introuvable', xbmcgui.NOTIFICATION_INFO, 2000, False)
    else:
        # penible ce dialog auth
        xbmc.executebuiltin('Dialog.Close(all,true)')
        xbmcgui.Dialog().notification('Info upload', 'Erreur pattern', xbmcgui.NOTIFICATION_ERROR, 2000, False)
