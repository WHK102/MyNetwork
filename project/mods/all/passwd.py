#!/usr/bin/env python
# -*- coding: utf-8 -*-

from internals.user import user

class passwd:

    def __init__(self, ctx):
        self.ctx = ctx
        self.info = {
            'name'        : self.__class__.__name__,
            'version'     : [1, 0, 0],
            'description' : 'Cambia la contraseña del usuario actual.'
        }

        # Argumentos
        self.ctx.args.setModuleInfo(self.info)
        self.ctx.args.appendArgument(a_short='h', a_long='help', description='Muestra este mensaje de ayuda')
        self.ctx.args.appendMainArgument(name='Nombre de usuario', description='Usuario a cambiar la contraseña')


    def callFromMain(self):

        # Verifica si se ha solicitado más información sobre el módulo
        if self.ctx.args.isCalled('help'):
            self.ctx.sendToClient(self.ctx.args.getHelpMessage())

        # Ejecución normal
        else:

            if self.ctx.auth.user.isLogged():
                if self.ctx.args.mainLength() == 0:
                    # Cambia la contraseña del usuario actual

                    self.ctx.sendToClient('Contraseña actual          : ', True)
                    current_password = self.ctx.getInput()
                    is_password = self.ctx.auth.user.isPassword(current_password)
                    if is_password:
                        new_password = self.getNewPassword()
                        if new_password:
                            self.ctx.auth.user.setNewPassword(new_password)
                            self.ctx.sendToClient('Contraseña cambiada correctamente!')
                        # else: nothing, Cancelado por el usuario

                    else:
                        self.ctx.sendToClient('! Contraseña incorrecta.')

                else:
                    # El usuario tiene permisos para realizar este cambio?
                    if self.ctx.auth.user.getGroupName() == 'admin':
                        
                        username = self.ctx.args.getMain(0).strip()
                        usr      = user(self.ctx.main_cls.basepath)
                        usr.loadByName(username)

                        # El usuario existe?
                        if usr.isLoaded():

                            # Cambia la contraseña
                            new_password = self.getNewPassword()
                            if new_password:
                                usr.setNewPassword(new_password)
                                self.ctx.sendToClient('Contraseña cambiada correctamente!')
                            # else: nothing, Cancelado por el usuario

                        else:
                            self.ctx.sendToClient('! El usuario "' + username + '" no existe.')

                    else:
                        # Solo el administrador puede cambiar contraseñas de otras personas
                        self.ctx.sendToClient('! No tienes permiso para cambiar la contraseña de otras personas.')

            else:
                self.ctx.sendToClient(
                    '! Necesitas estar autenticado para modificar una '
                    'contraseña de sesión. Para intgresar escriba "login".'
                )


    def getNewPassword(self):
        self.ctx.sendToClient('Nueva contraseña           : ', True)
        new_password_1 = self.ctx.getInput()

        # Validaciones de la contraseña
        if not new_password_1.strip():
            self.ctx.sendToClient('! La contraseña no puede quedar en blanco')
            return False

        self.ctx.sendToClient('Nueva contraseña otraves   : ', True)
        new_password_2 = self.ctx.getInput()

        if new_password_2 == new_password_1:
            return new_password_1
            
        else:
            self.ctx.sendToClient('! Ambas contraseñas no coinciden, inténtelo nuevamente.')
            return False
