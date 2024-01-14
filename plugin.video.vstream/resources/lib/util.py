# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import xbmc, isMatrix

try:
    import htmlentitydefs
    import urllib
except ImportError:
    import html.entities as htmlentitydefs
    import urllib.parse as urllib

import unicodedata
import re
import string


# function util n'utilise pas xbmc, xbmcgui, xbmcaddon ect...
class cUtil:
    # reste a transformer la class en fonction distante.
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

    def CheckOccurence(self, str1, str2):
        ignoreListe = ['3d', 'la', 'le', 'les', 'un', 'une', 'de', 'des', 'du', 'en', 'a', 'au', 'aux', 'is', 'the',
                       'in', 'of', 'and', 'mais', 'ou', 'no', 'dr', 'contre', 'dans', 'qui', 'et', 'donc', 'or', 'ni',
                       'ne', 'pas', 'car', 'je', 'tu', 'il', 'elle', 'on', 'nous', 'vous', 'ils', 'elles', 'i', 'you',
                       'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his', 'its', 'our']

        str1 = str1.replace('+', ' ').replace('%20', ' ').replace(':', ' ').replace('-', ' ')
        str2 = str2.replace(':', ' ').replace('-', ' ')

        str1 = self.CleanName(str1.replace('.', ' '))
        str2 = self.CleanName(str2.replace('.', ' '))

        i = 0
        list2 = str2.split(' ')      # Comparaison mot à mot
        for part in str1.split(' '):
            if part in ignoreListe:  # Mots à ignorer
                continue
            if len(part) == 1:       # Ignorer une seule lettre
                continue
            if part in list2:
                i += 1               # Nombre de mots correspondants
        return i

    def removeHtmlTags(self, sValue, sReplace=''):
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

    def unescape(self, text):
        def fixup(m):
            text = m.group(0)
            if text[:2] == '&#':
                # character reference
                try:
                    if text[:3] == '&#x':
                        return unichr(int(text[3:-1], 16))
                    else:
                        return unichr(int(text[2:-1]))
                except ValueError:
                    pass
                except NameError:
                    if text[:3] == '&#x':
                        return chr(int(text[3:-1], 16))
                    else:
                        return chr(int(text[2:-1]))
            else:
                # named entity
                try:
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                except KeyError:
                    pass
                except NameError:
                    text = chr(htmlentitydefs.name2codepoint[text[1:-1]])

            return text  # leave as is
        return re.sub('&#?\w+;', fixup, text)

    def titleWatched(self, title):
        if not isMatrix():
            if isinstance(title, str):
                # Must be encoded in UTF-8
                try:
                    title = title.decode('utf8')
                except AttributeError:
                    pass

            title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore')

        # cherche la saison et episode puis les balises [color]titre[/color]
        # title, saison = self.getSaisonTitre(title)
        # title, episode = self.getEpisodeTitre(title)
        # supprimer les balises
        title = re.sub(r'\[.*\]|\(.*\)', r'', str(title))
        title = title.replace('VF', '').replace('VOSTFR', '').replace('FR', '')
        # title = re.sub(r'[0-9]+?', r'', str(title))
        title = title.replace('-', ' ')  # on garde un espace pour que Orient-express ne devienne pas Orientexpress pour la recherche tmdb
        title = title.replace('Saison', '').replace('saison', '').replace('Season', '').replace('Episode', '').replace('episode', '')
        title = re.sub('[^%s]' % (string.ascii_lowercase + string.digits), ' ', title.lower())
        # title = QuotePlus(title)
        # title = title.decode('string-escape')
        return title

    def CleanName(self, name):
        if not isMatrix():
            # vire accent et '\'
            try:
                name = unicode(name, 'utf-8')  # converti en unicode pour aider aux convertions
            except:
                pass

            try:
                name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode('unicode_escape')
                name = name.encode('utf-8')  # on repasse en utf-8
            except TypeError:
                # name = unicodedata.normalize('NFKD', name.decode("utf-8")).encode('ASCII', 'ignore')
                pass

        # on cherche l'annee
        annee = ''
        m = re.search('(\([0-9]{4}\))', name)
        if m:
            annee = str(m.group(0))
            name = name.replace(annee, '')

        # vire tag
        name = re.sub('[\(\[].+?[\)\]]', '', name)
        # les apostrophes remplacer par des espaces
        name = name.replace("'", " ")
        # vire caractere special
        # name = re.sub('[^a-zA-Z0-9 ]', '', name)
        name = re.sub('[^a-zA-Z0-9 : -]', '', name)
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

    def FormatSerie(self, string):
        # vire doubles espaces
        string = re.sub(' +', ' ', string)

        # vire espace a la fin
        if string.endswith(' '):
            string = string[:-1]

        # vire espace au debut
        if string.startswith(' '):
            string = string[1:]

        SXEX = ''
        m = re.search('(?i)(\wpisode ([0-9\.\-\_]+))', string, re.UNICODE)
        if m:
            # ok y a des episodes
            string = string.replace(m.group(1), '')
            # SXEX + '%02d' % int(m.group(2))
            SXEX = m.group(2)
            if len(SXEX) < 2:
                SXEX = '0' + SXEX
            SXEX = 'E' + SXEX

            # pr les saisons
            m = re.search('(?i)(s(?:aison )*([0-9]+))', string)
            if m:
                string = string.replace(m.group(1), '')
                SXEX = 'S' + '%02d' % int(m.group(2)) + SXEX
            string = string + ' ' + SXEX

        else:
            # pas d'episode mais y a t il des saisons ?
            m = re.search('(?i)(s(?:aison )*([0-9]+))(?:$| )', string)
            if m:
                string = string.replace(m.group(1), '')
                SXEX = 'S' + '%02d' % int(m.group(2))

                string = string + ' ' + SXEX

        # reconvertion utf-8
        return string.encode('utf-8')

    def getSerieTitre(self, sTitle):
        serieTitle = re.sub(r'\[.*\]|\(.*\)', r'', sTitle)
        serieTitle = re.sub('[- –]+$', '', serieTitle)

        if '|' in serieTitle:
            serieTitle = serieTitle[:serieTitle.index('|')]

        # on repasse en utf-8
        if not isMatrix():
            return serieTitle.encode('utf-8')
        return serieTitle

    def getEpisodeTitre(self, sTitle):
        string = re.search('(?i)(e(?:[a-z]+sode\s?)*([0-9]+))', sTitle)
        if string:
            sTitle = sTitle.replace(string.group(1), '')
            self.__Episode = ('%02d' % int(string.group(2)))
            sTitle = '%s [COLOR %s]E%s[/COLOR]' % (sTitle, self.__sDecoColor, self.__Episode)
            self.addItemValues('Episode', self.__Episode)
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
# puis util.VSlog('test')
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
