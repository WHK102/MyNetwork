#!/usr/bin/env python
# -*- coding: utf-8 -*-

class version:

    def __init__(self):
        self.version = {
            'name'   : 'MyNetwork',
            'by'     : 'WHK',
            'number' : [1, 2, 1]
        }

    def humanFormat(self):
        return self.version['name'] + ' ' + '.'.join(str(n) for n in self.version['number']) + ' by ' + self.version['by']
