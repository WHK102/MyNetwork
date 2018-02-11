#!/usr/bin/env python
# -*- coding: utf-8 -*-


class exit:

    def __init__(self, ctx):
        self.ctx  = ctx
        self.info = {
            'name'        : self.__class__.__name__,
            'version'     : [1, 0, 0],
            'description' : 'End the active session and close the connection.'
        }

        # Arguments
        self.ctx.args.setModuleInfo(self.info)
        self.ctx.args.appendArgument(a_short='h', a_long='help', description='Show this help message')


    def callFromMain(self):
        # Check if more information about the module has been requested
        if self.ctx.args.isCalled('help'):
            self.ctx.sendToClient(self.ctx.args.getHelpMessage())

        # Normal execution
        else:
            self.ctx.exit()
