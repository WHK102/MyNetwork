#!/usr/bin/env python
# -*- coding: utf-8 -*-

class help:

    def __init__(self, ctx):
        self.ctx = ctx
        self.info = {
            'name'        : self.__class__.__name__,
            'version'     : [1, 0, 0],
            'description' : 'Muestra la información de ayuda.'
        }
        self.ctx.args.setModuleInfo(self.info)
        self.ctx.args.appendArgument(a_short='h', a_long='help', description='Muestra este mensaje de ayuda')


    def callFromMain(self):
        # Verifica si se ha solicitado más información sobre el módulo
        if self.ctx.args.isCalled('help'):
            self.ctx.sendToClient(self.ctx.args.getHelpMessage())

        # Ejecución normal
        else:
            self.ctx.sendToClient(
                '  Uso     : [módulo] [argumentos]\n'
                '  Ejemplo : test a b c\n'
                '  Para ver los módulos disponibles escriba: mods\n'
                '  Para mostrar la ayuda de cada módulo escriba:\n'
                '      modulo --help\n'
                '      modulo -h'
            )