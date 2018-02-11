#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from time import strftime


class __init__:

    def __init__(self, ctx):
        self.ctx = ctx
        self.info = {
            'name'        : self.__class__.__name__,
            'version'     : [7, 7, 7],
            'description' : 'Parent module of all other modules. Where is the mother?.'
        }
        self.ctx.args.setModuleInfo(self.info)
        self.ctx.args.appendArgument(a_short='h', a_long='help', description='Show this help message')


    def callFromMain(self):
        # Check if more information about the module has been requested
        if self.ctx.args.isCalled('help'):
            self.ctx.sendToClient(self.ctx.args.getHelpMessage())

        # Ejecución normal
        else:
            self.ctx.sendToClient(
                '\n'
                '_______ FAKE INIT ______\n'
                '   _  _    ___  _  _    \n'
                '  | || |  / _ \| || |   \n'
                '  | || |_| | | | || |_  \n'
                '  |_RETRO| | | |_404._| \n'
                '     | | | |_| |  | |   \n'
                '     |_|  \___/   |_|   \n'
                '________________________\n'
                '' + self.ctx.main_cls.version.humanFormat() + ' - ' + strftime("%Y-%m-%d %H:%M:%S") + '\n'
            )
