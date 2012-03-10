#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 02.03.2012
@author: anon <index4376867067@yandex.ru>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
   
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
   
    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
    MA 02110-1301, USA.
'''

from sys import platform

class Debug():
    
    _instance = None
    
    '''
    HEADER = '\033[95m' 
    OKBLUE = '\033[94m' 
    OKGREEN = '\033[92m' 
    WARNING = '\033[93m' 
    FAIL = '\033[91m' 
    ENDC = '\033[0m' 
    '''  
    HEAD = '\033[95m'
    END = '\033[0m'
    RED = '\033[91m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            from __builtin__ import G as _G #@UnresolvedImport
            from __builtin__ import CFG as _CFG #@UnresolvedImport
            G = _G
            CFG = _CFG
            cls._instance = super(Debug, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
    def err(self,s, n = True):
        if not CFG.enable_debug: return
        s = str(s)
        if platform != 'win32':
            m = '\033[91m# [Error]: %s\033[0m' % (s) 
        else:
            m = '# [Error]: %s' % (s) 
        if n: 
            print (m)
        else: 
                print (m,)
            
    def warr(self,s, n = True):
        if not CFG.enable_debug: return
        m = '# [Warring]: ' + str(s)
        if n: 
            print (m)
        else: 
            print (m,)
            
    def info(self,s, n = True):
        if not CFG.enable_debug: return
        m = '# [Info]: ' + str(s)
        if n: 
            print (m)
        else: 
            print (m,)
            
    def debug(self,s,color=None):
        if not CFG.enable_debug: return
        s = '# [Debug]: %s' % (s)
        if platform != 'win32':
            print (color+s+self.END)
        else:
            print (s)
            