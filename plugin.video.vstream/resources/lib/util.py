# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import isMatrix

try:        # python 2
    import htmlentitydefs
    import urllib
    import urlparse
except ImportError:     # python 3
    import html.entities as htmlentitydefs
    import urllib.parse as urllib
    urlparse = urllib

import unicodedata
import re
import string


# function util n'utilise pas xbmc, xbmcgui, xbmcaddon ect...
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

    # str1 : les mots à rechercher
    # str2 : Liste des mots à comparer
    # percent : pourcentage de concordance, 75% = il faut au moins 3 mots sur 4
    # retourne True si pourcentage atteint
    def CheckOccurence(self, str1, str2, percent=75):
        str2 = self.CleanName(str2)
        nbOccurence = nbWord = 0
        list2 = str2.split(' ')   # Comparaison mot à mot
        for part in str1.lower().split(' '):
            if len(part) == 1:    # Ignorer une seule lettre
                continue
            nbWord += 1           # nombre de mots au total
            if part in list2:
                nbOccurence += 1  # Nombre de mots correspondants

        if nbWord == 0:
            return False
        return 100*nbOccurence/nbWord >= percent

    def removeHtmlTags(self, sValue, sReplace=''):
        p = re.compile(r'<.*?>')
        return p.sub(sReplace, sValue)

    def formatTime(self, iSeconds):
        iSeconds = int(iSeconds)
        iMinutes = int(iSeconds / 60)
        iSeconds = iSeconds - (iMinutes * 60)
        if iSeconds < 10:
            iSeconds = '0' + str(iSeconds)

        if iMinutes < 10:
            iMinutes = '0' + str(iMinutes)

        return str(iMinutes) + ':' + str(iSeconds)

    def formatUTF8(self, text):
        # test si nécessaire de convertir
        n2 = re.sub('[^a-zA-Z0-9 ]', '', text)
        if n2 != text:
            bMatrix = isMatrix()
            if not bMatrix:
                try:
                    # converti en unicode pour aider aux convertions
                    text = text.decode('utf8', 'ignore')    
                except Exception as e:
                    pass
                
            try:
                text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore')
            except Exception as e:
                pass
            
            if bMatrix:
                try:
                    text = text.decode('utf8', 'ignore')
                except Exception as e:
                    pass
        return text

    def ASCIIDecode(self, string):
        i = 0
        l = len(string)
        ret = ''
        while i < l:
            c = string[i]
            if string[i:(i + 2)] == '\\x':
                c = chr(int(string[(i + 2):(i + 4)], 16))
                i += 3
            if string[i:(i+2)] == '\\u':
                c = chr(int(string[(i + 2):(i + 6)], 16))
                i += 5
            ret = ret + c
            i += 1
    
        return ret
    
    def unescape(self, text):
        # determine si conversion en unicode nécessaire        
        isStr = isinstance(text, str)

        def fixup(m):
            text = m.group(0)
            if text[:2] == '&#':
                # character reference
                if isStr:
                    if text[:3] == '&#x':
                        return chr(int(text[3:-1], 16))
                    else:
                        return chr(int(text[2:-1]))
                else:
                    if text[:3] == '&#x':
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
            else:
                # named entity
                if isStr:
                    text = chr(htmlentitydefs.name2codepoint[text[1:-1]])
                else:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])

            return text  # leave as is

        return re.sub('&#?\w+;', fixup, text)

    def titleWatched(self, title):

        title = title.replace('²', ' 2').replace('³', ' 3').replace('⁴', ' 4')

        title = self.formatUTF8(title)

        # cherche la saison et episode puis les balises [color]titre[/color]
        # title, saison = self.getSaisonTitre(title)
        # title, episode = self.getEpisodeTitre(title)
        # supprimer les balises

        title = title.replace('[', '').replace(']', '')
#        title = re.sub(r'\[.*\]|\(.*\)', r'', str(title))
        title = title.replace('VF', '').replace('VOSTFR', '')
        title = re.sub('(\W|_|^)FR(\W|_|$)', '', title) # FR s'il n'est pas entouré de caractere
        # title = re.sub(r'[0-9]+?', r'', str(title))
        title = title.replace('-', ' ')  # on garde un espace pour que Orient-express ne devienne pas Orientexpress pour la recherche tmdb
        title = title.replace('Saison', '').replace('saison', '').replace('Season', '').replace('Episode', '').replace('episode', '')
        title = re.sub('[^%s]' % (string.ascii_lowercase + string.digits), ' ', title.lower())
        title = re.sub(' +', ' ', title)  # vire espace double au milieu
        # title = QuotePlus(title)
        # title = title.decode('string-escape')
        return title

    def CleanName(self, name):

        name = Unquote(name)
        name = name.replace('%20', ' ')

        # on cherche l'annee
        annee = ''
        m = re.search('(\([0-9]{4}\))', name)
        if m:
            annee = str(m.group(0))
            name = name.replace(annee, '')

        # Suppression des ponctuations
        name = re.sub("[\’\'\-\–\:\+\._]", ' ', name)
        name = re.sub("[\,\&\?\!]", '', name)

        # vire tag
        name = re.sub('[\(\[].+?[\)\]]', '', name)
        name = name.replace('[', '').replace(']', '') # crochet orphelin

        # enlève les accents, si nécessaire
        name = self.formatUTF8(name)

        # tout en minuscule
        name = name.lower()
        # vire espace debut et fin
        name = name.strip()
        # vire espace double au milieu
        name = re.sub(' +', ' ', name)

        # on remet l'annee
        if annee:
            name = name + ' ' + annee

        return name

    def getSerieTitre(self, sTitle):
        serieTitle = re.sub(r'\[.*\]|\(.*\)', r'', sTitle)
        serieTitle = re.sub('[- –]+$', '', serieTitle)

        if '|' in serieTitle:
            serieTitle = serieTitle[:serieTitle.index('|')]

        return serieTitle

    def getEpisodeTitre(self, sTitle):
        string = re.search('(?i)(e(?:[a-z]+sode\s?)*([0-9]+))', sTitle)
        if string:
            sTitle = sTitle.replace(string.group(1), '')
            return sTitle, True

        return sTitle, False

    def EvalJSString(self, s):
        s = s.replace(' ', '')
        try:
            s = s.replace('!+[]', '1').replace('!![]', '1').replace('[]', '0')
            s = re.sub(r'(\([^()]+)\+\[\]\)', '(\\1)*10)', s)  # si le bloc fini par +[] >> *10
            s = re.sub(r'\[([^\]]+)\]', 'str(\\1)', s)
            if s[0] == '+':
                s = s[1:]
            val = int(eval(s))
            return val
        except:
            return 0


"""
# ***********************
# Fonctions lights
# ***********************
# Pour les avoirs
# from resources.lib import util
# puis util.Unquote('test')
"""


def Unquote(sUrl):
    return urllib.unquote(sUrl)


def Quote(sUrl):
    return urllib.quote(sUrl)


def UnquotePlus(sUrl):
    return urllib.unquote_plus(sUrl)


def QuotePlus(sUrl):
    return urllib.quote_plus(sUrl)


def QuoteSafe(sUrl):
    return urllib.quote(sUrl, safe=':/')


def urlEncode(sUrl):
    return urllib.urlencode(sUrl)


def urlHostName(sUrl):  # retourne le hostname d'une Url
    return urlparse.urlparse(sUrl).hostname
