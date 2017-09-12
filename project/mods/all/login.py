#!/usr/bin/env python
# -*- coding: utf-8 -*-


class login:

    def __init__(self, ctx):
        self.ctx = ctx
        self.info = {
            'name'        : self.__class__.__name__,
            'version'     : [1, 0, 0],
            'description' : 'Despliega el formulario de acceso al sistema.'
        }
        self.ctx.args.setModuleInfo(self.info)
        self.ctx.args.appendArgument(a_short='h', a_long='help', description='Muestra este mensaje de ayuda')


    def callFromMain(self):
        # Verifica si se ha solicitado más información sobre el módulo
        if self.ctx.args.isCalled('help'):
            self.ctx.sendToClient(self.ctx.args.getHelpMessage())

        # Ejecución normal
        else:
            if self.ctx.auth.user.isLogged():
                self.ctx.sendToClient('Ya has ingresado!, si deseas salir escribe "logout".')

            else:
                self.ctx.sendToClient('Ingreso al sistema')

                username = ''
                password = ''

                if self.ctx.args.mainLength() == 0:
                    # Solicita el nombre del usuario
                    self.ctx.sendToClient('Nombre de usuario : ', True)
                    username = self.ctx.getInput()

                    # Solicita la contraseña
                    self.ctx.sendToClient('Contraseña        : ', True)
                    password = self.ctx.getInput()

                else:
                    # El nombre del usuario fué establecido a traves de un argumento
                    username = self.ctx.args.getMain(0).strip()

                    # Solicita la contraseña
                    self.ctx.sendToClient('Contraseña : ', True)
                    password = self.ctx.getInput()


                # Inicia sesión con las credenciales obtenidas
                success = self.ctx.auth.user.login(username, password)
                if success:
                    self.ctx.sendToClient(
                        'Bienvenido ' + username + '!, tienes nuevos módulos '
                        'disponibles, escribe "mods" para verlos.'
                    )

                else:
                    self.ctx.sendToClient('! Datos de usuario incorectos.')