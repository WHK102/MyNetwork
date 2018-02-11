#!/usr/bin/env python
# -*- coding: utf-8 -*-


class userdel:

    def __init__(self, ctx):
        self.ctx = ctx
        self.info = {
            'name'        : self.__class__.__name__,
            'version'     : [1, 0, 0],
            'description' : 'Remove a user from the system.'
        }

        # Arguments
        self.ctx.args.setModuleInfo(self.info)
        self.ctx.args.appendArgument(a_short='h', a_long='help', description='Show this help message')
        self.ctx.args.appendMainArgument(name='Username', description='User that you want to delete')


    def callFromMain(self):

        # Check if more information about the module has been requested
        if self.ctx.args.isCalled('help') or self.ctx.args.mainLength() == 0:
            self.ctx.sendToClient(self.ctx.args.getHelpMessage())

        # Normal execution
        else:
            self.ctx.sendToClient('! Under construction.')