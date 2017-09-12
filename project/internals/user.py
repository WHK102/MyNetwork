#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import hashlib
import random
import time
import re
from   os.path import dirname, basename, isfile, isdir


class user(object):

    def __init__(self, basepath):
        self.basepath = basepath
        self.clearData()

    def loadByName(self, username):
        # Carga el objeto de usuario a traves de su nombre de usuario
        self.clearData()
        
        # Valida los carácteres permitidos del nombre de usuario
        username = re.sub(r'[\s\n\r]+', ' ', str(username)).strip()

        if username and username == re.sub(r'[^0-9a-zA-Z\-_]+', '', username):

            # Directorio del posible usuario
            path = self.basepath + 'database/users/' + '/'.join([username.lower()[i:i+2] for i in xrange(0, len(username), 2)]) + '/'

            # El archivo de contraseña debe existir, en caso contrario
            # es solo el directorio de un usuario con un nombre mas largo,
            # por ejemplo: "de" v/s "demo"
            if isdir(path) and isfile(path + 'password'):

                password_binary = self.getFileContents(path + '/password')
                password        = []
                if password_binary:
                    password = self.getFileContents(path + '/password').split(':')

                self.data['loaded']         = True
                self.data['homepath']       = path
                self.data['username']       = username
                self.data['groupname']      = self.getFileContents(self.data['homepath'] + '/group')
                if password:
                    self.data['password_token'] = password[0]
                    self.data['password_hash']  = password[1]
                else:
                    self.data['password_token'] = ''
                    self.data['password_hash']  = ''

                # Retorna la carga del usuario
                return {
                    'loaded' : True,
                    'error'  : 0,
                    'data'   : self.data
                }

            # El usuario no existe
            return {
                'loaded' : False,
                'error'  : -1,
                'data'   : {}
            }

        else:
            # Nombre de usuario inválido
            return {
                'loaded' : False,
                'error'  : -2,
                'data'   : {}
            }

    def login(self, username, password):
        # Si el usuario no está cargado lo cargará
        if not self.isLoaded():
            self.loadByName(username)

        # Fué cargado?
        if self.isLoaded():

            # La contraseña le pertenece?
            if self.isPassword(password):
                self.data['logged'] = True
                return True

            # La contraseña no coincide, descarga al usuario
            self.clearData()

        return False

    def getName(self):
        # Retorna el nombre del usuario
        return self.data['username']

    def getGroupName(self):
        # Retorna el nombre del grupo del usuario
        return self.data['groupname']

    def isLogged(self):
        # Valida si el objeto de usuario ha sido logueado
        return self.data['logged']

    def isLoaded(self):
        # Valida si el objeto de usuario ha sido cargado
        return self.data['loaded']

    def isPassword(self, password):
        # Valida si la contraseña pertenece al usuario
        if self.isLoaded():
            password = re.sub(r'[\n\r]+', '', str(password)).strip()
            return bool(self.data['password_hash'] == hashlib.sha1(self.data['password_token'] + hashlib.sha1(password).hexdigest()).hexdigest())
        return False

    def setNewPassword(self, new_password):
        # Cambia la contraseña del usuario
        if self.isLoaded():
            new_password = re.sub(r'[\n\r]+', '', str(new_password)).strip()
            self.data['password_token'] = hashlib.sha1(str(random.randint(10, 1000)) + str(time.time()) + self.data['username']).hexdigest()
            self.data['password_hash']  = hashlib.sha1(self.data['password_token'] + hashlib.sha1(new_password).hexdigest()).hexdigest()
            self.saveInFile(self.data['homepath'] + '/password', self.data['password_token'] + ':' + self.data['password_hash'])
            return True
        return False

    def delete(self):
        # Elimina casi permanentemente al usuario a menos que sus archivos sean
        # recuperados analizando el disco del servidor a bajo nivel como por ejemplo:
        # http://www.cgsecurity.org/wiki/PhotoRec_Step_By_Step
        if self.isLoaded() and self.data['homepath']:
            self.removeRecursive(self.data['homepath'])
            self.clearData()
            return True
        return False

    def logout(self):
        self.clearData()

    def clearData(self):
        # Limpia y establece los datos iniciales del usuario
        self.data     = {
            'logged'         : False,
            'loaded'         : False,
            'username'       : '',
            'groupname'      : 'guest',
            'homepath'       : '',
            'password_token' : '',
            'password_hash'  : ''
        }

    def getFileContents(self, filename):
        # Obtiene el contenido de un archivo
        with open(filename) as f:
            return f.read()

    def saveInFile(self, filepath, text):
        # Guarda contenido sobre un archivo
        f = open(filepath, 'w')
        f.write(text)
        f.close()

    def removeRecursive(self, path):
        # Elimina todos los archivos de manera recursiva
        if path and isdir(path):
            shutil.rmtree(path)