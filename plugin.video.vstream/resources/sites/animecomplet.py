# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# source 28
import re
import string
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

SITE_IDENTIFIER = 'animecomplet'
SITE_NAME = 'Animecomplet'
SITE_DESC = 'Series Anime'

URL_MAIN = 'https://animecomplet.co/'

tag_alpha = 'tagaplha'
ANIM_ANIMS = (True, 'load')
ANIM_NEWS = (URL_MAIN, 'showSeries')
ANIM_LIST = (URL_MAIN + 'liste-manga-vostfr-et-manga-vf/', 'showSeries')
ANIM_ALPHA = (tag_alpha, 'showAlpha')
ANIM_VOSTFRS = (URL_MAIN, 'showSeries')

tag_global = '#global'
URL_SEARCH_SERIES = (URL_MAIN + tag_global + '?s=', 'showSeries')
URL_SEARCH = (URL_MAIN + '?s=', 'showSeries')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animés (Derniers  épisodes récents)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_LIST[1], 'Animés (Liste complète)', 'listes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ALPHA[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ALPHA[1], 'Animés (Liste alphabétique)', 'az.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showAlpha():
    oGui = cGui()
    sAlpha = string.ascii_lowercase
    listAlpha = list(sAlpha)
    liste = []
    url1 = tag_alpha + ';'

    req = ANIM_LIST[0]
    oRequestHandler = cRequestHandler(req)
    sHtmlContent = oRequestHandler.request()

    # on propose quand meme en premier la liste complete
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_LIST[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSeries', ' [COLOR coral]' + 'Animés (Liste complète)' + '[/COLOR]', 'listes.png', oOutputParameterHandler)

    # récupere les chiffres dispos
    sPattern = 'href="#gti_(\d+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            liste.append([str(aEntry), url1 + str(aEntry)])

    for alpha in listAlpha:
        liste.append([str(alpha).upper(), url1 + str(alpha)])

    # sUrl = 'tagalpha ;alpha'
    for sTitle, sUrl in liste:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', 'Lettre [COLOR coral]' + sTitle + '[/COLOR]', 'listes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showSeries(sUrl)
        oGui.setEndOfDirectory()
        return


def showSeries(sSearch=''):
    oGui = cGui()

    bSearchGlobal = False
    if sSearch:
        sUrl = sSearch.replace(' ', '+').replace('%20', '+')
        if tag_global in sSearch:
            sUrl = sUrl.replace(tag_global, '')
            bSearchGlobal = True

    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    # pour la liste alpha on peu aussi faire sUrl=alpha (plus rapide)
    # sPattern = '<a href="([^"]+)">..' + alpha + '([^<]+).+?style="width'
    balpha = False
    sAlpha = ''
    if tag_alpha in sUrl:
        letag, sAlpha = sUrl.split(';')
        sUrl = ANIM_LIST[0]
        balpha = True

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if sUrl == ANIM_LIST[0]:  # category"><a href="([^"]+).+?title="([^"]+).+?meta-date">([^<]+).+?src=.([^">]+)
        sPattern = '<a href="([^"]+)">.([^<]+).+?style="width'
    else:
        # sPattern = 'category"><a href="([^"]+).+?title="([^"]+).+?meta-date">([^<]+).+?src=.([^">]+)'
        sPattern = '<center><p><img.*?src=.([^">]+).*?category"><a href="([^"]+).+?title="([^"]+).+?meta-date">([^<]+)'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    icurrent = 0
    list_simlilar= []

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:

            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break
            icurrent = icurrent + 1
            sThumb = ''
            sDesc = ''
            if sUrl == ANIM_LIST[0]:
                sUrl2 = aEntry[0]
                sTitle = aEntry[1]

                if '(0)' in sTitle or 'EPISODES' in sTitle:  # EPISODES  1 element pattern a revoir pattern
                    continue

                if balpha:
                    sTitle2 = sTitle.strip().lower()
                    if not sTitle2.startswith(sAlpha):
                        continue

            else:
                sThumb = aEntry[0]
                sUrl2 = aEntry[1]
                sTitle = aEntry[2]
                sDesc = 'Mise à jour : ' + aEntry[3]

            try:
                sTitle = sTitle.decode('ascii', errors='ignore')
            except:
            	pass
            	
            if 'http' not in sThumb:
                sThumb = URL_MAIN + sThumb

            # le lien liés a l'episode va
            # nous fournir apres tous les episodes saisons
            # donc inutile de tout afficher si titre semblable
            if bSearchGlobal and icurrent > 3:
                bvalid, sim = similarTitle(sTitle)
                if bvalid:
                    if sim not in list_simlilar:
                        list_simlilar.append(sim)
                    else:
                        continue

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addAnime(SITE_IDENTIFIER, 'showEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            sNumPage = ''
            try:
                sNumPage = re.search('page.([0-9]+)', sNextPage).group(1)
            except:
                pass
            oGui.addNext(SITE_IDENTIFIER, 'showSeries', 'Page ' + sNumPage, oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'class="next page.+?href="([^"]+).+?Next'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]
    return False


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
    if (aResult[0] == True):
        sDesc = aResult[1][0]
        sDesc = ('[I][COLOR coral]%s[/COLOR][/I] %s') % (' SYNOPSIS : \r\n\r\n', sDesc)
    else:
        sDesc = ''

    sPattern = 'class="item">.+?href="([^"]+)".+?<h2>([^<]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sTitle = sMovieTitle + ' ' + aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
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
    # sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    # sThumb = oInputParameterHandler.getValue('sThumb')
    # sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<h2 class="entry-title">.+?b>([^<]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sDesc = ('[I][COLOR grey]%s[/COLOR][/I]') % ('Anime Complet ')
    if (aResult[0] == True):
        sDesc = ('[I][COLOR grey]%s[/COLOR][/I] %s') % ('Synopsis :', aResult[1][0])

    # inutile (pour l'instant)
    start = sHtmlContent.find('<div class="post-content">')
    sHtmlContent = sHtmlContent[start:]

    sPattern = '<h2><a href="([^"]+).+?title="([^"]+).+?src=.([^">]+)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sUrl2 = aEntry[0]
            sTitle = aEntry[1]
            sThumb = aEntry[2]
            if 'http' not in sThumb:
                sThumb = URL_MAIN + sThumb

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addEpisode(SITE_IDENTIFIER, 'seriesHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            sNumPage = ''
            try:
                sNumPage = re.search('page.([0-9]+)', sNextPage).group(1)
            except:
                pass
            oGui.addNext(SITE_IDENTIFIER, 'showEpisodes', 'Page ' + sNumPage, oOutputParameterHandler)

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

    sPattern = '<iframe.*?src="([^"]+)'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            sUrl2 = aEntry

            if 'https' not in sUrl2:
                sUrl2 = 'https:' + sUrl2

            # sHost = ''
            oHoster = cHosterGui().checkHoster(sUrl2)
            if (oHoster != False):
                sHost = '[COLOR coral]' + oHoster.getDisplayName() + '[/COLOR]'
            else:
                sHost = '[COLOR pink]' + getHostName(sUrl2) + '[/COLOR]'

            # juste pour dire que c'est le lien le plus fiable en generale
            if 'SendVid' in sHost:
                sHost = sHost + ' #'

            sDisplayTitle = sMovieTitle + ' ' + sHost
            oOutputParameterHandler = cOutputParameterHandler()
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
    # referer = oInputParameterHandler.getValue('referer')

    sHosterUrl = sUrl
    sDisplayMovieTitle = sMovieTitle

    if 'oload.tv' in sUrl:  # https://oload.tv/embed/0rRYBdB_3Xw/# #ace attorney vostfr
        oGui.addText(SITE_IDENTIFIER, ' vStream : Accès refusé : Le site Oload.tv n\'est pas sécurisé')
        oGui.setEndOfDirectory()
        return

    oHoster = cHosterGui().checkHoster(sHosterUrl)
    if (oHoster != False):
        oHoster.setDisplayName(sDisplayMovieTitle)
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
            snew = sx[0] + ' ' + sx[1]
            for spe in list_spe:
                snews = snew.replace(spe, '')
            return True, snews.lower()
        except:
            return False, False
    return False, False
