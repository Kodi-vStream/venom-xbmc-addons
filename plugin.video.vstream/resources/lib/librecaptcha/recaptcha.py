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
from resources.lib.comaddon import progress, VSlog  # import du dialog progress
from .errors import UserError
from .extract_strings import extract_and_save

from html.parser import HTMLParser
from threading import Thread
from urllib.parse import urlparse

import requests
import base64
import json
import re
import time

BASE_URL = "https://www.google.com/recaptcha/api2/"
API_JS_URL = "https://www.google.com/recaptcha/api.js"
JS_URL_TEMPLATE = "https://www.gstatic.com/recaptcha/releases/{}/recaptcha__fr.js"

STRINGS_VERSION = "0.1.0"
STRINGS_PATH = 'special://home/userdata/addon_data/plugin.video.vstream'

DYNAMIC_SELECT_DELAY = 4.5  # seconds
FIND_GOAL_SEARCH_DISTANCE = 10


def get_full_url(url):
    return BASE_URL.rstrip("/") + "/" + url.lstrip("/")


def get_rc_site_url(url):
    parsed = urlparse(url)
    if not parsed.hostname:
        raise UserError("Error: Site URL has no hostname.")
    if not parsed.scheme:
        raise UserError("Error: Site URL has no scheme.")
    if parsed.scheme not in ["http", "https"]:
        raise UserError(
            "Error: Site URL has invalid scheme: {}".format(parsed.scheme),
        )
    port = parsed.port
    if port is None:
        port = {"http": 80, "https": 443}[parsed.scheme]
    return "{}://{}:{}".format(parsed.scheme, parsed.hostname, port)


def rc_base64(string):
    data = string
    if isinstance(string, str):
        data = string.encode()
    return base64.b64encode(data, b"-_").decode().replace("=", ".")


def load_rc_json(text):
    return json.loads(text.split("\n", 1)[1])


def get_meta(pmeta, probable_index):
    if not isinstance(pmeta, list):
        raise TypeError("pmeta is not a list: {!r}".format(pmeta))

    def matches(meta):
        return meta and isinstance(meta, list)

    if probable_index < len(pmeta):
        meta = pmeta[probable_index]
        if matches(meta):
            return meta

    for child in pmeta:
        if matches(child):
            return child
    raise RuntimeError("Could not find meta; pmeta: {!r}".format(pmeta))


def get_rresp(uvresp):
    if not isinstance(uvresp, list):
        raise TypeError("uvresp is not a list: {!r}".format(uvresp))

    for child in uvresp:
        if child and isinstance(child, list) and child[0] == "rresp":
            return child
    return None


def get_js_strings(user_agent, rc_version):
    def get_json():
        with open(STRINGS_PATH) as f:
            version, text = f.read().split("\n", 1)
            if version != "{}/{}".format(STRINGS_VERSION, rc_version):
                raise OSError("Incorrect version: {}".format(version))
            return json.loads(text)

    try:
        return get_json()
    except (OSError, ValueError, json.JSONDecodeError):
        pass

    result = extract_and_save(
        JS_URL_TEMPLATE.format(rc_version), STRINGS_PATH, STRINGS_VERSION,
        rc_version, user_agent,
    )
    return result


def get_rc_version(user_agent):
    match = re.search(r"/recaptcha/releases/(.+?)/", requests.get(
        API_JS_URL, headers={
            "User-Agent": user_agent,
        },
    ).text)
    if match is None:
        raise RuntimeError("Could not extract version from api.js.")
    return match.group(1)


class Solver:
    def __init__(self, recaptcha):
        self.rc = recaptcha

    def on_solved(response, **kwargs):
        """Callback; set this attribute in the parent class."""
        raise NotImplementedError


class HasGrid:
    @property
    def num_rows(self):
        return self.dimensions[0]

    @property
    def num_columns(self):
        return self.dimensions[1]

    @property
    def num_tiles(self):
        return self.num_rows * self.num_columns


