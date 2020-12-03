# Copyright (C) 2017, 2019 nickolas360 <contact@nickolas360.com>
#
# This file is part of librecaptcha.
#
# librecaptcha is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# librecaptcha is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with librecaptcha.  If not, see <http://www.gnu.org/licenses/>.
from . import pyparsing
from resources.lib.comaddon import VSlog
import requests

import json
import xbmcvfs

def load_javascript(url, user_agent):
    r = requests.get(url, headers={
        "User-Agent": user_agent,
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
    })
    return r.text


def extract_strings(javascript):
    parsed = pyparsing.nestedExpr().parseString(javascript)
    strings = []

    def add_strings(tree, found):
        if tree is None:
            return

        if isinstance(tree, (list, tuple)):
            for child in tree:
                add_strings(child, found)

        elif isinstance(tree, dict):
            if ("type" in tree and tree["type"] == "Literal"
                and "value" in tree and isinstance(tree["value"], str)):

                found.append(tree["value"])
            for value in tree.values():
                add_strings(value, found)

        return found

    return add_strings(parsed, strings)


def extract_and_save(url, path, version, rc_version, user_agent):
    f = xbmcvfs.File(path + "/data.txt", "wb")
    js = load_javascript(url, user_agent)
    strings = extract_strings(js)
    strings_json = json.dumps(strings)
    f.write(str(js))
    f.close()
    return strings