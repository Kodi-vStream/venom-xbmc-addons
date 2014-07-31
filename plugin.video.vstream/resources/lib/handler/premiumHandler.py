from resources.lib.config import cConfig
import logger

class cPremiumHandler:

    def __init__(self, sHosterIdentifier):
        self.__sHosterIdentifier = sHosterIdentifier

    def isPremiumModeAvailable(self):
        bIsPremium = cConfig().getSetting('hoster_' + str(self.__sHosterIdentifier) + '_premium')        
        if (bIsPremium == 'true'):
            logger.info('usa premiumaccount for hoster: ' + str(self.__sHosterIdentifier))
            return True

        logger.info('us freeaccount for hoster: ' + str(self.__sHosterIdentifier))
        return False

    def getUsername(self):
        sUsername = cConfig().getSetting('hoster_' + str(self.__sHosterIdentifier) + '_username')
        return sUsername

    def getPassword(self):
        sPassword = cConfig().getSetting('hoster_' + str(self.__sHosterIdentifier) + '_password')
        return sPassword
