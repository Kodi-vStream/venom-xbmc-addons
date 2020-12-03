# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
return False
import base64
import os
import re
import xbmcaddon
import xbmcvfs

from resources.lib.comaddon import progress, dialog, xbmc, xbmcgui, VSlog, addon
from resources.lib.config import GestionCookie
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import Noredirection, urlEncode
from resources.lib.multihost import cMultiup

ADDON = addon()
UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'

SITE_IDENTIFIER = 'time2watch'
SITE_NAME = '[COLOR violet]Time2Watch[/COLOR]'
SITE_DESC = 'films en streaming, streaming hd, streaming 720p, Films/séries, récent'

URL_MAIN = 'https://time2watch.io/'

URL_SEARCH = (URL_MAIN + 'search/?q=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

MOVIE_MOVIE = (True, 'showMenuFilms')
DERNIER_AJOUT = (URL_MAIN + 'last/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'film/last/', 'showMovies')
MOVIE_POPULAR = (URL_MAIN + "film/popular/", 'showMovies')
MOVIE_HD1080 = (URL_MAIN + 'film/bluray/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'film/vostfr/', 'showMovies')
MOVIE_VFR = (URL_MAIN + 'film/vfr/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'film/loved/', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'film/genre/', 'showGenre')
MOVIE_ANNEES = (URL_MAIN + 'film/date/', 'showYears')

SERIE_SERIES = (True, 'showMenuSeries')
SERIE_NEWS = (URL_MAIN + 'serie/last/', 'showMovies')
SERIE_POPULAR = (URL_MAIN + "serie/popular/", 'showMovies')
SERIE_HD1080 = (URL_MAIN + 'serie/bluray/', 'showMovies')
SERIE_VOSTFR = (URL_MAIN + 'serie/vostfr/', 'showMovies')
SERIE_VFR = (URL_MAIN + 'serie/vfr/', 'showMovies')
SERIE_NOTES = (URL_MAIN + 'serie/loved/', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'serie/genre/', 'showGenre')
SERIE_ANNEES = (URL_MAIN + 'serie/date/', 'showYears')

ANIM_ANIMS = (True, 'showMenuMangas')
ANIM_NEWS = (URL_MAIN + 'anime/last/', 'showMovies')
ANIM_POPULAR = (URL_MAIN + "anime/popular/", 'showMovies')
ANIM_HD1080 = (URL_MAIN + 'anime/bluray/', 'showMovies')
ANIM_VOSTFR = (URL_MAIN + 'anime/vostfr/', 'showMovies')
ANIM_VFR = (URL_MAIN + 'anime/vfr/', 'showMovies')
ANIM_NOTES = (URL_MAIN + 'anime/loved/', 'showMovies')
ANIM_GENRES = (URL_MAIN + 'anime/genre/', 'showGenre')
ANIM_ANNEES = (URL_MAIN + 'anime/date/', 'showYears')

DOC_NEWS = (URL_MAIN + 'documentaires/', 'showMovies')
SPECTACLE_NEWS = (URL_MAIN + 'theatre/', 'showMovies')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showDetail', '[COLOR red]Explication pour le site[/COLOR]', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DERNIER_AJOUT[0])
    oGui.addDir(SITE_IDENTIFIER, DERNIER_AJOUT[1], 'Derniers Ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuAutre', 'Autres', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuFilms():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD1080[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD1080[1], 'Bluray 1080P', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_POPULAR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_POPULAR[1], 'Films (Les plus populaires)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VFR[1], 'Films (VFR)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'notes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Series (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Series (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Series (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD1080[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD1080[1], 'Bluray 1080P', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_POPULAR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_POPULAR[1], 'Series (Les plus populaires)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFR[1], 'Series (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFR[1], 'Series (VFR)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NOTES[1], 'Series (Les mieux notées)', 'notes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animes (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animes (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANNEES[1], 'Animes (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_HD1080[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_HD1080[1], 'Bluray 1080P', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_POPULAR[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_POPULAR[1], 'Animes (Les plus populaires)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFR[1], 'Animés (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFR[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFR[1], 'Animés (VFR)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NOTES[1], 'Animés (Les mieux notés)', 'notes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showDetail():
    dialog().VStextView(desc="""Explication du Captcha:
Pour passer le Captcha il suffit de choisir l'image qui corresponds la plus a celle de gauche.
Il se peut que la couleur ou l'orientation de l'image sous différente.
Mais le pictogramme lui sera le meme.
Attention vous avez 20 secondes pour valider votre réponse.
Si jamais vous vous trompez il suffit de recharger la page.

Utilité d'avoir un compte:
Le site est limité en nombre de passage pour les personnes qui n'ont pas de compte.
Avoir un compte permet aussi de ne pas avoir le Captcha qui apparait à chaque fois.
Vous pouvez activer la connexion au compte dans les paramètres de vStream.""", title="Fonctionnement du site")


def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    html = re.search('<section id="section_genre">(.+?)</section>', sHtmlContent, re.DOTALL).group(1)
    sPattern = '<a href="([^"]+)">([^"]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(html, sPattern)

    for genre in aResult[1]:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + genre[0])
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', genre[1], 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showYears():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    html = re.search('<section id="section_genre">(.+?)</section>', sHtmlContent, re.DOTALL).group(1)
    sPattern = '<a href="([^"]+)">([^"]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(html, sPattern)

    for Years in aResult[1]:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + Years[0])
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Years[1], 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    Cookie = GestionCookie().Readcookie('time2watch')

    oRequestHandler = cRequestHandler(sUrl)
    if Cookie:
        oRequestHandler.addHeaderEntry('Cookie', Cookie)
    sHtmlContent = oRequestHandler.request()

    # Connection pour passer la limite
    if not 'Déconnexion' in sHtmlContent and ADDON.getSetting('hoster_time2watch_premium') == "true":
        VSlog("Connection")

        data = {'username': ADDON.getSetting('hoster_time2watch_username'), 'pwd': ADDON.getSetting('hoster_time2watch_password')}

        data = urlEncode(data)

        opener = Noredirection()

        opener.addheaders = [('User-Agent', UA)]
        opener.addheaders.append(('Content-Type', 'application/x-www-form-urlencoded'))
        opener.addheaders.append(('Accept-Encoding', 'gzip, deflate'))
        opener.addheaders.append(('Content-Length', str(len(data))))

        response = opener.open("https://time2watch.io/login/", data)
        head = response.info()

        # get cookie
        Cookie = ''
        if 'Set-Cookie' in head:
            oParser = cParser()
            sPattern = '(?:^|,) *([^;,]+?)=([^;,\/]+?);'
            aResult = oParser.parse(str(head['Set-Cookie']), sPattern)
            # print(aResult)
            if (aResult[0] == True):
                for cook in aResult[1]:
                    if 'deleted' in cook[1]:
                        continue
                    Cookie = Cookie + cook[0] + '=' + cook[1] + ';'

        GestionCookie().SaveCookie('time2watch', Cookie)

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.addHeaderEntry('Cookie', Cookie)
        sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="col-lg-4.+?<a href="([^"]+)">.+?affiche_liste" src="([^"]+)".+?alt="([^"]+)".+?<i class="fa fa-tv"></i>([^<]+)<.+?div class="synopsis_hover".+?>([^<]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = URL_MAIN + aEntry[0]
            sThumb = URL_MAIN + aEntry[1]
            sTitle = aEntry[2]
            sQual = aEntry[3].replace(' ', '')
            sDesc = aEntry[4]

            sTitle = sTitle.replace('En streaming', '')

            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oOutputParameterHandler.addParameter('sCookie', Cookie)

            if '/serie/' in sUrl2 or '/anime/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisonEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLink', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            number = re.search('/([0-9]+)', sNextPage).group(1)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Page ' + number + ' >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<a class="light_pagination" href="([^"]+)" aria-label="Next">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]

    return False


def showMoviesLink():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    Cookie = oInputParameterHandler.getValue('sCookie')

    oRequestHandler = cRequestHandler(sUrl)
    if Cookie:
        oRequestHandler.addHeaderEntry('Cookie', Cookie)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<i class="fa fa-download fa-fw"></i>.+?<b>(.+?)</b></a>'
    var = re.search('var hash = (.+?);', sHtmlContent).group(1).replace('"', "").strip('][').split(',')
    url = re.search("document\.getElementById\(\'openlink_\'\+n\).href = '(.+?)';", sHtmlContent).group(1)

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry, VAR in zip(aResult[1], var):
            sUrl2 = URL_MAIN + url.replace("'+nhash+'", VAR)
            sTitle = ('%s [%s]') % (sMovieTitle, aEntry)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sCookie', Cookie)

            oGui.addLink(SITE_IDENTIFIER, 'decryptTime', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSaisonEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    Cookie = oInputParameterHandler.getValue('sCookie')

    oRequestHandler = cRequestHandler(sUrl)
    if Cookie:
        oRequestHandler.addHeaderEntry('Cookie', Cookie)
    sHtmlContent = oRequestHandler.request()

    url = re.search("document\.getElementById\(\'openlink_\'\+n\).href = '(.+?)';", sHtmlContent).group(1)
    oParser = cParser()
    sPattern = '<span style="margin-left: 20px;">(.+?)</span>|<span style="margin-left: 35px;">(.+?)<.+?<span class="fa arrow">|setfatherasseen.+?<i class="fa fa-download fa-fw">.+?<b>(.+?)</b>.+?var hash_.+?= "(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:
            if aEntry[0]:
                ses = aEntry[0]

            elif aEntry[1]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + ses + ' ' + aEntry[1] + '[/COLOR]')

            else:
                sUrl2 = URL_MAIN + url.replace("'+nhash+'", aEntry[3])
                sDisplayTitle = ('%s [%s]') % (sMovieTitle, aEntry[2])

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oOutputParameterHandler.addParameter('sCookie', Cookie)

                oGui.addEpisode(SITE_IDENTIFIER, 'decryptTime', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def getLinkHtml(sHtmlContent):
    if not "Limite atteinte" in sHtmlContent:
        oParser = cParser()
        sPattern = 'style="color: #adadad;"(.+?)no_our_shit_us'
        aResult = oParser.parse(sHtmlContent, sPattern)
        return aResult[1][0]
    return False


def decryptTime():
    oGui = cGui()
    oParser = cParser()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    Cookie = oInputParameterHandler.getValue('sCookie')

    oRequestHandler = cRequestHandler(sUrl)
    if Cookie:
        oRequestHandler.addHeaderEntry('Cookie', Cookie)
    sHtmlContent = oRequestHandler.request()

    if "Test de s" in sHtmlContent:
        sPattern = '<img style="margin: auto; display: block; width: 120px; height: 120px;" src="([^"]+)"/>.+?name="challenge" value="([^"]+)"'
        result = oParser.parse(sHtmlContent, sPattern)
        challenge = result[1][0][0]
        challengeTok = result[1][0][1]

        sPattern = '<img onclick="choose\(\'([^\']+)\'\).+?src="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        Filename = []
        i = 0

        oRequestHandler = cRequestHandler(challenge)
        if Cookie:
            oRequestHandler.addHeaderEntry('Cookie', Cookie)
        sHtmlContent = oRequestHandler.request()

        downloaded_image = xbmcvfs.File("special://home/userdata/addon_data/plugin.video.vstream/challenge.png", 'wb')
        downloaded_image.write(bytearray(sHtmlContent))
        downloaded_image.close()

        for imgURL in aResult[1]:
            oRequestHandler = cRequestHandler(imgURL[1])
            if Cookie:
                oRequestHandler.addHeaderEntry('Cookie', Cookie)
            imgdata = oRequestHandler.request()

            downloaded_image = xbmcvfs.File("special://home/userdata/addon_data/plugin.video.vstream/test" + str(i) + ".png", 'wb')
            downloaded_image.write(bytearray(imgdata))
            downloaded_image.close()
            Filename.append("special://home/userdata/addon_data/plugin.video.vstream/test" + str(i) + ".png")
            i = i + 1

        oSolver = cInputWindow(captcha=Filename, challenge="special://home/userdata/addon_data/plugin.video.vstream/challenge.png")
        retArg = oSolver.get()

        data = "g-recaptcha-response=" + aResult[1][int(retArg)][0] + "&challenge=" + challengeTok

        oRequestHandler = cRequestHandler(sUrl)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Content-Type',  "application/x-www-form-urlencoded")
        oRequestHandler.addHeaderEntry('Content-Length', len(str(data)))
        if Cookie:
            oRequestHandler.addHeaderEntry('Cookie', Cookie)
        oRequestHandler.addParametersLine(data)
        sHtmlContent = getLinkHtml(oRequestHandler.request())
        if sHtmlContent == False:
            dialog().VSok(desc="Limite journalière atteinte, pour continuez à utiliser le site aujourd'hui, il faut utilisez un compte (c'est gratuit)", title="Limites atteintes")

    else:
        sHtmlContent = getLinkHtml(sHtmlContent)

    sPattern = '<img src=.+?<a href="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] == True:
        for aEntry in aResult[1]:
            if 'multiup' in aEntry:
                aResult = cMultiup().GetUrls(aEntry)

                if (aResult):
                    for aEntry in aResult:
                        sHosterUrl = aEntry

                        oHoster = cHosterGui().checkHoster(sHosterUrl)
                        if (oHoster != False):
                            oHoster.setDisplayName(sMovieTitle)
                            oHoster.setFileName(sMovieTitle)
                            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            else:      
                oHoster = cHosterGui().checkHoster(aEntry)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, aEntry, sThumb)

    oGui.setEndOfDirectory()

class cInputWindow(xbmcgui.WindowDialog):
    def __init__(self, *args, **kwargs):
        self.cptloc = kwargs.get('captcha')
        i = 0
        u = 0
        pos = []

        bg_image = 'special://home/addons/plugin.video.vstream/resources/art/background.png'
        check_image = 'special://home/addons/plugin.video.vstream/resources/art/trans_checked.png'

        self.ctrlBackground = xbmcgui.ControlImage(0, 0, 1280, 720, bg_image)
        self.cancelled = False
        self.addControl (self.ctrlBackground)

        self.img = [0]*10

        self.strActionInfo = xbmcgui.ControlLabel(250, 20, 724, 400, 'Veuillez sélectionnez l\'image qui ressemble le plus \n a l\'image qui se trouve le plus a gauche.', 'font40', '0xFFFF00FF')
        self.addControl(self.strActionInfo)

        self.img[0] = xbmcgui.ControlImage(450, 110, 260, 166, self.cptloc[0])
        self.addControl(self.img[0])

        self.img[1] = xbmcgui.ControlImage(450 + 260, 110, 260, 166, self.cptloc[1])
        self.addControl(self.img[1])

        self.img[2] = xbmcgui.ControlImage(450 + 520, 110, 260, 166, self.cptloc[2])
        self.addControl(self.img[2])
        
        self.img[3] = xbmcgui.ControlImage(450, 110 + 166, 260, 166, self.cptloc[3])
        self.addControl(self.img[3])

        self.img[4] = xbmcgui.ControlImage(450 + 260, 110 + 166, 260, 166, self.cptloc[4])
        self.addControl(self.img[4])

        self.img[5] = xbmcgui.ControlImage(450 + 520, 110 + 166, 260, 166, self.cptloc[5])
        self.addControl(self.img[5])

        self.img[6] = xbmcgui.ControlImage(450, 110 + 332, 260, 166,self.cptloc[6])
        self.addControl(self.img[6])

        self.img[7] = xbmcgui.ControlImage(450 + 260, 110 + 332, 260, 166, self.cptloc[7])
        self.addControl(self.img[7])

        self.img[8] = xbmcgui.ControlImage(450 + 520, 110 + 332, 260, 166, self.cptloc[8])
        self.addControl(self.img[8])

        self.img[9] = xbmcgui.ControlImage(100, 80, 260, 166, kwargs.get('challenge'))
        self.addControl(self.img[9])

        self.chk = [0]*9
        self.chkbutton = [0]*9
        self.chkstate = [False]*9

        if 1 == 2:
            self.chk[0] = xbmcgui.ControlCheckMark(450, 110, 260, 166, '1', font='font14', focusTexture=check_image, checkWidth=260, checkHeight=166)
            self.chk[1] = xbmcgui.ControlCheckMark(450 + 260, 110, 260, 166, '2', font='font14', focusTexture=check_image, checkWidth=260, checkHeight=166)
            self.chk[2] = xbmcgui.ControlCheckMark(450 + 520, 110, 260, 166, '3', font='font14', focusTexture=check_image, checkWidth=260, checkHeight=166)

            self.chk[3] = xbmcgui.ControlCheckMark(450, 110 + 166, 260, 166, '4', font='font14', focusTexture=check_image, checkWidth=260, checkHeight=166)
            self.chk[4] = xbmcgui.ControlCheckMark(450 + 260, 110 + 166, 260, 166, '5', font='font14', focusTexture=check_image, checkWidth=260, checkHeight=166)
            self.chk[5] = xbmcgui.ControlCheckMark(450 + 520, 110 + 166, 260, 166, '6', font='font14', focusTexture=check_image, checkWidth=260, checkHeight=166)

            self.chk[6] = xbmcgui.ControlCheckMark(450, 110 + 332, 260, 166, '7', font='font14', focusTexture=check_image, checkWidth=260, checkHeight=166)
            self.chk[7] = xbmcgui.ControlCheckMark(450 + 260, 110 + 332, 260, 166, '8', font='font14', focusTexture=check_image, checkWidth=260, checkHeight=166)
            self.chk[8] = xbmcgui.ControlCheckMark(450 + 520, 110 + 332, 260, 166, '9', font='font14', focusTexture=check_image, checkWidth=260, checkHeight=166)

        else:
            self.chk[0] = xbmcgui.ControlImage(450, 110, 260, 166, check_image)
            self.chk[1] = xbmcgui.ControlImage(450 + 260, 110, 260, 166, check_image)
            self.chk[2] = xbmcgui.ControlImage(450 + 520, 110, 260, 166, check_image)

            self.chk[3] = xbmcgui.ControlImage(450, 110 + 166, 260, 166, check_image)
            self.chk[4] = xbmcgui.ControlImage(450 + 260, 110 + 166, 260, 166, check_image)
            self.chk[5] = xbmcgui.ControlImage(450 + 520, 110 + 166, 260, 166, check_image)

            self.chk[6] = xbmcgui.ControlImage(450, 110 + 332, 260, 166, check_image)
            self.chk[7] = xbmcgui.ControlImage(450 + 260, 110 + 332, 260, 166, check_image)
            self.chk[8] = xbmcgui.ControlImage(450 + 520, 110 + 332, 260, 166, check_image)

            self.chkbutton[0] = xbmcgui.ControlButton(450, 110, 260, 166, '1', font='font1')
            self.chkbutton[1] = xbmcgui.ControlButton(450 + 260, 110, 260, 166, '2', font='font1')
            self.chkbutton[2] = xbmcgui.ControlButton(450 + 520, 110, 260, 166, '3', font='font1')

            self.chkbutton[3] = xbmcgui.ControlButton(450, 110 + 166, 260, 166, '4', font='font1')
            self.chkbutton[4] = xbmcgui.ControlButton(450 + 260, 110 + 166, 260, 166, '5', font='font1')
            self.chkbutton[5] = xbmcgui.ControlButton(450 + 520, 110 + 166, 260, 166, '6', font='font1')

            self.chkbutton[6] = xbmcgui.ControlButton(450, 110 + 332, 260, 166, '7', font='font1')
            self.chkbutton[7] = xbmcgui.ControlButton(450 + 260, 110 + 332, 260, 166, '8', font='font1')
            self.chkbutton[8] = xbmcgui.ControlButton(450 + 520, 110 + 332, 260, 166, '9', font='font1')

        for obj in self.chk:
            self.addControl(obj)
            obj.setVisible(False)
        for obj in self.chkbutton:
            self.addControl(obj)

        self.cancelbutton = xbmcgui.ControlButton(250 + 260 - 70, 620, 140, 50, 'Cancel', alignment=2)
        self.okbutton = xbmcgui.ControlButton(250 + 520 - 50, 620, 100, 50, 'OK', alignment=2)
        self.addControl(self.okbutton)
        self.addControl(self.cancelbutton)

        self.chkbutton[6].controlDown(self.cancelbutton);  self.chkbutton[6].controlUp(self.chkbutton[3])
        self.chkbutton[7].controlDown(self.cancelbutton);  self.chkbutton[7].controlUp(self.chkbutton[4])
        self.chkbutton[8].controlDown(self.okbutton);      self.chkbutton[8].controlUp(self.chkbutton[5])

        self.chkbutton[6].controlLeft(self.chkbutton[8]);  self.chkbutton[6].controlRight(self.chkbutton[7]);
        self.chkbutton[7].controlLeft(self.chkbutton[6]);  self.chkbutton[7].controlRight(self.chkbutton[8]);
        self.chkbutton[8].controlLeft(self.chkbutton[7]);  self.chkbutton[8].controlRight(self.chkbutton[6]);

        self.chkbutton[3].controlDown(self.chkbutton[6]);  self.chkbutton[3].controlUp(self.chkbutton[0])
        self.chkbutton[4].controlDown(self.chkbutton[7]);  self.chkbutton[4].controlUp(self.chkbutton[1])
        self.chkbutton[5].controlDown(self.chkbutton[8]);  self.chkbutton[5].controlUp(self.chkbutton[2])

        self.chkbutton[3].controlLeft(self.chkbutton[5]);  self.chkbutton[3].controlRight(self.chkbutton[4]);
        self.chkbutton[4].controlLeft(self.chkbutton[3]);  self.chkbutton[4].controlRight(self.chkbutton[5]);
        self.chkbutton[5].controlLeft(self.chkbutton[4]);  self.chkbutton[5].controlRight(self.chkbutton[3]);

        self.chkbutton[0].controlDown(self.chkbutton[3]);  self.chkbutton[0].controlUp(self.cancelbutton)
        self.chkbutton[1].controlDown(self.chkbutton[4]);  self.chkbutton[1].controlUp(self.cancelbutton)
        self.chkbutton[2].controlDown(self.chkbutton[5]);  self.chkbutton[2].controlUp(self.okbutton)

        self.chkbutton[0].controlLeft(self.chkbutton[2]);  self.chkbutton[0].controlRight(self.chkbutton[1]);
        self.chkbutton[1].controlLeft(self.chkbutton[0]);  self.chkbutton[1].controlRight(self.chkbutton[2]);
        self.chkbutton[2].controlLeft(self.chkbutton[1]);  self.chkbutton[2].controlRight(self.chkbutton[0]);

        self.cancelled = False
        self.setFocus(self.okbutton)
        self.okbutton.controlLeft(self.cancelbutton);      self.okbutton.controlRight(self.cancelbutton);
        self.cancelbutton.controlLeft(self.okbutton);      self.cancelbutton.controlRight(self.okbutton);
        self.okbutton.controlDown(self.chkbutton[2]);      self.okbutton.controlUp(self.chkbutton[8]);
        self.cancelbutton.controlDown(self.chkbutton[0]);  self.cancelbutton.controlUp(self.chkbutton[6]);

    def get(self):
        self.doModal()
        self.close()
        if not self.cancelled:
            retval = ""
            for objn in range(9):
                if self.chkstate[objn]:
                    retval += ("" if retval == "" else ",") + str(objn)
            return retval

        else:
            return ""

    def anythingChecked(self):
        for obj in self.chkstate:
            if obj:
                return True
        return False

    def onControl(self, control):
        if str(control.getLabel()) == "OK":
            if self.anythingChecked():
                self.close()
        elif str(control.getLabel()) == "Cancel":
            self.cancelled = True
            self.close()
        try:
            if 'xbmcgui.ControlButton' in repr(type(control)):
                index = control.getLabel()
                if index.isnumeric():
                    self.chkstate[int(index)-1] = not self.chkstate[int(index)-1]
                    self.chk[int(index)-1].setVisible(self.chkstate[int(index)-1])

        except:
            pass

    def onAction(self, action):
        if action == 10:
            self.cancelled = True
            self.close()