class DynamicSolver(Solver, HasGrid):
    def __init__(self, recaptcha, pmeta):
        super().__init__(recaptcha)
        self.selections = []
        meta = get_meta(pmeta, 1)
        self.meta = meta
        self.dimensions = (meta[3], meta[4])
        self.tile_index_map = list(range(self.num_tiles))
        self.last_request_map = [0] * self.num_tiles
        self.latest_index = self.num_tiles - 1

    def on_initial_image(self, image, **kwargs):
        """Callback; set this attribute in the parent class."""
        raise NotImplementedError

    def on_tile_image(self, index, image, **kwargs):
        """Callback; set this attribute in the parent class."""
        raise NotImplementedError

    def run(self):
        self.rc.show_challenge_goal(self.meta)
        self.first_payload()

    def finish(self, block=True):
        if block:
            time.sleep(self.final_timeout)
        self.on_solved(self.selections)

    @property
    def final_timeout(self):
        return max(self.get_timeout(i) for i in range(self.num_tiles))

    def get_timeout(self, index):
        elapsed = time.monotonic() - self.last_request_map[index]
        duration = max(DYNAMIC_SELECT_DELAY - elapsed, 0)
        return duration

    def first_payload(self):
        image = self.rc.get("payload", api=False, params={
            "c": self.rc.current_token,
            "k": self.rc.api_key,
        }).url
        self.on_initial_image(image)

    def select_tile(self, index):
        def target():
            time.sleep(self.get_timeout(index))
            self.on_tile_image(index, image)
        image = self.replace_tile(index)
        Thread(target=target, daemon=True).start()

    def replace_tile(self, index):
        real_index = self.tile_index_map[int(index)]
        self.selections.append(int(real_index))
        r = self.rc.post("replaceimage", data={
            "c": self.rc.current_token,
            "ds": "[{}]".format(real_index),
        })

        self.last_request_map[index] = time.monotonic()
        data = load_rc_json(r.text)
        self.latest_index += 1
        self.tile_index_map[index] = self.latest_index

        self.rc.current_token = data[1]
        replacement_id = data[2][0]

        image = self.rc.get("payload", api=False, params={
            "c": self.rc.current_token,
            "k": self.rc.api_key,
            "id": replacement_id,
        }).url
        return image


class MultiCaptchaSolver(Solver, HasGrid):
    def __init__(self, recaptcha, pmeta):
        super().__init__(recaptcha)
        self.selection_groups = []
        self.dimensions = None
        self.challenge_type = None
        self.previous_token = None
        self.previous_id = None
        self.id = "2"
        self.metas = list(get_meta(pmeta, 5)[0])
        self.next_challenge()

    def on_image(self, image, **kwargs):
        """Callback; set this attribute in the parent class."""
        raise NotImplementedError

    def run(self):
        self.first_payload()

    def next_challenge(self):
        meta = self.metas.pop(0)
        self.dimensions = (meta[3], meta[4])
        self.rc.show_challenge_goal(meta)

    def select_indices(self, indices):
        self.selection_groups.append(list(sorted(indices)))
        VSlog("Reste a faire :" + str(len(self.metas)))
        if self.metas:
            self.replace_image()
            return
        self.on_solved(self.selection_groups)

    def first_payload(self):
        image = self.rc.get("payload", api=False, params={
            "c": self.rc.current_token,
            "k": self.rc.api_key,
        }).url
        self.on_image(image)

    def replace_image(self):
        selections = self.selection_groups[-1]
        r = self.rc.post("replaceimage", data={
            "c": self.rc.current_token,
            "ds": json.dumps([selections], separators=",:"),
        })

        data = load_rc_json(r.text)
        self.previous_token = self.rc.current_token
        self.rc.current_token = data[1]

        replacement_id = (data[2] or [None])[0]
        self.previous_id = self.id
        self.id = replacement_id
        self.next_challenge()

        image = self.rc.get("payload", api=False, params={
            "c": self.previous_token,
            "k": self.rc.api_key,
            "id": self.previous_id,
        }).url
        self.on_image(image)


