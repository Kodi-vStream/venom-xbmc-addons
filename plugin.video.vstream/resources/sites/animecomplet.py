# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re
import string

from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import siteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'animecomplet'
SITE_NAME = 'Animecomplet'
SITE_DESC = 'Series Anime'

URL_MAIN = siteManager().getUrlMain(SITE_IDENTIFIER)

ANIM_ANIMS = (True, 'load')
# ANIM_NEWS = (URL_MAIN, 'showAnims')
# ANIM_ALPHA = (URL_MAIN, 'showAlpha')

tag_global = '#global'
URL_SEARCH_ANIMS = (URL_MAIN + tag_global + '?s=', 'showAnims')
URL_SEARCH = (URL_MAIN + '?s=', 'showAnims')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    # oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers  épisodes récents)', 'series.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', ANIM_ALPHA[0])
    # oGui.addDir(SITE_IDENTIFIER, ANIM_ALPHA[1], 'Animés (Liste alphabétique)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAlpha():
    oGui = cGui()
    sAlpha = string.ascii_lowercase
    listAlpha = list(sAlpha)
    liste = []

    req = ANIM_LIST[0]
    oRequestHandler = cRequestHandler(req)
    sHtmlContent = oRequestHandler.request()

    # on propose quand meme en premier la liste complete
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_LIST[1], ' [COLOR coral]' + 'Animés (Liste complète)' + '[/COLOR]', 'listes.png', oOutputParameterHandler)

    # récupere les chiffres dispos
    sPattern = 'href="#gti_(\d+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        for aEntry in aResult[1]:
            liste.append([str(aEntry), url1 + str(aEntry)])

    for alpha in listAlpha:
        liste.append([str(alpha).upper(), url1 + str(alpha)])

    # sUrl = 'tagalpha ;alpha'
    for sTitle, sUrl in liste:
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showAnims', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if sSearchText:
        sUrl = URL_SEARCH[0] + sSearchText
        showAnims(sUrl)
        oGui.setEndOfDirectory()
        return


