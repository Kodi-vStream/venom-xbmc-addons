import urllib
import sys

class cInputParameterHandler:

    def __init__(self):          
        aParams = dict()
        if len(sys.argv)>=2 and len(sys.argv[2])>0:
            aParams = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
          
        self.__aParams = aParams

    def getAllParameter(self):
            return self.__aParams

    def getValue(self, sParamName):
        if self.exist(sParamName):
            sParamValue = self.__aParams[sParamName]
            if not sParamValue.startswith('http'):
                return urllib.unquote_plus(sParamValue)
            else:
                return urllib.unquote(sParamValue)
        return False

    def exist(self, sParamName):
        if sParamName in self.__aParams:
            return sParamName
