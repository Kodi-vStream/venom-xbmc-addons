# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# https://forums.tvaddons.ag/tknorris-release-repository/10792-debugging-daclips-2.html

import re

from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.GKDecrypter import GKDecrypter


class cHoster(iHoster):

    def __init__(self):
        iHoster.__init__(self, 'vidbull', 'VidBull')

    def _getMediaLinkForGuest(self):

        url_stream = ''

        oRequest = cRequestHandler(self._url)
        sHtmlContent = oRequest.request()

        oParser = cParser()

        sPattern = "<script type='text\/javascript'>(eval\(function\(p,a,c,k,e,d.+?)<\/script>"
        aResult = oParser.parse(sHtmlContent, sPattern)

        if aResult[0] is True:
            for i in aResult[1]:
                sHtmlContent = cPacker().unpack(i)
                # xbmc.log(sHtmlContent)

                # Premiere methode avec <embed>
                if '<embed' in sHtmlContent:
                    pass

                # deuxieme methode, lien code aes
                else:
                    EncodedLink = re.search('file:"([^"]+)"', sHtmlContent, re.DOTALL)

                    if EncodedLink:

                        Key = "a949376e37b369" + "f17bc7d3c7a04c5721"
                        x = GKDecrypter(128, 128)
                        sUrl = x.decrypt(EncodedLink.group(1), Key.decode("hex"), "ECB").split('\0')[0]

                        # Si utilise pyaes
                        # import resources.lib.pyaes as pyaes
                        # decryptor = pyaes.new(Key.decode("hex"), pyaes.MODE_ECB, IV = '')
                        # sUrl = decryptor.decrypt(lt.decode("hex")).replace('\x00', '')

                        # xbmc.log('>> ' + sUrl)

                        url_stream = sUrl

        if url_stream:
            return True, url_stream
        else:
            return False, False

        return False, False
