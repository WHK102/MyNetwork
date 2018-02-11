#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shlex


class arguments:

    def __init__(self):
        # Arguments obtained from the call of the module
        self.parsed         = []

        # Main arguments called
        self.mains          = []

        # Arguments of the module
        self.arguments      = []

        # Main arguments of the module (that do not depend on an argument variable, for example: useradd demo)
        self.main_arguments = []

        # Reporting of the module that is making use of this class
        self.module_info    = {}


    def setModuleInfo(self, info):
        self.module_info = info

    def parseFromString(self, text):
        try:
            # Converts plain text arguments to array
            self.parsed = shlex.split(str(text))

            # Get all the main arguments
            self.mains  = []
            for arg in self.parsed:
                if arg[0:1] != '-':
                    self.mains.append(arg)

        except ValueError as e:
            # Quotation without closing, etc
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
            'Module ' + self.module_info['name'] + ' v' + '.'.join(str(n) for n in self.module_info['version']) + '. '
            '' + self.module_info['description'] + '\n'
            '\n'
        )

        if arguments_to:
            str_data += (
                'Use: ' + self.module_info['name'] + ' [-' + '] [-'.join(arguments_short_to) + ']\n'
                'Optional arguments:\n'
                '' + '\n'.join(arguments_to) + ''
            )
        else:
            str_data += '  Use: ' + self.module_info['name'] + '\n'

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
