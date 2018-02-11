#!/usr/bin/env python
# -*- coding: utf-8 -*-


class logout:

    def __init__(self, ctx):
        self.ctx = ctx
        self.info = {
            'name'        : self.__class__.__name__,
            'version'     : [1, 0, 0],
            'description' : 'End the active session without disconnecting from the system.'
        }
        self.ctx.args.setModuleInfo(self.info)
        self.ctx.args.appendArgument(a_short='h', a_long='help', description='Show this help message')


    def callFromMain(self):
        # Check if more information about the module has been requested
        if self.ctx.args.isCalled('help'):
            self.ctx.sendToClient(self.ctx.args.getHelpMessage())

        # Normal execution
        else:
            if self.ctx.auth.user.isLogged():
                username = self.ctx.auth.user.getName()
                self.ctx.auth.user.logout()
                self.ctx.sendToClient('Bye ' + str(username) + '!')

            else:
                self.ctx.sendToClient('You are not authenticated.')
