#!/usr/bin/env python
# -*- coding: utf-8 -*-

class help:

    def __init__(self, ctx):
        self.ctx = ctx
        self.info = {
            'name'        : self.__class__.__name__,
            'version'     : [1, 0, 0],
            'description' : 'Show help information'
        }
        self.ctx.args.setModuleInfo(self.info)
        self.ctx.args.appendArgument(a_short='h', a_long='help', description='Show this help message')


    def callFromMain(self):
        # Check if more information about the module has been requested
        if self.ctx.args.isCalled('help'):
            self.ctx.sendToClient(self.ctx.args.getHelpMessage())

        # Normal execution
        else:
            self.ctx.sendToClient(
                '  Use     : [module] [arguments]\n'
                '  Example : test a b c\n'
                '  To see the available modules, type: mods\n'
                '  To show the help of each module write:\n'
                '      module --help\n'
                '      module -h'
            )