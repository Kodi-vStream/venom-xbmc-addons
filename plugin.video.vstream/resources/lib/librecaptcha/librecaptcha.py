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
from resources.lib.comaddon import progress, VSlog
from . import cli
from .errors import GtkImportError, UserError
from .recaptcha import ReCaptcha

__version__ = "0.6.3-dev"


def _get_gui():
    try:
        from . import gui
    except GtkImportError:
        raise UserError(
            "Error: Could not load the GUI. Is PyGObject installed?\n"
            "Try (re)installing librecaptcha[gtk] with pip.\n"
            "For more details, add the --debug option.",
        )
    return gui


def has_gui():
    try:
        from . import gui  # noqa: F401
    except GtkImportError:
        return False
    return True


def get_token(api_key, site_url, user_agent, **_3to2kwargs):
    if 'debug' in _3to2kwargs:
        debug = _3to2kwargs['debug']; del _3to2kwargs['debug']
    else:
        debug = False

    if 'gui' in _3to2kwargs:
        gui = _3to2kwargs['gui']; del _3to2kwargs['gui']
    else:
        gui = False
        
    rc = ReCaptcha(api_key, site_url, user_agent, debug=debug)
    ui = (_get_gui().Gui if gui else cli.Cli)(rc)

    uvtoken = None

    def callback(token):
        get_token.uvtoken = token
        
    ui.run(callback)
    return get_token.uvtoken
