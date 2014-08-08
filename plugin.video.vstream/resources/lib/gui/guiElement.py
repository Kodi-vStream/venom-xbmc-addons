#-*- coding: utf-8 -*-
#Venom.
from resources.lib.config import cConfig
import os, re
class cGuiElement:

    DEFAULT_FOLDER_ICON = 'icon.png'

    def __init__(self):
        self.__sRootArt = os.path.join(os.getcwd(), 'resources/art/')
        self.__sType = 'video'
        self.__sMeta = 0
        self.__sMetaAddon = cConfig().getSetting('meta-view')
        self.__sMediaUrl = ''
        self.__sTitle = ''
        self.__sTitleSecond = ''
        self.__sDescription = ''
        self.__sThumbnail = ''
        self.__sIcon = self.DEFAULT_FOLDER_ICON
        self.__sFanart = self.__sRootArt+'fanart.jpg'
        self.__aItemValues = {}
        self.__aProperties = {}
        self.__aContextElements = []

    def setType(self, sType):
        self.__sType = sType

    def getType(self):
        return self.__sType
        
    def setMeta(self, sMeta):
        self.__sMeta = sMeta

    def getMeta(self):
        return self.__sMeta

    def setMediaUrl(self, sMediaUrl):
        self.__sMediaUrl = sMediaUrl

    def getMediaUrl(self):
        return self.__sMediaUrl

    def setSiteName(self, sSiteName):
        self.__sSiteName = sSiteName

    def getSiteName(self):
        return self.__sSiteName

    def setFunction(self, sFunctionName):
        self.__sFunctionName = sFunctionName

    def getFunction(self):
        return self.__sFunctionName

    def setTitle(self, sTitle):
        self.__sTitle = sTitle;

    def getTitle(self):
        return self.__sTitle

    def setTitleSecond(self, sTitleSecond):
        self.__sTitleSecond = sTitleSecond

    def getTitleSecond(self):
        return self.__sTitleSecond

    def setDescription(self, sDescription):
        self.__sDescription = sDescription

    def getDescription(self):
        return self.__sDescription

    def setThumbnail(self, sThumbnail):
        self.__sThumbnail = sThumbnail

    def getThumbnail(self):
        return self.__sThumbnail
    
    def setFanart(self, sFanart):
        self.__sFanart = sFanart

    def getFanart(self):
        return self.__sFanart

    def setIcon(self, sIcon):
        self.__sIcon = sIcon

    def getIcon(self):
        return self.__sRootArt+self.__sIcon

    def addItemValues(self, sItemKey, mItemValue):
        self.__aItemValues[sItemKey] = mItemValue
    
    def getMeta(self):
        from metahandler import metahandlers
        grab = metahandlers.MetaData()
        #sTitle = self.__sTitle.decode('latin-1').encode("utf-8")
        sTitle=re.sub(r'\[.*\]|\(.*\)',r'',str(self.__sTitle))

        if self.__sMeta == 1:
            meta = grab.get_meta('movie',sTitle,'','','')
        elif self.__sMeta == 2:
            sTitle=re.sub(r'[0-9]+?',r'',str(sTitle))
            sTitle=sTitle.replace('-','').replace('Saison','').replace('saison','').replace('Season','').replace('Episode','').replace('episode','')
            meta = grab.get_meta('tvshow',sTitle,'','','')
        else:
            return
        for key, value in meta.items():
            self.addItemValues(key, value) 
        #print meta['backdrop_url']
        if meta['backdrop_url']:
            self.addItemProperties('fanart_image', meta['backdrop_url'])
        return

    def getItemValues(self):
        self.__aItemValues['Title'] = self.getTitle()
        self.__aItemValues['Plot'] = self.getDescription()
        self.addItemProperties('fanart_image', self.__sFanart)

        if self.__sMeta > 0 and self.__sMetaAddon == 'true':
            self.getMeta()
        return self.__aItemValues
    
    def addItemProperties(self, sPropertyKey, mPropertyValue):
        self.__aProperties[sPropertyKey] = mPropertyValue

    def getItemProperties(self):
        return self.__aProperties

    def addContextItem(self, oContextElement):
        self.__aContextElements.append(oContextElement)

    def getContextItems(self):
        return self.__aContextElements


