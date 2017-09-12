#!/usr/bin/env python
# -*- coding: utf-8 -*-


class logout:

    def __init__(self, ctx):
        self.ctx = ctx
        self.info = {
            'name'        : self.__class__.__name__,
            'version'     : [1, 0, 0],
            'description' : 'Finaliza la sesión activa sin desconectarse del sistema.'
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
                username = self.ctx.auth.user.getName()
                self.ctx.auth.user.logout()
                self.ctx.sendToClient('Hasta luego ' + str(username) + '!')

            else:
                self.ctx.sendToClient('No estás autenticado.')
