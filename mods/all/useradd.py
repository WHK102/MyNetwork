#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

class useradd:

    def __init__(self, ctx):
        self.ctx = ctx
        self.info = {
            'name'        : self.__class__.__name__,
            'version'     : [1, 0, 0],
            'description' : 'Create a new user with basic permissions and no access password.'
        }

        # Arguments
        self.ctx.args.setModuleInfo(self.info)
        self.ctx.args.appendArgument(a_short='h', a_long='help', description='Show this help message')
        self.ctx.args.appendMainArgument(name='Username', description='User that you want to add')


    def callFromMain(self):
        # Check if more information about the module has been requested
        if self.ctx.args.isCalled('help') or self.ctx.args.mainLength() == 0:
            self.ctx.sendToClient(self.ctx.args.getHelpMessage())

        # Normal execution
        else:
            username = self.ctx.args.getMain(0).strip()

            status_new = self.ctx.auth.new(username)
            if status_new == -1:
                self.ctx.sendToClient('! The ' + username + ' user already exists.')

            elif status_new == -2:
                self.ctx.sendToClient('! The username "' + username + '" can not contain invalid characters.')
                self.ctx.sendToClient(
                    'The allowed characters are:\n'
                    ' • Alphanumeric ("a" a la "z" and from 0 to 9) with and without capitals\n'
                    ' • Blanks\n'
                    ' • - and _\n'
                )

            elif status_new == -3:
                self.ctx.sendToClient('! The user\'s name is missing.')

            elif status_new == 0:
                self.ctx.sendToClient(
                    'Created user: ' + username + '\n'
                    'Remember to set a password and its privileges using:\n'
                    '  passwd [username]\n'
                    '  usermod group [group name]'
                )

            else:
                self.ctx.sendToClient('! An error was not controlled by the module.')


    def saveInFile(self, filepath, text):
        f = open(filepath, 'w')
        f.write(text)
        f.close()

# TODO: Under construction
# List users
# [OK] Edit users
# Show user details
# [OK] Make new user
# Delete user
# -> useradd usergroup passwd userlist userfind userdel usershow