def showAnims(sSearch=''):
    oGui = cGui()

    bSearchGlobal = False
    if sSearch:
        oUtil = cUtil()
        sSearchText = sSearch.replace(URL_SEARCH[0], '')
        sSearchText = sSearchText.replace(URL_SEARCH_ANIMS[0], '')
        sSearchText = oUtil.CleanName(sSearchText)
        sUrl = sSearch.replace(' ', '+').replace('%20', '+')
        if tag_global in sSearch:
            sUrl = sUrl.replace(tag_global, '')
            bSearchGlobal = True
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    # pour la liste alpha on peu aussi faire sUrl = alpha (plus rapide)
    # sPattern = '<a href="([^"]+)">..' + alpha + '([^<]+).+?style="width'

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<article id=".+?img src="([^\"]+)".+?<a href="([^\"]+)"><.+?>(.+?)<'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    iCurrent = 0
    list_simlilar = []

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)
    else:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            iCurrent = iCurrent + 1
            sThumb = ''
            sDesc = ''
            sThumb = aEntry[0]
            sUrl2 = aEntry[1]
            sTitle = aEntry[2]
            try:
                sTitle = sTitle.decode('ascii', errors='ignore')
            except:
                pass
            sTitle = sTitle.replace(' - Episode', ' Episode').replace(' VOSTFR', '').replace(' VF', '')
            if sSearch and not oUtil.CheckOccurence(sSearchText, sTitle):
                continue    # Filtre de recherche

            sLang = ''
            if ' VOSTFR' in sTitle:
                sLang = 'VOSTFR'
            if ' VF' in sTitle:
                sLang = 'VF'
            if 'http' not in sThumb:
                sThumb = URL_MAIN + sThumb

            # le lien liés a l'episode va nous fournir apres tous
            # les episodes saisons donc inutile de tout afficher si titre semblable
            if bSearchGlobal and iCurrent > 3:
                bValid, sim = similarTitle(sTitle)
                if bValid:
                    if sim not in list_simlilar:
                        list_simlilar.append(sim)
                    else:
                        continue
            sDisplayTtitle = sTitle + ' (' + sLang + ')'

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sLang', sLang)
            oGui.addAnime(SITE_IDENTIFIER, 'seriesHosters', sDisplayTtitle, '', sThumb, sDesc, oOutputParameterHandler)

    if not bSearchGlobal:
        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage is not False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showAnims', 'Page ' + sPaging, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '>([^<]+)</a><a class="next page.+?href="([^"]+).+?Suivant'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sNumberMax = aResult[1][0][0]
        sNextPage = URL_MAIN + aResult[1][0][1]
        sNumberNext = re.search('paged=([0-9]+)', sNextPage).group(1)
        sPaging = sNumberNext + '/' + sNumberMax
        return sNextPage, sPaging

    return False, 'none'


def showSaisons():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'colo_cont">.+?>([^<]*)</p>'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = aResult[1][0]
        sDesc = ('[I][COLOR coral]%s[/COLOR][/I] %s') % (' SYNOPSIS : \r\n\r\n', sDesc)
    else:
        sDesc = ''

    sPattern = 'class="item">.+?href="([^"]+)".+?<h2>([^<]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sTitle = sMovieTitle + ' ' + aEntry[1]

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showEpisodes():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<h2 class="entry-title">.+?b>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sDesc = ('[I][COLOR grey]%s[/COLOR][/I]') % ('Anime Complet')
    if aResult[0]:
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    # inutile (pour l'instant)
    start = sHtmlContent.find('<div class="post-content">')
    sHtmlContent = sHtmlContent[start:]

    sPattern = '<h2><a href="([^"]+).+?title="([^"]+).+?src=.([^">]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if not aResult[0]:
        oGui.addText(SITE_IDENTIFIER)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sUrl2 = aEntry[0]
            sTitle = aEntry[1]
            if ' VOSTFR' in sTitle:
                sTitle = sTitle.replace(' - Episode', ' Episode').replace(' VOSTFR', '')
            sThumb = aEntry[2]
            if 'http' not in sThumb:
                sThumb = URL_MAIN + sThumb

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addAnime(SITE_IDENTIFIER, 'seriesHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        sNextPage, sPaging = __checkForNextPage(sHtmlContent)
        if sNextPage is not False:
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showEpisodes', 'Page ' + sPaging, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def seriesHosters():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'iframe.+?src="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0]:
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry

            if 'https' not in sUrl2:
                sUrl2 = 'https:' + sUrl2

            # sHost = ''
            oHoster = cHosterGui().checkHoster(sUrl2)
            if not oHoster:
                continue
            sHost = '[COLOR coral]' + oHoster.getDisplayName() + '[/COLOR]'

            sDisplayTitle = sMovieTitle + ' ' + sHost
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('referer', sUrl)
            oGui.addLink(SITE_IDENTIFIER, 'hostersLink', sDisplayTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def getHostName(url):
    try:
        if 'www' not in url:
            sHost = re.search('http.*?\/\/([^.]*)', url).group(1)
        else:
            sHost = re.search('htt.+?\/\/(?:www).([^.]*)', url).group(1)
            sHost = str(sHost).capitalize()
    except:
        sHost = url
    return sHost


def hostersLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sHosterUrl = sUrl

    if 'oload.tv' in sUrl:  # https://oload.tv/embed/0rRYBdB_3Xw/# #ace attorney vostfr
        oGui.addText(SITE_IDENTIFIER, ' vStream : Accès refusé : Le site Oload.tv n\'est pas sécurisé')
        oGui.setEndOfDirectory()
        return

    # Petit hack pour conserver le nom de domaine du site
    # necessaire pour userload.
    if 'userload' in sHosterUrl:
        sHosterUrl = sHosterUrl + "|Referer=" + URL_MAIN

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if oHoster:
        oHoster.setDisplayName(sMovieTitle)
        oHoster.setFileName(sMovieTitle)
        cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def similarTitle(s):
    list_spe = ['&', '\'', ',', '.', ';', '!']

    s = s.strip()
    if ' ' in s:
        try:
            s = str(s).lower()
            sx = s.split(' ')
            snews = sx[0] + ' ' + sx[1]
            for spe in list_spe:
                snews = snews.replace(spe, '')
            return True, snews.lower()
        except:
            return False, False
    return False, False
