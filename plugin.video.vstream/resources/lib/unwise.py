# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons

"""
    urlresolver XBMC Addon
    Copyright (C) 2013 Bstrdsmkr

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Adapted for use in xbmc from:
    http://playonscripts.com/?w=files&id=34
    
    usage:
    html_with_unpacked_js = unwise_process(html_with_packed_js)

Unpacker for w.i.s.e
"""

import re


def unwise1(w):
    int1 = 0
    result = ""
    while int1 < len(w):
        result = result + chr(int(w[int1:int1 + 2], 36))
        int1 += 2
    return result


def unwise(w, i, s, e, wi, ii, si, ei):
    int1 = 0
    int2 = 0
    int3 = 0
    int4 = 0
    string1 = ""
    string2 = ""
    while True:
        if w != "":
            if int1 < wi:
                string2 = string2 + w[int1:int1 + 1]
            elif int1 < len(w):
                string1 = string1 + w[int1:int1 + 1]
            int1 += 1
        if i != "":
            if int2 < ii:
                string2 = string2 + i[int2:int2 + 1]
            elif int2 < len(i):
                string1 = string1 + i[int2:int2 + 1]
            int2 += 1
        if s != "":
            if int3 < si:
                string2 = string2 + s[int3:int3 + 1]
            elif int3 < len(s):
                string1 = string1 + s[int3:int3 + 1]
            int3 = int3 + 1
        if e != "":
            if int4 < ei:
                string2 = string2 + e[int4:int4 + 1]
            elif int4 < len(e):
                string1 = string1 + e[int4:int4 + 1]
            int4 = int4 + 1
        if len(w) + len(i) + len(s) + len(e) == len(string1) + len(string2):
            break
    int1 = 0
    int2 = 0
    result = ""
    while int1 < len(string1):
        flag = -1
        if ord(string2[int2:int2 + 1]) % 2:
            flag = 1
        result = result + chr(int(string1[int1:int1 + 2], 36) - flag)
        int2 += 1
        if int2 >= len(string2):
            int2 = 0
        int1 += 2
    return result


def unwise_process(result):
    while True:
        a = re.compile(r';?eval\s*\(\s*function\s*\(\s*w\s*,\s*i\s*,\s*s\s*,\s*e\s*\).+?[\"\']\s*\)\s*\)(?:\s*;)?').search(result)
        if not a:
            break
        a = a.group()
        tmp = re.compile(r'\}\s*\(\s*[\"\'](\w*)[\"\']\s*,\s*[\"\'](\w*)[\"\']\s*,\s*[\"\'](\w*)[\"\']\s*,\s*[\"\'](\w*)[\"\']').search(a)
        if not tmp:
            result = result.replace(a, "")
        else:
            wise = ["", "", "", ""]
            wise = tmp.groups()
            if a.find("while") == -1:
                result = result.replace(a, unwise1(wise[0]))
            else:
                c = 0
                wisestr = ["", "", "", ""]
                wiseint = [0, 0, 0, 0]
                b = re.compile(r'while(.+?)var\s*\w+\s*=\s*\w+\.join\(\s*[\"\'][\"\']\s*\)').search(a).group(1)
                for d in re.compile(r'if\s*\(\s*\w*\s*\<\s*(\d+)\)\s*\w+\.push').findall(b):
                    wisestr[c] = wise[c]
                    wiseint[c] = int(d)
                    c += 1
                result = result.replace(a, unwise(wisestr[0], wisestr[1], wisestr[2], wisestr[3], wiseint[0], wiseint[1], wiseint[2], wiseint[3]))
    return result


def resolve_var(HTML, key):  # this should probably be located elsewhere
    key = re.escape(key)
    tmp1 = HTML.replace("\r", "")
    tmp1 = tmp1.replace("\n", ";")
    tmp2 = re.compile(r'[^\w\.]' + key + '\s*=\s*([^\"\']*?)[;,]').search(tmp1)  # expect var first, movshare
    if tmp2:
        tmp2 = resolve_var(HTML, tmp2.group(1))
    else:
        tmp2 = re.compile(r'[^\w\.]' + key + '\s*=\s*[\"\'](.*?)[\"\']').search(tmp1)
        if tmp2:
            tmp2 = tmp2.group(1)
        else:
            key = key.split("\\.")
            if len(key) == 2:
                tmp2 = re.compile(r'[^\w\.]' + key[0] + '\s*=\s*\{.*[^\w\.]' + key[1] + '\s*\:\s*[\"\'](.*?)[\"\']').search(tmp1)  # for 'vars = {key: "value"}', cloudy
            if tmp2:
                tmp2 = tmp2.group(1)
            else:
                tmp2 = ""  # oops, should not happen in the variable is valid
    return tmp2