class ReCaptcha:
    def __init__(self, api_key, site_url, user_agent, debug=False,
                 make_requests=True):
        self.api_key = api_key
        self.site_url = get_rc_site_url(site_url)
        self._debug = debug
        self.co = rc_base64(self.site_url)

        self.first_token = None
        self.current_token = None
        self.user_agent = user_agent

        self.js_strings = None
        self.rc_version = None
        if make_requests:
            self.rc_version = get_rc_version(self.user_agent)
            self.js_strings = get_js_strings(self.user_agent, self.rc_version)

    def on_goal(goal: str, meta, *, raw: str):
        """Callback; set this attribute in the parent class."""
        raise NotImplementedError

    def on_token(token: str, **kwargs):
        """Callback; set this attribute in the parent class."""
        raise NotImplementedError

    def on_challenge(type: str, **kwargs):
        """Callback (optional); set this attribute in the parent class."""
        pass

    def on_challenge_dynamic(solver: DynamicSolver, **kwargs):
        """Callback; set this attribute in the parent class."""
        raise NotImplementedError

    def on_challenge_multicaptcha(solver: MultiCaptchaSolver, **kwargs):
        """Callback; set this attribute in the parent class."""
        raise NotImplementedError

    def on_challenge_blocked(type: str, **kwargs):
        """Callback; set this attribute in the parent class."""
        raise NotImplementedError

    def on_challenge_unknown(type: str, **kwargs):
        """Callback; set this attribute in the parent class."""
        raise NotImplementedError

    def find_challenge_goal(self, id, raw=False):
        start = 0
        matching_strings = []

        def try_find():
            nonlocal start
            index = self.js_strings.index(id, start)
            for i in range(FIND_GOAL_SEARCH_DISTANCE):
                next_str = self.js_strings[index + i + 1]
                if re.search(r"\bselect all\b", next_str, re.I):
                    matching_strings.append((i, index, next_str))
            start = index + FIND_GOAL_SEARCH_DISTANCE + 1

        try:
            while True:
                try_find()
        except (ValueError, IndexError):
            pass

        try:
            goal = min(matching_strings)[2]
        except ValueError:
            return None, None

        raw = goal
        plain = raw.replace("<strong>", "").replace("</strong>", "")
        return raw, plain

    def show_challenge_goal(self, meta):
        raw, goal = self.find_challenge_goal(meta[0])
        self.on_goal(goal, meta, raw=raw)

    def get_headers(self, headers):
        headers = headers or {}
        if "User-Agent" not in headers:
            headers["User-Agent"] = self.user_agent
        if "Accept-Language" not in headers:
            headers["Accept-Language"] = "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3"
        return headers

    def get(self, url, *, params=None, api=True, headers=None,
            allow_errors=None, **kwargs):
        params = params or {}
        if api:
            params["k"] = self.api_key
            params["v"] = self.rc_version
            params["hl"] = "fr"
        headers = self.get_headers(headers)

        r = requests.get(
            get_full_url(url), params=params, headers=headers,
            **kwargs,
        )
        if not (allow_errors is True or r.status_code in (allow_errors or {})):
            r.raise_for_status()
        return r

    def post(self, url, *, params=None, data=None, api=True, headers=None,
             allow_errors=None, no_debug_response=False, **kwargs):
        params = params or {}
        data = data or {}
        if api:
            params["k"] = self.api_key
            data["v"] = self.rc_version
            params["hl"] = "fr"
        headers = self.get_headers(headers)

        r = requests.post(
            get_full_url(url), params=params, data=data, headers=headers,
            **kwargs,
        )
        if not (allow_errors is True or r.status_code in (allow_errors or {})):
            r.raise_for_status()
        return r

    def request_first_token(self):
        class Parser(HTMLParser):
            def __init__(p_self):
                p_self.token = None
                super().__init__()

            def handle_starttag(p_self, tag, attrs):
                attrs = dict(attrs)
                if attrs.get("id") == "recaptcha-token":
                    p_self.token = attrs.get("value")

        text = self.get("anchor", params={"co": self.co}).text
        parser = Parser()
        parser.feed(text)
        #VSlog(text)

        if not parser.token:
            raise RuntimeError(
                "Could not get first token. Response:\n{}".format(text),
            )

        self.first_token = parser.token
        self.current_token = self.first_token

    def verify(self, response):
        VSlog("reponse :" + str(response))
        response_text = json.dumps({"response": response}, separators=",:")
        response_b64 = rc_base64(response_text)

        r = self.post("userverify", data={
            "c": self.current_token,
            "response": response_b64,
        })

        uvresp = load_rc_json(r.text)
        rresp = get_rresp(uvresp)
        uvresp_token = uvresp[1]
        return (uvresp_token, rresp)

    def get_first_rresp(self):
        r = self.post("reload", data={"reason": "fi", "c": self.first_token})
        rresp = load_rc_json(r.text)
        return rresp

    def handle_solved(self, response, **kwargs):
        uvtoken, rresp = self.verify(response)
        if rresp is not None:
            self.solve_challenge(rresp)
            return
        if not uvtoken:
            raise RuntimeError("Got neither uvtoken nor new rresp.")
        self.on_token(uvtoken)

    def solve_challenge(self, rresp):
        challenge_type = rresp[5]
        pmeta = rresp[4]
        self.current_token = rresp[1]
        
        VSlog("Captcha type :" + str(challenge_type) )

        solver_class = {
            "dynamic": DynamicSolver,
            "multicaptcha": MultiCaptchaSolver,
        }.get(challenge_type)

        handler = {
            "dynamic": self.on_challenge_dynamic,
            "multicaptcha": self.on_challenge_multicaptcha,
            "default": self.on_challenge_blocked,
            "doscaptcha": self.on_challenge_blocked,
        }.get(challenge_type)

        self.on_challenge(challenge_type)
        if handler is None:
            self.on_challenge_unknown(challenge_type)
            return
        if solver_class is None:
            handler(challenge_type)
            return
        solver = solver_class(self, pmeta)
        solver.on_solved = self.handle_solved
        handler(solver)

    def run(self):
        self.request_first_token()
        rresp = self.get_first_rresp()
        self.solve_challenge(rresp)
