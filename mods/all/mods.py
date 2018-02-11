#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, basename, isfile
import glob


class mods:

    def __init__(self, ctx):
        self.ctx = ctx
        self.info = {
            'name'        : self.__class__.__name__,
            'version'     : [1, 0, 0],
            'description' : 'Display all available modules depending on the permissions of the user session.'
        }
        self.ctx.args.setModuleInfo(self.info)
        self.ctx.args.appendArgument(a_short='h', a_long='help', description='Show this help message')


    def callFromMain(self):
        # Check if more information about the module has been requested
        if self.ctx.args.isCalled('help'):
            self.ctx.sendToClient(self.ctx.args.getHelpMessage())

        # Normal execution
        else:
            modules = sorted(glob.glob(dirname(__file__) + '/*.py'))
            total = len(modules) - 1 # __init__.py

            if total:
                self.ctx.sendToClient('Available modules (' + str(total) + '):')

                for f in modules:
                    if isfile(f) and not f.endswith('__init__.py'):
                        # total -= 1
                        module_name = basename(f)[:-3]
                        self.ctx.sendToClient(' • ' + module_name)
                        # if total == 0:
                        #     self.ctx.sendToClient('   └── ' + module_name)
                        # else:
                        #     self.ctx.sendToClient('   ├── ' + module_name)
                        
                self.ctx.sendToClient(
                    'To know the operation of each one, write the name of '
                    'the module followed by the help argument: "-h"\n'
                    'By example: ' + self.info['name'] + ' -h'
                )