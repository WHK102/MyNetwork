#!/usr/bin/env python
# -*- coding: utf-8 -*-


class exit:

    def __init__(self, ctx):
        self.ctx  = ctx
        self.info = {
            'name'        : self.__class__.__name__,
            'version'     : [1, 0, 0],
            'description' : 'Finaliza la sesión activa y cierra la conexión.'
        }

        # Argumentos
        self.ctx.args.setModuleInfo(self.info)
        self.ctx.args.appendArgument(a_short='h', a_long='help', description='Muestra este mensaje de ayuda')


    def callFromMain(self):
        # Verifica si se ha solicitado más información sobre el módulo
        if self.ctx.args.isCalled('help'):
            self.ctx.sendToClient(self.ctx.args.getHelpMessage())

        # Ejecución normal
        else:
            self.ctx.exit()
