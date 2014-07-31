import xbmc

LOG_LEVEL_INFO = 0;
LOG_LEVEL_ERROR = 1;
LOG_LEVEL_FATAL = 2;

logLevel = LOG_LEVEL_INFO# (config.getSetting("debug")=="true")

def info(sInfo):
    if (logLevel <= LOG_LEVEL_INFO):
        __writeLog(sInfo, xbmc.LOGNOTICE);

def error(sInfo):
    if (logLevel <= LOG_LEVEL_FATAL):
         __writeLog(sInfo, xbmc.LOGERROR);

def fatal(sInfo):
    if (logLevel <= LOG_LEVEL_FATAL):
         __writeLog(sInfo, xbmc.LOGFATAL);

def __writeLog(sLog, cLogLevel):
    xbmc.log("\t[PLUGIN] xStream: " + str(sLog), cLogLevel)

