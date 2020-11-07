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
from __future__ import with_statement
from __future__ import absolute_import
from resources.lib.comaddon import dialog, VSlog

from .errors import UserError
from .frontend import Frontend
from .gui import cInputWindow, cInputWindowYesNo
from threading import Thread, RLock

try:
    from Queue import Queue
except:
    from queue import Queue

import json
import time
import xbmcvfs, re

Objectif = ""
DimTab = []
STRINGS_PATH = 'special://home/userdata/addon_data/plugin.video.vstream'

class CliSolver(object):
    def __init__(self, solver):
        self.solver = solver
        self.__image_procs = []

    def show_image(self, image):
        oSolver = cInputWindow(captcha=image, msg= Objectif, dimtab = DimTab , roundnum=1)
        retArg = oSolver.get()
        if retArg == False:
            return False
        else:
            return retArg

    def run(self):
        self.solver.run()

class CliDynamicSolver(CliSolver):
    def __init__(self, solver):
        super(CliDynamicSolver, self).__init__(solver)
        solver.on_initial_image = self.handle_initial_image
        solver.on_tile_image = self.handle_tile_image
        self.image_open = False
        self.image_queue = Queue()
        self.num_pending = 0
        self.lock = RLock()

    def handle_initial_image(self, image, **kwargs):
        solver = self.solver
        indices = self.show_image(image)

        if indices == False:
            return False

        self.select_initial(indices)
        self.new_tile_loop()
        solver.finish()

    def show_imageNewTile(self, image):
        oSolver = cInputWindowYesNo(captcha=image, msg="Est-ce que cette image est en lien avec le theme ?", roundnum=1)
        retArg = oSolver.get()
        return retArg

    def new_tile_loop(self):
        while self.num_pending > 0:
            index, image = self.image_queue.get()
            self.num_pending -= 1
            accept = self.show_imageNewTile(image)[:1].lower() == "y"
            if accept:
                self.select_tile(index)

    # Called from a non-main thread.
    def handle_tile_image(self, index, image, **kwargs):
        self.image_queue.put((index, image))

    def select_initial(self, indices):
        if indices == False:
            solver = self.solver
            solver.finish()

        for i, index in enumerate(indices):
            # Avoid sending initial requests simultaneously.
            self.select_tile(index, 0.25 * i)

    def select_tile_sync(self, index):
        self.num_pending += 1
        self.solver.select_tile(index)

    def select_tile(self, index, delay=0):
        def target():
            delay and time.sleep(delay)
            with self.lock:
                self.select_tile_sync(index)
                
        myThread = Thread(target=target)
        myThread.daemon = True
        myThread.start()


class CliMultiCaptchaSolver(CliSolver):
    def __init__(self, solver):
        super(CliMultiCaptchaSolver, self).__init__(solver)
        solver.on_image = self.handle_image

    def handle_image(self, image, **kwargs):
        solver = self.solver
        indices = self.show_image(image)
        if indices == False:
            return False
        solver.select_indices(indices)

BLOCKED_MSG = """\
ERROR: Received challenge type "{}".

This is usually an indication that reCAPTCHA requests from this network are
being blocked.

Try installing Tor (the full installation, not just the browser bundle) and
running this program over Tor with the "torsocks" command.

Alternatively, try waiting a while before requesting another challenge over
this network.
"""


class Cli(Frontend):
    def __init__(self, recaptcha):
        super(Cli, self).__init__(recaptcha)
        rc = recaptcha
        rc.on_goal = self.handle_goal
        rc.on_challenge = self.handle_challenge
        rc.on_challenge_dynamic = self.challenge_dynamic
        rc.on_challenge_multicaptcha = self.challenge_multicaptcha
        rc.on_challenge_blocked = self.challenge_blocked
        rc.on_challenge_unknown = self.challenge_unknown
        self._first = True

    def handle_goal(self, goal, meta, **kwargs):
        if goal:
            return
        global Objectif, DimTab

        ID = json.dumps(meta).split(',')[0].replace('[','')

        f = xbmcvfs.File(STRINGS_PATH + "/data.txt")
        content = f.read()
        f.close()

        Objectif = re.findall('case '+ID+'.+?<strong>([^<]+)</strong>', content)

        #Récupere le theme de maniere plus précis.
        if (int(json.dumps(meta).split(',')[3]) * int(json.dumps(meta).split(',')[4]) > 9):
            Objectif = Objectif[0].encode('utf-8').decode('unicode-escape')
        else:
            Objectif = Objectif[1].encode('utf-8').decode('unicode-escape') 
                      
        DimTab = [int(json.dumps(meta).split(',')[3]),int(json.dumps(meta).split(u',')[4])]

    def handle_challenge(self, ctype, **kwargs):
        if not self._first:
            VSlog("You must solve another challenge.")
        self._first = False

    def challenge_dynamic(self, solver, **kwargs):
        CliDynamicSolver(solver).run()

    def challenge_multicaptcha(self, solver, **kwargs):
        CliMultiCaptchaSolver(solver).run()

    def challenge_blocked(self, ctype, **kwargs):
        self.raise_challenge_blocked(ctype)

    def challenge_unknown(self, ctype, **kwargs):
        self.raise_challenge_unknown(ctype)

    @classmethod
    def raise_challenge_blocked(cls, ctype):
        raise UserError(
            "Error: Unsupported challenge type: {}.\n".format(ctype) +
            "Requests are most likely being blocked; see the message above.",
        )

    @classmethod
    def raise_challenge_unknown(cls, ctype):
        raise UserError(
            "Error: Got unsupported challenge type: {}\n".format(ctype) +
            "Please file an issue if this problem persists.",
        )
