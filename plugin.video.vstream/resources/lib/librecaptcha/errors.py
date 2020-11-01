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


class UserError(Exception):
    """A user-facing exception for an expected error condition (e.g., bad
    user-supplied data). When librecaptcha is run as a program, exceptions of
    this type are shown without a traceback unless --debug is passed.
    """
    def __init__(self, message):
        super().__init__(message)

    @property
    def message(self):
        return self.args[0]


class UserExit(UserError):
    """When librecaptcha is run as a program, throwing this exception causes
    the program to terminate. The exception message is not shown by default.
    """
    def __init__(self, message="Program terminated."):
        super().__init__(message)


class GtkImportError(ImportError):
    pass
