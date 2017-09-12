#!/usr/bin/env python
# -*- coding: utf-8 -*-

from auth import auth

class context:

    def __init__(self, main_cls):
        self.main_cls    = main_cls
        self.auth        = auth(self.main_cls.basepath)
        self.socket      = {}
        self.module_name = ''
        self.args        = ''

    def setSocket(self, socket_context):
        self.socket = socket_context

    def setModule(self, module_name, args):
        self.module_name = module_name
        self.args        = args

    def log(self, msg):
        return self.main_cls.log(msg, self)

    def sendToClient(self, msg, raw=False):
        return self.main_cls.sendToClient(msg, self, raw)

    def getInput(self):
        return self.main_cls.getInput(self)

    def exit(self):
        self.auth.user.logout()
        self.main_cls.endConnection(self)