# Copyright (C) 2019 nickolas360 <contact@nickolas360.com>
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


class Frontend:
    def __init__(self, recaptcha):
        self.rc = rc = recaptcha
        rc.on_token = self.__handle_token

    def __handle_token(self, token, **kwargs):
        self.on_token(token)

    def on_token(self, token: str, **kwargs):
        """Callback; set this attribute in the parent class."""
        raise NotImplementedError

    def run(self, callback=None):
        if callback:
            self.on_token = callback
        self.rc.run()
