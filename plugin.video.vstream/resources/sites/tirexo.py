# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import random
import re
import requests
import time
import xbmc

from resources.lib.comaddon import progress, dialog, VSlog
from resources.lib.config import GestionCookie
from resources.lib.gui.gui import cGui
from resources.lib.gui.hoster import cHosterGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser

# from test.test_socket import try_address


UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

SITE_IDENTIFIER = 'tirexo'
SITE_NAME = '[COLOR violet]Tirexo[/COLOR]'
SITE_DESC = 'Films/Séries/Reportages/Concerts'
# URL_HOST = 'https://www2.tirexo.ai/'


# def getURL():
    # oParser = cParser()
    # oRequestHandler = cRequestHandler(URL_HOST)
    # oRequestHandler.addHeaderEntry('User-Agent', UA)
    # sHtmlContent = oRequestHandler.request()

    # sPattern = '<a class="full-wrap clearfix btn btn-danger" href="([^"]+)">Acc&eacute;der au site</a></div>'
    # aResult = oParser.parse(sHtmlContent, sPattern)
    # if aResult[0]:
        # return aResult[1][0]


#def GetURL_MAIN():
    #ADDON = addon()
    #oInputParameterHandler = cInputParameterHandler()
    #sUrl = oInputParameterHandler.getValue('siteUrl')
    #Sources = oInputParameterHandler.getValue('function')

    # z = oInputParameterHandler.getAllParameter()
    # VSlog(z)

    # quand vstream load tous les sites on passe >> globalSources
    # quand vstream load a partir du menu home on passe >> callplugin
    # quand vstream fabrique une liste de plugin pour menu(load site globalRun and call function search) >> search
    # quand l'url ne contient pas celle déjà enregistrer dans settings et que c'est pas dlprotect on active.
    #if not (Sources == 'callpluging' or Sources == 'globalSources' or Sources == 'search') and not ADDON.getSetting('Tirexo')[6:] in sUrl and not 'dl-protect.' in sUrl and not 'zt-protect.' in sUrl:
        #MemorisedHost = getURL()
        #if MemorisedHost is not None and MemorisedHost != '' :
            #if not 'cf_chl_jschl_tk' in MemorisedHost:
                #ADDON.setSetting('Tirexo', MemorisedHost)
                #VSlog("Tirexo url  >> " + str(MemorisedHost) + ' sauvegarder >> ' + ADDON.getSetting('Tirexo'))
        #else:
            #ADDON.setSetting('Tirexo', URL_HOST)
            #VSlog("Url non changer car égal à None le site peux être surcharger utilisation de >> ADDON.getSetting('Tirexo')")

        #return ADDON.getSetting('Tirexo')
    #else:
        # si pas de zt dans settings on récup l'url une fois dans le site
        #if not ADDON.getSetting('Tirexo') and not (Sources == 'callpluging' or Sources == 'globalSources' or Sources == 'search'):
            #MemorisedHost = getURL()
            #if MemorisedHost is not None and MemorisedHost != '':
                #if not 'cf_chl_jschl_tk' in MemorisedHost:
                    #ADDON.setSetting('Tirexo', MemorisedHost)
                    #VSlog("Tirexo url vide  >> " + str(MemorisedHost) + ' sauvegarder >> ' + ADDON.getSetting('Tirexo'))
            #else:
                #ADDON.setSetting('Tirexo', URL_HOST)
                #VSlog("Url non changer car égal à None le site peux être surcharger utilisation de >> ADDON.getSetting('Tirexo')")

            #return ADDON.getSetting('Tirexo')
        #else:
            #VSlog("Tirexo pas besoin d'url")
            #return ADDON.getSetting('Tirexo')

