#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.hosters.hoster import iHoster
from resources.lib.packer import cPacker
from resources.lib.util import VScreateDialogSelect
from resources.lib.util import VSlog
import re

#Meme code que thevideo

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'VidUp'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'vidup'
        
    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True
    
    def __getIdFromUrl(self, sUrl):
        sPattern = 'https*://vidup.tv/([^<]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''
        
    def setUrl(self, sUrl):
        #self.__sUrl = str(sUrl).replace('beta.vidup.tv','vidup.tv')
        #self.__sUrl = re.sub('(-\d+x\d+\.html)','',self.__sUrl)
        #self.__sUrl = self.__sUrl.replace('embed-', '')
        self.__sUrl = sUrl

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):
    
        sUrl = self.__sUrl
        
        #sId = self.__getIdFromUrl(self.__sUrl)
        #sUrl = 'http://vidup.tv/embed-' + sId + '.html'

        VSlog(sUrl)
        
        stream_url = ''
        oRequest = cRequestHandler(sUrl)
        sHtmlContent = oRequest.request()
        
        #decodage de la page html
        sHtmlContent3 = sHtmlContent
        code = ''
        maxboucle = 3
        while (maxboucle > 0):
            VSlog('loop : ' + str(maxboucle))
            sHtmlContent3 = CheckCpacker(sHtmlContent3)
            #sHtmlContent3 = CheckJJDecoder(sHtmlContent3)           
            #sHtmlContent3 = CheckAADecoder(sHtmlContent3)
            
            maxboucle = maxboucle - 1   
         
        sHtmlContent = sHtmlContent3
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent)
        #fh.close()
        
        oParser = cParser()
        
        sPattern = "var thief='([^']+)';"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if not (aResult[0]):
            return False , False
            
        key = aResult[1][0].replace('+','')
            
        sPattern = "'rc=[^<>]+?\/(.+?)'\.concat"
        aResult = oParser.parse(sHtmlContent, sPattern)
        if not (aResult[0]):
            return False , False
            
        ee = aResult[1][0]
        if ee.endswith('\\'):
            ee = ee[:-1]
            
        url2 = 'https://vidup.tv/' + ee + '/' + key
        
        VSlog(url2)

        oRequest = cRequestHandler(url2)
        sHtmlContent2 = oRequest.request()
        
        
        #fh = open('c:\\test.txt', "w")
        #fh.write(sHtmlContent2)
        #fh.close()
        
        code = cPacker().unpack(sHtmlContent2)
        sPattern = '"vt=([^"]+)'
        r2 = re.search(sPattern,code)
        if not (r2):
            return False,False
        
        sPattern = '{"file":"([^"]+)","label":"(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
        
            #Remplissage des tableaux
            for i in aResult[1]:
                url.append(str(i[0]))
                qua.append(str(i[1]))
                
            #Si  1 url
            if len(url) == 1:
                api_call = url[0]
            #Affichage du tableau
            elif len(url) > 1:
                ret = VScreateDialogSelect(qua)
                if (ret > -1):
                    api_call = url[ret]

        #xbmc.sleep(5000)
                    
        if (api_call):
            api_call = api_call + '?direct=false&ua=1&vt=' + r2.group(1)
            return True, api_call
            
        return False, False

        
#-----------------------------------------------------------------------------------------
def CheckCpacker(str):

    sPattern = '(eval\(function\(p,a,c,k,e(?:.|\s)+?\)\)\s*)<'
    aResult = re.search(sPattern, str,re.DOTALL | re.UNICODE)
    if (aResult):
        #VSlog('Cpacker encryption')
        str2 = aResult.group(1)
        
        if not str2.endswith(';'):
            str2 = str2 + ';'

        #if not str2.startswith('eval'):
        #    str2 = 'eval(function' + str2[4:]
        
        try:
            tmp = cPacker().unpack(str2)
            #tmp = tmp.replace("\\'","'")
        except:
            tmp =''
            
        #VSlog(tmp)

        return str[:(aResult.start() + 1)] + tmp + str[(aResult.end()-1):]
        
    return str
