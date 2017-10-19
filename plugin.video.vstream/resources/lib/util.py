#-*- coding: utf-8 -*-
import re
import urllib
import xbmc
import xbmcgui
import xbmcaddon
import htmlentitydefs
import unicodedata
import sys,xbmcplugin

COUNT = 0
DIALOG2 = None

class cUtil:

    def CheckOrd(self, label):
        count = 0
        try:
            label = label.lower()
            label = label.strip()
            label = unicode(label, 'utf-8')
            label = unicodedata.normalize('NFKD', label).encode('ASCII', 'ignore')
            for i in label:
                count += ord(i)
        except:
            pass

        return count

    def CheckOccurence(self,str1,str2):

        Ignoreliste = ['du', 'la', 'le', 'les', 'de', 'un', 'une','des']

        str1 = str1.replace('+',' ').replace('%20',' ')
        str1 = str1.lower()
        str2 = str2.lower()
        try:
            str1 = unicode(str1, 'utf-8')
        except:
            pass
        try:
            str2 = unicode(str2, 'utf-8')
        except:
            pass
        str1 = unicodedata.normalize('NFKD', str1).encode('ASCII', 'ignore')
        str2 = unicodedata.normalize('NFKD', str2).encode('ASCII', 'ignore')

        #xbmc.log(str1 + ' ---- ' + str2, xbmc.LOGNOTICE)

        i = 0
        for part in str1.split(' '):
            if (part in str2) and (part not in Ignoreliste):
                i = i + 1
        return i

    def removeHtmlTags(self, sValue, sReplace = ''):
        p = re.compile(r'<.*?>')
        return p.sub(sReplace, sValue)


    def formatTime(self, iSeconds):
        iSeconds = int(iSeconds)

        iMinutes = int(iSeconds / 60)
        iSeconds = iSeconds - (iMinutes * 60)
        if (iSeconds < 10):
            iSeconds = '0' + str(iSeconds)

        if (iMinutes < 10):
            iMinutes = '0' + str(iMinutes)

        return str(iMinutes) + ':' + str(iSeconds)

    def urlDecode(self, sUrl):
        return urllib.unquote(sUrl)

    def urlEncode(self, sUrl):
        return urllib.quote(sUrl)

    def unquotePlus(self, sUrl):
        return urllib.unquote_plus(sUrl)

    def quotePlus(self, sUrl):
        return urllib.quote_plus(sUrl)

    def dialog(self, sName):
        oDialog = xbmcgui.DialogProgress()
        oDialog.create(sName)
        return oDialog

    def DecoTitle(self, string):
        return string


    def DecoTitle2(self, string):

        #on vire ancienne deco en cas de bug
        string = re.sub('\[\/*COLOR.*?\]','',str(string))

        #pr les tag Crochet
        string = re.sub('([\[].+?[\]])',' [COLOR coral]\\1[/COLOR] ', string)
        #pr les tag parentheses
        string = re.sub('([\(](?![0-9]{4}).{1,7}[\)])',' [COLOR coral]\\1[/COLOR] ', string)
        #pr les series
        string = self.FormatSerie(string)
        string = re.sub('(?i)(.*) ((?:[S|E][0-9\.\-\_]+){1,2})','\\1 [COLOR coral]\\2[/COLOR] ', string)

        #vire doubles espaces
        string = re.sub(' +',' ',string)

        return string

    def unescape(self,text):
        def fixup(m):
            text = m.group(0)
            if text[:2] == "&#":
                # character reference
                try:
                    if text[:3] == "&#x":
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
            return text # leave as is
        return re.sub("&#?\w+;", fixup, text)


    def CleanName(self,name):
        #vire accent et '\'
        try:
            name = unicode(name, 'utf-8')#converti en unicode pour aider aux convertions
        except:
            pass
        name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("unicode_escape")
        name = name.encode("utf-8") #on repasse en utf-8

        #on cherche l'annee
        annee = ''
        m = re.search('(\([0-9]{4}\))', name)
        if m:
            annee = str(m.group(0))
            name = name.replace(annee,'')

        #vire tag
        name = re.sub('[\(\[].+?[\)\]]','', name)
        #les apostrohes remplacer par des espaces
        name = name.replace("'", " ")
        #vire caractere special
        name = re.sub("[^a-zA-Z0-9 ]", "",name)
        #tout en minuscule
        name = name.lower()
        #vire espace double
        name = re.sub(' +',' ',name)

        #vire espace a la fin
        if name.endswith(' '):
            name = name[:-1]

        #on remet l'annee
        if annee:
            name = name + ' ' + annee

        return name

    def FormatSerie(self,string):

        #xbmc.log(string)

        #vire doubles espaces
        string = re.sub(' +',' ',string)

        #vire espace a la fin
        if string.endswith(' '):
            string = string[:-1]

        #vire espace au debut
        if string.startswith(' '):
            string = string[1:]

        #convertion unicode
        string = string.decode("utf-8")

        SXEX = ''
        #m = re.search( ur'(?i)(\wpisode ([0-9\.\-\_]+))(?:$| [^a\u00E0])',string,re.UNICODE)
        m = re.search( ur'(?i)(\wpisode ([0-9\.\-\_]+))',string,re.UNICODE)
        if m:
            #ok y a des episodes
            string = string.replace(m.group(1),'')
            #SXEX + "%02d" % int(m.group(2))
            SXEX = m.group(2)
            if len(SXEX) < 2:
                SXEX = '0' + SXEX
            SXEX = 'E' + SXEX

            #pr les saisons
            m = re.search('(?i)(s(?:aison )*([0-9]+))', string)
            if m:
                string = string.replace(m.group(1),'')
                SXEX = 'S' + "%02d" % int(m.group(2)) + SXEX
            string = string + ' ' + SXEX

        else:
            #pas d'episode mais y a t il des saisons ?
            m = re.search('(?i)(s(?:aison )*([0-9]+))(?:$| )', string)
            if m:
                string = string.replace(m.group(1),'')
                SXEX = 'S' + "%02d" % int(m.group(2))

                string = string + ' ' + SXEX

        #reconvertion utf-8
        return string.encode('utf-8')

    def EvalJSString(self,s):
        s = s.replace(' ','')
        try:
            s = s.replace('!+[]','1').replace('!![]','1').replace('[]','0')
            s = re.sub(r'(\([^()]+)\+\[\]\)','(\\1)*10)',s)  # si le bloc fini par +[] >> *10
            s = re.sub(r'\[([^\]]+)\]','str(\\1)',s)
            # s = s.replace('[','(').replace(']',')')
            if s[0]=='+':
                s = s[1:]
            val = int(eval(s))
            return val
        except:
            return 0



