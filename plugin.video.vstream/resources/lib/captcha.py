# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
#
# Pour l'utiliser
# from resources.lib.captcha import Captcha_Get_Reponse
#

from resources.lib.comaddon import progress, dialog, xbmc, xbmcgui
import xbmcvfs
import urllib2

NewMethod = True


def Captcha_Get_Reponse(img, cookie):
    # on telecharge l'image
    # PathCache = xbmc.translatePath(xbmcaddon.Addon("plugin.video.vstream").getAddonInfo("profile"))
    # filename  = os.path.join(PathCache, "Captcha.raw").decode("utf-8")
    filename = "special://home/userdata/addon_data/plugin.video.vstream/Captcha.raw"

    headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0",
        # "Referer": url ,
        "Host": "protect.ddl-island.su",
        "Accept": "image/png,image/*;q=0.8,*/*;q=0.5",
        "Accept-Language": "fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4",
        "Accept-Encoding": "gzip, deflate",
        # "Content-Type": "application/x-www-form-urlencoded",
        }

    if cookie:
        headers2["Cookie"] = cookie

    try:
        req = urllib2.Request(img, None, headers2)
        image_on_web = urllib2.urlopen(req)
        if image_on_web.headers.maintype == "image":
            buf = image_on_web.read()
            # downloaded_image = file(filename, "wb")
            downloaded_image = xbmcvfs.File(filename, "wb")
            downloaded_image.write(buf)
            downloaded_image.close()
            image_on_web.close()
        else:
            return ""
    except:
        return ""

    # on affiche le dialogue
    solution = ""

    if NewMethod:
        # nouveau captcha
        try:
            # affichage du dialog perso
            class XMLDialog(xbmcgui.WindowXMLDialog):
                # """
                # Dialog class for captcha
                # """
                def __init__(self, *args, **kwargs):
                    xbmcgui.WindowXMLDialog.__init__(self)
                    pass

                def onInit(self):
                    # image background captcha
                    self.getControl(1).setImage(filename.encode("utf-8"), False)
                    # image petit captcha memory fail
                    self.getControl(2).setImage(filename.encode("utf-8"), False)
                    self.getControl(2).setVisible(False)
                    # Focus clavier
                    self.setFocus(self.getControl(21))

                def onClick(self, controlId):
                    if controlId == 20:
                        # button Valider
                        solution = self.getControl(5000).getLabel()
                        xbmcgui.Window(10101).setProperty("captcha", str(solution))
                        self.close()
                        return

                    elif controlId == 30:
                        # button fermer
                        self.close()
                        return

                    elif controlId == 21:
                        # button clavier
                        self.getControl(2).setVisible(True)
                        kb = xbmc.Keyboard(self.getControl(5000).getLabel(), "", False)
                        kb.doModal()

                        if kb.isConfirmed():
                            self.getControl(5000).setLabel(kb.getText())
                            self.getControl(2).setVisible(False)
                        else:
                            self.getControl(2).setVisible(False)

                def onFocus(self, controlId):
                    self.controlId = controlId

                def _close_dialog(self):
                    self.close()

                def onAction(self, action):
                    # touche return 61448
                    if action.getId() in (9, 10, 11, 30, 92, 216, 247, 257, 275, 61467, 61448):
                        self.close()

            path = "special://home/addons/plugin.video.vstream"
            wd = XMLDialog("DialogCaptcha.xml", path, "default", "720p")
            wd.doModal()
            del wd
        finally:

            solution = xbmcgui.Window(10101).getProperty("captcha")
            if solution == "":
                dialogs.VSinfo("Vous devez taper le captcha")

    else:
        # ancien Captcha
        try:
            img = xbmcgui.ControlImage(450, 0, 400, 130, filename.encode("utf-8"))
            wdlg = xbmcgui.WindowDialog()
            wdlg.addControl(img)
            wdlg.show()
            # xbmc.sleep(3000)
            kb = xbmc.Keyboard("", "Tapez les Lettres/chiffres de l'image", False)
            kb.doModal()
            if kb.isConfirmed():
                solution = kb.getText()
                if solution == "":
                    dialogs.VSinfo("Vous devez taper le captcha")
            else:
                dialogs.VSinfo("Vous devez taper le captcha")
        finally:
            wdlg.removeControl(img)
            wdlg.close()

    return solution
