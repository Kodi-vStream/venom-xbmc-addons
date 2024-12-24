# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

#
# Modified version From https://github.com/Kodi-vStream/venom-xbmc-addons
#
#
# Unpacker for Dean Edward's p.a.c.k.e.r, a part of javascript beautifier
# by Einar Lielmanis <einar@jsbeautifier.org>
#
#     written by Stefano Sanfilippo <a.little.coder@gmail.com>
#
# usage:
#
# if detect(some_string):
#     unpacked = unpack(some_string)
#

"""Unpacker for Dean Edward's p.a.c.k.e.r"""

import re

class cPacker():
    def detect(self, source):
        """Detects whether `source` is P.A.C.K.E.R. coded."""
        mystr = re.search(
            r"eval[ ]*\([ ]*function[ ]*\([ ]*p[ ]*,[ ]*a[ ]*,[ ]*c["
            r" ]*,[ ]*k[ ]*,[ ]*e[ ]*,[ ]*",
            source,
        )
        return mystr is not None

    def unpack(self, source):
        """Unpacks P.A.C.K.E.R. packed js code."""
        payload, symtab, radix, count = self._filterargs(source)

        # correction pour eviter bypass
        if (len(symtab) > count) and (count > 0):
            del symtab[count:]
        if (len(symtab) < count) and (count > 0):
            symtab.append('BUGGED')

        if count != len(symtab):
            raise UnpackingError('Malformed p.a.c.k.e.r. symtab.')

        try:
            unbase = Unbaser(radix)
        except TypeError:
            raise UnpackingError('Unknown p.a.c.k.e.r. encoding.')

        def lookup(match):
            """Look up symbols in the synthetic symtab."""
            word = match.group(0)
            return symtab[int(word)] if radix == 1 else symtab[unbase(word)] or word

        def getstring(c, a=radix):
            foo = chr(c % a + 161)
            if c < a:
                return foo
            else:
                return getstring(int(c / a), a) + foo

        payload = payload.replace("\\\\", "\\").replace("\\'", "'")
        p = re.search(r'eval\(function\(p,a,c,k,e.+?String\.fromCharCode\(([^)]+)', source)
        if p:
            pnew = re.findall(r'String\.fromCharCode\(([^)]+)', source)[0].split('+')[1] == '161'
        else:
            pnew = False

        if pnew:
            for i in range(count - 1, -1, -1):
                payload = payload.replace(getstring(i), symtab[i])
            return _replacejsstrings((self._replacestrings(payload)))
        else:
            source = re.sub(r"\b\w+\b", lookup, payload, flags=re.UNICODE)
            return self._replacestrings(source)

    def _filterargs(self, source):
        """Juice from a source file the four args needed by decoder."""

        source = source.replace(',[],',',0,').replace("\\'", "'")

        juicer = (r"}\s*\(\s*(.*?)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*\((.*?)\).split\((.*?)\)")
        args = re.search(juicer, source, re.DOTALL)
        if args:
            a = args.groups()
            try:
                return self._cleanstr(a[0]), self._cleanstr(a[3]).split(self._cleanstr(a[4])), int(a[1]), int(a[2])
            except ValueError:
                raise UnpackingError('Corrupted p.a.c.k.e.r. data.')

        juicer = (r"}\('(.*)', *(\d+), *(\d+), *'(.*)'\.split\('(.*?)'\)")
#        juicer = (r"}\(\\'(.*)', *(\d+), *(\d+), *\\'(.*)'\.split\(\\'(.*?)\\'\)")
        args = re.search(juicer, source, re.DOTALL)
        if args:
            a = args.groups()
            try:
                return a[0], a[3].split(a[4]), int(a[1]), int(a[2])
            except ValueError:
                raise UnpackingError('Corrupted p.a.c.k.e.r. data.')

        # could not find a satisfying regex
        raise UnpackingError('Could not make sense of p.a.c.k.e.r data (unexpected code structure)')

    def _replacestrings(self, source):
        """Strip string lookup table (list) and replace values in source."""
        match = re.search(r'var *(_\w+)=\["(.*?)"];', source, re.DOTALL)

        if match:
            varname, strings = match.groups()
            startpoint = len(match.group(0))
            lookup = strings.split('","')
            variable = '%s[%%d]' % varname
            for index, value in enumerate(lookup):
                if '\\x' in value:
                    value = value.replace('\\x', '')
                    value = binascii.unhexlify(value).decode('ascii')
                source = source.replace(variable % index, '"%s"' % value)
            return source[startpoint:]
        return source
        
    def _replacejsstrings(self, source):
        """Strip JS string encodings and replace values in source."""
        match = re.findall(r'\\x([0-7][0-9A-F])', source)

        if match:
            match = set(match)
            for value in match:
                source = source.replace('\\x{0}'.format(value), binascii.unhexlify(value).decode('ascii'))

        return source


def UnpackingError(Exception):
    # Badly packed source or general error.#
    print(Exception)
    pass


class Unbaser(object):
    """Functor for a given base. Will efficiently convert
    strings to natural numbers."""
    ALPHABET = {
        62: '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        95: (' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ'
             '[\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
    }

    def __init__(self, base):
        self.base = base

        # Error not possible, use 36 by defaut
        if base == 0:
            base = 36

        # If base can be handled by int() builtin, let it do it for us
        if 2 <= base <= 36:
            self.unbase = lambda string: int(string, base)
        else:
            if base < 62:
                self.ALPHABET[base] = self.ALPHABET[62][0:base]
            elif 62 < base < 95:
                self.ALPHABET[base] = self.ALPHABET[95][0:base]
            # Build conversion dictionary cache
            try:
                self.dictionary = dict((cipher, index) for index, cipher in enumerate(self.ALPHABET[base]))
            except KeyError:
                raise TypeError('Unsupported base encoding.')

            self.unbase = self._dictunbaser

    def __call__(self, string):
        return self.unbase(string)

    def _dictunbaser(self, string):
        """Decodes a  value to an integer."""
        ret = 0

        for index, cipher in enumerate(string[::-1]):
            ret += (self.base ** index) * self.dictionary[cipher]
        return ret