#***********************
#Fonctions lights
#***********************

#Pour les avoir
#from resources.lib import util
#puis util.VSlog('test')
def isKrypton():
    try:
        version = xbmc.getInfoLabel('system.buildversion')
        if version[0:2] >= "17":
            return True
        else:
            return False
    except:
        return False

def Unquote(sUrl):
    return urllib.unquote(sUrl)

def Quote(sUrl):
    return urllib.quote(sUrl)

def UnquotePlus(sUrl):
    return urllib.unquote_plus(sUrl)

def QuotePlus(sUrl):
    return urllib.quote_plus(sUrl)

def QuoteSafe(sUrl):
    return urllib.quote(sUrl,safe=':/')

def VSlog(e):
    xbmc.log('\t[PLUGIN] Vstream: '+str(e), xbmc.LOGNOTICE)

def VSupdate(self):
    xbmc.executebuiltin("Container.Refresh")

def VS_show_busy_dialog():
    xbmc.executebuiltin('ActivateWindow(busydialog)')

def VS_hide_busy_dialog():
    xbmc.executebuiltin('Dialog.Close(busydialog)')
    while xbmc.getCondVisibility('Window.IsActive(busydialog)'):
        xbmc.sleep(100)

def VScreateDialogOK(label):
    oDialog = xbmcgui.Dialog()
    oDialog.ok('vStream', label)
    return oDialog