# Teste pour le moment avec une url fixe.
URL_MAIN = "https://www2.tirexo.ai/"
# URL_MAIN = "https://www.tirexo......./"  # Les regex sont différentes mais il n'y a pas cloudflare
URL_SEARCH_MOVIES = (URL_MAIN + 'index.php?do=search&subaction=search&search_start=0&full_search=1&result_from=1&story=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + 'index.php?do=search&subaction=search&catlist=15&story=', 'showMovies')
URL_SEARCH_ANIMS = (URL_MAIN + 'index.php?do=search&subaction=search&catlist=32&story=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + 'index.php?do=search&subaction=search&catlist=39&story=', 'showMovies')

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_COLLECTION = (URL_MAIN + 'collections/', 'showMovies')
MOVIE_EXCLUS = (URL_MAIN + 'exclus/', 'showMovies')
MOVIE_3D = (URL_MAIN + 'films-bluray-3d/', 'showMovies')
MOVIE_SD = (URL_MAIN + 'films-bluray-hd/', 'showMovies')
MOVIE_MKV = (URL_MAIN + 'films-mkv/', 'showMovies')
MOVIE_HD = (URL_MAIN + 'films-bluray-hd-1080/', 'showMovies')
MOVIE_BDRIP = (URL_MAIN + 'films-dvdrip-bdrip/', 'showMovies')
MOVIE_SDLIGHT = (URL_MAIN + 'hdlight-720/', 'showMovies')
MOVIE_HDLIGHT = (URL_MAIN + 'hdlight-1080/', 'showMovies')
MOVIE_4KL = (URL_MAIN + 'film-ultra-hdlight-x265/', 'showMovies')
MOVIE_4K = (URL_MAIN + 'film-ultra-hd-x265/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'films-gratuit/', 'showMovies')

MOVIE_2010 = (URL_MAIN + 'films-2010-2019/', 'showMovies')
MOVIE_2000 = (URL_MAIN + 'films-2000-2009/', 'showMovies')
MOVIE_1990 = (URL_MAIN + 'films-1990-1999/', 'showMovies')
MOVIE_1980 = (URL_MAIN + 'films-1980-1989/', 'showMovies')
MOVIE_1970 = (URL_MAIN + 'films-1970-1979/', 'showMovies')
MOVIE_1960 = (URL_MAIN + 'films-1960-1969/', 'showMovies')
MOVIE_1950 = (URL_MAIN + 'films-1950-1959/', 'showMovies')
MOVIE_1900 = (URL_MAIN + 'films-1900-1950/', 'showMovies')

MOVIE_GENRES = ('films-gratuit/', 'showGenre')
SERIE_GENRES = ('telecharger-series/', 'showGenre')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_VFS = (URL_MAIN + 'series-vf/', 'showMovies')
SERIE_VF_720 = (URL_MAIN + 'series-vf-en-hd/', 'showMovies')
SERIE_VF_1080 = (URL_MAIN + 'series-vf-1080p/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'series-vostfr/', 'showMovies')
SERIE_VOSTFRS_720 = (URL_MAIN + 'series-vostfr-hd/', 'showMovies')
SERIE_VOSTFRS_1080 = (URL_MAIN + 'series-vostfr-1080p/', 'showMovies')
SERIE_VO = (URL_MAIN + 'series-vo/', 'showMovies')
SERIE_NEWS = (URL_MAIN + 'telecharger-series/', 'showMovies')

ANIM_ANIMS = (True, 'showMenuMangas')
ANIM_VFS = (URL_MAIN + 'animes-vf/', 'showMovies')
ANIM_VF_720 = (URL_MAIN + 'animes-vf-720p/', 'showMovies')
ANIM_VF_1080 = (URL_MAIN + 'animes-vf-1080p/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'animes-vostfr/', 'showMovies')
ANIM_VOSTFRS_720 = (URL_MAIN + 'animes-vostfr-720p/', 'showMovies')
ANIM_VOSTFRS_1080 = (URL_MAIN + 'animes-vostfr-1080p/', 'showMovies')
FILM_ANIM = (URL_MAIN + 'films-animes/', 'showMovies')
ANIM_NEWS = (URL_MAIN + 'animes/', 'showMovies')

DOC_NEWS = (URL_MAIN + 'emissions-tv-documentaires/souscate_doc-Documentaire/', 'showMovies')
SPORT_SPORTS = (URL_MAIN + 'emissions-tv-documentaires/souscate_doc-Sport/', 'showMovies')
TV_NEWS = (URL_MAIN + 'emissions-tv-documentaires/souscate_doc-Émissions+TV/', 'showMovies')
SPECT_NEWS = (URL_MAIN + 'emissions-tv-documentaires/souscate_doc-Spectacle/', 'showMovies')
CONCERT_NEWS = (URL_MAIN + 'musiques-mp3-gratuite/souscat_music-Concerts/', 'showMovies')


# bypass cloudflare avec Selenium

def redi(url):  # Pour la redirection avec /link
    if url:
        try:  # On passe par la méthode request quand cloudflare n'est pas présent
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
                       'Content-Type': 'text/html; charset=UTF-8',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                       'Accept-encoding': 'gzip, deflate, br',
                       'Accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,nl;q=0.6,it;q=0.5,es;q=0.4,de;q=0.3'}
            r = requests.get(url, allow_redirects=False, headers=headers)
            r.status_code
            r.url
            result = r.headers['location']
            return result
        except:
            pass

    try:
        from selenium import webdriver
        from selenium.webdriver.common.driver_utils import get_driver_path
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver import Chrome
        from selenium.webdriver.chrome.options import Options

        # from selenium.webdriver.firefox.options import Options
        # from selenium.webdriver import Firefox

        # from selenium.webdriver.common.by import By
        # from selenium.webdriver.support import expected_conditions as EC

        VSlog("Chargement Selenium ok")

    except:
        pass
    driverPath = get_driver_path('chromedriver')
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(driverPath, options=options)
    browser.get(url)

    # On attends la redirection
    wait = WebDriverWait(browser, 10)
    wait.until(lambda driver: browser.current_url != url)

    current_url = browser.current_url

    browser.close()
    print(current_url)
    return current_url


def resolvenocloudflare(url, cookie):  # Méthode classique
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    if cookie:
        oRequestHandler.addHeaderEntry('Cookie', cookie)
    # oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()
    return sHtmlContent


def cloudflare(url):  # Bypass cloudflare avec selenium

    if url:  # On passe par la méthode classique en cas ou cloudflare n'est pas présent
        try:
            c = GestionCookie().Readcookie('tirexo_com')  # On lie le cookie enregistré
            sHtmlContent = resolvenocloudflare(url, c)  # On passe par la fonction resolvenocloudflare avec l'url et le cookie
            VSlog("cookies encore valables")  # Un log en cas que le cookie est valide
            return sHtmlContent  # On renvoie le contenu html de l'url qui a été validé
        except:  # En cas d'exception /ou erreur
            pass  # On ignore et on passe le code précédent si le cookie n'est plus valide

    try:
        from selenium import webdriver
        from selenium.webdriver.common.driver_utils import get_driver_path
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver import Chrome
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver import DesiredCapabilities

        # from selenium.webdriver.firefox.options import Options
        # from selenium.webdriver import Firefox

        # from selenium.webdriver.common.by import By
        # from selenium.webdriver.support import expected_conditions as EC

        VSlog("Chargement Selenium ok")

    except:
        pass

    CloudflarePassed = False

    if True:
        driverPath = get_driver_path('chromedriver')
        options = Options()

        # options.add_argument("headless")
        # options.add_argument("window-size=1920,1080")
        options.add_argument("'user-agent={}".format(UA))
        # options.add_argument("disable-gpu")

        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True

        browser = webdriver.Chrome(driverPath, options=options, desired_capabilities=capabilities)
    else:
        path = r"C:\Users\XXXX\AppData\Roaming\Kodi\addons\script.module.selenium\bin\geckodriver\win32\geckodriver\geckodriver.exe"
        # path sert pour firefox
        browser = webdriver.Firefox(executable_path=path, options=options, log_path="")

    browser.get(url)

    # On boucle si Cloudflare n'est pas résolu.
    # On loop que 3 fois maxi.
    loop = 0
    while (CloudflarePassed == False):
        if loop > 3:
            break

        # On se sert du cookie pour voir si Cloudflare est résolu
        Cookies = browser.get_cookies()
        if "cf_clearance" in str(Cookies):
            break

        # Si pas de protection CF
        if 'Checking your browser before accessing' not in browser.page_source:
            break

        # On récupere le timeout de maniere dynamique
        try:
            time.sleep(float(re.search(r'submit\(\);\r?\n\s*},\s*([0-9]+)',
                                       browser.page_source).group(1)) / float(1000) + 1)

        except:
            # Sauf sur la nouvelle version où il n'est pas présent
            time.sleep(6)

        VSlog("loop : " + str(loop))

        loop = loop + 1

    VSlog("""Cloudflare Passed, Cookie : """ + str({cookie['name']: cookie['value'] for cookie in browser.get_cookies()})
          + """\n User Agent : """ + browser.execute_script("return navigator.userAgent"))

    # Sauvegarde des cookies
    c = ""
    for cookie in browser.get_cookies():
        c = c + cookie['name'] + '=' + cookie['value'] + ';'
    c = str(c[:-1])

    GestionCookie().SaveCookie('tirexo_com', c)

    page_source = (browser.page_source).encode('utf-8', errors='replace')
    browser.close()

    return page_source


def showInstall():
    xbmc.executebuiltin('InstallAddon(script.module.selenium)')


def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    # oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    # oGui.addDir(SITE_IDENTIFIER, 'showDetail', '[COLOR red]Explication pour le site[/COLOR]', 'films.png', oOutputParameterHandler)

    # oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    # oGui.addDir(SITE_IDENTIFIER, 'showInstall', '[COLOR blue]Cliquer ici pour installer selenium[/COLOR]', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMovies', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuTvShows', 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuAutres', 'Autres', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMovies():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MOVIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher films', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_COLLECTION[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_COLLECTION[1], 'Les collections', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_EXCLUS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_EXCLUS[1], 'Exclus (Films populaires)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SD[1], 'Films (720p)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD[1], 'Films (1080p)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIP[1], 'Films (BDRIP)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4K[1], 'Films (4K)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_MKV[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_MKV[1], 'Films (dvdrip mkv)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_SDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_SDLIGHT[1], 'Films (720p - Light)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HDLIGHT[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HDLIGHT[1], 'Films (1080p - Light)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4KL[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4KL[1], 'Films (4K - light)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'Films (3D)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_2010[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_2010[1], 'Films (2010)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_2000[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_2000[1], 'Films (2000)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1990[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1990[1], 'Films (1990)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1980[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1980[1], 'Films (1980)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1970[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1970[1], 'Films (1970)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1960[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1960[1], 'Films (1960)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1950[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1950[1], 'Films (1950)', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1900[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1900[1], 'Films (1900)', 'films.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuTvShows():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher séries', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries (VF)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF_720[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries 720p (VF)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VF_1080[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFS[1], 'Séries 1080p (VF)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'Séries (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS_720[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS_720[1], 'Séries 720p (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS_1080[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS_1080[1], 'Séries 1080p (VOSTFR)', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SERIE_VO[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VO[1], 'Séries (VO)', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_ANIMS[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher Animes', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Derniers ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], 'Animes (VF)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VF_720[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VF_720[1], 'Animes 720p (VF)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VF_1080[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VF_1080[1], 'Animes 1080p (VF)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], 'Animes (VOSTFR)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS_720[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS_720[1], 'Animes 720p (VOSTFR)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS_1080[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS_1080[1], 'Animes 1080p (VOSTFR)', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', FILM_ANIM[0])
    oGui.addDir(SITE_IDENTIFIER, FILM_ANIM[1], 'Films d\'animes ', 'animes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMenuAutres():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_SEARCH_MISC[0])
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Rechercher autres', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', DOC_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, DOC_NEWS[1], 'Documentaires', 'doc.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPORT_SPORTS[0])
    oGui.addDir(SITE_IDENTIFIER, SPORT_SPORTS[1], 'Sports', 'sport.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', SPECT_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SPECT_NEWS[1], 'Spectacles', 'star.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', CONCERT_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, CONCERT_NEWS[1], 'Concerts', 'music.png', oOutputParameterHandler)

    oOutputParameterHandler.addParameter('siteUrl', TV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, TV_NEWS[1], 'Emissions TV', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showDetail():
    dialog().VStextView(desc="""Explication pour le changement:
Nous avons remarqué que ces derniers temps nous avons beaucoup de problèmes avec cloudflare.
C'est pourquoi nous avons changé de méthode pour passer la protection.
Nous utiliserons votre navigateur afin de récupérer le bon contenu du site et non cloudflare
En aucun cas nous n'utiliseront vos données confidentielles.


- Pour avoir plus d'information rendez vous sur notre github officiel:
https://github.com/Kodi-vStream/venom-xbmc-addons.
- Pour l'installation et le fonctionnement de Selenium:
https://github.com/Kodi-vStream/venom-xbmc-addons/issues/2948.


Le fonctionnement:
Une fenêtre va s'ouvrir pour ouvrir un serveur local(et aussi le navigateur de temps en temps) et récupérer le contenu
du site. Veuillez ne pas le(s) fermer(s) il(s) se fermera(ont) automatiquement.
Pour le navigateur nous passons par Google Chrome car c'est le plus simple à configurer malheureusement.
Si vous n'avez pas Google Chrome alors ça ne fonctionnera pas donc je vous conseille de l'installer à jour important !!!
Veuillez noter que nous réfléchissons à une solution pour utiliser les autres navigateurs


PS:
Si Jamais de temps en temps ça ne passe pas retentez une deuxième fois.
Veuillez noter aussi qu'il vous faut un ordinateur Windows ou linux (Mac est incompatible pour l'instant).
Pour les appareils de types Android, Ios, Libreelec, Xbox et autres ne sont pas compatible avec Selenium et c'est
impossible de résoudre ce problème désolé.

                                        Merci d'avoir lu notre explication
                                        Vive vStream !!!!""", title="Fonctionnement du site")


def showSearch():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sUrl + sSearchText  # + '&search_start=0'
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return


def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    URL_MOVIES = URL_MAIN + sUrl + 'genre-'

    listeGenres = ['Action', 'Animation', 'Arts Martiaux', 'Aventure', 'Biopic', 'Bollywood', 'Comédie Dramatique',
                   'Comédie Musicale', 'Comédie', 'Documentaire', 'Drame', 'Epouvante-horreur', 'Espionnage',
                   'Famille', 'Fantastique', 'Guerre', 'Historique', 'Horreur', 'Musical', 'Péplum',
                   'Policier', 'Romance', 'Science Fiction', 'Thriller', 'Western']

    oOutputParameterHandler = cOutputParameterHandler()
    for genre in listeGenres:
        oOutputParameterHandler.addParameter('siteUrl', URL_MOVIES + genre.replace(' ', '%20') + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', genre, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch=''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    if sSearch:
        sUrl = sSearch

    if sSearch or "index" in sUrl:  # en mode recherche
        sPattern = 'class="mov-t nowrap" href="(https://www.tirexo.pro/films.+?|https://www.tirexo.pro/telecharger-series.+?|https://www.tirexo.pro/animes.+?|https://www.tirexo.pro/emissions-tv-documentaires.+?)" title="([^"]+).+?data-content="([^"]+).+?<img src="/([^"]+).+?<div style="height: 51px" class="mov-c nowrap'
    elif 'collections/' in sUrl:
        sPattern = 'class="mov-t nowrap" href=".+?<img src="\/([^"]+)" width="200px" height="320px" title="([^"]+).+?data-link="([^"]+)'
    else:
        sPattern = 'class="mov-t nowrap" href="([^"]+)">  <.+?data-content="([^"]+).+?img src="([^"]+).+?title="([^"]+)'

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    aResult = oParser.parse(sHtmlContent, sPattern)
    # VSlog(aResult)

    titles = set()
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if 'collections/' in sUrl:
                sThumb = aEntry[0]
                sTitle = aEntry[1]
                sUrl2 = aEntry[2]
                sDesc = ''
            elif sSearch or 'index' in sUrl:
                sUrl2 = aEntry[0]
                sTitle = aEntry[1]
                sDesc = aEntry[2]
                sThumb = URL_MAIN + aEntry[3]
            else:
                sUrl2 = aEntry[0]
                sDesc = aEntry[1]
                sThumb = URL_MAIN + aEntry[2]
                sTitle = aEntry[3]

                # Enlever les films en doublons (même titre)
                # il s'agit du même film dans une autre qualité qu'on retrouvera au moment du choix de la qualité
            key = sTitle
            if key in titles:
                continue
            titles.add(key)

            # sDesc = re.sub('<[^<]+?>', '', sDesc)
            sDisplayTitle = sTitle

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            if 'series' in sUrl2 or 'animes' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            elif 'collections/' in sUrl:
                oGui.addMoviePack(SITE_IDENTIFIER, 'showCollec', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        if 'index' in sUrl:
            sPattern = '<a name="nextlink".+?javascript:list_submit\((.+?)\)'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', re.sub('search_start=(\d+)', 'search_start=' + str(aResult[1][0]), sUrl))
                number = re.search('([0-9]+)', aResult[1][0]).group(1)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + number, oOutputParameterHandler)
        else:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                number = re.search('/page/([0-9]+)', sNextPage).group(1)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', 'Page ' + number, oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()


def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = 'href="([^"]+)"><span class="fa fa-arrow-right">'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        nextPage = aResult[1][0]
        if not nextPage.startswith('https'):
            nextPage = URL_MAIN[:-1] + nextPage
        return nextPage
    return False


def showCollec():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sPattern = 'class="mov-t nowrap" href="([^"]+).+?data-content="([^"]+).+?<img src="/([^"]+).+?title="([^"]+)'

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    aResult = oParser.parse(sHtmlContent, sPattern)

    titles = set()
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[0]
            sDesc = aEntry[1]
            sThumb = aEntry[2]
            sTitle = aEntry[3]

            # Enlever les films en doublons (même titre)
            # il s'agit du même film dans une autre qualité qu'on retrouvera au moment du choix de la qualité
            key = sTitle
            if key in titles:
                continue
            titles.add(key)

            sDesc = re.sub('<[^<]+?>', '', sDesc)
            sDisplayTitle = sTitle

            if not sThumb.startswith('http'):
                sThumb = URL_MAIN[:-1] + sThumb

            if not sUrl2.startswith('http'):
                sUrl2 = URL_MAIN[:-1] + sUrl2

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)

            oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLinks', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()


def showMoviesLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    # Affichage du texte
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles pour ce film:[/COLOR]')

    # récupération du Synopsis
    sPattern = '<span data-slice="200" itemprop="description">(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if aResult[0]:
        sDesc = aResult[1][0]
        sDesc = sDesc.replace('<span>', '').replace('</span>', '')
        sDesc = sDesc.replace('<b>', '').replace('</b>', '')
        sDesc = sDesc.replace('<i>', '').replace('</i>', '')
        sDesc = sDesc.replace('<br>', '').replace('<br />', '')

    # on recherche d'abord la qualité courante
    sPattern = 'couleur-qualitesz"> *Qualité (.+?) <.+?"couleur-languesz">(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sTitle = sMovieTitle
    if (aResult[0]):
        sQual = aResult[1][0][0]
        sLang = aResult[1][0][1]
        sTitle = ('%s [%s] (%s)') % (sMovieTitle, sQual, sLang)

    # On ajoute le lien même si on n'a pas réussi à déterminer la qualité
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oOutputParameterHandler.addParameter('sDesc', sDesc)

    oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    # on regarde si dispo dans d'autres qualités
    sPattern = '<a href="([^"]+)"><span class="otherquality">.+?<b>([^<>]+)</b>.+?<b>([^<>]+)</b>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:
            sUrl2 = aEntry[0]
            sQual = aEntry[1]
            sLang = aEntry[2]
            sTitle = ('%s [%s] %s') % (sMovieTitle, sQual, sLang)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, sDesc, oOutputParameterHandler)

    # Qualité STREAMING
    sPattern = '<a rel=\'nofollow\' class=\'streaming\' href="([^"]+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        sUrl2 = URL_MAIN + aResult[1][0]
        sTitle = ('%s [STREAMING]') % (sMovieTitle)

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl2)
        oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
        oOutputParameterHandler.addParameter('sThumb', sThumb)
        oOutputParameterHandler.addParameter('sDesc', sDesc)
        oGui.addLink(SITE_IDENTIFIER, 'showHostersLink', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSeriesLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    # Affichage du texte
    oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Qualités disponibles pour cette saison :[/COLOR]')

    # récupération du Synopsis
    try:
        sPattern = '<span data-slice="200" itemprop="description">(.+?)</span>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if aResult[0]:
            sDesc = aResult[1][0]
            sDesc = sDesc.replace('<span>', '').replace('</span>', '')
            sDesc = sDesc.replace('<b>', '').replace('</b>', '')
            sDesc = sDesc.replace('<i>', '').replace('</i>', '')
            sDesc = sDesc.replace('<br>', '').replace('<br />', '')
    except:
        pass

    # Mise à jour du titre
    sPattern = '<h2>T.+?charger <b itemprop="name">(.+?)</b>.+?>(.+?)</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    sTitle = sMovieTitle
    if (aResult[0]):
        sTitle = aResult[1][0][0] + " " + aResult[1][0][1]

    numSaison = str(aResult[1][0][1]).lower().replace("saison", "").strip()
    saisons = []
    saisons.append(numSaison)

    # on recherche d'abord la qualité courante
    sPattern = 'couleur-qualitesz">Qualit.+? (.+?) <.+?couleur-languesz">(.+?)</span><br>.+?"couleur-seriesz">(.+?)\['
    aResult = oParser.parse(sHtmlContent, sPattern)

    sDisplayTitle = sTitle
    if (aResult[0]):
        sQual = aResult[1][0][0]
        sLang = aResult[1][0][1]
        sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sLang)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oOutputParameterHandler.addParameter('sDesc', sDesc)
    oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

    # on regarde si dispo dans d'autres qualités
    sHtmlContent1 = CutQual(sHtmlContent)
    sPattern1 = '<a href="([^"]+)"><span class="otherquality">.+?<b>([^"]+)</b>.+?<b>([^"]+)</b>.+?<b> (.+?)<'
    aResult1 = oParser.parse(sHtmlContent1, sPattern1)

    otherSaison = False

    if (aResult1[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult1[1]:
            # Si saison différente
            sSaison = aEntry[1].strip()
            if numSaison != sSaison:
                otherSaison = True
                continue

            sQual = aEntry[2]
            sLang = aEntry[3]
            sDisplayTitle = ('%s [%s] %s') % (sTitle, sQual, sLang)

            sUrl = aEntry[0]
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesHosters', sDisplayTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

    # on regarde si dispo d'autres saisons
    if (otherSaison):

        # Affichage du titre
        oGui.addText(SITE_IDENTIFIER, '[COLOR olive]Autres saisons disponibles pour cette série :[/COLOR]')

        # Une ligne par saison, pas besoin d'afficher les qualités ici
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult1[1]:

            sSaison = aEntry[1].strip()
            if sSaison in saisons:
                continue
            saisons.append(sSaison)
            sSaison = 'Saison ' + sSaison
            sDisplayTitle = ('%s %s') % (sMovieTitle, sSaison)

            sUrl = aEntry[0]

            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addEpisode(SITE_IDENTIFIER, 'showSeriesLinks', sDisplayTitle, 'series.png', sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')
    # oGui.addText(SITE_IDENTIFIER, '[COLOR blue]Veuillez attendre que le navigateur se ferme tout seul [/COLOR]')
    # oGui.addText(SITE_IDENTIFIER, '[COLOR blue]Pour qu\'il puisse récupérer automatiquement le bon lien [/COLOR]')

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()

    # Ajout des liens DL
    # Gere si un Hoster propose plusieurs liens
    # Retire les resultats proposés en plusieurs parties (ce sont des .rar)
    sPattern = '<th scope="col" class="no-sort"><img src=.+?>([^<]+)</th>|class=\'download\'.+?href=\'([^\']+)\'>T.+?charger <'
    aResult = oParser.parse(sHtmlContent, sPattern)
    # VSlog(aResult)

    if (aResult[0] == True):
        oOutputParameterHandler = cOutputParameterHandler()
        for aEntry in aResult[1]:

            sHoster = re.sub('\.\w+', '', aEntry[0])

            # filtrer les hosts connus
            oHoster = cHosterGui().checkHoster(sHoster)
            if not oHoster:
                continue

            sUrl2 = URL_MAIN[:-1] + aEntry[1]
            sTitle = ('%s [COLOR coral]%s[/COLOR]') % (sMovieTitle, sHoster)

            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addLink(SITE_IDENTIFIER, 'Display_protected_link', sTitle, sThumb, sDesc, oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showHostersLink():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = 'src="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        if not aResult[1][0].startswith('http'):
            sHosterUrl = "https:" + aResult[1][0]
        else:
            sHosterUrl = aResult[1][0]

        oHoster = cHosterGui().checkHoster(sHosterUrl)
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle)
            oHoster.setFileName(sMovieTitle)
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def showSeriesHosters():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    # oGui.addText(SITE_IDENTIFIER, '[COLOR blue]Veuillez attendre que le navigateur se ferme tout seul [/COLOR]')
    # oGui.addText(SITE_IDENTIFIER, '[COLOR blue]Pour qu\'il puisse récupérer automatiquement le bon lien [/COLOR]')

    oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<th scope="col" class="no-sort"><img alt=.+?>([^<>]+)</th>|href=\'([^\']+?)\'>Episode ([^>]+)<'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):

        for aEntry in aResult[1]:
            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + re.sub('\.\w+', '', aEntry[0]) + '[/COLOR]')

            else:
                sUrl2 = URL_MAIN[:-1] + aEntry[1]
                sTitle = sMovieTitle + ' E' + aEntry[2].replace('FINAL ', '')
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addLink(SITE_IDENTIFIER, 'Display_protected_link', sTitle, sThumb, sDesc, oOutputParameterHandler)

        oGui.setEndOfDirectory()
    else:   # certains films mals classés apparaissent dans les séries
        showHosters()


def Display_protected_link():
    # VSlog('Display_protected_link')
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    # Ne marche pas
    if (False):
        code = {'123455600123455602123455610123455615': 'http://uptobox.com/',
                '1234556001234556071234556111234556153': 'http://turbobit.net/',
                '123455600123455605123455615': 'http://ul.to/',
                '123455600123455608123455610123455615': 'http://nitroflare.com/',
                '123455601123455603123455610123455615123455617': 'https://1fichier.com/?',
                '123455600123455606123455611123455615': 'http://rapidgator.net/'}

        for k in code:
            match = re.search(k + '(.+)$', sUrl)
            if match:
                sHosterUrl = code[k] + match.group(1)
                sHosterUrl = sHosterUrl.replace('123455615', '/')
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)
                oGui.setEndOfDirectory()
                return

    if 'link' in sUrl:
        # Temporairement car la flemme de se battre avec les redirections
        # oRequestHandler = cRequestHandler(sUrl)
        # oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler = cRequestHandler(sUrl.replace(' ', '%20'))
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
        oRequestHandler.request()
        sUrl = oRequestHandler.getRealUrl()
        # VSlog(sUrl)

    if "journaldupirate" in sUrl:
        sHtmlContent = DecryptDlProtecte(sUrl)
        # VSlog(sHtmlContent)

        if sHtmlContent:
            # Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotecte = (True, [sHtmlContent])
            else:
                sPattern_dlprotecte = '<div class="alert">.+?<a href="(.+?)"'
                aResult_dlprotecte = oParser.parse(sHtmlContent, sPattern_dlprotecte)

        else:
            dialog().VSok('Erreur de décryptage du lien')
            aResult_dlprotecte = (False, False)

    # Si lien normal
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotecte = (True, [sUrl])

    if (aResult_dlprotecte[0]):

        episode = 1

        for aEntry in aResult_dlprotecte[1]:
            sHosterUrl = aEntry

            sTitle = sMovieTitle
            if len(aResult_dlprotecte[1]) > 1:
                sTitle = sMovieTitle + ' episode ' + episode

            episode += 1

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()


def CutQual(sHtmlContent):
    oParser = cParser()
    sPattern = 'Qualit.+?galement disponibles pour cette saison:</span><br>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        return aResult[1][0]
    else:
        return sHtmlContent

    return ''


def CutSais(sHtmlContent):
    oParser = cParser()
    sPattern = '"otherversionsspan">Saisons.+?galement disponibles pour cette série:(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0]):
        return aResult[1][0]
    return ''


def DecryptDlProtecte(url):  # Passe par Selenium
    VSlog('DecryptDlProtecte : ' + url)

    if not (url):
        return ''
    try:
        from selenium import webdriver
        from selenium.webdriver.common.driver_utils import get_driver_path
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver import Chrome
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC

        # from selenium.webdriver.firefox.options import Options
        # from selenium.webdriver import Firefox

        VSlog("Chargement Selenium ok")

    except:
        pass

    """ Selenium est désactivé car dl protect ne l'utilise plus mais laissé le code quand même"""

    # CloudflarePassed = False
    # driverPath = get_driver_path('chromedriver')
    # options = Options()
    # options.headless = True # Faut le laisser comme ça sinon ça ne fonctionne pas
    # browser = webdriver.Chrome(driverPath, options=options)
    # browser.get(url)

    # On boucle si Cloudflare n'est pas résolu.
    # On loop que 3 fois maxi.
    # loop = 0
    # while CloudflarePassed == False:
        # if loop > 3:
            # break

        # On se sert du cookie pour voir si Cloudflare est résolu
        # Cookies = browser.get_cookies()
        # if "cf_clearance" in str(Cookies):
            # break

        # On récupere le timeout de maniere dynamique
    # try:
        # time.sleep(float(
                    # re.search(
                        # r'submit\(\);\r?\n\s*},\s*([0-9]+)',
                        # browser.page_source
                    # ).group(1)
                # ) / float(1000) + 1)

    # except:
        # Sauf sur la nouvelle version où il n'est pas présent
        # time.sleep(6)

    # loop = loop + 1

    # browser.find_element(By.NAME, "submit").click()
    # page_source = (browser.page_source).encode('utf-8', errors='replace')
    # browser.close()
    # print(page_source)
    # VSlog(page_source)
    # return page_source

    """ Nouvelle méthode pour dl protect qui passe par requests"""
    s = requests.Session()

    response = s.get(url)
    sHtmlContent = str(response.content)
    cookie_string = "; ".join([str(x) + "=" + str(y) for x, y in s.cookies.items()])

    sPattern = 'type="hidden" name="_token" value="(.+?)">'
    aResult = re.search(sPattern, sHtmlContent).group(1)

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('Host', url.split('/')[2])
    oRequestHandler.addHeaderEntry('Referer', url)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Content-Length', len(str("_token=" + aResult + "&getlink=1")))
    oRequestHandler.addHeaderEntry('Content-Type', "application/x-www-form-urlencoded")
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    oRequestHandler.addHeaderEntry('Cookie', cookie_string)
    oRequestHandler.addParameters("_token", aResult)
    oRequestHandler.addParametersLine("_token=" + aResult + "&getlink=1")

    sHtmlContent = oRequestHandler.request()

    return sHtmlContent


def exectProtect(cookies, url):  # Ne sert plus
    # Tout ca a virer et utiliser oRequestHandler.addMultipartFiled('sess_id': sId, 'upload_type': 'url', 'srv_tmp_url': sTmp) quand ca marchera
    import string
    _BOUNDARY_CHARS = string.digits
    boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(30))
    multipart_form_data = {'hidden': 'continuer'}
    data, headersMulti = encode_multipart(multipart_form_data, {}, boundary)

    # 2 eme requete pour avoir le lien
    oRequestHandler = cRequestHandler(url)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('Host', url.split('/')[2])
    oRequestHandler.addHeaderEntry('Referer', url)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Content-Length', headersMulti['Content-Length'])
    oRequestHandler.addHeaderEntry('Content-Type', headersMulti['Content-Type'])
    oRequestHandler.addHeaderEntry('Cookie', cookies)
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')

    oRequestHandler.addParametersLine(data)

    sHtmlContent = oRequestHandler.request()
    return sHtmlContent

# ******************************************************************************
# from http://code.activestate.com/recipes/578668-encode-multipart-form-data-for-uploading-files-via/


"""Encode multipart form data to upload files via POST."""


def encode_multipart(fields, files, boundary):
    r"""Encode dict of form fields and dict of files as multipart/form-data.
    Return tuple of (body_string, headers_dict). Each value in files is a dict
    with required keys 'filename' and 'content', and optional 'mimetype' (if
    not specified, tries to guess mime type or uses 'application/octet-stream').

    >>> body, headers = encode_multipart({'FIELD': 'VALUE'},
    ...                                  {'FILE': {'filename': 'F.TXT', 'content': 'CONTENT'}},
    ...                                  boundary='BOUNDARY')
    >>> print('\n'.join(repr(l) for l in body.split('\r\n')))
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FIELD"'
    ''
    'VALUE'
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FILE"; filename="F.TXT"'
    'Content-Type: text/plain'
    ''
    'CONTENT'
    '--BOUNDARY--'
    ''
    >>> print(sorted(headers.items()))
    [('Content-Length', '193'), ('Content-Type', 'multipart/form-data; boundary=BOUNDARY')]
    >>> len(body)
    193
    """

    import mimetypes
    import string

    _BOUNDARY_CHARS = string.digits

    def escape_quote(s):
        return s.replace('"', '\\"')

    lines = []

    for name, value in fields.items():
        lines.extend(('-----------------------------{0}'.format(boundary),
                      'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name)), '', str(value),
                      '-----------------------------{0}--'.format(boundary), ''))

    for name, value in files.items():
        filename = value['filename']
        if 'mimetype' in value:
            mimetype = value['mimetype']
        else:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        lines.extend((
            '--{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name), escape_quote(filename)),
            'Content-Type: {0}'.format(mimetype),
            '',
            value['content']))

    body = '\r\n'.join(lines)

    headers = {'Content-Type': 'multipart/form-data; boundary=---------------------------{0}'.format(boundary),
               'Content-Length': str(len(body))}

    return (body, headers)
