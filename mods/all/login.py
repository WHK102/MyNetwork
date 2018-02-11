#!/usr/bin/env python
# -*- coding: utf-8 -*-


class login:

    def __init__(self, ctx):
        self.ctx = ctx
        self.info = {
            'name'        : self.__class__.__name__,
            'version'     : [1, 0, 0],
            'description' : 'Display the system access form.'
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
                self.ctx.sendToClient('You have already entered !, if you want to exit, type "logout".')

            else:
                self.ctx.sendToClient('Login to the system')

                username = ''
                password = ''

                if self.ctx.args.mainLength() == 0:
                    # Request the name of the user
                    self.ctx.sendToClient('Username : ', True)
                    username = self.ctx.getInput()

                    # Request the password of the user
                    self.ctx.sendToClient('Password : ', True)
                    password = self.ctx.getInput()

                else:
                    # The user's name was established through an argument
                    username = self.ctx.args.getMain(0).strip()

                    # Request the password
                    self.ctx.sendToClient('Password : ', True)
                    password = self.ctx.getInput()


                # Log in with the credentials obtained
                success = self.ctx.auth.user.login(username, password)
                if success:
                    self.ctx.sendToClient(
                        'Welcome ' + username + '!, you have new modules '
                        'available, write "mods" to see them.'
                    )

                else:
                    self.ctx.sendToClient('! Incorrect user data.')