def VScreateDialogYesNo(label):
    oDialog = xbmcgui.Dialog()
    qst = oDialog.yesno("vStream", label)
    return qst

def VScreateDialogSelect(label,sTitle=''):
    oDialog = xbmcgui.Dialog()
    if sTitle:
        ret = oDialog.select(sTitle, label)
    else:
        ret = oDialog.select('Sélectionner une qualité', label)

    return ret

def VSDialogSelectQual(list_qual,list_url):
    if len(list_url) == 0:
        return ''
    if len(list_url) == 1:
        return list_url[0]

    oDialog = xbmcgui.Dialog()
    ret = oDialog.select('Sélectionner une qualité', list_qual)
    if ret > -1:
        return list_url[ret]
    return ''

def createDialog(sSite):
    global DIALOG2
    if DIALOG2 == None:
        oDialog = xbmcgui.DialogProgress()
        oDialog.create(sSite)
        DIALOG2 = oDialog
        return oDialog
    else:
        return DIALOG2


def updateDialog(dialog,total):
    if xbmcgui.Window(10101).getProperty('search') != 'true':
       global COUNT
       COUNT += 1
       iPercent = int(float(COUNT * 100) / total)
       dialog.update(iPercent, 'Chargement: '+str(COUNT)+'/'+str(total))

def finishDialog(dialog):
    if xbmcgui.Window(10101).getProperty('search') != 'true':
       dialog.close()
       del dialog

def updateDialogSearch(dialog, total, site):
    global COUNT
    COUNT += 1
    iPercent = int(float(COUNT * 100) / total)
    dialog.update(iPercent, 'Chargement: '+str(site))

def VSerror(e):
    xbmcgui.Dialog().notification('Vstream','Erreur: '+str(e),xbmcgui.NOTIFICATION_ERROR,2000)
    VSlog('Erreur: ' + str(e))

def VSshowInfo(sTitle, sDescription, iSeconds=0,sound = True):
    if (iSeconds == 0):
        iSeconds = 1000
    else:
        iSeconds = iSeconds * 1000

    # On ne peut pas aller voir si l'option est activee car on doit recharger la classe cConfig > aussi lourd a executer
    #if self.getSetting('Block_Noti_sound') == 'true':
    #    sound = False

    xbmcgui.Dialog().notification(str(sTitle), str(sDescription),xbmcgui.NOTIFICATION_INFO,iSeconds,sound)

def VStranslatePathAddon(location):
    #Note, location = (author,changelog,description,disclaimer,fanart,icon,id,name,path,profile,stars,summary,type,version)
    #ex util.VStranslatePathAddon("profile")
    return xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getAddonInfo(location)).decode("utf-8")

def VStranslatePath(location):
    #ex util.VStranslatePath("special://logpath/") > http://kodi.wiki/view/Special_protocol
    return xbmc.translatePath(location).decode("utf-8")

def VSlang(lang):
    #util.VSlang(30003)
    #Bug avec accent return xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getLocalizedString(lang)).decode("utf-8")
    return xbmc.translatePath(xbmcaddon.Addon('plugin.video.vstream').getLocalizedString(lang))

def VSshowYear(sUrl,start = '',end = '',endswithslash = ''):
    if start and end:
        fstart = start
        fend = end
    else:
        fstart = 1936
        fend = 2018

    lstYear = []
    lstUrl = []
    for i in reversed(xrange(fstart,fend)):
        lstYear.append(str(i))
        lstUrl.append(sUrl+str(i)+endswithslash)

    ret = VScreateDialogSelect(lstYear,sTitle='Sélectionner une année')
    if (ret > -1):
        return lstUrl[ret]
    else:
        xbmcplugin.endOfDirectory(int(sys.argv[1]),True,False,False)
        xbmc.sleep(500) #sleep obligatoire
        xbmc.executebuiltin("Action(Back)") #back evite erreur du au clic sur un dossier qui mene nulle part
