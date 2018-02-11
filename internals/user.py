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
        # Upload the user object through your username
        self.clearData()
        
        # Validate the allowed characters of the username
        username = re.sub(r'[\s\n\r]+', ' ', str(username)).strip()

        if username and username == re.sub(r'[^0-9a-zA-Z\-_]+', '', username):

            # Possible user's directory
            path = self.basepath + 'database/users/' + '/'.join([username.lower()[i:i+2] for i in xrange(0, len(username), 2)]) + '/'

            # The password file must exist, otherwise it is just the directory of a user with a longer name, for example: "of" v/s "offroad"
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

                # Returns the user's load
                return {
                    'loaded' : True,
                    'error'  : 0,
                    'data'   : self.data
                }

            # Username does not exist
            return {
                'loaded' : False,
                'error'  : -1,
                'data'   : {}
            }

        else:
            # Invalid username
            return {
                'loaded' : False,
                'error'  : -2,
                'data'   : {}
            }

    def login(self, username, password):
        # If the user is not loaded it will load it
        if not self.isLoaded():
            self.loadByName(username)

        # Was it charged?
        if self.isLoaded():

            # Does the password belong to the user?
            if self.isPassword(password):
                self.data['logged'] = True
                return True

            # The password does not match, unload the user
            self.clearData()

        return False

    def getName(self):
        # Returns the user's name
        return self.data['username']

    def getGroupName(self):
        # Returns the name of the user's group
        return self.data['groupname']

    def isLogged(self):
        # Validate if the user object has been logged
        return self.data['logged']

    def isLoaded(self):
        # Valid if the user object has been loaded
        return self.data['loaded']

    def isPassword(self, password):
        # Validate if the password belongs to the user
        if self.isLoaded():
            password = re.sub(r'[\n\r]+', '', str(password)).strip()
            return bool(self.data['password_hash'] == hashlib.sha1(self.data['password_token'] + hashlib.sha1(password).hexdigest()).hexdigest())
        return False

    def setNewPassword(self, new_password):
        # Change the user's password
        if self.isLoaded():
            new_password = re.sub(r'[\n\r]+', '', str(new_password)).strip()
            self.data['password_token'] = hashlib.sha1(str(random.randint(10, 1000)) + str(time.time()) + self.data['username']).hexdigest()
            self.data['password_hash']  = hashlib.sha1(self.data['password_token'] + hashlib.sha1(new_password).hexdigest()).hexdigest()
            self.saveInFile(self.data['homepath'] + '/password', self.data['password_token'] + ':' + self.data['password_hash'])
            return True
        return False

    def delete(self):
        # It eliminates the user almost permanently unless his files are recovered by analyzing
        # the disk of the server at a low level such as:
        # http://www.cgsecurity.org/wiki/PhotoRec_Step_By_Step
        if self.isLoaded() and self.data['homepath']:
            self.removeRecursive(self.data['homepath'])
            self.clearData()
            return True
        return False

    def logout(self):
        self.clearData()

    def clearData(self):
        # Clean and set the user's initial data
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
        # Get the contents of a file
        with open(filename) as f:
            return f.read()

    def saveInFile(self, filepath, text):
        # Save content on a file
        f = open(filepath, 'w')
        f.write(text)
        f.close()

    def removeRecursive(self, path):
        # Delete all files recursively
        if path and isdir(path):
            shutil.rmtree(path)