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

from __future__ import absolute_import
from .errors import UserError, UserExit
from .librecaptcha import get_token, __version__
from .user_agents import random_user_agent
import os
import re
import sys


def get_cmd():
    if not sys.argv:
        return "librecaptcha"
    if sys.argv[0].startswith("./"):
        return sys.argv[0]
    return os.path.basename(sys.argv[0])


CMD = get_cmd()
USAGE = """\
Usage:
  {0} [options] [--] <api-key> <site-url> [<user-agent>]
  {0} -h | --help | --version

Arguments:
     <api-key>  The reCAPTCHA API key to use. This is usually the value of the
                "data-sitekey" HTML attribute.

    <site-url>  The URL of the site that contains the reCAPTCHA challenge.
                Should start with http:// or https://. Everything after the
                hostname is optional. For example: https://example.com

  <user-agent>  A user-agent string. The client that will use the obtained
                reCAPTCHA token should have this user-agent string. If not
                provided, a random user-agent string will be chosen and shown.

Options:
   -g --gui  Use the GTK 3 GUI (as opposed to the CLI).
    --debug  Show debugging information while running.
  -h --help  Show this help message.
  --version  Show the program version.
""".format(CMD)


def usage(file=sys.stdout):
    print(USAGE)


def usage_error(exit=True):
    usage(sys.stderr)
    if exit:
        sys.exit(1)


class ParsedArgs(object):
    def __init__(self):
        self.parse_error = None
        self.api_key = None
        self.site_url = None
        self.user_agent = None
        self.gui = False
        self.debug = False
        self.help = False
        self.version = False


class ArgParser(object):
    def __init__(self, args):
        self.args = args
        self.index = 0
        self.positional_index = 0
        self.parsed = ParsedArgs()
        self.options_done = False
        self.end_early = False

    @property
    def arg(self):
        try:
            return self.args[self.index]
        except IndexError:
            return None

    @property
    def done(self):
        return self.end_early or self.index >= len(self.args)

    def advance(self):
        self.index += 1

    def error(self, message):
        self.parsed.parse_error = message
        self.end_early = True

    def parse_long_option(self, arg):
        body = arg[len("--"):]
        if body == "debug":
            self.parsed.debug = True
            return
        if body == "help":
            self.parsed.help = True
            self.end_early = True
            return
        if body == "version":
            self.parsed.version = True
            self.end_early = True
            return
        if body == "gui":
            self.parsed.gui = True
            return
        self.error("Unrecognized option: {}".format(arg))

    def parse_short_option_char(self, char):
        if char == "h":
            self.parsed.help = True
            self.end_early = True
            return
        if char == "g":
            self.parsed.gui = True
            return
        self.error("Unrecognized option: -{}".format(char))

    def parse_short_option(self, arg):
        body = arg[len("-"):]
        for char in body:
            self.parse_short_option_char(char)

    def try_parse_option(self):
        arg = self.arg
        if arg == "--":
            self.options_done = True
            return True
        if re.match("--[^-]", arg):
            self.parse_long_option(arg)
            return True
        if re.match("-[^-]", arg):
            self.parse_short_option(arg)
            return True
        return False

    def parse_positional(self):
        arg = self.arg
        if self.positional_index == 0:
            self.parsed.api_key = arg
            return
        if self.positional_index == 1:
            self.parsed.site_url = arg
            return
        if self.positional_index == 2:
            self.parsed.user_agent = arg
            return
        self.error("Unexpected positional argument: {}".format(arg))

    def parse_single(self):
        if not self.options_done and self.try_parse_option():
            return
        self.parse_positional()
        self.positional_index += 1

    def handle_end(self):
        if self.end_early:
            return
        if self.positional_index < 1:
            self.error("Missing positional argument: <api-key>")
            return
        if self.positional_index < 2:
            self.error("Missing positional argument: <site-url>")
            return

    def parse(self):
        while not self.done:
            self.parse_single()
            self.advance()
        self.handle_end()
        return self.parsed


GOT_TOKEN_MSG = """\
Received token. This token should usually be submitted with the form as the
value of the "g-recaptcha-response" field.
"""


def run(args):
    random_ua = False
    user_agent = args.user_agent
    if args.user_agent is None:
        random_ua = True
        user_agent = random_user_agent()
    if args.debug:
        print("User-agent string: {}".format(user_agent))

    uvtoken = get_token(args.api_key, args.site_url, user_agent, gui=args.gui, debug=args.debug)
    print(GOT_TOKEN_MSG)
    if random_ua:
        print("Note: The following user-agent string was used:")
        print(user_agent)
    print("Token:")
    print(uvtoken)


UNEXPECTED_ERR_MSG = """An unexpected error occurred. The exception traceback is shown below:"""


def run_or_exit(args):
    if args.debug:
        return run(args)
    try:
        return run(args)
    except UserExit:
        sys.exit(2)
    except UserError:
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(2)
    except Exception:
        print(UNEXPECTED_ERR_MSG)
        raise


def main():
    args = sys.argv[1:]
    parsed = ArgParser(args).parse()
    error = parsed.parse_error

    if error is not None:
        print(error)
        print("For usage information, run: {} --help".format(CMD))
        sys.exit(1)

    if parsed.help:
        usage()
        return

    if parsed.version:
        print(__version__)
        return
    run_or_exit(parsed)


if __name__ == "__main__":
    main()
