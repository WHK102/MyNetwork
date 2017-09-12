#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, basename, isfile
import glob


class mods:

    def __init__(self, ctx):
        self.ctx = ctx
        self.info = {
            'name'        : self.__class__.__name__,
            'version'     : [1, 0, 0],
            'description' : 'Despliega todos los módulos disponibles dependiendo de los permisos de la sesión de usuario.'
        }
        self.ctx.args.setModuleInfo(self.info)
        self.ctx.args.appendArgument(a_short='h', a_long='help', description='Muestra este mensaje de ayuda')


    def callFromMain(self):
        # Verifica si se ha solicitado más información sobre el módulo
        if self.ctx.args.isCalled('help'):
            self.ctx.sendToClient(self.ctx.args.getHelpMessage())

        # Ejecución normal
        else:
            modules = sorted(glob.glob(dirname(__file__) + '/*.py'))
            total = len(modules) - 1 # __init__.py

            if total:
                self.ctx.sendToClient('Módulos disponibles (' + str(total) + '):')

                for f in modules:
                    if isfile(f) and not f.endswith('__init__.py'):
                        # total -= 1
                        module_name = basename(f)[:-3]
                        self.ctx.sendToClient(' • ' + module_name)
                        # if total == 0:
                        #     self.ctx.sendToClient('   └── ' + module_name)
                        # else:
                        #     self.ctx.sendToClient('   ├── ' + module_name)
                        
                self.ctx.sendToClient(
                    'Para conocer el funcionamiento de cada uno escriba '
                    'el nombre del módulo seguido por el argumento de ayuda: "-h"\n'
                    'Por ejemplo: ' + self.info['name'] + ' -h'
                )