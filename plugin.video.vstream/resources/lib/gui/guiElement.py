class cGuiElement:

    DEFAULT_FOLDER_ICON = 'DefaultFolder.png'

    def __init__(self):
        self.__sType = 'video'
        self.__sMediaUrl = ''
        self.__sTitle = ''
        self.__sTitleSecond = ''
        self.__sDescription = ''
        self.__sThumbnail = ''
        self.__sIcon = self.DEFAULT_FOLDER_ICON
        self.__aItemValues = {}
        self.__aProperties = {}
        self.__aContextElements = []

    def setType(self, sType):
        self.__sType = sType

    def getType(self):
        return self.__sType

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

    def setIcon(self, sIcon):
        self.__sIcon = sIcon

    def getIcon(self):
        return self.__sIcon

    def addItemValues(self, sItemKey, mItemValue):
        self.__aItemValues[sItemKey] = mItemValue

    def getItemValues(self):
        self.__aItemValues['Title'] = self.getTitle()
        self.__aItemValues['Plot'] = self.getDescription()
        return self.__aItemValues
    
    def addItemProperties(self, sPropertyKey, mPropertyValue):
        self.__aProperties[sPropertyKey] = mPropertyValue

    def getItemProperties(self):
        return self.__aProperties

    def addContextItem(self, oContextElement):
        self.__aContextElements.append(oContextElement)

    def getContextItems(self):
        return self.__aContextElements


