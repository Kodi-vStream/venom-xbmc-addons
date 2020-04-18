# -*- coding: utf-8 -*-
# *************************************************************************************************************************
# from Shani's LPro Code https://github.com/Shani-08/ShaniXBMCWork2/blob/master/other/unCaptcha.py
# and https://github.com/OpenMediaVault-Plugin-Developers/openmediavault-pyload/blob/master/usr/share/pyload/module/plugins/captcha/ReCaptcha.py
# and https://gitlab.com/iptvplayer-for-e2/iptvplayer-for-e2
# *************************************************************************************************************************
from resources.lib.comaddon import xbmcgui, xbmc, VSlog
from resources.lib.handler.requestHandler import cRequestHandler
import re, base64, random, time, os, xbmcaddon, xbmcvfs
import urlparse, urllib, urllib2, cookielib

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
__addon__ = xbmcaddon.Addon('plugin.video.vstream')
__sLang__ = 'fr'


class cInputWindow(xbmcgui.WindowDialog):
    def __init__(self, *args, **kwargs):

        self.cptloc = kwargs.get('captcha')
        # self.img = xbmcgui.ControlImage(250, 110, 780, 499, '')
        # xbmc.sleep(500)
        self.img = xbmcgui.ControlImage(250, 110, 780, 499, self.cptloc)
        xbmc.sleep(500)

        bg_image = os.path.join( __addon__.getAddonInfo('path'), 'resources/art/' ) + 'background.png'
        check_image = os.path.join( __addon__.getAddonInfo('path'), 'resources/art/' ) + 'trans_checked.png'

        self.ctrlBackground = xbmcgui.ControlImage(0, 0, 1280, 720, bg_image)
        self.cancelled = False
        self.addControl (self.ctrlBackground)

        self.strActionInfo = xbmcgui.ControlLabel(250, 20, 724, 400, 'Veuillez sélectionnez les images correspondants au thème.\nIl devrait y en avoir 3 ou 4 à sélectionner.', 'font40', '0xFFFF00FF')
        self.addControl(self.strActionInfo)

        self.msg = kwargs.get('msg')
        self.roundnum = kwargs.get('roundnum')
        self.strActionInfo = xbmcgui.ControlLabel(250, 70, 700, 300, 'Le thème est: ' + self.msg, 'font13', '0xFFFF00FF')
        self.addControl(self.strActionInfo)

        self.addControl(self.img)

        self.chk = [0]*9
        self.chkbutton = [0]*9
        self.chkstate = [False]*9

        if 1 == 2:
            self.chk[0] = xbmcgui.ControlCheckMark(250, 110, 260, 166, '1', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[1] = xbmcgui.ControlCheckMark(250 + 260, 110, 260, 166, '2', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[2] = xbmcgui.ControlCheckMark(250 + 520, 110, 260, 166, '3', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)

            self.chk[3] = xbmcgui.ControlCheckMark(250, 110 + 166, 260, 166, '4', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[4] = xbmcgui.ControlCheckMark(250 + 260, 110 + 166, 260, 166, '5', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[5] = xbmcgui.ControlCheckMark(250 + 520, 110 + 166, 260, 166, '6', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)

            self.chk[6] = xbmcgui.ControlCheckMark(250, 110 + 332, 260, 166, '7', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[7] = xbmcgui.ControlCheckMark(250 + 260, 110 + 332, 260, 166, '8', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[8] = xbmcgui.ControlCheckMark(250 + 520, 110 + 332, 260, 166, '9', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)

        else:
            self.chk[0] = xbmcgui.ControlImage(250, 110, 260, 166, check_image)
            self.chk[1] = xbmcgui.ControlImage(250 + 260, 110, 260, 166, check_image)
            self.chk[2] = xbmcgui.ControlImage(250 + 520, 110, 260, 166, check_image)

            self.chk[3] = xbmcgui.ControlImage(250, 110 + 166, 260, 166, check_image)
            self.chk[4] = xbmcgui.ControlImage(250 + 260, 110 + 166, 260, 166, check_image)
            self.chk[5] = xbmcgui.ControlImage(250 + 520, 110 + 166, 260, 166, check_image)

            self.chk[6] = xbmcgui.ControlImage(250, 110 + 332, 260, 166, check_image)
            self.chk[7] = xbmcgui.ControlImage(250 + 260, 110 + 332, 260, 166, check_image)
            self.chk[8] = xbmcgui.ControlImage(250 + 520, 110 + 332, 260, 166, check_image)

            self.chkbutton[0] = xbmcgui.ControlButton(250, 110, 260, 166, '1', font = 'font1')
            self.chkbutton[1] = xbmcgui.ControlButton(250 + 260, 110, 260, 166, '2', font = 'font1')
            self.chkbutton[2] = xbmcgui.ControlButton(250 + 520, 110, 260, 166, '3', font = 'font1')

            self.chkbutton[3] = xbmcgui.ControlButton(250, 110 + 166, 260, 166, '4', font = 'font1')
            self.chkbutton[4] = xbmcgui.ControlButton(250 + 260, 110 + 166, 260, 166, '5', font = 'font1')
            self.chkbutton[5] = xbmcgui.ControlButton(250 + 520, 110 + 166, 260, 166, '6', font = 'font1')

            self.chkbutton[6] = xbmcgui.ControlButton(250, 110 + 332, 260, 166, '7', font = 'font1')
            self.chkbutton[7] = xbmcgui.ControlButton(250 + 260, 110 + 332, 260, 166, '8', font = 'font1')
            self.chkbutton[8] = xbmcgui.ControlButton(250 + 520, 110 + 332, 260, 166, '9', font = 'font1')

        for obj in self.chk:
            self.addControl(obj)
            obj.setVisible(False)
        for obj in self.chkbutton:
            self.addControl(obj)

        self.cancelbutton = xbmcgui.ControlButton(250 + 260 - 70, 620, 140, 50, 'Cancel', alignment = 2)
        self.okbutton = xbmcgui.ControlButton(250 + 520 - 50, 620, 100, 50, 'OK', alignment = 2)
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
        if control == self.okbutton:
            if self.anythingChecked():
                self.close()
        elif control == self.cancelbutton:
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


def ResolveCaptcha(key, urlOuo):
    urlBase = 'https://www.google.com/recaptcha/api/fallback?k=' + key
    oRequestHandler = cRequestHandler(urlBase)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    oRequestHandler.addHeaderEntry('Referer', urlOuo)
    body = oRequestHandler.request()

    captchaScrap = re.findall('value="8"><img class="fbc-imageselect-payload" src="(.+?)"', str(body))

    text = re.search('<div class="rc-imageselect.+?">.+?<strong>(.+?)</strong>', str(body)).group(1)

    c = re.search('method="POST"><input type="hidden" name="c" value="(.+?)"', str(body)).group(1)
    k = re.search('k=(.+?)" alt=', str(body)).group(1)
    params = {
        "c": c,
        "k": k,
    }
    query_string = urllib.urlencode(params)

    url = 'https://www.google.com' + str(captchaScrap[0]) + '?' + query_string

    filePath = 'special://home/userdata/addon_data/plugin.video.vstream/Captcha.raw'

    oRequestHandler = cRequestHandler(url)
    htmlcontent = oRequestHandler.request()

    downloaded_image = xbmcvfs.File(filePath, 'wb')
    downloaded_image.write(htmlcontent)
    downloaded_image.close()

    oSolver = cInputWindow(captcha = filePath, msg = text, roundnum = 1)
    retArg = oSolver.get()

    allNumber = [int(s) for s in re.findall('([0-9])', str(retArg))]
    responseFinal = ""
    for rep in allNumber:
        responseFinal = responseFinal + '&response=' + str(rep)

    headers = {'User-Agent': UA,
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
               'Accept-Encoding': 'gzip, deflate',
               'Referer': url,
               'Content-Type': 'application/x-www-form-urlencoded',
               'Content-Length': str(len(params))}

    params = 'c=' + c + responseFinal

    oRequestHandler = cRequestHandler(urlBase)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
    oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
    oRequestHandler.addHeaderEntry('Referer', url)
    oRequestHandler.addHeaderEntry('Content-Type', 'application/x-www-form-urlencoded')
    oRequestHandler.addHeaderEntry('Content-Length', str(len(params)))
    oRequestHandler.addParametersLine(params)

    sHtmlContent = oRequestHandler.request()

    token = re.search('<textarea dir="ltr" readonly>(.+?)<', sHtmlContent).group(1)
    if not token:
        dialogs = dialog()
        dialogs.VSinfo("Captcha non valide")
    return token


def getUrl(url, cookieJar = None, post = None, timeout = 20, headers = None, noredir = False):

    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)

    if noredir:
        opener = urllib2.build_opener(NoRedirection, cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    else:
        opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    # opener = urllib2.install_opener(opener)
    req = urllib2.Request(url)

    if headers:
        for h, hv in headers:
            req.add_header(h, hv)
    else:
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
        req.add_header('Accept-Language', __sLang__)

    VSlog('post : ' + str(post))
    response = opener.open(req, post, timeout=timeout)
    link = response.read()
    response.close()
    return link


class UnCaptchaReCaptcha:

    def _collect_api_info(self):

        html = getUrl("http://www.google.com/recaptcha/api.js")
        a    = re.search(r'po.src = \'(.*?)\';', html).group(1)
        vers = a.split("/")[5]

        questionfile = a
        VSlog("Fichier questions: %s" % questionfile)
        VSlog("API version: %s" % vers)

        language = a.split("__")[1].split(".")[0]
        VSlog("API language: %s" % language)

        html = getUrl("https://apis.google.com/js/api.js")
        b    = re.search(r'"h":"(.*?)","', html).group(1)
        jsh  = b.decode('unicode-escape')

        VSlog("API jsh-string: %s" % jsh)
        return vers, language, jsh, questionfile

    def _prepare_time_and_rpc(self):
        # getUrl("http://www.google.com/recaptcha/api2/demo")
        millis = int(round(time.time() * 1000))
        VSlog ("Time: %s" % millis)

        rand = random.randint(1, 99999999)
        a    = "0.%s" % str(rand * 2147483647)
        rpc  = int(100000000 * float(a))

        VSlog ("Rpc-token: %s" % rpc)
        return millis, rpc

    def ExtReg(self, r, chain):
        r = re.search(r, chain)
        if not r:
            return ''
        return r.group(1)

    def processCaptcha(self, key,lang, gcookieJar):
        headers=[("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0"),
                 # ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
                 ("Referer", "https://www.google.com/recaptcha/api2/demo"),
                 ("Accept-Language", lang)]

        millis, rpc = self._prepare_time_and_rpc()
        co = base64.b64encode('https://www.google.com:443')
        botguardstring = "!A"
        vers, language, jsh, questionfile = self._collect_api_info()

        post_data = None
        token = ''
        iteration = 0
        reCaptchaUrl = 'http://www.google.com/recaptcha/api/fallback?k=%s' % key

        while iteration < 20:

            millis_captcha_loading = int(round(time.time() * 1000))

            # ,'cookiefile':self.COOKIE_FILE, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True
            data = getUrl(reCaptchaUrl ,headers = headers, post = post_data ,cookieJar = gcookieJar)
            VSlog(reCaptchaUrl)
            imgUrl = re.search(r'"(/recaptcha/api2/payload[^"]+?)"', data).group(1)

            VSlog(imgUrl)
            iteration += 1
            message = self.ExtReg(r'<label[^>]+class="fbc-imageselect-message-text"[^>]*>(.*?)</label>', data)

            if '' == message:
                message = self.ExtReg(r'<div[^>]+class="fbc-imageselect-message-error">(.*?)</div>', data)
            if '' == message:
                token = re.search(r'"this\.select\(\)">(.*?)</textarea>', data).group(1)
                if '' != token:
                    VSlog('>>>>>>>> Captcha token[%s]' % (token))
                else:
                    VSlog('>>>>>>>> Captcha Failed')
                break

            cval = re.search(r'name="c"\s+value="([^"]+)', data).group(1)
            imgUrl = 'https://www.google.com%s' % (imgUrl.replace('&amp;', '&'))
            accepLabel = re.search(r'type="submit"\s+value="([^"]+)', data).group(1)

            filePath = 'c://c.jpeg'
            import random
            n = random.randint(1, 1000)
            filePath = 'c://c' + str(n) + '.jpeg'

            VSlog(">>>>>>>> Captcha message[%s]" % message)
            VSlog(">>>>>>>> Captcha accep label[%s]" % accepLabel)
            VSlog(">>>>>>>> Captcha imgUrl[%s] filePath[%s]" % (imgUrl, filePath))

            # params = {'maintype': 'image', 'subtypes':['jpeg'], 'check_first_bytes':['\xFF\xD8', '\xFF\xD9']}
            # ret = self.cm.saveWebFile(filePath, imgUrl, params)
            # retArg = self.sessionEx.waitForFinishOpen(UnCaptchaReCaptchaWidget, imgFilePath=filePath, message=message, title="reCAPTCHA v2", additionalParams={'accep_label':accepLabel})

            ret = ''
            ret = getUrl(imgUrl, headers = headers, cookieJar = gcookieJar)
            downloaded_image = file(filePath, 'wb')
            downloaded_image.write(ret)
            downloaded_image.close()

            oSolver = cInputWindow(captcha = filePath, msg = message, roundnum = iteration)
            retArg = oSolver.get()
            VSlog('>>>>>>>> Captcha response [%s]' % retArg)

            responses = base64.b64encode('{"response":[%s]}' % retArg)
            # VSlog(responses)
            responses=responses.replace('=', '.')

            if retArg is not None and len(retArg) and retArg[0]:
                post_data = urllib.urlencode({'c': cval, 'response': responses}, doseq = True)
            else:
                break

            if False:
                timeToSolve     = int(round(time.time() * 1000)) - millis_captcha_loading
                timeToSolveMore = timeToSolve  # timeToSolve + int(float("0." + str(random.randint(1, 99999999))) * 500)

                postdata = urllib.urlencode({'c'        : cval,
                                              'response': responses,
                                              'v'       : vers,
                                              't'       : timeToSolve,
                                              'bg'      : botguardstring,
                                              'ct'      : timeToSolveMore})
                html = getUrl('https://www.google.com/recaptcha/api2/userverify?k=' + key, post = postdata, headers = headers)
                # fh = open('c:\\test.txt', 'w')
                # fh.write(html)
                # fh.close()

        return token


def getg():
    return None
    cookieJar = cookielib.LWPCookieJar()
    try:
        cookieJar.load("./gsite.jwl")
    except:
        pass


def performCaptcha(sitename, cj, returnpage = True, captcharegex = 'data-sitekey="(.*?)"', lang = "fr", headers = None):
    gcookieJar = getg()
    sitepage = getUrl(sitename, cookieJar = cj, headers = headers)
    sitekey = re.findall(captcharegex, sitepage)
    token = ""
    if len(sitekey) >= 1:
        # getUrl('https://www.google.com/', cookieJar = gcookieJar)
        c = UnCaptchaReCaptcha()
        token = c.processCaptcha(sitekey[0], lang, gcookieJar)
        if returnpage:
            # gcookieJar.save('./gsite.jwl');
            headers = [("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0"),
             ("Referer", sitename)]
            sitepage = getUrl(sitename, cookieJar = cj, post = urllib.urlencode({"g-recaptcha-response": token}), headers = headers)

    if returnpage:
        # fh = open('c:\\reussi.txt', 'w')
        # fh.write(sitepage)
        # fh.close()
        return sitepage
    else:
        return token

##performCaptcha("http://www.livetv.tn/", cookieJar)
