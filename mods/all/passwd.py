#!/usr/bin/env python
# -*- coding: utf-8 -*-

from internals.user import user

class passwd:

    def __init__(self, ctx):
        self.ctx = ctx
        self.info = {
            'name'        : self.__class__.__name__,
            'version'     : [1, 0, 0],
            'description' : 'Change the password of the current user.'
        }

        # Arguments
        self.ctx.args.setModuleInfo(self.info)
        self.ctx.args.appendArgument(a_short='h', a_long='help', description='Show this help message')
        self.ctx.args.appendMainArgument(name='Username', description='User to change the password')


    def callFromMain(self):

        # Check if more information about the module has been requested
        if self.ctx.args.isCalled('help'):
            self.ctx.sendToClient(self.ctx.args.getHelpMessage())

        # Normal execution
        else:

            if self.ctx.auth.user.isLogged():
                if self.ctx.args.mainLength() == 0:
                    # Change the password of the current user

                    self.ctx.sendToClient('Current password : ', True)
                    current_password = self.ctx.getInput()
                    is_password = self.ctx.auth.user.isPassword(current_password)
                    if is_password:
                        new_password = self.getNewPassword()
                        if new_password:
                            self.ctx.auth.user.setNewPassword(new_password)
                            self.ctx.sendToClient('Password changed correctly!')
                        # else: nothing, Canceled by the user

                    else:
                        self.ctx.sendToClient('! Incorrect password.')

                else:
                    # The user has permission to make this change?
                    if self.ctx.auth.user.getGroupName() == 'admin':
                        
                        username = self.ctx.args.getMain(0).strip()
                        usr      = user(self.ctx.main_cls.basepath)
                        usr.loadByName(username)

                        # The user exists?
                        if usr.isLoaded():

                            # Change the password
                            new_password = self.getNewPassword()
                            if new_password:
                                usr.setNewPassword(new_password)
                                self.ctx.sendToClient('Password changed correctly!')
                            # else: nothing, Canceled by the user

                        else:
                            self.ctx.sendToClient('! The user "' + username + '" not exists.')

                    else:
                        # Solo el administrador puede cambiar contraseñas de otras personas
                        self.ctx.sendToClient('! You do not have permission to change other people\'s password.')

            else:
                self.ctx.sendToClient('! You need to be authenticated to modify a session password. To enter, type "login"')


    def getNewPassword(self):
        self.ctx.sendToClient('New password : ', True)
        new_password_1 = self.ctx.getInput()

        # Password validation
        if not new_password_1.strip():
            self.ctx.sendToClient('! The password can not be left blank')
            return False

        self.ctx.sendToClient('New password again : ', True)
        new_password_2 = self.ctx.getInput()

        if new_password_2 == new_password_1:
            return new_password_1
            
        else:
            self.ctx.sendToClient('! Both passwords do not match, try again.')
            return False
