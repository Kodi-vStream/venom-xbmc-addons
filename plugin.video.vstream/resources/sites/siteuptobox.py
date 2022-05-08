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

from resources.lib.comaddon import progress, dialog, addon, isMatrix, siteManager
from resources.lib.config import GestionCookie
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.premiumHandler import cPremiumHandler
from resources.lib.handler.requestHandler import cRequestHandler, MPencode
from resources.lib.parser import cParser
from resources.lib.util import Quote

SITE_IDENTIFIER = 'siteuptobox'
SITE_NAME = '[COLOR dodgerblue]Compte UpToBox[/COLOR]'
SITE_DESC = 'Fichiers sur compte UpToBox'
URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)
BURL = URL_MAIN + '?op=my_files'
API_URL = 'https://uptobox.com/api/user/files?token=none&orderBy=file_created&dir=desc&offset=0&limit=100&path='

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'
headers = {'User-Agent': UA}


def load():
    oGui = cGui()
    sToken = cPremiumHandler('uptobox').getToken()

    if not sToken:
        oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + 'Nécessite un Compte Uptobox Premium ou Gratuit' + '[/COLOR]')
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', '//')#'http://venom/')
        oGui.addDir(SITE_IDENTIFIER, 'opensetting', addon().VSlang(30023), 'none.png', oOutputParameterHandler)
        oGui.setEndOfDirectory()
        return

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', '//')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', '//')
    oGui.addDir(SITE_IDENTIFIER, 'showFile', 'Mes Fichiers et Dossiers', 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def opensetting():
    addon().openSettings()


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if sSearchText != False:
        sUrlSearch = '&searchField=file_name&search=' + sSearchText
        showFile(sUrlSearch)


def showFile(sSearch=''):

    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sSiteUrl = oInputParameterHandler.getValue('siteUrl')
    
    sOffset = 0
    if oInputParameterHandler.exist('sOffset'):
        sOffset = int(oInputParameterHandler.getValue('sOffset'))

    sNext = 0
    if oInputParameterHandler.exist('sNext'):
        sNext = int(oInputParameterHandler.getValue('sNext'))

    oPremiumHandler = cPremiumHandler('uptobox')
    sToken = oPremiumHandler.getToken()

    # parcourir un dossier virtuel, séparateur ':'
    searchFolder = ''
    if sSiteUrl[-1:] == ':':
        idxFolder = sSiteUrl.rindex('/')
        searchFolder = sSiteUrl[idxFolder+1:-1]
        sSiteUrl = sSiteUrl[:idxFolder]


    oRequestHandler = cRequestHandler(API_URL.replace('none', sToken) + sSiteUrl)
    sHtmlContent = oRequestHandler.request()
    content = json.loads(sHtmlContent)
    
    if content['statusCode'] == 1:
        dialog().VSinfo(content['data'])
        oGui.setEndOfDirectory()
        return
    
    content = content['data']
    if not content:
        oGui.setEndOfDirectory()
        return

    # ajout des dossiers en premier, sur la première page seulement
    if not sSearch and sOffset == 0 and 'folders' in content:


        # dossiers trier par ordre alpha
        folders = sorted(content['folders'], key=lambda f: f['fld_name'])
        
        sFoldername = ''
        
        # Sous-dossiers virtuels identifiés par les deux-points
        subFolders = set()
        
        for folder in folders:
            if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
                sTitle = folder['name']
                sFoldername = folder['fld_name']
            else:
                sTitle = folder['name'].encode('utf-8')
                sFoldername = folder['fld_name'].encode('utf-8')

            if sTitle.startswith('REP_'):
                sTitle=sTitle.replace('REP_', '')
            if sTitle.startswith('00_'):
                sTitle=sTitle.replace('00_', '')

            if ':' in sTitle:
                subName, subFolder = sTitle.split(':')
                if folder['path'].endswith(subName):
                    sTitle = subFolder.strip()
                else:
                    if searchFolder:
                        if subName == searchFolder:
                            sTitle = subFolder
                            sFoldername = sFoldername
                    else:
                        if subName in subFolders:
                            continue
                        subFolders.add(subName)
                        sTitle = subName
                        sFoldername = sSiteUrl + '/' + subName + ':'
            else:
                if searchFolder:
                    continue

            sUrl = Quote(sFoldername).replace('//', '%2F%2F')

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oGui.addDir(SITE_IDENTIFIER, 'showFile', sTitle, 'genres.png', oOutputParameterHandler)


    # ajout des fichiers
    for file in content['files']:
        if xbmc.getInfoLabel('system.buildversion')[0:2] >= '19':
            sTitle = file['file_name']
        else:
            sTitle = file['file_name'].encode('utf-8')
            
        sHosterUrl = URL_MAIN + file['file_code']
        path = content['path'].upper()
        if 'FILM' in path or 'MOVIE' in path:
            
            # seulement les formats vidéo (ou sans extensions)
            if sTitle[-4] == '.':
                if sTitle[-4:] not in '.mkv.avi.mp4.iso':
                    continue
                # enlever l'extension
                sTitle = sTitle[:-4]

            sMovieTitle = sTitle
            
            # recherche des métadonnées
            pos = len(sMovieTitle)
            sPattern = ['[^\w]([0-9]{4})[^\w]']
            sYear, pos = getTag(sMovieTitle, sPattern, pos)
            
            sPattern = ['HDLIGHT', '\d{3,4}P', '4K', 'UHD', 'BDRIP', 'BRRIP', 'DVDRIP', 'DVDSCR', 'TVRIP', 'HDTV', 'BLURAY', '[^\w](R5)[^\w]', '[^\w](CAM)[^\w]', 'WEB-DL', 'WEBRIP', '[^\w](WEB)[^\w]']
            sRes, pos = getTag(sMovieTitle, sPattern, pos)
            if sRes:
                sRes = sRes.replace('2160P', '4K')
            
            sPattern = ['TM(\d+)TM']
            sTmdbId, pos = getTag(sMovieTitle, sPattern, pos)

            sPattern = ['VFI', 'VFF', 'VFQ', 'SUBFRENCH', 'TRUEFRENCH', 'FRENCH', 'VF', 'VOSTFR', '[^\w](VOST)[^\w]', '[^\w](VO)[^\w]', 'QC', '[^\w](MULTI)[^\w]']
            sLang, pos = getTag(sMovieTitle, sPattern, pos)

            sMovieTitle = sMovieTitle[:pos].replace('.', ' ').strip()
            
            sTitle = sMovieTitle
            if sRes:
                sMovieTitle += ' [%s]' % sRes
            if sLang:
                sMovieTitle += ' (%s)' % sLang
            
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sHosterUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sYear', sYear)
            oOutputParameterHandler.addParameter('sRes', sRes)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
            
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sMovieTitle, '', '', '', oOutputParameterHandler)
        else:
            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if oHoster != False:
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
        sNext += 1

    # Lien Suivant >>
    if not sSearch:
        sPath = getpath(content)
        if content['currentFolder']['fileCount'] != int(sNext):
            oOutputParameterHandler = cOutputParameterHandler()

            sOffset = int(sOffset) + 100
            nextPage = int((sOffset+ 100)/100)

            oOutputParameterHandler.addParameter('siteUrl', API_URL.replace('none', sToken).replace('offset=0', 'offset=' + str(sOffset)))
            oOutputParameterHandler.addParameter('sNext', sNext)
            oOutputParameterHandler.addParameter('sOffset', sOffset)
            oOutputParameterHandler.addParameter('sPath', sPath)
            oGui.addNext(SITE_IDENTIFIER, 'showFile', 'Page ' + str(nextPage), oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sHosterUrl = oInputParameterHandler.getValue('siteUrl')
    sTitle = oInputParameterHandler.getValue('sMovieTitle')
    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster != False:
        oHoster.setDisplayName(sTitle)
        oHoster.setFileName(sTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
    oGui.setEndOfDirectory()



def getTag(sMovieTitle, tags, pos):
    for t in tags:
        aResult = re.search(t, sMovieTitle, re.IGNORECASE)
        if aResult:
            l = len(aResult.groups())
            ret = aResult[l]
            p = sMovieTitle.index(aResult[0])
            if p<pos:
                pos = p
            return ret.upper(), pos
    return False, pos



def getpath(content):
    for x in content:
        if x == 'path':
            sPath = Quote(content[x].encode('utf-8')).replace('//', '%2F%2F')
            return sPath


def AddmyAccount():
    upToMyAccount()


def upToMyAccount():
    addons = addon()

    if (addons.getSetting('hoster_uptobox_username') == '') and (addons.getSetting('hoster_uptobox_password') == ''):
        return
    oInputParameterHandler = cInputParameterHandler()
    sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')

    oPremiumHandler = cPremiumHandler('uptobox')

    sHtmlContent = oPremiumHandler.GetHtml(URL_MAIN)
    cookies = GestionCookie().Readcookie('uptobox')

    aResult = re.search('<form id="fileupload" action="([^"]+)"', sHtmlContent, re.DOTALL)
    if aResult:
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

        # pénible ce dialog auth
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
        if aResult[0] is True:
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
            # pénible ce dialog auth
            xbmc.executebuiltin('Dialog.Close(all,true)')
            xbmcgui.Dialog().notification('Info upload', 'Fichier introuvable', xbmcgui.NOTIFICATION_INFO, 2000, False)
    else:
        # pénible ce dialog auth
        xbmc.executebuiltin('Dialog.Close(all,true)')
        xbmcgui.Dialog().notification('Info upload', 'Erreur pattern', xbmcgui.NOTIFICATION_ERROR, 2000, False)
