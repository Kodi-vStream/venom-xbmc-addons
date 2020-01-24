#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#17/12/18
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import GestionCookie
from resources.lib.recaptcha import ResolveCaptcha
from resources.lib.comaddon import progress, dialog, xbmc, xbmcgui, VSlog

import re, urllib

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'

SITE_IDENTIFIER = 'cinemegatoil_org'
SITE_NAME = 'CineMegaToil'
SITE_DESC = 'Films - Films HD'

URL_MAIN = 'https://www.cinemegatoil.org/'

MOVIE_NEWS = (URL_MAIN + 'film', 'showMovies')
MOVIE_MOVIE = ('http://', 'load')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?do=search&mode=advanced&subaction=search&titleonly=3&story=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?do=search&mode=advanced&subaction=search&titleonly=3&story=', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)


    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'action'] )
    liste.append( ['Animation', URL_MAIN + 'animation'] )
    liste.append( ['Arts-martiaux', URL_MAIN + 'arts-martiaux'] )
    liste.append( ['Aventure', URL_MAIN + 'aventure'] )
    liste.append( ['Biopic', URL_MAIN + 'biopic'] )
    liste.append( ['Comédie', URL_MAIN + 'comedie'] )
    liste.append( ['Comédie musicale', URL_MAIN + 'comedie-musicale'] )#l'url sur le site n'est pas bonne
    liste.append( ['Documentaire', URL_MAIN + 'documentaire'] )
    liste.append( ['Drame', URL_MAIN + 'drame'] )
    liste.append( ['Epouvante-horreur', URL_MAIN + 'epouvante-horreur'] )
    liste.append( ['Espionnage', URL_MAIN + 'espionnage'] )
    liste.append( ['Exclu', URL_MAIN + 'exclu'] )
    liste.append( ['Famille', URL_MAIN + 'famille'] )
    liste.append( ['Fantastique', URL_MAIN + 'fantastique'] )
    liste.append( ['Guerre', URL_MAIN + 'guerre'] )
    liste.append( ['Historique', URL_MAIN + 'historique'] )
    liste.append( ['Musical', URL_MAIN + 'musical'] )
    liste.append( ['Policier', URL_MAIN + 'policier'] )
    liste.append( ['Romance', URL_MAIN + 'romance'] )
    liste.append( ['Science-fiction', URL_MAIN + 'science-fiction'] )
    liste.append( ['Thriller', URL_MAIN + 'thriller'] )
    liste.append( ['Vieux Film', URL_MAIN + 'vieux-film'] )
    liste.append( ['Western', URL_MAIN + 'western'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        if URL_SEARCH[0] in sSearch:
            sUrl = sSearch
        else:
            sUrl = URL_SEARCH[0] + sSearch
        sUrl = sUrl.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = 'class="poster.+?img src="([^"]+)".+?class="quality">([^<]+)<\/div>.+?class="title"><a href="([^"]+)".+?title="([^"]+)".+?class="label">Ann.+?<a href.+?>([^<]+)</a>.+?class="shortStory">([^<]+)</div>'
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

            sUrl2 = aEntry[2]
            sThumb = aEntry[0]
            if sThumb.startswith('//'):
                sThumb = 'http:' + sThumb

            sTitle = aEntry[3]
            sQual = aEntry[1]
            sYear = aEntry[4]
            sDesc = aEntry[5]
            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sYear)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sDesc', sDesc)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Suivant >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="prev-next">.+?href="([^"]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return  aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sDesc = oInputParameterHandler.getValue('sDesc')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #Vire les bandes annonces
    sHtmlContent = sHtmlContent.replace('src="https://www.youtube.com/', '')

    #sHtmlContent = oParser.abParse(sHtmlContent, '<div class="tcontainer video-box">', '<div class="tcontainer video-box" id=')

    sPattern = '<b>([^"]+)</b><tr> <br>|(?:<a class="" rel="noreferrer" href="([^"]+)".+?<img src="/templates/Flymix/images/(.+?).png" /> *</a>|<a href="([^"]+)" >([^"]+)</a>)'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        oGui.addText(SITE_IDENTIFIER, sMovieTitle)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            else:
                if aEntry[3]:
                    try:
                        sHost, sTitle = aEntry[4].split('-',1)
                        sHost = '[COLOR coral]' + sHost + '[/COLOR]'
                        sUrl = aEntry[3]
                    except ValueError:
                        sHost = '[COLOR coral]' + aEntry[4].capitalize() + '[/COLOR]'
                        sHost = re.sub('\.\w+', '', sHost)
                        sUrl = aEntry[3]
                else:
                    sHost = '[COLOR coral]' + aEntry[2].capitalize() + '[/COLOR]'
                    sHost = re.sub('\.\w+', '', sHost)
                    sUrl = aEntry[1]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oOutputParameterHandler.addParameter('sDesc', sDesc)
                oGui.addLink(SITE_IDENTIFIER, 'Display_protected_link', sHost, sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def Display_protected_link():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')

    if 'ouo' in sUrl:
        sHosterUrl = DecryptOuo(sUrl)
        if (sHosterUrl):
            sTitle = sMovieTitle

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

        oGui.setEndOfDirectory()

    #Est ce un lien dl-protect ?
    if '/l.k.s/' in sUrl:
        sHtmlContent = DecryptddlProtect(sUrl)

        if sHtmlContent:
            #Si redirection
            if sHtmlContent.startswith('http'):
                aResult_dlprotect = (True, [sHtmlContent])
            else:
                sPattern_dlprotect = '<p><a href="(.+?)">.+?</a></p>'
                aResult_dlprotect = oParser.parse(sHtmlContent, sPattern_dlprotect)

        else:
            oDialog = dialog().VSok('Désolé, problème de captcha.\n Veuillez en rentrer un directement sur le site, le temps de réparer')
            aResult_dlprotect = (False, False)

    elif 'keeplinks' in sUrl:
        oDialog = dialog().VSinfo('Keeplinks non pris en charge', 'cinemegatoil', 10)
    #Si lien normal
    else:
        if not sUrl.startswith('http'):
            sUrl = 'http://' + sUrl
        aResult_dlprotect = (True, [sUrl])

    if (aResult_dlprotect[0]):
        for aEntry in aResult_dlprotect[1]:
            sHosterUrl = aEntry

            sTitle = sMovieTitle

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()

def DecryptddlProtect(url):
    #VSlog 'entering DecryptddlProtect'
    if not (url): return ''

    #Get host
    tmp = url.split('/')
    host = tmp[0] + '//' + tmp[2] + '/' + tmp[3] + '/'
    host1 = tmp[2]

    cookies = ''
    dialogs = dialog()
    #try to get previous cookie
    cookies = GestionCookie().Readcookie('cinemegatoil_org')

    oRequestHandler = cRequestHandler(url)
    if cookies:
        oRequestHandler.addHeaderEntry('Cookie', cookies)
    sHtmlContent = oRequestHandler.request()

    #A partir de la on a les bon cookies pr la protection cloudflare

    #Si ca demande le captcha
    if 'Vérification Captcha:' in sHtmlContent:
        if cookies:
            GestionCookie().DeleteCookie('cinemegatoil_org')
            oRequestHandler = cRequestHandler(url)
            sHtmlContent = oRequestHandler.request()

        s = re.findall('<img src="([^<>"]+?)" /><br />', sHtmlContent)
        if host in s[0]:
            image = s[0]
        else:
            image = host + s[0]

        captcha,cookies2 = get_response(image, cookies)
        cookies = cookies2.replace(';', '')

        oRequestHandler = cRequestHandler(url)
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Host',host1)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4')
        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('Cookie', cookies)
        oRequestHandler.addHeaderEntry('Referer', url)

        oRequestHandler.addParameters('submit1', 'Submit')
        oRequestHandler.addParameters('security_code', captcha)

        sHtmlContent = oRequestHandler.request()

        if 'Code de securite incorrect' in sHtmlContent:
            dialogs.VSinfo("Mauvais Captcha")
            return 'rate'

        if 'Veuillez recopier le captcha ci-dessus' in sHtmlContent:
            dialogs.VSinfo("Rattage")
            return 'rate'

        #si captcha reussi
        #save cookies
        GestionCookie().SaveCookie('cinemegatoil_org', cookies)

    return sHtmlContent

def get_response(img,cookie):
    #on telecharge l'image
    import xbmcvfs

    dialogs = dialog()

    filename = "special://home/userdata/addon_data/plugin.video.vstream.dev/Captcha.raw"
    #PathCache = xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream.dev').getAddonInfo("profile"))
    #filename  = os.path.join(PathCache, 'Captcha.raw')

    hostComplet = re.sub(r'(https*:\/\/[^/]+)(\/*.*)', '\\1', img)
    host = re.sub(r'https*:\/\/', '', hostComplet)
    url = img

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.addHeaderEntry('User-Agent' , UA)
    #oRequestHandler.addHeaderEntry('Referer', url)
    oRequestHandler.addHeaderEntry('Cookie', cookie)

    htmlcontent = oRequestHandler.request()

    NewCookie = oRequestHandler.GetCookies()

    downloaded_image = xbmcvfs.File(filename, 'wb')
    #downloaded_image = file(filename, "wb")
    downloaded_image.write(htmlcontent)
    downloaded_image.close()

#on affiche le dialogue
    solution = ''

    if (True):
        ####nouveau captcha
        try:
            ##affichage du dialog perso
            class XMLDialog(xbmcgui.WindowXMLDialog):
                #"""
                #Dialog class for captcha
                #"""
                def __init__(self, *args, **kwargs):
                    xbmcgui.WindowXMLDialog.__init__(self)
                    pass

                def onInit(self):
                    #image background captcha
                    self.getControl(1).setImage(filename.encode("utf-8"), False)
                    #image petit captcha memory fail
                    self.getControl(2).setImage(filename.encode("utf-8"), False)
                    self.getControl(2).setVisible(False)
                    ##Focus clavier
                    self.setFocus(self.getControl(21))

                def onClick(self, controlId):
                    if controlId == 20:
                        #button Valider
                        solution = self.getControl(5000).getLabel()
                        xbmcgui.Window(10101).setProperty('captcha', solution)
                        self.close()
                        return

                    elif controlId == 30:
                        #button fermer
                        self.close()
                        return

                    elif controlId == 21:
                        #button clavier
                        self.getControl(2).setVisible(True)
                        kb = xbmc.Keyboard(self.getControl(5000).getLabel(), '', False)
                        kb.doModal()

                        if (kb.isConfirmed()):
                            self.getControl(5000).setLabel(kb.getText())
                            self.getControl(2).setVisible(False)
                        else:
                            self.getControl(2).setVisible(False)

                def onFocus(self, controlId):
                    self.controlId = controlId

                def _close_dialog(self):
                    self.close()

                def onAction(self, action):
                    #touche return 61448
                    if action.getId() in (9, 10, 11, 30, 92, 216, 247, 257, 275, 61467, 61448):
                        self.close()

            path = "special://home/addons/plugin.video.vstream.dev"
            #path = cConfig().getAddonPath().decode("utf-8")
            wd = XMLDialog('DialogCaptcha.xml', path, 'default', '720p')
            wd.doModal()
            del wd
        finally:

            solution = xbmcgui.Window(10101).getProperty('captcha')
            if solution == '':
                dialogs.VSinfo("Vous devez taper le captcha")

    else:
        #ancien Captcha
        try:
            img = xbmcgui.ControlImage(450, 0, 400, 130, filename.encode("utf-8"))
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
            #xbmc.sleep(3000)
            kb = xbmc.Keyboard('', 'Tapez les Lettres/chiffres de l\'image', False)
            kb.doModal()
            if (kb.isConfirmed()):
                solution = kb.getText()
                if solution == '':
                    dialogs.VSinfo("Vous devez taper le captcha")
            else:
                dialogs.VSinfo("Vous devez taper le captcha")
        finally:
            wdlg.removeControl(img)
            wdlg.close()

    return solution, NewCookie

def DecryptOuo(sUrl):
    urlOuo = sUrl
    if not '/fbc/' in urlOuo:
        urlOuo = urlOuo.replace('io/', 'io/fbc/').replace('press/', 'press/fbc/')

    oRequestHandler = cRequestHandler(urlOuo)
    sHtmlContent = oRequestHandler.request()
    Cookie = oRequestHandler.GetCookies()

    key = re.search('sitekey: "(.+?)"', str(sHtmlContent)).group(1)
    OuoToken = re.search('<input name="_token" type="hidden" value="(.+?)">', str(sHtmlContent)).group(1)

    gToken = ResolveCaptcha(key, urlOuo)

    url = urlOuo.replace('/fbc/', '/go/')
    params = '_token=' + OuoToken + '&g-recaptcha-response=' + gToken

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    oRequestHandler.addHeaderEntry('Referer', urlOuo)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Content-Length', str(len(params)))
    oRequestHandler.addHeaderEntry('Cookie', Cookie)
    oRequestHandler.addParametersLine(params)
    sHtmlContent = oRequestHandler.request()

    final = re.search('<form method="POST" action="(.+?)" accept-charset="UTF-8"><input name="_token" type="hidden" value="(.+?)">', str(sHtmlContent))

    url = final.group(1)
    params = '_token=' + final.group(2)

    oRequestHandler = cRequestHandler(url)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    oRequestHandler.addHeaderEntry('Referer', urlOuo)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Content-Length', str(len(params)))
    oRequestHandler.addHeaderEntry('Cookie', Cookie)
    oRequestHandler.addParametersLine(params)
    sHtmlContent = oRequestHandler.request()

    return oRequestHandler.getRealUrl()
