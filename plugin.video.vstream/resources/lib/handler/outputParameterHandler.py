# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.util import urlEncode, Unquote, cUtil

class cOutputParameterHandler:
    def __init__(self):
        self.__aParams = {}

    def addParameter(self, sParameterName, mParameterValue):
        if not mParameterValue:
            return

        try:
            if not isinstance(mParameterValue, str):
                mParameterValue = str(mParameterValue)
        except:
            mParameterValue = cUtil().formatUTF8(mParameterValue)

        mParameterValue = Unquote(mParameterValue)
        self.__aParams[sParameterName] = mParameterValue

    def getParameterAsUri(self):
        if len(self.__aParams) > 0:
            return urlEncode(self.__aParams)

        return 'params=0'

    def getValue(self, sParamName):
        if (self.exist(sParamName)):
            sParamValue = self.__aParams[sParamName]
            return Unquote(sParamValue)

        return False

    def clearParameter(self):
        self.__aParams.clear()

    def exist(self, sParamName):
        if sParamName in self.__aParams:
            return sParamName
