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
            'description' : 'Crea un nuevo usuario con los permisos básicos y sin contraseña de acceso.'
        }

        # Argumentos
        self.ctx.args.setModuleInfo(self.info)
        self.ctx.args.appendArgument(a_short='h', a_long='help', description='Muestra este mensaje de ayuda')
        self.ctx.args.appendMainArgument(name='Nombre de usuario', description='Usuario que se desea agregar')


    def callFromMain(self):
        # Verifica si se ha solicitado más información sobre el módulo
        if self.ctx.args.isCalled('help') or self.ctx.args.mainLength() == 0:
            self.ctx.sendToClient(self.ctx.args.getHelpMessage())

        # Ejecución normal
        else:
            username = self.ctx.args.getMain(0).strip()

            status_new = self.ctx.auth.new(username)
            if status_new == -1:
                self.ctx.sendToClient('! El usuario ' + username + ' ya existe.')

            elif status_new == -2:
                self.ctx.sendToClient('! El nombre de usuario "' + username + '" no puede contener carácteres inválidos.')
                self.ctx.sendToClient(
                    'Los carácteres permitidos son:\n'
                    ' • Alfanuméricos ("a" a la "z" y del 0 al 9) con y sin mayúsculas\n'
                    ' • Espacios en blanco\n'
                    ' • Guiones (- y _)\n'
                )

            elif status_new == -3:
                self.ctx.sendToClient('! Falta el nombre del usuario.')

            elif status_new == 0:
                self.ctx.sendToClient(
                    'Usuario creado: ' + username + '\n'
                    'Recuerde establecer una contraseña y sus privilegios utilizando:\n'
                    '  passwd [nombre de usuario]\n'
                    '  usermod group [nombre del grupo]'
                )

            else:
                self.ctx.sendToClient('!Se produjo un error no controlado por parte del módulo.')


    def saveInFile(self, filepath, text):
        f = open(filepath, 'w')
        f.write(text)
        f.close()

# listar usuarios
# [OK] editar usuario
# ver usuario
# [OK] crear usuario
# eliminar usuario

# useradd usergroup passwd userlist userfind userdel usershow
