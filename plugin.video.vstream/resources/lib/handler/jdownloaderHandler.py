# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.comaddon import addon, dialog, VSlog


class cJDownloaderHandler:
    ADDON = addon()
    DIALOG = dialog()

    def sendToJDownloader(self, sUrl):
        if (self.__checkConfig() == False):
            VSlog('Settings ueberpruefen (XBMC)')
            return False

        if (self.__checkConnection() == False):
            VSlog('Verbindung fehlgeschlagen (JD aus?)')
            return False

        bDownload = self.__download(sUrl)
        if (bDownload == True):
            self.DIALOG.VSinfo('Link gesendet', 'JDownloader')

    def __checkConfig(self):
        bEnabled = self.ADDON.getSetting('jd_enabled')
        if (bEnabled == 'true'):
            return True
        return False

    def __getHost(self):
        return self.ADDON.getSetting('jd_host')

    def __getPort(self):
        return self.ADDON.getSetting('jd_port')

    def __getAutomaticStart(self):
        bAutomaticStart = self.ADDON.getSetting('jd_automatic_start')
        if (bAutomaticStart == 'true'):
            return True
        return False

    def __getLinkGrabber(self):
        bAutomaticStart = self.ADDON.getSetting('jd_grabber')
        if (bAutomaticStart == 'true'):
            return True
        return False

    def __download(self, sFileUrl):
        sHost = self.__getHost()
        sPort = self.__getPort()
        bAutomaticDownload = self.__getAutomaticStart()
        bLinkGrabber = self.__getLinkGrabber()

        sLinkForJd = self.__createJDUrl(sFileUrl, sHost, sPort, bAutomaticDownload, bLinkGrabber)
        VSlog("JD Link " + str(sLinkForJd))

        oRequestHandler = cRequestHandler(sLinkForJd)
        oRequestHandler.request()
        return True

    def __createJDUrl(self, sFileUrl, sHost, sPort, bAutomaticDownload, bLinkGrabber):
        sGrabber = '0'
        if (bLinkGrabber == True):
            sGrabber = '1'

        sAutomaticStart = '0'
        if (bAutomaticDownload == True):
            sAutomaticStart = '1'

        sUrl = 'http://' + str(sHost) + ':' + str(sPort) + '/action/add/links/grabber' + str(sGrabber) + '/start' + str(sAutomaticStart) + '/' + sFileUrl
        return sUrl

    def __checkConnection(self):
        VSlog("check JD Connection")
        sHost = self.__getHost()
        sPort = self.__getPort()

        sLinkForJd = 'http://' + str(sHost) + ':' + str(sPort)

        try:
            oRequestHandler = cRequestHandler(sLinkForJd)
            sHtmlContent = oRequestHandler.request()
            return True
        except Exception:
            return False
        return False



