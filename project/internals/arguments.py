#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shlex


class arguments:

    def __init__(self):
        # Argumentos obtenidos desde la llamada del módulo
        self.parsed         = []

        # Argumentos principales llamados
        self.mains          = []

        # Argumentos del módulo
        self.arguments      = []

        # Argumentos principales del módulo (que no dependen de una
        # variable de argumento, por ejemplo: useradd demo)
        self.main_arguments = []

        # Informeación del módulo que está haciendo uso de esta clase
        self.module_info    = {}


    def setModuleInfo(self, info):
        self.module_info = info

    def parseFromString(self, text):
        try:
            # Convierte los argumentos de texto plano a arreglo
            self.parsed = shlex.split(str(text))

            # Obtiene todos los argumentos principales
            self.mains  = []
            for arg in self.parsed:
                if arg[0:1] != '-':
                    self.mains.append(arg)

        except ValueError as e:
            # Comillas sin cerrar, etc
            return False

        except Exception as e:
            return False

        return True
        

    def appendArgument(self, a_short, a_long='', description=''):
        self.arguments.append({
            'short'       : a_short,
            'long'        : a_long,
            'description' : description
        })

    def appendMainArgument(self, name, description):
        self.main_arguments.append({
            'name'        : name,
            'description' : description
        })

    def getMain(self, index):
        if len(self.mains) >= index:
            return self.mains[index]
        return ''

    def mainLength(self):
        return len(self.mains)

    def getHelpMessage(self):
        arguments_to       = []
        arguments_short_to = []

        for argument_item in self.arguments:
            arguments_to.append('    -' + argument_item['short'] + ', --' + argument_item['long'] + '  ' + argument_item['description'])
            arguments_short_to.append(argument_item['short'])

        str_data = (
            'Módulo ' + self.module_info['name'] + ' v' + '.'.join(str(n) for n in self.module_info['version']) + '. '
            '' + self.module_info['description'] + '\n'
            '\n'
        )

        if arguments_to:
            str_data += (
                'Uso: ' + self.module_info['name'] + ' [-' + '] [-'.join(arguments_short_to) + ']\n'
                'Argumentos opcionales:\n'
                '' + '\n'.join(arguments_to) + ''
            )
        else:
            str_data += '  Uso: ' + self.module_info['name'] + '\n'

        str_data += '\n'

        return str_data


    def getArgumentData(self, a):
        for argument_item in self.arguments:
            if (a == argument_item['long']) or (a == argument_item['short']):
                return argument_item
        return {
            'short'       : '',
            'long'        : '',
            'description' : ''
        }


    def isCalled(self, a):
        argument_data = self.getArgumentData(a)

        if argument_data:
            for parsed_item in self.parsed:
                if (parsed_item == ('--' + argument_data['long'])) or (parsed_item == ('-' + argument_data['short'])):
                    return True
        return False
